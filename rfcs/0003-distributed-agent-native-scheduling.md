- RFC Number: 0003
- Title: Distributed Agent-Native Scheduling (AIDE v2.1)
- Agent Used: Claude Code on web
- Agent Model: claude-opus-4-7
- Research Method: in-session pipeline run + 2026-05-04 weekly intel digest curation
- Date: 2026-05-04
- Status: Draft

## Summary

RFC-0002 (AIDE v2.0) put the Evolution Engine in a single GitHub Actions
workflow that orchestrated three vendor CLIs (Claude Code CLI, Codex CLI,
Gemini CLI) on a monthly cron. In practice that workflow has been disabled
since 2026-02 awaiting OAuth-policy clarification, with the side effect that
`docs/`, `principle-metadata.yaml`, and `rfcs/` have not received a single
agent-driven update in ~2.5 months.

This RFC proposes **AIDE v2.1: Distributed Agent-Native Scheduling**. The
heavy CI cron pipeline is retired. Each participating agent runs on its own
platform's scheduler (Claude Code on web for Anthropic, Codex app for OpenAI)
and opens / reviews PRs in this repository directly. Gemini is removed from
the loop until a comparable scheduler is available; axioms A2 and A4 are
re-aligned to require **≥2 different-vendor agents** with an explicit
tie-breaker rule (1:1 split blocks).

Axiom *statements* are not weakened — A2 already said "different models or
different vendors" and A4 already said "at least 2 independent agents". This
RFC only synchronizes the enforcement plumbing and the body documentation
with what the statements already permitted.

## Motivation

### 1. The CI-orchestrated pipeline never moved past disabled state

`.github/workflows/aide-evolution-engine.yml` carried a comment header:

> ⚠️ DISABLED: Awaiting OAuth policy clarification from Anthropic
> See: https://github.com/anthropics/claude-code/issues/27125

For 2.5 months the schedule and `repository_dispatch` triggers remained
commented out. As a consequence:

- `docs/en/AIDE-METHODOLOGY.md` and `docs/ko/AIDE-METHODOLOGY.md`: last
  substantive change 2026-02-22 (cd31b71, MkDocs setup).
- `rfcs/`, `principle-metadata.yaml`: last change 2026-02-20 (f23461b, the
  v2.0 introduction itself).
- `evolution/history/`: empty — not a single autonomous evolution cycle has
  ever completed.

The Weekly Intel Loop (`aide-weekly-intel.yml`) was the only piece of v2.0
that has run reliably on its schedule, but its `repository_dispatch` events
had no listener.

### 2. Per-platform schedulers exist now

Since 2026-Q2 both Anthropic (Claude Code on web) and OpenAI (Codex app)
ship native task scheduling. A scheduled session there:

- Runs in a managed sandbox with platform-side auth — no GitHub Actions
  secrets to register or rotate.
- Has direct access to the platform's tool ecosystem (web search, file
  system, MCP servers) without a CLI bridge.
- Opens PRs and posts review comments via the GitHub MCP server, so the
  collaboration surface is identical to a human contributor.

The pattern was empirically validated this week: Claude Code on web ran the
weekly intel curation on 2026-05-04 and merged PR #6 (machine-fetched
digest + AIDE-relevance commentary) — exactly the role the CI Evolution
Engine was supposed to play but never did.

### 3. Gemini scheduler gap

Google has not (as of 2026-05-04) shipped a comparable Gemini scheduler that
can autonomously open / review PRs. Forcing Gemini participation through a
human-in-the-loop bridge would re-introduce the human bottleneck this whole
methodology exists to remove. Removing Gemini temporarily is the lesser
violation — and it is permitted by the existing axiom statements.

## Detailed Design

### 1. Workflow changes

| File | Change |
|---|---|
| `.github/workflows/aide-evolution-engine.yml` | **Deleted.** The 4-phase CI pipeline (sense → deliberate → validate → apply) is replaced by per-platform scheduled agents. |
| `.github/workflows/aide-weekly-intel.yml` | **Retained.** Still the cheapest mechanical sense pass; produces `evolution/intel/weekly-YYYY-MM-DD.md` every Monday 00:00 UTC. |
| `.github/workflows/axiom-gate.yml` | **Retained.** Hard-coded enforcement of A1-A5 on every PR; does not require API keys. |
| `.github/workflows/deploy-pages.yml` | **Retained.** Unrelated to this change. |

### 2. Script changes (`evolution/scripts/`)

The CI pipeline scripts that were tightly coupled to the deleted workflow
are removed:

- `collect_benchmarks.py`, `scan_models.py`, `check_triggers.py`,
  `compile_sense_report.py`
- `deliberate_research.py`, `deliberate_adversary.py`,
  `deliberate_synthesis.py`
- `validate_baseline.py`, `validate_modified.py`, `empirical_gate.py`
- `apply_changes.py`, `update_docs.py`, `record_history.py`,
  `drift_detection.py`

The Weekly Intel scripts (`evolution/scripts/intel/*`) are retained — they
remain the foundation that scheduled agents build on.

### 3. Axiom enforcement re-alignment

