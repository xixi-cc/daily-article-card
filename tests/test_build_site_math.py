import unittest

from scripts.build_site import (
    generate_head,
    markdown_to_html,
    render_detail_sections,
    render_note_cover,
    render_source_cover,
)
from scripts.validate_paper_cards import validate_v2_card


class MathRenderingTests(unittest.TestCase):
    def test_head_loads_site_local_mathjax_with_dollar_delimiters(self):
        head = generate_head("Title", "Description", "../../", include_math=True)
        self.assertIn("../../assets/vendor/mathjax/tex-chtml.js", head)
        self.assertNotIn("cdn.jsdelivr.net", head)
        self.assertIn("inlineMath: [['$', '$']", head)
        self.assertIn("displayMath: [['$$', '$$']", head)
        self.assertIn("dataset.mathReady = 'true'", head)

    def test_non_detail_head_does_not_load_mathjax(self):
        head = generate_head("Title", "Description")
        self.assertNotIn("tex-chtml.js", head)

    def test_markdown_preserves_inline_tex_for_mathjax(self):
        rendered = markdown_to_html(r"模型为 $\partial_t\rho+\nabla\cdot\mathbf J=0$。")
        self.assertIn(r"$\partial_t\rho+\nabla\cdot\mathbf J=0$", rendered)

    def test_markdown_preserves_display_tex_for_mathjax(self):
        rendered = markdown_to_html(r"\[S(k)\sim k^{-2+\eta}\]")
        self.assertIn(r"\[S(k)\sim k^{-2+\eta}\]", rendered)

    def test_detail_section_places_evidence_figure_by_claim(self):
        record = {
            "sections": [{"title": "核心结果与证据", "html": "<p>claim</p>"}],
            "figure_refs": [{
                "label": "Figure 7",
                "asset_path": "assets/collection-figures/test.webp",
                "section": "核心结果与证据",
                "alt_text": "test figure",
                "caption": "what is plotted",
                "interpretation": "physical reading",
                "evidence": "paper.pdf p. 13, Figure 7",
            }],
        }
        rendered = render_detail_sections(record)
        self.assertIn("../../assets/collection-figures/test.webp", rendered)
        self.assertIn("物理解读：physical reading", rendered)

    def test_v2_theory_card_has_no_formula_quota(self):
        card = {
            "paper_profile": "theory",
            "style_reference": "physicist_daily_arxiv",
            "selection_record": {
                "selected_by": "codex_direct_arxiv",
                "grade": "S",
                "report_date": "2026-08-25",
                "listing_date": "2026-08-25",
                "score": 36,
                "rubric_version": "1.0",
            },
            "equation_refs": [],
            "sections": [],
        }
        errors = validate_v2_card(card, "test")
        self.assertFalse(any("equation" in error for error in errors), errors)

    def test_title_abstract_cover_contains_both_elements(self):
        record = {
            "title": "The inconvenient truth about flocks",
            "title_zh": "关于鸟群理论的不便真相",
            "cover_summary": "对称性只给出两条精确标度关系，不能封闭三个指数。",
            "cover_theme": {"from": "#000", "to": "#333"},
        }
        rendered = render_note_cover(record)
        self.assertIn("TITLE · ABSTRACT", rendered)
        self.assertIn("对称性只给出两条精确标度关系", rendered)

    def test_source_cover_uses_structured_figure_metadata(self):
        record = {
            "title": "Probability flows",
            "title_zh": "概率流",
            "cover_label": "Figure 7",
            "cover_alt_text": "MIPS interface field map",
        }
        rendered = render_source_cover(record, "../../assets/figure.webp")
        self.assertIn("../../assets/figure.webp", rendered)
        self.assertIn("Figure 7", rendered)
        self.assertIn("MIPS interface field map", rendered)

    def test_v23_card_requires_cover_decision(self):
        card = {
            "card_standard_version": "2.3",
            "paper_profile": "theory",
            "style_reference": "physicist_daily_arxiv",
            "selection_record": {
                "selected_by": "codex_direct_arxiv",
                "grade": "S",
                "report_date": "2026-08-26",
                "listing_date": "2026-08-26",
                "score": 36,
                "rubric_version": "1.0",
            },
            "equation_refs": [],
            "figure_refs": [],
            "sections": [],
        }
        errors = validate_v2_card(card, "test")
        self.assertTrue(any("structured cover" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
