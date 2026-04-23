from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable


EventHandler = Callable[[dict[str, Any]], None]


@dataclass
class EventBus:
    _handlers: dict[str, list[EventHandler]]

    def __init__(self) -> None:
        self._handlers = defaultdict(list)

    def on(self, event_name: str, handler: EventHandler) -> None:
        self._handlers[event_name].append(handler)

    def emit(self, event_name: str, payload: dict[str, Any]) -> None:
        for handler in self._handlers.get(event_name, []):
            handler(payload)


@dataclass
class EngagementStore:
    """Tracks prior engagement so SMS remains warm-channel only."""

    email_replied_by_address: set[str]

    def __init__(self) -> None:
        self.email_replied_by_address = set()

    def mark_email_reply(self, email: str) -> None:
        self.email_replied_by_address.add(email.strip().lower())

    def has_prior_email_engagement(self, email: str) -> bool:
        return email.strip().lower() in self.email_replied_by_address
