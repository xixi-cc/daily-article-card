#!/usr/bin/env python3
"""Build a compact, page-addressable Paper Card packet from MinerU output."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

try:
    from build_fulltext_evidence_packets import (
        captions,
        first_matching_excerpt,
        headings,
        pdf_pages,
        quantitative_lines,
        urls,
    )
except ModuleNotFoundError:  # Imported as scripts.build_mineru_evidence_packet.
    from scripts.build_fulltext_evidence_packets import (
        captions,
        first_matching_excerpt,
        headings,
        pdf_pages,
        quantitative_lines,
        urls,
    )


SECTION_LIMIT = 1_800
PACKET_TOKEN_TARGET = 8_000
PACKET_CHARACTER_TARGET = PACKET_TOKEN_TARGET * 4
SECTION_SIGNALS = (
    "abstract",
    "introduction",
    "background",
    "method",
    "model",
    "approach",
    "experiment",
    "evaluation",
    "result",
    "discussion",
    "limitation",
    "conclusion",
)


def compact(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def approximate_tokens(value: str) -> int:
    return (len(value) + 3) // 4


def markdown_sections(markdown: str) -> list[dict[str, str]]:
    matches = list(re.finditer(r"(?m)^(#{1,4})\s+(.+?)\s*$", markdown))
    sections: list[dict[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        body = markdown[start:end].strip()
        sections.append(
            {
                "level": str(len(match.group(1))),
                "title": compact(match.group(2)),
                "text": body[:SECTION_LIMIT],
            }
        )
    return sections


def selected_sections(markdown: str) -> list[dict[str, str]]:
    sections = markdown_sections(markdown)
    selected = [
        section
        for section in sections
        if any(signal in section["title"].casefold() for signal in SECTION_SIGNALS)
    ]
    if not selected:
        selected = sections[:8]
    return selected[:8]


def markdown_equations(markdown: str) -> list[str]:
    patterns = (
        r"\$\$(.+?)\$\$",
        r"\\\[(.+?)\\\]",
        r"\\begin\{(?:equation\*?|align\*?|gather\*?)\}(.+?)\\end\{(?:equation\*?|align\*?|gather\*?)\}",
    )
    found: list[str] = []
    for pattern in patterns:
        for match in re.finditer(pattern, markdown, re.S):
            equation = compact(match.group(1))[:1_200]
            if equation and equation not in found:
                found.append(equation)
            if len(found) >= 12:
                return found
    return found


def markdown_images(markdown: str) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    for match in pattern.finditer(markdown):
        item = {"alt": compact(match.group(1)), "path": match.group(2).strip()}
        if item not in found:
            found.append(item)
        if len(found) >= 16:
            break
    return found


def page_evidence(pages: list[str]) -> dict[str, object]:
    evidence = {
        "headings": headings(pages)[:20],
        "introduction": first_matching_excerpt(
            pages,
            (r"^\s*(?:I\.?|1\.?)?\s*INTRODUCTION\s*$", r"^\s*1\s+Introduction\s*$"),
            3_000,
        ),
        "method": first_matching_excerpt(
            pages,
            (
                r"^\s*(?:\d+(?:\.\d+)*|[IVXLC]+)\.?\s+(?:MODEL|METHODS?|METHODOLOGY|THEORETICAL FRAMEWORK|APPROACH)\b[^\n]*$",
                r"^\s*(?:MODEL|METHODS?|METHODOLOGY|OUR APPROACH)\s*$",
            ),
            3_000,
        ),
        "results": first_matching_excerpt(
            pages,
            (
                r"^\s*(?:\d+(?:\.\d+)*|[IVXLC]+)\.?\s+(?:RESULTS?|EXPERIMENTS?|EVALUATION)\b[^\n]*$",
                r"^\s*(?:RESULTS?|EXPERIMENTS?|EVALUATION)\s*$",
            ),
            3_000,
        ),
        "conclusion_or_limitations": first_matching_excerpt(
            pages,
            (
                r"^\s*(?:\d+(?:\.\d+)*|[IVXLC]+)\.?\s+(?:CONCLUSION(?:S)?|DISCUSSION|SUMMARY(?: AND OUTLOOK)?|LIMITATIONS?)\b[^\n]*$",
                r"^\s*(?:CONCLUSION(?:S)?|DISCUSSION|SUMMARY AND OUTLOOK|LIMITATIONS?)\s*$",
            ),
            3_000,
        ),
        "captions": captions(pages)[:8],
        "quantitative_lines": quantitative_lines(pages)[:12],
        "urls": urls(pages),
    }
    for item in evidence["captions"]:
        item["text"] = str(item["text"])[:800]
    for item in evidence["quantitative_lines"]:
        item["text"] = str(item["text"])[:350]
    return evidence


def campaign_item(campaign: dict[str, object], card_id: str) -> dict[str, object]:
    selection = campaign.get("selection")
    if not isinstance(selection, list):
        raise ValueError("campaign selection is missing")
    matches = [item for item in selection if item.get("card_id") == card_id]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one campaign item for {card_id}, found {len(matches)}")
    return matches[0]


def build_packet(
    item: dict[str, object], pdf: Path, markdown_path: Path
) -> dict[str, object]:
    markdown = markdown_path.read_text(encoding="utf-8")
    pages = pdf_pages(pdf)
    packet: dict[str, object] = {
        "schema": "mineru-paper-card-evidence-v1",
        "campaign_item": item,
        "source": {
            "pdf_path": str(pdf),
            "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
            "pdf_bytes": pdf.stat().st_size,
            "pdf_page_count": len([page for page in pages if page.strip()]),
            "mineru_markdown_path": str(markdown_path),
            "mineru_markdown_characters": len(markdown),
            "mineru_engine": "open-api",
            "mineru_api_model": "auto",
        },
        "first_page": compact(pages[0])[:4_000] if pages else "",
        "page_evidence": page_evidence(pages),
        "mineru_sections": selected_sections(markdown),
        "mineru_equation_candidates": markdown_equations(markdown),
        "mineru_images": markdown_images(markdown),
        "quality_boundary": {
            "mineru_role": "structured reading aid",
            "equation_authority": "matching arXiv TeX, otherwise the rendered source PDF",
            "page_authority": "page-delimited source PDF text plus rendered source PDF",
            "required_boundary": "full-text verified; no independent reproduction performed",
        },
    }
    serialized = json.dumps(packet, ensure_ascii=False)
    packet["size"] = {
        "characters": len(serialized),
        "approximate_tokens": approximate_tokens(serialized),
        "target_tokens": PACKET_TOKEN_TARGET,
        "within_target": approximate_tokens(serialized) <= PACKET_TOKEN_TARGET,
    }
    return packet


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--card-id", required=True)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    campaign = json.loads(args.campaign.read_text(encoding="utf-8"))
    item = campaign_item(campaign, args.card_id)
    packet = build_packet(item, args.pdf, args.markdown)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "card_id": args.card_id,
                "page_count": packet["source"]["pdf_page_count"],
                **packet["size"],
                "output": str(args.output),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
