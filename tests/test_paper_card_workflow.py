import hashlib
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from scripts.create_paper_card_scaffold import build_scaffold, write_scaffold
from scripts.paper_card_evidence_layers import approximate_tokens, split_packet
from scripts.paper_card_metrics import audit_cards, finish_stage, start_stage


def metadata():
    return {
        "arxiv_id": "2609.00001",
        "version": "v1",
        "title": "A Verified Test Paper",
        "authors": ["A. Author"],
        "categories": ["cs.LG"],
        "primary_category": "cs.LG",
        "published": "2026-09-01T00:00:00Z",
        "abstract": "A sufficiently complete authoritative abstract.",
    }


def collection_provenance():
    return {
        "program": "Collection",
        "catalog": "Paper Collection",
        "catalog_record_id": "record-1",
        "catalog_topic": "Training Dynamics",
        "collection_date": "2026-09-01",
        "sampled_at": "2026-09-04",
        "selected_by": "test_campaign",
        "sampling_seed": "source_complete",
    }


class EvidenceLayerTests(unittest.TestCase):
    def test_split_preserves_exact_full_packet_and_bounds_core(self):
        packet = {
            "schema": "test-packet",
            "campaign_item": {"card_id": "2609.00001"},
            "source": {"pdf_page_count": 80, "pdf_sha256": "a" * 64},
            "quality_boundary": {
                "equation_authority": "source PDF",
                "required_boundary": "full-text verified; no independent reproduction performed",
            },
            "first_page": "first " * 2000,
            "page_evidence": {
                "introduction": {"page": 1, "text": "intro " * 1500},
                "method": {"page": 3, "text": "method " * 1500},
                "results": {"page": 8, "text": "results " * 1500},
                "conclusion_or_limitations": {"page": 12, "text": "limits " * 1500},
                "captions": [{"page": 8, "text": "caption " * 400}],
                "quantitative_lines": [{"page": 8, "text": "value " * 300}],
                "headings": [{"page": 1, "title": "Introduction"}],
                "urls": ["https://example.test/code"],
            },
            "mineru_sections": [{"title": "Methods", "text": "body " * 5000}],
            "mineru_equation_candidates": ["x=y"],
            "mineru_images": [{"path": "images/a.png"}],
            "size": {"approximate_tokens": 8000},
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "evidence_packet.json"
            payload = (json.dumps(packet, ensure_ascii=False, indent=2) + "\n").encode()
            source.write_bytes(payload)
            output = root / "layers"
            manifest = split_packet(source, output, target_tokens=1500)
            core = json.loads((output / "core.json").read_text())
            self.assertLessEqual(approximate_tokens(core), 1500)
            self.assertEqual(core["required_on_demand"], ["equations", "figures", "full_packet"])
            self.assertEqual((output / "supplements" / "full_packet.json").read_bytes(), payload)
            self.assertEqual(manifest["source_sha256"], hashlib.sha256(payload).hexdigest())
            self.assertTrue(manifest["lossless_full_packet_preserved"])

    def test_split_refuses_nonempty_output_without_force(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "packet.json"
            source.write_text("{}")
            output = root / "layers"
            output.mkdir()
            (output / "keep.txt").write_text("keep")
            with self.assertRaises(FileExistsError):
                split_packet(source, output)


class ScaffoldTests(unittest.TestCase):
    def test_collection_scaffold_has_stable_shape_and_provenance(self):
        card = build_scaffold(
            metadata(), "Collection", "theory_numerics", "核验测试论文", collection_provenance()
        )
        self.assertEqual(card["card_standard_version"], "2.4")
        self.assertEqual(card["audience_profile"], "physics_ai_literate_physicist")
        self.assertEqual(card["curation_status"], "draft")
        self.assertEqual(card["provenance"]["program"], "Collection")
        self.assertNotIn("selection_record", card)
        self.assertEqual(len(card["sections"]), 9)
        self.assertIn("给物理学家的 AI 导读", [section["title"] for section in card["sections"]])
        self.assertTrue(all("paragraphs" in section for section in card["sections"]))

    def test_daily_scaffold_rejects_non_s_selection(self):
        selection = {
            "selected_by": "codex_direct_arxiv",
            "report_date": "2026-09-04",
            "listing_date": "2026-09-03",
            "grade": "A",
            "score": "30/40",
            "rubric_version": "v1",
        }
        with self.assertRaisesRegex(ValueError, "grade S"):
            build_scaffold(metadata(), "Daily", "theory", "核验测试论文", selection_record=selection)

    def test_write_scaffold_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "draft.json"
            card = build_scaffold(
                metadata(), "Collection", "theory", "核验测试论文", collection_provenance()
            )
            write_scaffold(path, card)
            with self.assertRaises(FileExistsError):
                write_scaffold(path, card)


class MetricsTests(unittest.TestCase):
    def test_stage_receipt_records_duration_tokens_and_artifact_hash(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            receipt = root / "metrics.json"
            artifact = root / "packet.json"
            artifact.write_text("{}\n")
            start_stage(
                receipt,
                "2609.00001",
                "evidence",
                datetime(2026, 9, 4, 1, 0, tzinfo=timezone.utc),
            )
            result = finish_stage(
                receipt,
                "2609.00001",
                "evidence",
                "passed",
                {"input": 5000, "output": 1000, "cached": 400},
                {"packet": artifact},
                now=datetime(2026, 9, 4, 1, 2, tzinfo=timezone.utc),
            )
            self.assertEqual(result["stages"]["evidence"]["duration_seconds"], 120)
            self.assertEqual(result["summary"]["input_tokens"], 5000)
            self.assertEqual(result["summary"]["cached_tokens"], 400)
            self.assertEqual(
                result["stages"]["evidence"]["artifacts"]["packet"]["sha256"],
                hashlib.sha256(b"{}\n").hexdigest(),
            )
            with self.assertRaisesRegex(ValueError, "distinct retry stage name"):
                start_stage(receipt, "2609.00001", "evidence")

    def test_risk_audit_routes_review_without_calling_it_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cards = root / "cards"
            cards.mkdir()
            card = {
                "arxiv_id": "2609.00001",
                "card_standard_version": "2.3",
                "paper_profile": "theory",
                "sections": [{"title": "研究问题", "paragraphs": ["short"]}],
                "equation_refs": [],
                "figure_refs": [],
                "evidence_refs": ["a", "b", "c"],
                "cover": {"mode": "title_abstract"},
            }
            (cards / "2609.00001.json").write_text(json.dumps(card))
            packets = root / "packets" / "2609.00001"
            packets.mkdir(parents=True)
            packet = {
                "campaign_item": {"card_id": "2609.00001"},
                "source": {"pdf_page_count": 75},
                "size": {"approximate_tokens": 7900},
            }
            (packets / "evidence_packet.json").write_text(json.dumps(packet))
            report = audit_cards([cards], [root / "packets"])
            self.assertEqual(report["summary"]["cards"], 1)
            self.assertEqual(report["summary"]["risk_items"], 1)
            self.assertEqual(
                set(report["items"][0]["risks"]),
                {
                    "near_depth_floor",
                    "theory_without_equation_review",
                    "minimum_evidence_only",
                    "evidence_packet_near_cap",
                    "long_paper_review",
                },
            )
            self.assertIn("do not establish", report["boundary"])

    def test_risk_audit_routes_legacy_schema_fields(self):
        with tempfile.TemporaryDirectory() as temporary:
            cards = Path(temporary) / "cards"
            cards.mkdir()
            (cards / "legacy.json").write_text(
                json.dumps({"arxiv_id": "legacy", "sections": [{"paragraphs": ["x" * 2100]}]})
            )
            report = audit_cards([cards])
            self.assertEqual(
                set(report["items"][0]["risks"]),
                {
                    "legacy_standard_review",
                    "missing_or_invalid_profile_review",
                    "missing_cover_review",
                    "minimum_evidence_only",
                },
            )

    def test_risk_audit_routes_malformed_v24_reader_bridge(self):
        with tempfile.TemporaryDirectory() as temporary:
            cards = Path(temporary) / "cards"
            cards.mkdir()
            card = {
                "arxiv_id": "2609.00002",
                "card_standard_version": "2.4",
                "paper_profile": "ai_empirical",
                "sections": [{"title": "研究问题", "paragraphs": ["x" * 2100]}],
                "equation_refs": [],
                "figure_refs": [],
                "evidence_refs": ["a", "b", "c", "d"],
                "cover": {"mode": "title_abstract"},
            }
            (cards / "2609.00002.json").write_text(json.dumps(card))
            report = audit_cards([cards])
            self.assertIn("physicist_reader_bridge_review", report["items"][0]["risks"])
            self.assertEqual(report["summary"]["audience_profiles"], {"missing": 1})


if __name__ == "__main__":
    unittest.main()
