from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException

from agent.config import load_settings
from agent.events import EngagementStore, EventBus
from agent.integrations.email import EmailClient
from agent.integrations.sms import SmsClient


settings = load_settings()
event_bus = EventBus()
engagement_store = EngagementStore()
logs_dir = settings.interim_artifacts_dir / "webhook_logs"
logs_dir.mkdir(parents=True, exist_ok=True)
email_client = EmailClient(settings, logs_dir / "email_webhooks.jsonl", event_bus=event_bus)
sms_client = SmsClient(settings, logs_dir / "sms_webhooks.jsonl", event_bus=event_bus, engagement_store=engagement_store)


def _track_email_reply(event_payload: dict) -> None:
    from_email = event_payload.get("payload", {}).get("data", {}).get("from_email")
    if from_email:
        engagement_store.mark_email_reply(from_email)


event_bus.on("email_reply_received", _track_email_reply)
app = FastAPI(title="Tenacious Inbound Webhooks", version="1.0.0")


@app.post("/webhooks/email")
def inbound_email_webhook(payload: dict, x_webhook_secret: str | None = Header(default=None)) -> dict:
    event = email_client.handle_webhook(payload, auth_header=x_webhook_secret)
    if event.event_type == "email_webhook_rejected":
        raise HTTPException(status_code=401, detail="invalid webhook secret")
    if event.event_type == "email_webhook_malformed":
        raise HTTPException(status_code=400, detail="malformed email webhook payload")
    return {"ok": True, "event_type": event.event_type, "correlation_id": event.correlation_id}


@app.post("/webhooks/sms")
def inbound_sms_webhook(payload: dict, x_webhook_secret: str | None = Header(default=None)) -> dict:
    event = sms_client.handle_webhook(payload, auth_header=x_webhook_secret)
    if event.event_type == "sms_webhook_rejected":
        raise HTTPException(status_code=401, detail="invalid webhook secret")
    if event.event_type == "sms_webhook_malformed":
        raise HTTPException(status_code=400, detail="malformed sms webhook payload")
    return {"ok": True, "event_type": event.event_type, "correlation_id": event.correlation_id}
