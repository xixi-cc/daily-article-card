"""Reader-facing metadata derived from existing verified cards.

These views never modify the scientific source, admission, or provenance.
"""
from __future__ import annotations

import re
from datetime import date


MATH_TOKEN = re.compile(r"\\\(.+?\\\)|\\\[.+?\\\]|\$\$.+?\$\$|(?<!\$)\$(?!\$)[^$]+\$", re.DOTALL)


def preview_prose(text: str) -> str:
    tokens: list[str] = []
    def stash(match: re.Match) -> str:
        tokens.append(match.group(0))
        return f"MATHPLACEHOLDER{len(tokens)-1}END"
    prose = MATH_TOKEN.sub(stash, text)
    prose = re.sub(r"\*\*|__|`", "", prose)
    prose = re.sub(r"[（(][^（）()]*\bPDF\b[^（）()]*[）)]", "", prose)
    prose = re.sub(r"\s+[。；]", lambda m: m.group(0).strip(), prose)
    for i, token in enumerate(tokens):
        prose = prose.replace(f"MATHPLACEHOLDER{i}END", token)
    return prose


def date_value(value: object) -> str:
    text = str(value or "")
    match = re.match(r"^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?(?:T|$)", text)
    if not match:
        return ""
    year, month, day = match.groups()
    try:
        date(int(year), int(month or 1), int(day or 1))
    except ValueError:
        return ""
    return "-".join(part for part in (year, month, day) if part)


def section_entries(card: dict, titles: tuple[str, ...]) -> list[str]:
    for section in card.get("sections", []):
        if isinstance(section, dict) and any(t in section.get("title", "") for t in titles):
            return [str(x) for x in (section.get("paragraphs") or section.get("bullets") or [])]
    return []


def chinese_preview(card: dict, fallback: str = "") -> str:
    """Use complete existing Chinese sentences, never clip a math expression."""
    candidates = section_entries(card, ("摘要",)) + section_entries(card, ("研究问题", "论文概述"))
    candidates += [fallback]
    for candidate in candidates:
        if not re.search(r"[\u4e00-\u9fff]", candidate):
            continue
        candidate = re.sub(r"^本文的论证主线由以下经过全文核验的节点构成[：:]\s*", "", candidate)
        candidate = preview_prose(candidate)
        # Production bookkeeping is not an abstract.
        if re.match(r"^(作者[：:]|机构[：:]|版本[：:]|来源[：:]|卡片内容来自|本文按本地全文)", candidate):
            continue
        math_tokens: list[str] = []
        def protect(match: re.Match) -> str:
            math_tokens.append(match.group(0))
            return f"MATHSENTENCE{len(math_tokens)-1}END"
        protected = MATH_TOKEN.sub(protect, candidate.strip())
        sentences = re.split(r"(?<=[。！？])", protected)
        parts: list[str] = []
        for sentence in sentences:
            if not sentence:
                continue
            for i, token in enumerate(math_tokens):
                sentence = sentence.replace(f"MATHSENTENCE{i}END", token)
            if parts and len("".join(parts)) + len(sentence) > 240:
                break
            parts.append(sentence)
            if len(parts) == 3:
                break
        result = "".join(parts).strip()
        # An explicit limitation at the end of a short abstract belongs in it.
        if len(candidate) <= 320:
            result = candidate.strip()
        return result
    return ""


