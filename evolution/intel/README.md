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
      ▼  job: collect (sensor pass — commits to running branch)
┌──────────────────────────────┐
│ Phase A: Vendor releases     │  Anthropic / OpenAI / Google RSS + changelogs
├──────────────────────────────┤
│ Phase B: Social signals      │  HN Algolia, tech blogs, X (nitter), Threads
├──────────────────────────────┤
│ Phase C: Benchmark snapshot  │  SWE-bench, Terminal-bench, WebArena, SWE-rebench
├──────────────────────────────┤
│ Phase D: Digest + dispatch   │  Merge → commit MD digest → repository_dispatch if signal
└──────────────────────────────┘
      │
      ├── if signal: → Evolution Engine (multi-agent deliberation)
      │
      ▼  job: synthesize (judgement pass — opens a PR for reviewer)
┌──────────────────────────────┐
│ Phase E: Research synthesis  │  Draft research/{en,ko}/{date}-weekly-synthesis.md
├──────────────────────────────┤
│ Phase F: RFC draft           │  If thresholds firmly crossed → rfcs/NNNN-…
├──────────────────────────────┤
│ Phase G: CHANGELOG entry     │  Append under [Unreleased]
└──────────────────────────────┘
      │
      └── opens draft PR to running branch (so axiom-gate runs and
          a different-vendor reviewer can co-sign per A2 / A4)
```

### Why two jobs?

`collect` produces **signal** — what the sensors saw. It is reversible,
fully deterministic, and safe to push directly to the branch.

`synthesize` produces **judgement** — candidate architectural claims and
RFC stubs. Judgement requires adversarial separation: it goes through a
PR so the axiom-gate runs and a different-vendor reviewer can sign or
reject before any of it lands.

### What `synthesize` will and will not touch

| Path | Editable by Phase E–G? | Rationale |
|---|:---:|---|
| `research/{en,ko}/{date}-weekly-synthesis.md` | ✔ | Draft surface; awaits reviewer |
| `rfcs/NNNN-weekly-intel-{date}.md` | ✔ (when thresholds fire) | Draft RFC; status remains `Draft` |
| `CHANGELOG.md` (`[Unreleased]` only) | ✔ | Idempotent — same-day re-run does not duplicate |
| `principle-metadata.yaml` | ✘ | Requires multi-vendor consensus (A4) |
| `axioms.yaml` | ✘ | Immutable by construction |
| `docs/{en,ko}/AIDE-METHODOLOGY.md` | ✘ | Body changes require co-signed RFC |

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
| `evolution/intel/vendor-releases.yaml`       |    ✘    | Raw vendor feed dump (volatile)  |
| `evolution/intel/social-signals.yaml`        |    ✘    | Raw HN/blog/X dump (volatile)    |
| `evolution/intel/benchmarks.yaml`            |    ✘    | Raw leaderboard dump (volatile)  |
| `evolution/intel/weekly-digest.yaml`         |    ✘    | Machine-readable digest          |
| `evolution/intel/dispatch.json`              |    ✘    | Transient dispatch decision flag |
| `evolution/intel/rfc-decision.json`          |    ✘    | Phase F decision: did we draft an RFC, and why |
| `research/{en,ko}/{date}-weekly-synthesis.md`|    ✔    | Phase E synthesis draft (via PR)                |
| `rfcs/NNNN-weekly-intel-{date}.md`           |    ✔    | Phase F RFC stub (via PR, when thresholds fire) |
| `CHANGELOG.md` `[Unreleased]`                |    ✔    | Phase G entry (via PR)                          |

## Running manually

```
# GitHub Actions
gh workflow run aide-weekly-intel.yml -f lookback_days=14

# Locally — sensor pass only
export PYTHONPATH=evolution/scripts/intel
python evolution/scripts/intel/fetch_vendor_releases.py
python evolution/scripts/intel/fetch_social_signals.py
python evolution/scripts/intel/fetch_benchmarks.py
python evolution/scripts/intel/compile_weekly_digest.py

# Locally — judgement pass (Phase E–G)
python evolution/scripts/intel/synthesize_research.py
python evolution/scripts/intel/draft_rfc.py
python evolution/scripts/intel/update_changelog.py
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
