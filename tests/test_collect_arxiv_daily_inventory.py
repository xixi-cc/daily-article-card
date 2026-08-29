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


if __name__ == "__main__":
    unittest.main()
