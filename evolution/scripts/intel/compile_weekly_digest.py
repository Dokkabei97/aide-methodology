"""Weekly Intel — Phase D: Digest compilation & evolution dispatch.

Merges the three fetcher outputs into:
  1. A machine-readable YAML snapshot   (evolution/intel/weekly-digest.yaml)
  2. A human-readable Markdown digest    (evolution/intel/weekly-YYYY-MM-DD.md)
  3. A dispatch decision flag            (evolution/intel/dispatch.json)

The dispatch decision is what makes the loop "agent-autonomous": when
signal thresholds are crossed (new vendor model, >2pp SWE-bench SOTA
shift, >=3 viral HN stories on the same topic), we emit a
repository_dispatch payload so the monthly Evolution Engine wakes up
and re-deliberates.
"""

from __future__ import annotations

import json
import os
from datetime import date

import yaml

from _common import utc_now


INTEL_DIR = os.environ.get("INTEL_DIR", "evolution/intel")
VENDOR_PATH = os.path.join(INTEL_DIR, "vendor-releases.yaml")
SOCIAL_PATH = os.path.join(INTEL_DIR, "social-signals.yaml")
BENCH_PATH = os.path.join(INTEL_DIR, "benchmarks.yaml")

DIGEST_YAML = os.path.join(INTEL_DIR, "weekly-digest.yaml")
DISPATCH_FILE = os.path.join(INTEL_DIR, "dispatch.json")

HN_VIRAL_POINTS = 150
SWE_BENCH_DELTA_PP = 2.0

MODEL_KEYWORDS = [
    "claude",
    "opus",
    "sonnet",
    "haiku",
    "gpt-",
    "codex",
    "gemini",
    "agent",
    "release",
    "launch",
]


