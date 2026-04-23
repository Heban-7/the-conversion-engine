from __future__ import annotations

from pathlib import Path

from agent.config import load_settings
from agent.orchestrator import build_default_prospect, run_single_prospect_flow


def main() -> None:
    settings = load_settings()
    output_dir = settings.interim_artifacts_dir / "single_prospect_flow"
    prospect = build_default_prospect()
    run_single_prospect_flow(settings, prospect, output_dir)
    print(f"single flow artifacts written to: {output_dir}")


if __name__ == "__main__":
    main()
