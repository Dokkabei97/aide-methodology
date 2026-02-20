"""
AIDE Evolution Engine — Phase 1: Compile Sense Report

Merges benchmark data, model scans, and trigger checks into
a single sense report for the Deliberation phase.
"""

import os
import yaml
from datetime import datetime, timezone


OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "evolution/benchmarks")


def load_yaml_safe(path: str) -> dict:
    try:
        with open(path) as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {"error": f"File not found: {path}"}


def main():
    benchmarks = load_yaml_safe(os.path.join(OUTPUT_DIR, "latest.yaml"))
    models = load_yaml_safe(os.path.join(OUTPUT_DIR, "models.yaml"))
    triggers = load_yaml_safe(os.path.join(OUTPUT_DIR, "trigger-report.yaml"))

    report = {
        "schema_version": "1.0",
        "report_type": "sense",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "benchmarks": benchmarks,
        "model_landscape": models,
        "trigger_analysis": triggers,
        "summary": {
            "triggers_activated": triggers.get("triggers_activated", 0),
            "new_model_releases": sum(
                1 for p in models.get("providers", {}).values()
                if p.get("new_release_detected", False)
            ),
            "recommendation": (
                "proceed_to_deliberation"
                if triggers.get("triggers_activated", 0) > 0
                else "no_action_needed"
            ),
        },
    }

    output_path = os.path.join(OUTPUT_DIR, "sense-report.yaml")
    with open(output_path, "w") as f:
        yaml.dump(report, f, default_flow_style=False, allow_unicode=True)

    print(f"Sense report compiled -> {output_path}")
    print(f"Triggers activated: {report['summary']['triggers_activated']}")
    print(f"Recommendation: {report['summary']['recommendation']}")


if __name__ == "__main__":
    main()
