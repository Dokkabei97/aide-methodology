"""Weekly Intel — Phase G: Append weekly entry to docs/{en,ko}/recent-intel.md.

The protected methodology body (`docs/en/AIDE-METHODOLOGY.md`) is never
touched by this run. Instead, a side-channel catalog document at
`docs/en/recent-intel.md` and `docs/ko/recent-intel.md` keeps a
human-discoverable trail of every weekly run, with links to:
  * the raw digest under `evolution/intel/weekly-YYYY-MM-DD.md`
  * the synthesized note under `research/intel/YYYY-MM-DD-weekly-synthesis.md`
  * any auto-generated RFC draft

The file is *prepend-then-append* style: newest entries at top, keeps
the index page short and scannable. The catalog itself is not part of
AIDE's methodology body — it is documentation about the sensor.
"""

from __future__ import annotations

import json
import os
from datetime import date

import yaml


INTEL_DIR = os.environ.get("INTEL_DIR", "evolution/intel")
DIGEST_YAML = os.path.join(INTEL_DIR, "weekly-digest.yaml")
SYNTHESIS_SUMMARY = os.path.join(INTEL_DIR, "synthesis-summary.json")
RFC_REPORT = os.path.join(INTEL_DIR, "rfc-draft-report.json")

DOCS_PATHS = {
    "en": "docs/en/recent-intel.md",
    "ko": "docs/ko/recent-intel.md",
}

EN_HEADER = """# Recent Intel — Weekly Pipeline Log

> **Catalog only.** This page lists every run of the AIDE Weekly Intel pipeline. It is
> *not* part of the AIDE methodology body. The methodology body lives in
> `docs/en/AIDE-METHODOLOGY.md` and is changed only via the RFC process with
> different-vendor co-sign (Axioms A2 / A4).
>
> Pipeline source: `.github/workflows/aide-weekly-intel.yml`.
> Schedule: every Monday 00:00 UTC (09:00 KST).

## Entries (newest first)
"""

KO_HEADER = """# 주간 인텔 — 파이프라인 실행 로그

> **카탈로그 전용.** 이 페이지는 AIDE 주간 인텔 파이프라인의 매 실행을 기록합니다.
> AIDE 방법론 본문이 아닙니다. 방법론 본문은 `docs/ko/AIDE-METHODOLOGY.md`이며,
> 변경은 다른 벤더 에이전트의 공동 서명을 거친 RFC 프로세스를 통해서만 가능합니다 (공리 A2 / A4).
>
> 파이프라인 소스: `.github/workflows/aide-weekly-intel.yml`.
> 스케줄: 매주 월요일 00:00 UTC (09:00 KST).

## 실행 기록 (최신순)
"""

ENTRY_MARK = "<!-- entry: {date} -->"


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


def _build_entry(lang: str, today: str, digest: dict, synthesis: dict, rfc: dict) -> str:
    health = digest.get("source_health") or {}
    ok = health.get("ok", 0)
    total = health.get("total", 0)
    dispatch = (digest.get("dispatch") or {}).get("should_dispatch", False)
    counts = synthesis.get("counts") or {}
    rfc_number = rfc.get("rfc_number")
    rfc_path = rfc.get("rfc_path")

    digest_link = f"../../evolution/intel/weekly-{today}.md"
    synthesis_link = (
        f"../../research/intel/{today}-weekly-synthesis.md"
        if synthesis.get("wrote_synthesis")
        else None
    )
    rfc_link = (
        f"../../{rfc_path}" if rfc_path else None
    )

    if lang == "en":
        bullet_synthesis = (
            f"- Synthesis: [{today}-weekly-synthesis.md]({synthesis_link})"
            if synthesis_link
            else "- Synthesis: _no AIDE-relevant items this week_"
        )
        bullet_rfc = (
            f"- RFC draft: [RFC-{rfc_number:04d}]({rfc_link})"
            if rfc_link
            else "- RFC draft: _threshold not crossed_"
        )
        section = [
            ENTRY_MARK.format(date=today),
            f"### {today}",
            "",
            f"- Digest: [weekly-{today}.md]({digest_link}) — source reach {ok}/{total}",
            bullet_synthesis,
            bullet_rfc,
            f"- Evolution Engine dispatched: **{'yes' if dispatch else 'no'}**",
            f"- Items kept by relevance filter: "
            f"vendor={counts.get('vendor_items', 0)}, "
            f"social={counts.get('social_items', 0)}, "
            f"benchmark_shifts={counts.get('benchmark_shifts', 0)}",
            "",
        ]
    else:
        bullet_synthesis = (
            f"- 합성 노트: [{today}-weekly-synthesis.md]({synthesis_link})"
            if synthesis_link
            else "- 합성 노트: _이번 주 AIDE 관련성 항목 없음_"
        )
        bullet_rfc = (
            f"- RFC 초안: [RFC-{rfc_number:04d}]({rfc_link})"
            if rfc_link
            else "- RFC 초안: _임계치 미달_"
        )
        section = [
            ENTRY_MARK.format(date=today),
            f"### {today}",
            "",
            f"- 다이제스트: [weekly-{today}.md]({digest_link}) — 소스 도달률 {ok}/{total}",
            bullet_synthesis,
            bullet_rfc,
            f"- Evolution Engine 디스패치: **{'예' if dispatch else '아니오'}**",
            f"- 관련성 필터 통과 항목 수: "
            f"vendor={counts.get('vendor_items', 0)}, "
            f"social={counts.get('social_items', 0)}, "
            f"benchmark_shifts={counts.get('benchmark_shifts', 0)}",
            "",
        ]
    return "\n".join(section) + "\n"


def _write_with_entry(path: str, header: str, entry: str, today: str) -> None:
    mark = ENTRY_MARK.format(date=today)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(header.rstrip() + "\n\n" + entry)
        return
    with open(path) as f:
        contents = f.read()
    if mark in contents:
        print(f"Entry for {today} already present in {path}; skipping.")
        return
    if "## Entries" in contents or "## 실행 기록" in contents:
        marker = "## Entries (newest first)" if "## Entries" in contents else "## 실행 기록 (최신순)"
        idx = contents.find(marker)
        if idx == -1:
            new = contents.rstrip() + "\n\n" + entry
        else:
            split_at = contents.find("\n", idx) + 1
            head = contents[:split_at]
            tail = contents[split_at:]
            new = head + "\n" + entry + tail
    else:
        new = header.rstrip() + "\n\n" + entry + contents
    with open(path, "w") as f:
        f.write(new)


def main() -> None:
    today = date.today().isoformat()
    digest = _load_yaml(DIGEST_YAML)
    synthesis = _load_json(SYNTHESIS_SUMMARY)
    rfc = _load_json(RFC_REPORT)

    en_entry = _build_entry("en", today, digest, synthesis, rfc)
    ko_entry = _build_entry("ko", today, digest, synthesis, rfc)

    _write_with_entry(DOCS_PATHS["en"], EN_HEADER, en_entry, today)
    _write_with_entry(DOCS_PATHS["ko"], KO_HEADER, ko_entry, today)
    print(f"docs/{{en,ko}}/recent-intel.md updated for {today}")


if __name__ == "__main__":
    main()
