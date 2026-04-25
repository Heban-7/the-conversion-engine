# Full Project Guide (Beginner-Friendly)

This guide explains the complete story of this project from setup to final submission, assuming you are new to the codebase.

---

## 0) What This Project Is

You are building an automated conversion engine for Tenacious:

1. find and enrich synthetic prospects,
2. generate grounded outreach (email first),
3. handle warm-lead scheduling over SMS,
4. book calls through Cal.com,
5. track events in HubSpot + Langfuse,
6. evaluate quality with tau2-bench and probe suites,
7. produce evidence-backed reports for interim and final submissions.

Channel hierarchy enforced by spec:
- **Email = primary**
- **SMS = secondary (warm leads only)**
- **Voice = optional bonus**

---

## 1) Repository Map

- `agent/` -> all app logic (orchestration, integrations, enrichment, webhooks)
- `eval/` -> evaluation scripts and generated benchmark artifacts
- `infra/` -> kill-switch and smoke checks
- `artifacts/interim/` -> interim execution evidence
- `probes/` -> final probe package (Act III)
- `method.md` -> mechanism write-up (Act IV)
- `ablation_results.json`, `held_out_traces.jsonl` -> final eval package (currently placeholder mode)
- `evidence_graph.json`, `invoice_summary.json` -> claim/evidence + cost mapping
- `report/` -> interim and final memo draft markdown files
- `source_file/` -> provided seed docs, schemas, baseline/source data

---

## 2) Prerequisites

- Python 3.11+
- pip
- (for live enrichment scrape) Playwright browser install
- Provider credentials:
  - Resend or MailerSend
  - Africa's Talking
  - HubSpot developer sandbox
  - Cal.com
  - Langfuse

---

## 3) Initial Setup

1. Install dependencies:

```bash
python -m pip install -r agent/requirements.txt
```

2. Copy env file:

```bash
copy .env.example .env
```

3. Fill required keys in `.env`.

4. Keep `TENACIOUS_OUTBOUND_ENABLED` **unset** while testing sink-safe mode.

5. Run smoke test:

```powershell
powershell -ExecutionPolicy Bypass -File infra/smoke_test.ps1
```

---

## 4) Implementation Flow (End-to-End Story)

### Step A: Baseline Evaluation (Act I)

Run:

```bash
python -m eval.run_tau2_wrapper
```

This creates:
- `eval/score_log.json`
- `eval/trace_log.jsonl`
- `eval/run_metadata.json`

Use `baseline.md` as the narrative summary for reproduction, CI, cost, and latency.

### Step B: Production Stack Flow (Act II)

Run a single synthetic conversation:

```bash
python -m agent.scripts.run_single_flow
```

Run interaction latency batch:

```bash
python -m agent.scripts.run_latency_batch
```

Start inbound webhooks:

```bash
uvicorn agent.webhooks:app --host 0.0.0.0 --port 8000
```

What happens in the flow:
1. enrichment builds `hiring_signal_brief.json` and `competitor_gap_brief.json`,
2. composer creates cold email,
3. email handler sends through selected provider,
4. inbound reply marks engagement state,
5. SMS send allowed only if prior email engagement exists,
6. Cal booking link generated and confirmation captured,
7. HubSpot/Langfuse adapters log state transitions.

### Step C: Probe and Failure Work (Act III)

Files:
- `probes/probe_library.md`
- `probes/failure_taxonomy.md`
- `probes/target_failure_mode.md`

Use probes to identify the highest-cost failure mode and tie it to business cost.

### Step D: Method and Ablation (Act IV)

Current implementation includes placeholder-mode final artifacts:

```bash
python -m eval.generate_final_eval_artifacts
```

Generates:
- `ablation_results.json`
- `held_out_traces.jsonl`
- `eval/final_eval_metadata.json`

Then read:
- `method.md`

Important: before final lock, rerun these on real sealed held-out data and replace placeholder values.

### Step E: Final Memo and Evidence (Act V)

Use:
- `report/memo_final_pdf_ready.md` (content source for 2-page memo)
- `evidence_graph.json` (claim mapping)
- `invoice_summary.json` (cost source)

Export final memo as `memo.pdf` (exactly 2 pages).

---

## 5) Live Execution Mode vs Placeholder Mode

### Placeholder Mode (currently supported now)

- Uses generated/simulated final eval package for structure completion.
- Good for code completion and document assembly.

### Live Execution Mode (your selected target)

To fully complete final submission quality:

1. provide real provider credentials in `.env`,
2. run real outreach and webhook flow against sandbox endpoints,
3. run sealed held-out evaluation for day1/auto-opt/our_method,
4. replace placeholder fields in:
   - `ablation_results.json`
   - `held_out_traces.jsonl`
   - `invoice_summary.json`
   - `evidence_graph.json`
   - `report/memo_final_pdf_ready.md`

---

## 6) Final Submission Checklist (Practical)

### Repo Files

- [ ] `probes/probe_library.md` (30+ entries)
- [ ] `probes/failure_taxonomy.md`
- [ ] `probes/target_failure_mode.md`
- [ ] `method.md`
- [ ] `ablation_results.json` (real held-out)
- [ ] `held_out_traces.jsonl` (real held-out)
- [ ] `evidence_graph.json`
- [ ] `invoice_summary.json`
- [ ] `README.md` (handover-ready)

### Report/Media

- [ ] `memo.pdf` exactly 2 pages
- [ ] interim and final evidence screenshots/traces packaged
- [ ] demo video (<=8 min, public, no login)

---

## 7) Common Troubleshooting

- **Email send failed** -> verify `EMAIL_PROVIDER` and provider API key.
- **SMS blocked** -> expected if no prior email engagement; this is warm-channel policy.
- **Webhook rejected** -> check webhook secret header matches `.env`.
- **Enrichment source errors** -> inspect `data_sources_checked` in hiring brief.
- **Playwright import error** -> install dependency and browser runtime.

---

## 8) What To Do Next (Recommended Order)

1. Switch to live credential mode and verify each integration.
2. Replace placeholder final eval with sealed held-out runs.
3. Recompute evidence graph with final numeric claims.
4. Export strict 2-page `memo.pdf`.
5. Record demo video using the checklist in spec.

---

## 9) Quick Command Reference

```bash
# Baseline
python -m eval.run_tau2_wrapper

# Single end-to-end run
python -m agent.scripts.run_single_flow

# Latency batch
python -m agent.scripts.run_latency_batch

# Final placeholder ablation package
python -m eval.generate_final_eval_artifacts

# Webhooks
uvicorn agent.webhooks:app --host 0.0.0.0 --port 8000
```

---

If you follow this guide in order, you can move from setup to a complete final-submission package with clear evidence linkage and repeatable execution steps.
