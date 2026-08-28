#!/usr/bin/env python3
"""Create a complete, deterministic campaign for every Paper Collection record."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlparse


ARXIV_PATTERN = re.compile(r"arxiv\.org/(?:abs|pdf)/([^?#]+)", re.IGNORECASE)
DOI_PATTERN = re.compile(r"10\.\d{4,9}/[^?#\s]+", re.IGNORECASE)

# Catalog URLs can hide a canonical DOI behind an aggregator page. Keep the
# evidence-backed exceptions explicit so reinitializing the campaign cannot
# manufacture a second "work" for the same paper.
CATALOG_SOURCE_ALIASES: dict[str, tuple[str, str, str, str]] = {
    "56bc183d58cbbde2": (
        "doi",
        "10.1140/epje/s10189-023-00364-w",
        "doi-10.1140-epje-s10189-023-00364-w",
        "https://doi.org/10.1140/epje/s10189-023-00364-w",
    ),
}


def arxiv_id(record: dict[str, object]) -> str | None:
    links = record.get("links")
    candidates = [record.get("url", "")]
    if isinstance(links, dict):
        candidates.insert(0, links.get("arxiv", ""))
    for candidate in candidates:
        match = ARXIV_PATTERN.search(str(candidate))
        if match:
            return re.sub(r"v\d+$", "", match.group(1).removesuffix(".pdf"), flags=re.I)
    return None


def doi(record: dict[str, object]) -> str | None:
    links = record.get("links")
    candidates = [record.get("url", "")]
    if isinstance(links, dict):
        candidates.insert(0, links.get("publication", ""))
    for candidate in candidates:
        match = DOI_PATTERN.search(unquote(str(candidate)))
        if match:
            return match.group(0).rstrip("./").lower()
    return None


def safe_id(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-.").lower()
    return value[:120]


def source_identity(record: dict[str, object]) -> tuple[str, str, str, str]:
    alias = CATALOG_SOURCE_ALIASES.get(str(record["id"]))
    if alias is not None:
        return alias
    paper_id = arxiv_id(record)
    if paper_id:
        return "arxiv", paper_id, safe_id(paper_id), f"https://arxiv.org/abs/{paper_id}"
    paper_doi = doi(record)
    if paper_doi:
        return "doi", paper_doi, f"doi-{safe_id(paper_doi)}", f"https://doi.org/{paper_doi}"
    record_id = str(record["id"])
    url = str((record.get("links") or {}).get("publication") or record.get("url", ""))
    return "url", record_id, f"record-{safe_id(record_id)}", url


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--cards-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    records = json.loads(args.catalog.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise SystemExit("catalog must be a JSON list")
    existing = {path.stem for path in args.cards_dir.glob("*.json")}
    works: dict[tuple[str, str], dict[str, object]] = {}
    for record in records:
        source_kind, source_id, card_id, source_url = source_identity(record)
        key = (source_kind, source_id.casefold())
        item = works.setdefault(
            key,
            {
                "sequence": 0,
                "status": "card_existing" if card_id in existing else "pending",
                "card_id": card_id,
                "source_kind": source_kind,
                "source_id": source_id,
                "source_url": source_url,
                "catalog_record_ids": [],
                "titles": [],
                "topics": [],
                "card_path": f"data/collection_cards/{card_id}.json",
                "card_url_path": f"collection-papers/{card_id}/",
            },
        )
        item["catalog_record_ids"].append(str(record["id"]))
        item["titles"].append(str(record.get("title", "")))
        item["topics"].append(str(record.get("tags", ["", "Other"])[-1]))

    selection = sorted(works.values(), key=lambda item: (str(item["source_kind"]), str(item["source_id"])))
    for index, item in enumerate(selection, start=1):
        item["sequence"] = index
    manifest = {
        "campaign": "paper-collection-full-backfill-2026-08-26",
        "card_standard_version": "2.3",
        "catalog_records": len(records),
        "unique_works": len(selection),
        "existing_cards": sum(item["status"] == "card_existing" for item in selection),
        "pending_cards": sum(item["status"] == "pending" for item in selection),
        "source_kind_counts": {
            kind: sum(item["source_kind"] == kind for item in selection)
            for kind in ("arxiv", "doi", "url")
        },
        "selection": selection,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: manifest[key] for key in ("catalog_records", "unique_works", "existing_cards", "pending_cards", "source_kind_counts")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
