#!/usr/bin/env python3
"""Record Paper Card stage costs and produce a risk-ranked structural audit."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from scripts.card_taxonomy import PROFILE_LABELS
except ModuleNotFoundError:  # Direct execution sets scripts/ as sys.path[0].
    from card_taxonomy import PROFILE_LABELS


METRICS_SCHEMA = "paper-card-stage-metrics-v1"
AUDIT_SCHEMA = "paper-card-risk-audit-v1"
THEORY_PROFILES = {"theory", "theory_numerics", "theory_experiment"}


def version_tuple(value: object) -> tuple[int, ...] | None:
    if not isinstance(value, str):
        return None
    parts = value.split(".")
    if not parts or any(not part.isdigit() for part in parts):
        return None
    return tuple(int(part) for part in parts)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def atomic_write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(payload, encoding="utf-8")
    temporary.replace(path)


def file_record(path: Path) -> dict[str, object]:
    payload = path.read_bytes()
    return {
        "path": str(path),
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def load_receipt(path: Path, card_id: str) -> dict[str, Any]:
    if not path.exists():
        return {"schema": METRICS_SCHEMA, "card_id": card_id, "stages": {}}
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema") != METRICS_SCHEMA or value.get("card_id") != card_id:
        raise ValueError("metrics receipt identity mismatch")
    return value


def start_stage(path: Path, card_id: str, stage: str, now: datetime | None = None) -> dict[str, Any]:
    receipt = load_receipt(path, card_id)
    stages = receipt.setdefault("stages", {})
    if stage in stages:
        raise ValueError(f"stage already exists; use a distinct retry stage name: {stage}")
    timestamp = (now or utc_now()).isoformat()
    stages[stage] = {"started_at": timestamp, "status": "running"}
    receipt.setdefault("created_at", timestamp)
    receipt["updated_at"] = timestamp
    atomic_write(path, receipt)
    return receipt


def finish_stage(
    path: Path,
    card_id: str,
    stage: str,
    status: str,
    token_counts: dict[str, int] | None = None,
    artifacts: dict[str, Path] | None = None,
    note: str = "",
    now: datetime | None = None,
) -> dict[str, Any]:
    receipt = load_receipt(path, card_id)
    entry = receipt.get("stages", {}).get(stage)
    if not isinstance(entry, dict) or not entry.get("started_at"):
        raise ValueError(f"stage has not started: {stage}")
    if entry.get("finished_at"):
        raise ValueError(f"stage already finished: {stage}")
    finished = now or utc_now()
    started = parse_time(str(entry["started_at"]))
    if finished < started:
        raise ValueError("finish time precedes start time")
    entry.update(
        {
            "finished_at": finished.isoformat(),
            "duration_seconds": round((finished - started).total_seconds(), 6),
            "status": status,
        }
    )
    if token_counts:
        entry["tokens"] = token_counts
    if artifacts:
        entry["artifacts"] = {name: file_record(value) for name, value in artifacts.items()}
    if note:
        entry["note"] = note
    receipt["updated_at"] = finished.isoformat()
    completed = [item for item in receipt["stages"].values() if item.get("finished_at")]
    receipt["summary"] = {
        "completed_stages": len(completed),
        "duration_seconds": round(sum(float(item.get("duration_seconds", 0)) for item in completed), 6),
        "input_tokens": sum(int(item.get("tokens", {}).get("input", 0)) for item in completed),
        "output_tokens": sum(int(item.get("tokens", {}).get("output", 0)) for item in completed),
        "cached_tokens": sum(int(item.get("tokens", {}).get("cached", 0)) for item in completed),
    }
    atomic_write(path, receipt)
    return receipt


def string_chars(value: object) -> int:
    if isinstance(value, str):
        return len(value)
    if isinstance(value, list):
        return sum(string_chars(item) for item in value)
    if isinstance(value, dict):
        return sum(string_chars(item) for item in value.values())
    return 0


def packet_index(packet_roots: list[Path]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for root in packet_roots:
        for path in root.rglob("evidence_packet.json"):
            try:
                packet = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            campaign_item = packet.get("campaign_item")
            card_id = campaign_item.get("card_id") if isinstance(campaign_item, dict) else None
            card_id = card_id or packet.get("arxiv_id")
            if card_id:
                result[str(card_id)] = packet
    return result


def audit_cards(
    card_dirs: list[Path],
    packet_roots: list[Path] | None = None,
    depth_warning: int = 2_000,
    packet_warning_tokens: int = 7_800,
) -> dict[str, Any]:
    packets = packet_index(packet_roots or [])
    items: list[dict[str, Any]] = []
    cover_modes: Counter[str] = Counter()
    profiles: Counter[str] = Counter()
    equation_counts: Counter[int] = Counter()
    figure_counts: Counter[int] = Counter()
    for directory in card_dirs:
        for path in sorted(directory.glob("*.json")):
            try:
                card = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as error:
                items.append({"card_id": path.stem, "path": str(path), "risks": [f"invalid_json:{error}"]})
                continue
            card_id = str(card.get("arxiv_id") or card.get("card_id") or path.stem)
            profile = str(card.get("paper_profile", "missing"))
            equations = card.get("equation_refs") if isinstance(card.get("equation_refs"), list) else []
            figures = card.get("figure_refs") if isinstance(card.get("figure_refs"), list) else []
            cover = card.get("cover") if isinstance(card.get("cover"), dict) else {}
            evidence = card.get("evidence_refs") if isinstance(card.get("evidence_refs"), list) else []
            section_chars = string_chars(card.get("sections", []))
            risks: list[str] = []
            card_version = version_tuple(card.get("card_standard_version"))
            if card_version is None or card_version < (2, 3):
                risks.append("legacy_standard_review")
            if profile not in PROFILE_LABELS:
                risks.append("missing_or_invalid_profile_review")
            if not cover.get("mode"):
                risks.append("missing_cover_review")
            if section_chars < depth_warning:
                risks.append("near_depth_floor")
            if profile in THEORY_PROFILES and not equations:
                risks.append("theory_without_equation_review")
            if len(evidence) <= 3:
                risks.append("minimum_evidence_only")
            packet = packets.get(card_id)
            packet_tokens = None
            pdf_pages = None
            if isinstance(packet, dict):
                size = packet.get("size")
                source = packet.get("source")
                if isinstance(size, dict):
                    packet_tokens = size.get("approximate_tokens")
                if isinstance(source, dict):
                    pdf_pages = source.get("pdf_page_count")
                if isinstance(packet_tokens, int) and packet_tokens >= packet_warning_tokens:
                    risks.append("evidence_packet_near_cap")
                if isinstance(pdf_pages, int) and pdf_pages > 50:
                    risks.append("long_paper_review")
            cover_modes[str(cover.get("mode", "missing"))] += 1
            profiles[profile] += 1
            equation_counts[len(equations)] += 1
            figure_counts[len(figures)] += 1
            if risks:
                items.append(
                    {
                        "card_id": card_id,
                        "path": str(path),
                        "paper_profile": profile,
                        "card_standard_version": card.get("card_standard_version"),
                        "section_chars": section_chars,
                        "equation_refs": len(equations),
                        "figure_refs": len(figures),
                        "evidence_refs": len(evidence),
                        "packet_tokens": packet_tokens,
                        "pdf_pages": pdf_pages,
                        "risks": risks,
                    }
                )
    items.sort(key=lambda item: (-len(item["risks"]), item["card_id"]))
    total_cards = sum(profiles.values())
    return {
        "schema": AUDIT_SCHEMA,
        "thresholds": {
            "depth_warning": depth_warning,
            "packet_warning_tokens": packet_warning_tokens,
        },
        "summary": {
            "cards": total_cards,
            "risk_items": len(items),
            "cover_modes": dict(cover_modes),
            "paper_profiles": dict(profiles),
            "equation_ref_counts": {str(key): value for key, value in equation_counts.items()},
            "figure_ref_counts": {str(key): value for key, value in figure_counts.items()},
        },
        "items": items,
        "boundary": "Risk flags route review; they do not establish a scientific error.",
    }


def parse_artifacts(values: list[str]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise ValueError("artifact must use NAME=PATH")
        name, raw_path = value.split("=", 1)
        path = Path(raw_path)
        if not name or not path.is_file():
            raise ValueError(f"invalid artifact: {value}")
        result[name] = path
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start")
    start.add_argument("--receipt", type=Path, required=True)
    start.add_argument("--card-id", required=True)
    start.add_argument("--stage", required=True)

    finish = subparsers.add_parser("finish")
    finish.add_argument("--receipt", type=Path, required=True)
    finish.add_argument("--card-id", required=True)
    finish.add_argument("--stage", required=True)
    finish.add_argument("--status", choices=("passed", "failed", "blocked"), required=True)
    finish.add_argument("--input-tokens", type=int, default=0)
    finish.add_argument("--output-tokens", type=int, default=0)
    finish.add_argument("--cached-tokens", type=int, default=0)
    finish.add_argument("--artifact", action="append", default=[])
    finish.add_argument("--note", default="")

    audit = subparsers.add_parser("audit")
    audit.add_argument("--cards-dir", type=Path, action="append", required=True)
    audit.add_argument("--packet-root", type=Path, action="append", default=[])
    audit.add_argument("--depth-warning", type=int, default=2_000)
    audit.add_argument("--packet-warning-tokens", type=int, default=7_800)
    audit.add_argument("--output", type=Path)

    args = parser.parse_args()
    if args.command == "start":
        result = start_stage(args.receipt, args.card_id, args.stage)
    elif args.command == "finish":
        result = finish_stage(
            args.receipt,
            args.card_id,
            args.stage,
            args.status,
            {"input": args.input_tokens, "output": args.output_tokens, "cached": args.cached_tokens},
            parse_artifacts(args.artifact),
            args.note,
        )
    else:
        result = audit_cards(
            args.cards_dir,
            args.packet_root,
            args.depth_warning,
            args.packet_warning_tokens,
        )
        if args.output:
            atomic_write(args.output, result)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
