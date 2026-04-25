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

