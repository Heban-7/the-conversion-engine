from __future__ import annotations

from agent.policy import build_tone_scorecard


def compose_cold_email(*, first_name: str, company: str, lead_signal: str, ask: str) -> tuple[str, dict[str, int]]:
    body = (
        f"{first_name}, your team at {company} shows clear public signal for AI-related hiring. "
        f"{lead_signal} "
        f"{ask}"
    )
    # Keep the body under 120 words to respect style guide constraints.
    words = body.split()
    if len(words) > 120:
        body = " ".join(words[:120])
    return body, build_tone_scorecard()


def compose_sms_for_scheduling(*, first_name: str, booking_link: str) -> str:
    return f"{first_name}, sharing the booking link for the 15-minute discovery call: {booking_link}"
