import json
import tempfile
import unittest
from pathlib import Path

from scripts.update_ziming_mineru_campaign import update_campaign, valid_transition


class UpdateZimingMineruCampaignTests(unittest.TestCase):
    def test_transition_rules_are_strictly_serial(self) -> None:
        self.assertTrue(valid_transition("pending", "extracting"))
        self.assertTrue(valid_transition("card_staged", "card_installed"))
        self.assertTrue(valid_transition("packet_ready", "blocked"))
        self.assertFalse(valid_transition("pending", "card_installed"))
        self.assertFalse(valid_transition("card_installed", "blocked"))
        self.assertFalse(valid_transition("blocked", "extracting"))
        self.assertTrue(valid_transition("blocked", "extracting", retry_blocked=True))
        self.assertFalse(valid_transition("blocked", "packet_ready", retry_blocked=True))

    def test_updates_atomically_and_appends_hashed_event(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            campaign = root / "campaign.json"
            events = root / "events.jsonl"
            artifact = root / "paper.pdf"
            artifact.write_bytes(b"%PDF-test")
            campaign.write_text(
                json.dumps(
                    {
                        "selection": [
                            {"card_id": "one", "status": "pending"},
                            {"card_id": "two", "status": "card_existing"},
                        ]
                    }
                ),
                encoding="utf-8",
            )

            event = update_campaign(
                campaign,
                events,
                "one",
                "extracting",
                {"pdf": artifact},
                "started",
            )

            updated = json.loads(campaign.read_text(encoding="utf-8"))
            self.assertEqual(updated["selection"][0]["status"], "extracting")
            self.assertEqual(updated["pending_cards"], 1)
            self.assertEqual(event["artifacts"]["pdf"]["bytes"], 9)
            self.assertEqual(len(events.read_text(encoding="utf-8").splitlines()), 1)

    def test_explicit_blocked_retry_is_auditable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            campaign = root / "campaign.json"
            events = root / "events.jsonl"
            campaign.write_text(
                json.dumps({"selection": [{"card_id": "one", "status": "blocked"}]}),
                encoding="utf-8",
            )

            event = update_campaign(
                campaign,
                events,
                "one",
                "extracting",
                {},
                "transient transport failure cleared",
                retry_blocked=True,
            )

            updated = json.loads(campaign.read_text(encoding="utf-8"))
            self.assertEqual(updated["selection"][0]["status"], "extracting")
            self.assertEqual(event["from"], "blocked")
            self.assertEqual(event["to"], "extracting")


if __name__ == "__main__":
    unittest.main()
