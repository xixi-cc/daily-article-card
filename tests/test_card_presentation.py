import unittest

from scripts.card_presentation import date_value, chinese_preview, presentation_fields, merge_reader_lists, reader_metadata
from scripts.build_site import generate_index_html, render_detail_sections


class ReaderPresentationTests(unittest.TestCase):
    def test_no_invented_dates_or_collection_grades(self):
        self.assertEqual(date_value("2026"), "2026")
        self.assertEqual(date_value("2026-09"), "2026-09")
        self.assertEqual(date_value("2026-02-30"), "")
        self.assertEqual(date_value("2026-09-02T00:00:00Z"), "2026-09-02")
        fields = presentation_fields({"provenance": {"collection_date": "2026-09"}}, {"program": "Collection"})
        self.assertEqual(fields["grade"], "")
        self.assertEqual(fields["collection_date"], "")

    def test_problem_is_preview_instead_of_author_bookkeeping(self):
        card = {"sections": [{"title": "作者信息", "paragraphs": ["作者：某某。官方列表制作记录。"]},
                             {"title": "研究问题", "paragraphs": [r"研究随机场 \(\phi(x)\) 的涨落。结果仅适用于低温。"]}]}
        preview = chinese_preview(card)
        self.assertIn("研究随机场", preview)
        self.assertIn("仅适用于低温", preview)
        self.assertNotIn("官方列表", preview)

    def test_math_with_sentence_punctuation_is_never_split(self):
        formula = r"\(\text{第一句。第二句！} + y\)"
        card = {"sections": [{"title": "摘要", "paragraphs": ["研究" + formula + "。" + "后文" * 180 + "。"]}]}
        preview = chinese_preview(card)
        self.assertIn(formula, preview)
        self.assertEqual(preview.count(r"\("), preview.count(r"\)"))

    def test_published_citation_survives_author_section_removal(self):
        metadata = reader_metadata({"verified_metadata": {"doi": "10.example/paper", "comment": "Journal of Physics 247, 76 (2023); open access"}}, "doi-example")
        self.assertEqual(metadata["journal"], "Journal of Physics 247, 76 (2023)")
        self.assertEqual(metadata["citation_publication_year"], "2023")
        self.assertNotEqual(reader_metadata({"verified_metadata": {"doi": "10.example/paper"}}, "doi-example")["journal"], "预印本")

    def test_dedup_preserves_independent_provenance_and_favorites(self):
        base = {"arxiv_id": "1234.56789", "grade": "", "published": "2024", "paper_image_path": ""}
        daily = {**base, "program": "Daily", "detail_path": "papers/1234.56789/", "grade": "S", "collection_date": "2026-09-01"}
        collection = {**base, "program": "Collection", "detail_path": "collection-papers/1234.56789/", "paper_image_path": "assets/test.webp", "collection_date": "2026-08-01"}
        result = merge_reader_lists([daily], [collection])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["grade"], "S")
        self.assertEqual(result[0]["collection_date"], "2026-09-01")
        self.assertEqual(result[0]["source_records"][1]["grade"], "")
        self.assertEqual(result[0]["favorite_keys"], ["daily:1234.56789", "collection:1234.56789"])
        self.assertEqual(result[0]["paper_image_path"], "assets/test.webp")

    def test_legacy_entry_points_share_controls_and_do_not_show_source_switch(self):
        for mode in ("Daily", "Collection"):
            html = generate_index_html(mode)
            self.assertIn('id="browse-mode"', html)
            self.assertIn('id="grade-filter"', html)
            self.assertIn('id="pagination"', html)
            self.assertNotIn('id="favorites-export"', html)
            self.assertNotIn("每日自动更新", html)
            self.assertNotIn('>Collection</a>', html)

    def test_sections_keep_science_with_simple_heading(self):
        html = render_detail_sections({"authors": "A", "sections": [
            {"title": "作者信息", "html": "<p>制作日志</p>"},
            {"title": "模型与方法", "html": "<p>原有模型和条件。</p>"}]})
        self.assertIn("原有模型和条件", html)
        self.assertNotIn("制作日志", html)
        self.assertNotIn("Card 0", html)
        self.assertNotIn("reading-step-note", html)


if __name__ == "__main__":
    unittest.main()
