#!/usr/bin/env python3
"""Deterministic domain categories and topic tags for paper cards."""

from __future__ import annotations

import re
from typing import Dict, Iterable, List, Mapping, Sequence


PROFILE_LABELS = {
    "theory": "理论",
    "theory_numerics": "理论与数值",
    "theory_experiment": "理论与实验",
    "numerical": "数值计算",
    "experiment": "实验",
    "ai_empirical": "AI 实证",
}

CATEGORY_TAGS = {
    "cs.LG": "机器学习",
    "stat.ML": "机器学习",
    "cs.AI": "人工智能",
    "cs.CL": "语言模型",
    "cs.RO": "机器人",
    "cs.CV": "计算机视觉",
    "cs.NE": "神经计算",
    "q-bio.NC": "神经动力学",
    "math.PR": "随机过程",
    "math.AP": "应用数学",
    "math.OC": "优化理论",
    "math.NA": "数值分析",
    "math.DS": "动力系统",
    "math-ph": "数学物理",
    "cond-mat.stat-mech": "统计物理",
    "cond-mat.dis-nn": "无序系统与神经网络",
    "cond-mat.soft": "软物质",
    "cond-mat.str-el": "强关联体系",
    "nlin.AO": "非线性动力学",
    "nlin.CD": "混沌动力学",
    "physics.comp-ph": "计算物理",
    "physics.data-an": "物理数据分析",
    "physics.bio-ph": "生物物理",
    "physics.flu-dyn": "流体动力学",
    "quant-ph": "量子信息",
    "hep-th": "高能理论",
    "hep-lat": "格点场论",
}

KEYWORD_TAGS = (
    (("transformer", "attention head", "residual stream"), "Transformer"),
    (("large language model", "language model", "llm", "chain-of-thought"), "语言模型"),
    (("diffusion model", "flow matching", "generative model", "score-based"), "生成模型"),
    (("world model", "world-model"), "世界模型"),
    (("reinforcement learning", "policy learning", "agent"), "强化学习"),
    (("robot", "manipulation", "embodied", "vision-language-action", "vla"), "具身智能"),
    (("neural operator", "operator learning", "pdebench", "partial differential"), "神经算子"),
    (("stochastic differential", "spde", "langevin", "fokker-planck"), "随机动力学"),
    (("active matter", "active particle"), "活性物质"),
    (("phase transition", "critical", "bifurcation"), "相变与临界性"),
    (("representation", "feature learning", "latent"), "表示学习"),
    (("generalization", "sample complexity", "learnability"), "泛化理论"),
    (("optimization", "optimizer", "gradient descent", "newton-schulz", "muon"), "优化动力学"),
    (("mechanistic interpretability", "circuit", "communication map"), "机制可解释性"),
    (("scaling law", "compute scaling", "power law"), "标度律"),
    (("gauge", "symmetry", "equivariant", "invariant"), "对称性与规范结构"),
    (("stochastic", "probability", "large deviation", "random matrix"), "概率与随机过程"),
    (("fluid", "hydrodynamic", "navier-stokes", "turbulence"), "流体与水动力学"),
    (("biological", "cell", "protein", "molecular"), "生物与分子系统"),
)

FOUNDATION_KEYWORDS = (
    "theory", "theorem", "dynamics", "mechanism", "representation", "generalization",
    "optimization", "scaling", "phase transition", "bifurcation", "symmetry", "gauge",
    "learnability", "implicit bias", "information-theoretic", "operator",
)


def _ordered_unique(values: Iterable[str]) -> List[str]:
    seen = set()
    result: List[str] = []
    for value in values:
        value = str(value).strip()
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _metadata_categories(card: Mapping[str, object]) -> List[str]:
    metadata = card.get("verified_metadata")
    if not isinstance(metadata, Mapping):
        return []
    categories = metadata.get("categories")
    if not isinstance(categories, Sequence) or isinstance(categories, (str, bytes)):
        categories = []
    primary = str(metadata.get("primary_category", "")).strip()
    return _ordered_unique([primary, *(str(item) for item in categories)])


def _card_text(card: Mapping[str, object]) -> str:
    chunks = [str(card.get("title_en", "")), str(card.get("title_zh", ""))]
    metadata = card.get("verified_metadata")
    if isinstance(metadata, Mapping):
        chunks.extend([str(metadata.get("title", "")), str(metadata.get("abstract", ""))])
    provenance = card.get("provenance")
    if isinstance(provenance, Mapping):
        chunks.append(str(provenance.get("catalog_topic", "")))
    sections = card.get("sections")
    if isinstance(sections, Sequence) and not isinstance(sections, (str, bytes)):
        for section in sections:
            if not isinstance(section, Mapping):
                continue
            chunks.append(str(section.get("title", "")))
            entries = section.get("bullets") or section.get("paragraphs")
            if isinstance(entries, Sequence) and not isinstance(entries, (str, bytes)):
                chunks.extend(str(item) for item in entries[:3])
    return " ".join(chunks).lower()


