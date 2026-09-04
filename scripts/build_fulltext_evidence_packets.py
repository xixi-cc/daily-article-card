#!/usr/bin/env python3
"""Build page-addressable evidence packets for long-form paper-card curation."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CARDS_DIR = ROOT / "data" / "curated_cards"
PDF_DIR = ROOT / "tmp" / "pdfs"
OUTPUT_DIR = ROOT / "tmp" / "card-evidence-audit" / "packets"


def compact(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def pdf_pages(path: Path) -> list[str]:
    result = subprocess.run(
        ["pdftotext", "-layout", str(path), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.split("\f")


def page_excerpt(page: str, match: re.Match[str], limit: int = 3000) -> str:
    start = max(0, match.start() - 200)
    return compact(page[start : match.start() + limit])


def first_matching_excerpt(
    pages: list[str], patterns: tuple[str, ...], limit: int = 3000
) -> dict[str, object] | None:
    # These patterns describe section-heading lines. Searching them against an
    # entire PDF page can trigger catastrophic backtracking when the PDF text
    # layer contains a multi-megabyte line (typically an embedded vector
    # figure). Scan bounded individual lines instead, while retaining the
    # original page offset used for the returned excerpt.
    compiled = tuple(re.compile(pattern, re.I) for pattern in patterns)
    for page_number, page in enumerate(pages, start=1):
        offset = 0
        for raw_line in page.splitlines(keepends=True):
            line = raw_line.rstrip("\r\n")
            if len(line) <= 500:
                for pattern in compiled:
                    match = pattern.search(line)
                    if match:
                        absolute_start = offset + match.start()
                        excerpt_start = max(0, absolute_start - 200)
                        return {
                            "page": page_number,
                            "matched": compact(match.group(0)),
                            "text": compact(
                                page[excerpt_start : absolute_start + limit]
                            ),
                        }
            offset += len(raw_line)
    return None


def headings(pages: list[str]) -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    pattern = re.compile(
        r"(?m)^\s*(?:(?:[IVXLC]+|\d+(?:\.\d+)*)[.)]?\s+)([A-Z][^\n]{2,100})$"
    )
    for page_number, page in enumerate(pages, start=1):
        for match in pattern.finditer(page):
            title = compact(match.group(1)).strip(" .")
            if len(title) > 100 or any(item["title"] == title for item in found):
                continue
            found.append({"page": page_number, "title": title})
            if len(found) >= 24:
                return found
    return found


def captions(pages: list[str]) -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    pattern = re.compile(r"(?im)^\s*((?:fig(?:ure)?|table)\s*[A-Z]?\d+[^\n]*(?:\n(?!\s*\n)[^\n]*){0,3})")
    for page_number, page in enumerate(pages, start=1):
        for match in pattern.finditer(page):
            text = compact(match.group(1))[:1400]
            if text and not any(item["text"] == text for item in found):
                found.append({"page": page_number, "text": text})
            if len(found) >= 12:
                return found
    return found


def quantitative_lines(pages: list[str]) -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    signal = re.compile(
        r"(?i)(?:\d+(?:\.\d+)?\s*%|±|\\pm|state[- ]of[- ]the[- ]art|outperform|sample|epoch|iteration|convergen|error|accuracy|success rate)"
    )
    for page_number, page in enumerate(pages, start=1):
        for raw in page.splitlines():
            line = compact(raw)
            if 40 <= len(line) <= 500 and signal.search(line):
                found.append({"page": page_number, "text": line})
            if len(found) >= 20:
                return found
    return found


def urls(pages: list[str]) -> list[str]:
    values: list[str] = []
    for page in pages:
        for value in re.findall(r"https?://[^\s)>}\]]+", page):
            value = value.rstrip(".,;")
            if value not in values and "arxiv.org" not in value:
                values.append(value)
    return values[:12]


def build_packet(card_path: Path) -> dict[str, object]:
    card = json.loads(card_path.read_text(encoding="utf-8"))
    arxiv_id = str(card["arxiv_id"])
    paper = PDF_DIR / arxiv_id / "paper.pdf"
    if not paper.exists():
        raise FileNotFoundError(paper)
    pages = pdf_pages(paper)
    first_page = compact(pages[0])[:5000]
    return {
        "arxiv_id": arxiv_id,
        "title_en": card["title_en"],
        "title_zh": card["title_zh"],
        "source_version": card.get("source_version"),
        "page_count": len(pages),
        "first_page": first_page,
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", action="append", dest="ids")
    args = parser.parse_args()
    selected = set(args.ids or [])
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    for card_path in sorted(CARDS_DIR.glob("*.json")):
        if selected and card_path.stem not in selected:
            continue
        packet = build_packet(card_path)
        destination = OUTPUT_DIR / card_path.name
        destination.write_text(
            json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        count += 1
        print(f"packet {packet['arxiv_id']}: {packet['page_count']} pages")
    print(f"Built {count} evidence packets in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
