from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_card_delivery import asset_source, check_card, math_errors


class DeliveryTests(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
