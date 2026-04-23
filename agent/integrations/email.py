from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

import requests

from agent.config import Settings
from agent.io_utils import append_jsonl
from agent.events import EventBus
from agent.policy import enforce_kill_switch
from agent.types import InteractionEvent, utc_now_iso


@dataclass
class EmailMessage:
    to: str
    subject: str
    body: str
    headers: dict[str, str]


class EmailClient:
    def __init__(self, settings: Settings, log_path: Path, event_bus: EventBus | None = None) -> None:
        self.settings = settings
        self.log_path = log_path
        self.event_bus = event_bus or EventBus()
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self.log_path.write_text("", encoding="utf-8")

    def send(self, message: EmailMessage) -> InteractionEvent:
        routed_to = enforce_kill_switch(self.settings, message.to)
        base_payload = {
            "provider": self.settings.email_provider,
            "from": self.settings.email_from,
            "to_original": message.to,
            "to_routed": routed_to,
            "subject": message.subject,
            "headers": message.headers,
        }
        try:
            provider_response = self._send_via_provider(
                routed_to=routed_to,
                subject=message.subject,
                body=message.body,
                headers=message.headers,
            )
            event = InteractionEvent.build(
                channel="email",
                event_type="email_sent",
                payload={**base_payload, "provider_response": provider_response},
            )
        except Exception as exc:
            event = InteractionEvent.build(
                channel="email",
                event_type="email_send_failed",
                payload={**base_payload, "error": str(exc)},
            )
        self._append({"event": event.to_dict(), "message": asdict(message), "created_at": utc_now_iso()})
        self.event_bus.emit(event.event_type, event.to_dict())
        return event

    def simulate_reply(self, from_email: str, body: str) -> InteractionEvent:
        event = InteractionEvent.build(
            channel="email",
            event_type="email_reply_received",
            payload={"from_email": from_email, "body": body},
        )
        self._append({"event": event.to_dict(), "created_at": utc_now_iso()})
        self.event_bus.emit(event.event_type, event.to_dict())
        return event

    def handle_webhook(self, payload: dict[str, Any], *, auth_header: str | None) -> InteractionEvent:
        if self.settings.email_webhook_secret and auth_header != self.settings.email_webhook_secret:
            event = InteractionEvent.build(
                channel="email",
                event_type="email_webhook_rejected",
                payload={"reason": "invalid_secret"},
            )
            self._append({"event": event.to_dict(), "payload": payload, "created_at": utc_now_iso()})
            self.event_bus.emit(event.event_type, event.to_dict())
            return event

        event_type = str(payload.get("type", "")).lower()
        data = payload.get("data", payload)
        if not event_type:
            event = InteractionEvent.build(
                channel="email",
                event_type="email_webhook_malformed",
                payload={"reason": "missing_type", "payload": payload},
            )
            self._append({"event": event.to_dict(), "created_at": utc_now_iso()})
            self.event_bus.emit(event.event_type, event.to_dict())
            return event

        mapped = {
            "reply.received": "email_reply_received",
            "email.replied": "email_reply_received",
            "email.bounced": "email_bounced",
            "bounce": "email_bounced",
            "email.failed": "email_send_failed",
        }.get(event_type, "email_webhook_unknown")
        event = InteractionEvent.build(channel="email", event_type=mapped, payload={"raw_type": event_type, "data": data})
        self._append({"event": event.to_dict(), "created_at": utc_now_iso()})
        self.event_bus.emit(event.event_type, event.to_dict())
        return event

    def _send_via_provider(self, *, routed_to: str, subject: str, body: str, headers: dict[str, str]) -> dict[str, Any]:
        provider = self.settings.email_provider.strip().lower()
        if provider == "resend":
            return self._send_resend(routed_to=routed_to, subject=subject, body=body, headers=headers)
        if provider == "mailersend":
            return self._send_mailersend(routed_to=routed_to, subject=subject, body=body)
        raise ValueError(f"Unsupported email provider '{self.settings.email_provider}'")

    def _send_resend(self, *, routed_to: str, subject: str, body: str, headers: dict[str, str]) -> dict[str, Any]:
        if not self.settings.resend_api_key:
            raise RuntimeError("RESEND_API_KEY is required for resend provider")
        request_payload = {
            "from": self.settings.email_from,
            "to": [routed_to],
            "subject": subject,
            "html": body,
            "headers": headers,
        }
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {self.settings.resend_api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps(request_payload),
            timeout=20,
        )
        response.raise_for_status()
        return response.json()

    def _send_mailersend(self, *, routed_to: str, subject: str, body: str) -> dict[str, Any]:
        if not self.settings.mailersend_api_key:
            raise RuntimeError("MAILERSEND_API_KEY is required for mailersend provider")
        request_payload = {
            "from": {"email": self.settings.email_from},
            "to": [{"email": routed_to}],
            "subject": subject,
            "html": body,
        }
        response = requests.post(
            "https://api.mailersend.com/v1/email",
            headers={
                "Authorization": f"Bearer {self.settings.mailersend_api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps(request_payload),
            timeout=20,
        )
        response.raise_for_status()
        if response.text.strip():
            return response.json()
        return {"status_code": response.status_code}

    def _append(self, item: dict) -> None:
        append_jsonl(self.log_path, item)
