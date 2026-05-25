"""Weekly Intel — Phase F: RFC draft generator.

If Phase D set ``should_dispatch: true`` AND the dispatch reasons are
strong enough to warrant a structural change proposal, Phase F drops an
RFC draft into ``rfcs/NNNN-weekly-intel-{date}.md`` with the next
available RFC number.

The draft is intentionally a *stub*. It pre-fills:
  * the RFC template header (Agent Used / Agent Model / Research Method / Date / Status)
  * a summary linking back to the weekly synthesis under ``research/``
  * the empirical evidence collected this week
  * placeholder sections for Detailed Design / Impact / Alternatives

A different-vendor reviewer agent must fill the placeholders and
co-sign before the RFC moves from ``Draft`` to ``Discussion``. This
preserves Axioms A2 (Adversarial Separation) and A4 (No Single
Authority): the auto-generated draft has zero authority on its own.

Threshold for drafting:
  * dispatch.should_dispatch is true, AND
  * at least 2 of {vendor_release_count >= 3, viral_hn_count >= 3,
                   benchmark_shift_count >= 1}.

If only one mild reason fires, the weekly synthesis records it but no
RFC is opened — RFCs are expensive review surface and should not be
created for every quiet signal.
"""

from __future__ import annotations

import json
import os
import re
from datetime import date

import yaml


INTEL_DIR = os.environ.get("INTEL_DIR", "evolution/intel")
RFCS_DIR = os.environ.get("RFCS_DIR", "rfcs")
RESEARCH_DIR = os.environ.get("RESEARCH_DIR", "research")
AUTHOR_MODEL = os.environ.get("SYNTHESIS_AUTHOR_MODEL", "claude-opus-4-7")
AUTHOR_VENDOR = os.environ.get("SYNTHESIS_AUTHOR_VENDOR", "anthropic")

DISPATCH_FILE = os.path.join(INTEL_DIR, "dispatch.json")
DIGEST_YAML = os.path.join(INTEL_DIR, "weekly-digest.yaml")

RFC_DECISION_FILE = os.path.join(INTEL_DIR, "rfc-decision.json")


def _load_json(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f) or {}


