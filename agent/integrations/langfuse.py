from __future__ import annotations

from pathlib import Path
from typing import Any

from agent.io_utils import append_jsonl
from agent.types import utc_now_iso


class LangfuseClient:
    def __init__(self, trace_log_path: Path) -> None:
        self.trace_log_path = trace_log_path

    def trace(self, name: str, correlation_id: str, metadata: dict[str, Any]) -> None:
        append_jsonl(
            self.trace_log_path,
            {
                "trace_name": name,
                "correlation_id": correlation_id,
                "timestamp": utc_now_iso(),
                "metadata": metadata,
            },
        )
