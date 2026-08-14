#!/usr/bin/env python3
"""Expand compact arXiv Daily cards with authoritative arXiv metadata."""

from __future__ import annotations

import argparse
import html
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS_MD = ROOT / "papers.md"
ATOM = {"a": "http://www.w3.org/2005/Atom"}


def compact(value: str) -> str:
    return " ".join(html.unescape(value).split())


def fetch_metadata(ids: list[str]) -> dict[str, dict[str, object]]:
    records: dict[str, dict[str, object]] = {}
    for offset in range(0, len(ids), 20):
        batch = ids[offset : offset + 20]
        query = urllib.parse.urlencode({"id_list": ",".join(batch), "max_results": len(batch)})
        request = urllib.request.Request(
            "https://export.arxiv.org/api/query?" + query,
            headers={"User-Agent": "physics-AI-daily-cards/1.0"},
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            root = ET.fromstring(response.read())
        for entry in root.findall("a:entry", ATOM):
            arxiv_id = entry.findtext("a:id", default="", namespaces=ATOM).rsplit("/", 1)[-1].split("v")[0]
            records[arxiv_id] = {
                "abstract": compact(entry.findtext("a:summary", default="", namespaces=ATOM)),
                "authors": [compact(author.findtext("a:name", default="", namespaces=ATOM)) for author in entry.findall("a:author", ATOM)],
                "categories": [category.attrib.get("term", "") for category in entry.findall("a:category", ATOM)],
                "comment": compact(entry.findtext("a:comment", default="", namespaces=ATOM)),
            }
        if offset + 20 < len(ids):
            time.sleep(2)
    return records


def split_sentences(abstract: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", abstract)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def extract_section(details: str, title: str) -> str:
    match = re.search(rf"## {re.escape(title)}<br>(.*?)(?=<br><br>## |</details>)", details)
    if not match:
        return ""
    value = compact(match.group(1).replace("<br>", " "))
    return re.sub(r"^(?:-\s+)+", "", value)


def bullets(items: list[str]) -> str:
    return "<br>".join(f"- {item}" for item in items if item)


def enrich_row(line: str, metadata: dict[str, dict[str, object]]) -> str:
    match = re.match(r"^\|\s*([^|]+)\|\s*([^|]+)\|\s*(https?://[^|]+)\|\s*(.*?)\s*\|$", line)
    if not match:
        return line
    date, title, link, details = (part.strip() for part in match.groups())
    id_match = re.search(r"(\d{4}\.\d{4,5})", link)
    if not id_match or id_match.group(1) not in metadata:
        return line

    arxiv_id = id_match.group(1)
    meta = metadata[arxiv_id]
    abstract = str(meta["abstract"])
    sentences = split_sentences(abstract)
    grade = extract_section(details, "评级") or "来自 arXiv Daily"
    contribution = extract_section(details, "核心贡献") or extract_section(details, "论文概述")
    limitation = extract_section(details, "主要限制") or "请结合论文正文判断方法适用范围。"
    authors = [str(author) for author in meta["authors"]]
    categories = [str(category) for category in meta["categories"]]
    comment = str(meta["comment"])

    overview = sentences[:3] or [abstract]
    method = sentences[3:6] or sentences[1:3] or ["方法细节请参阅论文正文。"]
    results = sentences[6:] or sentences[-2:] or ["实验与理论结果请参阅论文正文。"]
    resources = [f"arXiv 分类：{', '.join(categories)}"]
    if comment:
        resources.append(f"作者备注：{comment}")
    else:
        resources.append("计算资源、数据集和实现细节以论文正文及补充材料为准。")

    expanded = (
        "<details><summary>展开</summary>"
        f"## 评级<br>{grade}<br><br>"
        "## 研究单位<br>- arXiv 元数据未结构化提供作者单位，请以论文首页为准。<br><br>"
        f"## 论文概述<br>{bullets(overview)}<br><br>"
        f"## 核心贡献<br>- {contribution}<br><br>"
        f"## 方法描述<br>{bullets(method)}<br><br>"
        f"## 数据集与资源<br>{bullets(resources)}<br><br>"
        f"## 评估与结果<br>{bullets(results)}<br><br>"
        f"## 主要限制<br>- {limitation}<br><br>"
        f"## 作者<br>- {'、'.join(authors)}<br><br>"
        f"## arXiv<br>- {arxiv_id}</details>"
    )
    return f"| {date} | {title} | {link} | {expanded} |"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=PAPERS_MD)
    args = parser.parse_args()
    text = args.input.read_text(encoding="utf-8")
    ids = list(dict.fromkeys(re.findall(r"arxiv.org/abs/(\d{4}\.\d{4,5})", text)))
    metadata = fetch_metadata(ids)
    missing = sorted(set(ids) - set(metadata))
    if missing:
        raise SystemExit(f"arXiv metadata missing for: {', '.join(missing)}")
    output = "\n".join(enrich_row(line, metadata) for line in text.splitlines()) + "\n"
    args.input.write_text(output, encoding="utf-8")
    print(f"Expanded {len(ids)} paper cards with arXiv metadata")


if __name__ == "__main__":
    main()
