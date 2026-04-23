from __future__ import annotations

from pathlib import Path

from agent.io_utils import append_jsonl, write_json
from agent.types import InteractionEvent, utc_now_iso


class CalComClient:
    def __init__(self, events_log: Path, booking_snapshot_path: Path) -> None:
        self.events_log = events_log
        self.booking_snapshot_path = booking_snapshot_path

    def create_booking_link(self, prospect_domain: str) -> tuple[str, InteractionEvent]:
        link = f"https://cal.example/{prospect_domain}/discovery-call"
        event = InteractionEvent.build(
            channel="calcom",
            event_type="booking_link_generated",
            payload={"booking_link": link},
        )
        append_jsonl(self.events_log, {"event": event.to_dict(), "created_at": utc_now_iso()})
        return link, event

    def confirm_booking(self, booking_link: str, timeslot_utc: str) -> InteractionEvent:
        event = InteractionEvent.build(
            channel="calcom",
            event_type="booking_confirmed",
            payload={"booking_link": booking_link, "timeslot_utc": timeslot_utc},
        )
        snapshot = {
            "captured_at": utc_now_iso(),
            "booking_link": booking_link,
            "timeslot_utc": timeslot_utc,
            "status": "confirmed",
        }
        append_jsonl(self.events_log, {"event": event.to_dict(), "created_at": utc_now_iso()})
        write_json(self.booking_snapshot_path, snapshot)
        return event
