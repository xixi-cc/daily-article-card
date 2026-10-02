#!/usr/bin/env python3
"""Private, append-only paper disposition registry; no intake or publication."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import unicodedata

from reconcile_card_resume import digest

STATUSES = {'not_selected', 'source_exception', 'incomplete', 'stopped_unstarted',
            'staged_unpublished', 'publication_blocked', 'has_card', 'in_progress', 'needs_review'}
NO_CARD = STATUSES - {'has_card'}


def default_registry():
    for root in Path(__file__).resolve().parents:
        if (root/'sites/daily-paper-card').is_dir():
            return root/'local-state/paper-card-registry'
    raise ValueError('cannot locate website workspace; supply an explicit registry')


def identity(value):
    raw = str(value).strip()
    doi = re.search(r'(?:doi:|https?://(?:dx\.)?doi\.org/)?(10\.\d{4,9}/[^\s]+)', raw, re.I)
    if doi:
        return 'doi:'+doi[1].lower(), None
    legacy = re.fullmatch(r'([a-z-]+(?:\.[A-Z]{2})?)-(\d{7})', raw)
    if legacy:
        return legacy[1]+'/'+legacy[2], None
    if re.fullmatch(r'(?:record-[a-f0-9]+|doi-[a-zA-Z0-9._-]+)', raw):
        return raw.lower(), None
    match = re.search(r'(\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?/\d{7})(v\d+)?', str(value))
    if not match:
        raise ValueError('an arXiv ID, DOI, or stable Collection record ID is required')
    return match[1], match[2]


def title_key(value):
    return ''.join(c for c in unicodedata.normalize('NFKC', value).casefold() if c.isalnum())


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def connect(root, create=False):
    root = Path(root).resolve()
    # Runtime records must never leak into any Git checkout.
    if any((p/'.git').exists() for p in [root, *root.parents]):
        raise ValueError('registry must be outside Git repositories')
    db = root/'registry.sqlite3'
    if not create and not db.is_file():
        raise ValueError('registry missing; refresh dispositions before claiming papers')
    if create:
        root.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db), timeout=10)
    if create:
        conn.execute('PRAGMA journal_mode=WAL')
        conn.execute('PRAGMA synchronous=FULL')
        conn.execute('CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY, event_id TEXT UNIQUE NOT NULL, payload TEXT NOT NULL, sha256 TEXT NOT NULL)')
        conn.execute("CREATE TRIGGER IF NOT EXISTS immutable_update BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT, 'events are immutable'); END")
        conn.execute("CREATE TRIGGER IF NOT EXISTS immutable_delete BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT, 'events are immutable'); END")
        conn.commit()
    else:
        conn.execute('PRAGMA query_only=ON')
    return conn


def record_many(root, records):
    with connect(root, create=True) as conn:
        added = 0
        for record in records:
            r = dict(record)
            r['paper_id'], embedded_version = identity(r['paper_id'])
            r.setdefault('source_version', embedded_version)
            if r['program'] not in {'Daily', 'Collection'} or r['status'] not in STATUSES:
                raise ValueError('invalid program/status')
            if not isinstance(r.get('reason'), str) or not r['reason'].strip():
                raise ValueError('explicit disposition reason required')
            if not r.get('evidence'):
                raise ValueError('evidence references required')
            r.setdefault('title', '')
            r.setdefault('reopen_condition', 'Explicit authorized review of changed version, evidence or scope; reuse existing evidence first.')
            payload = encode(r)
            checksum = hashlib.sha256(payload.encode()).hexdigest()
            event_id = r.get('event_id', checksum)
            previous = conn.execute('SELECT sha256 FROM events WHERE event_id=?', (event_id,)).fetchone()
            if previous:
                if previous[0] != checksum:
                    raise ValueError('event ID reused with different content')
                continue
            for ref in r['evidence'].values():
                if digest(ref['path']) != ref['sha256']:
                    raise ValueError('changed source evidence: ' + ref['path'])
            conn.execute('INSERT INTO events(event_id,payload,sha256) VALUES (?,?,?)', (event_id,payload,checksum))
            added += 1
    return added


def current(root):
    latest = {}
    with connect(root) as conn:
        for seq, payload, checksum in conn.execute('SELECT seq,payload,sha256 FROM events ORDER BY seq'):
            if hashlib.sha256(payload.encode()).hexdigest() != checksum:
                raise ValueError('registry payload checksum mismatch')
            row = json.loads(payload)
            latest[(row['program'],row['paper_id'])] = dict(row, registry_seq=seq)
    return list(latest.values())


def lookup(root, value=None, program=None, version=None, title=None, repo=None):
    rows = current(root)
    aid, detected = identity(value) if value else (None, None)
    version = version or detected
    matches = [r for r in rows if r['paper_id'] == aid or aid in r.get('aliases', [])] if aid else [r for r in rows if title and title_key(r['title']) == title_key(title)]
    ids = {r['paper_id'] for r in matches}
    if len(ids) > 1:
        return dict(action='identity_conflict', matches=matches, boundary='Title match is ambiguous; resolve identity manually.')
    if ids:
        aid = next(iter(ids))
    installed = []
    if repo and aid:
        for p, folder in [('Daily','curated_cards'), ('Collection','collection_cards')]:
            path = Path(repo)/'data'/folder/(aid+'.json') if '/' not in aid else Path(repo)/'__no_direct_doi_filename__'
            if path.is_file():
                installed.append(dict(program=p, card=str(path.resolve()), sha256=digest(path)))
    own = next((r for r in matches if r['program'] == program), None)
    if any(r['program'] == program for r in installed) or own and own['status'] == 'has_card':
        action = 'reuse_existing_card'
    elif own:
        if own['status'] == 'stopped_unstarted':
            action = 'scope_stopped'
        elif own['status'] in {'staged_unpublished','publication_blocked','in_progress','incomplete'}:
            action = 'resume_existing_evidence_only'
        elif version and own['source_version'] and version != own['source_version']:
            action = 'changed_version_review_required'
        else:
            action = 'skip_previous_disposition'
    elif matches or installed:
        action = 'review_other_program_evidence'
    else:
        action = 'not_recorded'
    return dict(paper_id=aid, program=program, requested_version=version, action=action,
                matches=matches, installed=installed,
                boundary='Lookup does not authorize intake, invalidate a disposition, or confer Daily eligibility. Unknown versions require manual comparison.')


def guard_claim(root, key, version=None, repo=None):
    program, aid = key.split(':',1)
    result = lookup(root, aid, program, version, repo=repo)
    if result['action'] not in {'not_recorded','review_other_program_evidence'}:
        raise ValueError('registry blocks duplicate/reopened claim: ' + result['action'])
    if any(r['status'] in {'source_exception','needs_review','in_progress'} for r in result['matches']):
        raise ValueError('other program has unresolved evidence/ownership; review existing unit first')
    return result


def accept_decision(root, decision_path):
    path = Path(decision_path).resolve()
    decision = json.loads(path.read_text())
    if decision.get('scientific_acceptance') is not True:
        raise ValueError('only parent-accepted decisions enter the disposition registry')
    status = {'accepted_not_selected':'not_selected', 'accepted_source_exception':'source_exception',
              'accepted_staged':'staged_unpublished', 'accepted_for_release':'staged_unpublished'}.get(decision.get('decision'))
    if not status:
        raise ValueError('unsupported acceptance decision; publication needs its separate receipt')
    program, aid = decision['key'].split(':',1)
    evidence = {'decision':{'path':str(path),'sha256':digest(path)}}
    receipt_ref = decision['receipt']
    if digest(receipt_ref['path']) != receipt_ref['sha256']:
        raise ValueError('accepted worker receipt changed')
    evidence['receipt'] = receipt_ref
    receipt = json.loads(Path(receipt_ref['path']).read_text())
    if receipt.get('key') != decision['key']:
        raise ValueError('parent decision and worker receipt identify different papers')
    result_ref = receipt.get('result')
    version = decision.get('source_version')
    if result_ref:
        if digest(result_ref['path']) != result_ref['sha256']:
            raise ValueError('accepted result changed')
        evidence['result'] = result_ref
        result = json.loads(Path(result_ref['path']).read_text())
        if result.get('key') != decision['key']:
            raise ValueError('accepted result belongs to another paper')
        version = version or result.get('source_version')
    event_id = 'decision:'+digest(path)
    with connect(root) as conn:
        old = conn.execute('SELECT payload,sha256 FROM events WHERE event_id=?',(event_id,)).fetchone()
        if old:
            if hashlib.sha256(old[0].encode()).hexdigest() != old[1]:
                raise ValueError('accepted decision registry checksum mismatch')
            return 0
    previous = next((r for r in current(root) if r['program']==program and r['paper_id']==identity(aid)[0]), None)
    row = dict(event_id='decision:'+digest(path), paper_id=aid, program=program,
               status='has_card' if previous and previous['status']=='has_card' else status,
               review_disposition=status, title=decision.get('title') or (previous or {}).get('title',''),
               source_version=version, reason=decision.get('boundary') or decision.get('source_issue') or decision['decision'],
               reopen_condition=decision.get('reopen_condition') or (previous or {}).get('reopen_condition','Only explicitly authorized changed-evidence review.'),
               evidence=evidence, formal_grade=decision.get('grade'), formal_score=decision.get('score'))
    return record_many(root,[row])


def export(root):
    root = Path(root)
    rows = sorted(current(root), key=lambda r:(r['program'],r['paper_id']), reverse=True)
    all_no_cards = [r for r in rows if r['status'] in NO_CARD]
    ignored = [r for r in all_no_cards if r['program'] == 'Daily' and r['status'] == 'not_selected']
    no_cards = [r for r in all_no_cards if not (r['program'] == 'Daily' and r['status'] == 'not_selected')]
    result = dict(schema_version=1, generated_at_utc=datetime.now(timezone.utc).isoformat(),
                  counts=dict(Counter(r['status'] for r in no_cards)), no_card_records=len(no_cards),
                  ignored_daily_below_s=len(ignored), historical_no_card_records=len(all_no_cards),
                  counts_by_program=dict(Counter(r['program'] for r in no_cards)),
                  unique_no_card_works=len({r['paper_id'] for r in no_cards}),
                  has_card_records=sum(r['status']=='has_card' for r in rows), rows=no_cards,
                  boundary='Daily not-selected/no-card outcomes are ignored in this view but retained for deduplication. Per-program dispositions; no-card includes staged/blocked/stopped, not only scientific rejection. No new paper processing authorized.')
    labels={'not_selected':'已审阅但未入选','source_exception':'来源或承重证据异常','incomplete':'已开始但未完成',
            'stopped_unstarted':'尚未启动／停领','staged_unpublished':'已有草稿／尚未发布',
            'publication_blocked':'已审阅但发布条件缺失','in_progress':'已有进行中工作','needs_review':'状态需人工核对'}
    lines=['# 未制作／未发布卡片清单','', '本清单按 Daily / Collection 分开记录；不是论文质量黑名单。',
           '同一论文其他项目已有卡片时优先复用；未知版本保留未知。领取、下载或制卡前先查询 registry。',
           '',f"记录数：{len(no_cards)}；去重论文：{result['unique_no_card_works']}；已有卡片项目记录：{result['has_card_records']}。",'']
    lines += [f"已忽略 {len(ignored)} 条未达到 S 门槛且未制卡的 Daily 记录；历史结论仍用于查重，不列入当前清单。", '']
    for status in labels:
        group=[r for r in no_cards if r['status']==status]
        if not group:continue
        lines += [f'## {labels[status]}（{len(group)}）','', '| 项目 / 论文 ID | 标题 | 已审版本 | 结论 / 再开条件 | 证据 |','| --- | --- | --- | --- | --- |']
        for r in group:
            clean=lambda s: str(s or '').replace('|','\\|').replace('\n',' ')
            ref=next(iter(r['evidence'].values()))
            lines.append(f"| {r['program']} / {r['paper_id']} | {clean(r['title'])} | {clean(r['source_version'] or '未知')} | {clean(r['reason'])}；再开：{clean(r['reopen_condition'])} | [记录]({ref['path']}) |")
        lines.append('')
    for name, text in [('no-card-current.json',json.dumps(result,ensure_ascii=False,indent=2)+'\n'),('no-card-current.md','\n'.join(lines)+'\n')]:
        tmp=root/(name+'.tmp')
        tmp.write_text(text)
        tmp.replace(root/name)
    return {k:v for k,v in result.items() if k!='rows'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['record','lookup','export','accept'])
    p.add_argument('--registry',type=Path)
    p.add_argument('--input',type=Path)
    p.add_argument('--decision',type=Path)
    p.add_argument('--id');p.add_argument('--title');p.add_argument('--version')
    p.add_argument('--program',choices=['Daily','Collection']);p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1])
    args=p.parse_args()
    try:
        root=args.registry or default_registry()
        if args.command=='record':
            if not args.input:p.error('--input required')
            records=json.loads(args.input.read_text())
            if isinstance(records,dict):records=[records]
            result=dict(added=record_many(root,records),snapshot=export(root))
        elif args.command=='accept':
            if not args.decision:p.error('--decision required')
            result=dict(added=accept_decision(root,args.decision))
        elif args.command=='export':result=export(root)
        else:
            if not (args.id or args.title):p.error('--id or --title required')
            result=lookup(root,args.id,args.program,args.version,args.title,args.repo)
        print(json.dumps(result,ensure_ascii=False))
    except (ValueError,KeyError,TypeError,OSError,sqlite3.Error) as exc:p.exit(1,str(exc)+'\n')


if __name__=='__main__':main()
