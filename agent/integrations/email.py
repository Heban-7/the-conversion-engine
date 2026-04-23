from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from agent.config import Settings
from agent.io_utils import append_jsonl
from agent.policy import enforce_kill_switch
from agent.types import InteractionEvent, utc_now_iso


@dataclass
class EmailMessage:
    to: str
    subject: str
    body: str
    headers: dict[str, str]


class EmailClient:
    def __init__(self, settings: Settings, log_path: Path) -> None:
        self.settings = settings
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self.log_path.write_text("", encoding="utf-8")

    def send(self, message: EmailMessage) -> InteractionEvent:
        routed_to = enforce_kill_switch(self.settings, message.to)
        event = InteractionEvent.build(
            channel="email",
            event_type="email_sent",
            payload={
                "provider": self.settings.email_provider,
                "from": self.settings.email_from,
                "to_original": message.to,
                "to_routed": routed_to,
                "subject": message.subject,
                "headers": message.headers,
            },
        )
        self._append({"event": event.to_dict(), "message": asdict(message), "created_at": utc_now_iso()})
        return event

    def simulate_reply(self, from_email: str, body: str) -> InteractionEvent:
        event = InteractionEvent.build(
            channel="email",
            event_type="email_reply_received",
            payload={"from_email": from_email, "body": body},
        )
        self._append({"event": event.to_dict(), "created_at": utc_now_iso()})
        return event

    def _append(self, item: dict) -> None:
        append_jsonl(self.log_path, item)