def _load_yaml(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def _next_rfc_number() -> int:
    if not os.path.isdir(RFCS_DIR):
        return 1
    used = []
    for f in os.listdir(RFCS_DIR):
        m = re.match(r"(\d{4})-", f)
        if m:
            used.append(int(m.group(1)))
    return max(used) + 1 if used else 1


def _should_draft(dispatch: dict) -> tuple[bool, list[str]]:
    if not dispatch.get("should_dispatch"):
        return False, ["dispatch flag is false"]

    payload = dispatch.get("client_payload") or {}
    strong = []
    if (payload.get("vendor_release_count") or 0) >= 3:
        strong.append(f"vendor_release_count={payload.get('vendor_release_count')}")
    if (payload.get("viral_hn_count") or 0) >= 3:
        strong.append(f"viral_hn_count={payload.get('viral_hn_count')}")
    if (payload.get("benchmark_shift_count") or 0) >= 1:
        strong.append(f"benchmark_shift_count={payload.get('benchmark_shift_count')}")

    if len(strong) >= 2:
        return True, strong
    return False, [f"only {len(strong)} strong reason(s): {strong}"]


def _render_rfc(rfc_number: int, today: str, dispatch: dict, digest: dict) -> str:
    payload = dispatch.get("client_payload") or {}
    reasons = dispatch.get("reasons") or []
    synth_path = f"{RESEARCH_DIR}/en/{today}-weekly-synthesis.md"
    intel_path = f"{INTEL_DIR}/weekly-{today}.md"

    vendor_releases = digest.get("vendor_releases") or []
    viral_hn = digest.get("viral_hn") or []
    benchmark_shifts = digest.get("benchmark_shifts") or []

    lines: list[str] = []
    lines.append(f"- RFC Number: {rfc_number:04d}")
    lines.append(f"- Title: Weekly Intel Signal Response — {today}")
    lines.append(f"- Agent Used: aide-weekly-intel/draft_rfc.py v1 (drafter)")
    lines.append(f"- Agent Model: {AUTHOR_MODEL} (vendor: {AUTHOR_VENDOR}) — single-vendor draft")
    lines.append(f"- Research Method: Weekly intel sensor scan (Phases A–D) + deterministic synthesis (Phase E)")
    lines.append(f"- Date: {today}")
    lines.append(f"- Status: Draft (awaits different-vendor reviewer per Axiom A2 / A4)")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(
        f"The weekly intel sensor for {today} crossed dispatch thresholds in "
        f"{len(reasons)} category/categories ({'; '.join(reasons)}). "
        "This RFC is the structural review surface for the resulting "
        "candidate methodology changes. The reviewer's task is to confirm, "
        "amend, or reject the architectural claims surfaced in "
        f"`{synth_path}`, then promote this RFC to `Discussion` once at "
        "least one different-vendor agent co-signs."
    )
    lines.append("")
    lines.append("## Motivation")
    lines.append("")
    lines.append(
        "AIDE's adaptive principles are calibrated against the actual "
        "frontier of agent capability. When that frontier moves materially "
        "in a single week — new vendor capability, viral developer "
        "convergence on a topic, or measurable benchmark shift — the "
        "monthly Evolution Engine cycle is too coarse a feedback loop. "
        "This RFC exists to make those signals reviewable on a weekly "
        "cadence without prematurely editing `principle-metadata.yaml` "
        "(which still requires multi-vendor consensus per A4)."
    )
    lines.append("")

    lines.append("## Evidence")
    lines.append("")
    lines.append(f"Raw signals collected in `{intel_path}`. Synthesis in `{synth_path}`.")
    lines.append("")
    lines.append(f"- **Vendor-shipped agent capabilities**: {len(vendor_releases)} keyword-matched releases.")
    for hit in vendor_releases[:5]:
        lines.append(f"  - {hit.get('vendor')} — [{hit.get('title')}]({hit.get('url')})")
    if len(vendor_releases) > 5:
        lines.append(f"  - … and {len(vendor_releases) - 5} more")
    lines.append("")
    lines.append(f"- **Community pressure (viral HN)**: {len(viral_hn)} stories ≥150 pts.")
    for v in viral_hn[:5]:
        lines.append(f"  - [{v.get('title')}]({v.get('url')}) — {v.get('points')} pts · query `{v.get('query')}`")
    if len(viral_hn) > 5:
        lines.append(f"  - … and {len(viral_hn) - 5} more")
    lines.append("")
    lines.append(f"- **Benchmark SOTA shifts**: {len(benchmark_shifts)} tracked deltas ≥2.0pp.")
    for s in benchmark_shifts:
        lines.append(f"  - **{s.get('benchmark')}**: {s.get('prior_pct'):.2f}% → {s.get('current_pct'):.2f}% (Δ {s.get('delta_pp'):+.2f}pp)")
    lines.append("")
    src_health = payload.get("source_health") or {}
    lines.append(f"- **Source health (A5)**: {src_health.get('ok', 0)}/{src_health.get('total', 0)} sources reached this scan.")
    lines.append("")

    lines.append("## Detailed Design")
    lines.append("")
    lines.append(
        "_(Reviewer to fill.)_ Based on the evidence above, propose at "
        "most one structural change to either:"
    )
    lines.append("")
    lines.append("1. `principle-metadata.yaml` adaptive parameters (numeric calibration), or")
    lines.append("2. An adaptive principle's validity conditions / invalidation triggers, or")
    lines.append("3. `docs/{en,ko}/AIDE-METHODOLOGY.md` body text (requires the strongest evidence).")
    lines.append("")
    lines.append(
        "Per the existing RFC-0003 §4 contract, body changes to the "
        "methodology require co-signed RFCs; numeric calibration changes "
        "can proceed via `principle-metadata.yaml` edits in the same PR if "
        "the evidence is calibration-grade."
    )
    lines.append("")

    lines.append("## Impact Assessment")
    lines.append("")
    lines.append("- **Existing principles**: _(Reviewer to fill — which adaptive principles' validity conditions are touched.)_")
    lines.append("- **Adopters**: _(Reviewer to fill — backward-compatible? requires migration note?)_")
    lines.append("- **Axioms**: This RFC cannot modify axioms. If the evidence appears to challenge an axiom, escalate to an Axiom Review (separate process) instead of editing here.")
    lines.append("")

    lines.append("## Alternatives Considered")
    lines.append("")
    lines.append("- **Do nothing this week**: appropriate if reviewer judges the evidence as below calibration-grade. Document the reasoning here so future weeks have a precedent.")
    lines.append("- **Wait for monthly Evolution Engine**: appropriate if the change is large enough to require empirical sandbox runs.")
    lines.append("- **Open a Discussion thread without RFC**: appropriate for community signals that have not yet produced measurable architectural pressure.")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "**Reviewer checklist (must complete before promoting Status):**"
    )
    lines.append("")
    lines.append("- [ ] Different-vendor reviewer model identified (Axiom A2)")
    lines.append("- [ ] Reviewer has independently verified at least one piece of evidence above against its primary source")
    lines.append("- [ ] If proposing a `principle-metadata.yaml` edit: evidence is quantitative (Axiom A3)")
    lines.append("- [ ] Detailed Design section filled with a concrete diff")
    lines.append("- [ ] Reverse path documented (Axiom A1 — what does revert look like?)")
    return "\n".join(lines) + "\n"


def main() -> None:
    dispatch = _load_json(DISPATCH_FILE)
    digest = _load_yaml(DIGEST_YAML)

    decision = {
        "evaluated_at": None,
        "drafted": False,
        "reason": "",
        "rfc_path": None,
        "rfc_number": None,
    }

    from datetime import datetime, timezone
    decision["evaluated_at"] = datetime.now(timezone.utc).isoformat()

    if not dispatch:
        decision["reason"] = "no dispatch.json — Phase D did not produce a decision"
        _write_decision(decision)
        print(decision["reason"])
        return

    should_draft, reason_detail = _should_draft(dispatch)
    if not should_draft:
        decision["reason"] = f"below RFC threshold: {reason_detail}"
        _write_decision(decision)
        print(decision["reason"])
        return

    today = date.today().isoformat()
    rfc_number = _next_rfc_number()
    rfc_path = os.path.join(RFCS_DIR, f"{rfc_number:04d}-weekly-intel-{today}.md")
    os.makedirs(RFCS_DIR, exist_ok=True)

    if os.path.exists(rfc_path):
        decision["reason"] = f"RFC already exists at {rfc_path} — not overwriting"
        _write_decision(decision)
        print(decision["reason"])
        return

    body = _render_rfc(rfc_number, today, dispatch, digest)
    with open(rfc_path, "w") as f:
        f.write(body)

    decision.update(
        {
            "drafted": True,
            "reason": f"thresholds crossed: {reason_detail}",
            "rfc_path": rfc_path,
            "rfc_number": rfc_number,
        }
    )
    _write_decision(decision)
    print(f"RFC draft -> {rfc_path}")


def _write_decision(decision: dict) -> None:
    os.makedirs(INTEL_DIR, exist_ok=True)
    with open(RFC_DECISION_FILE, "w") as f:
        json.dump(decision, f, indent=2)


if __name__ == "__main__":
    main()
