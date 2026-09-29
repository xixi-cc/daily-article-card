#!/usr/bin/env python3
"""Extract immutable, one-paper Daily nominations from a frozen candidate queue."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prepare(manifest_path, queue_path, paper_ids, out):
    manifest_path, queue_path, out = map(lambda p: Path(p).resolve(),
                                         (manifest_path, queue_path, out))
    manifest = json.loads(manifest_path.read_text())
    expected = manifest['source_hashes'].get(str(queue_path))
    if not expected or sha(queue_path) != expected:
        raise ValueError('Queue is not a verified frozen input of this run.')
    protected = [queue_path.parents[1]]
    protected += [Path(v['path']).resolve() for v in manifest['production'].values()]
    if any(out == root or root in out.parents for root in protected):
        raise ValueError('Intakes must be outside frozen sources and production worktrees.')
    if out.exists():
        raise ValueError('Output directory exists; use a new intake checkpoint.')
    wanted = list(dict.fromkeys(paper_ids))
    if len(wanted) != len(paper_ids):
        raise ValueError('Duplicate requested paper ID.')
    rows = {r['arxiv_id']: r for r in manifest['rows'] if r['program'] == 'Daily'}
    if any(i not in rows or rows[i]['run_state'] != 'pending_fulltext' for i in wanted):
        raise ValueError('Requested ID is not a pending Daily fulltext item.')
    queue = json.loads(queue_path.read_text())
    candidates = {}
    for candidate in queue['candidates']:
        ident = candidate['arxiv_id']
        if ident in wanted:
            if ident in candidates:
                raise ValueError('Duplicate candidate in frozen queue: ' + ident)
            candidates[ident] = candidate
    if set(candidates) != set(wanted):
        raise ValueError('Missing candidate in frozen queue: ' + ', '.join(set(wanted)-set(candidates)))
    out.mkdir(parents=True)
    for ident in wanted:
        entry = {'schema_version': 1, 'key': 'Daily:' + ident,
                 'source_queue': {'path': str(queue_path), 'sha256': expected},
                 'source_manifest': {'path': str(manifest_path), 'sha256': sha(manifest_path)},
                 'candidate': candidates[ident],
                 'claim_strength': 'abstract nomination only; exact-version fulltext review pending'}
        (out/(ident+'.json')).write_text(json.dumps(entry, ensure_ascii=False, indent=2)+'\n')
    return {'count': len(wanted), 'intake_dir': str(out)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--queue', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('ids', nargs='+')
    a = p.parse_args()
    try:
        print(json.dumps(prepare(a.manifest, a.queue, a.ids, a.out)))
    except (ValueError, KeyError, OSError) as exc:
        p.exit(1, str(exc)+'\n')


if __name__ == '__main__':
    main()
