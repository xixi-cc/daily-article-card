import unittest

from scripts.card_taxonomy import classify_card


class CardTaxonomyTests(unittest.TestCase):
    def test_robotics_category_and_tags(self) -> None:
        card = {
            "paper_profile": "ai_empirical",
            "title_en": "A world model for robot manipulation",
            "verified_metadata": {"categories": ["cs.RO", "cs.LG"], "primary_category": "cs.RO"},
        }
        result = classify_card(card)
        self.assertEqual(result["category"], "机器人与具身智能")
        self.assertIn("机器人", result["tags"])
        self.assertIn("世界模型", result["tags"])

    def test_physics_ai_cross_domain(self) -> None:
        card = {
            "paper_profile": "theory_numerics",
            "title_en": "Statistical mechanics of representation learning",
            "verified_metadata": {
                "categories": ["cond-mat.stat-mech", "cs.LG"],
                "primary_category": "cond-mat.stat-mech",
            },
        }
        result = classify_card(card)
        self.assertEqual(result["category"], "AI for Science")
        self.assertEqual(result["research_type"], "理论与数值")
        self.assertIn("统计物理", result["tags"])

    def test_fallback_supplies_legacy_metadata(self) -> None:
        daily = {"title_en": "A theory of generalization"}
        collection = {
            "paper_profile": "theory",
            "verified_metadata": {"categories": ["cs.LG"], "primary_category": "cs.LG"},
        }
        result = classify_card(daily, collection)
        self.assertEqual(result["category"], "AI 基础理论")
        self.assertIn("泛化理论", result["tags"])

    def test_ai_theory_cross_listed_in_math_stays_ai(self) -> None:
        card = {
            "title_en": "A Mean-Field Theory of Transformers",
            "paper_profile": "theory",
            "verified_metadata": {
                "primary_category": "math.AP",
                "categories": ["math.AP", "cs.LG"],
            },
        }
        self.assertEqual(classify_card(card)["category"], "AI 基础理论")

    def test_mckean_vlasov_does_not_trigger_vla_robotics(self) -> None:
        card = {
            "title_en": "Mean-field Transformer dynamics",
            "paper_profile": "theory",
            "verified_metadata": {
                "primary_category": "math.AP",
                "categories": ["math.AP", "cs.LG"],
                "abstract": "We prove a McKean-Vlasov limit for attention training.",
            },
        }
        self.assertEqual(classify_card(card)["category"], "AI 基础理论")


if __name__ == "__main__":
    unittest.main()
