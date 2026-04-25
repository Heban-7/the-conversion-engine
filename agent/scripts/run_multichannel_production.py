from __future__ import annotations

import json

from agent.config import load_settings
from agent.multichannel_production import MultiChannelProductionService
from agent.orchestrator import build_default_prospect


def main() -> None:
    settings = load_settings()
    output_dir = settings.interim_artifacts_dir / "production_multichannel"
    service = MultiChannelProductionService(settings=settings, base_dir=output_dir)
    summary = service.run_for_prospect(build_default_prospect())
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
