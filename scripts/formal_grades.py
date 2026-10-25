"""Formal reader ratings, independent of historical selection/admission.

The controller owns data/formal_grades.json. Never infer a rating from a card
or a total score, or resolve IDs/versions beyond that file's explicit keys.
"""
from __future__ import annotations

import json
import math
from html import escape
from pathlib import Path


def axis_scores(assessment: dict, axes: list[str]) -> list[float]:
    breakdown = assessment["score_breakdown"]
    if isinstance(breakdown, dict) and set(breakdown) == set(axes):
        return [breakdown[axis] for axis in axes]
    if isinstance(breakdown, list) and len(breakdown) == len(axes):
        return breakdown
    raise ValueError("Formal assessment must contain all eight rubric axes")


def load_formal_grades(path: Path) -> dict:
    if not path.exists():
        return {"assessments": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    rubric = data.get("rubric", {})
    axes = rubric.get("axes", [])
    if (data.get("schema_version") != 1 or rubric.get("max_score") != 40
            or not isinstance(axes, list) or len(axes) != 8
            or not all(isinstance(axis, str) and axis for axis in axes)
            or len(set(axes)) != 8 or not isinstance(data.get("assessments"), dict)):
        raise ValueError("Unsupported formal grading schema/rubric")
    for identifier, assessment in data["assessments"].items():
        try:
            scores = axis_scores(assessment, axes)
            score = assessment["score"]
            if (assessment["grade"] not in ("S", "A", "B")
                    or any(type(value) not in (int, float) or not math.isfinite(value)
                           or not 0 <= value <= 5 for value in scores)
                    or type(score) not in (int, float) or not math.isfinite(score)
                    or abs(sum(scores) - score) > 1e-9):
                raise ValueError("Invalid formal grade/score")
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"Invalid formal assessment: {identifier}") from error
    return data


def attach_formal_grades(records: list[dict], data: dict) -> None:
    for record in records:
        identifier = str(record.get("card_id") or record.get("arxiv_id") or "")
        assessment = data["assessments"].get(identifier)
        record["grade"] = assessment["grade"] if assessment else ""
        record["formal_grade"] = ({**assessment, **data["rubric"]} if assessment else None)


def display_text(value: object) -> str:
    if value is None:
        return "未提供"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def render_formal_grade(record: dict) -> str:
    assessment = record.get("formal_grade")
    if not assessment:
        return '<p class="formal-grade-status">正式评级：未评级</p>'
    def text(value: object) -> str:
        return escape(display_text(value))
    rows = "".join(f'<tr><th scope="row">{text(axis)}</th><td>{score:g} / 5</td></tr>'
                   for axis, score in zip(assessment["axes"], axis_scores(assessment, assessment["axes"])))
    reuse = ('<p class="formal-grade-note">复用 Collection 正式评审；该评级不代表 Daily 准入判定。</p>'
             if record.get("program") == "Daily" and assessment.get("source_program") == "Collection" else "")
    html = f'''<details class="formal-grade">
      <summary>正式评级：{text(assessment["grade"])} · {assessment["score"]:g} / 40</summary>
      <p>评审版本：{text(assessment.get("source_version"))} · 原评审来源：{text(assessment.get("source_program"))}</p>
      {reuse}
      <table><caption>八轴评分（每轴 5 分，满分 40 分）</caption><tbody>{rows}</tbody></table>
      <p>评级理由：{text(assessment.get("rationale"))}</p>
      <p>评审边界：{text(assessment.get("review_boundary"))}</p>
      <p>S级贡献门槛确认：{text({True: "是", False: "否"}.get(assessment.get("load_bearing_contribution_confirmed"), "未提供")) if assessment.get("grade") == "S" else "不适用（当前评级非S）"}</p>
      <details class="formal-grade-evidence"><summary>评审记录</summary>
        <p>Registry 序号：{text(assessment.get("registry_seq"))}</p>
        <p>原文 PDF SHA-256：<code>{text(assessment.get("source_pdf_sha256"))}</code></p>
        <p>评审 SHA-256：<code>{text(assessment.get("assessment_sha256"))}</code></p>
      </details>
    </details>'''
    return '\n'.join(line.rstrip() for line in html.splitlines())
