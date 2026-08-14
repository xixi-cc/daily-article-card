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
CURATED_CARDS_DIR = ROOT / "data" / "curated_cards"
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


def load_curated_cards() -> dict[str, dict[str, object]]:
    cards: dict[str, dict[str, object]] = {}
    if not CURATED_CARDS_DIR.exists():
        return cards
    for path in sorted(CURATED_CARDS_DIR.glob("*.json")):
        card = json.loads(path.read_text(encoding="utf-8"))
        arxiv_id = str(card.get("arxiv_id", "")).strip()
        if not arxiv_id:
            raise ValueError(f"Curated card has no arxiv_id: {path}")
        cards[arxiv_id] = card
    return cards


def render_curated_details(card: dict[str, object]) -> str:
    rendered: list[str] = ["<details><summary>展开</summary>"]
    sections = card.get("sections", [])
    if not isinstance(sections, list):
        raise ValueError(f"Invalid curated sections for {card.get('arxiv_id')}")
    for index, section in enumerate(sections):
        if not isinstance(section, dict) or not section.get("title"):
            raise ValueError(f"Invalid curated section for {card.get('arxiv_id')}")
        if index:
            rendered.append("<br><br>")
        rendered.append(f"## {section['title']}<br>")
        blocks: list[str] = []
        paragraphs = section.get("paragraphs", [])
        section_bullets = section.get("bullets", [])
        if isinstance(paragraphs, list):
            blocks.extend(str(value) for value in paragraphs if value)
        if isinstance(section_bullets, list):
            blocks.extend(f"- {value}" for value in section_bullets if value)
        rendered.append("<br>".join(blocks))
    rendered.append("</details>")
    return "".join(rendered)


def classify_paper(title: str, abstract: str, categories: list[str]) -> str:
    text = f"{title} {abstract}".lower()
    has_ai = any(category.startswith(("cs.", "stat.ML")) for category in categories)
    has_physics = any(
        category.startswith(("cond-mat", "physics", "hep-", "nucl-", "astro-ph", "quant-ph"))
        for category in categories
    )
    physics_of_ai_terms = (
        "phase transition", "criticality", "statistical mechanics", "attractor",
        "learning dynamics", "scaling law", "entropy production", "correlation flow",
    )
    ai_for_physics_terms = (
        "pde", "operator learning", "force field", "physical state", "simulation",
        "scientific machine learning", "phase diagram",
    )
    if has_ai and any(term in text for term in physics_of_ai_terms):
        return "physics of AI"
    if has_ai and (has_physics or any(term in text for term in ai_for_physics_terms)):
        return "AI for physics"
    if has_ai:
        return "pure AI"
    return "pure physics"


