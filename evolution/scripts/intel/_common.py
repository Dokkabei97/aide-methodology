"""Shared helpers for weekly intel fetchers.

Every fetcher must degrade gracefully: if a source is unreachable, record
the error in the output and continue. Never raise out of main().
"""

from __future__ import annotations

import os
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Callable

import requests


USER_AGENT = (
    "AIDE-Weekly-Intel/1.0 (+https://github.com/Dokkabei97/aide-methodology)"
)
DEFAULT_TIMEOUT = 15
LOOKBACK_DAYS = int(os.environ.get("INTEL_LOOKBACK_DAYS", "7"))


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def lookback_cutoff() -> datetime:
    return utc_now() - timedelta(days=LOOKBACK_DAYS)


def http_get(url: str, *, accept: str = "*/*", timeout: int = DEFAULT_TIMEOUT) -> requests.Response:
    headers = {"User-Agent": USER_AGENT, "Accept": accept}
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp


def safe_fetch(label: str, fn: Callable[[], Any]) -> dict:
    """Wrap a fetch function so partial failure never aborts the pipeline."""
    started = utc_now().isoformat()
    for attempt in range(3):
        try:
            data = fn()
            return {
                "source": label,
                "status": "ok",
                "started_at": started,
                "finished_at": utc_now().isoformat(),
                "data": data,
            }
        except Exception as exc:
            if attempt == 2:
                return {
                    "source": label,
                    "status": "error",
                    "started_at": started,
                    "finished_at": utc_now().isoformat(),
                    "error": f"{type(exc).__name__}: {exc}",
                }
            time.sleep(1.5 * (attempt + 1))
    return {"source": label, "status": "error", "error": "unreachable"}


def parse_rfc_date(raw: str | None) -> datetime | None:
    if not raw:
        return None
    for fmt in (
        "%a, %d %b %Y %H:%M:%S %Z",
        "%a, %d %b %Y %H:%M:%S %z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d",
    ):
        try:
            dt = datetime.strptime(raw.strip(), fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    return None


def recent_only(items: list[dict], date_key: str = "published_at") -> list[dict]:
    cutoff = lookback_cutoff()
    out = []
    for item in items:
        dt = parse_rfc_date(item.get(date_key))
        if dt is None or dt >= cutoff:
            out.append(item)
    return out
