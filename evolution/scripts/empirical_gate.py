"""
AIDE Evolution Engine — Phase 3: Empirical Gate

Compares baseline vs modified task results to decide whether
the proposed principle changes should be applied.

Gate rules (all must pass):
- test_pass_rate(modified) >= test_pass_rate(baseline)
- code_quality(modified) >= code_quality(baseline)
- security_vulns(modified) <= security_vulns(baseline)
"""

import os
import yaml
from datetime import datetime, timezone

BASELINE = os.environ.get("BASELINE", "evolution/sandbox/baseline-results.yaml")
MODIFIED = os.environ.get("MODIFIED", "evolution/sandbox/modified-results.yaml")
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "evolution/sandbox")


def load_yaml(path: str) -> dict:
    try:
        with open(path) as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def compare_metrics(baseline: dict, modified: dict) -> dict:
    """Compare baseline and modified metrics. Return gate result."""
    b_metrics = baseline.get("metrics", {})
    m_metrics = modified.get("metrics", {})

    checks = []

    # Check 1: Test pass rate must not decrease
    b_tpr = b_metrics.get("test_pass_rate", 0)
    m_tpr = m_metrics.get("test_pass_rate", 0)
    checks.append({
        "metric": "test_pass_rate",
        "baseline": b_tpr,
        "modified": m_tpr,
        "delta": m_tpr - b_tpr,
        "requirement": "delta >= 0",
        "passed": m_tpr >= b_tpr,
    })

    # Check 2: Code quality must not decrease
    b_cq = b_metrics.get("code_quality_score", 0)
    m_cq = m_metrics.get("code_quality_score", 0)
    checks.append({
        "metric": "code_quality_score",
        "baseline": b_cq,
        "modified": m_cq,
        "delta": m_cq - b_cq,
        "requirement": "delta >= 0",
        "passed": m_cq >= b_cq,
    })

    # Check 3: Security vulnerabilities must not increase
    b_sv = b_metrics.get("security_vulnerability_count", 0)
    m_sv = m_metrics.get("security_vulnerability_count", 0)
    checks.append({
        "metric": "security_vulnerability_count",
        "baseline": b_sv,
        "modified": m_sv,
        "delta": m_sv - b_sv,
        "requirement": "delta <= 0",
        "passed": m_sv <= b_sv,
    })

    all_passed = all(c["passed"] for c in checks)
    return {
        "checks": checks,
        "all_passed": all_passed,
    }


def main():
    baseline = load_yaml(BASELINE)
    modified = load_yaml(MODIFIED)

    result = compare_metrics(baseline, modified)

    report = {
        "schema_version": "1.0",
        "gate_type": "empirical",
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "baseline_source": BASELINE,
        "modified_source": MODIFIED,
        "gate_result": "PASS" if result["all_passed"] else "FAIL",
        "checks": result["checks"],
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    report_path = os.path.join(OUTPUT_DIR, "empirical-gate-report.yaml")
    with open(report_path, "w") as f:
        yaml.dump(report, f, default_flow_style=False, allow_unicode=True)

    if result["all_passed"]:
        with open(os.path.join(OUTPUT_DIR, "gate-passed.flag"), "w") as f:
            f.write(f"Gate passed at {report['evaluated_at']}\n")
        print("EMPIRICAL GATE: PASSED — all metrics within acceptable range")
    else:
        failed = [c["metric"] for c in result["checks"] if not c["passed"]]
        print(f"EMPIRICAL GATE: FAILED — metrics degraded: {', '.join(failed)}")

    print(f"Gate report -> {report_path}")


if __name__ == "__main__":
    main()
