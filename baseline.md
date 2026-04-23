# τ²-Bench Retail Baseline (Act I)

I reproduced the retail-domain dev-slice baseline using the wrapper in `eval/run_tau2_wrapper.py`, which reads `source_file/trace_log.jsonl` and writes canonical interim outputs to `eval/score_log.json` and `eval/trace_log.jsonl`. The run covers 30 tasks with 5 trials per task (150 simulations), using commit `d11a97072c49d093f7b5a3e4fe9da95b490d43ba` as recorded in `eval/score_log.json`.

Core metrics from the reproduced run are:
- pass@1 = 0.7267
- 95% CI = [0.6504, 0.7917]
- average agent cost per simulation = $0.0199
- p50 latency = 105.9521 seconds
- p95 latency = 551.6491 seconds
- infra errors = 0 (from source benchmark metadata)

Methodology: the wrapper computes empirical pass rate directly from rewards in `eval/trace_log.jsonl` and computes the 95% interval using a Wilson interval for a Bernoulli process. Latency and trial metadata are carried from the source score record and mirrored into the interim score artifact for report consistency.

Unexpected behavior observed in trajectories: latency has a long tail despite stable median performance; several interactions run significantly slower than p50, which pushes p95 into the 9-minute range. This is acceptable for baseline reproduction but highlights a cost/latency sensitivity that needs guardrails in production workflows (especially if multi-step retries are enabled).

Provenance map:
- Runner: `eval/run_tau2_wrapper.py`
- Score artifact: `eval/score_log.json`
- Trace artifact: `eval/trace_log.jsonl`
- Run metadata: `eval/run_metadata.json`
