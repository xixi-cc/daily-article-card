#!/usr/bin/env python3
"""Fail closed when active Paper Card Standard consumers drift apart."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CURRENT_VERSION = "2.3"


def require(path: Path, fragments: tuple[str, ...]) -> list[str]:
    if not path.is_file():
        return [f"missing active standard consumer: {path.relative_to(ROOT)}"]
    text = path.read_text(encoding="utf-8")
    return [
        f"{path.relative_to(ROOT)} missing required marker: {fragment}"
        for fragment in fragments
        if fragment not in text
    ]


def main() -> int:
    errors: list[str] = []
    standard = ROOT / "docs" / "PAPER_CARD_STANDARD.md"
    if not standard.is_file():
        errors.append("missing canonical docs/PAPER_CARD_STANDARD.md")
    else:
        match = re.search(r"^Version:\s*([^\s]+)", standard.read_text(encoding="utf-8"), re.MULTILINE)
        actual = match.group(1) if match else "missing"
        if actual != CURRENT_VERSION:
            errors.append(f"canonical standard is {actual}; sync checker expects {CURRENT_VERSION}")

    errors.extend(require(
        ROOT / "docs" / "CODEX_DAILY_SCREENING_AND_PUBLICATION.md",
        ("version 2.3 or later", "figure_refs", "cover", "prefer the most important physical visualization"),
    ))
    errors.extend(require(
        ROOT / "docs" / "PAPER_CARD_STANDARD_INTEGRATION.md",
        (f"Current required version: {CURRENT_VERSION}", "arxiv-daily", "scripts/validate_paper_cards.py", "scripts/build_site.py"),
    ))
    errors.extend(require(
        ROOT / "scripts" / "validate_paper_cards.py",
        ('version_at_least(card, (2, 3))', "v2.3 requires a structured cover decision", "v2.2 forbids legacy $$ display delimiters"),
    ))
    errors.extend(require(
        ROOT / "scripts" / "build_site.py",
        ('record["cover_mode"]', "render_source_cover", "render_note_cover"),
    ))
    errors.extend(require(
        ROOT / ".github" / "workflows" / "deploy.yml",
        ("python scripts/check_card_standard_sync.py", "python scripts/validate_paper_cards.py"),
    ))
    errors.extend(require(
        ROOT / "AGENTS.md",
        ("Every completed website update must be pushed to GitHub", "git ls-remote origin", "never replaced by a Sites"),
    ))
    errors.extend(require(
        ROOT / "README.md",
        ("Every completed website update must be pushed to GitHub", "OpenAI Sites", "HEAD"),
    ))

    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Paper Card Standard v{CURRENT_VERSION} is synchronized across active repository consumers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
