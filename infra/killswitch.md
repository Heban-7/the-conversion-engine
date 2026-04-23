# Kill Switch Contract

All outbound messages must pass through the kill-switch gate.

## Environment Flag

- Flag: `TENACIOUS_OUTBOUND_ENABLED`
- Default: unset
- Required behavior when unset:
  - Email routes to `TENACIOUS_OUTBOUND_SINK_EMAIL`
  - SMS routes to `TENACIOUS_OUTBOUND_SINK_SMS`

## Why This Exists

Challenge policy requires synthetic-only outreach during the interim window. Code paths that bypass routing are non-compliant even if the destination is still synthetic.

## Verification

Run:

```bash
bash infra/smoke_test.sh
```

or in PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File infra/smoke_test.ps1
```
