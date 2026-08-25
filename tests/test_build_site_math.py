import unittest

from scripts.build_site import generate_head, markdown_to_html


class MathRenderingTests(unittest.TestCase):
    def test_head_loads_pinned_mathjax_with_dollar_delimiters(self):
        head = generate_head("Title", "Description", include_math=True)
        self.assertIn("mathjax@3.2.2/es5/tex-chtml.js", head)
        self.assertIn("inlineMath: [['$', '$']", head)
        self.assertIn("displayMath: [['$$', '$$']", head)

    def test_non_detail_head_does_not_load_mathjax(self):
        head = generate_head("Title", "Description")
        self.assertNotIn("tex-chtml.js", head)

    def test_markdown_preserves_inline_tex_for_mathjax(self):
        rendered = markdown_to_html(r"模型为 $\partial_t\rho+\nabla\cdot\mathbf J=0$。")
        self.assertIn(r"$\partial_t\rho+\nabla\cdot\mathbf J=0$", rendered)

    def test_markdown_preserves_display_tex_for_mathjax(self):
        rendered = markdown_to_html(r"$$S(k)\sim k^{-2+\eta}$$")
        self.assertIn(r"$$S(k)\sim k^{-2+\eta}$$", rendered)


if __name__ == "__main__":
    unittest.main()
