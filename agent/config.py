from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    root_dir: Path
    source_dir: Path
    artifacts_dir: Path
    interim_artifacts_dir: Path
    outbound_enabled: bool
    outbound_sink_email: str
    outbound_sink_sms: str
    email_provider: str
    email_from: str


def _as_bool(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def load_settings() -> Settings:
    root_dir = Path(__file__).resolve().parent.parent
    source_dir = root_dir / "source_file"
    artifacts_dir = root_dir / "artifacts"
    interim_artifacts_dir = artifacts_dir / "interim"
    interim_artifacts_dir.mkdir(parents=True, exist_ok=True)

    return Settings(
        root_dir=root_dir,
        source_dir=source_dir,
        artifacts_dir=artifacts_dir,
        interim_artifacts_dir=interim_artifacts_dir,
        outbound_enabled=_as_bool(os.getenv("TENACIOUS_OUTBOUND_ENABLED")),
        outbound_sink_email=os.getenv("TENACIOUS_OUTBOUND_SINK_EMAIL", "staff-sink@trp1.example"),
        outbound_sink_sms=os.getenv("TENACIOUS_OUTBOUND_SINK_SMS", "+251700000000"),
        email_provider=os.getenv("EMAIL_PROVIDER", "resend"),
        email_from=os.getenv("EMAIL_FROM", "research-partner@gettenacious.com"),
    )