def _load(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def _iter_vendor_entries(vendor_report: dict):
    vendors = (vendor_report.get("vendors") or {})
    for vendor_key, wrapped in vendors.items():
        data = (wrapped or {}).get("data") or {}
        feeds = data.get("feeds") or {}
        for feed_name, entries in feeds.items():
            if isinstance(entries, list):
                for entry in entries:
                    yield vendor_key, feed_name, entry


def _detect_vendor_releases(vendor_report: dict) -> list[dict]:
    hits = []
    for vendor, feed, entry in _iter_vendor_entries(vendor_report):
        title = (entry.get("title") or "").lower()
        if any(k in title for k in MODEL_KEYWORDS):
            hits.append(
                {
                    "vendor": vendor,
                    "feed": feed,
                    "title": entry.get("title"),
                    "url": entry.get("url"),
                    "published_at": entry.get("published_at"),
                }
            )
    return hits


def _detect_viral_hn(social_report: dict) -> list[dict]:
    hn = (
        social_report.get("channels", {})
        .get("hackernews", {})
        .get("data", {})
        .get("queries", {})
    )
    viral = []
    for query, hits in hn.items():
        if not isinstance(hits, list):
            continue
        for hit in hits:
            points = hit.get("points") or 0
            if isinstance(points, int) and points >= HN_VIRAL_POINTS:
                viral.append(
                    {
                        "query": query,
                        "title": hit.get("title"),
                        "url": hit.get("url"),
                        "points": points,
                        "num_comments": hit.get("num_comments"),
                    }
                )
    return viral


def _audit_fetcher_health(
    vendor_report: dict, social_report: dict, bench_report: dict
) -> dict:
    """Walk every fetched feed and tag it ok / error so A5 stays honest.

    A weekly run where every source 403s must look different from a
    genuinely quiet week — otherwise the "no signal" path silently
    masks an upstream outage and the dispatch decision becomes a lie.
    """
    failures: list[dict] = []
    ok_count = 0

    def _record(scope: str, name: str, payload):
        nonlocal ok_count
        if isinstance(payload, dict) and "error" in payload:
            failures.append({"scope": scope, "name": name, "error": payload["error"]})
        elif isinstance(payload, list) and payload and isinstance(payload[0], dict) and "error" in payload[0]:
            failures.append({"scope": scope, "name": name, "error": payload[0]["error"]})
        else:
            ok_count += 1

    for vendor_key, wrapped in (vendor_report.get("vendors") or {}).items():
        feeds = ((wrapped or {}).get("data") or {}).get("feeds") or {}
        for feed_name, payload in feeds.items():
            _record(f"vendor:{vendor_key}", feed_name, payload)

    channels = social_report.get("channels") or {}
    hn_queries = (
        ((channels.get("hackernews") or {}).get("data") or {}).get("queries") or {}
    )
    for q, payload in hn_queries.items():
        _record("hn", q, payload)
    blog_feeds = (
        ((channels.get("tech_blogs") or {}).get("data") or {}).get("feeds") or {}
    )
    for name, payload in blog_feeds.items():
        _record(f"blog:{name}", "feed", payload)
    x_accounts = (
        ((channels.get("x") or {}).get("data") or {}).get("accounts") or {}
    )
    for handle, payload in x_accounts.items():
        _record(f"x:{handle}", "feed", payload)

    for name, wrapped in (bench_report.get("benchmarks") or {}).items():
        data = (wrapped or {}).get("data") or {}
        if "variants" in data:
            for variant_name, payload in data["variants"].items():
                _record(f"bench:{name}", variant_name, payload)
        else:
            _record(f"bench:{name}", "leaderboard", data)

    total = ok_count + len(failures)
    return {
        "ok": ok_count,
        "failed": len(failures),
        "total": total,
        "failures": failures,
        "all_failed": total > 0 and ok_count == 0,
    }


def _detect_benchmark_shift(bench_report: dict) -> list[dict]:
    shifts = []
    benchmarks = bench_report.get("benchmarks", {})
    history_path = os.path.join(INTEL_DIR, "benchmark-history.yaml")
    history = _load(history_path)
    latest = {}

    def _top(wrapped: dict) -> float | None:
        d = (wrapped or {}).get("data") or {}
        if "variants" in d:
            verified = d["variants"].get("verified") or {}
            return verified.get("top_score_pct")
        return d.get("top_score_pct")

    for name, wrapped in benchmarks.items():
        top = _top(wrapped)
        if top is None:
            continue
        latest[name] = top
        prior = history.get(name)
        if prior is not None and abs(top - prior) >= SWE_BENCH_DELTA_PP:
            shifts.append(
                {"benchmark": name, "prior_pct": prior, "current_pct": top, "delta_pp": top - prior}
            )

    if latest:
        merged = {**history, **latest}
        with open(history_path, "w") as f:
            yaml.dump(merged, f, default_flow_style=False, sort_keys=True)
    return shifts


def _render_markdown(payload: dict) -> str:
    today = date.today().isoformat()
    lines = [f"# AIDE Weekly Intel — {today}", ""]
    lines.append("## Vendor releases (keyword-matched)")
    if not payload["vendor_releases"]:
        lines.append("_No matching releases this week._")
    for hit in payload["vendor_releases"]:
        lines.append(f"- **{hit['vendor']}** · [{hit['title']}]({hit['url']}) — {hit.get('published_at','')}")
    lines.append("")
    lines.append("## Viral HN stories (>= {} points)".format(HN_VIRAL_POINTS))
    if not payload["viral_hn"]:
        lines.append("_No viral stories on tracked queries._")
    for hit in payload["viral_hn"]:
        lines.append(
            f"- [{hit['title']}]({hit['url']}) — {hit['points']} pts · "
            f"query `{hit['query']}` · {hit.get('num_comments', 0)} comments"
        )
    lines.append("")
    lines.append("## Benchmark SOTA shifts (>= {:.1f}pp)".format(SWE_BENCH_DELTA_PP))
    if not payload["benchmark_shifts"]:
        lines.append("_No material shift detected._")
    for s in payload["benchmark_shifts"]:
        lines.append(
            f"- **{s['benchmark']}**: {s['prior_pct']:.2f}% → {s['current_pct']:.2f}% "
            f"(Δ {s['delta_pp']:+.2f}pp)"
        )
    lines.append("")
    lines.append("## Source health")
    health = payload.get("source_health") or {}
    total = health.get("total", 0)
    ok = health.get("ok", 0)
    failed = health.get("failed", 0)
    lines.append(f"- Sources reached: **{ok}/{total}** (failed: {failed})")
    if health.get("all_failed"):
        lines.append(
            "- **WARNING**: every external source failed this week. The empty signal "
            "above reflects an outage, not a quiet week. Dispatch suppressed for safety."
        )
    elif failed:
        sample = health.get("failures", [])[:5]
        for f in sample:
            lines.append(f"  - `{f['scope']}/{f['name']}` — {f['error']}")
        if failed > len(sample):
            lines.append(f"  - … and {failed - len(sample)} more")
    lines.append("")
    lines.append("## Dispatch decision")
    lines.append(
        f"- Evolution Engine dispatch: **{'YES' if payload['dispatch']['should_dispatch'] else 'no'}**"
    )
    lines.append(f"- Reasons: {', '.join(payload['dispatch']['reasons']) or 'none'}")
    return "\n".join(lines) + "\n"


def main() -> None:
    vendor = _load(VENDOR_PATH)
    social = _load(SOCIAL_PATH)
    bench = _load(BENCH_PATH)

    vendor_releases = _detect_vendor_releases(vendor)
    viral_hn = _detect_viral_hn(social)
    benchmark_shifts = _detect_benchmark_shift(bench)
    source_health = _audit_fetcher_health(vendor, social, bench)

    reasons = []
    if vendor_releases:
        reasons.append(f"{len(vendor_releases)} vendor release candidates")
    if len(viral_hn) >= 3:
        reasons.append(f"{len(viral_hn)} viral HN stories")
    if benchmark_shifts:
        reasons.append(f"{len(benchmark_shifts)} benchmark SOTA shifts")

    suppress_dispatch = source_health.get("all_failed", False)
    dispatch = {
        "should_dispatch": bool(reasons) and not suppress_dispatch,
        "reasons": reasons if not suppress_dispatch else ["suppressed: all sources failed"],
        "event_type": "weekly_intel_signal",
        "client_payload": {
            "vendor_release_count": len(vendor_releases),
            "viral_hn_count": len(viral_hn),
            "benchmark_shift_count": len(benchmark_shifts),
            "source_health": source_health,
        },
    }

    payload = {
        "schema_version": "1.0",
        "generated_at": utc_now().isoformat(),
        "vendor_releases": vendor_releases,
        "viral_hn": viral_hn,
        "benchmark_shifts": benchmark_shifts,
        "source_health": source_health,
        "dispatch": dispatch,
    }

    os.makedirs(INTEL_DIR, exist_ok=True)
    with open(DIGEST_YAML, "w") as f:
        yaml.dump(payload, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    md_path = os.path.join(INTEL_DIR, f"weekly-{date.today().isoformat()}.md")
    with open(md_path, "w") as f:
        f.write(_render_markdown(payload))

    with open(DISPATCH_FILE, "w") as f:
        json.dump(dispatch, f, indent=2)

    print(f"Digest -> {DIGEST_YAML}")
    print(f"Markdown -> {md_path}")
    print(f"Dispatch -> {DISPATCH_FILE} (should_dispatch={dispatch['should_dispatch']})")


if __name__ == "__main__":
    main()
