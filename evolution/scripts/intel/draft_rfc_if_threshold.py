"""Weekly Intel — Phase F: Conditional RFC draft generator.

Generates a *draft* RFC under rfcs/ when the weekly digest crosses a
high-signal threshold, and otherwise does nothing. Conservative on
purpose: every draft costs the maintainer a triage cycle, and an
auto-RFC that nobody reads erodes the RFC process itself.

A draft only emerges when at least one of:
  * ≥ 2 vendor-release candidates AND ≥ 1 of them is a new model/agent
    runtime (keywords: opus, sonnet, haiku, gpt-, gemini, agent sdk,
    cli, runtime, platform).
  * ≥ 1 benchmark SOTA shift ≥ 2.0pp.
  * ≥ 3 viral HN stories on tracked queries.

All drafts are clearly marked agent-generated, awaiting different-vendor
review (A2/A4). The RFC number is auto-assigned by scanning rfcs/ for
the highest existing number + 1.
"""

from __future__ import annotations

import json
import os
import re
from datetime import date

import yaml

from _common import utc_now


INTEL_DIR = os.environ.get("INTEL_DIR", "evolution/intel")
DIGEST_YAML = os.path.join(INTEL_DIR, "weekly-digest.yaml")
SYNTHESIS_SUMMARY = os.path.join(INTEL_DIR, "synthesis-summary.json")
RFC_DIR = os.environ.get("RFC_DIR", "rfcs")
RFC_REPORT = os.path.join(INTEL_DIR, "rfc-draft-report.json")

NEW_RUNTIME_KEYWORDS = (
    "opus",
    "sonnet",
    "haiku",
    "gpt-",
    "gemini",
    "agent sdk",
    "cli",
    "runtime",
    "platform",
    "subagent",
    "antigravity",
    "codex",
)


def _load_digest() -> dict:
    if not os.path.exists(DIGEST_YAML):
        return {}
    with open(DIGEST_YAML) as f:
        return yaml.safe_load(f) or {}


def _load_summary() -> dict:
    if not os.path.exists(SYNTHESIS_SUMMARY):
        return {}
    with open(SYNTHESIS_SUMMARY) as f:
        return json.load(f) or {}


def _next_rfc_number() -> int:
    highest = 0
    if not os.path.isdir(RFC_DIR):
        return 1
    for name in os.listdir(RFC_DIR):
        m = re.match(r"^(\d{4})-", name)
        if m:
            highest = max(highest, int(m.group(1)))
    return highest + 1


def _should_draft(digest: dict) -> tuple[bool, list[str]]:
    reasons: list[str] = []

    releases = digest.get("vendor_releases") or []
    has_new_runtime = any(
        any(kw in (r.get("title") or "").lower() for kw in NEW_RUNTIME_KEYWORDS)
        for r in releases
    )
    if len(releases) >= 2 and has_new_runtime:
        reasons.append(
            f"{len(releases)} vendor releases, at least one new model/runtime"
        )

    shifts = digest.get("benchmark_shifts") or []
    if shifts:
        reasons.append(f"{len(shifts)} benchmark SOTA shift(s) ≥ 2.0pp")

    viral = digest.get("viral_hn") or []
    if len(viral) >= 3:
        reasons.append(f"{len(viral)} viral HN stories on tracked queries")

    return (bool(reasons), reasons)


