#!/usr/bin/env python3
"""Insert missing Codex-direct Daily cards into the canonical Markdown table."""

from __future__ import annotations

import json
import re
from pathlib import Path

from enrich_daily_cards import canonical_curated_row


ROOT = Path(__file__).resolve().parents[1]
PAPERS_MD = ROOT / "papers.md"
CARDS_DIR = ROOT / "data" / "curated_cards"


def main() -> None:
    source = PAPERS_MD.read_text(encoding="utf-8")
    existing = set(re.findall(r"https://arxiv\.org/abs/([^\s|<]+)", source))
    rows: list[tuple[str, str]] = []
    for path in sorted(CARDS_DIR.glob("*.json")):
        card = json.loads(path.read_text(encoding="utf-8"))
        arxiv_id = str(card.get("arxiv_id", "")).strip()
        selection = card.get("selection_record")
        provenance = card.get("provenance")
        if (
            not arxiv_id
            or arxiv_id in existing
            or not isinstance(selection, dict)
            or selection.get("selected_by") != "codex_direct_arxiv"
            or selection.get("grade") != "S"
            or not isinstance(provenance, dict)
            or provenance.get("program") != "Daily"
        ):
            continue
        report_date = str(selection.get("report_date", "")).strip()
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", report_date):
            raise ValueError(f"{arxiv_id}: invalid report_date")
        row = canonical_curated_row(
            report_date,
            f"https://arxiv.org/abs/{arxiv_id}",
            card,
        )
        rows.append((f"{report_date}:{arxiv_id}", row))

    if not rows:
        print("No missing Codex-direct Daily rows.")
        return

    rows.sort(reverse=True)
    lines = source.splitlines()
    if len(lines) < 2 or not lines[1].startswith("| ---"):
        raise ValueError("papers.md does not start with the expected Markdown table")
    lines[2:2] = [row for _, row in rows]
    PAPERS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Inserted {len(rows)} Codex-direct Daily rows.")


if __name__ == "__main__":
    main()
