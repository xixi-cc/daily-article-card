#!/usr/bin/env python3
"""Create a deterministic, duplicate-free Paper Collection card campaign."""

from __future__ import annotations

import argparse
import json
import random
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARXIV_PATTERN = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})")


def normalized_title(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"[^a-z0-9]+", "", value)


def arxiv_id(record: dict[str, object]) -> str | None:
    links = record.get("links")
    candidates = [record.get("url", "")]
    if isinstance(links, dict):
        candidates.insert(0, links.get("arxiv", ""))
    for candidate in candidates:
        match = ARXIV_PATTERN.search(str(candidate))
        if match:
            return match.group(1)
    return None


def load_cards(directory: Path) -> dict[str, dict[str, object]]:
    cards: dict[str, dict[str, object]] = {}
    for path in sorted(directory.glob("*.json")):
        card = json.loads(path.read_text(encoding="utf-8"))
        cards[path.stem] = card
    return cards


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--target", type=int, default=50)
    parser.add_argument("--seed", default="paper-collection-random50-2026-08-26-v1")
    args = parser.parse_args()

    records = json.loads(args.catalog.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise SystemExit("catalog must be a JSON list")

    daily = load_cards(ROOT / "data" / "curated_cards")
    collection = load_cards(ROOT / "data" / "collection_cards")
    by_arxiv: dict[str, dict[str, object]] = {}
    seen_titles: dict[str, str] = {}
    duplicate_catalog_records: list[dict[str, str]] = []
    for record in sorted(records, key=lambda item: str(item.get("id", ""))):
        paper_id = arxiv_id(record)
        if not paper_id:
            continue
        title_key = normalized_title(str(record.get("title", "")))
        if paper_id in by_arxiv or (title_key and title_key in seen_titles):
            duplicate_catalog_records.append({
                "catalog_record_id": str(record.get("id", "")),
                "arxiv_id": paper_id,
                "title": str(record.get("title", "")),
            })
            continue
        by_arxiv[paper_id] = record
        if title_key:
            seen_titles[title_key] = paper_id

    missing_existing = sorted(set(collection) - set(by_arxiv))
    if missing_existing:
        raise SystemExit(f"existing Collection cards absent from catalog: {missing_existing}")

    selected: list[dict[str, object]] = []
    for paper_id in sorted(collection):
        record = by_arxiv[paper_id]
        selected.append({
            "sequence": len(selected) + 1,
            "status": "card_existing",
            "arxiv_id": paper_id,
            "catalog_record_id": str(record.get("id", "")),
            "title": str(record.get("title", "")),
            "topic": list(record.get("tags", ["", ""]))[-1],
            "source_url": str(record.get("links", {}).get("arxiv", record.get("url", ""))),
            "card_path": f"data/collection_cards/{paper_id}.json",
            "card_url_path": f"collection-papers/{paper_id}/",
        })

    eligible = [
        (paper_id, record)
        for paper_id, record in sorted(by_arxiv.items())
        if paper_id not in daily and paper_id not in collection
    ]
    needed = args.target - len(selected)
    if needed < 0 or len(eligible) < needed:
        raise SystemExit(f"cannot select {args.target} unique papers from {len(eligible)} eligible records")
    rng = random.Random(args.seed)
    for paper_id, record in rng.sample(eligible, needed):
        selected.append({
            "sequence": len(selected) + 1,
            "status": "pending",
            "arxiv_id": paper_id,
            "catalog_record_id": str(record.get("id", "")),
            "title": str(record.get("title", "")),
            "topic": list(record.get("tags", ["", ""]))[-1],
            "source_url": str(record.get("links", {}).get("arxiv", record.get("url", ""))),
            "card_path": f"data/collection_cards/{paper_id}.json",
            "card_url_path": f"collection-papers/{paper_id}/",
        })

    ids = [str(item["arxiv_id"]) for item in selected]
    titles = [normalized_title(str(item["title"])) for item in selected]
    if len(ids) != args.target or len(ids) != len(set(ids)) or len(titles) != len(set(titles)):
        raise SystemExit("campaign selection is not duplicate-free")

    manifest = {
        "campaign": "paper-collection-random50-2026-08-26",
        "card_standard_version": "2.3",
        "selection_seed": args.seed,
        "target_unique_cards": args.target,
        "existing_cards_at_start": len(collection),
        "new_cards_required": needed,
        "daily_ids_excluded": sorted(set(daily) & set(by_arxiv)),
        "duplicate_catalog_records_excluded": duplicate_catalog_records,
        "selection": selected,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Selected {len(selected)} unique papers: {len(collection)} existing, {needed} pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
