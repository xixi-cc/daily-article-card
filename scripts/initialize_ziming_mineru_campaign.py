#!/usr/bin/env python3
"""Build an incremental MinerU campaign for one Paper Collection source."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from initialize_full_collection_campaign import source_identity
except ModuleNotFoundError:  # Imported as scripts.initialize_ziming_mineru_campaign.
    from scripts.initialize_full_collection_campaign import source_identity


DEFAULT_SOURCE_NAME = "Ziming Liu Paper Collection"
DEFAULT_SOURCE_URL_FRAGMENT = "ziming-paper-collection"


def has_source(
    record: dict[str, object], source_name: str, source_url_fragment: str
) -> bool:
    sources = record.get("curation_sources")
    if not isinstance(sources, list):
        return False
    for source in sources:
        if not isinstance(source, dict):
            continue
        if source.get("name") == source_name:
            return True
        if source_url_fragment in str(source.get("url", "")):
            return True
    return False


def build_campaign(
    catalog_path: Path,
    cards_dir: Path,
    source_name: str = DEFAULT_SOURCE_NAME,
    source_url_fragment: str = DEFAULT_SOURCE_URL_FRAGMENT,
) -> dict[str, object]:
    payload = catalog_path.read_bytes()
    records = json.loads(payload)
    if not isinstance(records, list):
        raise ValueError("catalog must be a JSON list")

    selected_records = [
        record
        for record in records
        if has_source(record, source_name, source_url_fragment)
    ]
    existing = {path.stem for path in cards_dir.glob("*.json")}
    works: dict[tuple[str, str], dict[str, object]] = {}
    for record in selected_records:
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
        tags = record.get("tags")
        topic = tags[-1] if isinstance(tags, list) and tags else "Other"
        item["topics"].append(str(topic))

    selection = sorted(
        works.values(), key=lambda item: (str(item["source_kind"]), str(item["source_id"]))
    )
    for sequence, item in enumerate(selection, start=1):
        item["sequence"] = sequence

    pending = [item for item in selection if item["status"] == "pending"]
    return {
        "campaign": "ziming-mineru-paper-cards",
        "source_name": source_name,
        "source_url_fragment": source_url_fragment,
        "source_catalog_sha256": hashlib.sha256(payload).hexdigest(),
        "source_catalog_records": len(records),
        "source_records": len(selected_records),
        "unique_works": len(selection),
        "existing_cards": len(selection) - len(pending),
        "pending_cards": len(pending),
        "pending_source_kind_counts": {
            kind: sum(item["source_kind"] == kind for item in pending)
            for kind in ("arxiv", "doi", "url")
        },
        "selection": selection,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--cards-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-name", default=DEFAULT_SOURCE_NAME)
    parser.add_argument("--source-url-fragment", default=DEFAULT_SOURCE_URL_FRAGMENT)
    args = parser.parse_args()

    campaign = build_campaign(
        args.catalog,
        args.cards_dir,
        args.source_name,
        args.source_url_fragment,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(campaign, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    summary = {key: value for key, value in campaign.items() if key != "selection"}
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