def _infer_profile(card: Mapping[str, object], categories: Sequence[str], text: str) -> str:
    profile = str(card.get("paper_profile", "")).strip()
    if profile in PROFILE_LABELS:
        return profile
    has_theory = any(token in text for token in FOUNDATION_KEYWORDS) or any(
        category.startswith("math.") or category in {"math-ph", "hep-th", "cond-mat.stat-mech"}
        for category in categories
    )
    has_numerics = any(token in text for token in ("simulation", "numerical", "benchmark", "dataset"))
    has_experiment = any(token in text for token in ("experiment", "measurement", "microscopy", "laboratory"))
    has_ai = any(category.startswith(("cs.", "stat.ML")) for category in categories)
    if has_theory and has_experiment:
        return "theory_experiment"
    if has_theory and has_numerics:
        return "theory_numerics"
    if has_experiment:
        return "experiment"
    if has_theory:
        return "theory"
    if has_ai:
        return "ai_empirical"
    if has_numerics:
        return "numerical"
    return "theory"


def _infer_domain(categories: Sequence[str], text: str, profile: str) -> str:
    category_set = set(categories)
    if "cs.RO" in category_set or re.search(r"\b(?:robot(?:ics)?|embodied|manipulation|vla)\b", text):
        return "机器人与具身智能"
    if any(category.startswith("q-bio.") for category in categories) or "physics.bio-ph" in category_set:
        return "生物与神经"
    has_ai_category = any(category.startswith("cs.") or category == "stat.ML" for category in categories)
    has_ai = has_ai_category or any(
        token in text
        for token in (
            "neural", "learning", "transformer", "language model", "world model", "generative model",
            "deep learning", "representation", "optimizer", "reinforcement", "agentic", "operator learning",
        )
    )
    has_physics_category = any(
        category.startswith(("cond-mat.", "physics.", "hep-", "nlin.")) or category in {"math-ph", "quant-ph"}
        for category in categories
    )
    has_physics_text = any(
        token in text
        for token in (
            "statistical mechanics", "stochastic", "langevin", "field theory", "scalar field", "spde",
            "navier-stokes", "hydrodynamic", "condensate", "lattice gas", "active brownian", "amorphous solid",
            "fluctuation", "phase transition", "kuramoto", "hamilton-jacobi", "diffusive system",
        )
    )
    has_physics = has_physics_category or has_physics_text
    if any(token in text for token in ("tissue", "biological", "cellular", "protein", "neural circuit")):
        return "生物与神经"
    if has_ai and (has_physics_category or any(
        token in text
        for token in (
            "statistical mechanics", "langevin", "scalar field", "spde", "navier-stokes",
            "hydrodynamic", "condensate", "lattice gas", "active brownian", "amorphous solid",
            "fluctuation", "kuramoto", "diffusive system",
        )
    )):
        return "AI for Science"
    if any(category.startswith("cond-mat.") or category.startswith("nlin.") for category in categories):
        return "凝聚态与复杂系统"
    if has_ai:
        if profile in {"theory", "theory_numerics", "theory_experiment"} or any(
            token in text for token in FOUNDATION_KEYWORDS
        ):
            return "AI 基础理论"
        return "AI 方法与系统"
    if any(category.startswith("math.") or category in {"math-ph", "quant-ph", "hep-th", "hep-lat"} for category in categories):
        return "统计与数学物理"
    if has_physics:
        return "物理与复杂系统"
    return "跨学科"


def classify_card(
    card: Mapping[str, object],
    fallback_card: Mapping[str, object] | None = None,
) -> Dict[str, object]:
    """Return stable broad category, research type, and ordered topic tags."""

    fallback_card = fallback_card or {}
    categories = _ordered_unique([*_metadata_categories(card), *_metadata_categories(fallback_card)])
    text = f"{_card_text(card)} {_card_text(fallback_card)}"
    profile = _infer_profile(card, categories, text)
    if not card.get("paper_profile") and fallback_card.get("paper_profile") in PROFILE_LABELS:
        profile = str(fallback_card["paper_profile"])
    provenance = card.get("provenance")
    if not isinstance(provenance, Mapping):
        provenance = fallback_card.get("provenance") if isinstance(fallback_card.get("provenance"), Mapping) else {}
    catalog_topic = str(provenance.get("catalog_topic", "")).strip() if isinstance(provenance, Mapping) else ""

    tags: List[str] = []
    if catalog_topic:
        tags.append(catalog_topic)
    tags.extend(CATEGORY_TAGS[category] for category in categories if category in CATEGORY_TAGS)
    for keywords, label in KEYWORD_TAGS:
        if any(re.search(rf"(?<![a-z0-9]){re.escape(keyword)}(?![a-z0-9])", text) for keyword in keywords):
            tags.append(label)
    tags = _ordered_unique(tags)[:6]
    if not tags:
        tags = ["跨学科"]

    return {
        "category": _infer_domain(categories, text, profile),
        "research_type": PROFILE_LABELS.get(profile, "理论"),
        "tags": tags,
        "arxiv_categories": categories,
    }
