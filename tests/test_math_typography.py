import unittest

from scripts.math_typography import normalize_inline_math_notation


class MathTypographyTests(unittest.TestCase):
    def test_wraps_subscripts_relations_groups_and_greek(self) -> None:
        text = "把 p_init 输运到 p_data；当 h→0 时在 SE(3) 上扫描 β。"
        rendered = normalize_inline_math_notation(text)
        self.assertIn(r"\(p_{\mathrm{init}}\)", rendered)
        self.assertIn(r"\(p_{\mathrm{data}}\)", rendered)
        self.assertIn(r"\(h\to 0\)", rendered)
        self.assertIn(r"\(\mathrm{SE}(3)\)", rendered)
        self.assertIn(r"\(\beta\)", rendered)

    def test_preserves_authored_math_urls_and_code(self) -> None:
        text = r"保留 \(x_t\)、$J=0$ 与 https://example.org/p_init，也保留 `p_data`。"
        self.assertEqual(normalize_inline_math_notation(text), text)

    def test_wraps_compact_equation_once(self) -> None:
        rendered = normalize_inline_math_notation("使用 dX_t=u_t(X_t)dt。")
        self.assertEqual(rendered.count(r"\("), 1)
        self.assertEqual(rendered.count(r"\)"), 1)

    def test_wraps_differential_operator_with_argument(self) -> None:
        rendered = normalize_inline_math_notation("边界是 ∂A(x0)，梯度为 ∇f。")
        self.assertIn(r"\(\partial A(x_{0})\)", rendered)
        self.assertIn(r"\(\nabla f\)", rendered)

    def test_wraps_common_standalone_variables(self) -> None:
        rendered = normalize_inline_math_notation("表示 T 对输入 X 和标签 Y 的信息。")
        self.assertEqual(rendered, r"表示 \(T\) 对输入 \(X\) 和标签 \(Y\) 的信息。")


if __name__ == "__main__":
    unittest.main()
