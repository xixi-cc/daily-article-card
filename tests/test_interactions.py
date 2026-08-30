from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_site import generate_atom_feed, generate_paper_html  # noqa: E402


class InteractionBuildTests(unittest.TestCase):
    def test_atom_feed_uses_stable_program_identifier(self) -> None:
        xml = generate_atom_feed(
            [
                {
                    "program": "Daily",
                    "arxiv_id": "2608.26556",
                    "detail_path": "papers/2608.26556/",
                    "title": "A & B",
                    "feed_date": "2026-08-29",
                    "hook_text": "Result < limit",
                }
            ],
            title="Feed",
            subtitle="Updates",
            feed_path="feed.xml",
        )
        self.assertIn("urn:xixi-paper:daily:2608.26556", xml)
        self.assertIn("A &amp; B", xml)
        self.assertIn("Result &lt; limit", xml)

    def test_detail_page_maps_comments_and_favorite_by_program(self) -> None:
        record = {
            "program": "Collection",
            "arxiv_id": "2608.26556",
            "page_dir": "2608.26556",
            "title": "Example",
            "title_zh": "示例",
            "preview_text": "Preview",
            "paper_image_path": "",
            "cover_theme": {},
            "cover_summary": "",
            "sections": [],
            "figure_refs": [],
            "link": "https://arxiv.org/abs/2608.26556",
            "category": "Machine Learning",
            "research_type": "理论",
            "tags": [],
            "reading_minutes": 1,
            "section_count": 0,
            "research_unit": "",
            "date": "2026-08-29",
            "authors": "",
            "hook_text": "Preview",
            "cover_caption": "",
            "cover_alt_text": "",
        }
        html = generate_paper_html(record)
        self.assertIn('data-paper-program="collection"', html)
        self.assertIn('data-term="collection:2608.26556"', html)
        self.assertIn('id="detail-favorite"', html)
        self.assertIn("xixi-cc/xixi-research-comments", html)


if __name__ == "__main__":
    unittest.main()