def reader_metadata(card: dict, identifier: str = "") -> dict:
    metadata = card.get("verified_metadata") or {}
    authors = metadata.get("authors") or card.get("authors") or []
    if isinstance(authors, list):
        authors = "、".join(str(a.get("name", "")) if isinstance(a, dict) else str(a) for a in authors)
    if not authors:
        entries = section_entries(card, ("作者信息", "研究单位"))
        for entry in entries:
            match = re.match(r"^作者[：:]\s*(.+?)(?:[。；]|$)", entry)
            if match:
                authors = match.group(1)
                break
        if not authors and entries:
            authors = re.split(r"[。；]", entries[0], maxsplit=1)[0]
            authors = re.sub(r"（[^）]*）|\([^)]*\)", "", authors).strip()
    reference = metadata.get("journal_reference") or metadata.get("journal_ref")
    journal = metadata.get("journal") or metadata.get("venue") or reference or ""
    if not isinstance(journal, str):
        journal = ""
    numbering = []
    citation_year = ""
    if not journal:
        candidates = [str(metadata.get("comment") or "")]
        candidates += section_entries(card, ("作者信息",))
        for candidate in candidates:
            # Only a printed bibliographic citation, not an affiliation/year guess.
            jhep = re.search(r"((?:JHEP|Journal of High Energy Physics)\s+\d{2}\s*\((\d{4})\)\s*\d+)", candidate)
            if jhep:
                journal, citation_year = jhep.groups()
                break
            match = re.search(r"(?:^|[；;])\s*([^；;。\n]+?\s+\d+[A-Za-z]?\s*,\s*[\dA-Za-z–\-]+\s*\((\d{4})\))", candidate)
            if match:
                journal = re.sub(r"^(?:期刊|发表于|发表)[：:]?\s*", "", match.group(1))
                citation_year = match.group(2)
                break
            venue = re.search(r"(?:来源|期刊|会议|发表于)[：:]\s*([^；;。]+)", candidate)
            if venue and re.search(r"ICML|ICLR|NeurIPS|COLT|AAAI|AISTATS|CVPR|ICCV|ECCV|PNAS|Nature|Science|Physical Review|Phys\. Rev|PRL|PRX|PRE|PRR|JHEP|Journal|Archive|Transactions|Proceedings", venue.group(1)):
                journal = venue.group(1).strip()
                year = re.search(r"年份[：:]\s*(\d{4})", candidate)
                citation_year = year.group(1) if year else ""
                break
    for key, label in (("volume", "卷"), ("issue", "期"), ("article_number", "文章号"), ("article", "文章号"), ("pages", "页")):
        value = metadata.get(key)
        if value and not (key == "article" and metadata.get("article_number")):
            numbering.append(f"{label} {value}")
    if not journal:
        journal = "发表信息待核验" if (metadata.get("doi") or identifier.startswith("doi-")) else "预印本" if identifier else "发表信息待核验"
        if identifier:
            numbering = [f"arXiv:{identifier}"] if re.match(r"\d{4}\.\d+", identifier) else [identifier]
    return {"authors": str(authors or "作者信息待核验"), "journal": journal, "journal_number": " · ".join(numbering), "citation_publication_year": citation_year}


def presentation_fields(card: dict, record: dict) -> dict:
    metadata = card.get("verified_metadata") or {}
    provenance = card.get("provenance") or {}
    selection = card.get("selection_record") or {}
    grade = selection.get("grade", "")
    # Private Collection editorial grades are independently attributed.
    if grade not in ("S", "A", "B"):
        assessment = card.get("editorial_assessment") or {}
        grade = assessment.get("grade", "") if isinstance(assessment, dict) else ""
    bibliography = reader_metadata(card, str(record.get("arxiv_id") or record.get("card_id") or ""))
    published = date_value(metadata.get("publication_date") or metadata.get("original_publication_date") or bibliography["citation_publication_year"] or metadata.get("published"))
    collected = date_value(record.get("date")) if record.get("program") == "Daily" else date_value(provenance.get("collection_date") or provenance.get("sampled_at"))
    return {
        **bibliography,
        "work_id": str(metadata.get("arxiv_id") or record.get("arxiv_id") or record.get("card_id") or ""),
        "published": published,
        "collection_date": collected if len(collected) == 10 else "",
        "grade": grade if grade in ("S", "A", "B") else "",
        "preview_text": chinese_preview(card, str(record.get("preview_text", ""))),
    }


def merge_reader_lists(daily: list[dict], collection: list[dict]) -> list[dict]:
    """Merge presentation only; retain aliases and both independent records."""
    merged: dict[str, dict] = {}
    for item in [*daily, *collection]:
        identity = str(item.get("work_id") or item.get("arxiv_id") or item.get("card_id") or item["detail_path"])
        identity = re.sub(r"v\d+$", "", identity)
        program = "collection" if item.get("program") == "Collection" else "daily"
        alias = f"{program}:{item.get('arxiv_id') or item['detail_path']}"
        aliases = [alias]
        if not item.get("arxiv_id") and item.get("card_id"):
            aliases.append(f"{program}:{item['card_id']}")
        if identity not in merged:
            merged[identity] = {**item, "favorite_keys": aliases, "source_records": [{"program": item.get("program"), "detail_path": item["detail_path"], "collection_date": item.get("collection_date", ""), "grade": item.get("grade", "")}]}
        else:
            current = merged[identity]
            current["favorite_keys"].extend(key for key in aliases if key not in current["favorite_keys"])
            current["source_records"].append({"program": item.get("program"), "detail_path": item["detail_path"], "collection_date": item.get("collection_date", ""), "grade": item.get("grade", "")})
            better_image = not current.get("paper_image_path") or (current.get("cover_mode") == "source_excerpt" and item.get("cover_mode") == "source_figure")
            if better_image and item.get("paper_image_path"):
                # Open the matching reviewed detail/cover, not a different
                # version's text-only page behind the image used in the list.
                for field in ("paper_image_path", "paper_image_full_path", "cover_mode", "cover_alt_text", "detail_path", "cover_path", "title", "title_zh", "preview_text", "reader_cover_revision", "authors", "reading_minutes", "section_count"):
                    current[field] = item.get(field, "")
            if not current.get("published"):
                current["published"] = item.get("published", "")
    return list(merged.values())
