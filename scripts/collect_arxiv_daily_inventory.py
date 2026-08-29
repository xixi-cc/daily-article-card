#!/usr/bin/env python3
"""Collect one official arXiv listing day into a reproducible JSON inventory."""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timezone
from html import unescape
from pathlib import Path
from typing import Dict, Iterable, List


CORE_CATEGORIES = (
    "cs.LG", "cs.AI", "cs.CL", "cs.RO", "stat.ML", "math.PR", "math.AP",
    "cond-mat.stat-mech", "cond-mat.soft", "nlin",
)
SUPPLEMENTARY_CATEGORIES = (
    "cs.IT", "cs.CV", "cs.NE", "cs.SY", "physics.comp-ph", "cond-mat.dis-nn",
)
USER_AGENT = "daily-article-card/1.0 (research inventory; contact via github.com/xixi-cc)"
ATOM = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def fetch_text(url: str, retries: int = 3) -> str:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=45) as response:
                return response.read().decode("utf-8")
        except Exception as error:  # Network errors are retried conservatively.
            last_error = error
            if attempt + 1 < retries:
                time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"failed to fetch {url}: {last_error}")


def clean_html(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(value)).strip()


def parse_listing_day(html: str, listing_date: date, category: str) -> List[Dict[str, str]]:
    label = listing_date.strftime("%a, %d %b %Y")
    heading = re.search(rf"<h3>\s*{re.escape(label)}\b[^<]*</h3>", html, re.IGNORECASE)
    if not heading:
        raise ValueError(f"listing date {label} not present for {category}")
    next_heading = re.search(r"<h3>", html[heading.end():], re.IGNORECASE)
    end = heading.end() + next_heading.start() if next_heading else len(html)
    section = html[heading.end():end]
    entries: List[Dict[str, str]] = []
    for match in re.finditer(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", section, re.IGNORECASE | re.DOTALL):
        dt_html, dd_html = match.groups()
        id_match = re.search(r"href\s*=\s*[\"']/abs/([^\"']+)", dt_html, re.IGNORECASE)
        title_match = re.search(
            r"class=[\"']list-title mathjax[\"'][^>]*>(.*?)</div>", dd_html, re.IGNORECASE | re.DOTALL
        )
        primary_match = re.search(
            r"class=[\"']primary-subject[\"'][^>]*>.*?\(([^()]+)\)\s*</span>",
            dd_html,
            re.IGNORECASE | re.DOTALL,
        )
        if not id_match or not title_match or not primary_match:
            continue
        arxiv_id = re.sub(r"v\d+$", "", id_match.group(1).strip(), flags=re.IGNORECASE)
        title = clean_html(re.sub(r"<span[^>]*>\s*Title:\s*</span>", "", title_match.group(1), flags=re.IGNORECASE))
        entries.append(
            {
                "arxiv_id": arxiv_id,
                "title": title,
                "primary_category": primary_match.group(1).strip(),
                "listing_category": category,
            }
        )
    return entries


def chunks(values: List[str], size: int) -> Iterable[List[str]]:
    for index in range(0, len(values), size):
        yield values[index:index + size]


def fetch_metadata(arxiv_ids: List[str]) -> Dict[str, Dict[str, object]]:
    metadata: Dict[str, Dict[str, object]] = {}
    batches = list(chunks(arxiv_ids, 40))
    for index, batch in enumerate(batches):
        query = urllib.parse.urlencode({"id_list": ",".join(batch), "max_results": len(batch)})
        xml = fetch_text(f"https://export.arxiv.org/api/query?{query}")
        root = ET.fromstring(xml)
        for entry in root.findall("atom:entry", ATOM):
            full_id = (entry.findtext("atom:id", default="", namespaces=ATOM).rsplit("/", 1)[-1]).strip()
            version_match = re.search(r"v(\d+)$", full_id)
            version = f"v{version_match.group(1)}" if version_match else ""
            arxiv_id = re.sub(r"v\d+$", "", full_id)
            primary_node = entry.find("arxiv:primary_category", ATOM)
            metadata[arxiv_id] = {
                "arxiv_id": arxiv_id,
                "version": version,
                "title": re.sub(r"\s+", " ", entry.findtext("atom:title", default="", namespaces=ATOM)).strip(),
                "abstract": re.sub(r"\s+", " ", entry.findtext("atom:summary", default="", namespaces=ATOM)).strip(),
                "authors": [
                    node.findtext("atom:name", default="", namespaces=ATOM).strip()
                    for node in entry.findall("atom:author", ATOM)
                ],
                "categories": [node.attrib.get("term", "") for node in entry.findall("atom:category", ATOM)],
                "primary_category": primary_node.attrib.get("term", "") if primary_node is not None else "",
                "published": entry.findtext("atom:published", default="", namespaces=ATOM),
                "updated": entry.findtext("atom:updated", default="", namespaces=ATOM),
                "comment": entry.findtext("arxiv:comment", default="", namespaces=ATOM),
                "abs_url": f"https://arxiv.org/abs/{arxiv_id}",
                "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}",
            }
        if index + 1 < len(batches):
            time.sleep(3)
    missing = sorted(set(arxiv_ids) - set(metadata))
    if missing:
        raise RuntimeError(f"official metadata missing for {missing}")
    return metadata


def collect(listing_date: date) -> Dict[str, object]:
    source_counts: Dict[str, int] = {}
    records: Dict[str, Dict[str, object]] = {}
    all_categories = [*CORE_CATEGORIES, *SUPPLEMENTARY_CATEGORIES]
    for category in all_categories:
        url = f"https://arxiv.org/list/{category}/pastweek?show=2000"
        entries = parse_listing_day(fetch_text(url), listing_date, category)
        primary_entries = [entry for entry in entries if entry["primary_category"] == category]
        source_counts[category] = len(primary_entries)
        scope = "core" if category in CORE_CATEGORIES else "supplementary"
        for entry in primary_entries:
            records.setdefault(entry["arxiv_id"], {**entry, "scope": scope})

    ids = sorted(records)
    metadata = fetch_metadata(ids)
    final_records: List[Dict[str, object]] = []
    replacements_excluded: List[str] = []
    for arxiv_id in ids:
        item = {**records[arxiv_id], **metadata[arxiv_id]}
        if item.get("version") != "v1":
            replacements_excluded.append(arxiv_id)
            continue
        final_records.append(item)

    return {
        "schema_version": 1,
        "listing_date": listing_date.isoformat(),
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "source": "official arXiv category pastweek listings plus official export API metadata",
        "category_counts": source_counts,
        "core_new_v1": sum(1 for item in final_records if item["scope"] == "core"),
        "supplementary_new_v1": sum(1 for item in final_records if item["scope"] == "supplementary"),
        "official_new_v1": len(final_records),
        "replacements_excluded": replacements_excluded,
        "records": final_records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="Official listing date in YYYY-MM-DD format")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    listing_date = date.fromisoformat(args.date)
    inventory = collect(listing_date)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"{args.date}: {inventory['official_new_v1']} new v1 "
        f"({inventory['core_new_v1']} core, {inventory['supplementary_new_v1']} supplementary)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
