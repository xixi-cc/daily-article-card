#!/usr/bin/env python3
"""Merge evidence-backed catalog aliases into canonical Collection works."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


ALIASES = [
    {
        "alias_card_id": "record-56bc183d58cbbde2",
        "canonical_card_id": "doi-10.1140-epje-s10189-023-00364-w",
        "catalog_record_id": "56bc183d58cbbde2",
        "basis": (
            "PMC10603022 identifies DOI 10.1140/epje/s10189-023-00364-w; "
            "the title and authors match the canonical DOI record."
        ),
    }
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", type=Path, required=True)
    args = parser.parse_args()

    campaign = json.loads(args.campaign.read_text(encoding="utf-8"))
    selection = campaign.get("selection")
    if not isinstance(selection, list):
        raise SystemExit("campaign selection must be a list")

    for alias in ALIASES:
        by_card_id = {str(item["card_id"]): item for item in selection}
        canonical = by_card_id.get(str(alias["canonical_card_id"]))
        if canonical is None:
            raise SystemExit(f"missing canonical campaign work: {alias['canonical_card_id']}")
        duplicate = by_card_id.get(str(alias["alias_card_id"]))
        if duplicate is not None:
            for field in ("catalog_record_ids", "titles", "topics"):
                target_values = canonical.setdefault(field, [])
                source_values = duplicate.get(field, [])
                if not isinstance(target_values, list) or not isinstance(source_values, list):
                    raise SystemExit(f"campaign field {field} must be a list")
                target_values.extend(value for value in source_values if value not in target_values)
            selection.remove(duplicate)
        elif str(alias["catalog_record_id"]) not in canonical.get("catalog_record_ids", []):
            raise SystemExit(f"alias disappeared without canonical coverage: {alias['catalog_record_id']}")

    for sequence, item in enumerate(selection, start=1):
        item["sequence"] = sequence
    campaign["unique_works"] = len(selection)
    campaign["source_kind_counts"] = {
        kind: sum(str(item.get("source_kind")) == kind for item in selection)
        for kind in ("arxiv", "doi", "url")
    }
    campaign["resolved_identity_aliases"] = ALIASES
    args.campaign.write_text(
        json.dumps(campaign, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "catalog_records": campaign["catalog_records"],
                "unique_works": campaign["unique_works"],
                "resolved_aliases": len(ALIASES),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
