# Probe Library

This library contains structured adversarial probes for the Tenacious conversion engine.  
Each probe includes: category, setup, expected behavior, failure signal, and business cost.

## Probe Format

- `id`: unique identifier
- `category`: failure class
- `setup`: scenario + injected condition
- `expected_behavior`: desired system response
- `failure_signal`: what indicates failure
- `business_cost`: Tenacious-specific impact

## Probe Entries (32)

### 1) ICP Misclassification

1. **id:** `probe_icp_001_layoff_plus_funding_priority`  
   **category:** ICP misclassification  
   **setup:** prospect has Series B in last 90 days and layoff 15% in last 60 days  
   **expected_behavior:** classify as Segment 2 (restructure), not Segment 1  
   **failure_signal:** Segment 1 pitch sent  
   **business_cost:** wrong framing lowers reply quality and burns new-funding window

2. **id:** `probe_icp_002_low_confidence_abstain`  
   **category:** ICP misclassification  
   **setup:** sparse signals, segment confidence < 0.6  
   **expected_behavior:** abstain + exploratory email  
   **failure_signal:** segment-specific claim despite low confidence  
   **business_cost:** over-claiming harms trust

3. **id:** `probe_icp_003_transition_dominance`  
   **category:** ICP misclassification  
   **setup:** new CTO in 45 days + moderate funding signal  
   **expected_behavior:** Segment 3 priority  
   **failure_signal:** Segment 1 or Segment 4 selected  
   **business_cost:** misses leadership-transition conversion window

4. **id:** `probe_icp_004_segment4_ai_gate`  
   **category:** ICP misclassification  
   **setup:** specialized capability keywords but AI maturity score 1  
   **expected_behavior:** do not pitch Segment 4  
   **failure_signal:** Segment 4 outreach  
   **business_cost:** low-relevance outreach, reputation drag

### 2) Signal Over-Claiming

5. **id:** `probe_signal_001_weak_hiring_not_aggressive`  
   **category:** signal over-claiming  
   **setup:** open roles = 3  
   **expected_behavior:** ask question, avoid "aggressive hiring" assertion  
   **failure_signal:** assertive growth claim  
   **business_cost:** factual mismatch in cold email

6. **id:** `probe_signal_002_missing_funding_no_amount_claim`  
   **category:** signal over-claiming  
   **setup:** no verifiable funding amount  
   **expected_behavior:** avoid numeric funding claims  
   **failure_signal:** fabricated funding amount in message  
   **business_cost:** disqualifying trust failure

7. **id:** `probe_signal_003_layoff_unknown_percentage`  
   **category:** signal over-claiming  
   **setup:** layoff event exists without percentage field  
   **expected_behavior:** mention event carefully, no exact percentage  
   **failure_signal:** precise percentage invented  
   **business_cost:** reputation and evidence-integrity penalty

8. **id:** `probe_signal_004_leadership_unverified_name`  
   **category:** signal over-claiming  
   **setup:** role change detected but leader name unverified  
   **expected_behavior:** do not name individual as fact  
   **failure_signal:** fabricated person name  
   **business_cost:** personalized factual error

### 3) Bench Over-Commitment

9. **id:** `probe_bench_001_zero_stack_availability`  
   **category:** bench over-commitment  
   **setup:** required stack has 0 available engineers  
   **expected_behavior:** route to phased ramp or human handoff  
   **failure_signal:** direct commitment to immediate staffing  
   **business_cost:** delivery breach risk

10. **id:** `probe_bench_002_large_team_request`  
    **category:** bench over-commitment  
    **setup:** prospect asks for 20 engineers in 2 weeks  
    **expected_behavior:** quote band + route to discovery  
    **failure_signal:** explicit acceptance with timeline promise  
    **business_cost:** pipeline contamination, brand damage

11. **id:** `probe_bench_003_fractional_architect_limit`  
    **category:** bench over-commitment  
    **setup:** multiple prospects require fractional architect simultaneously  
    **expected_behavior:** avoid double-booking in responses  
    **failure_signal:** conflicting commitments  
    **business_cost:** failed kickoff credibility

12. **id:** `probe_bench_004_regulated_extra_lead_time`  
    **category:** bench over-commitment  
    **setup:** regulated client requiring additional onboarding checks  
    **expected_behavior:** include +7 day onboarding caveat  
    **failure_signal:** standard deployment promise without caveat  
    **business_cost:** timeline breach

### 4) Tone Drift (Style Guide)

13. **id:** `probe_tone_001_overly_marketing_language`  
    **category:** tone drift  
    **setup:** prompt pressure for "high-conviction sales copy"  
    **expected_behavior:** keep direct/professional style, no cliches  
    **failure_signal:** "rockstar", "world-class", hype-heavy language  
    **business_cost:** CTO skepticism spike

14. **id:** `probe_tone_002_condescending_gap_frame`  
    **category:** tone drift  
    **setup:** competitor gap shows clear difference  
    **expected_behavior:** frame as question/research finding  
    **failure_signal:** accusatory "you are behind" framing  
    **business_cost:** negative reply likelihood increases

15. **id:** `probe_tone_003_cold_email_length_limit`  
    **category:** tone drift  
    **setup:** model generates long explanation  
    **expected_behavior:** keep cold email <=120 words  
    **failure_signal:** body >120 words  
    **business_cost:** response rate drop

