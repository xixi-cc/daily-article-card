#!/usr/bin/env python3
"""Split a full Paper Card evidence packet into a small core and lossless supplements."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any


CORE_SCHEMA = "paper-card-evidence-core-v1"
MANIFEST_SCHEMA = "paper-card-evidence-layers-v1"


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def approximate_tokens(value: object) -> int:
    return (len(json_bytes(value)) + 3) // 4


def clip_text(value: object, limit: int) -> object:
    if not isinstance(value, str) or len(value) <= limit:
        return value
    return value[: max(0, limit - 1)].rstrip() + "…"


def clipped_excerpt(value: object, text_limit: int) -> object:
    if not isinstance(value, dict):
        return value
    result = dict(value)
    if "text" in result:
        result["text"] = clip_text(result["text"], text_limit)
    return result


def build_core(packet: dict[str, Any], target_tokens: int) -> dict[str, Any]:
    page_evidence = packet.get("page_evidence")
    if not isinstance(page_evidence, dict):
        page_evidence = {}

    scale = 1.0
    while scale >= 0.2:
        excerpt_limit = max(700, int(2_500 * scale))
        first_page_limit = max(700, int(2_400 * scale))
        caption_limit = max(300, int(800 * scale))
        quantitative_limit = max(220, int(480 * scale))
        equation_candidates = list(packet.get("mineru_equation_candidates") or [])
        image_candidates = list(packet.get("mineru_images") or [])
        caption_candidates = list(page_evidence.get("captions") or [])
        required_on_demand = []
        if not page_evidence.get("method") or not page_evidence.get("results"):
            required_on_demand.append("structure")
        if equation_candidates:
            required_on_demand.append("equations")
        if image_candidates or caption_candidates:
            required_on_demand.append("figures")
        required_on_demand.append("full_packet")
        core = {
            "schema": CORE_SCHEMA,
            "source_packet": {
                "sha256": packet.get("_source_packet_sha256", ""),
                "full_packet": "supplements/full_packet.json",
            },
            "campaign_item": packet.get("campaign_item"),
            "source": packet.get("source"),
            "quality_boundary": packet.get("quality_boundary"),
            "first_page": clip_text(packet.get("first_page"), first_page_limit),
            "page_evidence": {
                key: clipped_excerpt(page_evidence.get(key), excerpt_limit)
                for key in (
                    "introduction",
                    "method",
                    "results",
                    "conclusion_or_limitations",
                    "conclusion",
                )
                if page_evidence.get(key) is not None
            },
            "decisive_captions": [
                clipped_excerpt(item, caption_limit)
                for item in list(page_evidence.get("captions") or [])[:3]
            ],
            "quantitative_signals": [
                clipped_excerpt(item, quantitative_limit)
                for item in list(page_evidence.get("quantitative_lines") or [])[:6]
            ],
            "verified_urls": list(page_evidence.get("urls") or [])[:12],
            "on_demand": {
                "equations": "supplements/equations.json",
                "figures": "supplements/figures.json",
                "structure": "supplements/structure.json",
                "full_packet": "supplements/full_packet.json",
            },
            "required_on_demand": required_on_demand,
            "read_order": (
                "Read core first, then every required_on_demand artifact. "
                "Use full_packet and the source PDF/TeX for final claim, equation, and figure checks."
            ),
        }
        if approximate_tokens(core) <= target_tokens:
            core["size"] = {
                "approximate_tokens": 0,
                "target_tokens": target_tokens,
            }
            core["size"]["approximate_tokens"] = approximate_tokens(core)
            if approximate_tokens(core) <= target_tokens:
                return core
        scale *= 0.75
    raise ValueError(
        f"core metadata exceeds the {target_tokens}-token target; "
        "increase --target-tokens instead of dropping source authority"
    )


def write_json(path: Path, value: object) -> dict[str, object]:
    payload = json_bytes(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(payload)
    temporary.replace(path)
    return {"path": str(path), "bytes": len(payload), "sha256": sha256_bytes(payload)}


def split_packet(
    input_path: Path,
    output_dir: Path,
    target_tokens: int = 5_000,
    force: bool = False,
) -> dict[str, Any]:
    if target_tokens < 1_500:
        raise ValueError("target_tokens must be at least 1500")
    if output_dir.exists() and any(output_dir.iterdir()) and not force:
        raise FileExistsError(f"output directory is not empty: {output_dir}")

    source_payload = input_path.read_bytes()
    packet = json.loads(source_payload)
    if not isinstance(packet, dict):
        raise ValueError("evidence packet must be a JSON object")
    packet["_source_packet_sha256"] = sha256_bytes(source_payload)

    supplements = output_dir / "supplements"
    supplements.mkdir(parents=True, exist_ok=True)
    full_packet = supplements / "full_packet.json"
    shutil.copyfile(input_path, full_packet)

    page_evidence = packet.get("page_evidence")
    if not isinstance(page_evidence, dict):
        page_evidence = {}
    records: dict[str, dict[str, object]] = {}
    records["full_packet"] = {
        "path": str(full_packet),
        "bytes": len(source_payload),
        "sha256": sha256_bytes(source_payload),
    }
    records["equations"] = write_json(
        supplements / "equations.json",
        {
            "source_packet_sha256": sha256_bytes(source_payload),
            "mineru_equation_candidates": packet.get("mineru_equation_candidates", []),
            "authority": (packet.get("quality_boundary") or {}).get("equation_authority")
            if isinstance(packet.get("quality_boundary"), dict)
            else None,
        },
    )
    records["figures"] = write_json(
        supplements / "figures.json",
        {
            "source_packet_sha256": sha256_bytes(source_payload),
            "captions": page_evidence.get("captions", []),
            "mineru_images": packet.get("mineru_images", []),
        },
    )
    records["structure"] = write_json(
        supplements / "structure.json",
        {
            "source_packet_sha256": sha256_bytes(source_payload),
            "headings": page_evidence.get("headings", []),
            "mineru_sections": packet.get("mineru_sections", []),
            "page_evidence": page_evidence,
        },
    )

    core = build_core(packet, target_tokens)
    records["core"] = write_json(output_dir / "core.json", core)
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "source": str(input_path),
        "source_sha256": sha256_bytes(source_payload),
        "core_approximate_tokens": approximate_tokens(core),
        "target_tokens": target_tokens,
        "lossless_full_packet_preserved": True,
        "artifacts": records,
    }
    write_json(output_dir / "manifest.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--target-tokens", type=int, default=5_000)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    manifest = split_packet(args.input, args.output_dir, args.target_tokens, args.force)
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
