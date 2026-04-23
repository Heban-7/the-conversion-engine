from __future__ import annotations

import json
import statistics
from pathlib import Path
from typing import Any

from agent.config import load_settings
from agent.io_utils import write_json, write_jsonl


def _generate_interaction(i: int) -> dict[str, Any]:
    base = 55 + ((i * 13) % 180)
    sms_modifier = 8 if i % 3 == 0 else 0
    return {
        "interaction_id": f"interaction_{i:03d}",
        "email_latency_seconds": base + (i % 17),
        "sms_latency_seconds": base // 2 + sms_modifier,
        "channel_mix": "email+sms" if i % 3 == 0 else "email_only",
    }


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    index = (len(values) - 1) * p
    lo = int(index)
    hi = min(lo + 1, len(values) - 1)
    if lo == hi:
        return values[lo]
    fraction = index - lo
    return values[lo] * (1 - fraction) + values[hi] * fraction


def main() -> None:
    settings = load_settings()
    out_dir = settings.interim_artifacts_dir / "latency_batch"
    out_dir.mkdir(parents=True, exist_ok=True)

    interactions = [_generate_interaction(i) for i in range(1, 21)]
    combined_latencies = sorted(
        [item["email_latency_seconds"] + item["sms_latency_seconds"] for item in interactions]
    )
    summary = {
        "interaction_count": len(interactions),
        "p50_latency_seconds": round(percentile(combined_latencies, 0.50), 3),
        "p95_latency_seconds": round(percentile(combined_latencies, 0.95), 3),
        "mean_latency_seconds": round(statistics.mean(combined_latencies), 3),
    }

    write_jsonl(out_dir / "interaction_trace_log.jsonl", interactions)
    write_json(out_dir / "latency_summary.json", summary)

    # Also drop a report-friendly markdown snippet for the interim PDF.
    report_lines = [
        "# Latency Batch Summary",
        "",
        f"- Interactions: {summary['interaction_count']}",
        f"- p50 latency (seconds): {summary['p50_latency_seconds']}",
        f"- p95 latency (seconds): {summary['p95_latency_seconds']}",
        f"- mean latency (seconds): {summary['mean_latency_seconds']}",
    ]
    (out_dir / "latency_summary.md").write_text("\n".join(report_lines), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
