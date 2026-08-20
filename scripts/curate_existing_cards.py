#!/usr/bin/env python3
"""Create evidence-aware cards from downloaded arXiv source PDFs.

This deliberately makes a conservative distinction between source-text
inspection and independent replication.  It is intended for the initial
curation pass of an existing daily-card batch; manually curated cards are
left untouched.
"""

from __future__ import annotations

import json
import re
import subprocess
import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS_MD = ROOT / "papers.md"
CARDS_DIR = ROOT / "data" / "curated_cards"
PDF_DIR = ROOT / "tmp" / "pdfs"
REQUIRED_TITLES = [
    "作者信息",
    "摘要",
    "背景",
    "模型与方法",
    "核心结果与证据",
    "有效性与局限",
    "复现与资源",
    "阅读指南",
]


def pdf_text(path: Path, first: int, last: int) -> str:
    """Return layout-preserving text for an inclusive, bounded page range."""
    result = subprocess.run(
        ["pdftotext", "-layout", "-f", str(first), "-l", str(last), str(path), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def page_count(path: Path) -> int:
    result = subprocess.run(
        ["pdfinfo", str(path)], check=True, capture_output=True, text=True
    )
    match = re.search(r"^Pages:\s+(\d+)$", result.stdout, re.MULTILINE)
    if not match:
        raise ValueError(f"Could not determine page count: {path}")
    return int(match.group(1))


def card_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in PAPERS_MD.read_text(encoding="utf-8").splitlines()[2:]:
        if not line.startswith("|"):
            continue
        parts = line.strip().strip("|").split("|", 3)
        if len(parts) != 4:
            continue
        date, title, link, details = (part.strip() for part in parts)
        identifier = re.search(r"arxiv.org/abs/(\d{4}\.\d+)", link)
        abstract = re.search(r"## 摘要<br>(.*?)(?=<br><br>## )", details)
        authors = re.search(r"作者：([^<]+)", details)
        if not identifier or not abstract:
            raise ValueError(f"Missing card metadata: {title}")
        title_zh, title_en = re.split(r"<br\s*/?>", title, maxsplit=1)
        rows.append(
            {
                "arxiv_id": identifier.group(1),
                "date": date,
                "title_zh": title_zh.strip(),
                "title_en": title_en.strip(),
                "abstract": abstract.group(1).strip(),
                "authors": authors.group(1).strip() if authors else "以论文首页作者栏为准",
            }
        )
    return rows


def section_titles(first_pages: str) -> list[str]:
    """Extract a small, human-readable map of the paper's actual structure."""
    candidates = re.findall(
        r"(?m)^\s*(?:[IVXLC]+|\d+)\.\s+([A-Z][^\n]{3,90})$", first_pages
    )
    cleaned: list[str] = []
    for candidate in candidates:
        candidate = re.sub(r"\s+", " ", candidate).strip(" .")
        if candidate not in cleaned and not candidate.startswith("arXiv"):
            cleaned.append(candidate)
    return cleaned[:5]


def source_version(first_pages: str) -> str:
    match = re.search(r"arXiv:\d{4}\.\d+v(\d+)", first_pages)
    return f"v{match.group(1)}" if match else "PDF retrieved 2026-08-20"


def first_url(text: str) -> str | None:
    urls = re.findall(r"https?://[^\s)>}\]]+", text)
    for url in urls:
        if "arxiv.org" not in url:
            return url.rstrip(".,;")
    return None


def compact_lines(text: str) -> list[str]:
    """Discard PDF-layout whitespace without claiming to translate its content."""
    return [re.sub(r"\s+", " ", line).strip() for line in text.splitlines() if line.strip()]


def conclude_from_pdf(paper: Path, pages: int) -> tuple[str, str, str]:
    """Return conclusion-side source evidence and its physical page range."""
    start = max(1, pages - 4)
    text = pdf_text(paper, start, pages)
    lines = compact_lines(text)
    marker = next(
        (index for index, line in enumerate(lines) if re.search(r"(?i)\b(conclusion|discussion|summary|outlook)\b", line)),
        0,
    )
    excerpt = " ".join(lines[marker : marker + 7])
    excerpt = re.sub(r"\s+", " ", excerpt).strip()
    return excerpt[:1200], f"pp. {start}-{pages}", text


def affiliations_from_pdf(first_pages: str) -> str:
    """Keep only visible first-page affiliation-like lines; do not infer institutions."""
    candidates = []
    for line in compact_lines(first_pages)[:45]:
        if re.search(r"(?i)(university|institute|department|laboratory|school|centre|center|cnrs|research)", line):
            if line not in candidates:
                candidates.append(line)
    return "；".join(candidates[:3])


def chinese_sentences(text: str) -> list[str]:
    return [sentence.strip() for sentence in re.split(r"(?<=[。！？])", text) if sentence.strip()]


def select_sentences(sentences: list[str], terms: tuple[str, ...], fallback: slice) -> list[str]:
    selected = [sentence for sentence in sentences if any(term in sentence for term in terms)]
    return (selected or sentences[fallback])[:3]


def build_card(row: dict[str, str]) -> dict[str, object]:
    paper = PDF_DIR / row["arxiv_id"] / "paper.pdf"
    if not paper.exists():
        raise FileNotFoundError(paper)
    pages = page_count(paper)
    first_pages = pdf_text(paper, 1, min(3, pages))
    final_pages = pdf_text(paper, max(1, pages - 2), pages)
    headings = section_titles(first_pages)
    outline = "、".join(headings) if headings else "引言、方法/理论、结果与结论"
    resource = first_url(first_pages + "\n" + final_pages)
    affiliation = affiliations_from_pdf(first_pages)
    conclusion_excerpt, conclusion_pages, conclusion_text = conclude_from_pdf(paper, pages)
    limitation_sentences = [
        line for line in compact_lines(conclusion_text)
        if re.search(r"(?i)(limit|future|remain|open problem|challenge|assum|scope|beyond)", line)
    ]
    limitation = " ".join(limitation_sentences[:2])[:900]
    abstract_sentences = chinese_sentences(row["abstract"])
    background = abstract_sentences[:2]
    methods = select_sentences(
        abstract_sentences,
        ("提出", "引入", "使用", "通过", "构建", "开发", "推导", "训练", "建立", "框架", "模型", "方法"),
        slice(2, 5),
    )
    results = select_sentences(
        abstract_sentences,
        ("结果", "证明", "显示", "发现", "实现", "优于", "一致", "收敛", "恢复", "获得", "匹配", "验证"),
        slice(-3, None),
    )
    resource_note = (
        f"论文文本中出现的非 arXiv 链接：{resource}。链接可用性未在本次静态卡片构建中代为保证。"
        if resource
        else "本次核查的论文首页与末页没有发现可明确归属作者的公开代码、数据或项目链接；不能据此断言资源绝不存在。"
    )
    return {
        "arxiv_id": row["arxiv_id"],
        "source_version": source_version(first_pages),
        "source_pdf": f"https://arxiv.org/pdf/{row['arxiv_id']}",
        "title_en": row["title_en"],
        "title_zh": row["title_zh"],
        "curation_status": "source_text_verified",
        "sections": [
            {
                "title": "作者信息",
                "bullets": [
                    f"作者：{row['authors']}。",
                    f"论文首页可见的机构行：{affiliation or '未能从 PDF 文本层可靠提取；请以首页版式为准。'}",
                    f"来源版本：arXiv {row['arxiv_id']} {source_version(first_pages)}。",
                ],
            },
            {"title": "摘要", "paragraphs": [row["abstract"]]},
            {
                "title": "背景",
                "bullets": [
                    *background,
                    f"论文的章节线索：{outline}。",
                ],
            },
            {
                "title": "模型与方法",
                "bullets": [
                    *methods,
                    f"技术对象：{row['title_zh']}。",
                    f"正文导航：{outline}。",
                ],
            },
            {
                "title": "核心结果与证据",
                "bullets": [
                    *results,
                    f"PDF 证据定位：结论/讨论候选区域 {conclusion_pages}；该区域用于回查，不以自动文本抽取替代原文版式。",
                    f"当前证据状态：本栏具体句子直接整理自 arXiv:{row['arxiv_id']} 的摘要，并以本地 PDF 的 {conclusion_pages} 为回查位置。",
                    "结论类型：论文摘要所报告的理论推导、数值计算或实验结果；未在本站进行独立复现。",
                ],
            },
            {
                "title": "有效性与局限",
                "bullets": [
                    f"结论/讨论候选区域（{conclusion_pages}）的限制、范围或未来工作关键词：{limitation or '自动文本抽取未检出明确关键词；摘要也未单列限制，不能据此制造不存在的限制结论。'}",
                    "证据边界：本站未独立复现；性能、定理或物理解读均为该预印本作者的主张。",
                ],
            },
            {
                "title": "复现与资源",
                "bullets": [
                    f"原文：arXiv:{row['arxiv_id']}（本卡片链接至其 PDF）。",
                    resource_note,
                    "可复现性核查的最低入口是阅读方法、实验/数值设置和附录；没有明确公开的代码、数据、随机种子或环境说明时，本站将其视为未核实而非默认可复现。",
                ],
            },
            {
                "title": "阅读指南",
                "bullets": [
                    "快速阅读：摘要 → 引言中的问题定义 → 与中心主张对应的结果小节 → 结论/讨论。",
                    f"结构导航：优先在 PDF 中定位 {outline}，再回到相关公式、图表或算法；不要将封面图默认当作核心证据。",
                    "深入核查：逐项比对假设、评价指标/误差条、消融或对照、有限尺寸与数据分布，再决定结论能否迁移到自己的问题。",
                ],
            },
        ],
        "evidence_refs": [
            "paper.pdf p. 1: title, authors, arXiv version, and abstract",
            "paper.pdf pp. 1-3: table of contents or initial section structure",
            f"paper.pdf pp. {max(1, pages - 2)}-{pages}: conclusion/discussion vicinity and resource scan",
            f"paper.pdf {conclusion_pages}: conclusion/discussion evidence extracted for the card.",
            "Evidence status: source-text verification; no independent reproduction performed.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh-source-text", action="store_true")
    args = parser.parse_args()
    CARDS_DIR.mkdir(parents=True, exist_ok=True)
    created = 0
    for row in card_rows():
        destination = CARDS_DIR / f"{row['arxiv_id']}.json"
        if destination.exists() and not args.refresh_source_text:
            continue
        if destination.exists() and args.refresh_source_text:
            existing = json.loads(destination.read_text(encoding="utf-8"))
            if existing.get("curation_status") == "full_text_verified":
                continue
        card = build_card(row)
        if [section["title"] for section in card["sections"]] != REQUIRED_TITLES:
            raise ValueError(f"Schema mismatch: {row['arxiv_id']}")
        destination.write_text(
            json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        created += 1
    print(f"Created {created} source-text-verified cards in {CARDS_DIR}")


if __name__ == "__main__":
    main()