| Axiom | Statement (unchanged) | Enforcement check (synchronized) |
|---|---|---|
| **A2 Adversarial Separation** | "different models or different vendors" | "At least 2 different vendor models participate" — already in `axioms.yaml`, kept. |
| **A4 No Single Agent Authority** | "consensus from at least 2 independent agents" | Was "Evolution Engine deliberation requires 3 agents from different vendors". Updated to: "Evolution proposals require at least 2 agents from different vendors" + a **tie-breaker rule**: a 1:1 split blocks the change (no auto-resolution). |

Axiom statements are immutable. This RFC only updates the *enforcement check
list* under `enforcement.checks[]`, which is the implementation surface the
statements explicitly delegate to.

### 4. Per-platform scheduling contract

Each scheduled agent must, at minimum:

1. Read the latest `evolution/intel/weekly-*.md` digest produced by the CI
   sense pass.
2. Score each external signal against AIDE's 10 principles and 5 axioms.
3. If a principle re-tuning candidate is identified, open a PR that:
   - Modifies `principle-metadata.yaml` (numeric guideline) and/or
     `docs/en/AIDE-METHODOLOGY.md` + `docs/ko/AIDE-METHODOLOGY.md` in lockstep.
   - Includes an `evolution/history/<timestamp>.yaml` audit entry with
     quantitative evidence (A3 / A5).
   - Is opened as **draft** until a different-vendor agent has approved.
4. If reviewing another agent's PR, post a structured review comment with:
   - Approve / request-changes / block verdict.
   - Quantitative evidence for the verdict.
   - Author and reviewer model IDs in PR metadata for A2 verification.

### 5. Concurrency: weekly intel CI vs. scheduled curator

Both `aide-weekly-intel.yml` and the Claude Code on web Monday session
target `evolution/intel/weekly-YYYY-MM-DD.md`. This RFC mandates the
following coordination:

- **CI runs first**, at 00:00 UTC. Writes the canonical machine-fetched
  digest to `weekly-YYYY-MM-DD.md` and commits.
- **Scheduled curator runs after**, at 00:30 UTC or later. Pulls master,
  *amends* the existing file with curator commentary on top, opens a PR.
- If the curator's branch is divergent at PR time, it must rebase onto
  master and merge intelligently (preserving CI-fetched raw items).

This codifies the manual conflict resolution performed in PR #6.

## Evidence

- **Disabled-state evidence**: `aide-evolution-engine.yml` lines 13-21
  contain the `# DISABLED` block as of 2026-05-04.
- **Empty history evidence**: `ls evolution/history/` returned 0 entries.
- **Stale docs evidence**: `git log -1 -- docs/en/AIDE-METHODOLOGY.md`
  returns commit `cd31b71` from 2026-02-22 (MkDocs scaffolding only).
- **Working pattern evidence**: this session (2026-05-04) successfully
  produced the 2026-05-04 weekly digest via Claude Code on web's scheduler,
  including the merge-conflict resolution between the CI cron and the
  scheduled curator. PR #6 (merged) is the empirical proof-of-concept.

## Impact Assessment

### Affected principles

| Principle | Impact |
|---|---|
| P3, P5, P7, P8, P9 (permanent) | None |
| P1, P2, P4, P6, P10 (adaptive) | Faster recalibration cycle (weekly instead of monthly) |

### Affected axioms

| Axiom | Statement | Enforcement |
|---|---|---|
| A1 Reversibility | unchanged | unchanged |
| A2 Adversarial Separation | unchanged | wording already permitted ≥2 vendors; clarified |
| A3 Empiricism | unchanged | unchanged |
| A4 No Single Authority | unchanged | tie-breaker rule made explicit; "3 agents" enforcement line softened to "≥2 agents" |
| A5 Self-Observability | unchanged | improved — `compile_weekly_digest.py` now surfaces source health |

### Adopters

- **AIDE v2.0 adopters**: backwards-compatible. Existing axioms.yaml /
  principle-metadata.yaml schema unchanged. Only enforcement plumbing
  changes.
- **New adopters**: simpler entry — no need to register
  `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `GOOGLE_API_KEY` /
  `AIDE_BOT_TOKEN` GitHub secrets.

## Alternatives Considered

### Alt 1: Re-enable the CI Evolution Engine and require human-in-the-loop Gemini

Rejected. Human bridging re-introduces a single point of human
unavailability that contradicts AIDE's core thesis.

### Alt 2: Replace Gemini with a different third vendor (xAI Grok, Mistral, Cohere)

Rejected for v2.1. None of the candidates ship a scheduler equivalent to
Claude Code on web or the Codex app yet. Will be revisited as a future RFC
when one does.

### Alt 3: Keep both pipelines — CI cron and per-platform schedule — running redundantly

Rejected. Double-writes to `evolution/intel/weekly-YYYY-MM-DD.md` produce
merge conflicts every Monday (empirically observed in PR #6). The CI sense
pass + per-platform curator pattern is a *layered*, not *redundant*,
architecture.

### Alt 4: Defer the decision and continue with the current frozen state

Rejected. The current state — Sense running but no Deliberate / Validate /
Apply — is exactly the failure mode RFC-0002's evidence section warned
about: "AIDE v1.0 has no mechanism to automatically respond to model
evolution scenarios." Two and a half months of unchanged docs is empirical
evidence the failure mode is active.
