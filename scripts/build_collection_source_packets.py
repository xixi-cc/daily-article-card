#!/usr/bin/env python3
"""Download and index full-text sources for the Collection card campaign."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
import urllib.request
from pathlib import Path

from build_fulltext_evidence_packets import (
    captions,
    first_matching_excerpt,
    headings,
    pdf_pages,
    quantitative_lines,
    urls,
)
from enrich_daily_cards import fetch_metadata


ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "tmp" / "collection-card-campaign"
PDF_DIR = WORK_DIR / "pdfs"
PACKET_DIR = WORK_DIR / "packets"
USER_AGENT = "physics-AI-paper-cards/2.3 (local research workflow)"


def download_pdf(arxiv_id: str) -> Path:
    destination = PDF_DIR / f"{arxiv_id}.pdf"
    if destination.is_file() and destination.stat().st_size > 1_000:
        return destination
    request = urllib.request.Request(
        f"https://arxiv.org/pdf/{arxiv_id}", headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        payload = response.read()
    if not payload.startswith(b"%PDF"):
        raise ValueError(f"{arxiv_id}: official source did not return a PDF")
    destination.write_bytes(payload)
    return destination


def build_packet(item: dict[str, object], metadata: dict[str, object], pdf: Path) -> dict[str, object]:
    pages = pdf_pages(pdf)
    return {
        "arxiv_id": item["arxiv_id"],
        "catalog_record_id": item["catalog_record_id"],
        "catalog_title": item["title"],
        "catalog_topic": item["topic"],
        "metadata": metadata,
        "pdf": {
            "source_url": item["source_url"],
            "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
            "bytes": pdf.stat().st_size,
            "page_count": len(pages),
        },
        "first_page": " ".join(pages[0].split())[:5000],
        "headings": headings(pages),
        "introduction": first_matching_excerpt(
            pages, (r"^\s*(?:I\.?|1\.?)?\s*INTRODUCTION\s*$", r"^\s*1\s+Introduction\s*$")
        ),
        "method": first_matching_excerpt(
            pages,
            (
                r"^\s*(?:\d+(?:\.\d+)*|[IVXLC]+)\.?\s+(?:MODEL|METHODS?|METHODOLOGY|THEORETICAL FRAMEWORK|APPROACH)\b[^\n]*$",
                r"^\s*(?:MODEL|METHODS?|METHODOLOGY|OUR APPROACH)\s*$",
            ),
            5000,
        ),
        "results": first_matching_excerpt(
            pages,
            (
                r"^\s*(?:\d+(?:\.\d+)*|[IVXLC]+)\.?\s+(?:RESULTS?|EXPERIMENTS?|EVALUATION)\b[^\n]*$",
                r"^\s*(?:RESULTS?|EXPERIMENTS?|EVALUATION)\s*$",
            ),
            5000,
        ),
        "conclusion": first_matching_excerpt(
            pages,
            (
                r"^\s*(?:\d+(?:\.\d+)*|[IVXLC]+)\.?\s+(?:CONCLUSION(?:S)?|DISCUSSION|SUMMARY(?: AND OUTLOOK)?|LIMITATIONS?)\b[^\n]*$",
                r"^\s*(?:CONCLUSION(?:S)?|DISCUSSION|SUMMARY AND OUTLOOK|LIMITATIONS?)\s*$",
            ),
            5000,
        ),
        "captions": captions(pages),
        "quantitative_lines": quantitative_lines(pages),
        "urls": urls(pages),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--start", type=int, default=6)
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    campaign = json.loads(args.campaign.read_text(encoding="utf-8"))
    items = [
        item for item in campaign["selection"]
        if item["status"] == "pending" and int(item["sequence"]) >= args.start
    ][: args.limit]
    ids = [str(item["arxiv_id"]) for item in items]
    if not ids:
        print("No pending sources selected")
        return 0

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    metadata = fetch_metadata(ids)
    missing = sorted(set(ids) - set(metadata))
    if missing:
        raise SystemExit(f"official arXiv metadata missing: {missing}")

    for index, item in enumerate(items):
        paper_id = str(item["arxiv_id"])
        pdf = download_pdf(paper_id)
        packet = build_packet(item, metadata[paper_id], pdf)
        (PACKET_DIR / f"{paper_id}.json").write_text(
            json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(
            f"packet {paper_id}: {packet['pdf']['page_count']} pages, "
            f"sha256={packet['pdf']['sha256']}"
        )
        if index + 1 < len(items):
            time.sleep(3)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
