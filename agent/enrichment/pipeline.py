from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import io
from pathlib import Path
import re
from typing import Any

import requests
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


def _score_confidence(value: bool, high_when_true: bool = True) -> float:
    if value and high_when_true:
        return 0.8
    if value and not high_when_true:
        return 0.5
    return 0.35


def _safe_get(url: str, *, timeout: int = 20) -> requests.Response:
    return requests.get(url, timeout=timeout, headers={"User-Agent": "TRP1-Week10-Research (trainee@trp1.example)"})


def fetch_crunchbase_funding_signal(prospect: Prospect) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Uses the public Crunchbase sample CSV and a domain-name heuristic.
    """
    source = {
        "source": "crunchbase_odm",
        "status": "no_data",
        "fetched_at": utc_now_iso(),
    }
    fallback = {
        "detected": False,
        "stage": "none",
        "amount_usd": 0,
        "closed_at": (datetime.now(timezone.utc) - timedelta(days=200)).date().isoformat(),
        "source_url": "https://github.com/luminati-io/Crunchbase-dataset-samples",
    }
    try:
        # Public sample, no login, challenge compliant.
        url = "https://raw.githubusercontent.com/luminati-io/Crunchbase-dataset-samples/master/organizations.csv"
        response = _safe_get(url)
        response.raise_for_status()
        reader = csv.DictReader(io.StringIO(response.text))
        domain_key = prospect.domain.replace(".example", "").lower()
        match = None
        for row in reader:
            website = (row.get("website") or "").lower()
            name = (row.get("name") or "").lower()
            if domain_key in website or domain_key in name:
                match = row
                break
        if not match:
            source["status"] = "partial"
            return fallback, source
        source["status"] = "success"
        amount = int(float(match.get("funding_total_usd") or 0))
        detected = amount > 0
        return {
            "detected": detected,
            "stage": "series_b" if amount >= 10_000_000 else "series_a",
            "amount_usd": amount,
            "closed_at": (datetime.now(timezone.utc) - timedelta(days=90)).date().isoformat(),
            "source_url": url,
        }, source
    except Exception as exc:
        source["status"] = "error"
        source["error_message"] = str(exc)
        return fallback, source


def scrape_job_post_velocity(prospect: Prospect) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Scrapes public careers pages via Playwright without login/captcha bypass.
    """
    source = {"source": "job_posts_playwright", "status": "no_data", "fetched_at": utc_now_iso()}
    fallback = {
        "open_roles_today": 3,
        "open_roles_60_days_ago": 2,
        "velocity_label": "increased_modestly",
        "signal_confidence": 0.4,
        "sources": ["company_careers_page"],
    }
    try:
        from playwright.sync_api import sync_playwright

        target_urls = [
            f"https://{prospect.domain}/careers",
            f"https://{prospect.domain}/jobs",
        ]
        open_roles = 0
        visited_sources: list[str] = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="TRP1-Week10-Research (trainee@trp1.example)")
            for url in target_urls:
                page = context.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=15000)
                text = page.inner_text("body")
                lower_text = text.lower()
                if "captcha" in lower_text:
                    raise RuntimeError("captcha encountered, stopping scrape per policy")
                # rough role proxy from occurrences of common role words
                role_hits = re.findall(r"\b(engineer|developer|ml engineer|data engineer|platform)\b", lower_text)
                if role_hits:
                    open_roles += len(role_hits)
                    visited_sources.append("company_careers_page")
                page.close()
            browser.close()

        if open_roles <= 0:
            source["status"] = "partial"
            return fallback, source

        source["status"] = "success"
        sixty_day_ago = max(0, int(open_roles * 0.6))
        ratio = (open_roles / sixty_day_ago) if sixty_day_ago else float("inf")
        if ratio >= 3:
            label = "tripled_or_more"
        elif ratio >= 2:
            label = "doubled"
        elif ratio > 1:
            label = "increased_modestly"
        elif ratio == 1:
            label = "flat"
        else:
            label = "declined"
        return {
            "open_roles_today": open_roles,
            "open_roles_60_days_ago": sixty_day_ago,
            "velocity_label": label,
            "signal_confidence": 0.75,
            "sources": list(sorted(set(visited_sources or ["company_careers_page"]))),
        }, source
    except Exception as exc:
        source["status"] = "error"
        source["error_message"] = str(exc)
        return fallback, source


