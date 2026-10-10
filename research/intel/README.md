# Weekly Intel Synthesis (auto-generated)

This directory holds **agent-generated weekly synthesis notes** produced by
Phase E of the AIDE Weekly Intel pipeline
(`evolution/scripts/intel/synthesize_research_note.py`).

## What lives here

- `YYYY-MM-DD-weekly-synthesis.md` — one file per Monday run. Catalogs only
  signals aligned with AIDE's purpose: delegating software engineering to
  autonomous agents, and the architecture / methodology that lets models —
  not humans — drive the build loop. Generic AI / consumer-product news is
  filtered out by the relevance scorer.

## What does *not* live here

- Human-curated research and the original v1.0 deep-research reports — those
  stay under `research/en/` and `research/ko/`.
- Methodology body changes — those belong in `docs/en/AIDE-METHODOLOGY.md` and
  may only land via the RFC process with different-vendor co-sign
  (Axioms A2 / A4).

## Lifecycle

1. **Monday 00:00 UTC** — Phase A–D collect raw signals into
   `evolution/intel/weekly-YYYY-MM-DD.md`.
2. **Phase E** filters those signals through the AIDE-relevance scorer and
   writes a synthesis here if any items survive the filter.
3. **Phase F** may, conditionally, raise an auto-draft RFC under `rfcs/` when
   high-signal thresholds are crossed.
4. **Phase G** appends a one-line catalog entry to `docs/en/recent-intel.md`
   and `docs/ko/recent-intel.md` so the run is discoverable from the docs
   navigation without touching the methodology body.

## Reviewing these notes

Every synthesis is explicitly marked as **single-vendor draft, awaits
different-vendor reviewer**. The reviewer's job is to either:

- Co-sign with a concrete `principle-metadata.yaml` change (then promote to an
  RFC under `rfcs/`), or
- Reject in writing, citing where the evidence falls short (Axiom A3).

Until that co-sign happens, the AIDE methodology body is unchanged.

---

## 한국어 요약

이 디렉토리는 AIDE 주간 인텔 파이프라인의 **Phase E (자동 합성기)**가
매주 월요일 생성하는 합성 노트를 보관합니다. AIDE 취지(자율 에이전트에게 개발 위임)와
연관된 신호만 관련성 스코어러로 필터링하여 카탈로그합니다.

- 본 노트는 **단일 벤더 초안**이며, 다른 벤더 리뷰어 에이전트의 공동 서명 전까지는
  방법론 본문(`docs/en/AIDE-METHODOLOGY.md`, `principle-metadata.yaml`,
  `axioms.yaml`)에 어떤 변경도 만들지 않습니다 (A2 / A4).
- 방법론 변경이 정당화될 경우 `rfcs/` 아래 RFC를 통해 다른 벤더 리뷰어와 함께 승격되어야 합니다.
