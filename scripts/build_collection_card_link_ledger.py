#!/usr/bin/env python3
"""Build a catalog-record link ledger from every verified Collection card."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from urllib.parse import unquote, urlsplit
from pathlib import Path


ARXIV_PATTERN = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})")


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


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


def work_keys(record: dict[str, object]) -> set[str]:
    """Use public work identities and exact normalized titles, never fuzzy matching."""
    keys: set[str] = set()
    metadata = record.get("verified_metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}
    values = [record.get("url", ""), record.get("source_pdf", ""),
              record.get("arxiv_id", ""), metadata.get("arxiv_id", "")]
    links = record.get("links", {})
    if isinstance(links, dict):
        values.extend(value for key, value in links.items() if key != "card")
    for value in values:
        value = str(value)
        match = re.search(r"(?:arxiv\.org/(?:abs|pdf)/)?(\d{4}\.\d{4,5})(?:v\d+)?(?:\.pdf)?$", value.split("?")[0])
        if match:
            keys.add("arxiv:" + match.group(1))
        doi = re.search(r"(?:doi\.org/|/abstract/|/articles/)(10\.\d{4,9}/[^?#]+)", unquote(value), re.I)
        if doi:
            keys.add("doi:" + doi.group(1).rstrip("/").lower())
        if value.startswith("https://") or value.startswith("http://"):
            parts = urlsplit(value)
            keys.add("url:" + parts.netloc.lower().removeprefix("www.") + unquote(parts.path).rstrip("/"))
    for doi in [record.get("doi", ""), metadata.get("doi", "")]:
        if doi:
            keys.add("doi:" + str(doi).lower().removeprefix("https://doi.org/").rstrip("/"))
    for title in [record.get("title", ""), record.get("title_en", ""), metadata.get("title", "")]:
        if title:
            text = unicodedata.normalize("NFKC", str(title)).casefold()
            text = re.sub(r"\s+-\s+(?:PMC|ScienceDirect)$", "", text, flags=re.I)
            keys.add("title:" + re.sub(r"[^\w]", "", text))
    return keys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--cards-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--site-base", default="https://physics-ai-daily.lezontbukercfdvs4.chatgpt.site"
    )
    args = parser.parse_args()

    records = load_json(args.catalog)
    if not isinstance(records, list):
        raise SystemExit("catalog must be a JSON list")
    by_arxiv: dict[str, list[dict[str, object]]] = {}
    by_record_id = {str(record["id"]): record for record in records}
    by_work_key: dict[str, list[dict[str, object]]] = {}
    for record in records:
        paper_id = arxiv_id(record)
        if paper_id:
            by_arxiv.setdefault(paper_id, []).append(record)
        for key in work_keys(record):
            by_work_key.setdefault(key, []).append(record)

    ledger: list[dict[str, str]] = []
    seen_record_ids: set[str] = set()
    cards_without_catalog_records: list[str] = []
    for path in sorted(args.cards_dir.glob("*.json")):
        card = load_json(path)
        if not isinstance(card, dict):
            raise SystemExit(f"{path}: card must be a JSON object")
        provenance = card.get("provenance")
        explicit_ids: list[str] = []
        if isinstance(provenance, dict):
            values = provenance.get("catalog_record_ids")
            if isinstance(values, list):
                explicit_ids.extend(str(value) for value in values)
            if provenance.get("catalog_record_id"):
                explicit_ids.append(str(provenance["catalog_record_id"]))
        paper_id = str(card.get("arxiv_id", ""))
        matches = list(by_arxiv.get(paper_id, []))
        for key in work_keys(card):
            for record in by_work_key.get(key, []):
                if record not in matches:
                    matches.append(record)
        for record_id in explicit_ids:
            record = by_record_id.get(record_id)
            if record is not None and record not in matches:
                matches.append(record)
        if not matches:
            cards_without_catalog_records.append(path.stem)
            continue
        for record in matches:
            record_id = str(record["id"])
            if record_id in seen_record_ids:
                continue
            seen_record_ids.add(record_id)
            ledger.append(
                {
                    "card_id": path.stem,
                    "arxiv_id": paper_id,
                    "catalog_record_id": record_id,
                    "title": str(record.get("title", card.get("title_en", ""))),
                    "card_url": (
                        f"{args.site_base.rstrip('/')}/collection-papers/{path.stem}/"
                    ),
                }
            )

    if cards_without_catalog_records:
        raise SystemExit(
            f"Collection cards absent from catalog: {cards_without_catalog_records}"
        )
    ledger.sort(key=lambda item: (item["catalog_record_id"], item["card_id"]))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"Collection link ledger: {len(ledger)} catalog records from "
        f"{len(list(args.cards_dir.glob('*.json')))} cards"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
