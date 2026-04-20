"""Weekly Intel — Phase B: Social / community signals.

Scans public discourse on AI agents from sources AIDE cares about:
  * Hacker News (Algolia Search API) — story-level resonance
  * Tech blogs (RSS) — long-form engineering perspectives
  * X (via nitter RSS mirrors) — vendor/engineer announcements
  * Threads — public RSS for the same accounts when available

Focus: keywords that match AIDE's purpose — delegating development to
agents, autonomous engineering, agent architecture, benchmark moves.
"""

from __future__ import annotations

import os
import re
import urllib.parse
import xml.etree.ElementTree as ET

import yaml

from _common import http_get, lookback_cutoff, parse_rfc_date, safe_fetch, utc_now


OUTPUT_PATH = os.environ.get(
    "SOCIAL_OUTPUT_PATH", "evolution/intel/social-signals.yaml"
)

# Keywords aligned with AIDE's purpose: agent-first delegation, autonomous dev.
HN_QUERIES = [
    "claude code",
    "codex cli",
    "gemini cli",
    "ai agent autonomous",
    "agentic coding",
    "swe-bench",
    "terminal-bench",
    "agent sdk",
]

# Vendor + AI-dev voices whose signal tends to be high.
NITTER_HOSTS = [
    "nitter.net",
    "nitter.privacydev.net",
    "nitter.poast.org",
]
X_HANDLES = [
    "AnthropicAI",
    "OpenAI",
    "GoogleDeepMind",
    "alexalbert__",
    "sama",
    "gdb",
    "jeffdean",
    "swyx",
]

TECH_BLOGS = {
    "simonwillison": "https://simonwillison.net/atom/everything/",
    "latent_space": "https://www.latent.space/feed",
    "anthropic_eng": "https://www.anthropic.com/engineering/rss.xml",
    "openai_eng": "https://openai.com/blog/rss.xml",
}


def _strip_html(raw: str) -> str:
    text = re.sub(r"<[^>]+>", " ", raw or "")
    return re.sub(r"\s+", " ", text).strip()


def _parse_feed(xml_text: str, source_url: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    items = []
    for node in root.findall(".//a:entry", ns) or root.findall(".//item"):
        title = node.find("a:title", ns) or node.find("title")
        link = node.find("a:link", ns) or node.find("link")
        date = (
            node.find("a:updated", ns)
            or node.find("a:published", ns)
            or node.find("pubDate")
        )
        summary = (
            node.find("a:summary", ns)
            or node.find("a:content", ns)
            or node.find("description")
        )
        href = None
        if link is not None:
            href = link.get("href") or (link.text or "").strip()
        items.append(
            {
                "title": (title.text or "").strip() if title is not None else "",
                "url": href or source_url,
                "published_at": (date.text or "").strip() if date is not None else None,
                "summary": _strip_html(summary.text) if summary is not None else "",
            }
        )
    cutoff = lookback_cutoff()
    return [
        i for i in items
        if parse_rfc_date(i.get("published_at")) is None
        or parse_rfc_date(i["published_at"]) >= cutoff
    ]


def fetch_hn() -> dict:
    """Hacker News via Algolia Search API — last 7 days, sorted by date."""
    cutoff = int(lookback_cutoff().timestamp())
    results: dict[str, list[dict]] = {}
    for query in HN_QUERIES:
        q = urllib.parse.quote_plus(query)
        url = (
            "https://hn.algolia.com/api/v1/search_by_date"
            f"?query={q}&numericFilters=created_at_i>{cutoff}&hitsPerPage=20"
        )
        try:
            data = http_get(url, accept="application/json").json()
            hits = [
                {
                    "title": h.get("title") or h.get("story_title"),
                    "url": h.get("url")
                    or f"https://news.ycombinator.com/item?id={h.get('objectID')}",
                    "points": h.get("points"),
                    "num_comments": h.get("num_comments"),
                    "published_at": h.get("created_at"),
                    "author": h.get("author"),
                }
                for h in data.get("hits", [])
            ]
            results[query] = hits
        except Exception as exc:
            results[query] = [{"error": f"{type(exc).__name__}: {exc}"}]
    return {"source": "hackernews", "queries": results}


def fetch_tech_blogs() -> dict:
    feeds: dict[str, list[dict] | dict] = {}
    for name, url in TECH_BLOGS.items():
        try:
            feeds[name] = _parse_feed(http_get(url).text, url)
        except Exception as exc:
            feeds[name] = {"error": f"{type(exc).__name__}: {exc}", "url": url}
    return {"source": "tech_blogs", "feeds": feeds}


def fetch_x_via_nitter() -> dict:
    """Best-effort X scrape via nitter RSS. Marks failure cleanly."""
    accounts: dict[str, list[dict] | dict] = {}
    for handle in X_HANDLES:
        last_error = None
        for host in NITTER_HOSTS:
            url = f"https://{host}/{handle}/rss"
            try:
                accounts[handle] = _parse_feed(http_get(url).text, url)
                last_error = None
                break
            except Exception as exc:
                last_error = f"{host}: {type(exc).__name__}: {exc}"
        if last_error:
            accounts[handle] = {
                "error": "all nitter mirrors unreachable",
                "last_error": last_error,
            }
    return {"source": "x_via_nitter", "accounts": accounts}


def fetch_threads() -> dict:
    """Threads lacks a stable public RSS. Placeholder endpoint, degrades cleanly."""
    # Threads profiles expose JSON via ?__a=1 style endpoints only with auth.
    # We record the gap explicitly — A5 Self-Observability.
    return {
        "source": "threads",
        "status": "not_collected",
        "reason": "No stable public API for non-auth scraping as of 2026-04.",
    }


def main() -> None:
    report = {
        "schema_version": "1.0",
        "scan_timestamp": utc_now().isoformat(),
        "lookback_days": int(os.environ.get("INTEL_LOOKBACK_DAYS", "7")),
        "channels": {
            "hackernews": safe_fetch("hackernews", fetch_hn),
            "tech_blogs": safe_fetch("tech_blogs", fetch_tech_blogs),
            "x": safe_fetch("x", fetch_x_via_nitter),
            "threads": safe_fetch("threads", fetch_threads),
        },
    }
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        yaml.dump(report, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    print(f"Social signal scan complete -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
