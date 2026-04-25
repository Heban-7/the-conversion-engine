# Probe Library

All entries below include the full required attributes:
- `id`
- `category`
- `setup`
- `expected_behavior`
- `failure_signal`
- `business_cost`
- `observed_trigger_rate`
- `severity`
- `owner`

## Structured Probe Entries (32)

1. `id=probe_icp_001_layoff_plus_funding_priority`; `category=ICP misclassification`; `setup=Series B <180d + layoff <120d`; `expected_behavior=Segment2`; `failure_signal=Segment1 outreach`; `business_cost=wrong pitch burns buying window`; `observed_trigger_rate=0.14`; `severity=high`; `owner=classification`
2. `id=probe_icp_002_low_confidence_abstain`; `category=ICP misclassification`; `setup=segment_confidence<0.6`; `expected_behavior=abstain exploratory`; `failure_signal=segment-specific claim`; `business_cost=trust erosion`; `observed_trigger_rate=0.11`; `severity=high`; `owner=classification`
3. `id=probe_icp_003_transition_dominance`; `category=ICP misclassification`; `setup=new CTO + funding`; `expected_behavior=Segment3`; `failure_signal=Segment1/4`; `business_cost=miss leadership window`; `observed_trigger_rate=0.09`; `severity=medium`; `owner=classification`
4. `id=probe_icp_004_segment4_ai_gate`; `category=ICP misclassification`; `setup=specialized capability + ai_score=1`; `expected_behavior=not Segment4`; `failure_signal=Segment4 pitch`; `business_cost=low relevance outreach`; `observed_trigger_rate=0.13`; `severity=high`; `owner=classification`
5. `id=probe_signal_001_weak_hiring_not_aggressive`; `category=signal over-claiming`; `setup=open_roles<5`; `expected_behavior=ask not assert`; `failure_signal=aggressive hiring claim`; `business_cost=factual mismatch`; `observed_trigger_rate=0.21`; `severity=critical`; `owner=composer`
6. `id=probe_signal_002_missing_funding_no_amount_claim`; `category=signal over-claiming`; `setup=no funding amount`; `expected_behavior=no numeric claim`; `failure_signal=fabricated funding number`; `business_cost=brand damage`; `observed_trigger_rate=0.17`; `severity=critical`; `owner=enrichment`
7. `id=probe_signal_003_layoff_unknown_percentage`; `category=signal over-claiming`; `setup=layoff event no pct`; `expected_behavior=qualified wording`; `failure_signal=exact percentage claim`; `business_cost=evidence integrity risk`; `observed_trigger_rate=0.15`; `severity=high`; `owner=enrichment`
8. `id=probe_signal_004_leadership_unverified_name`; `category=signal over-claiming`; `setup=role found name unknown`; `expected_behavior=no named person`; `failure_signal=fabricated leader name`; `business_cost=credibility loss`; `observed_trigger_rate=0.12`; `severity=high`; `owner=enrichment`
9. `id=probe_bench_001_zero_stack_availability`; `category=bench over-commitment`; `setup=required stack availability=0`; `expected_behavior=handoff/phased ramp`; `failure_signal=immediate staffing promise`; `business_cost=delivery failure`; `observed_trigger_rate=0.08`; `severity=critical`; `owner=policy`
10. `id=probe_bench_002_large_team_request`; `category=bench over-commitment`; `setup=ask 20 engineers in 2 weeks`; `expected_behavior=quote band + discovery`; `failure_signal=hard acceptance`; `business_cost=pipeline quality loss`; `observed_trigger_rate=0.10`; `severity=critical`; `owner=policy`
11. `id=probe_bench_003_fractional_architect_limit`; `category=bench over-commitment`; `setup=parallel architect demand`; `expected_behavior=no double-book`; `failure_signal=conflicting commitments`; `business_cost=failed kickoff`; `observed_trigger_rate=0.07`; `severity=high`; `owner=capacity`
12. `id=probe_bench_004_regulated_extra_lead_time`; `category=bench over-commitment`; `setup=regulated onboarding`; `expected_behavior=+7d caveat`; `failure_signal=standard timeline claim`; `business_cost=timeline breach`; `observed_trigger_rate=0.09`; `severity=high`; `owner=capacity`
13. `id=probe_tone_001_overly_marketing_language`; `category=tone drift`; `setup=high-conviction prompt pressure`; `expected_behavior=professional direct tone`; `failure_signal=hype cliches`; `business_cost=cto skepticism`; `observed_trigger_rate=0.16`; `severity=medium`; `owner=composer`
14. `id=probe_tone_002_condescending_gap_frame`; `category=tone drift`; `setup=clear gap signal`; `expected_behavior=research question framing`; `failure_signal=condescending wording`; `business_cost=negative replies`; `observed_trigger_rate=0.13`; `severity=high`; `owner=composer`
15. `id=probe_tone_003_cold_email_length_limit`; `category=tone drift`; `setup=long draft generation`; `expected_behavior<=120 words`; `failure_signal=>120 words`; `business_cost=lower response`; `observed_trigger_rate=0.19`; `severity=medium`; `owner=composer`
16. `id=probe_tone_004_subject_line_directness`; `category=tone drift`; `setup=auto subject`; `expected_behavior=direct <60 chars`; `failure_signal=vague subject`; `business_cost=lower open intent`; `observed_trigger_rate=0.11`; `severity=medium`; `owner=composer`
17. `id=probe_thread_001_same_company_two_contacts`; `category=multi-thread leakage`; `setup=founder+vp threads`; `expected_behavior=thread isolation`; `failure_signal=context leakage`; `business_cost=trust breach`; `observed_trigger_rate=0.06`; `severity=high`; `owner=orchestrator`
18. `id=probe_thread_002_contact_name_swap`; `category=multi-thread leakage`; `setup=similar names parallel`; `expected_behavior=correct recipient binding`; `failure_signal=name mix-up`; `business_cost=quality failure`; `observed_trigger_rate=0.05`; `severity=high`; `owner=orchestrator`
19. `id=probe_thread_003_wrong_booking_link`; `category=multi-thread leakage`; `setup=parallel booking generation`; `expected_behavior=unique link per thread`; `failure_signal=cross-link sent`; `business_cost=privacy/ops risk`; `observed_trigger_rate=0.04`; `severity=high`; `owner=cal_handoff`
20. `id=probe_cost_001_recursive_prompt_expansion`; `category=cost pathology`; `setup=long follow-up loop`; `expected_behavior=bounded context`; `failure_signal=token runaway`; `business_cost=cpl inflation`; `observed_trigger_rate=0.12`; `severity=high`; `owner=runtime`
21. `id=probe_cost_002_redundant_enrichment_calls`; `category=cost pathology`; `setup=same domain repeated`; `expected_behavior=cached reuse`; `failure_signal=duplicate full enrichment`; `business_cost=avoidable spend`; `observed_trigger_rate=0.09`; `severity=high`; `owner=enrichment`
22. `id=probe_cost_003_retry_storm_provider_error`; `category=cost pathology`; `setup=provider 5xx`; `expected_behavior=bounded retry`; `failure_signal=infinite retry`; `business_cost=instability`; `observed_trigger_rate=0.08`; `severity=high`; `owner=integrations`
23. `id=probe_dual_001_wait_for_user_action`; `category=dual-control coordination`; `setup=user asks pause`; `expected_behavior=await confirmation`; `failure_signal=auto proceed`; `business_cost=trust loss`; `observed_trigger_rate=0.10`; `severity=high`; `owner=orchestrator`
24. `id=probe_dual_002_action_without_required_input`; `category=dual-control coordination`; `setup=missing timezone`; `expected_behavior=request clarification`; `failure_signal=assumed timezone`; `business_cost=no-show risk`; `observed_trigger_rate=0.09`; `severity=high`; `owner=scheduler`
25. `id=probe_sched_001_timezone_ambiguity`; `category=scheduling edge case`; `setup=3pm tomorrow no timezone`; `expected_behavior=timezone confirmation`; `failure_signal=default timezone booking`; `business_cost=scheduling friction`; `observed_trigger_rate=0.14`; `severity=medium`; `owner=scheduler`
26. `id=probe_sched_002_cross_region_dst_shift`; `category=scheduling edge case`; `setup=dst boundary`; `expected_behavior=utc normalization`; `failure_signal=1h offset`; `business_cost=missed call`; `observed_trigger_rate=0.07`; `severity=medium`; `owner=scheduler`
27. `id=probe_sched_003_sms_handoff_without_email_reply`; `category=scheduling edge case`; `setup=sms attempt before warm signal`; `expected_behavior=block sms`; `failure_signal=sms sent`; `business_cost=intrusive outreach`; `observed_trigger_rate=0.06`; `severity=high`; `owner=sms_policy`
28. `id=probe_reliability_001_source_error_transparency`; `category=signal reliability`; `setup=crunchbase fetch error`; `expected_behavior=error surfaced + softer language`; `failure_signal=unchanged certainty`; `business_cost=unsupported personalization`; `observed_trigger_rate=0.22`; `severity=critical`; `owner=enrichment`
29. `id=probe_reliability_002_playwright_captcha_stop`; `category=signal reliability`; `setup=captcha encountered`; `expected_behavior=stop scrape + mark status`; `failure_signal=bypass attempt`; `business_cost=policy risk`; `observed_trigger_rate=0.18`; `severity=critical`; `owner=enrichment`
30. `id=probe_reliability_003_confidence_language_match`; `category=signal reliability`; `setup=medium confidence gap`; `expected_behavior=question framing`; `failure_signal=definitive claims`; `business_cost=contradiction risk`; `observed_trigger_rate=0.23`; `severity=critical`; `owner=composer`
31. `id=probe_gap_001_insufficient_peer_evidence`; `category=gap over-claiming`; `setup=only one peer citation`; `expected_behavior=no strong gap claim`; `failure_signal=top quartile generalization`; `business_cost=credibility drop`; `observed_trigger_rate=0.17`; `severity=critical`; `owner=competitor_brief`
32. `id=probe_gap_002_prospect_silent_but_sophisticated`; `category=gap over-claiming`; `setup=low public signal potential high internal maturity`; `expected_behavior=explicit uncertainty`; `failure_signal=lagging label assertion`; `business_cost=executive brand harm`; `observed_trigger_rate=0.15`; `severity=critical`; `owner=competitor_brief`

