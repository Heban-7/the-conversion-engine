# memo.pdf (Final Draft Content, 2-Page Layout)

> This markdown is formatted for export to `memo.pdf` with exact two-page layout in the final render tool.
> Current numeric values marked as placeholder must be replaced after sealed held-out execution.

---

## Page 1: The Decision

### Executive Summary (3 sentences)

We built a production-oriented conversion engine for Tenacious that runs email-first outreach, confidence-aware enrichment, warm-lead SMS scheduling, and booking orchestration with CRM/trace capture. On current artifacts, the system shows stronger controlled behavior on over-claiming and a placeholder Delta A improvement over Day-1 baseline in simulated held-out mode. Recommendation: proceed with a tightly scoped pilot on one segment, one outbound volume target, and one success metric, while finalizing sealed held-out evidence and live-provider verification.

### tau2-bench Results (with 95% CIs)

- Published reference (retail ceiling context): ~42% conversational pass@1 (public benchmark reference).
- Day-1 baseline: pass@1 `0.7267`, 95% CI `[0.6504, 0.7917]` (source: `eval/score_log.json`).
- Our method (placeholder held-out mode): pass@1 `1.00`, 95% CI `[0.8389, 1.0000]` (source: `ablation_results.json`).

### Cost per Qualified Lead

Placeholder formula (replace with real final values):

- Total spend = `$5.34` from `invoice_summary.json`
- Qualified leads in trace window = `N` (to be finalized from held-out + interaction trace tags)
- Cost per qualified lead = `total_spend / qualified_leads`

### Speed-to-Lead Delta (Stalled-Thread Framing)

- Manual baseline (Tenacious stated): `30-40%` stalled-thread risk.
- System status: interaction pipeline executes end-to-end with warm-channel SMS gating and booking completion.
- Next final calculation: compute stalled-thread rate from tagged traces in `held_out_traces.jsonl` + interaction logs.

### Competitive-Gap Outbound Performance

- Variant tracking framework established:
  - `research_led` (AI maturity + competitor gap)
  - `generic_pitch`
- Final calculation required for memo lock:
  - fraction of outbound by variant
  - reply-rate delta between variants

### Annualized Dollar Impact (Three Scenarios)

Scenarios to compute from final traces + seed ACV/conversion ranges:

1. One segment only
2. Two segments
3. All four segments

Each scenario must include:
- lead volume
- conversion cascade assumptions
- ACV range application
- annualized expected value with confidence bounds

### Pilot Scope Recommendation (30-Day)

- Segment: start with Segment 2 (cost restructuring) for high signal clarity.
- Lead volume: 40 qualified leads/month (initial).
- Budget: capped weekly spend linked to cost-per-qualified-lead threshold.
- Success criterion: measurable reduction in stalled-thread rate with no over-claim policy breaches.

---

## Page 2: The Skeptic's Appendix

### Four Tenacious-Specific Failure Modes tau2-Bench Misses

1. **Offshore-perception objection under executive pressure**  
   Why missed: benchmark does not model reputational or geopolitical sensitivity.  
   Added control: tone-risk probes + human escalation trigger.

2. **Bench mismatch after positive thread**  
   Why missed: benchmark does not include real-time internal staffing constraints.  
   Added control: hard bench gate + phased-ramp handoff policy.

3. **Wrong-signal brand damage at scale**  
   Why missed: benchmark rewards task completion, not external trust erosion.  
   Added control: confidence-to-language lock and contradiction blocker.

4. **Cross-thread leakage for same account stakeholders**  
   Why missed: benchmark usually scores single-thread trajectories.  
   Added control: strict thread-scoped state + correlation-id isolation checks.

### Public-Signal Lossiness (AI Maturity)

- False-negative pattern: quietly sophisticated companies with minimal public AI signal.
- False-positive pattern: highly public AI messaging with shallow implementation depth.
- Operational mitigation:
  - medium/low confidence => question framing only
  - no hard capability claims without corroborated evidence

### Gap-Analysis Risks

- Top-quartile practice may be intentionally non-optimal for prospect’s niche.
- Public evidence may overrepresent marketing posture over technical reality.
- Peer comparables can drift when sub-niche is too broad.

### Brand-Reputation Tradeoff (Unit Economics Framing)

For 1,000 outbound emails:
- if 5% contain wrong-signal claims, expected reputation cost must be explicitly modeled;
- outreach uplift must exceed combined direct + indirect trust damage to be net-positive.

### One Honest Unresolved Failure

Unresolved: reliability degradation when multiple public sources fail simultaneously still reduces personalization quality and can flatten reply-rate advantage.  
Business impact: lower conversion lift and possible increase in neutral/no-response outcomes.

### Kill-Switch Clause

- Trigger metric: wrong-signal claim rate in outbound QA sample.
- Threshold: pause system if wrong-signal rate exceeds 2% over rolling 7-day window.
- Rollback condition: resume only after verified fix and two consecutive clean QA windows.

---

## Sources

- `eval/score_log.json`
- `ablation_results.json`
- `held_out_traces.jsonl` (placeholder mode)
- `invoice_summary.json`
- `evidence_graph.json`
- `probes/target_failure_mode.md`
