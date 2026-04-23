from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from agent.composer import compose_cold_email, compose_sms_for_scheduling
from agent.config import Settings
from agent.enrichment.pipeline import EnrichmentOutputs, generate_briefs
from agent.integrations.calcom import CalComClient
from agent.integrations.email import EmailClient, EmailMessage
from agent.integrations.hubspot import HubSpotClient
from agent.integrations.langfuse import LangfuseClient
from agent.integrations.sms import SmsClient
from agent.io_utils import write_json
from agent.policy import evaluate_honesty_guards
from agent.types import InteractionEvent, Prospect


def _build_hubspot_contact(prospect: Prospect, enrichment: EnrichmentOutputs) -> dict[str, Any]:
    return {
        "email": prospect.contact_email,
        "firstname": prospect.contact_first_name,
        "company": prospect.name,
        "domain": prospect.domain,
        "segment": enrichment.hiring_signal_brief["primary_segment_match"],
        "segment_confidence": enrichment.hiring_signal_brief["segment_confidence"],
        "ai_maturity_score": enrichment.hiring_signal_brief["ai_maturity"]["score"],
        "tenacious_status": "draft",
        "enrichment_generated_at": enrichment.hiring_signal_brief["generated_at"],
    }


def run_single_prospect_flow(settings: Settings, prospect: Prospect, output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    logs_dir = output_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    email = EmailClient(settings, logs_dir / "email_events.jsonl")
    sms = SmsClient(settings, logs_dir / "sms_events.jsonl")
    hubspot = HubSpotClient(logs_dir / "hubspot_events.jsonl", output_dir / "hubspot_record_snapshot.json")
    calcom = CalComClient(logs_dir / "calcom_events.jsonl", output_dir / "cal_booking_snapshot.json")
    langfuse = LangfuseClient(logs_dir / "langfuse_traces.jsonl")

    enrichment = generate_briefs(settings.source_dir, output_dir, prospect)
    guardrails = evaluate_honesty_guards(
        open_roles_today=enrichment.hiring_signal_brief["hiring_velocity"]["open_roles_today"],
        bench_available=enrichment.hiring_signal_brief["bench_to_brief_match"]["bench_available"],
        gap_confidences=[entry["confidence"] for entry in enrichment.competitor_gap_brief["gap_findings"]],
    )

    lead_signal = (
        "Your hiring velocity rose from "
        f"{enrichment.hiring_signal_brief['hiring_velocity']['open_roles_60_days_ago']} to "
        f"{enrichment.hiring_signal_brief['hiring_velocity']['open_roles_today']} open engineering roles in 60 days."
    )
    ask = "Open to a 15-minute discovery call on where dedicated support can unblock hiring velocity?"
    email_body, tone_scorecard = compose_cold_email(
        first_name=prospect.contact_first_name,
        company=prospect.name,
        lead_signal=lead_signal,
        ask=ask,
    )

    subject = "Request: 15-minute AI delivery context call"
    sent_email = email.send(
        EmailMessage(
            to=prospect.contact_email,
            subject=subject,
            body=email_body,
            headers={"X-Tenacious-Status": "draft"},
        )
    )
    langfuse.trace("email_outbound", sent_email.correlation_id, {"subject": subject, "guardrails": guardrails.reasons})

    hubspot.upsert_contact(_build_hubspot_contact(prospect, enrichment))
    hubspot.append_event(sent_email.correlation_id, "email_sent", {"subject": subject})

    reply = email.simulate_reply(prospect.contact_email, "Thanks. Email is good, but SMS for scheduling is faster.")
    langfuse.trace("email_reply", reply.correlation_id, {"intent": "wants_sms_scheduling"})
    hubspot.append_event(reply.correlation_id, "email_reply_received", {"channel_preference": "sms"})

    booking_link, booking_link_event = calcom.create_booking_link(prospect.domain)
    hubspot.append_event(booking_link_event.correlation_id, "booking_link_generated", {"booking_link": booking_link})

    sms_text = compose_sms_for_scheduling(first_name=prospect.contact_first_name, booking_link=booking_link)
    sms_event = sms.send(prospect.contact_phone, sms_text)
    langfuse.trace("sms_outbound", sms_event.correlation_id, {"message_preview": sms_text[:60]})
    hubspot.append_event(sms_event.correlation_id, "sms_sent", {"booking_link": booking_link})

    confirmed = calcom.confirm_booking(
        booking_link=booking_link,
        timeslot_utc=(datetime.now(timezone.utc) + timedelta(days=3)).replace(microsecond=0).isoformat(),
    )
    langfuse.trace("cal_booking_confirmed", confirmed.correlation_id, {"booking_link": booking_link})
    hubspot.append_event(confirmed.correlation_id, "booking_confirmed", {"timeslot_utc": confirmed.payload["timeslot_utc"]})

    flow_summary = {
        "prospect": asdict(prospect),
        "guardrail_allowed_without_flags": guardrails.allowed,
        "guardrail_reasons": guardrails.reasons,
        "tone_scorecard": tone_scorecard,
        "events": [
            sent_email.to_dict(),
            reply.to_dict(),
            booking_link_event.to_dict(),
            sms_event.to_dict(),
            confirmed.to_dict(),
        ],
        "artifacts": {
            "hiring_signal_brief": str(enrichment.hiring_path),
            "competitor_gap_brief": str(enrichment.competitor_path),
            "hubspot_snapshot": str(output_dir / "hubspot_record_snapshot.json"),
            "cal_snapshot": str(output_dir / "cal_booking_snapshot.json"),
        },
    }
    write_json(output_dir / "single_flow_summary.json", flow_summary)
    return flow_summary


def build_default_prospect() -> Prospect:
    return Prospect(
        domain="orrin-labs.example",
        name="Orrin Labs Inc.",
        contact_first_name="Jordan",
        contact_email="jordan@orrin-labs.example",
        contact_phone="+251711000111",
        sector="Business Intelligence / Analytics",
        required_stacks=["python", "data"],
    )
