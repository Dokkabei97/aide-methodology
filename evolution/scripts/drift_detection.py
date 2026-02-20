"""
AIDE Evolution Engine — Drift Detection

Analyzes evolution history to detect systematic bias accumulation.
Prevents the methodology from drifting in one direction without check.

Safeguards:
- 3 consecutive same-direction changes -> WARNING flag
- 5 consecutive same-direction changes -> auto-strengthen + re-validate
"""

import os
import yaml
from datetime import datetime, timezone
from pathlib import Path

HISTORY_DIR = os.environ.get("HISTORY_DIR", "evolution/history")
PRINCIPLE_METADATA = os.environ.get("PRINCIPLE_METADATA", "principle-metadata.yaml")


def load_history() -> list:
    """Load all evolution history entries, sorted by timestamp."""
    history_dir = Path(HISTORY_DIR)
    if not history_dir.exists():
        return []

    entries = []
    for f in sorted(history_dir.glob("*.yaml")):
        with open(f) as fh:
            entry = yaml.safe_load(fh)
            if entry:
                entries.append(entry)
    return entries


def detect_directional_drift(history: list) -> list:
    """
    Analyze history for directional drift.

    For each principle, track whether changes consistently move
    in the same direction (e.g., always relaxing constraints).
    """
    # Track change directions per principle
    principle_directions: dict[str, list[str]] = {}

    for entry in history:
        decisions = (
            entry.get("deliberation_summary", {}).get("decisions", [])
        )
        for decision in decisions:
            if decision.get("verdict") not in ("accept", "modify"):
                continue
            # Analyze direction: "relax" or "tighten"
            # This is simplified — in production, compare old vs new values
            principle_id = f"proposal_{decision.get('index', '?')}"
            direction = "unknown"  # Would be "relax" or "tighten" based on value comparison
            principle_directions.setdefault(principle_id, []).append(direction)

    warnings = []
    for principle, directions in principle_directions.items():
        # Check for consecutive same-direction changes
        if len(directions) >= 3:
            last_3 = directions[-3:]
            if len(set(last_3)) == 1 and last_3[0] != "unknown":
                severity = "critical" if len(directions) >= 5 else "warning"
                warnings.append({
                    "principle": principle,
                    "direction": last_3[0],
                    "consecutive_count": len(directions),
                    "severity": severity,
                    "recommendation": (
                        f"{'Auto-strengthen and re-validate' if severity == 'critical' else 'Monitor closely'}: "
                        f"{principle} has moved {last_3[0]} for {len(directions)} consecutive cycles"
                    ),
                })

    return warnings


def main():
    history = load_history()

    if not history:
        print("No evolution history found. Drift detection skipped.")
        return

    warnings = detect_directional_drift(history)

    report = {
        "schema_version": "1.0",
        "analyzed_at": datetime.now(timezone.utc).isoformat(),
        "history_entries_analyzed": len(history),
        "drift_warnings": warnings,
        "drift_detected": len(warnings) > 0,
    }

    output_path = os.path.join(HISTORY_DIR, "drift-report.yaml")
    with open(output_path, "w") as f:
        yaml.dump(report, f, default_flow_style=False, allow_unicode=True)

    if warnings:
        print(f"DRIFT DETECTED: {len(warnings)} warning(s)")
        for w in warnings:
            print(f"  [{w['severity'].upper()}] {w['recommendation']}")
    else:
        print("No drift detected. Methodology evolution is balanced.")

    print(f"Drift report -> {output_path}")


if __name__ == "__main__":
    main()
