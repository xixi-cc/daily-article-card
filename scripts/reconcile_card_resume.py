#!/usr/bin/env python3
"""Read-only campaign reconciliation. Never changes frozen inputs or claims work."""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import subprocess
from datetime import datetime, timezone


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True, timeout=30).strip()


def work_id(row):
    for value in [row.get('url', ''), *row.get('links', {}).values()]:
        match = re.search(r'(\d{4}\.\d{4,5})(?:v\d+)?', str(value))
        if match:
            return match[1]
    return 'catalog:' + row['id']


def process_snapshot(workspace):
    """Point-in-time /proc evidence; bridge servers are not presumed paper writers."""
    rows, inaccessible = [], 0
    ancestors = set()
    pid = os.getpid()
    while pid > 1 and pid not in ancestors:
        ancestors.add(pid)
        try:
            pid = int((Path('/proc') / str(pid) / 'stat').read_text().rsplit(')', 1)[1].split()[1])
        except (OSError, ValueError, IndexError):
            break
    for proc in Path('/proc').glob('[0-9]*'):
        try:
            cwd = os.readlink(proc / 'cwd')
            argv = (proc / 'cmdline').read_bytes().split(b'\0')
            command = b' '.join(argv).decode(errors='replace')
            own = int(proc.name) in ancestors
            relevant = str(workspace) in cwd or any(x in command for x in
                ('card-backfill-20260926', 'github-refresh-20260911', 'card-resume-20260930'))
            writable = []
            for fd in (proc / 'fd').iterdir():
                try:
                    target = os.readlink(fd)
                    if not target.startswith(str(workspace) + '/'):
                        continue
                    flags = re.search(r'^flags:\s+(\d+)', (proc / 'fdinfo' / fd.name).read_text(), re.M)
                    if flags and int(flags[1], 8) & os.O_ACCMODE in (os.O_WRONLY, os.O_RDWR):
                        writable.append(target)
                except OSError:
                    pass
            if not relevant and not writable:
                continue
            service = any(s in command for s in ('gpd.mcp.servers.', 'ZhihuMCP/', 'mcp-server'))
            bridge = argv[0] == b'/init'
            kind = ('audit_process' if own else 'open_write_descriptor' if writable else
                    'service' if service else 'wsl_bridge' if bridge else 'needs_inspection')
            rows.append(dict(pid=int(proc.name), cwd=cwd, executable=argv[0].decode(errors='replace'),
                             comm=(proc / 'comm').read_text().strip(), classification=kind,
                             writable_files=writable,
                             start_ticks=(proc / 'stat').read_text().rsplit(')', 1)[1].split()[19]))
        except PermissionError:
            inaccessible += 1
        except (OSError, IndexError):
            pass
    return dict(host=socket.gethostname(), processes=rows, inaccessible_processes=inaccessible,
                possible_writers=[r for r in rows if r['classification'] in ('open_write_descriptor', 'needs_inspection')],
                boundary='Point-in-time Linux /proc inspection; no guarantee about future scheduler starts or Windows bridge internals. Recheck immediately before writing.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--campaign', type=Path, required=True)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--catalog-repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--check-remote', action='store_true')
    args = parser.parse_args()
    campaign, repo, catalog_repo, out = [p.resolve() for p in (args.campaign, args.repo, args.catalog_repo, args.out)]
    if out == campaign or campaign in out.parents or out == repo or repo in out.parents:
        parser.error('Output must be outside the frozen campaign and production repository.')
    if out.exists():
        parser.error('Use a new output directory; receipts are append-only.')
    inputs = {}

    def read(path):
        path = Path(path)
        inputs[str(path)] = digest(path)
        return json.loads(path.read_text())

    stop = read(campaign / 'scope-stop-20260929-corrected.json')
    overlay = read(campaign / 'daily-missing-date-audit/parent-runtime-overlay-222.json')
    coverage = read(campaign / 'closeout-final-coverage.json')
    links = read(campaign / 'closeout-link-audit.json')
    publication = read(campaign / 'closeout-publication.json')
    catalog = read(catalog_repo / 'public/papers.json')
    states = {r['arxiv_id']: r for r in overlay['candidate_states']}
    assert len(states) == overlay['candidate_count'] == 629
    assert dict(collections.Counter(r['state'] for r in states.values())) == overlay['state_counts']
    assert len(set(stop['daily_declined_unstarted'])) == 282
    assert len(set(stop['collection_declined_unstarted'])) == 235
    by_id = collections.defaultdict(list)
    for record in catalog:
        by_id[work_id(record)].append(record)
    unlinked = {work_id(r) for r in catalog if not r.get('links', {}).get('card')}
    outside = sorted(unlinked - set(stop['collection_declined_unstarted']))
    assert set(outside) == set(links['unlinked_outside_stopped_original_queue']) and len(outside) == 7
    rows = []

    def add(aid, program, cohort, position=None):
        folder = 'curated_cards' if program == 'Daily' else 'collection_cards'
        card = repo / 'data' / folder / (aid + '.json')
        other = repo / 'data' / ('collection_cards' if program == 'Daily' else 'curated_cards') / (aid + '.json')
        row = dict(key=program + ':' + aid, arxiv_id=aid, program=program, cohort=cohort,
                   source_position=position, eligible_to_claim=False,
                   installed=card.is_file(), other_program_installed=other.is_file(),
                   catalog_records=[dict(id=r['id'], title=r['title'], url=r['url'], card_url=r.get('links', {}).get('card')) for r in by_id[aid]])
        if program == 'Daily':
            state = states[aid]
            row.update(previous_state=state['state'], queue_position=state.get('queue_position'),
                       listing_dates=state.get('listing_dates'), unit=state.get('unit'))
        row['next_action'] = 'retain_stopped_until_batch_resume'
        if cohort == 'outside_original_collection_queue':
            row['next_action'] = 'resolve_catalog_identity_and_existing_evidence_before_intake'
        rows.append(row)
        return row

    for program, key in [('Daily', 'daily_declined_unstarted'), ('Collection', 'collection_declined_unstarted')]:
        for index, aid in enumerate(stop[key]):
            row = add(aid, program, 'stopped_unstarted', index)
            if program == 'Daily':
                assert states[aid]['state'] == 'stopped_unstarted_by_user'
    for aid in outside:
        add(aid, 'Collection', 'outside_original_collection_queue')
    row = add('2609.00292', 'Daily', 'started_metadata_only')
    unit = Path(row['unit'])
    row['pdfs_present'] = [str(p) for p in unit.rglob('*.pdf')]
    row['next_action'] = 'resume_fulltext_intake_only_after_batch_resume'
    for aid in ['2609.12594', '2608.27828']:
        row = add(aid, 'Daily', 'accepted_staged_not_installed')
        state = states[aid]
        staged, manifest = Path(state['staged_card']), Path(state['manifest_path'])
        acceptance = read(state['parent_acceptance'])
        packet = read(manifest)
        assert digest(manifest) == state['manifest_sha256']
        verified = []
        packets = [(manifest, packet)]
        if acceptance.get('original_manifest_path'):
            original = Path(acceptance['original_manifest_path'])
            packets.append((original, read(original)))
            assert digest(original) == acceptance['original_manifest_sha256']
        for manifest_path, manifest_data in packets:
            for item in manifest_data['records']:
                path = (manifest_path.parent / item['relative_path']).resolve()
                assert manifest_path.parent.resolve() in path.parents, path
                actual = digest(path)
                assert actual == item['sha256'] and path.stat().st_size == item['bytes'], path
                inputs[str(path)] = actual
                verified.append(str(path))
        inputs[str(staged)] = digest(staged)
        if state.get('staged_card_sha256'):
            assert digest(staged) == state['staged_card_sha256']
        row.update(staged_card=str(staged), staged_sha256=digest(staged), manifest=str(manifest),
                   manifest_records_verified=len(verified), acceptance=state['parent_acceptance'],
                   staged_matches_accepted_card=digest(staged) == digest(manifest.parent/'worker-cards'/f'{aid}.json'),
                   accepted_grade=acceptance['formal_grade'],
                   next_action='delivery_preflight_on_existing_draft_then_review_only_new_deltas')
        assert not row['installed']
    assert len(rows) == 527 and len({r['key'] for r in rows}) == 527
    broken = []
    for record in catalog:
        url = record.get('links', {}).get('card')
        if url:
            match = re.search(r'/(collection-papers|papers)/([^/]+)/?', url)
            if not match or not (repo / 'site' / match[1] / match[2] / 'index.html').is_file():
                broken.append(record['id'])
    assert not broken, broken
    production = {}
    for name, root, branch in [('cards', repo, 'master'), ('catalog', catalog_repo, 'main')]:
        head = git(root, 'rev-parse', 'HEAD')
        item = dict(path=str(root), head=head, local_branch=git(root, 'branch', '--show-current'),
                    public_branch=branch, origin=git(root, 'remote', 'get-url', 'origin'),
                    tracked_status=git(root, 'status', '--porcelain', '-uno'))
        if args.check_remote:
            remote = git(root, 'ls-remote', 'origin', 'refs/heads/' + branch).split()[0]
            item['remote_head'] = remote
            item['head_matches_remote'] = head == remote
            if head != remote:
                item['remote_delta_paths'] = git(root, 'diff', '--name-only', head, remote).splitlines()
                item['remote_is_descendant'] = subprocess.run(['git', '-C', str(root), 'merge-base', '--is-ancestor', head, remote]).returncode == 0
                item['release_gate'] = 'Reconcile remote delta before any future publish; do not reset/force-push.'
        production[name] = item
    processes = process_snapshot(campaign.parents[1])
    assert all(digest(p) == h for p, h in inputs.items()), 'Inputs changed during audit'
    out.mkdir(parents=True)
    report = dict(schema_version=1, created_at_utc=datetime.now(timezone.utc).isoformat(),
                  scope='reconciliation_only_no_intake_or_publication', production=production,
                  counts=dict(rows=len(rows), stopped=517, Daily_stopped=282, Collection_stopped=235,
                              outside=7, metadata_only=1, staged=2,
                              unique_works=len({r['arxiv_id'] for r in rows}),
                              Daily_cards=len(list((repo/'data/curated_cards').glob('*.json'))),
                              Collection_cards=len(list((repo/'data/collection_cards').glob('*.json'))),
                              catalog=len(catalog), linked=len(catalog)-len(unlinked), unlinked=len(unlinked)),
                  frozen_coverage=coverage['online_after'], processes=processes, rows=rows,
                  report_dates_still_missing=coverage['remaining_gaps']['missing_in_obtained_intake_days'],
                  source_hashes=inputs, source_inputs_unchanged=True)
    (out/'resume-ledger.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    (out/'production-lock.json').write_text(json.dumps(dict(production=production, note='Path/baseline pin, not a held process lock. Recheck writers before execution.'), indent=2)+'\n')
    (out/'staged-delivery.json').write_text(json.dumps(dict(cards=[dict(id=r['arxiv_id'], program=r['program'], card=r['staged_card']) for r in rows if 'staged_card' in r]), indent=2)+'\n')
    print(json.dumps(dict(output=str(out), counts=report['counts'], possible_writers=len(processes['possible_writers'])), ensure_ascii=False))


if __name__ == '__main__':
    main()
