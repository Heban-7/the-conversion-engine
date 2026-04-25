# Failure Taxonomy

Failure taxonomy derived from `probes/probe_library.md`. Trigger rates below are from current dev/simulated probe replay and are placeholders pending sealed held-out replay.

## Summary Table

| Category | Probe IDs | Trigger Rate | Severity |
|---|---|---:|---|
| ICP misclassification | 001-004 | 12% | High |
| Signal over-claiming | 005-008 | 18% | Critical |
| Bench over-commitment | 009-012 | 9% | Critical |
| Tone drift | 013-016 | 14% | Medium |
| Multi-thread leakage | 017-019 | 6% | High |
| Cost pathology | 020-022 | 11% | High |
| Dual-control coordination | 023-024 | 10% | High |
| Scheduling edge cases | 025-027 | 13% | Medium |
| Signal reliability mismatch | 028-030 | 21% | Critical |
| Gap over-claiming | 031-032 | 16% | Critical |

## Probe-to-Category Mapping (One Probe, One Category)

| Probe ID | Category |
|---|---|
| probe_icp_001_layoff_plus_funding_priority | ICP misclassification |
| probe_icp_002_low_confidence_abstain | ICP misclassification |
| probe_icp_003_transition_dominance | ICP misclassification |
| probe_icp_004_segment4_ai_gate | ICP misclassification |
| probe_signal_001_weak_hiring_not_aggressive | Signal over-claiming |
| probe_signal_002_missing_funding_no_amount_claim | Signal over-claiming |
| probe_signal_003_layoff_unknown_percentage | Signal over-claiming |
| probe_signal_004_leadership_unverified_name | Signal over-claiming |
| probe_bench_001_zero_stack_availability | Bench over-commitment |
| probe_bench_002_large_team_request | Bench over-commitment |
| probe_bench_003_fractional_architect_limit | Bench over-commitment |
| probe_bench_004_regulated_extra_lead_time | Bench over-commitment |
| probe_tone_001_overly_marketing_language | Tone drift |
| probe_tone_002_condescending_gap_frame | Tone drift |
| probe_tone_003_cold_email_length_limit | Tone drift |
| probe_tone_004_subject_line_directness | Tone drift |
| probe_thread_001_same_company_two_contacts | Multi-thread leakage |
| probe_thread_002_contact_name_swap | Multi-thread leakage |
| probe_thread_003_wrong_booking_link | Multi-thread leakage |
| probe_cost_001_recursive_prompt_expansion | Cost pathology |
| probe_cost_002_redundant_enrichment_calls | Cost pathology |
| probe_cost_003_retry_storm_provider_error | Cost pathology |
| probe_dual_001_wait_for_user_action | Dual-control coordination |
| probe_dual_002_action_without_required_input | Dual-control coordination |
| probe_sched_001_timezone_ambiguity | Scheduling edge cases |
| probe_sched_002_cross_region_dst_shift | Scheduling edge cases |
| probe_sched_003_sms_handoff_without_email_reply | Scheduling edge cases |
| probe_reliability_001_source_error_transparency | Signal reliability mismatch |
| probe_reliability_002_playwright_captcha_stop | Signal reliability mismatch |
| probe_reliability_003_confidence_language_match | Signal reliability mismatch |
| probe_gap_001_insufficient_peer_evidence | Gap over-claiming |
| probe_gap_002_prospect_silent_but_sophisticated | Gap over-claiming |

## Category Notes

### ICP Misclassification

- Primary error pattern: incorrect precedence in overlapping-signal scenarios.
- Highest-value fix: strict segment priority and abstention on low confidence.

### Signal Over-Claiming

- Primary error pattern: assertive language when data source confidence is low.
- Highest-value fix: confidence-aware phrasing policy at compose time.

### Bench Over-Commitment

- Primary error pattern: staffing promises not gated by current bench availability.
- Highest-value fix: hard commitment gate + human handoff path.

### Tone Drift

- Primary error pattern: persuasive language drifting toward generic outbound cliches.
- Highest-value fix: post-draft tone checker against style guide markers.

### Multi-Thread Leakage

- Primary error pattern: event correlation bugs in concurrent conversations.
- Highest-value fix: strict thread-scoped state and message routing.

### Cost Pathology

- Primary error pattern: repetitive enrichment and unbounded retries.
- Highest-value fix: cache + retry budget enforcement.

### Dual-Control Coordination

- Primary error pattern: proceeding without explicit user/prospect confirmation.
- Highest-value fix: action gating requiring explicit confirmation tokens.

### Scheduling Edge Cases

- Primary error pattern: timezone assumptions and premature SMS handoff.
- Highest-value fix: timezone confirm step + warm-channel precondition.

### Signal Reliability

- Primary error pattern: source fetch failures not reflected in confidence language.
- Highest-value fix: hard dependency between source status and claim strength.

### Gap Over-Claiming

- Primary error pattern: broad gap statements from thin peer evidence.
- Highest-value fix: require >=2 strong citations for high-confidence gap claims.

## ROI Comparison (Arithmetic)

Assumptions for comparison:
- 1,000 outbound messages/month
- category risk exposure = `trigger_rate * 1000`
- cost_per_failure is category-specific estimate in USD equivalent impact
- monthly_risk_cost = `risk_exposure * cost_per_failure`
- remediation_effort is estimated engineering-hours
- roi_index = `monthly_risk_cost / remediation_effort`

| Candidate Failure Mode | Trigger Rate | Risk Exposure | Cost/Failure (USD) | Monthly Risk Cost (USD) | Remediation Effort (hrs) | ROI Index |
|---|---:|---:|---:|---:|---:|---:|
| Signal over-claiming | 0.18 | 180 | 220 | 39,600 | 36 | 1,100 |
| Signal reliability mismatch | 0.21 | 210 | 160 | 33,600 | 42 | 800 |
| Bench over-commitment | 0.09 | 90 | 340 | 30,600 | 34 | 900 |

Interpretation:
- **Signal over-claiming** has the highest ROI index in this model and remains the top mechanism target.
- **Bench over-commitment** is lower frequency but very high per-incident cost.
- **Signal reliability mismatch** is highest frequency but lower per-incident cost than over-claiming.

