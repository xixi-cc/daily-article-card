#!/usr/bin/env python3
"""Validate full-text curated card sources and their rendered Markdown rows."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS_MD = ROOT / "papers.md"
CARDS_DIR = ROOT / "data" / "curated_cards"
COLLECTION_CARDS_DIR = ROOT / "data" / "collection_cards"
STANDARD_PATH = ROOT / "docs" / "PAPER_CARD_STANDARD.md"
SITE_PAPERS_DIR = ROOT / "site" / "papers"
SITE_COLLECTION_PAPERS_DIR = ROOT / "site" / "collection-papers"
SITE_MATHJAX_PATH = ROOT / "site" / "assets" / "vendor" / "mathjax" / "tex-chtml.js"
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
V2_PAPER_PROFILES = {
    "theory",
    "theory_numerics",
    "theory_experiment",
    "numerical",
    "experiment",
    "ai_empirical",
}
COVER_VISUAL_TYPES = {
    "real_space",
    "micrograph",
    "simulation_snapshot",
    "field_map",
    "schematic",
    "apparatus",
    "phase_diagram",
    "distribution",
    "trajectory",
    "comparison",
    "data_plot",
    "table",
}


def iter_strings(value: object):
    """Yield decoded strings recursively so escaped control characters cannot hide in JSON."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from iter_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_strings(item)


def is_v2_card(card: dict[str, object]) -> bool:
    version = str(card.get("card_standard_version", "1.0"))
    try:
        return tuple(int(part) for part in version.split(".")) >= (2, 0)
    except ValueError:
        return False


def version_at_least(card: dict[str, object], target: tuple[int, int]) -> bool:
    version = str(card.get("card_standard_version", "1.0"))
    try:
        return tuple(int(part) for part in version.split(".")) >= target
    except ValueError:
        return False


