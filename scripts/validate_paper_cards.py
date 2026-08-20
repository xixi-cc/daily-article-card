#!/usr/bin/env python3
"""Validate full-text curated card sources and their rendered Markdown rows."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS_MD = ROOT / "papers.md"
CARDS_DIR = ROOT / "data" / "curated_cards"
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
    if errors:
        raise SystemExit("\n".join(errors))
    print(
        f"Validated {len(paths)} full-text cards: strict JSON, evidence refs, "
        f"minimum depth, and rendered Markdown parity"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
