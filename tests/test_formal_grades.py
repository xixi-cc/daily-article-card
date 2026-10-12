import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.formal_grades import load_formal_grades, attach_formal_grades, render_formal_grade
from scripts.card_presentation import presentation_fields, merge_reader_lists
from scripts.build_site import build_list_data, generate_index_html


AXES = [f"评分轴{i}" for i in range(8)]


def dataset():
    return {
        "schema_version": 1,
        "rubric": {"axes": AXES, "max_score": 40},
        "assessments": {"1234.56789": {
            "grade": "B", "score": 40, "score_breakdown": [5] * 8,
            "source_version": "v2", "source_program": "Collection",
            "source_pdf_sha256": "a" * 64, "assessment_sha256": "b" * 64,
            "registry_seq": 123, "rationale": "<script>仅有限模型</script>",
            "review_boundary": "未独立复现", "load_bearing_contribution_confirmed": False,
        }},
    }


class FormalGradeTests(unittest.TestCase):
    def load(self, data):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "formal_grades.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            return load_formal_grades(path)

    def test_accepted_letter_is_not_inferred_from_total(self):
        data = self.load(dataset())
        records = [{"card_id": "1234.56789", "program": "Daily", "grade": "S"}]
        attach_formal_grades(records, data)
        self.assertEqual(records[0]["grade"], "B")
        html = render_formal_grade(records[0])
        self.assertIn("B · 40 / 40", html)
        self.assertEqual(html.count('<th scope="row">'), 8)
        for value in ("v2", "Collection", "不代表 Daily 准入", "未独立复现", "a" * 64, "b" * 64):
            self.assertIn(value, html)
        self.assertNotIn("<script>", html)

    def test_missing_formal_never_uses_history_or_alias(self):
        card = {"selection_record": {"grade": "S"}, "editorial_assessment": {"grade": "A"}}
        before = copy.deepcopy(card)
        self.assertEqual(presentation_fields(card, {"card_id": "1234.56789"})["grade"], "")
        records = [{"card_id": "1234.56789v2", "grade": "S"}, {"card_id": "missing", "grade": "A"}]
        attach_formal_grades(records, self.load(dataset()))
        self.assertEqual(len(records), 2)
        for record in records:
            self.assertEqual(record["grade"], "")
            self.assertIsNone(record["formal_grade"])
            self.assertIn("未评级", render_formal_grade(record))
        self.assertEqual(card, before)
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(load_formal_grades(Path(directory) / "missing.json"), {"assessments": {}})

    def test_axis_order_and_invalid_inputs(self):
        data = dataset()
        data["assessments"]["1234.56789"]["score_breakdown"] = dict(reversed([(axis, 5) for axis in AXES]))
        self.load(data)
        for change in ("sum", "missing-axis", "grade", "schema"):
            bad = dataset()
            if change == "sum": bad["assessments"]["1234.56789"]["score"] = 39
            if change == "missing-axis": bad["assessments"]["1234.56789"]["score_breakdown"].pop()
            if change == "grade": bad["assessments"]["1234.56789"]["grade"] = "C"
            if change == "schema": bad["schema_version"] = 2
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.load(bad)

    def test_formal_rating_follows_existing_merge_detail(self):
        base = {"arxiv_id": "1234.56789", "grade": "S", "formal_grade": {"grade": "S", "source_version": "v1"}}
        daily = {**base, "program": "Daily", "detail_path": "papers/id/", "paper_image_path": ""}
        collection = {**base, "program": "Collection", "detail_path": "collection-papers/id/", "paper_image_path": "image.webp", "grade": "B", "formal_grade": {"grade": "B", "source_version": "v2"}}
        merged = merge_reader_lists([daily], [collection])[0]
        self.assertEqual(merged["detail_path"], collection["detail_path"])
        self.assertEqual(merged["formal_grade"], collection["formal_grade"])
        self.assertEqual(merged["grade"], "B")

    def test_list_serialization_carries_same_assessment_as_detail(self):
        record = {key: "" for key in ("date", "title", "title_zh", "link", "arxiv_id", "detail_path", "cover_path", "paper_image_path", "preview_text", "research_unit", "hook_text", "cover_theme")}
        record.update(card_id="1234.56789", program="Daily", key_points=[], reading_minutes=1, section_count=1)
        attach_formal_grades([record], self.load(dataset()))
        item = build_list_data([record])[0]
        self.assertEqual(item["formal_grade"], record["formal_grade"])
        self.assertEqual(item["grade"], "B")
        self.assertIn('value="ungraded"', generate_index_html())


if __name__ == "__main__":
    unittest.main()
