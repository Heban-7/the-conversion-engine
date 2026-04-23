from __future__ import annotations

import json
import math
from pathlib import Path

from agent.io_utils import read_json, write_json, write_jsonl


def wilson_interval(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = successes / n
    denom = 1 + (z**2 / n)
    center = (p + (z**2 / (2 * n))) / denom
    margin = (z * math.sqrt((p * (1 - p) / n) + (z**2 / (4 * n**2)))) / denom
    return (center - margin, center + margin)


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    source_dir = repo_root / "source_file"
    score_source = source_dir / "score_log.json"
    trace_source = source_dir / "trace_log.jsonl"

    if not score_source.exists() or not trace_source.exists():
        raise FileNotFoundError("Missing source_file/score_log.json or source_file/trace_log.jsonl")

    score_payload = read_json(score_source)
    trace_lines = [json.loads(line) for line in trace_source.read_text(encoding="utf-8").splitlines() if line.strip()]

    successes = sum(1 for line in trace_lines if float(line.get("reward", 0.0)) >= 1.0)
    total = len(trace_lines)
    ci_low, ci_high = wilson_interval(successes, total)

    computed = {
        "domain": score_payload.get("domain", "retail"),
        "source": "source_file/trace_log.jsonl",
        "evaluated_simulations": total,
        "pass_at_1_empirical": round(successes / total if total else 0.0, 4),
        "pass_at_1_ci_95_empirical": [round(ci_low, 4), round(ci_high, 4)],
        "avg_agent_cost": round(sum(float(line["agent_cost"]) for line in trace_lines) / total, 4) if total else 0.0,
        "p50_latency_seconds": score_payload.get("p50_latency_seconds", 0),
        "p95_latency_seconds": score_payload.get("p95_latency_seconds", 0),
        "num_trials": score_payload.get("num_trials", 0),
        "total_tasks": score_payload.get("total_tasks", 0),
        "git_commit": score_payload.get("git_commit", "unknown"),
    }

    eval_dir = repo_root / "eval"
    write_json(eval_dir / "score_log.json", computed)
    write_jsonl(eval_dir / "trace_log.jsonl", trace_lines)

    run_meta = {
        "runner": "eval/run_tau2_wrapper.py",
        "note": "Interim wrapper copies source benchmark artifacts and recomputes CI from raw traces.",
    }
    write_json(eval_dir / "run_metadata.json", run_meta)
    print(json.dumps(computed, indent=2))


if __name__ == "__main__":
    main()
