#!/usr/bin/env python3
"""Expand compact arXiv Daily cards with authoritative arXiv metadata."""

from __future__ import annotations

import argparse
import html
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS_MD = ROOT / "papers.md"
TRANSLATIONS_ZH = ROOT / "data" / "arxiv_zh.json"
ATOM = {"a": "http://www.w3.org/2005/Atom"}

PROPER_NOUN_GLOSSARY = {
    "人工智能": "AI",
    "变形金刚": "Transformer",
    "威尔逊-费希尔": "Wilson–Fisher",
    "别列津斯基-科斯特利茨-托利斯": "Berezinskii–Kosterlitz–Thouless",
    "爱德华兹-威尔金森": "Edwards–Wilkinson",
    "卡达尔-帕里西-张": "Kardar–Parisi–Zhang",
    "哈密顿-雅可比-贝尔曼": "Hamilton–Jacobi–Bellman",
    "朗之万": "Langevin",
    "李-杨": "Lee–Yang",
    "库拉莫托": "Kuramoto",
    "布朗粒子": "Brownian 粒子",
    "沃瑟斯坦": "Wasserstein",
    "瓦瑟斯坦": "Wasserstein",
    "利普希茨": "Lipschitz",
    "希尔伯特-施密特": "Hilbert–Schmidt",
    "艾伦-卡恩": "Allen–Cahn",
    "莱维": "Lévy",
    "狄利克雷": "Dirichlet",
    "柯普曼": "Koopman",
    "海森": "Hessian",
    "马尔可夫": "Markov",
    "奥恩斯坦-乌伦贝克": "Ornstein–Uhlenbeck",
}


def compact(value: str) -> str:
    return " ".join(html.unescape(value).split())


def preserve_proper_nouns(value: str) -> str:
    for translated, original in PROPER_NOUN_GLOSSARY.items():
        value = value.replace(translated, original)
    return value


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
    sentences = re.split(r"(?<=[。！？])|(?<=[.!?])\s+(?=[A-Z0-9])", abstract)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def extract_section(details: str, title: str) -> str:
    match = re.search(rf"## {re.escape(title)}<br>(.*?)(?=<br><br>## |</details>)", details)
    if not match:
        return ""
    value = compact(match.group(1).replace("<br>", " "))
    return re.sub(r"^(?:-\s+)+", "", value)


def bullets(items: list[str]) -> str:
    return "<br>".join(f"- {item}" for item in items if item)


def enrich_row(
    line: str,
    metadata: dict[str, dict[str, object]],
    translations: dict[str, dict[str, str]],
) -> str:
    match = re.match(r"^\|\s*([^|]+)\|\s*([^|]+)\|\s*(https?://[^|]+)\|\s*(.*?)\s*\|$", line)
    if not match:
        return line
    date, title, link, details = (part.strip() for part in match.groups())
    id_match = re.search(r"(\d{4}\.\d{4,5})", link)
    if not id_match or id_match.group(1) not in metadata:
        return line

    arxiv_id = id_match.group(1)
    meta = metadata[arxiv_id]
    translation = translations.get(arxiv_id, {})
    title_en = re.split(r"\s*<br\s*/?>\s*", title, flags=re.IGNORECASE)[-1].strip()
    title_zh = preserve_proper_nouns(translation.get("title_zh", "").strip()) or title_en
    abstract = preserve_proper_nouns(translation.get("abstract_zh", "").strip())
    if not abstract:
        abstract = extract_section(details, "核心贡献") or extract_section(details, "论文概述")
    sentences = split_sentences(abstract)
    contribution = extract_section(details, "核心贡献") or extract_section(details, "论文概述")
    limitation = extract_section(details, "主要限制") or "请结合论文正文判断方法适用范围。"
    authors = [str(author) for author in meta["authors"]]
    categories = [str(category) for category in meta["categories"]]

    overview = sentences[:3] or [abstract]
    method = sentences[3:6] or sentences[1:3] or ["方法细节请参阅论文正文。"]
    results = sentences[6:] or sentences[-2:] or ["实验与理论结果请参阅论文正文。"]
    resources = [f"arXiv 分类：{', '.join(categories)}"]
    resources.append("计算资源、数据集和实现细节以论文正文及补充材料为准。")

    expanded = (
        "<details><summary>展开</summary>"
        f"## 作者信息<br>- 作者：{'、'.join(authors)}<br>- 研究机构：当前元数据未提供可核验的机构信息，暂不推测；需以论文首页为准。<br><br>"
        f"## 论文概述<br>{bullets(overview)}<br><br>"
        f"## 核心贡献<br>- {contribution}<br><br>"
        f"## 方法描述<br>{bullets(method)}<br><br>"
        f"## 数据集与资源<br>{bullets(resources)}<br><br>"
        f"## 评估与结果<br>{bullets(results)}<br><br>"
        f"## 主要限制<br>- {limitation}</details>"
    )
    return f"| {date} | {title_zh}<br>{title_en} | {link} | {expanded} |"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=PAPERS_MD)
    args = parser.parse_args()
    text = args.input.read_text(encoding="utf-8")
    translations = json.loads(TRANSLATIONS_ZH.read_text(encoding="utf-8"))
    ids = list(dict.fromkeys(re.findall(r"arxiv.org/abs/(\d{4}\.\d{4,5})", text)))
    metadata = fetch_metadata(ids)
    missing = sorted(set(ids) - set(metadata))
    if missing:
        raise SystemExit(f"arXiv metadata missing for: {', '.join(missing)}")
    output = "\n".join(enrich_row(line, metadata, translations) for line in text.splitlines()) + "\n"
    args.input.write_text(output, encoding="utf-8")
    print(f"Expanded {len(ids)} paper cards with arXiv metadata")


if __name__ == "__main__":
    main()
