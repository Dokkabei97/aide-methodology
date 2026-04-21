"""Weekly Intel — Phase A: Vendor release scanning.

Polls the official release/changelog feeds of the three major model
vendors. Everything here is the public web; no auth required. Each
source is wrapped in safe_fetch so a single outage never blocks the
pipeline.
"""

from __future__ import annotations

import os
import re
import xml.etree.ElementTree as ET

import yaml

from _common import http_get, recent_only, safe_fetch, utc_now


OUTPUT_PATH = os.environ.get(
    "VENDOR_OUTPUT_PATH", "evolution/intel/vendor-releases.yaml"
)


def _strip_html(raw: str) -> str:
    text = re.sub(r"<[^>]+>", " ", raw or "")
    return re.sub(r"\s+", " ", text).strip()


def _parse_atom(xml_text: str, source_url: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    ns = {"a": "http://www.w3.org/2005/Atom", "r": "http://purl.org/rss/1.0/"}
    entries = []
    for entry in root.findall(".//a:entry", ns) or root.findall(".//item"):
        title_el = entry.find("a:title", ns) or entry.find("title")
        link_el = entry.find("a:link", ns) or entry.find("link")
        date_el = (
            entry.find("a:updated", ns)
            or entry.find("a:published", ns)
            or entry.find("pubDate")
        )
        summary_el = (
            entry.find("a:summary", ns)
            or entry.find("a:content", ns)
            or entry.find("description")
        )
        href = None
        if link_el is not None:
            href = link_el.get("href") or (link_el.text or "").strip()
        entries.append(
            {
                "title": (title_el.text or "").strip() if title_el is not None else "",
                "url": href or source_url,
                "published_at": (date_el.text or "").strip() if date_el is not None else None,
                "summary": _strip_html(summary_el.text) if summary_el is not None else "",
            }
        )
    return recent_only(entries)


def fetch_anthropic() -> dict:
    urls = {
        "news": "https://www.anthropic.com/news/rss.xml",
        "release_notes": "https://docs.claude.com/en/release-notes.xml",
    }
    feeds = {}
    for name, url in urls.items():
        try:
            feeds[name] = _parse_atom(http_get(url, accept="application/atom+xml").text, url)
        except Exception as exc:
            feeds[name] = {"error": f"{type(exc).__name__}: {exc}", "url": url}
    return {"vendor": "Anthropic", "feeds": feeds}


def fetch_openai() -> dict:
    urls = {
        "news": "https://openai.com/news/rss.xml",
        "api_changelog": "https://platform.openai.com/docs/changelog.rss",
    }
    feeds = {}
    for name, url in urls.items():
        try:
            feeds[name] = _parse_atom(http_get(url, accept="application/rss+xml").text, url)
        except Exception as exc:
            feeds[name] = {"error": f"{type(exc).__name__}: {exc}", "url": url}
    return {"vendor": "OpenAI", "feeds": feeds}


def fetch_google() -> dict:
    urls = {
        "blog_ai": "https://blog.google/technology/ai/rss/",
        "developers_blog": "https://developers.googleblog.com/feeds/posts/default",
    }
    feeds = {}
    for name, url in urls.items():
        try:
            feeds[name] = _parse_atom(http_get(url, accept="application/atom+xml").text, url)
        except Exception as exc:
            feeds[name] = {"error": f"{type(exc).__name__}: {exc}", "url": url}
    return {"vendor": "Google", "feeds": feeds}


def main() -> None:
    report = {
        "schema_version": "1.0",
        "scan_timestamp": utc_now().isoformat(),
        "lookback_days": int(os.environ.get("INTEL_LOOKBACK_DAYS", "7")),
        "vendors": {
            "anthropic": safe_fetch("anthropic", fetch_anthropic),
            "openai": safe_fetch("openai", fetch_openai),
            "google": safe_fetch("google", fetch_google),
        },
    }
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        yaml.dump(report, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    print(f"Vendor release scan complete -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
