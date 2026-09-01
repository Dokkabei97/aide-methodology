# AIDE Weekly Intel Loop

The Weekly Intel Loop is AIDE v2.0's **external sensor**. It runs every
Monday 00:00 UTC (09:00 KST) to scan the outside world for signals that
matter to agent-led development, and — when thresholds are crossed —
wakes the monthly Evolution Engine for deliberation.

## Why a separate weekly loop?

The monthly Evolution Engine is heavy: three vendor-different agents
deliberate, validate empirically, and auto-apply principle updates.
Running it every week would waste API budget and amplify drift.

The weekly loop is **read-only, cheap, and keyless**. It only raises
its hand when the outside world actually moved, which is aligned with:

- **Axiom A3 (Empiricism)** — dispatches only on quantitative thresholds.
- **Axiom A5 (Self-Observability)** — persists every weekly digest as
  a permanent audit trail under `evolution/intel/weekly-YYYY-MM-DD.md`.
- **Principle of Progressive Disclosure** — vendor releases and social
  signals fan out first; only the distilled digest reaches the heavy
  deliberation pipeline.

## Pipeline

```
Monday 00:00 UTC
      │
      ▼
┌──────────────────────────────┐
│ Phase A: Vendor releases     │  Anthropic / OpenAI / Google RSS + changelogs
├──────────────────────────────┤
│ Phase B: Social signals      │  HN Algolia, tech blogs, X (nitter), Threads
├──────────────────────────────┤
│ Phase C: Benchmark snapshot  │  SWE-bench, Terminal-bench, WebArena, SWE-rebench
├──────────────────────────────┤
│ Phase D: Digest + dispatch   │  Merge → commit MD digest → repository_dispatch if signal
├──────────────────────────────┤
│ Phase E: Synthesis writer    │  AIDE-relevance filter → research/intel/YYYY-MM-DD-weekly-synthesis.md
├──────────────────────────────┤
│ Phase F: Conditional RFC     │  High-signal threshold → rfcs/NNNN-weekly-intel-*.md (draft)
├──────────────────────────────┤
│ Phase G: Docs catalog        │  Append entry to docs/{en,ko}/recent-intel.md
└──────────────────────────────┘
      │
      ├── if signal: → Evolution Engine (multi-agent deliberation)
      └── else:       → quiet, weekly MD + (maybe) synthesis + (rarely) RFC committed
```

### Why Phases E/F/G are isolated

Phase E onward writes outside `evolution/intel/`, so each new file path is
constrained to a safe surface:

| Phase | Writes to                                          | Touches methodology body? |
|-------|----------------------------------------------------|---------------------------|
| E     | `research/intel/YYYY-MM-DD-weekly-synthesis.md`    | No (research catalog)     |
| F     | `rfcs/NNNN-weekly-intel-*.md` (draft only)         | No (RFC is a *proposal*)  |
| G     | `docs/en/recent-intel.md`, `docs/ko/recent-intel.md` | No (catalog page, not body) |

The protected body files — `docs/en/AIDE-METHODOLOGY.md`,
`principle-metadata.yaml`, `axioms.yaml` — are **never** modified by the
weekly pipeline. That power belongs only to the monthly Evolution Engine,
which the same digest dispatches in parallel when signal thresholds fire.
This preserves A2 (Adversarial Separation) and A4 (No Single Authority) for
the body while still letting the weekly loop produce concrete artifacts.

## Dispatch thresholds

A `weekly_intel_signal` `repository_dispatch` event fires when **any** of:

| Signal               | Threshold                                            |
|----------------------|------------------------------------------------------|
| Vendor release       | ≥1 keyword-matched entry this week                   |
| Viral HN coverage    | ≥3 stories on tracked queries with ≥150 points      |
| Benchmark SOTA shift | ≥2.0 percentage points on any tracked leaderboard    |

Thresholds are deliberately conservative — false positives cost a full
Evolution Engine cycle. Adjust in `compile_weekly_digest.py`.

## Outputs

| Path                                         | Tracked? | Purpose                        |
|----------------------------------------------|:--------:|--------------------------------|
| `evolution/intel/weekly-YYYY-MM-DD.md`       |    ✔    | Permanent human-readable digest |
| `evolution/intel/benchmark-history.yaml`     |    ✔    | Cross-week SOTA comparison state |
| `research/intel/YYYY-MM-DD-weekly-synthesis.md` | ✔  | Phase E AIDE-filtered synthesis |
| `rfcs/NNNN-weekly-intel-*.md`                |    ✔    | Phase F auto-draft (rare)        |
| `docs/{en,ko}/recent-intel.md`               |    ✔    | Phase G catalog (append-only)    |
| `evolution/intel/vendor-releases.yaml`       |    ✘    | Raw vendor feed dump (volatile)  |
| `evolution/intel/social-signals.yaml`        |    ✘    | Raw HN/blog/X dump (volatile)    |
| `evolution/intel/benchmarks.yaml`            |    ✘    | Raw leaderboard dump (volatile)  |
| `evolution/intel/weekly-digest.yaml`         |    ✘    | Machine-readable digest          |
| `evolution/intel/dispatch.json`              |    ✘    | Transient dispatch decision flag |
| `evolution/intel/synthesis-summary.json`     |    ✘    | Phase E summary handoff to F/G   |
| `evolution/intel/rfc-draft-report.json`      |    ✘    | Phase F decision handoff to G    |

## Running manually

```
# GitHub Actions
gh workflow run aide-weekly-intel.yml -f lookback_days=14

# Locally
export PYTHONPATH=evolution/scripts/intel
python evolution/scripts/intel/fetch_vendor_releases.py
python evolution/scripts/intel/fetch_social_signals.py
python evolution/scripts/intel/fetch_benchmarks.py
python evolution/scripts/intel/compile_weekly_digest.py
python evolution/scripts/intel/synthesize_research_note.py
python evolution/scripts/intel/draft_rfc_if_threshold.py
python evolution/scripts/intel/update_docs_recent_intel.py
```

## Graceful degradation

Every fetcher wraps its work in `safe_fetch(...)`, which retries twice
and then records the error in the output YAML. A single outage (e.g.
all nitter mirrors down) never aborts the weekly scan — the digest just
notes the gap. This is the practical shape of Axiom A5.

---

## 한국어 요약 (Summary in Korean)

**주간 인텔 루프**는 매주 월요일 09:00 KST에 외부 세계(벤더 릴리스·HN·테크 블로그·X·벤치마크)를
읽기 전용으로 스캔해서 AIDE 방법론이 따라잡아야 할 신호가 있는지 감지합니다.
신호가 잡히면 월간 Evolution Engine에 `repository_dispatch`로 심의를 요청합니다.
신호가 없으면 조용히 주간 마크다운 요약만 커밋되어 영구 감사 기록으로 남습니다.
모든 페처는 실패 시 graceful degrade하여 파이프라인을 막지 않으며, 이는 A5(자기관측성) 공리를
구체화한 것입니다.
