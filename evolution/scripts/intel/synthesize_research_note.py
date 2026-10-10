"""Weekly Intel — Phase E: Auto-synthesis to research/intel/.

Converts the machine-readable weekly digest into a research note that
catalogs only items aligned with AIDE's purpose: delegating software
engineering to autonomous agents, and the architecture / methodology
that lets models — not humans — drive the build loop.

The note lives under research/intel/ so that the human-curated
research/en/ (and the protected docs/en/AIDE-METHODOLOGY.md body) are
never touched by a single-vendor automated run. A1 (Reversibility) is
preserved because the file is additive — `git revert` cleanly removes
it — and A4 (No Single Authority) is preserved because the note is
explicitly marked as agent-drafted and awaiting different-vendor review
before any methodology body change.
"""

from __future__ import annotations

import os
from datetime import date

import yaml

from _common import utc_now


INTEL_DIR = os.environ.get("INTEL_DIR", "evolution/intel")
DIGEST_YAML = os.path.join(INTEL_DIR, "weekly-digest.yaml")
VENDOR_PATH = os.path.join(INTEL_DIR, "vendor-releases.yaml")
SOCIAL_PATH = os.path.join(INTEL_DIR, "social-signals.yaml")
BENCH_PATH = os.path.join(INTEL_DIR, "benchmarks.yaml")

OUTPUT_DIR = os.environ.get("RESEARCH_INTEL_DIR", "research/intel")
SUMMARY_OUTPUT = os.path.join(INTEL_DIR, "synthesis-summary.json")

# Relevance scoring — items that signal "agents doing the engineering" weigh
# heaviest. Generic AI / product news is filtered out so the synthesis stays
# faithful to AIDE's purpose.
HIGH_SIGNAL_TERMS = (
    "agent sdk",
    "agentic coding",
    "agentic engineering",
    "autonomous agent",
    "autonomous engineering",
    "claude code",
    "codex cli",
    "codex",
    "gemini cli",
    "antigravity",
    "subagent",
    "agent platform",
    "agent runtime",
    "agent topology",
    "agent control plane",
    "agent-led",
    "agent-native",
    "long-running agent",
    "multi-agent",
    "swe-bench",
    "terminal-bench",
    "webarena",
    "swe-rebench",
    "mcp ",
    "model context protocol",
    "tool use",
    "function calling",
    "context engineering",
    "context window",
    "context budget",
)

MEDIUM_SIGNAL_TERMS = (
    "agent",
    "claude",
    "gpt-",
    "opus",
    "sonnet",
    "haiku",
    "gemini",
    "release",
    "launch",
    "benchmark",
    "leaderboard",
    "model",
)

# Outright excludes — generic AI consumer news that pollutes the catalog
# without informing agent architecture.
NOISE_TERMS = (
    "consumer ai",
    "image generator",
    "voice mode demo",
    "wallpaper",
    "iphone",
    "android phone",
    "marketing",
)


