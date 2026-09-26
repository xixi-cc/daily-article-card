from __future__ import annotations

import sys
import unittest
from unittest.mock import patch
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_site import assert_daily_eligibility  # noqa: E402
import build_site  # noqa: E402


class DailyBoundaryTests(unittest.TestCase):
    def attach_cover(self, cover: dict) -> dict:
        card = {"provenance": {"program": "Daily"},
                "selection_record": {"selected_by": "codex_direct_arxiv", "grade": "S"},
                "cover": cover, "figure_refs": [{"label": "Figure 2"}]}
        record = {"card_id": "example", "date": "2026-09-10", "paper_image_path": "old-preview.jpg"}
        with patch.object(build_site, "load_legacy_daily_dates", return_value=set()), \
             patch.object(build_site, "load_card_file", return_value=card), \
             patch.object(build_site, "classify_card", return_value={}):
            build_site.attach_daily_metadata([record])
        return record

    def test_structured_daily_source_cover_replaces_legacy_preview(self) -> None:
        record = self.attach_cover({"mode": "source_figure", "asset_path": "assets/source-figures/verified.png",
                                    "caption": "Figure 2, full panels", "alt_text": "All labels"})
        self.assertEqual(record["paper_image_path"], "assets/source-figures/verified.png")
        self.assertEqual(record["cover_caption"], "Figure 2, full panels")
        self.assertEqual(record["figure_refs"], [{"label": "Figure 2"}])

    def test_title_abstract_cover_removes_stale_legacy_image(self) -> None:
        record = self.attach_cover({"mode": "title_abstract", "abstract_text": "Verified abstract"})
        self.assertEqual(record["paper_image_path"], "")
        self.assertEqual(record["cover_summary"], "Verified abstract")

    def test_source_cover_keeps_separate_attribution(self) -> None:
        card = {"cover": {"caption": "Original Figure 2", "attribution": "Paper v1; CC BY 4.0"},
                "verified_metadata": {"authors": ["Author A", "Author B"]}}
        caption = build_site.source_cover_caption(card)
        self.assertIn("Original Figure 2", caption)
        self.assertIn("Author A、Author B", caption)
        self.assertIn("Paper v1; CC BY 4.0", caption)

    def test_rejects_collection_only_card(self) -> None:
        with self.assertRaisesRegex(ValueError, "Collection-only"):
            assert_daily_eligibility(
                {"card_id": "example", "date": "2026-08-29"},
                {"provenance": {"program": "Collection"}},
                set(),
            )

    def test_accepts_codex_direct_s_card(self) -> None:
        assert_daily_eligibility(
            {"card_id": "example", "date": "2026-08-29"},
            {
                "provenance": {"program": "Daily"},
                "selection_record": {
                    "selected_by": "codex_direct_arxiv",
                    "grade": "S",
                },
            },
            set(),
        )

    def test_rejects_non_s_card(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid Codex-direct"):
            assert_daily_eligibility(
                {"card_id": "example", "date": "2026-08-29"},
                {
                    "provenance": {"program": "Daily"},
                    "selection_record": {
                        "selected_by": "codex_direct_arxiv",
                        "grade": "A",
                    },
                },
                set(),
            )


if __name__ == "__main__":
    unittest.main()
