#!/usr/bin/env python3
"""Atomically advance one serial MinerU campaign item and append an event."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


STATUS_ORDER = {
    "pending": 0,
    "extracting": 1,
    "packet_ready": 2,
    "card_staged": 3,
    "card_installed": 4,
}


def file_record(path: Path) -> dict[str, object]:
    payload = path.read_bytes()
    return {
        "path": str(path),
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def valid_transition(
    current: str, destination: str, retry_blocked: bool = False
) -> bool:
    if retry_blocked:
        return current == "blocked" and destination == "extracting"
    if destination == "blocked":
        return current not in {"card_installed", "blocked"}
    if current not in STATUS_ORDER or destination not in STATUS_ORDER:
        return False
    return STATUS_ORDER[destination] == STATUS_ORDER[current] + 1


def update_campaign(
    campaign_path: Path,
    events_path: Path,
    card_id: str,
    destination: str,
    artifacts: dict[str, Path],
    note: str,
    retry_blocked: bool = False,
) -> dict[str, object]:
    campaign = json.loads(campaign_path.read_text(encoding="utf-8"))
    selection = campaign.get("selection")
    if not isinstance(selection, list):
        raise ValueError("campaign selection is missing")
    matches = [item for item in selection if item.get("card_id") == card_id]
    if len(matches) != 1:
        raise ValueError(f"expected one item for {card_id}, found {len(matches)}")
    item = matches[0]
    current = str(item.get("status", ""))
    if not valid_transition(current, destination, retry_blocked):
        raise ValueError(f"invalid status transition {current!r} -> {destination!r}")

    timestamp = datetime.now(timezone.utc).isoformat()
    artifact_records = {name: file_record(path) for name, path in artifacts.items()}
    item["status"] = destination
    item["status_updated_at"] = timestamp
    item["status_note"] = note
    if artifact_records:
        stored = item.setdefault("artifacts", {})
        stored.update(artifact_records)

    campaign["pending_cards"] = sum(
        candidate.get("status") not in {"card_existing", "card_installed", "blocked"}
        for candidate in selection
    )
    campaign["installed_cards"] = sum(
        candidate.get("status") == "card_installed" for candidate in selection
    )
    campaign["blocked_cards"] = sum(
        candidate.get("status") == "blocked" for candidate in selection
    )
    temporary = campaign_path.with_suffix(campaign_path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(campaign, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(campaign_path)

    event = {
        "timestamp": timestamp,
        "card_id": card_id,
        "from": current,
        "to": destination,
        "note": note,
        "artifacts": artifact_records,
    }
    events_path.parent.mkdir(parents=True, exist_ok=True)
    with events_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--card-id", required=True)
    parser.add_argument(
        "--status",
        required=True,
        choices=["extracting", "packet_ready", "card_staged", "card_installed", "blocked"],
    )
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--note", default="")
    parser.add_argument(
        "--retry-blocked",
        action="store_true",
        help="allow only the explicit recovery transition blocked -> extracting",
    )
    args = parser.parse_args()

    artifacts: dict[str, Path] = {}
    for value in args.artifact:
        if "=" not in value:
            raise SystemExit("--artifact must be NAME=PATH")
        name, raw_path = value.split("=", 1)
        path = Path(raw_path)
        if not name or not path.is_file():
            raise SystemExit(f"invalid artifact {value!r}")
        artifacts[name] = path

    event = update_campaign(
        args.campaign,
        args.events,
        args.card_id,
        args.status,
        artifacts,
        args.note,
        args.retry_blocked,
    )
    print(json.dumps(event, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
