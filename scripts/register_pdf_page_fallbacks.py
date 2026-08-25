#!/usr/bin/env python3
"""Use the first PDF page as the final cover fallback for image-less cards."""

from __future__ import annotations

import re
import subprocess
import tempfile
import urllib.request
from pathlib import Path

from fetch_paper_images import IMAGE_DIR, load_manifest, save_manifest


ROOT = Path(__file__).resolve().parents[1]
PAPERS_MD = ROOT / "papers.md"


def main() -> int:
    text = PAPERS_MD.read_text(encoding="utf-8")
    rows = re.findall(
        r"^\|\s*[^|]+\|\s*([^|]+?)\s*\|\s*(https?://[^|]+/abs/(\d{4}\.\d{4,5}))",
        text,
        flags=re.MULTILINE,
    )
    manifest = load_manifest()
    updated = 0
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    for title, abs_url, arxiv_id in rows:
        if arxiv_id in manifest:
            continue
        output = IMAGE_DIR / f"{arxiv_id}.png"
        try:
            if not output.exists():
                with tempfile.TemporaryDirectory(prefix="paper-cover-") as tmp:
                    pdf = Path(tmp) / f"{arxiv_id}.pdf"
                    request = urllib.request.Request(
                        f"https://arxiv.org/pdf/{arxiv_id}",
                        headers={"User-Agent": "physics-AI-daily-cards/1.0"},
                    )
                    with urllib.request.urlopen(request, timeout=90) as response:
                        pdf.write_bytes(response.read())
                    subprocess.run(
                        ["pdftoppm", "-f", "1", "-singlefile", "-scale-to-x", "1200", "-scale-to-y", "-1", "-png", str(pdf), str(output.with_suffix(""))],
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
            manifest[arxiv_id] = {
                "title": title.strip(),
                "abs_url": abs_url.strip(),
                "html_url": f"https://arxiv.org/pdf/{arxiv_id}",
                "path": f"assets/paper-images/{arxiv_id}.png",
                "image_url": f"https://arxiv.org/pdf/{arxiv_id}",
                "source": "pdf:first-page",
                "score": 40,
                "content_type": "image/png",
                "inside_figure": False,
                "width": 1200,
                "height": None,
            }
            updated += 1
        except Exception as exc:
            print(f"[pdf fallback] {arxiv_id} failed: {exc}")

    save_manifest(manifest)
    print(f"PDF-page cover fallbacks registered: {updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
