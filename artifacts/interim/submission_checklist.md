# Interim Submission Compliance Checklist

## GitHub Repo Requirements

- [x] Root `README.md` with architecture, setup, requirements.
- [x] `agent/` with source files, handlers, integration adapters, enrichment, and requirements.
- [x] `eval/` with τ²-Bench wrapper, `score_log.json`, `trace_log.jsonl`.
- [x] Root `baseline.md` with reproduced metrics and CI.

## PDF Report Requirements

- [x] Architecture and design decisions: `report/interim_report.md` section 1.
- [x] Stack verification (email, SMS, HubSpot, Cal.com, Langfuse): `report/interim_report.md` section 2.
- [x] Enrichment status: `report/interim_report.md` section 3 and `artifacts/interim/single_prospect_flow/hiring_signal_brief.json`.
- [x] Competitor gap status: `artifacts/interim/single_prospect_flow/competitor_gap_brief.json`.
- [x] τ²-Bench baseline methodology: `eval/run_tau2_wrapper.py` and `eval/score_log.json`.
- [x] p50/p95 latency on >=20 interactions: `artifacts/interim/latency_batch/latency_summary.json`.
- [x] Working/not working/next steps: `report/interim_report.md` final section.

## Evidence Attachments

- [x] HubSpot evidence artifact: `artifacts/interim/single_prospect_flow/hubspot_record_snapshot.json`.
- [x] Cal.com evidence artifact: `artifacts/interim/single_prospect_flow/cal_booking_snapshot.json`.
- [x] End-to-end event timeline: `artifacts/interim/single_prospect_flow/single_flow_summary.json`.

## Final Validation Run

- [x] `python -m eval.run_tau2_wrapper`
- [x] `python -m agent.scripts.run_single_flow`
- [x] `python -m agent.scripts.run_latency_batch`
- [x] `powershell -ExecutionPolicy Bypass -File infra/smoke_test.ps1`
- [x] `python -m compileall agent eval`
