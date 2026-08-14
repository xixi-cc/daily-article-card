#!/usr/bin/env python3
"""Validate the canonical evidence-aware physics+AI card structure."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS_MD = ROOT / "papers.md"
REQUIRED = [
    "作者信息",
    "一眼看懂",
    "问题与定位",
    "系统、模型与假设",
    "方法",
    "核心结果与证据",
    "有效性与局限",
    "复现与资源",
    "阅读指南",
]
FORBIDDEN = ["评级", "研究单位", "论文概述", "核心贡献", "方法描述", "评估与结果", "主要限制", "作者", "arXiv"]


def main() -> int:
    text = PAPERS_MD.read_text(encoding="utf-8")
    rows = [line for line in text.splitlines()[2:] if line.startswith("|")]
    errors: list[str] = []
    for index, row in enumerate(rows, start=1):
        headings = re.findall(r"## ([^<]+)<br>", row)
        if headings != REQUIRED:
            errors.append(f"row {index}: headings={headings}")
        for forbidden in FORBIDDEN:
            if f"## {forbidden}<br>" in row:
                errors.append(f"row {index}: forbidden section {forbidden}")
        if "当前证据状态：" not in row:
            errors.append(f"row {index}: missing evidence status")
        if "结论类型：" not in row:
            errors.append(f"row {index}: missing epistemic status")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated {len(rows)} cards against the canonical nine-section schema")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
