from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_site import assert_daily_eligibility  # noqa: E402


class DailyBoundaryTests(unittest.TestCase):
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