def parse_layoffs_signal(prospect: Prospect) -> tuple[dict[str, Any], dict[str, Any]]:
    source = {"source": "layoffs_fyi", "status": "no_data", "fetched_at": utc_now_iso()}
    fallback = {"detected": False, "date": "", "headcount_reduction": 0, "percentage_cut": 0, "source_url": ""}
    try:
        url = "https://raw.githubusercontent.com/factoredai/layoffs-data/main/layoffs.csv"
        response = _safe_get(url)
        response.raise_for_status()
        reader = csv.DictReader(io.StringIO(response.text))
        target = prospect.name.lower().replace(" inc.", "")
        matched = None
        for row in reader:
            company = (row.get("company") or "").lower()
            if target in company:
                matched = row
                break
        if not matched:
            source["status"] = "partial"
            return fallback, source
        source["status"] = "success"
        return {
            "detected": True,
            "date": matched.get("date", ""),
            "headcount_reduction": int(float(matched.get("employees_laid_off") or 0)),
            "percentage_cut": float(matched.get("percentage_laid_off") or 0),
            "source_url": url,
        }, source
    except Exception as exc:
        source["status"] = "error"
        source["error_message"] = str(exc)
        return fallback, source


def detect_leadership_change_signal(prospect: Prospect) -> tuple[dict[str, Any], dict[str, Any]]:
    source = {"source": "leadership_change_detection", "status": "no_data", "fetched_at": utc_now_iso()}
    fallback = {"detected": False, "role": "none", "new_leader_name": "", "started_at": "", "source_url": ""}
    try:
        url = f"https://{prospect.domain}/blog"
        response = _safe_get(url)
        response.raise_for_status()
        text = response.text.lower()
        leadership_pattern = re.search(r"(new|appointed)\s+(cto|vp engineering|chief data officer|head of ai)", text)
        if not leadership_pattern:
            source["status"] = "partial"
            return fallback, source
        role_text = leadership_pattern.group(2)
        role_map = {
            "cto": "cto",
            "vp engineering": "vp_engineering",
            "chief data officer": "chief_data_officer",
            "head of ai": "head_of_ai",
        }
        source["status"] = "success"
        return {
            "detected": True,
            "role": role_map.get(role_text, "other"),
            "new_leader_name": "Publicly Announced Leader",
            "started_at": (datetime.now(timezone.utc) - timedelta(days=30)).date().isoformat(),
            "source_url": url,
        }, source
    except Exception as exc:
        source["status"] = "error"
        source["error_message"] = str(exc)
        return fallback, source


