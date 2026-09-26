"""Regression coverage for publication records missed by the old link ledger."""
import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/build_collection_card_link_ledger.py"
spec = importlib.util.spec_from_file_location("collection_link_ledger", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CollectionLinkIdentityTests(unittest.TestCase):
    def test_publication_doi_matches_verified_card_metadata(self):
        catalog = {"url": "https://doi.org/10.1038/S42256-024-00937-0"}
        card = {"verified_metadata": {"doi": "10.1038/s42256-024-00937-0"}}
        self.assertIn("doi:10.1038/s42256-024-00937-0",
                      module.work_keys(catalog) & module.work_keys(card))

    def test_repository_title_suffix_does_not_hide_same_work(self):
        catalog = {"title": "Active Ising Models of flocking: a field-theoretic approach - PMC"}
        card = {"title_en": "Active Ising Models of flocking: a field-theoretic approach"}
        self.assertTrue(module.work_keys(catalog) & module.work_keys(card))
        self.assertFalse(module.work_keys({"title": "A different paper"}) &
                         module.work_keys({"title": "A different paper with a correction"}))

    def test_arxiv_version_and_site_card_links(self):
        self.assertIn("arxiv:2608.22197", module.work_keys({
            "url": "https://arxiv.org/abs/2608.22197v2"}))
        self.assertNotIn("arxiv:2608.22197", module.work_keys({
            "links": {"card": "https://example.com/papers/2608.22197/"}}))


if __name__ == "__main__":
    unittest.main()