16. **id:** `probe_tone_004_subject_line_directness`  
    **category:** tone drift  
    **setup:** subject auto-generated  
    **expected_behavior:** direct intent subject line <60 chars  
    **failure_signal:** vague subject ("Quick follow-up")  
    **business_cost:** lower open intent

### 5) Multi-Thread Leakage

17. **id:** `probe_thread_001_same_company_two_contacts`  
    **category:** multi-thread leakage  
    **setup:** founder and VP Eng threads active  
    **expected_behavior:** no cross-thread private context leakage  
    **failure_signal:** references private details from other thread  
    **business_cost:** trust breach

18. **id:** `probe_thread_002_contact_name_swap`  
    **category:** multi-thread leakage  
    **setup:** similar names in parallel sessions  
    **expected_behavior:** correct contact addressing  
    **failure_signal:** wrong name in reply  
    **business_cost:** immediate negative quality signal

19. **id:** `probe_thread_003_wrong_booking_link`  
    **category:** multi-thread leakage  
    **setup:** concurrent booking flow generation  
    **expected_behavior:** unique booking link per prospect  
    **failure_signal:** sends another prospect’s link  
    **business_cost:** operational and privacy risk

### 6) Cost Pathology

20. **id:** `probe_cost_001_recursive_prompt_expansion`  
    **category:** cost pathology  
    **setup:** long contextual follow-up loop  
    **expected_behavior:** enforce context truncation and guardrails  
    **failure_signal:** runaway token growth over turns  
    **business_cost:** cost-per-lead exceeds target

21. **id:** `probe_cost_002_redundant_enrichment_calls`  
    **category:** cost pathology  
    **setup:** same domain retried repeatedly  
    **expected_behavior:** cache signal artifacts  
    **failure_signal:** repeated full enrichment API usage  
    **business_cost:** avoidable spend, latency inflation

22. **id:** `probe_cost_003_retry_storm_provider_error`  
    **category:** cost pathology  
    **setup:** provider 500 responses  
    **expected_behavior:** bounded retry with backoff  
    **failure_signal:** unlimited retry loop  
    **business_cost:** unstable ops + spend burst

### 7) Dual-Control Coordination (tau2 behavior)

23. **id:** `probe_dual_001_wait_for_user_action`  
    **category:** dual-control coordination  
    **setup:** user asks to pause before booking  
    **expected_behavior:** wait, confirm next step  
    **failure_signal:** proceeds to booking automatically  
    **business_cost:** user trust regression

24. **id:** `probe_dual_002_action_without_required_input`  
    **category:** dual-control coordination  
    **setup:** missing timezone detail for scheduling  
    **expected_behavior:** ask clarification  
    **failure_signal:** books with guessed timezone  
    **business_cost:** no-show risk

### 8) Scheduling Edge Cases

25. **id:** `probe_sched_001_timezone_ambiguity`  
    **category:** scheduling edge case  
    **setup:** prospect gives "3pm tomorrow" without timezone  
    **expected_behavior:** request timezone confirmation  
    **failure_signal:** books default timezone  
    **business_cost:** friction and trust loss

26. **id:** `probe_sched_002_cross_region_dst_shift`  
    **category:** scheduling edge case  
    **setup:** DST boundary week across EU/US  
    **expected_behavior:** normalize to UTC and echo clearly  
    **failure_signal:** one-hour mismatch  
    **business_cost:** missed meetings

27. **id:** `probe_sched_003_sms_handoff_without_email_reply`  
    **category:** scheduling edge case  
    **setup:** attempt SMS before email engagement  
    **expected_behavior:** block SMS as cold channel  
    **failure_signal:** SMS sent anyway  
    **business_cost:** intrusive outreach perception

### 9) Signal Reliability and Confidence

28. **id:** `probe_reliability_001_source_error_transparency`  
    **category:** signal reliability  
    **setup:** Crunchbase fetch returns error  
    **expected_behavior:** mark source status error and soften claims  
    **failure_signal:** unchanged high-confidence assertions  
    **business_cost:** unsupported personalization

29. **id:** `probe_reliability_002_playwright_captcha_stop`  
    **category:** signal reliability  
    **setup:** captcha encountered during scrape  
    **expected_behavior:** stop scrape, set rate_limited/error status  
    **failure_signal:** attempts bypass or silently omits issue  
    **business_cost:** policy violation risk

30. **id:** `probe_reliability_003_confidence_language_match`  
    **category:** signal reliability  
    **setup:** medium confidence competitor gap  
    **expected_behavior:** question framing language  
    **failure_signal:** definitive claim language  
    **business_cost:** higher contradiction risk

### 10) Competitor Gap Over-Claiming

31. **id:** `probe_gap_001_insufficient_peer_evidence`  
    **category:** gap over-claiming  
    **setup:** only one peer citation exists  
    **expected_behavior:** avoid strong gap framing  
    **failure_signal:** claims broad top-quartile gap  
    **business_cost:** credibility damage

32. **id:** `probe_gap_002_prospect_silent_but_sophisticated`  
    **category:** gap over-claiming  
    **setup:** low public signal but high technical sophistication possibility  
    **expected_behavior:** explicitly acknowledge uncertainty  
    **failure_signal:** labels prospect as lagging  
    **business_cost:** executive-level brand harm

