#!/usr/bin/env python3
"""Bounded context views and per-paper handoffs; never dispatch or resume work."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

from reconcile_card_resume import digest

MAX_SUMMARY = 400
OUTCOMES = {'card_staged', 'not_selected', 'source_exception', 'needs_input',
            'metadata_only', 'interrupted', 'audit_complete'}


def read(path):
    return json.loads(Path(path).read_text())


def write_new(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def reference(path):
    path = Path(path).resolve()
    return dict(path=str(path), sha256=digest(path))


def protect_output(out, manifest):
    out = Path(out).resolve()
    roots = [Path(v['path']).resolve() for v in manifest['production'].values()]
    roots += [Path(p).parent.resolve() for p in manifest.get('source_hashes', {})
              if Path(p).name == 'scope-stop-20260929-corrected.json']
    if any(out == p or p in out.parents for p in roots):
        raise ValueError('Output must be outside production worktrees and frozen campaign.')
    if out.exists():
        raise ValueError('Output exists; choose a new checkpoint/packet/receipt path.')


def compact_row(row):
    return {k: row[k] for k in ('key', 'cohort', 'next_action', 'delivery_gate') if k in row}


def brief(manifest_path, out, limit=5, runtime_path=None, receipts_dir=None, decisions_dir=None):
    if not 0 <= limit <= 10:
        raise ValueError('Brief preview must contain 0..10 items.')
    manifest = read(manifest_path)
    protect_output(out, manifest)
    runtime = read(runtime_path) if runtime_path else None
    scope_authorized = bool(manifest.get('run_authorization'))
    active = runtime.get('active_units', []) if runtime else []
    if len(active) > 2:
        raise ValueError('This campaign permits at most two active paper workers.')
    if any(set(x) - {'key', 'agent_id', 'packet_path', 'stage'} for x in active):
        raise ValueError('Active-unit records must contain routing fields only.')
    if len({x['key'] for x in active}) != len(active):
        raise ValueError('Duplicate active paper ownership.')
    rows = manifest['rows']
    keys = {x['key'] for x in rows}
    if len(keys) != len(rows) or any(x['key'] not in keys for x in active):
        raise ValueError('Duplicate manifest keys or unknown active unit.')
    reported = {}
    for path in sorted(Path(receipts_dir).glob('*.receipt.json')) if receipts_dir else []:
        record = read(path)
        if record.get('key') not in keys or record.get('outcome') not in OUTCOMES:
            raise ValueError('Unknown paper/outcome in compact receipt.')
        if record['key'] in reported:
            raise ValueError('Keep one current receipt per paper; archive superseded receipts separately.')
        for field in ('packet', 'result'):
            if digest(record[field]['path']) != record[field]['sha256']:
                raise ValueError('Changed packet/result in receipt: ' + str(path))
        reported[record['key']] = dict(key=record['key'], outcome=record['outcome'], receipt=str(path.resolve()))
    accepted = {}
    for path in sorted(Path(decisions_dir).glob('*.json')) if decisions_dir else []:
        decision = read(path)
        key = decision.get('key')
        receipt_ref = decision.get('receipt', {})
        if (key not in keys or not decision.get('scientific_acceptance')
                or key not in reported or receipt_ref.get('path') != reported[key]['receipt']
                or digest(receipt_ref['path']) != receipt_ref.get('sha256')):
            raise ValueError('Decision is not bound to an accepted current receipt: ' + str(path))
        if key in accepted:
            raise ValueError('Duplicate accepted decision: ' + key)
        accepted[key] = dict(key=key, decision=decision['decision'], path=str(path.resolve()))
    awaiting = {k: v for k, v in reported.items() if k not in accepted}
    # Full lists and hashes stay on disk. This view is deliberately not a queue mutation.
    order = {'accepted_staged_not_installed': 0, 'started_metadata_only': 1,
             'stopped_unstarted': 2, 'outside_original_collection_queue': 3}
    ordered = sorted(rows, key=lambda x: (order.get(x['cohort'], 9), x['program'] != 'Daily',
                                         x.get('queue_position') or x.get('source_position') or 0))
    state = dict(schema_version=1, purpose='controller_context_only',
                 authority=reference(manifest_path),
                 runtime=reference(runtime_path) if runtime_path else None,
                 dispatch_authorized=scope_authorized,
                 scope=('User resumed campaign intake; verify active ownership before each dispatch.'
                        if scope_authorized else 'Preparing handoffs does not resume stopped papers.'),
                 counts=dict(total=len(rows), cohorts=dict(Counter(x['cohort'] for x in rows))),
                 production={k: {f: v[f] for f in ('path', 'head', 'remote_head', 'public_branch') if f in v}
                             for k, v in manifest['production'].items()},
                 active_units=active, runtime_state_known=runtime is not None,
                 preview=[compact_row(x) for x in ordered if x.get('run_state') not in
                          {'published', 'accepted_not_selected', 'accepted_source_exception'}
                          and x['key'] not in reported and x['key'] not in accepted
                          and x['key'] not in {a['key'] for a in active}][:limit],
                 reported_not_accepted=dict(count=len(awaiting),
                                            outcomes=dict(Counter(x['outcome'] for x in awaiting.values())),
                                            preview=list(awaiting.values())[:limit]),
                 accepted_decisions=dict(count=len(accepted),
                                         outcomes=dict(Counter(x['decision'] for x in accepted.values())),
                                         preview=list(accepted.values())[:limit]),
                 missing_report_dates=manifest.get('report_dates_still_missing', []),
                 rules=dict(worker_context='fresh; fork_context=false', papers_per_worker=1,
                            max_concurrent_paper_workers=2, parent_role='single integrator/publisher',
                            result_summary_max_chars=MAX_SUMMARY, build_after_at_most_accepted_cards=10,
                            scientific_evidence='full local packet; open on demand, never truncate to summary quota'))
    out = Path(out)
    out.mkdir(parents=True)
    write_new(out/'controller.json', state)
    lines = ['# Paper Card controller checkpoint', '',
             f"Authority: {state['authority']['path']}", f"SHA-256: {state['authority']['sha256']}",
             f"Items: {len(rows)}. Counts: {json.dumps(state['counts']['cohorts'])}", '',
             'Scope: '+state['scope'],
             'Keep this view, the current small batch, active IDs and receipt pointers in parent context.',
             'Do not read the full ledger, prior overlays, PDFs, all worker logs or other paper histories.',
             'Request one explicitly selected item with card_batch.py context packet.',
             'After actual user-authorized resume: fresh subagent, fork_context=false, one paper, at most two workers.',
             'Close accepted completed workers; retain an agent only for corrections to the SAME paper.',
             'Review central scientific claims through targeted independent review; a short receipt is not certification.',
             'No worker may edit the shared ledger, install cards or publish.', '', '## Production']
    lines += [f"- {k}: {v['path']} @ {v['head']} (observed remote {v.get('remote_head','unknown')})"
              for k, v in state['production'].items()]
    lines += ['', '## Routing preview (not a claim queue)']
    lines += [f"- {x['key']}: {x['cohort']}; {x['next_action']}" for x in state['preview']]
    lines += ['', f'## Reported, awaiting parent decision: {len(awaiting)}']
    lines += [f"- {x['key']}: {x['outcome']}; receipt={x['receipt']}" for x in list(awaiting.values())[:limit]]
    lines += ['', f'## Accepted parent decisions: {len(accepted)}']
    lines += [f"- {x['key']}: {x['decision']}; decision={x['path']}" for x in list(accepted.values())[:limit]]
    lines += ['', '## Runtime', json.dumps(active, ensure_ascii=False) if runtime else
              'No runtime registry supplied. Verify process/agent identity before assuming an item is free.',
              '', 'Each Goal continuation must produce an artifact, receipt or state decision. Await active work instead of unchanged polling.',
              'Compaction recovery starts here. This file does not clear existing chat history or alter Goal status.']
    text = '\n'.join(lines)+'\n'
    (out/'controller.md').write_text(text)
    return dict(checkpoint=str(out), items=len(rows), preview_items=len(state['preview']),
                controller_chars=len(text), controller_bytes=len(text.encode()),
                full_manifest_bytes=Path(manifest_path).stat().st_size, dispatched=False)


def packet(manifest_path, key, out, role, intake=None):
    manifest = read(manifest_path)
    protect_output(out, manifest)
    matches = [r for r in manifest['rows'] if r['key'] == key]
    if len(matches) != 1:
        raise ValueError('Select exactly one known program:paper ID.')
    row = matches[0]
    repo = Path(manifest['production']['cards']['path'])
    docs = ['AGENTS.md', 'docs/PAPER_CARD_STANDARD.md', 'docs/PAPER_CARD_STANDARD_INTEGRATION.md']
    if row['program'] == 'Daily':
        docs.append('docs/CODEX_DAILY_SCREENING_AND_PUBLICATION.md')
    instructions = [reference(repo/d) for d in docs]
    if row['program'] == 'Collection' and 'catalog' in manifest['production']:
        instructions.append(reference(Path(manifest['production']['catalog']['path'])/'AGENTS.md'))
    refs = {k: reference(row[k]) for k in ('staged_card', 'manifest', 'acceptance') if row.get(k)}
    if intake:
        nomination = read(intake)
        if nomination.get('key') != key or nomination.get('candidate', {}).get('arxiv_id') != row['arxiv_id']:
            raise ValueError('Intake belongs to a different paper.')
        source = nomination.get('source_queue', {})
        if (manifest.get('source_hashes', {}).get(source.get('path')) != source.get('sha256')
                or digest(source['path']) != source['sha256']):
            raise ValueError('Intake queue is not the frozen manifest input.')
        refs['intake'] = reference(intake)
    if row.get('staged_card'):
        card = read(row['staged_card'])
        version = card.get('source_version')
        title = card.get('title_en')
    else:
        version = None
        title = row.get('catalog_records', [{}])[0].get('title') if row.get('catalog_records') else None
    out = Path(out).resolve()
    job = dict(schema_version=1, key=key, role=role, authority=reference(manifest_path),
               execution_authorized=False, state='prepared_not_dispatched',
               program=row['program'], paper_id=row['arxiv_id'], source_version=version, title=title,
               cohort=row['cohort'], next_action=row['next_action'],
               listing_dates=row.get('listing_dates', []), catalog_records=row.get('catalog_records', []),
               existing_unit=row.get('unit'), existing_artifacts=refs,
               delivery_gate=row.get('delivery_gate'),
               instruction_files=instructions,
               write_root=str(out/'work'), result_path=str(out/'work/result.json'),
               return_policy=dict(max_summary_chars=MAX_SUMMARY, max_risk_flags=8,
                                  full_report='local file, never pasted to parent',
                                  final_message='key, outcome, receipt/result path, blocker only'),
               spawn_options=dict(fork_context=False),
               preserve='Old evidence and production source are read-only; stage changes only in write_root.')
    out.mkdir(parents=True)
    (out/'work').mkdir()
    write_new(out/'packet.json', job)
    prompt = f'''One independent Paper Card work unit: {key}; role={role}.
Read {out/'packet.json'} first. Do not read the parent conversation or other paper histories.
This is a PREPARED packet, not execution authorization. The dispatch message must explicitly authorize this unit's operation; otherwise return needs_input without processing the paper.
Use a fresh subagent with fork_context=false. Inherit the parent's model and reasoning; do not lower scientific standards.
Read the instruction_files listed in the packet. They remain the authoritative contract.
Read only this paper's existing_artifacts and existing_unit. Reuse accepted evidence by hashes; do not restart completed reading.
Write only under {out/'work'}. Do not change frozen sources, other units, shared ledgers, production cards, builds, releases or automation.
For unstarted research, preserve the full exact-version PDF, physical-page evidence, equations, figures and claim boundaries. The routing summary is NOT the paper evidence and has no scientific completeness quota.
For a reviewer, inspect the specified load-bearing claims and source artifacts independently; do not rely on an author's compact conclusion.
If an unresolved source/proof issue blocks the card, save the exact boundary and stop that item. Do not repair the paper through unlimited extra research.
For Daily historical recovery, a verified listing date is not evidence of the original report date. Check that date before drafting an installable card; if it is unavailable, keep the full-text score and any non-installable draft local, leave both report-date fields null, and report the publication blocker.
If an independently reviewed Daily candidate is graded below S, return not_selected even when its original report date is unknown; the date does not change that scientific disposition. Reserve needs_input for a missing fact that actually changes the next decision.
For a staged card, use one identical source_version string in result.json and the card; arXiv versions use vN, while a reviewed journal version may use its explicit journal identifier. Keep verified_metadata title, version and publication date aligned with the exact source actually reviewed; record any unverified final version as a boundary.
Use the site's canonical collection figure path assets/collection-figures/<paper_id>/<filename> for a permitted source figure. Record its source and reuse rights; use a text cover when reuse rights are not established. sampled_at describes the actual metadata observation time, not the publication date.
Save the detailed report and artifacts locally. Write {out/'work/result.json'} with schema_version=1, key, packet_sha256, outcome, source_version, summary (<=400 characters), risk_flags (<=8 short strings), next_action (<=240 characters), artifacts, and full_report.
Use exactly those top-level result keys; put any blocker in next_action and the brief final message, not in an extra result field.
Each artifacts entry and full_report is an object with absolute path and sha256. Full_report must be inside write_root; artifacts may also reference this packet's explicitly registered existing_artifacts. At most six artifact entries; use a source manifest for a larger evidence set. A card_staged result must include artifacts.card and artifacts.evidence_manifest. It is a PROPOSAL, never parent acceptance or publication.
Allowed outcomes: {', '.join(sorted(OUTCOMES))}. Use null source_version if still unresolved. Unknowns stay unknown.
Return only key, outcome, result path and any blocker (<=600 characters). Never paste full paper prose, derivations, screenshots, logs or a rewritten global progress report into the parent chat.
'''
    (out/'worker-prompt.txt').write_text(prompt)
    # Packet creation itself never calls an agent tool.
    return dict(key=key, packet=str(out/'packet.json'), packet_sha256=digest(out/'packet.json'),
                prompt=str(out/'worker-prompt.txt'), spawn_options=job['spawn_options'],
                prompt_chars=len(prompt), execution_authorized=False, dispatched=False)


def receipt(packet_path, result_path, out):
    job, result = read(packet_path), read(result_path)
    for ref in [*job['existing_artifacts'].values(), *job['instruction_files']]:
        if digest(ref['path']) != ref['sha256']:
            raise ValueError('Packet input changed; prepare a new packet instead of silently mixing versions.')
    if result.get('key') != job['key'] or result.get('packet_sha256') != digest(packet_path):
        raise ValueError('Result is bound to a different paper or packet hash.')
    allowed = {'schema_version','key','packet_sha256','outcome','source_version','summary',
               'risk_flags','next_action','artifacts','full_report'}
    if set(result) - allowed:
        raise ValueError('Keep long reports outside the compact result; unexpected fields.')
    if result.get('outcome') not in OUTCOMES or result.get('schema_version') != 1:
        raise ValueError('Invalid result outcome/schema.')
    if not isinstance(result.get('summary'), str) or not 1 <= len(result['summary']) <= MAX_SUMMARY:
        raise ValueError('Summary must be 1..400 characters; save full detail to a file, do not truncate evidence.')
    if not isinstance(result.get('next_action'), str) or not 1 <= len(result['next_action']) <= 240:
        raise ValueError('next_action must be 1..240 characters.')
    flags = result.get('risk_flags')
    if not isinstance(flags, list) or len(flags) > 8 or any(not isinstance(x,str) or len(x)>120 for x in flags):
        raise ValueError('At most 8 risk flags of at most 120 characters.')
    if job.get('source_version') and result.get('source_version') != job['source_version']:
        raise ValueError('Source version changed; prepare a new explicit packet for changed inputs.')
    artifacts = result.get('artifacts')
    if not isinstance(artifacts, dict) or len(artifacts) > 6:
        raise ValueError('At most six artifact pointers; use an evidence manifest for the complete packet.')
    write_root = Path(job['write_root']).resolve()
    registered = {v['path'] for v in job['existing_artifacts'].values()}
    full_report = result.get('full_report', {})
    references = dict(artifacts, full_report=full_report)
    for name, ref in references.items():
        if not isinstance(ref,dict) or set(ref) != {'path','sha256'}:
            raise ValueError('Artifacts require path and sha256 only.')
        path = Path(ref['path']).resolve()
        if write_root not in path.parents and (name == 'full_report' or str(path) not in registered):
            raise ValueError('Artifact is outside this work unit or registered inputs.')
        if digest(path) != ref['sha256']:
            raise ValueError('Artifact hash mismatch: ' + name)
    if result['outcome'] == 'card_staged':
        if not {'card','evidence_manifest'} <= set(artifacts):
            raise ValueError('card_staged needs card and evidence_manifest pointers.')
        card = read(artifacts['card']['path'])
        if (card.get('arxiv_id') or card.get('card_id')) != job['paper_id'] or card.get('source_version') != result.get('source_version'):
            raise ValueError('Staged card identity/version mismatch.')
        if card.get('provenance', {}).get('program') not in (None, job['program']):
            raise ValueError('Staged card program mismatch.')
    manifest = read(job['authority']['path'])
    if digest(job['authority']['path']) != job['authority']['sha256']:
        raise ValueError('Authoritative manifest changed; reconcile before accepting a result.')
    protect_output(out, manifest)
    output = dict(schema_version=1, key=job['key'], outcome=result['outcome'],
                  summary=result['summary'], risk_flags=flags, next_action=result['next_action'],
                  packet=reference(packet_path), result=reference(result_path),
                  full_report=full_report, artifacts=artifacts,
                  verification='pointer_hashes_only', scientific_acceptance=False,
                  installed=False, published=False, original_queue_mutated=False)
    write_new(out, output)
    return dict(key=job['key'], outcome=result['outcome'], receipt=str(Path(out).resolve()),
                summary=result['summary'], risk_flags=flags, next_action=result['next_action'],
                scientific_acceptance=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    p = commands.add_parser('brief')
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--limit', type=int, default=5)
    p.add_argument('--runtime', type=Path)
    p.add_argument('--receipts', type=Path)
    p.add_argument('--decisions', type=Path)
    p = commands.add_parser('packet')
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--key', required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--role', choices=['worker','reviewer','delivery_audit'], default='worker')
    p.add_argument('--intake', type=Path)
    p = commands.add_parser('receipt')
    p.add_argument('--packet', type=Path, required=True)
    p.add_argument('--result', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'brief':
            result = brief(args.manifest, args.out, args.limit, args.runtime, args.receipts, args.decisions)
        elif args.command == 'packet':
            result = packet(args.manifest, args.key, args.out, args.role, args.intake)
        else:
            result = receipt(args.packet, args.result, args.out)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, str(exc)+'\n')


if __name__ == '__main__':
    raise SystemExit(main())
