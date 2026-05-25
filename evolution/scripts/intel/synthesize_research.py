"""Weekly Intel — Phase E: Research synthesis drafter.

Reads the machine-collected intel (vendor releases + social signals +
benchmarks + weekly digest) and writes an English + Korean weekly
synthesis draft into ``research/{en,ko}/{YYYY-MM-DD}-weekly-synthesis.md``.

Design choices (why this exists separately from Phase D):
  * Phase D writes a *raw digest* under ``evolution/intel/`` — the
    permanent audit trail of what the sensors saw. It is signal, not
    judgement.
  * Phase E writes a *synthesis draft* under ``research/`` — a structured
    proposal for architectural claims, candidate principle-metadata
    edits, and reviewer questions. It is judgement, but explicitly
    labelled as a single-vendor draft awaiting different-vendor review
    per Axioms A2 / A4.

The drafter is deterministic. It does not call an LLM API. Its job is
to set the table so a different-vendor reviewer agent (or a human
curator) can challenge the claims, not to settle them.
"""

from __future__ import annotations

import os
import re
from collections import defaultdict
from datetime import date, timedelta

import yaml

from _common import utc_now


INTEL_DIR = os.environ.get("INTEL_DIR", "evolution/intel")
RESEARCH_DIR = os.environ.get("RESEARCH_DIR", "research")
AUTHOR_MODEL = os.environ.get("SYNTHESIS_AUTHOR_MODEL", "claude-opus-4-7")
AUTHOR_VENDOR = os.environ.get("SYNTHESIS_AUTHOR_VENDOR", "anthropic")

DIGEST_YAML = os.path.join(INTEL_DIR, "weekly-digest.yaml")
VENDOR_PATH = os.path.join(INTEL_DIR, "vendor-releases.yaml")
SOCIAL_PATH = os.path.join(INTEL_DIR, "social-signals.yaml")
BENCH_PATH = os.path.join(INTEL_DIR, "benchmarks.yaml")


# Heuristic mapping: signal keywords -> AIDE principle/axiom touched.
# This is the "candidate" mapping — it is *suggestive*, not authoritative.
# A reviewer agent must confirm before any principle-metadata edit.
KEYWORD_TO_PRINCIPLE = [
    (r"\b(security|vulnerab|exploit|attack|red team|sandbox)\b", "P9 (Security by Structure) · A2 (Adversarial Separation)"),
    (r"\b(price|multiplier|cost|token|context window|budget)\b", "P1 (Context Budget)"),
    (r"\b(subagent|agent.*cli|adk|skills|mcp)\b", "P10 (Meta-Code as First-Class) · P2 (Locality of Behavior)"),
    (r"\b(swe[- ]?bench|terminal[- ]?bench|webarena|leaderboard|benchmark)\b", "P3 (Functional Core) · P8 (Observability as Structure)"),
    (r"\b(test|spec|verif|eval)\b", "P5 (Test as Specification)"),
    (r"\b(observ|log|trace|metric|telemetry)\b", "P8 (Observability as Structure)"),
    (r"\b(refactor|monolith|locality|feature)\b", "P2 (Locality of Behavior)"),
    (r"\b(progressive|disclosure|stream|partial)\b", "P6 (Progressive Disclosure)"),
    (r"\b(deterministic|guardrail|gate|policy)\b", "P7 (Deterministic Guardrails)"),
    (r"\b(agents?\.md|claude\.md|gemini\.md|meta[- ]?code|prompt)\b", "P10 (Meta-Code as First-Class)"),
]


