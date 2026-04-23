from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Prospect:
    domain: str
    name: str
    contact_first_name: str
    contact_email: str
    contact_phone: str
    sector: str
    required_stacks: list[str]


@dataclass
class InteractionEvent:
    correlation_id: str
    channel: str
    event_type: str
    timestamp: str
    payload: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def build(cls, channel: str, event_type: str, payload: dict[str, Any] | None = None) -> "InteractionEvent":
        return cls(
            correlation_id=str(uuid4()),
            channel=channel,
            event_type=event_type,
            timestamp=utc_now_iso(),
            payload=payload or {},
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
