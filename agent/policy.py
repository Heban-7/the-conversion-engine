from __future__ import annotations

from dataclasses import dataclass

from agent.config import Settings


TONE_MARKERS = ("direct", "grounded", "honest", "professional", "non_condescending")


@dataclass(frozen=True)
class GuardrailResult:
    allowed: bool
    reasons: list[str]


def enforce_kill_switch(settings: Settings, destination: str) -> str:
    if settings.outbound_enabled:
        return destination
    return settings.outbound_sink_email if "@" in destination else settings.outbound_sink_sms


def evaluate_honesty_guards(
    *,
    open_roles_today: int,
    bench_available: bool,
    gap_confidences: list[str],
) -> GuardrailResult:
    reasons: list[str] = []
    if open_roles_today < 5:
        reasons.append("weak_hiring_velocity_signal")
    if not bench_available:
        reasons.append("bench_gap_detected")
    if not any(conf == "high" for conf in gap_confidences):
        reasons.append("no_high_confidence_gap")
    return GuardrailResult(allowed=not reasons, reasons=reasons)


def build_tone_scorecard() -> dict[str, int]:
    # Placeholder deterministic scorecard for interim traceability.
    return {marker: 4 for marker in TONE_MARKERS}
