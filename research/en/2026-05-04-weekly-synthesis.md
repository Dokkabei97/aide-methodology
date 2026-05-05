# Weekly Synthesis — 2026-05-04

> **Authoring agent**: Claude Code on web (claude-opus-4-7), single-vendor draft. Awaits different-vendor reviewer per Axiom A2 / A4.
> **Source digest**: `evolution/intel/weekly-2026-05-04.md`
> **Lookback**: 2026-04-28 → 2026-05-04 (UTC).
> **Lens**: signals that change *how much engineering work can be safely delegated to an autonomous agent* — not generic AI news.

This research note is the synthesis layer required by RFC-0003 §4 (per-platform scheduling contract). The Weekly Intel digest assembles raw signals; this note converts them into architectural claims for agent-led development and identifies the principle-metadata changes that follow.

## Three architectural claims this week supports

### Claim 1 — Cost is the new context constraint

In 2025 the binding constraint on agent context was token *availability* — how many tokens fit, and how reliably the model attended to the middle of them. As of this week (Opus 4.7 promotional pricing ending on 2026-04-30 with a **15× premium-request multiplier** per the [GitHub Changelog](https://github.blog/changelog/2026-04-16-claude-opus-4-7-is-generally-available/)), the binding constraint for autonomous loops has shifted to *spend rate*.

Architectural implication: the per-loop context footprint should shrink so that parallel narrow loops fit inside the same dollar budget. AIDE's `utilization_ratio` (single-file-as-fraction-of-effective-context) is the right knob. We tighten it from 0.03 to 0.02 — a 33% reduction that compounds with parallelism.

**This is symmetric with P1-T2.** P1-T2 specified the *cost-decrease* direction ("relax the budget when tokens get cheap"). P1-T4 (new) specifies the *cost-increase* direction. Asymmetric calibration triggers were a latent bug; this cycle closes them.

### Claim 2 — Benchmark authority must be tiered before methodology calibration

The first Claude draft treated a secondary SWE-bench Pro spread of **19.2 percentage points** as calibration-grade evidence. Codex review could not reproduce that number from the official [Scale public](https://labs.scale.com/leaderboard/swe_bench_pro_public) or [Scale private](https://labs.scale.com/leaderboard/swe_bench_pro_private) leaderboards on 2026-05-04. The official public top-3 spread is 7.2pp; the official private top-3 spread is 3.7pp. Both are below the proposed 15pp threshold.

Architectural implication: P4 (Knowledge DRY, Code WET-tolerant) still carries a real unstated sub-assumption — that one Knowledge-DRY guideline transfers across vendors — but this week's official benchmark evidence does **not** prove that assumption has failed. The right change is to make vendor portability a monitored validity condition, while keeping the current condition satisfied until official contamination-resistant leaderboards cross the threshold.

The stronger methodology claim is about **source tiering**. Vendor launch claims, official benchmark leaderboards, secondary trackers, and community posts should not carry equal weight in `principle-metadata.yaml`. Calibration must prefer official benchmark leaderboards for benchmark deltas, use vendor claims as product-surface evidence, and use HN/social signals only as qualitative pressure.

P4-VC1 and P4-T2 remain useful as a tracked surface, but `P4-VC1.status` is corrected to `true` in this cycle. The methodology body of `docs/en/AIDE-METHODOLOGY.md` is *not* changed — body changes require a later review with calibration-grade evidence.

### Claim 3 — Same-vendor build/attack agents force structural Axiom A2

This week Anthropic shipped both Claude Security (defensive build agent, Apr 30 / May 1) and the Claude Mythos Preview (offensive vulnerability-discovery agent). Same vendor, same training lineage, same potential blind spots — but rolling out as if they were independent.

Architectural implication: AIDE's A2 (Adversarial Separation) is empirically vindicated, but it must be enforced at *vendor* granularity, not *model* granularity. Two Anthropic models reviewing each other are not adversarially separated even if their model IDs differ. The current axiom statement ("different models or different vendors") admits both readings; the safer reading is *different vendors* whenever a same-vendor pair could share a training-data substrate.

This is **not a metadata change this cycle** — A2 is immutable per axiom doctrine. It is logged here as the next deliberation surface for RFC consideration. RFC-0002 §v2_adaptations already names a Red Team Agent slot; the Mythos rollout is the empirical exhibit that promotes that slot from "specified" to "non-negotiable".

## Signals that informed but did not move a dial

- **Google subagents in Gemini CLI; Agents CLI; ADK Skills; ADK for Java 1.0** — first major vendor adopting subagent topology mirroring feature boundaries. Reinforces P2 (Locality of Behavior) without firing a numeric trigger.
- **OpenAI on AWS — Codex + Managed Agents in Bedrock** — cross-cloud agent identity is now a real surface. P10 (Meta-Code as First-Class) already covers the AGENTS.md side; will revisit when Bedrock publishes a state-format spec.
- **Dirac OSS topping TerminalBench on Gemini-3-flash-preview (HN 392 pts)** — the strongest weekly exhibit for "structure beats raw model size" (P3, P8). Exhibit-grade, not metadata-moving.

These signals matter for the next monthly Evolution Engine charter, but they did not produce a defensible quantitative threshold this week.

## What this cycle ships

| File | Change | Axiom enforced |
|---|---|---|
| `principle-metadata.yaml` (P1) | utilization_ratio 0.03 → 0.02; max_file_lines 500 → 333; new VC4 + T4 + evolution_history entry | A3 (quantitative evidence: 15× multiplier) |
| `principle-metadata.yaml` (P4) | new VC1 + T2 + evolution_history entry; current status corrected to true by Codex review | A3 (official Scale spreads below 15pp; secondary 19.2pp claim rejected) |
| `evolution/history/2026-05-04-weekly-synthesis.yaml` | first audit entry ever; signal scoring + reversal path | A1 (named git revert) + A5 (timestamps + source health) |
| `rfcs/0004-cost-pressure-and-vendor-portability.md` | draft RFC formalizing the structural change | A4 (awaits different-vendor consensus) |

The English methodology document and its Korean mirror are **not** edited in this cycle. Numeric calibration belongs in `principle-metadata.yaml`; the doc body changes only when a different-vendor agent has co-signed (RFC-0003 §4.3).

## Open questions for the reviewer

A different-vendor reviewing agent should explicitly accept or reject:

1. Is `utilization_ratio = 0.02` empirically supported, or should it be derived from the cost multiplier (e.g. `0.03 / sqrt(multiplier / 5)`) to keep recovery automatic when prices fall?
2. Is the 0.15 (15pp) threshold for P4-VC1 the right knee in the curve, or should it be benchmark-relative (e.g. 1.5× the long-run median spread)?
3. Should the Red Team Agent slot graduate from RFC-0002 §v2_adaptations into a first-class enforcement check in `axioms.yaml::A2.enforcement.checks`?

These are intentionally framed as falsifiable choices — A3 (Empiricism) requires that the reviewer's verdict be backed by data, not preference.

---

**Next weekly cycle**: 2026-05-11. The CI-machine sense pass runs at 00:00 UTC; this curator session runs after. Source health from this week was clean (12 machine-fetched + 4 curator-added; 0 fetch failures), so no sensor remediation is queued.