def _load(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def _latest_raw_digest_path() -> str | None:
    """Find the most recent weekly-YYYY-MM-DD.md in INTEL_DIR."""
    if not os.path.isdir(INTEL_DIR):
        return None
    candidates = sorted(
        f for f in os.listdir(INTEL_DIR)
        if re.fullmatch(r"weekly-\d{4}-\d{2}-\d{2}\.md", f)
    )
    return os.path.join(INTEL_DIR, candidates[-1]) if candidates else None


def _classify(title: str) -> str:
    hits = []
    lower = (title or "").lower()
    for pattern, principle in KEYWORD_TO_PRINCIPLE:
        if re.search(pattern, lower):
            hits.append(principle)
    return "; ".join(dict.fromkeys(hits)) or "_(uncategorized — reviewer to classify)_"


def _group_vendor_releases(digest: dict) -> dict[str, list[dict]]:
    by_vendor: dict[str, list[dict]] = defaultdict(list)
    for hit in digest.get("vendor_releases") or []:
        by_vendor[hit.get("vendor") or "unknown"].append(hit)
    return dict(by_vendor)


def _candidate_metadata_changes(digest: dict, bench: dict) -> list[dict]:
    """Surface quantitative deltas that *could* support a calibration edit.

    Never edits ``principle-metadata.yaml`` itself — that is the job of
    the monthly Evolution Engine after multi-vendor consensus per A4.
    """
    candidates: list[dict] = []

    for shift in digest.get("benchmark_shifts") or []:
        candidates.append({
            "principle": "P3 / P8",
            "evidence": f"{shift['benchmark']}: {shift['prior_pct']:.2f}% → {shift['current_pct']:.2f}% (Δ {shift['delta_pp']:+.2f}pp)",
            "candidate_action": "Re-evaluate adaptive-principle calibration formula inputs for structure-vs-scale weighting.",
        })

    # Hunt for explicit multipliers / pricing deltas in vendor titles.
    for hit in digest.get("vendor_releases") or []:
        title = (hit.get("title") or "")
        if re.search(r"\b\d+\s*[x×]\b", title, re.IGNORECASE) or re.search(r"\$?\d+(?:\.\d+)?\s*(?:per|/)\s*(?:1?[mk]\b)", title, re.IGNORECASE):
            candidates.append({
                "principle": "P1 (Context Budget)",
                "evidence": f"{hit['vendor']} — {title} ({hit.get('url')})",
                "candidate_action": "Re-tune utilization_ratio / max_file_lines if pricing shift is sustained ≥2 weeks.",
            })

    return candidates


def _viral_themes(digest: dict) -> list[dict]:
    themes: list[dict] = []
    for v in digest.get("viral_hn") or []:
        themes.append({
            "title": v.get("title"),
            "url": v.get("url"),
            "points": v.get("points"),
            "query": v.get("query"),
            "classification": _classify(v.get("title") or ""),
        })
    return themes


def _source_health_summary(digest: dict) -> tuple[int, int, list[dict]]:
    h = digest.get("source_health") or {}
    return h.get("ok", 0), h.get("total", 0), h.get("failures", [])[:5]


def _render_english(today: str, digest: dict, bench: dict, raw_digest_path: str | None) -> str:
    by_vendor = _group_vendor_releases(digest)
    metadata_candidates = _candidate_metadata_changes(digest, bench)
    viral = _viral_themes(digest)
    ok, total, fails = _source_health_summary(digest)
    lookback_end = today
    lookback_start = (date.fromisoformat(today) - timedelta(days=7)).isoformat()

    raw_digest_ref = (
        os.path.relpath(raw_digest_path, ".") if raw_digest_path
        else f"{INTEL_DIR}/weekly-{today}.md"
    )

    lines: list[str] = []
    lines.append(f"# Weekly Synthesis — {today}")
    lines.append("")
    lines.append(f"> **Authoring agent**: aide-weekly-intel/synthesize_research.py v1 (drafter)")
    lines.append(f"> **Drafter model**: {AUTHOR_MODEL} (vendor: {AUTHOR_VENDOR}) — single-vendor draft. Awaits different-vendor reviewer per Axiom A2 / A4.")
    lines.append(f"> **Source digest**: `{raw_digest_ref}`")
    lines.append(f"> **Lookback**: {lookback_start} → {lookback_end} (UTC)")
    lines.append(f"> **Lens**: signals that change *how much engineering work can be safely delegated to an autonomous agent* — not generic AI news.")
    lines.append("")
    lines.append("This synthesis is the layer between the raw weekly intel digest and any principle-metadata edit. The drafter is deterministic and does not author claims by LLM — it groups, classifies, and surfaces *candidate* architectural claims for a human or different-vendor reviewer to confirm or reject. Per Axiom A3 (Empiricism), no claim here is calibration-grade until evidence is co-signed.")
    lines.append("")

    lines.append("## Vendor-shipped capability this week")
    if not by_vendor:
        lines.append("_No keyword-matched vendor releases captured by Phase A this cycle._")
    for vendor, hits in by_vendor.items():
        lines.append(f"### {vendor.title()}")
        for hit in hits[:8]:
            cls = _classify(hit.get("title") or "")
            lines.append(f"- [{hit.get('title')}]({hit.get('url')}) — touches: {cls}")
        if len(hits) > 8:
            lines.append(f"- … and {len(hits) - 8} more in `{raw_digest_ref}`")
        lines.append("")

    lines.append("## Community pressure (viral HN)")
    if not viral:
        lines.append("_No HN stories crossed the viral threshold (≥150 pts) on tracked queries._")
    for v in viral:
        lines.append(f"- [{v['title']}]({v['url']}) — **{v['points']} pts** · query `{v['query']}` · touches: {v['classification']}")
    lines.append("")

    lines.append("## Candidate principle-metadata signals")
    lines.append("")
    lines.append("These are **candidates** drawn from quantitative deltas in this week's data. They are not applied. The monthly Evolution Engine must validate them via multi-vendor deliberation + empirical gate before any edit to `principle-metadata.yaml`.")
    lines.append("")
    if not metadata_candidates:
        lines.append("_No quantitative deltas this week crossed an obvious calibration surface._")
    else:
        lines.append("| Principle surface | Evidence | Candidate action |")
        lines.append("|---|---|---|")
        for c in metadata_candidates:
            lines.append(f"| {c['principle']} | {c['evidence']} | {c['candidate_action']} |")
    lines.append("")

    lines.append("## Architectural claims for reviewer to accept or reject")
    lines.append("")
    lines.append("Per Axiom A4 (No Single Agent Authority), a different-vendor reviewer must explicitly accept, reject, or amend each claim. Silent acceptance is not accepted.")
    lines.append("")
    if by_vendor:
        vendor_count = sum(len(v) for v in by_vendor.values())
        lines.append(f"1. **Vendor velocity claim** — {vendor_count} agent-relevant releases this week across {len(by_vendor)} vendor(s) implies the cadence of agent-capability change exceeds AIDE's current monthly Evolution Engine charter. *Falsifier*: if next 2 weekly cycles each show <5 agent-relevant releases.")
    if viral:
        lines.append(f"2. **Community-pressure claim** — {len(viral)} viral story/stories on tracked queries indicates the developer community is converging on a topic AIDE has not yet documented. *Falsifier*: the topic does not recur in the next 4 weekly cycles.")
    if metadata_candidates:
        lines.append(f"3. **Calibration-surface claim** — {len(metadata_candidates)} quantitative delta(s) suggest at least one adaptive principle is operating on stale parameters. *Falsifier*: an empirical sandbox run shows current parameters within ±5% of optimum.")
    if not (by_vendor or viral or metadata_candidates):
        if total and ok == 0:
            lines.append("_No claims surfaced — but every external source failed this week ({0}/{1}). Treat this as **sensor outage**, not a quiet world. Re-run after restoring network access before drawing any architectural conclusion._".format(ok, total))
        elif total and (total - ok) >= max(3, total // 3):
            lines.append("_No claims surfaced this week. Source health was degraded ({0}/{1}); part of the apparent quiet could be coverage gaps, not absence of signal._".format(ok, total))
        else:
            lines.append("_No claims surfaced this week. Source health was clean ({0}/{1}); this records as a deliberate quiet cycle, not an outage._".format(ok, total))
    lines.append("")

    lines.append("## Source health (Axiom A5)")
    lines.append(f"- Sources reached: **{ok}/{total}** (failed: {total - ok})")
    if fails:
        for f in fails:
            lines.append(f"  - `{f['scope']}/{f['name']}` — {f['error']}")
    if total and ok == 0:
        lines.append("- **WARNING**: every external source failed. This synthesis is a stub; no signal-vs-noise interpretation above is reliable.")
    elif total and (total - ok) >= max(3, total // 3):
        lines.append("- **NOTE**: ≥1/3 of sources failed. Read all signal-absence above with that caveat.")
    lines.append("")

    lines.append("## What this synthesis does NOT ship")
    lines.append("")
    lines.append("- It does **not** edit `principle-metadata.yaml`. That requires multi-vendor consensus per A4.")
    lines.append("- It does **not** edit `axioms.yaml`. Axioms are immutable by construction.")
    lines.append("- It does **not** edit the methodology body in `docs/`. Body changes require a co-signed RFC.")
    lines.append("")
    lines.append("If `evolution/intel/dispatch.json` has `should_dispatch: true` this cycle, Phase F has also drafted an RFC under `rfcs/` for the reviewer queue. See that RFC for the structural change being proposed.")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"_Generated by `evolution/scripts/intel/synthesize_research.py` at {utc_now().isoformat()}._")
    return "\n".join(lines) + "\n"


def _render_korean(today: str, digest: dict, bench: dict, raw_digest_path: str | None) -> str:
    by_vendor = _group_vendor_releases(digest)
    metadata_candidates = _candidate_metadata_changes(digest, bench)
    viral = _viral_themes(digest)
    ok, total, fails = _source_health_summary(digest)
    lookback_end = today
    lookback_start = (date.fromisoformat(today) - timedelta(days=7)).isoformat()

    raw_digest_ref = (
        os.path.relpath(raw_digest_path, ".") if raw_digest_path
        else f"{INTEL_DIR}/weekly-{today}.md"
    )

    lines: list[str] = []
    lines.append(f"# 주간 합성 — {today}")
    lines.append("")
    lines.append(f"> **작성 에이전트**: aide-weekly-intel/synthesize_research.py v1 (자동 초안)")
    lines.append(f"> **초안 작성 모델**: {AUTHOR_MODEL} (벤더: {AUTHOR_VENDOR}) — 단일 벤더 초안. 공리 A2/A4에 따라 다른 벤더 리뷰어 서명 대기.")
    lines.append(f"> **소스 디지스트**: `{raw_digest_ref}`")
    lines.append(f"> **조회 구간**: {lookback_start} → {lookback_end} (UTC)")
    lines.append(f"> **렌즈**: *자율 에이전트에 안전하게 위임 가능한 엔지니어링 작업의 양*을 바꾸는 신호만 수용. 일반 AI 뉴스는 제외.")
    lines.append("")
    lines.append("본 합성은 원시 주간 인텔과 `principle-metadata.yaml` 변경 사이의 레이어다. 초안 생성기는 결정론적이며 LLM으로 주장을 작성하지 않는다 — 신호를 묶고 분류하여 **후보** 아키텍처 주장으로 노출시키며, 사람 또는 다른 벤더 리뷰어가 확정 또는 기각한다. 공리 A3(Empiricism)에 따라 여기의 어떤 주장도 공동 서명 전에는 calibration 등급이 아니다.")
    lines.append("")

    lines.append("## 이번 주 벤더가 출시한 역량")
    if not by_vendor:
        lines.append("_이번 사이클의 Phase A 키워드 매칭에 잡힌 벤더 릴리스 없음._")
    for vendor, hits in by_vendor.items():
        lines.append(f"### {vendor.title()}")
        for hit in hits[:8]:
            cls = _classify(hit.get("title") or "")
            lines.append(f"- [{hit.get('title')}]({hit.get('url')}) — 관련 원칙: {cls}")
        if len(hits) > 8:
            lines.append(f"- … 외 {len(hits) - 8}건은 `{raw_digest_ref}` 참조")
        lines.append("")

    lines.append("## 커뮤니티 압력 (HN viral)")
    if not viral:
        lines.append("_추적 쿼리에서 viral 임계값(150pts) 넘은 HN 스토리 없음._")
    for v in viral:
        lines.append(f"- [{v['title']}]({v['url']}) — **{v['points']} pts** · 쿼리 `{v['query']}` · 관련: {v['classification']}")
    lines.append("")

    lines.append("## 후보 principle-metadata 신호")
    lines.append("")
    lines.append("이번 주 데이터의 정량 delta에서 도출한 **후보**다. 적용되지 않는다. 월간 Evolution Engine이 다중 벤더 심의 + 경험적 게이트로 검증한 후에만 `principle-metadata.yaml`을 편집할 수 있다.")
    lines.append("")
    if not metadata_candidates:
        lines.append("_이번 주 정량 delta 중 명확한 calibration surface를 넘은 항목 없음._")
    else:
        lines.append("| 원칙 면 | 증거 | 후보 액션 |")
        lines.append("|---|---|---|")
        for c in metadata_candidates:
            lines.append(f"| {c['principle']} | {c['evidence']} | {c['candidate_action']} |")
    lines.append("")

    lines.append("## 리뷰어가 수락/기각/수정해야 할 아키텍처 주장")
    lines.append("")
    lines.append("공리 A4(No Single Agent Authority)에 따라 다른 벤더 리뷰어가 각 주장을 명시적으로 수락·기각·수정해야 한다. 침묵 수락은 인정되지 않는다.")
    lines.append("")
    if by_vendor:
        vendor_count = sum(len(v) for v in by_vendor.values())
        lines.append(f"1. **벤더 속도 주장** — 이번 주 {len(by_vendor)}개 벤더에서 {vendor_count}건의 에이전트 관련 릴리스가 있었다. 이는 에이전트 역량 변화 속도가 AIDE의 현 월간 Evolution Engine 차터를 초과함을 시사한다. *반증 조건*: 다음 2주간 weekly 사이클에서 주당 <5건이면 기각.")
    if viral:
        lines.append(f"2. **커뮤니티 압력 주장** — 추적 쿼리에서 {len(viral)}건의 viral 스토리는 개발자 커뮤니티가 AIDE가 아직 문서화하지 않은 주제로 수렴 중임을 시사한다. *반증 조건*: 다음 4주간 weekly 사이클에서 주제가 재등장하지 않으면 기각.")
    if metadata_candidates:
        lines.append(f"3. **Calibration surface 주장** — {len(metadata_candidates)}건의 정량 delta는 적어도 한 개 이상의 adaptive principle이 stale 파라미터로 운영 중임을 시사한다. *반증 조건*: 경험적 sandbox 실행이 현 파라미터가 ±5% 이내 최적임을 보이면 기각.")
    if not (by_vendor or viral or metadata_candidates):
        if total and ok == 0:
            lines.append("_surfaced된 주장 없음 — 그러나 이번 주 모든 외부 소스가 실패했다({0}/{1}). **센서 outage**로 취급하고 조용한 세상으로 해석하지 말 것. 네트워크 복구 후 재실행한 다음 아키텍처 결론을 내려야 한다._".format(ok, total))
        elif total and (total - ok) >= max(3, total // 3):
            lines.append("_이번 주 surfaced된 주장 없음. 소스 헬스가 저하됨({0}/{1}); 외관상 quiet의 일부는 신호 부재가 아닌 커버리지 갭일 수 있다._".format(ok, total))
        else:
            lines.append("_이번 주 surfaced된 주장 없음. 소스 헬스 양호({0}/{1}); 의도된 quiet cycle로 기록되며 outage가 아니다._".format(ok, total))
    lines.append("")

    lines.append("## 소스 헬스 (공리 A5)")
    lines.append(f"- 도달한 소스: **{ok}/{total}** (실패: {total - ok})")
    if fails:
        for f in fails:
            lines.append(f"  - `{f['scope']}/{f['name']}` — {f['error']}")
    if total and ok == 0:
        lines.append("- **경고**: 모든 외부 소스가 실패함. 본 합성은 스텁이며 위의 어떤 신호 대 잡음 해석도 신뢰할 수 없다.")
    elif total and (total - ok) >= max(3, total // 3):
        lines.append("- **참고**: 소스의 1/3 이상이 실패. 위의 모든 'signal-absence' 해석에 이 단서가 적용된다.")
    lines.append("")

    lines.append("## 본 합성이 출시하지 *않는* 것")
    lines.append("")
    lines.append("- `principle-metadata.yaml`을 편집하지 않는다. A4에 따라 다중 벤더 합의가 필요.")
    lines.append("- `axioms.yaml`을 편집하지 않는다. 공리는 구성상 불변.")
    lines.append("- `docs/`의 방법론 본문을 편집하지 않는다. 본문 변경은 공동 서명된 RFC가 필요.")
    lines.append("")
    lines.append("이번 사이클에 `evolution/intel/dispatch.json`이 `should_dispatch: true`이면, Phase F가 `rfcs/` 아래에 RFC 초안을 함께 만들어 리뷰 큐에 추가한다.")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"_`evolution/scripts/intel/synthesize_research.py`가 {utc_now().isoformat()}에 생성._")
    return "\n".join(lines) + "\n"


def main() -> None:
    digest = _load(DIGEST_YAML)
    bench = _load(BENCH_PATH)

    if not digest:
        print(f"No weekly digest at {DIGEST_YAML}; run Phase D first. Skipping Phase E.")
        return

    today = date.today().isoformat()
    raw_path = _latest_raw_digest_path()

    en_dir = os.path.join(RESEARCH_DIR, "en")
    ko_dir = os.path.join(RESEARCH_DIR, "ko")
    os.makedirs(en_dir, exist_ok=True)
    os.makedirs(ko_dir, exist_ok=True)

    en_path = os.path.join(en_dir, f"{today}-weekly-synthesis.md")
    ko_path = os.path.join(ko_dir, f"{today}-weekly-synthesis.md")

    with open(en_path, "w") as f:
        f.write(_render_english(today, digest, bench, raw_path))
    with open(ko_path, "w") as f:
        f.write(_render_korean(today, digest, bench, raw_path))

    print(f"Research synthesis (en) -> {en_path}")
    print(f"Research synthesis (ko) -> {ko_path}")


if __name__ == "__main__":
    main()