def _load(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def _score(text: str) -> int:
    """Return AIDE-relevance score for a piece of text (title+summary)."""
    if not text:
        return 0
    t = text.lower()
    if any(n in t for n in NOISE_TERMS):
        return 0
    score = 0
    for term in HIGH_SIGNAL_TERMS:
        if term in t:
            score += 3
    for term in MEDIUM_SIGNAL_TERMS:
        if term in t:
            score += 1
    return score


def _collect_vendor_items(vendor_report: dict) -> list[dict]:
    items: list[dict] = []
    for vendor_key, wrapped in (vendor_report.get("vendors") or {}).items():
        data = (wrapped or {}).get("data") or {}
        for feed_name, entries in (data.get("feeds") or {}).items():
            if not isinstance(entries, list):
                continue
            for entry in entries:
                title = entry.get("title") or ""
                summary = entry.get("summary") or ""
                score = _score(f"{title} {summary}")
                if score <= 0:
                    continue
                items.append(
                    {
                        "kind": "vendor",
                        "vendor": vendor_key,
                        "feed": feed_name,
                        "title": title.strip(),
                        "url": entry.get("url"),
                        "published_at": entry.get("published_at"),
                        "summary": summary[:280],
                        "score": score,
                    }
                )
    return items


def _collect_social_items(social_report: dict) -> list[dict]:
    items: list[dict] = []
    channels = social_report.get("channels") or {}

    hn_queries = (
        ((channels.get("hackernews") or {}).get("data") or {}).get("queries") or {}
    )
    for query, hits in hn_queries.items():
        if not isinstance(hits, list):
            continue
        for hit in hits:
            if not isinstance(hit, dict) or "error" in hit:
                continue
            title = hit.get("title") or ""
            score = _score(f"{title} {query}")
            points = hit.get("points") or 0
            if score <= 0 and points < 100:
                continue
            items.append(
                {
                    "kind": "hn",
                    "query": query,
                    "title": title.strip(),
                    "url": hit.get("url"),
                    "points": points,
                    "num_comments": hit.get("num_comments"),
                    "published_at": hit.get("published_at"),
                    "score": score + min(points // 50, 5),
                }
            )

    blog_feeds = (
        ((channels.get("tech_blogs") or {}).get("data") or {}).get("feeds") or {}
    )
    for blog, entries in blog_feeds.items():
        if not isinstance(entries, list):
            continue
        for entry in entries:
            title = entry.get("title") or ""
            summary = entry.get("summary") or ""
            score = _score(f"{title} {summary}")
            if score <= 0:
                continue
            items.append(
                {
                    "kind": "blog",
                    "blog": blog,
                    "title": title.strip(),
                    "url": entry.get("url"),
                    "published_at": entry.get("published_at"),
                    "summary": summary[:280],
                    "score": score,
                }
            )

    x_accounts = (
        ((channels.get("x") or {}).get("data") or {}).get("accounts") or {}
    )
    for handle, entries in x_accounts.items():
        if not isinstance(entries, list):
            continue
        for entry in entries:
            title = entry.get("title") or ""
            summary = entry.get("summary") or ""
            score = _score(f"{title} {summary}")
            if score <= 0:
                continue
            items.append(
                {
                    "kind": "x",
                    "handle": handle,
                    "title": title.strip(),
                    "url": entry.get("url"),
                    "published_at": entry.get("published_at"),
                    "summary": summary[:280],
                    "score": score,
                }
            )
    return items


def _collect_benchmarks(bench_report: dict, digest: dict) -> tuple[list[dict], list[dict]]:
    shifts = digest.get("benchmark_shifts") or []
    snapshot: list[dict] = []
    for name, wrapped in (bench_report.get("benchmarks") or {}).items():
        data = (wrapped or {}).get("data") or {}
        if "variants" in data:
            for variant, payload in data["variants"].items():
                if not isinstance(payload, dict) or "error" in payload:
                    continue
                top = payload.get("top_score_pct")
                if top is None:
                    continue
                snapshot.append(
                    {
                        "benchmark": f"{name}/{variant}",
                        "top_score_pct": top,
                        "top_system": payload.get("top_system_raw"),
                        "url": payload.get("url"),
                    }
                )
        elif isinstance(data, dict) and data.get("top_score_pct") is not None:
            snapshot.append(
                {
                    "benchmark": name,
                    "top_score_pct": data.get("top_score_pct"),
                    "url": data.get("url"),
                }
            )
    return snapshot, shifts


def _dedupe(items: list[dict]) -> list[dict]:
    seen: set[str] = set()
    out: list[dict] = []
    for item in items:
        key = (item.get("url") or item.get("title") or "").strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def _render_markdown(
    today: str,
    vendor_items: list[dict],
    social_items: list[dict],
    benchmark_snapshot: list[dict],
    benchmark_shifts: list[dict],
    digest: dict,
) -> str:
    lookback = digest.get("source_health", {}).get("total", "?")
    ok = digest.get("source_health", {}).get("ok", "?")
    health_note = f"Source reach: {ok}/{lookback} feeds responded."

    lines = [
        f"# Weekly Intel Synthesis — {today}",
        "",
        "> **Agent-generated** (single-vendor draft, Phase E of weekly intel pipeline).",
        "> Per Axiom A2/A4, methodology body changes (`docs/en/AIDE-METHODOLOGY.md`,",
        "> `principle-metadata.yaml`, `axioms.yaml`) are **not** touched by this run.",
        "> A different-vendor reviewing agent must co-sign before any promotion.",
        ">",
        f"> Source digest: `evolution/intel/weekly-{today}.md` · {health_note}",
        "",
        "## AIDE-relevance lens",
        "",
        "Only items that change *how much engineering can be delegated to an autonomous agent*",
        "are catalogued here. Generic product / consumer-AI news is filtered out by the",
        "relevance scorer in `evolution/scripts/intel/synthesize_research_note.py`.",
        "",
    ]

    lines.append("## Vendor signals (Anthropic / OpenAI / Google — official)")
    lines.append("")
    if not vendor_items:
        lines.append("_No agent-architecture-relevant vendor releases this week._")
    else:
        for item in sorted(vendor_items, key=lambda x: x["score"], reverse=True)[:25]:
            published = item.get("published_at") or "—"
            lines.append(
                f"- **{item['vendor']}** · [{item['title']}]({item['url']}) "
                f"· score `{item['score']}` · {published}"
            )
            if item.get("summary"):
                lines.append(f"  - {item['summary']}")
    lines.append("")

    lines.append("## Community signals (HN / tech blogs / X)")
    lines.append("")
    if not social_items:
        lines.append("_No relevant community discourse this week._")
    else:
        for item in sorted(social_items, key=lambda x: x["score"], reverse=True)[:25]:
            kind = item["kind"]
            if kind == "hn":
                lines.append(
                    f"- **HN** · [{item['title']}]({item['url']}) — "
                    f"{item.get('points', 0)} pts · query `{item.get('query', '')}` "
                    f"· score `{item['score']}`"
                )
            elif kind == "blog":
                lines.append(
                    f"- **blog/{item['blog']}** · [{item['title']}]({item['url']}) "
                    f"· score `{item['score']}`"
                )
            elif kind == "x":
                lines.append(
                    f"- **x/@{item['handle']}** · [{item['title']}]({item['url']}) "
                    f"· score `{item['score']}`"
                )
    lines.append("")

    lines.append("## Benchmark posture (SWE-bench, Terminal-bench, WebArena, SWE-rebench)")
    lines.append("")
    if benchmark_snapshot:
        for snap in benchmark_snapshot:
            top = snap["top_score_pct"]
            sys = snap.get("top_system") or "—"
            lines.append(
                f"- `{snap['benchmark']}`: {top:.2f}% — top: {sys} "
                f"([source]({snap.get('url')}))"
            )
    else:
        lines.append("_Benchmark scrapers returned no usable snapshot this week._")
    lines.append("")
    if benchmark_shifts:
        lines.append("### SOTA shifts week-over-week")
        for s in benchmark_shifts:
            lines.append(
                f"- **{s['benchmark']}**: {s['prior_pct']:.2f}% → {s['current_pct']:.2f}% "
                f"(Δ {s['delta_pp']:+.2f}pp)"
            )
        lines.append("")

    lines.append("## Architectural reading for AIDE")
    lines.append("")
    lines.append(
        "The items above are raw signal. A different-vendor reviewing agent is expected to:"
    )
    lines.append("")
    lines.append("1. Identify which signals (if any) move a numeric in `principle-metadata.yaml`.")
    lines.append("2. Cite official, contamination-resistant evidence (vendor docs ≫ secondary tracker ≫ HN).")
    lines.append("3. Either co-sign an RFC under `rfcs/` or reject this week's draft with a written reason.")
    lines.append("")
    lines.append("Until that co-sign happens, the AIDE methodology body is unchanged.")
    lines.append("")

    return "\n".join(lines) + "\n"


def main() -> None:
    digest = _load(DIGEST_YAML)
    vendor = _load(VENDOR_PATH)
    social = _load(SOCIAL_PATH)
    bench = _load(BENCH_PATH)

    vendor_items = _dedupe(_collect_vendor_items(vendor))
    social_items = _dedupe(_collect_social_items(social))
    benchmark_snapshot, benchmark_shifts = _collect_benchmarks(bench, digest)

    today = date.today().isoformat()
    md = _render_markdown(
        today, vendor_items, social_items, benchmark_snapshot, benchmark_shifts, digest
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f"{today}-weekly-synthesis.md")

    total_items = len(vendor_items) + len(social_items) + len(benchmark_shifts)
    wrote = False
    if total_items > 0:
        with open(out_path, "w") as f:
            f.write(md)
        wrote = True
        print(f"Synthesis written -> {out_path} ({total_items} relevant items)")
    else:
        print("No AIDE-relevant items this week — no synthesis written.")

    summary = {
        "generated_at": utc_now().isoformat(),
        "date": today,
        "wrote_synthesis": wrote,
        "synthesis_path": out_path if wrote else None,
        "counts": {
            "vendor_items": len(vendor_items),
            "social_items": len(social_items),
            "benchmark_snapshot": len(benchmark_snapshot),
            "benchmark_shifts": len(benchmark_shifts),
        },
        "top_vendor_titles": [v["title"] for v in vendor_items[:5]],
        "top_social_titles": [s["title"] for s in social_items[:5]],
    }
    import json

    with open(SUMMARY_OUTPUT, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Synthesis summary -> {SUMMARY_OUTPUT}")


if __name__ == "__main__":
    main()
