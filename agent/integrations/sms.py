from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import requests

from agent.config import Settings
from agent.events import EngagementStore, EventBus
from agent.io_utils import append_jsonl
from agent.policy import enforce_kill_switch
from agent.types import InteractionEvent, utc_now_iso


class SmsClient:
    def __init__(
        self,
        settings: Settings,
        log_path: Path,
        event_bus: EventBus | None = None,
        engagement_store: EngagementStore | None = None,
    ) -> None:
        self.settings = settings
        self.log_path = log_path
        self.event_bus = event_bus or EventBus()
        self.engagement_store = engagement_store or EngagementStore()

    def send(self, phone_number: str, body: str, *, recipient_email: str) -> InteractionEvent:
        if not self.engagement_store.has_prior_email_engagement(recipient_email):
            event = InteractionEvent.build(
                channel="sms",
                event_type="sms_blocked_cold_channel",
                payload={"phone_number": phone_number, "recipient_email": recipient_email},
            )
            append_jsonl(self.log_path, {"event": event.to_dict(), "created_at": utc_now_iso()})
            self.event_bus.emit(event.event_type, event.to_dict())
            return event

        routed_to = enforce_kill_switch(self.settings, phone_number)
        payload = {"to_original": phone_number, "to_routed": routed_to, "body": body, "username": self.settings.africas_talking_username}
        try:
            provider_response = self._send_africas_talking(routed_to, body)
            event = InteractionEvent.build(channel="sms", event_type="sms_sent", payload={**payload, "provider_response": provider_response})
        except Exception as exc:
            event = InteractionEvent.build(channel="sms", event_type="sms_send_failed", payload={**payload, "error": str(exc)})
        append_jsonl(self.log_path, {"event": event.to_dict(), "created_at": utc_now_iso()})
        self.event_bus.emit(event.event_type, event.to_dict())
        return event

    def handle_webhook(self, payload: dict[str, Any], *, auth_header: str | None) -> InteractionEvent:
        if self.settings.sms_webhook_secret and auth_header != self.settings.sms_webhook_secret:
            event = InteractionEvent.build(
                channel="sms",
                event_type="sms_webhook_rejected",
                payload={"reason": "invalid_secret"},
            )
            append_jsonl(self.log_path, {"event": event.to_dict(), "payload": payload, "created_at": utc_now_iso()})
            self.event_bus.emit(event.event_type, event.to_dict())
            return event

        from_number = payload.get("from")
        message = payload.get("text") or payload.get("message")
        if not from_number or not message:
            event = InteractionEvent.build(
                channel="sms",
                event_type="sms_webhook_malformed",
                payload={"payload": payload},
            )
            append_jsonl(self.log_path, {"event": event.to_dict(), "created_at": utc_now_iso()})
            self.event_bus.emit(event.event_type, event.to_dict())
            return event

        event = InteractionEvent.build(
            channel="sms",
            event_type="sms_reply_received",
            payload={"from_number": from_number, "message": message},
        )
        append_jsonl(self.log_path, {"event": event.to_dict(), "created_at": utc_now_iso()})
        self.event_bus.emit(event.event_type, event.to_dict())
        return event

    def _send_africas_talking(self, phone_number: str, message: str) -> dict[str, Any]:
        if not self.settings.africas_talking_api_key:
            raise RuntimeError("AFRICAS_TALKING_API_KEY is required")
        response = requests.post(
            "https://api.africastalking.com/version1/messaging",
            headers={
                "apiKey": self.settings.africas_talking_api_key,
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "username": self.settings.africas_talking_username,
                "to": phone_number,
                "message": message,
            },
            timeout=20,
        )
        response.raise_for_status()
        if response.text.strip():
            return response.json()
        return {"status_code": response.status_code, "raw": json.loads("{}")}
