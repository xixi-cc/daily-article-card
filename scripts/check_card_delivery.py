#!/usr/bin/env python3
"""Read-only pre-install checks for an explicit Daily/Collection delivery manifest.

This is a mechanical gate, not a scientific review or publication receipt.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import tempfile

import validate_paper_cards as standard
from enrich_daily_cards import verified_local_metadata
from reconcile_card_resume import digest


def asset_source(repo, asset, overrides=None):
    relative = Path(asset)
    if relative.is_absolute() or '..' in relative.parts or not asset.startswith('assets/'):
        raise ValueError('asset must be a safe site-relative assets/ path: ' + asset)
    if overrides and asset in overrides:
        return Path(overrides[asset]).resolve()
    for public, source in [('assets/card-figures/', 'data/card_figures/'),
                           ('assets/collection-figures/', 'data/collection_figures/')]:
        if asset.startswith(public):
            return repo / (source + asset[len(public):])
    raise ValueError('asset has no persistent source mapping; generated-site-only assets are rejected: ' + asset)


def math_errors(text):
    errors, stack = [], []
    # A TeX row break followed by '(' is not the inline opener '\('.
    for token in re.findall(r'(?<!\\)\$\$|(?<!\\)\\[\[\]()]|(?<!\\)\$', text):
        if token == '$$':
            errors.append('legacy $$ delimiter')
        elif token in ('\\[', '\\('):
            if stack:
                errors.append('nested math delimiter')
            stack.append(token)
        elif token in ('\\]', '\\)'):
            expected = '\\[' if token == '\\]' else '\\('
            if not stack or stack.pop() != expected:
                errors.append('mismatched math delimiter')
        elif stack and stack[-1] == '$':
            stack.pop()
        elif stack:
            errors.append('nested dollar delimiter')
        else:
            stack.append('$')
    if stack:
        errors.append('unclosed math delimiter')
    plain = re.sub(r'\\\[.*?\\\]|\\\(.*?\\\)|(?<!\\)\$[^$]*?(?<!\\)\$', '', text, flags=re.S)
    if re.search(r'\\[A-Za-z]+', plain):
        errors.append('bare TeX command outside math')
    return errors


def check_card(repo, entry):
    errors, hashes = [], {}
    path = Path(entry['card']).resolve()
    card = json.loads(path.read_text())
    hashes[str(path)] = digest(path)
    aid, program = entry['id'], entry['program']
    if program not in ('Daily', 'Collection'):
        return dict(id=aid, program=program, errors=['invalid program'], hashes=hashes)
    if (card.get('arxiv_id') or card.get('card_id')) != aid:
        errors.append('manifest/card identity mismatch')
    if not standard.version_at_least(card, (2, 3)):
        errors.append('new delivery requires standard >= 2.3')
    if card.get('curation_status') != 'full_text_verified':
        errors.append('curation_status is not full_text_verified')
    sections = card.get('sections', [])
    headings = [s.get('title') for s in sections if isinstance(s, dict)]
    for section in sections:
        if not isinstance(section, dict):
            errors.append('section is not an object')
            continue
        entries = section.get('bullets') or section.get('paragraphs')
        if not isinstance(entries, list) or not any(isinstance(x, str) and x.strip() for x in entries):
            errors.append('unrenderable section body: ' + str(section.get('title', '?')))
    missing = (standard.REQUIRED_CORE | {'背景'}) - set(headings)
    if missing:
        errors.append('missing sections: ' + ', '.join(sorted(missing)))
    for choices, label in [(standard.QUESTION_HEADINGS, 'question'), (standard.RESULT_HEADINGS, 'results')]:
        if not set(headings) & choices:
            errors.append('missing ' + label + ' section')
    if len(headings) != len(set(headings)):
        errors.append('duplicate section headings')
    content = json.dumps(sections, ensure_ascii=False)
    if len(content) < standard.MIN_CONTENT_CHARS:
        errors.append('card is below canonical minimum depth')
    for phrase in standard.FORBIDDEN_PHRASES:
        if phrase in content:
            errors.append('placeholder: ' + phrase)
    for text in standard.iter_strings(sections):
        errors.extend(math_errors(text))
    evidence = card.get('evidence_refs', [])
    if not isinstance(evidence, list) or len(evidence) < 3:
        errors.append('insufficient evidence_refs')
    if not (any('no independent reproduction' in str(x) for x in evidence) or
            card.get('independent_reproduction') is False and any('independent_reproduction=false' in str(x) for x in evidence)):
        errors.append('missing explicit independent-reproduction boundary')
    metadata = card.get('verified_metadata', {})
    for field in ('title', 'authors', 'published', 'version') + (('abstract',) if program == 'Daily' else ()):
        if not metadata.get(field):
            errors.append('verified_metadata missing ' + field)
    if metadata.get('version') != card.get('source_version'):
        errors.append('source version conflicts with verified metadata')
    version = str(card.get('source_version', '')).strip()
    if program == 'Daily' and not re.fullmatch(r'v\d+', version):
        errors.append('Daily requires an exact arXiv source version')
    elif program == 'Collection' and not version:
        errors.append('Collection requires an identified source version')
    try:
        date = str(metadata.get('published', ''))
        parsed = datetime.fromisoformat(date.replace('Z', '+00:00'))
        if parsed.tzinfo is None and (program == 'Daily' or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', date)):
            errors.append('publication date must have timezone; preserve day precision separately')
    except ValueError:
        errors.append('invalid publication date')
    if program == 'Daily':
        try:
            if verified_local_metadata(card) is None:
                errors.append('verified metadata unavailable')
        except ValueError as exc:
            errors.append(str(exc))
    elif any(k in card for k in ('selection_record', 'report_date', 'grade', 'score')):
        errors.append('Collection must not inherit Daily selection/date/grade/score')

    assets = {str(x.get('asset_path', '')) for x in card.get('figure_refs', []) if isinstance(x, dict)}
    cover = card.get('cover', {})
    if isinstance(cover, dict) and cover.get('asset_path'):
        assets.add(cover['asset_path'])
    assets.discard('')
    # The canonical validator checks site-relative files. A temporary mirror maps
    # persistent source assets without modifying the site or invoking a build.
    original_root = standard.ROOT
    with tempfile.TemporaryDirectory(prefix='card-delivery-') as tmp:
        standard.ROOT = Path(tmp)
        try:
            for asset in assets:
                try:
                    source = asset_source(repo, asset, entry.get('asset_sources'))
                    if not source.is_file():
                        raise ValueError('missing persistent asset: ' + str(source))
                    hashes[str(source)] = digest(source)
                    target = standard.ROOT / 'site' / asset
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.symlink_to(source)
                except ValueError as exc:
                    errors.append(str(exc))
            errors.extend(standard.validate_v2_card(card, aid, program))
        finally:
            standard.ROOT = original_root
    return dict(id=aid, program=program, card=str(path), hashes=hashes,
                errors=sorted(set(errors)), mechanical_pass=not errors,
                scientific_review='not performed by this tool', source_figure_visual_review='required separately')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        parser.error('receipt exists; choose a new output file')
    manifest = json.loads(args.manifest.read_text())
    entries = manifest['cards']
    keys = [(e['program'], e['id']) for e in entries]
    if not keys or len(keys) != len(set(keys)):
        parser.error('manifest must contain nonempty, unique program/id pairs')
    rows = []
    for entry in entries:
        try:
            rows.append(check_card(args.repo.resolve(), entry))
        except (KeyError, ValueError, TypeError, OSError) as exc:
            rows.append(dict(id=entry.get('id'), errors=[str(exc)], mechanical_pass=False))
    result = dict(schema_version=1, manifest_sha256=digest(args.manifest),
                  validator_sha256=digest(Path(standard.__file__)),
                  checker_sha256=digest(Path(__file__)), cards=rows,
                  passed=all(r['mechanical_pass'] for r in rows),
                  boundary='Mechanical delivery gate only; no card changes, installation, scientific certification or publication.')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(passed=result['passed'], cards=len(rows), failures=[dict(id=r['id'], errors=r['errors']) for r in rows if r['errors']]), ensure_ascii=False))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
