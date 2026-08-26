#!/usr/bin/env python3
"""Synchronize the 450-work Collection backfill campaign with card files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", type=Path, required=True)
    args = parser.parse_args()

    campaign = json.loads(args.campaign.read_text(encoding="utf-8"))
    selection = campaign.get("selection")
    if not isinstance(selection, list):
        raise SystemExit("campaign selection must be a list")

    completed = 0
    seen_card_ids: set[str] = set()
    seen_catalog_ids: set[str] = set()
    for item in selection:
        card_id = str(item["card_id"])
        record_ids = [str(value) for value in item.get("catalog_record_ids", [])]
        if card_id in seen_card_ids:
            raise SystemExit(f"duplicate campaign card id: {card_id}")
        overlap = seen_catalog_ids.intersection(record_ids)
        if overlap:
            raise SystemExit(f"duplicate catalog record ids: {sorted(overlap)}")
        seen_card_ids.add(card_id)
        seen_catalog_ids.update(record_ids)
        card_path = ROOT / str(item["card_path"])
        if card_path.is_file():
            item["status"] = "card_existing"
            completed += 1
        else:
            item["status"] = "pending"

    target = int(campaign["unique_works"])
    if len(selection) != target or len(seen_card_ids) != target:
        raise SystemExit("campaign is not duplicate-free at the unique-work boundary")
    if len(seen_catalog_ids) != int(campaign["catalog_records"]):
        raise SystemExit("campaign does not cover every catalog record exactly once")

    campaign["existing_cards"] = completed
    campaign["pending_cards"] = target - completed
    args.campaign.write_text(
        json.dumps(campaign, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Full Collection campaign: {completed}/{target} cards, {target - completed} pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
