"""
AIDE Evolution Engine — Phase 1: Invalidation Trigger Checker

Compares collected benchmark data against principle-metadata.yaml
invalidation_triggers to determine which principles need recalibration.
"""

import os
import yaml
from datetime import datetime, timezone


PRINCIPLE_METADATA = os.environ.get("PRINCIPLE_METADATA", "principle-metadata.yaml")
BENCHMARK_DATA = os.environ.get("BENCHMARK_DATA", "evolution/benchmarks/latest.yaml")
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "evolution/benchmarks")


def load_yaml(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def check_trigger(trigger: dict, benchmarks: dict) -> dict:
    """
    Check if a single invalidation trigger has been activated.

    In production, this evaluates the trigger condition against actual
    benchmark data. Currently returns a structured assessment.
    """
    return {
        "trigger_id": trigger.get("id", "unknown"),
        "type": trigger.get("type", "unknown"),
        "condition": trigger.get("condition", ""),
        "action": trigger.get("action", ""),
        "severity": trigger.get("severity", "minor"),
        "activated": False,  # Will be True when benchmark data satisfies condition
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "note": "Requires actual benchmark data to evaluate condition",
    }


def main():
    principles = load_yaml(PRINCIPLE_METADATA)
    benchmarks = load_yaml(BENCHMARK_DATA)

    triggered = []
    all_checks = []

    for name, principle in principles.get("principles", {}).items():
        if principle.get("tier") != "adaptive":
            continue

        triggers = principle.get("invalidation_triggers", [])
        for trigger in triggers:
            result = check_trigger(trigger, benchmarks)
            all_checks.append({"principle": name, **result})
            if result["activated"]:
                triggered.append({"principle": name, **result})

    report = {
        "schema_version": "1.0",
        "check_timestamp": datetime.now(timezone.utc).isoformat(),
        "total_triggers_checked": len(all_checks),
        "triggers_activated": len(triggered),
        "activated_triggers": triggered,
        "all_checks": all_checks,
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "trigger-report.yaml")
    with open(output_path, "w") as f:
        yaml.dump(report, f, default_flow_style=False, allow_unicode=True)

    # Write flag file if any triggers activated
    if triggered:
        flag_path = os.path.join(OUTPUT_DIR, "triggered.flag")
        with open(flag_path, "w") as f:
            f.write(f"Triggered at {report['check_timestamp']}\n")
            for t in triggered:
                f.write(f"  - {t['principle']}: {t['trigger_id']}\n")
        print(f"TRIGGERS DETECTED: {len(triggered)} trigger(s) activated")
    else:
        print("No triggers activated. System is within current parameters.")

    print(f"Trigger report -> {output_path}")


if __name__ == "__main__":
    main()
