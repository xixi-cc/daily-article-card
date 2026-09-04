import json
import tempfile
import unittest
from pathlib import Path

from scripts.initialize_ziming_mineru_campaign import build_campaign


class ZimingMineruCampaignTests(unittest.TestCase):
    def test_selects_source_deduplicates_and_excludes_existing_cards(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog = root / "papers.json"
            cards = root / "cards"
            cards.mkdir()
            (cards / "2401.00001.json").write_text("{}", encoding="utf-8")
            records = [
                {
                    "id": "one",
                    "title": "Existing",
                    "url": "https://arxiv.org/abs/2401.00001v2",
                    "tags": ["arXiv", "Theory"],
                    "curation_sources": [{"name": "Ziming Liu Paper Collection"}],
                },
                {
                    "id": "two",
                    "title": "Pending A",
                    "url": "https://arxiv.org/abs/2401.00002",
                    "tags": ["arXiv", "AI"],
                    "curation_sources": [
                        {"url": "https://example.test/ziming-paper-collection/"}
                    ],
                },
                {
                    "id": "three",
                    "title": "Pending A duplicate",
                    "url": "https://arxiv.org/pdf/2401.00002.pdf",
                    "tags": ["arXiv", "AI"],
                    "curation_sources": [{"name": "Ziming Liu Paper Collection"}],
                },
                {
                    "id": "other",
                    "title": "Not selected",
                    "url": "https://arxiv.org/abs/2401.00003",
                    "tags": ["arXiv", "Other"],
                    "curation_sources": [{"name": "Another source"}],
                },
            ]
            catalog.write_text(json.dumps(records), encoding="utf-8")

            campaign = build_campaign(catalog, cards)

            self.assertEqual(campaign["source_records"], 3)
            self.assertEqual(campaign["unique_works"], 2)
            self.assertEqual(campaign["existing_cards"], 1)
            self.assertEqual(campaign["pending_cards"], 1)
            pending = [
                item for item in campaign["selection"] if item["status"] == "pending"
            ]
            self.assertEqual(pending[0]["card_id"], "2401.00002")
            self.assertEqual(pending[0]["catalog_record_ids"], ["two", "three"])


if __name__ == "__main__":
    unittest.main()