def validate_v2_card(card: dict[str, object], arxiv_id: str, program: str = "Daily") -> list[str]:
    errors: list[str] = []
    profile = str(card.get("paper_profile", ""))
    if profile not in V2_PAPER_PROFILES:
        errors.append(f"{arxiv_id}: invalid or missing paper_profile")

    if card.get("style_reference") != "physicist_daily_arxiv":
        errors.append(f"{arxiv_id}: missing physicist_daily_arxiv style reference")

    selection = card.get("selection_record")
    if program == "Daily" and not isinstance(selection, dict):
        errors.append(f"{arxiv_id}: missing Codex selection_record")
    elif program == "Daily":
        assert isinstance(selection, dict)
        if selection.get("selected_by") != "codex_direct_arxiv":
            errors.append(f"{arxiv_id}: selection_record is not Codex-direct")
        if selection.get("grade") != "S":
            errors.append(f"{arxiv_id}: Daily publication requires grade S")
        for field in ("report_date", "listing_date", "score", "rubric_version"):
            if not selection.get(field):
                errors.append(f"{arxiv_id}: selection_record missing {field}")
    else:
        if selection is not None:
            errors.append(f"{arxiv_id}: Collection card must not contain a Daily selection_record")
        provenance = card.get("provenance")
        if not isinstance(provenance, dict) or provenance.get("program") != "Collection":
            errors.append(f"{arxiv_id}: missing Collection provenance")
        else:
            for field in (
                "catalog",
                "catalog_record_id",
                "catalog_topic",
                "collection_date",
                "sampled_at",
                "selected_by",
                "sampling_seed",
            ):
                if not provenance.get(field):
                    errors.append(f"{arxiv_id}: Collection provenance missing {field}")

    equation_refs = card.get("equation_refs")
    if not isinstance(equation_refs, list):
        errors.append(f"{arxiv_id}: equation_refs must be a list")
    else:
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

    figure_refs = card.get("figure_refs", [])
    if not isinstance(figure_refs, list):
        errors.append(f"{arxiv_id}: figure_refs must be a list")
    else:
        for index, figure in enumerate(figure_refs, start=1):
            if not isinstance(figure, dict):
                errors.append(f"{arxiv_id}: figure_ref {index} is not an object")
                continue
            for field in (
                "label",
                "asset_path",
                "section",
                "role",
                "evidence",
                "alt_text",
                "caption",
                "interpretation",
            ):
                if not figure.get(field):
                    errors.append(f"{arxiv_id}: figure_ref {index} missing {field}")
            asset_path = str(figure.get("asset_path", ""))
            if asset_path and not (ROOT / "site" / asset_path).is_file():
                errors.append(f"{arxiv_id}: figure_ref {index} asset missing: {asset_path}")
            section_names = {
                str(section.get("title", ""))
                for section in card.get("sections", [])
                if isinstance(section, dict)
            }
            if figure.get("section") not in section_names:
                errors.append(f"{arxiv_id}: figure_ref {index} targets a missing section")

    content = json.dumps(card.get("sections", []), ensure_ascii=False)
    if content.count("$$") % 2:
        errors.append(f"{arxiv_id}: unbalanced display-math delimiter")
    if version_at_least(card, (2, 2)):
        if "$$" in content:
            errors.append(f"{arxiv_id}: v2.2 forbids legacy $$ display delimiters")
        decoded_sections = json.dumps(card.get("sections", []), ensure_ascii=False)
        if decoded_sections.count(r"\[") != decoded_sections.count(r"\]"):
            errors.append(f"{arxiv_id}: unbalanced \\[...\\] display delimiters")
        inline_delimiters = re.findall(r"(?<!\\)\$(?!\$)", decoded_sections)
        if len(inline_delimiters) % 2:
            errors.append(f"{arxiv_id}: unbalanced inline-math delimiter")

    if version_at_least(card, (2, 3)):
        if any(any(ord(char) < 32 for char in text) for text in iter_strings(card)):
            errors.append(f"{arxiv_id}: decoded card text contains ASCII control characters")
        cover = card.get("cover")
        if not isinstance(cover, dict):
            errors.append(f"{arxiv_id}: v2.3 requires a structured cover decision")
        else:
            mode = cover.get("mode")
            rationale = str(cover.get("selection_rationale", "")).strip()
            if len(rationale) < 30:
                errors.append(f"{arxiv_id}: cover selection_rationale is too short")
            if mode == "source_figure":
                for field in (
                    "asset_path",
                    "label",
                    "visual_type",
                    "evidence",
                    "alt_text",
                    "caption",
                ):
                    if not cover.get(field):
                        errors.append(f"{arxiv_id}: source_figure cover missing {field}")
                visual_type = str(cover.get("visual_type", ""))
                if visual_type not in COVER_VISUAL_TYPES:
                    errors.append(f"{arxiv_id}: invalid cover visual_type {visual_type!r}")
                asset_path = str(cover.get("asset_path", ""))
                if asset_path and not asset_path.startswith("assets/"):
                    errors.append(f"{arxiv_id}: cover asset must be site-relative")
                if asset_path and not (ROOT / "site" / asset_path).is_file():
                    errors.append(f"{arxiv_id}: cover asset missing: {asset_path}")
            elif mode == "title_abstract":
                abstract_text = str(cover.get("abstract_text", "")).strip()
                if len(abstract_text) < 60:
                    errors.append(f"{arxiv_id}: title_abstract cover text is too short")
                if cover.get("asset_path"):
                    errors.append(f"{arxiv_id}: title_abstract cover must not set asset_path")
            else:
                errors.append(f"{arxiv_id}: invalid cover mode {mode!r}")

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
    daily_paths = sorted(CARDS_DIR.glob("*.json"))
    collection_paths = sorted(COLLECTION_CARDS_DIR.glob("*.json"))

    for program, path in [
        *(('Daily', path) for path in daily_paths),
        *(('Collection', path) for path in collection_paths),
    ]:
        try:
            card = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            errors.append(f"{path.name}: invalid JSON: {error}")
            continue

        arxiv_id = str(card.get("arxiv_id") or card.get("source_id") or path.stem)
        if program == "Collection" and not card.get("arxiv_id"):
            for field in ("card_id", "source_kind", "source_id", "source_url"):
                if not card.get(field):
                    errors.append(f"{path.stem}: non-arXiv Collection card missing {field}")
            if str(card.get("card_id", "")) != path.stem:
                errors.append(f"{path.stem}: card_id must equal its filename stem")
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
            errors.extend(validate_v2_card(card, arxiv_id, program))

        if program == "Daily":
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

    extra_rows = sorted(set(rows) - {path.stem for path in daily_paths})
    if extra_rows:
        errors.append(f"papers.md rows without curated cards: {extra_rows}")
    # A work may belong to both programs, provided each copy carries the
    # program-specific provenance validated above. Collection membership must
    # never promote a paper into Daily or inherit its Daily score/date.

    if SITE_PAPERS_DIR.exists() or SITE_COLLECTION_PAPERS_DIR.exists():
        missing_math = []
        detail_paths = [
            *SITE_PAPERS_DIR.glob("*/index.html"),
            *SITE_COLLECTION_PAPERS_DIR.glob("*/index.html"),
        ]
        for detail_path in detail_paths:
            site_html = detail_path.read_text(encoding="utf-8")
            if (
                "assets/vendor/mathjax/tex-chtml.js" not in site_html
                or "window.MathJax" not in site_html
                or "cdn.jsdelivr.net/npm/mathjax" in site_html
            ):
                missing_math.append(detail_path.parent.name)
        if missing_math:
            errors.append(
                f"generated detail pages missing MathJax: {missing_math[:5]}"
            )
        if detail_paths and not SITE_MATHJAX_PATH.is_file():
            errors.append("generated site missing packaged MathJax runtime")
    if errors:
        raise SystemExit("\n".join(errors))
    print(
        f"Validated {len(daily_paths)} Daily and {len(collection_paths)} Collection "
        f"full-text cards: strict JSON, provenance, evidence refs, minimum depth, "
        f"and rendered parity"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
