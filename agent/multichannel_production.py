from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from agent.composer import compose_cold_email, compose_sms_for_scheduling
from agent.config import Settings
from agent.enrichment.pipeline import generate_briefs
from agent.events import EngagementStore, EventBus
from agent.integrations.calcom import CalComClient
from agent.integrations.email import EmailClient, EmailMessage
from agent.integrations.hubspot import HubSpotClient
from agent.integrations.langfuse import LangfuseClient
from agent.integrations.sms import SmsClient
from agent.types import Prospect


@dataclass
class MultiChannelProductionService:
    """Concrete email->sms->crm->calendar->trace production workflow."""

    settings: Settings
    base_dir: Path

    def __post_init__(self) -> None:
        self.logs_dir = self.base_dir / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.event_bus = EventBus()
        self.engagement_store = EngagementStore()
        self.email = EmailClient(self.settings, self.logs_dir / "email_events.jsonl", event_bus=self.event_bus)
        self.sms = SmsClient(
            self.settings,
            self.logs_dir / "sms_events.jsonl",
            event_bus=self.event_bus,
            engagement_store=self.engagement_store,
        )
        self.hubspot = HubSpotClient(self.logs_dir / "hubspot_events.jsonl", self.base_dir / "hubspot_snapshot.json")
        self.calcom = CalComClient(self.logs_dir / "calcom_events.jsonl", self.base_dir / "cal_booking_snapshot.json")
        self.langfuse = LangfuseClient(self.logs_dir / "langfuse_events.jsonl")

    def run_for_prospect(self, prospect: Prospect) -> dict[str, Any]:
        enrichment = generate_briefs(self.settings.source_dir, self.base_dir, prospect)
        lead_signal = (
            f"Observed job-post velocity from {enrichment.hiring_signal_brief['hiring_velocity']['open_roles_60_days_ago']} "
            f"to {enrichment.hiring_signal_brief['hiring_velocity']['open_roles_today']} roles in 60 days."
        )
        email_body, _scorecard = compose_cold_email(
            first_name=prospect.contact_first_name,
            company=prospect.name,
            lead_signal=lead_signal,
            ask="Open to a 15-minute discovery call?",
        )
        sent = self.email.send(
            EmailMessage(
                to=prospect.contact_email,
                subject="Request: 15-minute discovery fit check",
                body=email_body,
                headers={"X-Tenacious-Status": "draft"},
            )
        )
        self.langfuse.trace("outbound_email", sent.correlation_id, {"prospect": prospect.domain})
        self.hubspot.upsert_contact(
            {
                "email": prospect.contact_email,
                "company": prospect.name,
                "domain": prospect.domain,
                "segment": enrichment.hiring_signal_brief["primary_segment_match"],
                "tenacious_status": "draft",
            }
        )

        # Example inbound email reply path -> unlock SMS warm channel.
        reply = self.email.simulate_reply(prospect.contact_email, "SMS is faster for scheduling.")
        self.engagement_store.mark_email_reply(prospect.contact_email)
        self.hubspot.append_event(reply.correlation_id, "email_reply_received", {"preference": "sms"})

        booking_link, booking_event = self.calcom.create_booking_link(prospect.domain)
        sms_text = compose_sms_for_scheduling(first_name=prospect.contact_first_name, booking_link=booking_link)
        sms_event = self.sms.send(prospect.contact_phone, sms_text, recipient_email=prospect.contact_email)
        self.langfuse.trace("outbound_sms", sms_event.correlation_id, {"prospect": prospect.domain})
        self.hubspot.append_event(booking_event.correlation_id, "booking_link_generated", {"url": booking_link})

        confirmed = self.calcom.confirm_booking(
            booking_link,
            (datetime.now(timezone.utc) + timedelta(days=2)).replace(microsecond=0).isoformat(),
        )
        self.hubspot.append_event(confirmed.correlation_id, "booking_confirmed", confirmed.payload)
        self.langfuse.trace("booking_confirmed", confirmed.correlation_id, {"prospect": prospect.domain})

        return {
            "prospect": prospect.domain,
            "email_event": sent.to_dict(),
            "sms_event": sms_event.to_dict(),
            "booking_event": confirmed.to_dict(),
            "hiring_signal_brief_path": str(self.base_dir / "hiring_signal_brief.json"),
            "competitor_gap_brief_path": str(self.base_dir / "competitor_gap_brief.json"),
        }
