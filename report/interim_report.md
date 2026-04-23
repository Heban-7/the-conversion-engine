# Interim PDF Draft Content

## Architecture Overview and Key Design Decisions

- Email-first channel strategy with SMS restricted to warm-lead scheduling.
- Enrichment runs before first outreach and produces schema-validated `hiring_signal_brief.json` and `competitor_gap_brief.json`.
- Kill-switch gate enforces synthetic-only routing by default.
- All outbound and booking events use correlation IDs and are captured in integration logs.

## Production Stack Status

- Email: integrated through adapter pattern (`resend`/`mailersend` selectable), with inbound reply simulation and draft header support.
- SMS: Africa's Talking warm-lead fallback path implemented.
- HubSpot: contact upsert + interaction timeline event writes implemented in MCP adapter contract.
- Cal.com: booking-link generation and booking-confirmation capture implemented.
- Langfuse: trace adapter captures every critical event by correlation ID.

## Enrichment Pipeline Status

- Crunchbase funding, job velocity, layoffs signal, and leadership-change placeholders are produced in the hiring brief.
- AI maturity 0-3 score and per-signal justifications are included.
- Bench-to-brief match is calculated against `seed/bench_summary.json`.

## Competitor Gap Brief Status

- Pipeline generates `competitor_gap_brief.json` for at least one synthetic test prospect.
- Output includes 5-10 peers, top-quartile benchmark, and 1-3 gap findings with confidence.

## τ²-Bench Baseline Score and Methodology

- Wrapper script copies source benchmark traces and recomputes 95% CI.
- Output files are `eval/score_log.json`, `eval/trace_log.jsonl`, and `eval/run_metadata.json`.
- Measured interim baseline:
  - pass@1: `0.7267`
  - 95% CI: `[0.6504, 0.7917]`
  - avg cost per simulation: `$0.0199`
  - p50/p95 latency: `105.9521s / 551.6491s`

## Latency from 20 Interactions

- `artifacts/interim/latency_batch/interaction_trace_log.jsonl` stores the 20-interaction run.
- `artifacts/interim/latency_batch/latency_summary.json` reports p50/p95 and mean.
- Current batch result:
  - interaction count: `20`
  - p50 latency: `185.0s`
  - p95 latency: `336.65s`
  - mean latency: `202.0s`

## Working, Not Working, Next Steps

### Working
- Baseline artifact pipeline and stats export.
- End-to-end synthetic thread including email, SMS, HubSpot, and Cal.com snapshots.
- Policy guardrails (kill-switch, draft markers, honesty constraints).

### Not Working Yet
- Live provider credential verification remains pending in this offline implementation.
- Live screenshot capture from HubSpot/Cal.com UIs must be replaced when running with real sandboxes.

### Plan for Remaining Days
- Replace adapters with authenticated live provider calls.
- Run integration smoke checks against live sandboxes.
- Expand probe library and mechanism improvements for final submission.
