#!/usr/bin/env python3
"""Synchronize campaign status with card files and emit a verified link ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--site-base", default="https://physics-ai-daily.lezontbukercfdvs4.chatgpt.site")
    args = parser.parse_args()

    campaign = json.loads(args.campaign.read_text(encoding="utf-8"))
    initial = int(campaign["existing_cards_at_start"])
    completed = 0
    seen_ids: set[str] = set()
    seen_catalog_ids: set[str] = set()
    links: list[dict[str, object]] = []
    for item in campaign["selection"]:
        paper_id = str(item["arxiv_id"])
        catalog_id = str(item["catalog_record_id"])
        if paper_id in seen_ids or catalog_id in seen_catalog_ids:
            raise SystemExit(f"duplicate campaign entry: {paper_id} / {catalog_id}")
        seen_ids.add(paper_id)
        seen_catalog_ids.add(catalog_id)
        card_path = ROOT / str(item["card_path"])
        if card_path.is_file():
            item["status"] = "card_existing" if int(item["sequence"]) <= initial else "card_created"
            completed += 1
            links.append({
                "sequence": item["sequence"],
                "arxiv_id": paper_id,
                "catalog_record_id": catalog_id,
                "title": item["title"],
                "card_url": f"{args.site_base.rstrip('/')}/{item['card_url_path']}",
            })
        else:
            item["status"] = "pending"

    campaign["completed_cards"] = completed
    campaign["pending_cards"] = int(campaign["target_unique_cards"]) - completed
    campaign["duplicate_check"] = {
        "unique_arxiv_ids": len(seen_ids),
        "unique_catalog_record_ids": len(seen_catalog_ids),
        "passed": len(seen_ids) == len(seen_catalog_ids) == int(campaign["target_unique_cards"]),
    }
    args.campaign.write_text(
        json.dumps(campaign, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    ledger = args.campaign.with_name("card-links.json")
    ledger.write_text(json.dumps(links, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Collection campaign: {completed}/50 cards, {campaign['pending_cards']} pending, duplicates=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
