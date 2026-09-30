from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_card_delivery import asset_source, check_card, cover_attribution_errors, main, math_errors


class DeliveryTests(unittest.TestCase):
    def test_delivery_fails_when_standard_sync_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp)/'manifest.json'
            out = Path(tmp)/'receipt.json'
            manifest.write_text(json.dumps({'cards': [{'id': '2609.00162', 'program': 'Daily',
                'card': str(ROOT/'data/curated_cards/2609.00162.json')}]}))
            with patch('sys.argv', ['delivery', '--repo', str(ROOT), '--manifest', str(manifest), '--out', str(out)]), \
                 patch('check_card_delivery.subprocess.run') as sync_run, redirect_stdout(StringIO()):
                sync_run.return_value.returncode = 1
                sync_run.return_value.stderr = 'canonical standard is 2.4; sync checker expects 2.3'
                self.assertEqual(main(), 1)
            self.assertFalse(json.loads(out.read_text())['passed'])
            self.assertIn('sync checker expects 2.3', json.loads(out.read_text())['standard_sync_errors'][0])

    def test_row_break_parenthesis_is_not_inline_delimiter(self):
        self.assertEqual(math_errors(r'\[\begin{aligned}a&=b,\\(I-P)u&=v\end{aligned}\]'), [])

    def test_unbalanced_and_raw_tex_fail(self):
        for text in [r'\[a=b', r'$a=\(b\)$', r'outside \alpha', r'$$x$$']:
            self.assertTrue(math_errors(text), text)

    def test_persistent_asset_paths(self):
        self.assertEqual(asset_source(ROOT, 'assets/card-figures/123/a.png'), ROOT/'data/card_figures/123/a.png')
        for asset in ['/etc/passwd', 'assets/../../private.png', 'assets/source-figures/output-only.png']:
            with self.assertRaises(ValueError):
                asset_source(ROOT, asset)

    def check_modified(self, mutate):
        card = json.loads((ROOT/'data/curated_cards/2609.00162.json').read_text())
        mutate(card)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/'card.json'
            p.write_text(json.dumps(card, ensure_ascii=False))
            return check_card(ROOT, dict(id='2609.00162', program='Daily', card=str(p)))

    def test_known_good_card(self):
        self.assertEqual(self.check_modified(lambda c: None)['errors'], [])

    def test_metadata_missing_before_build(self):
        r = self.check_modified(lambda c: c['verified_metadata'].pop('abstract'))
        self.assertTrue(any('abstract' in e for e in r['errors']))

    def test_noncanonical_heading_before_build(self):
        def change(c):
            c['sections'][1]['title'] = '研究问题或摘要'
        self.assertIn('missing question section', self.check_modified(change)['errors'])

    def test_version_mismatch(self):
        r = self.check_modified(lambda c: c['verified_metadata'].update(version='v99'))
        self.assertTrue(any('version' in e for e in r['errors']))

    def test_figure_output_only_is_rejected(self):
        def change(c):
            c['figure_refs'][0]['asset_path'] = 'assets/source-figures/output-only.png'
        r = self.check_modified(change)
        self.assertTrue(any('persistent source' in e for e in r['errors']))

    def test_missing_reproduction_boundary(self):
        r = self.check_modified(lambda c: c.update(evidence_refs=['p1','p2','p3']))
        self.assertIn('missing explicit independent-reproduction boundary', r['errors'])

    def test_collection_can_use_exact_journal_version(self):
        card = json.loads((ROOT/'data/collection_cards/2101.08176.json').read_text())
        card['source_version'] = 'JMLR-24-109-2023'
        card['verified_metadata']['version'] = 'JMLR-24-109-2023'
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/'card.json'
            p.write_text(json.dumps(card, ensure_ascii=False))
            r = check_card(ROOT, dict(id='2101.08176', program='Collection', card=str(p)))
        self.assertEqual(r['errors'], [])

    def test_content_field_without_rendered_paragraphs_is_rejected(self):
        def change(card):
            card['sections'][1]['content'] = card['sections'][1].pop('paragraphs')[0]
        r = self.check_modified(change)
        self.assertIn('unrenderable section body: 研究问题', r['errors'])

    def test_cover_source_is_not_repeated_by_builder(self):
        authors = ['Eric J. Michaud', 'Liv Gorton', 'Tom McGrath']
        cover = {'caption': '合成示例。来源：arXiv:2509.02565v2，CC BY 4.0。',
                 'attribution': 'Michaud, Gorton and McGrath; arXiv:2509.02565v2; CC BY 4.0'}
        self.assertIn('cover caption repeats automatically appended source attribution',
                      cover_attribution_errors(cover, authors))
        self.assertIn('cover attribution repeats automatically appended author names',
                      cover_attribution_errors(cover, authors))
        cover = {'caption': '合成示例。',
                 'attribution': 'arXiv:2509.02565v2; CC BY 4.0; https://arxiv.org/abs/2509.02565v2'}
        self.assertEqual(cover_attribution_errors(cover, authors), [])


if __name__ == '__main__':
    unittest.main()