def _render_rfc(
    rfc_number: int,
    today: str,
    digest: dict,
    reasons: list[str],
) -> tuple[str, str]:
    releases = digest.get("vendor_releases") or []
    shifts = digest.get("benchmark_shifts") or []
    viral = digest.get("viral_hn") or []

    if shifts:
        slug_seed = "benchmark-sota-shift"
        title = f"Benchmark SOTA Shift Response — {today}"
    elif any("new model" in r or "runtime" in r for r in reasons):
        vendors = sorted({r.get("vendor", "") for r in releases})
        vendor_str = "-".join(v for v in vendors if v) or "vendor"
        slug_seed = f"{vendor_str}-runtime-update"
        title = f"Vendor Runtime Update — {today}"
    else:
        slug_seed = "weekly-discourse-pressure"
        title = f"Weekly Discourse Pressure — {today}"

    filename = f"{rfc_number:04d}-weekly-intel-{slug_seed}-{today}.md"

    lines = [
        f"- RFC Number: {rfc_number:04d}",
        f"- Title: {title}",
        "- Agent Used: AIDE Weekly Intel (synthesize_research_note + draft_rfc_if_threshold)",
        "- Agent Model: single-vendor weekly intel pipeline (Phase E/F)",
        "- Research Method: automated multi-source scan (vendor RSS, HN Algolia, benchmark scrape) "
        "filtered by AIDE-relevance scorer",
        f"- Date: {today}",
        "- Status: Draft (auto-generated, awaits different-vendor co-sign per A2/A4)",
        "",
        "## Summary",
        "",
        "This RFC is an **auto-generated draft** raised by the AIDE Weekly Intel pipeline because the",
        "external sensor crossed at least one high-signal threshold this week. It does not propose a",
        "concrete methodology body change. It proposes that a different-vendor reviewing agent perform",
        "the deliberation described below and either promote this draft to a concrete change or close it",
        "with a written rejection reason.",
        "",
        "## Motivation",
        "",
        "Thresholds crossed this week:",
        "",
    ]
    for r in reasons:
        lines.append(f"- {r}")
    lines.append("")
    lines.append("Doing nothing in the face of a crossed threshold violates Axiom A3 (Empiricism): the")
    lines.append("sensor produced a quantitative signal and the methodology is required to respond,")
    lines.append("even if the response is an evidenced rejection.")
    lines.append("")

    lines.append("## Detailed Design")
    lines.append("")
    lines.append("The reviewing agent must answer, in order:")
    lines.append("")
    lines.append("1. Which `principle-metadata.yaml` numeric (if any) is moved by these signals?")
    lines.append("2. Which validity condition (VC*) or invalidation trigger (T*) is implicated?")
    lines.append("3. Is the supporting evidence official (vendor docs / benchmark leaderboard) or secondary?")
    lines.append("   Per the 2026-05-04 weekly synthesis, secondary trackers cannot calibrate metadata alone.")
    lines.append("4. If the answer to (1) is *none*, write a one-paragraph rejection citing the gap.")
    lines.append("")
    lines.append("Concrete proposed wording changes belong in this section after the reviewer responds.")
    lines.append("")

    lines.append("## Evidence")
    lines.append("")
    if releases:
        lines.append("### Vendor releases this week")
        lines.append("")
        for r in releases[:10]:
            lines.append(
                f"- **{r.get('vendor')}** · [{r.get('title')}]({r.get('url')}) — {r.get('published_at', '—')}"
            )
        if len(releases) > 10:
            lines.append(f"- … and {len(releases) - 10} more (see `evolution/intel/weekly-{today}.md`)")
        lines.append("")
    if shifts:
        lines.append("### Benchmark SOTA shifts")
        lines.append("")
        for s in shifts:
            lines.append(
                f"- **{s['benchmark']}**: {s['prior_pct']:.2f}% → {s['current_pct']:.2f}% "
                f"(Δ {s['delta_pp']:+.2f}pp)"
            )
        lines.append("")
    if viral:
        lines.append("### Viral HN coverage")
        lines.append("")
        for v in viral[:10]:
            lines.append(
                f"- [{v.get('title')}]({v.get('url')}) — {v.get('points')} pts · "
                f"query `{v.get('query')}` · {v.get('num_comments', 0)} comments"
            )
        lines.append("")

    lines.append("## Impact Assessment")
    lines.append("")
    lines.append("- **Existing principles**: not yet — promotion requires reviewer co-sign.")
    lines.append("- **Current adopters**: zero impact until this draft is accepted; the methodology body")
    lines.append("  (`docs/en/AIDE-METHODOLOGY.md`) is unchanged.")
    lines.append("- **Compatibility**: this draft only catalogs signals; it does not redefine axioms or")
    lines.append("  principle formulas. A1 (Reversibility) is preserved by trivial `git revert`.")
    lines.append("")

    lines.append("## Alternatives Considered")
    lines.append("")
    lines.append("- **Stay silent**: rejected — violates A3 by suppressing a measured signal.")
    lines.append("- **Auto-apply a metadata change**: rejected — violates A2/A4 because a single-vendor")
    lines.append("  weekly run cannot self-authorize a body change. That power belongs to the monthly")
    lines.append("  Evolution Engine, which the same digest already dispatches in parallel.")
    lines.append("- **Open a GitHub Issue instead**: the RFC path forces a structured response; Issues do not.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*Pipeline-generated on {utc_now().isoformat()} by `evolution/scripts/intel/draft_rfc_if_threshold.py`.*")
    lines.append("")

    return filename, "\n".join(lines)


def _update_rfc_readme(rfc_number: int, title: str, today: str, filename: str) -> bool:
    readme_path = os.path.join(RFC_DIR, "README.md")
    if not os.path.exists(readme_path):
        return False
    with open(readme_path) as f:
        contents = f.read()
    row = f"| [{rfc_number:04d}]({filename}) | {title} | Draft (auto) | {today} |"
    if row in contents:
        return False
    if "## Current RFCs" not in contents:
        return False
    # Append after the last table row.
    lines = contents.splitlines()
    last_row_idx = -1
    for i, line in enumerate(lines):
        if line.startswith("| [") and "](" in line and ".md)" in line:
            last_row_idx = i
    if last_row_idx == -1:
        return False
    lines.insert(last_row_idx + 1, row)
    with open(readme_path, "w") as f:
        f.write("\n".join(lines) + ("\n" if not contents.endswith("\n") else ""))
    return True


def main() -> None:
    digest = _load_digest()
    summary = _load_summary()

    should_draft, reasons = _should_draft(digest)
    report = {
        "generated_at": utc_now().isoformat(),
        "should_draft": should_draft,
        "reasons": reasons,
        "rfc_path": None,
        "rfc_number": None,
        "synthesis_present": bool(summary.get("wrote_synthesis")),
    }

    if not should_draft:
        print("Threshold not crossed — no RFC draft generated.")
        with open(RFC_REPORT, "w") as f:
            json.dump(report, f, indent=2)
        return

    rfc_number = _next_rfc_number()
    today = date.today().isoformat()
    filename, body = _render_rfc(rfc_number, today, digest, reasons)
    out_path = os.path.join(RFC_DIR, filename)
    os.makedirs(RFC_DIR, exist_ok=True)
    with open(out_path, "w") as f:
        f.write(body)

    title_line = next(
        (line for line in body.splitlines() if line.startswith("- Title:")), ""
    )
    title = title_line.replace("- Title:", "").strip() or "Untitled"
    _update_rfc_readme(rfc_number, title, today, filename)

    report["rfc_path"] = out_path
    report["rfc_number"] = rfc_number
    with open(RFC_REPORT, "w") as f:
        json.dump(report, f, indent=2)
    print(f"RFC draft -> {out_path} (RFC-{rfc_number:04d})")


if __name__ == "__main__":
    main()
