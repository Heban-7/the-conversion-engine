from __future__ import annotations

from pathlib import Path
from typing import Any

from agent.io_utils import append_jsonl, write_json
from agent.types import utc_now_iso


class HubSpotClient:
    def __init__(self, events_log: Path, snapshot_path: Path) -> None:
        self.events_log = events_log
        self.snapshot_path = snapshot_path

    def upsert_contact(self, contact: dict[str, Any]) -> None:
        payload = {"type": "hubspot_upsert_contact", "timestamp": utc_now_iso(), "payload": contact}
        append_jsonl(self.events_log, payload)
        write_json(self.snapshot_path, payload)

    def append_event(self, correlation_id: str, event_type: str, metadata: dict[str, Any]) -> None:
        append_jsonl(
            self.events_log,
            {
                "type": "hubspot_append_event",
                "timestamp": utc_now_iso(),
                "correlation_id": correlation_id,
                "event_type": event_type,
                "metadata": metadata,
            },
        )
