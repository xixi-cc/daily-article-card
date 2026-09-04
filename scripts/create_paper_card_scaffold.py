#!/usr/bin/env python3
"""Create a deterministic, provenance-aware draft Paper Card JSON scaffold."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    from scripts.card_taxonomy import PROFILE_LABELS
except ModuleNotFoundError:  # Direct execution sets scripts/ as sys.path[0].
    from card_taxonomy import PROFILE_LABELS


ROOT = Path(__file__).resolve().parents[1]
STANDARD_PATH = ROOT / "docs" / "PAPER_CARD_STANDARD.md"
COLLECTION_FIELDS = (
    "catalog",
    "catalog_record_id",
    "catalog_topic",
    "collection_date",
    "sampled_at",
    "selected_by",
    "sampling_seed",
)
DAILY_FIELDS = (
    "selected_by",
    "report_date",
    "listing_date",
    "grade",
    "score",
    "rubric_version",
)
SECTION_TITLES = (
    "作者信息",
    "研究问题",
    "背景",
    "给物理学家的 AI 导读",
    "模型与方法",
    "核心结果与证据",
    "有效性与局限",
    "复现与资源",
    "阅读指南",
)


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def standard_version(path: Path = STANDARD_PATH) -> str:
    match = re.search(r"^Version:\s*([0-9]+(?:\.[0-9]+)+)\s*$", path.read_text(), re.M)
    if not match:
        raise ValueError(f"cannot resolve Paper Card Standard version from {path}")
    return match.group(1)


def require_fields(value: dict[str, Any], fields: tuple[str, ...], label: str) -> None:
    missing = [field for field in fields if not value.get(field)]
    if missing:
        raise ValueError(f"{label} missing required fields: {', '.join(missing)}")


def build_scaffold(
    metadata: dict[str, Any],
    program: str,
    paper_profile: str,
    title_zh: str,
    provenance: dict[str, Any] | None = None,
    selection_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if paper_profile not in PROFILE_LABELS:
        raise ValueError(f"invalid paper_profile: {paper_profile}")
    require_fields(
        metadata,
        ("arxiv_id", "version", "title", "authors", "categories", "primary_category", "published", "abstract"),
        "metadata",
    )
    arxiv_id = str(metadata["arxiv_id"])
    if not re.fullmatch(r"(?:\d{4}\.\d{4,5}|[a-z-]+/\d{7})", arxiv_id):
        raise ValueError(f"unsupported arXiv identifier: {arxiv_id}")
    if not title_zh.strip():
        raise ValueError("title_zh must not be empty")

    program_normalized = program.capitalize()
    if program_normalized == "Collection":
        if selection_record is not None:
            raise ValueError("Collection cards must not contain selection_record")
        provenance = dict(provenance or {})
        provenance["program"] = "Collection"
        require_fields(provenance, COLLECTION_FIELDS, "Collection provenance")
    elif program_normalized == "Daily":
        selection_record = dict(selection_record or {})
        require_fields(selection_record, DAILY_FIELDS, "Daily selection_record")
        if selection_record.get("selected_by") != "codex_direct_arxiv":
            raise ValueError("Daily selected_by must be codex_direct_arxiv")
        if selection_record.get("grade") != "S":
            raise ValueError("Daily cards require grade S")
        provenance = {
            "program": "Daily",
            "discovery_source": "official arXiv category listings",
            "listing_date": selection_record["listing_date"],
        }
    else:
        raise ValueError(f"unsupported program: {program}")

    return {
        "arxiv_id": arxiv_id,
        "source_version": str(metadata["version"]),
        "source_pdf": str(metadata.get("source_pdf") or f"https://arxiv.org/pdf/{arxiv_id}"),
        "title_en": str(metadata["title"]),
        "title_zh": title_zh.strip(),
        "curation_status": "draft",
        "card_standard_version": standard_version(),
        "audience_profile": "physics_ai_literate_physicist",
        "paper_profile": paper_profile,
        "style_reference": "physicist_daily_arxiv",
        **({"selection_record": selection_record} if selection_record is not None else {}),
        "provenance": provenance,
        "verified_metadata": metadata,
        "equation_refs": [],
        "figure_refs": [],
        "cover": {},
        "sections": [{"title": title, "paragraphs": []} for title in SECTION_TITLES],
        "evidence_refs": [],
        "draft_contract": {
            "install_only_after": "full-text review, source-page checks, figure review, and strict validation",
            "required_boundary": "Evidence status: full-text verified; no independent reproduction performed.",
            "reader_test": "An AI-literate non-specialist physicist can follow the input-to-observable chain without an external AI glossary.",
        },
    }


def write_scaffold(path: Path, scaffold: dict[str, Any], force: bool = False) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(scaffold, ensure_ascii=False, indent=2) + "\n"
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(payload, encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--program", choices=("Daily", "Collection"), required=True)
    parser.add_argument("--paper-profile", choices=tuple(PROFILE_LABELS), required=True)
    parser.add_argument("--title-zh", required=True)
    parser.add_argument("--provenance", type=Path)
    parser.add_argument("--selection-record", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    scaffold = build_scaffold(
        load_object(args.metadata),
        args.program,
        args.paper_profile,
        args.title_zh,
        load_object(args.provenance) if args.provenance else None,
        load_object(args.selection_record) if args.selection_record else None,
    )
    write_scaffold(args.output, scaffold, args.force)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
