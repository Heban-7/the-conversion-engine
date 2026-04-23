from __future__ import annotations

from pathlib import Path

from agent.config import Settings
from agent.io_utils import append_jsonl
from agent.policy import enforce_kill_switch
from agent.types import InteractionEvent, utc_now_iso


class SmsClient:
    def __init__(self, settings: Settings, log_path: Path) -> None:
        self.settings = settings
        self.log_path = log_path

    def send(self, phone_number: str, body: str) -> InteractionEvent:
        routed_to = enforce_kill_switch(self.settings, phone_number)
        event = InteractionEvent.build(
            channel="sms",
            event_type="sms_sent",
            payload={"to_original": phone_number, "to_routed": routed_to, "body": body},
        )
        append_jsonl(self.log_path, {"event": event.to_dict(), "created_at": utc_now_iso()})
        return event
