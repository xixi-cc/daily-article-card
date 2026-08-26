#!/usr/bin/env python3
"""Upgrade legacy full-text cards into independent v2.3 Collection cards."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ARXIV_PATTERN = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})")


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def record_arxiv_id(record: dict[str, object]) -> str | None:
    links = record.get("links")
    candidates = [record.get("url", "")]
    if isinstance(links, dict):
        candidates.insert(0, links.get("arxiv", ""))
    for candidate in candidates:
        match = ARXIV_PATTERN.search(str(candidate))
        if match:
            return match.group(1)
    return None


def display_math_v23(value: object) -> object:
    if isinstance(value, str):
        return re.sub(r"\$\$([\s\S]*?)\$\$", r"\\[\1\\]", value)
    if isinstance(value, list):
        return [display_math_v23(item) for item in value]
    if isinstance(value, dict):
        return {key: display_math_v23(item) for key, item in value.items()}
    return value


def cover_abstract(card: dict[str, object]) -> str:
    metadata = card.get("verified_metadata")
    if isinstance(metadata, dict):
        abstract = " ".join(str(metadata.get("abstract", "")).split())
        if len(abstract) >= 60:
            return abstract[:900]
    for section in card.get("sections", []):
        if not isinstance(section, dict) or section.get("title") not in {"摘要", "研究问题"}:
            continue
        entries = section.get("bullets") or section.get("paragraphs") or []
        abstract = " ".join(str(item).strip() for item in entries if str(item).strip())
        if len(abstract) >= 60:
            return abstract[:900]
    raise ValueError(f"{card.get('arxiv_id')}: no evidence-grounded cover abstract")


def paper_profile(record: dict[str, object], card: dict[str, object]) -> str:
    text = " ".join(
        [str(record.get("title", "")), *(str(tag) for tag in record.get("tags", []))]
    ).casefold()
    content = json.dumps(card.get("sections", []), ensure_ascii=False).casefold()
    if any(term in text for term in ("experiment", "robot", "vision-language-action")):
        return "ai_empirical"
    if any(term in text for term in ("neural", "learning", "transformer", "diffusion", "flow matching")):
        return "ai_empirical"
    if any(term in content for term in ("实验", "experiment")) and any(
        term in content for term in ("理论", "方程", "theory")
    ):
        return "theory_experiment"
    if any(term in content for term in ("数值", "simulation", "numerical")):
        return "theory_numerics"
    return "theory"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--legacy-dir", type=Path, required=True)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--migration-date", default="2026-08-26")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    records = load_json(args.catalog)
    if not isinstance(records, list):
        raise SystemExit("catalog must be a JSON list")
    by_arxiv: dict[str, list[dict[str, object]]] = {}
    for record in records:
        paper_id = record_arxiv_id(record)
        if paper_id:
            by_arxiv.setdefault(paper_id, []).append(record)

    planned: list[tuple[Path, dict[str, object]]] = []
    skipped_existing = 0
    skipped_absent = 0
    for source in sorted(args.legacy_dir.glob("*.json")):
        paper_id = source.stem
        matches = by_arxiv.get(paper_id, [])
        if not matches:
            skipped_absent += 1
            continue
        destination = args.output_dir / source.name
        if destination.exists():
            skipped_existing += 1
            continue
        source_card = load_json(source)
        if not isinstance(source_card, dict):
            raise SystemExit(f"{source}: card must be a JSON object")
        primary = matches[0]
        card = display_math_v23(source_card)
        assert isinstance(card, dict)
        card.pop("selection_record", None)
        card.pop("import_provenance", None)
        card["card_standard_version"] = "2.3"
        card["paper_profile"] = paper_profile(primary, card)
        card["style_reference"] = "physicist_daily_arxiv"
        card["provenance"] = {
            "program": "Collection",
            "catalog": "Paper Collection",
            "catalog_record_id": str(primary["id"]),
            "catalog_record_ids": [str(record["id"]) for record in matches],
            "catalog_topic": str(primary.get("tags", ["", "Other"])[-1]),
            "collection_date": str(primary.get("date", args.migration_date)),
            "sampled_at": args.migration_date,
            "selected_by": "full_collection_backfill",
            "sampling_seed": "not_applicable_full_collection",
            "candidate_count": len(records),
            "legacy_full_text_card": source.name,
        }
        card["equation_refs"] = card.get("equation_refs", [])
        card["figure_refs"] = card.get("figure_refs", [])
        card["cover"] = {
            "mode": "title_abstract",
            "abstract_text": cover_abstract(card),
            "selection_rationale": (
                "该旧版全文证据包没有经过 v2.3 的逐图导出与图号核验；为避免错配图片，"
                "封面使用论文题目和经全文核对的摘要，关键论证保留在卡片正文中。"
            ),
        }
        planned.append((destination, card))

    if not args.check:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for destination, card in planned:
            destination.write_text(
                json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
    print(
        json.dumps(
            {
                "ready_to_migrate": len(planned),
                "skipped_existing": skipped_existing,
                "skipped_absent_from_catalog": skipped_absent,
                "mode": "check" if args.check else "write",
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
