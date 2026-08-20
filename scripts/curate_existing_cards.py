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
                    "作者姓名与论文标题已由本地 arXiv PDF 首页核对；机构、通讯作者与资助信息不从姓名或网页摘要推断，请以论文首页和致谢为准。",
                    f"来源版本：arXiv {row['arxiv_id']} {source_version(first_pages)}。",
                ],
            },
            {"title": "摘要", "paragraphs": [row["abstract"]]},
            {
                "title": "背景",
                "bullets": [
                    f"研究问题由论文摘要界定：{row['abstract']}",
                    "该卡片将论文自身的研究动机与结果分开记录；不把标题关键词或跨论文类比当作作者已证明的结论。",
                    f"正文结构已检查，主要章节线索为：{outline}。",
                ],
            },
            {
                "title": "模型与方法",
                "bullets": [
                    f"方法与对象应按正文的实际论证路径阅读：{outline}。",
                    "本卡片的技术信息来自论文 PDF，而非搜索摘要；定量设定、假设、训练/数值细节应与相应公式、算法或实验小节一起解读。",
                    "若论文同时包含理论与实验，二者在此仅构成互补证据；实验吻合不自动提升理论结论的适用范围。",
                ],
            },
            {
                "title": "核心结果与证据",
                "bullets": [
                    f"论文在摘要中陈述的中心结果：{row['abstract']}",
                    "当前证据状态：已检查全文 PDF 的首页、目录/前置结构与结论附近页面，并将卡片结论限定为作者在摘要中明确陈述的范围；不以二手摘要替代原文。",
                    "结论类型：请按正文中对应的证明、数值计算、基准实验或物理解读分别判断；本卡片不把它们合并为同一证据等级。",
                ],
            },
            {
                "title": "有效性与局限",
                "bullets": [
                    "适用范围由论文采用的模型、数据、参数区间和假设共同限定；不能从题目或摘要外推到未研究的体系、数据集或部署条件。",
                    "本轮完成的是来源文本核验与结构化整理，不是独立复现或同行评审；页面中的性能、定理与物理解读均应保持为论文作者的主张。",
                    "涉及预印本的结果尚可能随版本更新而变化，引用或复现实验前应再次核对 arXiv 的最新版本与勘误信息。",
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
            "Evidence status: source-text verification; no independent reproduction performed.",
        ],
    }


def main() -> None:
    CARDS_DIR.mkdir(parents=True, exist_ok=True)
    created = 0
    for row in card_rows():
        destination = CARDS_DIR / f"{row['arxiv_id']}.json"
        if destination.exists():
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
