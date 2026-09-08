import unittest
from datetime import date

from scripts.collect_arxiv_daily_inventory import parse_listing_day


class ListingParserTests(unittest.TestCase):
    def test_parses_primary_category_and_title(self) -> None:
        html = """
        <h3>Fri, 28 Aug 2026 (showing 1 of 1 entries)</h3>
        <dt><a href="/abs/2608.26556" title="Abstract">arXiv:2608.26556</a></dt>
        <dd><div class="meta">
          <div class="list-title mathjax"><span class="descriptor">Title:</span> A Phase Theory </div>
          <div class="list-subjects"><span class="primary-subject">Disordered Systems (cond-mat.dis-nn)</span></div>
        </div></dd>
        <h3>Thu, 27 Aug 2026</h3>
        """
        result = parse_listing_day(html, date(2026, 8, 28), "cond-mat.dis-nn")
        self.assertEqual(result[0]["arxiv_id"], "2608.26556")
        self.assertEqual(result[0]["title"], "A Phase Theory")
        self.assertEqual(result[0]["primary_category"], "cond-mat.dis-nn")

    def test_accepts_single_digit_day_with_or_without_leading_zero(self) -> None:
        for rendered_day in ("2", "02"):
            with self.subTest(rendered_day=rendered_day):
                html = f"""
                <h3>Wed, {rendered_day} Sep 2026 (showing 1 of 1 entries)</h3>
                <dt><a href="/abs/2609.00001" title="Abstract">arXiv:2609.00001</a></dt>
                <dd><div class="meta">
                  <div class="list-title mathjax"><span class="descriptor">Title:</span> September Paper </div>
                  <div class="list-subjects"><span class="primary-subject">Machine Learning (cs.LG)</span></div>
                </div></dd>
                """
                result = parse_listing_day(html, date(2026, 9, 2), "cs.LG")
                self.assertEqual(result[0]["arxiv_id"], "2609.00001")


if __name__ == "__main__":
    unittest.main()
