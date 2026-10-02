#!/usr/bin/env python3
"""Append-only controller ledger and measured stage usage; never dispatch/publish.

Runtime state belongs outside the repository. Only the controller writes events.
This journal records supplied evidence; it does not certify scientific quality.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
import sqlite3
from pathlib import Path

from reconcile_card_resume import digest
import card_registry as registry

STAGES = ['registered', 'claimed', 'pdf_frozen', 'fulltext_read', 'evidence_verified',
          'draft', 'reviewed', 'sealed', 'published']
TERMINAL = {'not_selected', 'source_exception', 'unable_to_finish', 'stopped_unstarted'}
ACTIVE = set(STAGES[1:-2])
MEASUREMENTS = {'extraction', 'reading', 'evidence', 'writing', 'review', 'validation', 'publication'}
TOKENS = ('input_tokens', 'cached_input_tokens', 'output_tokens')


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def stamp():
    return datetime.now(timezone.utc).isoformat()


def instant(value):
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if dt.tzinfo is None:
        raise ValueError('timestamps require a timezone')
    return dt.timestamp()


def refs(items):
    if not isinstance(items, dict) or not 1 <= len(items) <= 8:
        raise ValueError('need 1..8 artifact pointers; use a manifest for larger evidence sets')
    result = {}
    for name, path in items.items():
        p = Path(path).resolve()
        result[name] = {'path': str(p), 'sha256': digest(p)}
    return result


def verify_refs(items):
    for ref in items.values():
        if digest(ref['path']) != ref['sha256']:
            raise ValueError('changed evidence: ' + ref['path'])


def replay(path):
    events, previous = [], None
    if not path.exists():
        return events
    text = path.read_text()
    if text and not text.endswith('\n'):
        raise ValueError('incomplete journal tail; preserve and recover before appending')
    for line in text.splitlines():
        event = json.loads(line)
        checksum = event.pop('sha256')
        if (event['seq'] != len(events) + 1 or event['previous'] != previous or
                hashlib.sha256(canonical(event).encode()).hexdigest() != checksum):
            raise ValueError('journal checksum/sequence mismatch')
        event['sha256'] = checksum
        events.append(event)
        previous = checksum
    return events


def state(events):
    if not events or events[0]['kind'] != 'init':
        raise ValueError('initialize the journal first')
    rows = {r['key']: dict(r) for r in events[0]['data']['rows']}
    for event in events[1:]:
        if event['kind'] == 'transition':
            rows[event['data']['key']]['stage'] = event['data']['stage']
    return rows


@contextmanager
def locked(directory):
    directory = Path(directory).resolve()
    repo = Path(__file__).resolve().parents[1]
    if directory == repo or repo in directory.parents:
        raise ValueError('runtime ledger must be outside production repository')
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / 'writer.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield directory / 'events.jsonl'


def append(path, events, kind, data):
    event = dict(seq=len(events) + 1, previous=events[-1]['sha256'] if events else None,
                 recorded_at=stamp(), kind=kind, data=data)
    event['sha256'] = hashlib.sha256(canonical(event).encode()).hexdigest()
    with path.open('a') as stream:
        stream.write(canonical(event) + '\n')
        stream.flush()
        os.fsync(stream.fileno())
    directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)
    return event


def initialize(directory, roster):
    """Import an explicit immutable roster; defaults prohibit new intake."""
    rows = roster['rows']
    keys = [r['key'] for r in rows]
    if not rows or len(keys) != len(set(keys)):
        raise ValueError('roster requires unique program:paper keys')
    policy = roster.get('policy', {})
    if set(policy) - {'max_active', 'max_batch'}:
        raise ValueError('unknown policy; intake authorization is deliberately unsupported')
    policy = dict(max_active=policy.get('max_active', 2), max_batch=policy.get('max_batch', 10))
    if any(type(policy[k]) is not int or not 1 <= policy[k] <= bound
           for k, bound in [('max_active', 2), ('max_batch', 10)]):
        raise ValueError('max_active must be 1..2 and max_batch 1..10')
    normalized = []
    for row in rows:
        if row['key'].split(':', 1)[0] not in {'Daily', 'Collection'} or ':' not in row['key']:
            raise ValueError('invalid program:paper key')
        started = row.get('already_started')
        if type(started) is not bool:
            raise ValueError('already_started must be explicit')
        stage = row.get('stage', 'registered' if started else 'stopped_unstarted')
        if stage not in set(STAGES) | TERMINAL or (not started and stage != 'stopped_unstarted'):
            raise ValueError('unstarted papers must remain stopped')
        evidence = refs(row['artifacts']) if row.get('artifacts') else {}
        if started and not evidence:
            raise ValueError('started items need an existing checkpoint/evidence reference')
        normalized.append(dict(key=row['key'], already_started=started, stage=stage,
                               source_version=row.get('source_version'), title=row.get('title', ''), artifacts=evidence))
    if sum(r['stage'] in ACTIVE for r in normalized) > policy['max_active']:
        raise ValueError('import exceeds active worker limit; reconcile ownership first')
    with locked(directory) as path:
        if path.exists():
            raise ValueError('journal already exists; never reinitialize historical state')
        return append(path, [], 'init', dict(rows=normalized, policy=policy,
                                            intake='closed', registry=str(Path(roster['registry']).resolve()) if roster.get('registry') else None,
                                            authority=refs(roster['authority'])))


def record(directory, kind, data):
    with locked(directory) as path:
        events = replay(path)
        rows = state(events)
        verify_refs(events[0]['data']['authority'])
        if events[0]['data'].get('registry'):
            sync_registry(directory)
        allowed = ({'key', 'stage', 'note', 'artifacts'} if kind == 'transition' else
                   {'key', 'stage', 'measurement_id', 'started_at', 'ended_at', 'usage', 'artifacts'})
        if set(data) - allowed:
            raise ValueError('unexpected fields; keep full evidence outside small events')
        key = data['key']
        if key not in rows:
            raise ValueError('unknown paper; roster expansion is unsupported')
        row = rows[key]
        if not row['already_started']:
            raise ValueError('unstarted paper is stopped by scope')
        if kind == 'transition':
            target, current = data['stage'], row['stage']
            if target == 'claimed' and events[0]['data'].get('registry'):
                registry.guard_claim(events[0]['data']['registry'], key, row['source_version'], Path(__file__).resolve().parents[1])
            if current in TERMINAL or current == 'published':
                raise ValueError('terminal paper cannot be reopened')
            if target not in TERMINAL and (current not in STAGES or target not in STAGES or
                                           STAGES.index(target) != STAGES.index(current) + 1):
                raise ValueError('invalid or repeated stage transition')
            if target == 'stopped_unstarted':
                raise ValueError('started paper cannot be classified as unstarted')
            if target in ACTIVE and current not in ACTIVE:
                if any(k != key and k.split(':', 1)[1] == key.split(':', 1)[1] and r['stage'] in ACTIVE
                       for k, r in rows.items()):
                    raise ValueError('same paper already active in another provenance stream')
                if sum(r['stage'] in ACTIVE for r in rows.values()) >= events[0]['data']['policy']['max_active']:
                    raise ValueError('active worker limit reached')
            if not data.get('note', '').strip() or len(data['note']) > 400:
                raise ValueError('transition needs a concise conclusion (1..400 characters)')
            if not data.get('artifacts'):
                raise ValueError('transition requires durable evidence/receipt pointers')
            data = dict(data, artifacts=refs(data['artifacts']))
        elif kind == 'measurement':
            if data['stage'] not in MEASUREMENTS:
                raise ValueError('unknown measurement stage')
            start, end = instant(data['started_at']), instant(data['ended_at'])
            if end < start:
                raise ValueError('negative measured duration')
            if not data.get('measurement_id') or len(data['measurement_id']) > 120:
                raise ValueError('measurement_id is required (max 120 characters)')
            if any(e['kind'] == kind and e['data']['measurement_id'] == data['measurement_id'] for e in events):
                raise ValueError('measurement already recorded; do not double-count')
            usage = data.get('usage', {})
            if set(usage) - set(TOKENS):
                raise ValueError('usage accepts input/cached input/output only')
            usage = {k: usage.get(k) for k in TOKENS}
            if any(v is not None and (type(v) is not int or v < 0) for v in usage.values()):
                raise ValueError('token values must be nonnegative integers or null')
            if usage['cached_input_tokens'] is not None and (usage['input_tokens'] is None or
                    usage['cached_input_tokens'] > usage['input_tokens']):
                raise ValueError('cached input must be a subset of total input')
            # Usage must be an interval delta from a runtime receipt, never repeated cumulative counters.
            if not data.get('artifacts'):
                raise ValueError('measurement needs timing/usage source receipt')
            data = dict(data, usage=usage, artifacts=refs(data['artifacts']),
                        elapsed_seconds=end-start)
        else:
            raise ValueError('unsupported event kind')
        event = append(path, events, kind, data)
        if events[0]['data'].get('registry'):
            # Journal is authoritative; sync-registry idempotently repairs a failed second write.
            try:
                sync_registry(directory)
            except (ValueError, OSError, sqlite3.Error) as exc:
                raise ValueError('journal event saved; registry sync failed; run sync-registry before continuing: '+str(exc)) from exc
        return event


def sync_registry(directory):
    events = replay(Path(directory)/'events.jsonl')
    rows = state(events)
    root = events[0]['data'].get('registry')
    if not root:
        raise ValueError('legacy journal has no registry binding; import decisions with registry record/accept')
    records = []
    statuses = {'not_selected':'not_selected', 'source_exception':'source_exception',
                'unable_to_finish':'incomplete', 'claimed':'in_progress',
                'draft':'staged_unpublished', 'sealed':'staged_unpublished', 'published':'has_card'}
    for event in events[1:]:
        data = event['data']
        if event['kind'] != 'transition' or data['stage'] not in statuses:
            continue
        program, aid = data['key'].split(':',1)
        row = rows[data['key']]
        records.append(dict(event_id='workflow:'+event['sha256'], paper_id=aid, program=program,
                            status=statuses[data['stage']], reason=data['note'],
                            title=row.get('title',''), source_version=row.get('source_version'),
                            evidence=data['artifacts'], journal=str((Path(directory)/'events.jsonl').resolve())))
    return dict(registry=root, added=registry.record_many(root, records))


def union_seconds(intervals):
    total, right = 0, None
    for start, end in sorted(intervals):
        total += max(0, end - max(start, right if right is not None else start))
        right = max(end, right if right is not None else end)
    return total


def report(directory, key=None):
    events = replay(Path(directory) / 'events.jsonl')
    rows = state(events)
    if key is not None and key not in rows:
        raise ValueError('unknown paper')
    stages = defaultdict(list)
    for event in events:
        if event['kind'] == 'measurement' and (key is None or event['data']['key'] == key):
            stages[event['data']['stage']].append(event['data'])
    totals = {}
    for stage, measurements in stages.items():
        known = {}
        for token in TOKENS:
            values = [m['usage'][token] for m in measurements]
            known[token] = dict(known_sum=sum(v for v in values if v is not None),
                                unknown_measurements=sum(v is None for v in values))
        effective = [m['usage']['input_tokens'] - m['usage']['cached_input_tokens'] + m['usage']['output_tokens']
                     for m in measurements if all(m['usage'][k] is not None for k in TOKENS)]
        totals[stage] = dict(measurements=len(measurements),
                            elapsed_seconds_sum=sum(m['elapsed_seconds'] for m in measurements),
                            covered_wall_seconds=union_seconds([(instant(m['started_at']), instant(m['ended_at']))
                                                                for m in measurements]),
                            usage=known, uncached_input_plus_output_known_sum=sum(effective),
                            effective_usage_unknown_measurements=len(measurements)-len(effective))
    return dict(schema_version=1, journal_head=events[-1]['sha256'], event_count=len(events),
                intake='closed', key=key, counts=dict(Counter(r['stage'] for k, r in rows.items() if key is None or k == key)),
                stages=totals, boundary='Measured interval deltas only, not labor hours, Goal counters, account quota or scientific certification.')


def audit(directory):
    events = replay(Path(directory) / 'events.jsonl')
    state(events)
    verify_refs(events[0]['data']['authority'])
    for row in events[0]['data']['rows']:
        verify_refs(row['artifacts'])
    for event in events[1:]:
        verify_refs(event['data']['artifacts'])
    return dict(journal_head=events[-1]['sha256'], event_count=len(events), artifacts_unchanged=True,
                boundary='Integrity only; independent scientific review remains required.')


def batch(directory):
    events = replay(Path(directory) / 'events.jsonl')
    rows = state(events)
    limit = events[0]['data']['policy']['max_batch']
    verify_refs(events[0]['data']['authority'])
    ready = [key for key, row in rows.items() if row['stage'] == 'sealed'][:limit]
    for key in ready:
        latest = next((e for e in reversed(events) if e['kind'] == 'transition' and e['data']['key'] == key), None)
        verify_refs(latest['data']['artifacts'] if latest else rows[key]['artifacts'])
    return dict(journal_head=events[-1]['sha256'], keys=ready, max_batch=limit,
                action='Proposal only: parent must verify scientific acceptance, delivery, build, render and release receipts.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['init', 'transition', 'measurement', 'report', 'batch', 'audit', 'sync-registry'])
    parser.add_argument('--state', type=Path, required=True)
    parser.add_argument('--input', type=Path)
    parser.add_argument('--registry', type=Path, help='Private disposition registry for a new journal')
    parser.add_argument('--out', type=Path)
    parser.add_argument('--key', help='Filter report measurements to one program:paper')
    args = parser.parse_args()
    try:
        if args.out and args.out.exists():
            raise ValueError('output exists; choose a new snapshot path before mutation')
        if args.key and args.command != 'report':
            raise ValueError('--key is supported only by report')
        if args.command in {'report', 'batch', 'audit', 'sync-registry'}:
            result = (report(args.state, args.key) if args.command == 'report' else
                      batch(args.state) if args.command == 'batch' else
                      audit(args.state) if args.command == 'audit' else sync_registry(args.state))
        else:
            if not args.input:
                parser.error('--input is required')
            data = json.loads(args.input.read_text())
            if args.command == 'init':
                data['registry'] = str(args.registry or data.get('registry') or registry.default_registry())
                registry.current(data['registry'])  # missing registry fails closed before creation
                result = initialize(args.state, data)
            else:
                result = record(args.state, args.command, data)
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            with args.out.open('x') as stream:
                stream.write(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps(result if args.command in {'report', 'batch', 'audit', 'sync-registry'} else
                         dict(seq=result['seq'], sha256=result['sha256']), ensure_ascii=False))
    except (ValueError, KeyError, TypeError, OSError, sqlite3.Error) as exc:
        parser.exit(1, str(exc) + '\n')


if __name__ == '__main__':
    main()
