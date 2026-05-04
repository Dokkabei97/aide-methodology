# AIDE Evolution Engine (v2.1 — Distributed Agent-Native Scheduling)

The Evolution Engine is AIDE v2.0's autonomous self-evolution system. As of
2026-05-04 (RFC-0003) the heavy CI-cron pipeline has been retired. Each
participating agent now runs on its own platform's scheduler and opens PRs
into this repository directly.

## Architecture

```
                      Weekly Intel Loop (sensor, keyless)
                      Mon 00:00 UTC — vendors, HN, blogs, benchmarks
                                     │
                                     ▼ commits weekly digest, surfaces signals
   Distributed scheduled agents (per-platform schedulers, no shared CI):

   Mon 00:00 UTC  Claude Code on web   ──>  curates digest, opens PR with
                  (Anthropic side)          AIDE-relevance commentary +
                                            principle re-tuning candidates
   Mon 00:00 UTC  Codex app schedule   ──>  adversarial review of the
                  (OpenAI side)             Claude PR; blocks or approves;
                                            posts critique
                                     │
                                     ▼  consensus (≥2 different-vendor agents)
                  Axiom Gate CI       ──>  enforces A1-A5; merges on pass
```

The **Weekly Intel Loop** (`evolution/intel/`, workflow `aide-weekly-intel.yml`)
remains the cheap, keyless mechanical sense pass. See `evolution/intel/README.md`.

The **per-platform scheduled agents** replace the previous CI cron because:
- Platform schedulers (Claude Code on web, Codex app) handle auth, retries,
  tool access, and budgets natively — no GitHub Actions secrets to manage.
- Each agent stays in its native environment (no CLI bridge layer).
- A schedule outage on one platform doesn't block the others.
- Gemini is currently out of the loop (no scheduler support yet); axioms A2 / A4
  were updated to require ≥2 different-vendor agents instead of 3, with an
  explicit tie-breaker rule (1:1 split blocks).

## Directory Structure

```
evolution/
  scripts/intel/        # Weekly Intel Loop — external signal scanners
    fetch_vendor_releases.py  # Anthropic / OpenAI / Google releases
    fetch_social_signals.py   # HN, tech blogs, X, Threads
    fetch_benchmarks.py       # SWE-bench, Terminal-bench, WebArena, SWE-rebench
    compile_weekly_digest.py  # Merge + dispatch decision + source health
  benchmarks/           # Reserved for benchmark snapshots fetched by agents
  deliberation/         # Reserved for agent deliberation artifacts (PR-attached)
  sandbox/              # Reserved for empirical validation results
  history/              # Evolution audit trail (permanent record)
  intel/                # Weekly intel digests (permanent MDs + transient YAMLs)
```

The `benchmarks/`, `deliberation/`, `sandbox/` directories are now populated by
the scheduled agents themselves on a per-PR basis rather than by a CI pipeline.

## Triggering

- **Weekly machine sense**: `aide-weekly-intel.yml` runs every Monday 00:00 UTC.
- **Curated proposal**: Claude Code on web is scheduled to run every Monday and
  opens a PR with the curated digest and any principle re-tuning candidates.
- **Adversarial review**: Codex app (OpenAI) is scheduled to review the Claude
  PR within 24 hours. Approval from the Codex agent satisfies A4 (≥2 different-
  vendor consensus).
- **Manual trigger**: `gh workflow run aide-weekly-intel.yml`.

## Required Secrets

Repository-side: **none required for the new pipeline.** Each scheduled agent
runs in its own platform with its own auth.

CI-side (the workflows that remain in this repo):

| Workflow | Secret | Purpose |
|---|---|---|
| `aide-weekly-intel.yml` | none | Reads only public RSS / APIs |
| `axiom-gate.yml` | none | Static checks on PR metadata |

## Axiom Compliance

Every evolution PR verifies compliance with the 5 Immutable Axioms:
- **A1 Reversibility**: All changes are git-backed and revertable.
- **A2 Adversarial Separation**: ≥2 different-vendor agents participate
  (e.g., Claude proposes, Codex reviews).
- **A3 Empiricism**: Changes require quantitative evidence (benchmark deltas,
  repo metrics) — agent reasoning alone is insufficient.
- **A4 No Single Authority**: Consensus from ≥2 independent agents required;
  a 1:1 split blocks the change (no auto-resolution).
- **A5 Self-Observability**: Full audit trail in `evolution/history/` and the
  weekly digest under `evolution/intel/`.
