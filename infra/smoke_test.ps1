$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Write-Host "Running interim smoke checks in $Root"

$checks = @(
    ".env.example",
    "infra/killswitch.md",
    "agent/orchestrator.py",
    "eval/run_tau2_wrapper.py",
    "agent/requirements.txt"
)

foreach ($item in $checks) {
    $path = Join-Path $Root $item
    if (-not (Test-Path $path)) {
        throw "[fail] missing $item"
    }
    Write-Host "[ok] $item exists"
}

Write-Host "Smoke test complete."
