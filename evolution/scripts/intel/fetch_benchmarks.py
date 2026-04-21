"""Weekly Intel — Phase C: Benchmark leaderboard scanning.

Pulls the latest leaderboard snapshot of benchmarks that AIDE tracks as
proxies for agent-led development capability:
  * SWE-bench (Verified, Lite, Full)
  * Terminal-bench
  * WebArena
  * SWE-rebench (multi-file real-world PRs)

The goal is not to measure our own agents, but to detect when the SOTA
moves — which feeds into principle-metadata calibration.
"""

from __future__ import annotations

import os
import re

import yaml

from _common import http_get, safe_fetch, utc_now


OUTPUT_PATH = os.environ.get(
    "BENCH_OUTPUT_PATH", "evolution/intel/benchmarks.yaml"
)


def _first_match(pattern: str, text: str) -> str | None:
    m = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return m.group(1).strip() if m else None


def fetch_swe_bench() -> dict:
    """Scrape public SWE-bench landing pages for top score."""
    results: dict[str, dict] = {}
    for variant, url in {
        "verified": "https://www.swebench.com/verified.html",
        "lite": "https://www.swebench.com/lite.html",
        "full": "https://www.swebench.com/",
    }.items():
        try:
            html = http_get(url, accept="text/html").text
            top_score = _first_match(r"(\d{1,3}\.\d{1,2})\s*%", html)
            top_system = _first_match(
                r"<tr[^>]*>.*?<td[^>]*>\s*1\s*</td>.*?<td[^>]*>(.*?)</td>", html
            )
            results[variant] = {
                "url": url,
                "top_score_pct": float(top_score) if top_score else None,
                "top_system_raw": re.sub(r"<[^>]+>", " ", top_system or "").strip() or None,
            }
        except Exception as exc:
            results[variant] = {"url": url, "error": f"{type(exc).__name__}: {exc}"}
    return {"benchmark": "SWE-bench", "variants": results}


def fetch_terminal_bench() -> dict:
    url = "https://www.tbench.ai/leaderboard"
    try:
        html = http_get(url, accept="text/html").text
        top_score = _first_match(r"(\d{1,3}\.\d{1,2})\s*%", html)
        return {
            "benchmark": "Terminal-bench",
            "url": url,
            "top_score_pct": float(top_score) if top_score else None,
        }
    except Exception as exc:
        return {"benchmark": "Terminal-bench", "url": url, "error": f"{type(exc).__name__}: {exc}"}


def fetch_webarena() -> dict:
    url = "https://webarena.dev/"
    try:
        html = http_get(url, accept="text/html").text
        top_score = _first_match(r"(\d{1,3}\.\d{1,2})\s*%", html)
        return {
            "benchmark": "WebArena",
            "url": url,
            "top_score_pct": float(top_score) if top_score else None,
        }
    except Exception as exc:
        return {"benchmark": "WebArena", "url": url, "error": f"{type(exc).__name__}: {exc}"}


def fetch_swe_rebench() -> dict:
    url = "https://swe-rebench.com/leaderboard"
    try:
        html = http_get(url, accept="text/html").text
        top_score = _first_match(r"(\d{1,3}\.\d{1,2})\s*%", html)
        return {
            "benchmark": "SWE-rebench",
            "url": url,
            "top_score_pct": float(top_score) if top_score else None,
        }
    except Exception as exc:
        return {"benchmark": "SWE-rebench", "url": url, "error": f"{type(exc).__name__}: {exc}"}


def main() -> None:
    report = {
        "schema_version": "1.0",
        "scan_timestamp": utc_now().isoformat(),
        "benchmarks": {
            "swe_bench": safe_fetch("swe_bench", fetch_swe_bench),
            "terminal_bench": safe_fetch("terminal_bench", fetch_terminal_bench),
            "webarena": safe_fetch("webarena", fetch_webarena),
            "swe_rebench": safe_fetch("swe_rebench", fetch_swe_rebench),
        },
    }
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        yaml.dump(report, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    print(f"Benchmark scan complete -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
