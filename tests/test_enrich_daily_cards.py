import unittest
from urllib.error import URLError

from scripts.enrich_daily_cards import arxiv_id_from_entry_url, enrich_text


def card(with_metadata=True):
    value = {
        "arxiv_id": "2608.99999",
        "source_version": "v1",
        "title_en": "Verified Offline Paper",
        "title_zh": "离线核验论文",
        "curation_status": "full_text_verified",
        "sections": [{"title": "摘要", "paragraphs": ["已核验内容。"]}],
    }
    if with_metadata:
        value["verified_metadata"] = {
            "arxiv_id": "2608.99999",
            "version": "v1",
            "title": "Verified Offline Paper",
            "authors": ["A. Author"],
            "published": "2026-08-20T00:00:00Z",
            "primary_category": "cs.LG",
            "categories": ["cs.LG"],
            "abstract": "Official abstract.",
        }
    return value


SOURCE = (
    "| 日期 | 标题 | 链接 | 简要总结 |\n"
    "| --- | --- | --- | --- |\n"
    "| 2026-08-21 | placeholder | https://arxiv.org/abs/2608.99999 | placeholder |\n"
)


class OfflineEnrichmentTests(unittest.TestCase):
    def test_legacy_arxiv_id_keeps_archive_prefix(self):
        self.assertEqual(
            arxiv_id_from_entry_url("http://arxiv.org/abs/cond-mat/0107443v2"),
            "cond-mat/0107443v2",
        )

    def test_complete_verified_metadata_never_calls_network(self):
        def forbidden(_ids):
            raise AssertionError("network must not be called")

        rendered = enrich_text(SOURCE, {}, {"2608.99999": card()}, forbidden)
        self.assertIn("离线核验论文<br>Verified Offline Paper", rendered)
        self.assertIn("## 摘要<br>已核验内容。", rendered)

    def test_network_failure_is_fail_closed_when_local_evidence_missing(self):
        def unavailable(ids):
            self.assertEqual(ids, ["2608.99999"])
            raise URLError("offline")

        with self.assertRaises(URLError):
            enrich_text(SOURCE, {}, {"2608.99999": card(False)}, unavailable)

    def test_mismatched_local_title_fails_without_network(self):
        value = card()
        value["verified_metadata"]["title"] = "Different Official Title"
        with self.assertRaisesRegex(ValueError, "title mismatch"):
            enrich_text(SOURCE, {}, {"2608.99999": value}, lambda _ids: {})


if __name__ == "__main__":
    unittest.main()
