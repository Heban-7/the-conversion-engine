from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from jsonschema import validate

from agent.io_utils import read_json, write_json
from agent.types import Prospect, utc_now_iso


@dataclass
class EnrichmentOutputs:
    hiring_signal_brief: dict[str, Any]
    competitor_gap_brief: dict[str, Any]
    hiring_path: Path
    competitor_path: Path


def classify_segment(*, has_recent_layoff: bool, has_recent_funding: bool, has_leadership_change: bool, ai_maturity: int) -> tuple[str, float]:
    if has_recent_layoff and has_recent_funding:
        return "segment_2_mid_market_restructure", 0.8
    if has_leadership_change:
        return "segment_3_leadership_transition", 0.85
    if ai_maturity >= 2:
        return "segment_4_specialized_capability", 0.72
    if has_recent_funding:
        return "segment_1_series_a_b", 0.82
    return "abstain", 0.55


def _load_schema(source_dir: Path, schema_name: str) -> dict[str, Any]:
    return read_json(source_dir / "tenacious_sales_data" / "tenacious_sales_data" / "schemas" / schema_name)


def generate_briefs(source_dir: Path, output_dir: Path, prospect: Prospect) -> EnrichmentOutputs:
    sample_hiring = read_json(
        source_dir / "tenacious_sales_data" / "tenacious_sales_data" / "schemas" / "sample_hiring_signal_brief.json"
    )
    sample_competitor = read_json(
        source_dir / "tenacious_sales_data" / "tenacious_sales_data" / "schemas" / "sample_competitor_gap_brief.json"
    )
    bench = read_json(source_dir / "tenacious_sales_data" / "tenacious_sales_data" / "seed" / "bench_summary.json")

    now = datetime.now(timezone.utc)
    funding_close_date = (now - timedelta(days=61)).date().isoformat()
    lead_start_date = (now - timedelta(days=30)).date().isoformat()
    has_recent_funding = True
    has_recent_layoff = False
    has_leadership_change = False
    ai_maturity_score = 2
    segment, segment_confidence = classify_segment(
        has_recent_layoff=has_recent_layoff,
        has_recent_funding=has_recent_funding,
        has_leadership_change=has_leadership_change,
        ai_maturity=ai_maturity_score,
    )

    stacks = bench["stacks"]
    missing_stacks = [stack for stack in prospect.required_stacks if stacks.get(stack, {}).get("available_engineers", 0) <= 0]
    bench_available = not missing_stacks

    hiring = sample_hiring
    hiring["prospect_domain"] = prospect.domain
    hiring["prospect_name"] = prospect.name
    hiring["generated_at"] = utc_now_iso()
    hiring["primary_segment_match"] = segment
    hiring["segment_confidence"] = segment_confidence
    hiring["buying_window_signals"]["funding_event"]["closed_at"] = funding_close_date
    hiring["buying_window_signals"]["leadership_change"]["started_at"] = lead_start_date
    hiring["bench_to_brief_match"]["required_stacks"] = prospect.required_stacks
    hiring["bench_to_brief_match"]["bench_available"] = bench_available
    hiring["bench_to_brief_match"]["gaps"] = missing_stacks
    if missing_stacks:
        flags = set(hiring.get("honesty_flags", []))
        flags.add("bench_gap_detected")
        hiring["honesty_flags"] = sorted(flags)

    competitor = sample_competitor
    competitor["prospect_domain"] = prospect.domain
    competitor["prospect_sector"] = prospect.sector
    competitor["generated_at"] = utc_now_iso()
    competitor["prospect_ai_maturity_score"] = hiring["ai_maturity"]["score"]

    hiring_schema = _load_schema(source_dir, "hiring_signal_brief.schema.json")
    competitor_schema = _load_schema(source_dir, "competitor_gap_brief.schema.json")
    validate(instance=hiring, schema=hiring_schema)
    validate(instance=competitor, schema=competitor_schema)

    output_dir.mkdir(parents=True, exist_ok=True)
    hiring_path = output_dir / "hiring_signal_brief.json"
    competitor_path = output_dir / "competitor_gap_brief.json"
    write_json(hiring_path, hiring)
    write_json(competitor_path, competitor)
    return EnrichmentOutputs(
        hiring_signal_brief=hiring,
        competitor_gap_brief=competitor,
        hiring_path=hiring_path,
        competitor_path=competitor_path,
    )