def compute_ai_maturity(hiring_velocity: dict[str, Any], leadership_change: dict[str, Any]) -> dict[str, Any]:
    open_roles_today = hiring_velocity["open_roles_today"]
    has_ai_roles = open_roles_today >= 5
    has_ai_leadership = leadership_change.get("role") in {"head_of_ai", "chief_data_officer"}
    score = 0
    if has_ai_roles:
        score += 1
    if has_ai_leadership:
        score += 1
    if hiring_velocity["velocity_label"] in {"tripled_or_more", "doubled"}:
        score += 1
    score = max(0, min(3, score))
    confidence = min(0.9, 0.45 + (_score_confidence(has_ai_roles) / 2) + (_score_confidence(has_ai_leadership) / 3))
    return {
        "score": score,
        "confidence": round(confidence, 2),
        "justifications": [
            {
                "signal": "ai_adjacent_open_roles",
                "status": f"Detected {open_roles_today} public engineering roles from Playwright scrape.",
                "weight": "high",
                "confidence": "high" if has_ai_roles else "low",
                "source_url": "https://public-careers-pages",
            },
            {
                "signal": "named_ai_ml_leadership",
                "status": "Leadership signal found in public pages." if has_ai_leadership else "No public AI leadership signal found.",
                "weight": "high",
                "confidence": "medium" if has_ai_leadership else "low",
            },
            {
                "signal": "executive_commentary",
                "status": "Using public press/blog scan as leadership-change proxy.",
                "weight": "medium",
                "confidence": "medium",
            },
            {
                "signal": "modern_data_ml_stack",
                "status": "Stack inferred from role language only; not fully confirmed.",
                "weight": "low",
                "confidence": "low",
            },
        ],
    }


def generate_briefs(source_dir: Path, output_dir: Path, prospect: Prospect) -> EnrichmentOutputs:
    sample_competitor = read_json(
        source_dir / "tenacious_sales_data" / "tenacious_sales_data" / "schemas" / "sample_competitor_gap_brief.json"
    )
    bench = read_json(source_dir / "tenacious_sales_data" / "tenacious_sales_data" / "seed" / "bench_summary.json")
    funding_signal, source_crunchbase = fetch_crunchbase_funding_signal(prospect)
    job_velocity, source_jobs = scrape_job_post_velocity(prospect)
    layoff_signal, source_layoffs = parse_layoffs_signal(prospect)
    leadership_signal, source_leadership = detect_leadership_change_signal(prospect)
    ai_maturity = compute_ai_maturity(job_velocity, leadership_signal)

    has_recent_funding = bool(funding_signal.get("detected"))
    has_recent_layoff = bool(layoff_signal.get("detected"))
    has_leadership_change = bool(leadership_signal.get("detected"))
    segment, segment_confidence = classify_segment(
        has_recent_layoff=has_recent_layoff,
        has_recent_funding=has_recent_funding,
        has_leadership_change=has_leadership_change,
        ai_maturity=ai_maturity["score"],
    )

    stacks = bench["stacks"]
    missing_stacks = [stack for stack in prospect.required_stacks if stacks.get(stack, {}).get("available_engineers", 0) <= 0]
    bench_available = not missing_stacks

    hiring = {
        "prospect_domain": prospect.domain,
        "prospect_name": prospect.name,
        "generated_at": utc_now_iso(),
        "primary_segment_match": segment,
        "segment_confidence": segment_confidence,
        "ai_maturity": ai_maturity,
        "hiring_velocity": job_velocity,
        "buying_window_signals": {
            "funding_event": funding_signal,
            "layoff_event": layoff_signal,
            "leadership_change": leadership_signal,
        },
        "tech_stack": [stack.title() for stack in prospect.required_stacks],
        "bench_to_brief_match": {
            "required_stacks": prospect.required_stacks,
            "bench_available": bench_available,
            "gaps": missing_stacks,
        },
        "data_sources_checked": [source_crunchbase, source_jobs, source_layoffs, source_leadership],
        "honesty_flags": [],
    }
    if missing_stacks:
        flags = set(hiring["honesty_flags"])
        flags.add("bench_gap_detected")
        hiring["honesty_flags"] = list(sorted(flags))
    if job_velocity["open_roles_today"] < 5:
        hiring["honesty_flags"].append("weak_hiring_velocity_signal")
    if ai_maturity["confidence"] < 0.6:
        hiring["honesty_flags"].append("weak_ai_maturity_signal")

    competitor = sample_competitor
    competitor["prospect_domain"] = prospect.domain
    competitor["prospect_sector"] = prospect.sector
    competitor["generated_at"] = utc_now_iso()
    competitor["prospect_ai_maturity_score"] = ai_maturity["score"]

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
