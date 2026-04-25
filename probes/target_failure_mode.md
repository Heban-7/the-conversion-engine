# Target Failure Mode

## Selected Target

`signal_overclaiming_under_source_uncertainty`

## Why This Is Highest ROI

This failure mode combines:
- high trigger rate (`18%` from current dev/simulated probes),
- direct brand risk (factual trust in first contact),
- large downstream business cost (reply drop + reputation penalty).

## Side-by-Side ROI Comparison (With Arithmetic)

Formula:
- `risk_exposure = trigger_rate * 1000_outbound`
- `monthly_risk_cost = risk_exposure * cost_per_failure`
- `roi_index = monthly_risk_cost / remediation_hours`

| Failure Mode | Trigger Rate | Cost/Failure (USD) | Remediation Hours | Arithmetic | ROI Index |
|---|---:|---:|---:|---|---:|
| signal_overclaiming_under_source_uncertainty (target) | 0.18 | 220 | 36 | (0.18*1000*220)/36 | 1,100 |
| bench_overcommitment_promises | 0.09 | 340 | 34 | (0.09*1000*340)/34 | 900 |
| signal_reliability_confidence_mismatch | 0.21 | 160 | 42 | (0.21*1000*160)/42 | 800 |

Conclusion: target mode has highest ROI index and highest near-term business-risk reduction per engineering hour.

## Tenacious Business-Cost Derivation

### Assumptions (from challenge numbers)

- Signal-grounded outbound top-quartile reply rate: 7-12%.
- Baseline cold outbound reply rate: 1-3%.
- ACV range used in scenario math: talent outsourcing and project consulting ranges from seed materials.
- Stalled-thread risk and brand penalty applied to wrong-signal emails.

### Cost Sketch

For 1,000 outbound messages:
- If 5% contain wrong-signal assertions, that is 50 brand-risk touches.
- Conservative impact model:
  - direct lost positive replies on those 50 touches,
  - indirect trust penalty on follow-on threads within same prospect cohort.
- With conversion funnel compounding, this can erase much of the expected uplift from signal-grounded outreach.

## Failure Signature

- `data_sources_checked` shows `error/partial`, but generated outreach still uses high-certainty language.
- Weak hiring velocity (`<5` roles) still rendered as “aggressive hiring”.
- Missing funding/leadership detail still rendered as precise factual claim.

## Proposed Mechanism (Implemented Direction)

1. Source-status-aware confidence model (hard link between source reliability and language strength).
2. Composer policy:
   - high confidence -> assertive evidence statement
   - medium confidence -> soft comparative framing
   - low confidence -> question-only framing
3. Guardrail that blocks send on contradictory claim-confidence combinations.

## Success Criterion

- Reduce over-claiming probe trigger rate by >=50% on dev suite.
- Demonstrate positive Delta A on held-out slice with p < 0.05 against Day-1 baseline.