def enrich_row(
    line: str,
    metadata: dict[str, dict[str, object]],
    translations: dict[str, dict[str, str]],
    curated_cards: dict[str, dict[str, object]],
) -> str:
    match = re.match(r"^\|\s*([^|]+)\|\s*([^|]+)\|\s*(https?://[^|]+)\|\s*(.*?)\s*\|$", line)
    if not match:
        return line
    date, title, link, details = (part.strip() for part in match.groups())
    id_match = re.search(r"(\d{4}\.\d{4,5})", link)
    if not id_match or id_match.group(1) not in metadata:
        return line

    arxiv_id = id_match.group(1)
    curated = curated_cards.get(arxiv_id)
    if curated:
        title_en = str(curated.get("title_en", "")).strip() or re.split(
            r"\s*<br\s*/?>\s*", title, flags=re.IGNORECASE
        )[-1].strip()
        title_zh = str(curated.get("title_zh", "")).strip() or title_en
        return f"| {date} | {title_zh}<br>{title_en} | {link} | {render_curated_details(curated)} |"

    meta = metadata[arxiv_id]
    translation = translations.get(arxiv_id, {})
    title_en = re.split(r"\s*<br\s*/?>\s*", title, flags=re.IGNORECASE)[-1].strip()
    title_zh = preserve_proper_nouns(translation.get("title_zh", "").strip()) or title_en
    abstract = preserve_proper_nouns(translation.get("abstract_zh", "").strip())
    if not abstract:
        abstract = extract_section(details, "核心贡献") or extract_section(details, "论文概述")
    sentences = split_sentences(abstract)
    contribution = extract_section(details, "核心贡献") or extract_section(details, "论文概述")
    if not contribution:
        prior_results = extract_section(details, "核心结果与证据")
        match = re.search(r"摘要层面的核心陈述：(.+?)(?:\s+-\s+当前证据状态：|$)", prior_results)
        contribution = match.group(1).strip() if match else "核心结果需从全文核验。"
    limitation = extract_section(details, "主要限制")
    if not limitation:
        prior_limits = extract_section(details, "有效性与局限")
        match = re.search(r"已知局限：(.+?)(?:\s+-\s+有效性范围|$)", prior_limits)
        limitation = match.group(1).strip() if match else "请结合论文正文判断方法适用范围。"
    authors = [str(author) for author in meta["authors"]]
    categories = [str(category) for category in meta["categories"]]

    overview = sentences[:3] or [abstract]
    paper_class = classify_paper(title_en, str(meta["abstract"]), categories)

    expanded = (
        "<details><summary>展开</summary>"
        f"## 作者信息<br>- 作者：{'、'.join(authors)}<br>- 研究机构：当前元数据未提供可核验的机构信息，暂不推测；需以论文首页为准。<br><br>"
        f"## 摘要<br>{abstract}<br><br>"
        f"## 背景<br>{bullets(overview)}<br>- 交叉分类：{paper_class}<br>- 与前人工作的精确差异：待从 Introduction 与 Related Work 逐项核验，不根据摘要补写。<br><br>"
        "## 模型与方法<br>- 物理系统、数据集、模型架构或数学对象：待从全文定义与方法部分核验。<br>- 理论、推导、数值方法、实验或训练流程：待从全文核验，不根据摘要推断。<br>- 控制参数、边界/初始条件、近似、基线、计算资源与适用范围：待从全文核验。<br><br>"
        f"## 核心结果与证据<br>- 摘要层面的核心陈述：{contribution}<br>- 当前证据状态：摘要陈述，尚未逐项绑定定理、方程、图、表、模拟或实验。<br>- 结论类型：待全文核验后标注为严格证明、受控渐近、微扰、数值观察、实验观察或物理解释。<br><br>"
        f"## 有效性与局限<br>- 已知局限：{limitation}<br>- 有效性范围、有限尺寸/数据集/架构限制与失败模式：待全文核验。<br><br>"
        f"## 复现与资源<br>- arXiv 分类：{', '.join(categories)}<br>- Code、data、checkpoint、模拟参数与硬件：当前尚未从全文和项目链接完成核验；缺失项明确保留为缺失。<br><br>"
        "## 阅读指南<br>- 最重要的图：待完成全文 figure-candidate 比较后确定，禁止默认采用第一张图。<br>- 最重要的方程或定理：待核验全文编号与上下文后确定。<br>- 快速阅读与深入阅读路径：待根据论文实际论证结构生成。</details>"
    )
    return f"| {date} | {title_zh}<br>{title_en} | {link} | {expanded} |"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=PAPERS_MD)
    args = parser.parse_args()
    text = args.input.read_text(encoding="utf-8")
    translations = json.loads(TRANSLATIONS_ZH.read_text(encoding="utf-8"))
    curated_cards = load_curated_cards()
    ids = list(dict.fromkeys(re.findall(r"arxiv.org/abs/(\d{4}\.\d{4,5})", text)))
    metadata = fetch_metadata(ids)
    missing = sorted(set(ids) - set(metadata))
    if missing:
        raise SystemExit(f"arXiv metadata missing for: {', '.join(missing)}")
    output = "\n".join(
        enrich_row(line, metadata, translations, curated_cards) for line in text.splitlines()
    ) + "\n"
    args.input.write_text(output, encoding="utf-8")
    print(f"Expanded {len(ids)} paper cards with arXiv metadata")


if __name__ == "__main__":
    main()
