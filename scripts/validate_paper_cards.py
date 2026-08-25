#!/usr/bin/env python3
"""Validate full-text curated card sources and their rendered Markdown rows."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS_MD = ROOT / "papers.md"
CARDS_DIR = ROOT / "data" / "curated_cards"
STANDARD_PATH = ROOT / "docs" / "PAPER_CARD_STANDARD.md"
SITE_PAPERS_DIR = ROOT / "site" / "papers"
REQUIRED_CORE = {
    "作者信息",
    "模型与方法",
    "有效性与局限",
    "复现与资源",
    "阅读指南",
}
QUESTION_HEADINGS = {"研究问题", "摘要"}
RESULT_HEADINGS = {"核心结果与证据", "核心定理与证据"}
FORBIDDEN_PHRASES = (
    "。。。",
    "自动文本抽取",
    "技术对象：",
    "未能从 PDF",
    "待从全文核验",
    "尚未逐项绑定",
)
MIN_CONTENT_CHARS = 1_800
V2_THEORY_PROFILES = {"theory", "theory_numerics", "theory_experiment"}
V2_EQUATION_MINIMUM = {
    "theory": 3,
    "theory_numerics": 3,
    "theory_experiment": 3,
    "numerical": 2,
    "experiment": 1,
    "ai_empirical": 1,
}


def count_math_expressions(content: str) -> int:
    """Count display and inline TeX without double-counting ``$$...$$``."""
    display_pattern = re.compile(r"\$\$.*?\$\$|\\\[.*?\\\]", re.DOTALL)
    display_count = len(display_pattern.findall(content))
    without_display = display_pattern.sub("", content)
    inline_pattern = re.compile(
        r"(?<!\\)\$(?!\$).+?(?<!\\)\$(?!\$)|\\\(.*?\\\)",
        re.DOTALL,
    )
    return display_count + len(inline_pattern.findall(without_display))


def is_v2_card(card: dict[str, object]) -> bool:
    version = str(card.get("card_standard_version", "1.0"))
    try:
        return tuple(int(part) for part in version.split(".")) >= (2, 0)
    except ValueError:
        return False


def validate_v2_card(card: dict[str, object], arxiv_id: str) -> list[str]:
    errors: list[str] = []
    profile = str(card.get("paper_profile", ""))
    if profile not in V2_EQUATION_MINIMUM:
        errors.append(f"{arxiv_id}: invalid or missing paper_profile")

    if card.get("style_reference") != "physicist_daily_arxiv":
        errors.append(f"{arxiv_id}: missing physicist_daily_arxiv style reference")

    selection = card.get("selection_record")
    if not isinstance(selection, dict):
        errors.append(f"{arxiv_id}: missing Codex selection_record")
    else:
        if selection.get("selected_by") != "codex_direct_arxiv":
            errors.append(f"{arxiv_id}: selection_record is not Codex-direct")
        if selection.get("grade") != "S":
            errors.append(f"{arxiv_id}: Daily publication requires grade S")
        for field in ("report_date", "listing_date", "score", "rubric_version"):
            if not selection.get(field):
                errors.append(f"{arxiv_id}: selection_record missing {field}")

    equation_refs = card.get("equation_refs")
    minimum = V2_EQUATION_MINIMUM.get(profile, 1)
    if not isinstance(equation_refs, list) or len(equation_refs) < minimum:
        errors.append(
            f"{arxiv_id}: {profile or 'unknown'} card needs at least {minimum} equation_refs"
        )
    else:
        roles: set[str] = set()
        for index, equation in enumerate(equation_refs, start=1):
            if not isinstance(equation, dict):
                errors.append(f"{arxiv_id}: equation_ref {index} is not an object")
                continue
            for field in ("label", "latex", "role", "evidence", "interpretation"):
                if not equation.get(field):
                    errors.append(f"{arxiv_id}: equation_ref {index} missing {field}")
            symbols = equation.get("symbols")
            if not isinstance(symbols, dict) or not symbols:
                errors.append(f"{arxiv_id}: equation_ref {index} missing symbol definitions")
            roles.add(str(equation.get("role", "")))

        if profile in V2_THEORY_PROFILES:
            if not roles & {"model", "definition", "governing_equation"}:
                errors.append(f"{arxiv_id}: theory card lacks a model/definition equation")
            if not roles & {"central_result", "scaling_law", "bound", "theorem"}:
                errors.append(f"{arxiv_id}: theory card lacks a result equation")

    content = json.dumps(card.get("sections", []), ensure_ascii=False)
    math_expression_count = count_math_expressions(content)
    if math_expression_count < minimum:
        errors.append(
            f"{arxiv_id}: card prose contains {math_expression_count} rendered equations; "
            f"needs {minimum}"
        )
    if content.count("$$") % 2:
        errors.append(f"{arxiv_id}: unbalanced display-math delimiter")

    return errors


def rendered_rows() -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in PAPERS_MD.read_text(encoding="utf-8").splitlines()[2:]:
        if not line.startswith("|"):
            continue
        match = re.search(r"arxiv.org/abs/(\d{4}\.\d{4,5})", line)
        if match:
            rows[match.group(1)] = line
    return rows


def main() -> int:
    errors: list[str] = []
    if not STANDARD_PATH.exists():
        errors.append("missing canonical docs/PAPER_CARD_STANDARD.md")
    rows = rendered_rows()
    paths = sorted(CARDS_DIR.glob("*.json"))

    for path in paths:
        try:
            card = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            errors.append(f"{path.name}: invalid JSON: {error}")
            continue

        arxiv_id = str(card.get("arxiv_id", ""))
        sections = card.get("sections", [])
        titles = [section.get("title") for section in sections if isinstance(section, dict)]
        title_set = set(titles)
        missing = REQUIRED_CORE - title_set
        if missing:
            errors.append(f"{arxiv_id}: missing sections {sorted(missing)}")
        if not (title_set & QUESTION_HEADINGS):
            errors.append(f"{arxiv_id}: missing research question or abstract")
        if not (title_set & RESULT_HEADINGS):
            errors.append(f"{arxiv_id}: missing evidence-bearing results section")
        if card.get("curation_status") != "full_text_verified":
            errors.append(f"{arxiv_id}: curation_status is not full_text_verified")

        evidence_refs = card.get("evidence_refs", [])
        if not isinstance(evidence_refs, list) or len(evidence_refs) < 3:
            errors.append(f"{arxiv_id}: insufficient evidence_refs")
        elif not any("no independent reproduction" in str(ref) for ref in evidence_refs):
            errors.append(f"{arxiv_id}: missing independent-reproduction boundary")

        content = json.dumps(sections, ensure_ascii=False)
        if len(content) < MIN_CONTENT_CHARS:
            errors.append(f"{arxiv_id}: content too short ({len(content)} chars)")
        for phrase in FORBIDDEN_PHRASES:
            if phrase in content:
                errors.append(f"{arxiv_id}: placeholder phrase {phrase!r}")

        if is_v2_card(card):
            errors.extend(validate_v2_card(card, arxiv_id))

        row = rows.get(arxiv_id)
        if row is None:
            errors.append(f"{arxiv_id}: missing from papers.md")
            continue
        rendered_titles = re.findall(r"## ([^<]+)<br>", row)
        if rendered_titles != titles:
            errors.append(
                f"{arxiv_id}: rendered headings differ: {rendered_titles} != {titles}"
            )
        if card.get("title_zh") not in row or card.get("title_en") not in row:
            errors.append(f"{arxiv_id}: rendered title differs from curated source")

    extra_rows = sorted(set(rows) - {path.stem for path in paths})
    if extra_rows:
        errors.append(f"papers.md rows without curated cards: {extra_rows}")
    if SITE_PAPERS_DIR.exists():
        missing_math = []
        for detail_path in SITE_PAPERS_DIR.glob("*/index.html"):
            site_html = detail_path.read_text(encoding="utf-8")
            if "tex-chtml.js" not in site_html or "window.MathJax" not in site_html:
                missing_math.append(detail_path.parent.name)
        if missing_math:
            errors.append(
                f"generated detail pages missing MathJax: {missing_math[:5]}"
            )
    if errors:
        raise SystemExit("\n".join(errors))
    print(
        f"Validated {len(paths)} full-text cards: strict JSON, evidence refs, "
        f"minimum depth, and rendered Markdown parity"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
