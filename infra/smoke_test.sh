#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "Running interim smoke checks in ${ROOT_DIR}"

[[ -f "${ROOT_DIR}/.env.example" ]] && echo "[ok] env template exists"
[[ -f "${ROOT_DIR}/infra/killswitch.md" ]] && echo "[ok] kill switch docs exist"
[[ -f "${ROOT_DIR}/agent/orchestrator.py" ]] && echo "[ok] orchestrator exists"
[[ -f "${ROOT_DIR}/eval/run_tau2_wrapper.py" ]] && echo "[ok] eval wrapper exists"
[[ -f "${ROOT_DIR}/agent/requirements.txt" ]] && echo "[ok] requirements exist"

echo "Smoke test complete."
