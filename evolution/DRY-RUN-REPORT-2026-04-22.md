# AIDE Evolution Engine — Dry-Run Report (2026-04-22)

> **Dry-run, not a real evolution cycle.** This report was produced by a single Claude Code session acting as all three deliberation agents. It is intentionally **non-compliant with Axioms A2 (Adversarial Separation) and A4 (No Single Authority)** and **does not modify `principle-metadata.yaml`**. It exists to exercise the pipeline end-to-end with real 2026 benchmark data.

## What this run did

| Phase | Action | Result |
|---|---|---|
| **SENSE** | WebSearch pulled real 2026 benchmark, model release, and pricing data, then wrote to `evolution/benchmarks/*.yaml` | 0 invalidation triggers activated; 3 soft signals recorded |
| **DELIBERATE** | Single Claude session played Research, Adversary, and Synthesis roles | 3 proposals → 1 defer, 1 modify-to-noop, 1 accept-as-log |
| **VALIDATE** | Empirical gate intentionally skipped | Gate = `NOT_RUN`; no sandbox exists |
| **APPLY** | Not attempted | `principle-metadata.yaml` untouched |

## Headline findings from real 2026 data

- **SWE-bench Verified**: Claude Mythos Preview 93.9 %, Claude Opus 4.7 87.6 %, GPT-5.3 Codex 85 % — average across 86 models ≈ 64 %.
- **SWE-bench Pro (hard, multi-file)**: frontier models cap at ~23 % public / ~15-18 % private. Multi-file resolution rate is still an order of magnitude below P2's `> 0.90` trigger.
- **Long context (RULER / MRCR v2)**: frontier 1 M windows retain ~60-70 % of advertised capacity. Gemini 3.1 Pro drops to 26 % retrieval at 1 M; Llama 4 Scout advertises 10 M but degrades past 1.4 M.
- **Frontier pricing (input $/M tokens)**: GPT-5.3 Codex $1.75, GPT-5.4 $2.50, Gemini 3.1 Pro $2.00 (≤ 200K) / $4.00 (> 200K), Claude Sonnet 4.6 $3.00, Claude Opus 4.7 $5.00. Median ~$2.85 — still ~28× P1-T2's $0.10/M trigger.

## Invalidation trigger evaluation

| Trigger | Condition | Observed | Fires? |
|---|---|---|---|
| P1-T1 | `effective_context_at_95_accuracy > 5 M` | ~1.0 M | ❌ |
| P1-T2 | `avg_token_cost_per_million_input < $0.10` | $2.85 | ❌ |
| P1-T3 | `litm_severity_index < 0.1` | ~0.35 | ❌ |
| P2-T1 | `multi_file_resolution_rate > 0.90` | 0.23 | ❌ |
| P2-T2 | `multi_hop_reasoning_accuracy > 0.80` | ~0.25 | ❌ |
| P4-T1 | `context_budget_utilization < 0.3` | unmeasurable | ❌ |
| P6-T1 | `attention_diffusion_in_long_context < 0.1` | ~0.35 | ❌ |

**Net: 0 / 7 triggers active.** The adaptive principles are still within their current validity envelope.

## Soft signals (no trigger, but worth logging)

- **SS-1** — `P1.effective_context_tokens` at 800 K is stale vs. ~1.0 M realistic effective capacity.
- **SS-2** — `P2.multi_hop_reasoning_accuracy = 0.15` is defensible using SWE-bench Pro private rate (0.15-0.18), so refreshing it produces no change to stored values — a true no-op.
- **SS-3** — **A5 observability gap**: `P1.max_file_lines.value = 500` but the formula `round(800 000 / 18 × 0.03) = 1333`. Stored value diverges from its own self-calibration formula.

## Deliberation outcome

| Proposal | Research verdict | Adversary verdict | Synthesis verdict |
|---|---|---|---|
| PROP-1 — refresh `effective_context_tokens` 800 K → 1 M | propose | accept (with rename) | **defer** (95 %-accuracy naming mismatch) |
| PROP-2 — refresh `multi_hop_reasoning_accuracy` 0.15 → 0.23 | propose | modify (use private 0.15) | **modify → no-op** |
| PROP-3 — log `max_file_lines` formula/value gap | propose (log-only) | accept | **accept** |

**Synthesis set `proceed_to_validation: false`** citing single-vendor dry-run → blocks any auto-apply. This is the correct outcome under A2/A4.

## Axiom compliance summary

| Axiom | Status | Notes |
|---|---|---|
| A1 Reversibility | ✅ | All proposals are trivially revertable YAML edits; none applied. |
| A2 Adversarial Separation | ❌ | All three roles = one Anthropic session. **PR blocker.** |
| A3 Empiricism | ⚠️ | Real benchmark evidence cited, but PROP-1 mislabelled threshold; PROP-2 used the wrong subset. |
| A4 No Single Authority | ❌ | Single agent made all decisions. **PR blocker.** |
| A5 Self-Observability | ✅ | Full audit trail under `evolution/benchmarks/`, `evolution/deliberation/`, `evolution/sandbox/`. |

## What this PR should and should not do

**Should**
- Land the pipeline artifacts as a single-commit demonstration that the Evolution Engine produces sensible output when fed real 2026 data.
- Surface the A5 observability gap in `P1.max_file_lines` (value ≠ formula) for a follow-up RFC.
- Stay **draft**.

**Should not**
- Merge to `main`.
- Modify `principle-metadata.yaml`, `axioms.yaml`, or any documentation.
- Be treated as evidence for any methodology change under A3.

## Follow-ups suggested

1. **Fix `collect_benchmarks.py`**: currently emits placeholder `None` metrics — wire it to real APIs (SWE-bench, RULER, vendor pricing) so monthly runs aren't empty.
2. **Fix `check_triggers.py`**: currently hard-codes `activated: False` — implement actual condition evaluation against `latest.yaml`.
3. **Bootstrap empirical validation sandbox**: required before any real apply cycle can run.
4. **Open RFC**: reconcile the `max_file_lines` stored value vs. formula divergence (either update stored value to formula output, or document that stored values are conservative policy caps that intentionally diverge).
5. **Enable Evolution Engine workflow triggers**: `aide-evolution-engine.yml` schedule/dispatch is currently commented out pending Anthropic OAuth policy clarification.

## Data sources

- SWE-bench Verified leaderboard, Vals.ai, Epoch AI, BenchLM, llm-stats, Simon Willison's Feb 2026 SWE-bench note
- SWE-bench Pro public leaderboard (Scale)
- RULER / MRCR v2 consolidated long-context reporting (awesomeagents.ai, claude5.com, Vellum)
- Vendor pricing pages (Anthropic, OpenAI Developers / Codex, Google Vertex AI), TokenCost, PricePerToken, OpenRouter

---

*Generated 2026-04-22 by a single Claude Code session — not a compliant Evolution Engine cycle.*
