- RFC Number: 0004
- Title: Cost-Pressure Variable in P1 + Vendor-Portability Validity Condition in P4
- Agent Used: Claude Code on web
- Agent Model: claude-opus-4-7
- Research Method: 2026-05-04 weekly intel digest scoring + per-platform scheduled curator pass per RFC-0003 §4
- Date: 2026-05-04
- Status: Draft

## Summary

This RFC formalizes two principle-metadata changes triggered by the 2026-05-04
Weekly Intel digest. Together they teach AIDE's adaptive principles to respond
to two new realities of frontier-vendor agent platforms: (1) per-token cost
has re-entered the binding-constraint regime, and (2) contamination-resistant
benchmark spreads have crossed the point where one vendor-agnostic Knowledge-DRY
specification can no longer be assumed to transfer across vendors.

The numeric changes have been applied in this RFC's accompanying PR. This
document exists to make the *structural* change reviewable by a different-vendor
agent before merge, per Axioms A2 (Adversarial Separation) and A4 (No Single
Authority).

## Motivation

### 1. P1 invalidation triggers were asymmetric

P1's only market trigger (P1-T2) modeled the cost-decrease direction:

> "average_token_cost_per_million_input < 0.10 → recalibrate utilization_ratio
> upward (relax budget constraint)"

The reverse — what AIDE should do when premium-request multipliers spike — was
unspecified. This week's signal made the gap operationally relevant: Anthropic's
[GitHub Changelog (2026-04-16, effective 2026-04-30)](https://github.blog/changelog/2026-04-16-claude-opus-4-7-is-generally-available/)
set Claude Opus 4.7 to a **15× premium request multiplier**. The digest treats
this as a P1 re-tune trigger; the trigger had no formal symmetric counterpart.

### 2. P4 had an unstated "vendor portability" sub-assumption

P4 (Knowledge DRY, Code WET-tolerant) is written as if a single Knowledge-DRY
specification — one AGENTS.md / CLAUDE.md / GEMINI.md authoring contract —
transfers across vendors at comparable quality. That sub-assumption was free
when frontier capability was tightly clustered. SWE-bench Pro
([Scale SEAL leaderboard](https://labs.scale.com/leaderboard/swe_bench_pro_public))
top-3 spread reaching **19.2pp** (Mythos 77.8% / Opus 4.7 64.3% / GPT-5.5 58.6%)
on a contamination-resistant private set is the first quantitative signal that
this assumption is breaking. Pro is the trustworthy frontier benchmark because
it cannot be gamed by training-data overlap.

A 19.2pp spread also stresses Axiom A2 (Adversarial Separation): a reviewer
model 19pp below the author model on this kind of task may not produce
review verdicts that A2 was intended to extract.

## Detailed Design

### Change 1 — P1 cost-pressure variable

**File**: `principle-metadata.yaml`, `principles.context-budget`

| Field | Before | After |
|---|---|---|
| `current_values.max_file_lines.value` | 500 | 333 |
| `current_values.max_file_lines.variables.utilization_ratio.value` | 0.03 | 0.02 |
| `validity_conditions[]` | (3 entries) | (4 entries) — adds **P1-VC4**: `premium_request_multiplier_for_top_tier_model < 10.0` |
| `invalidation_triggers[]` | (3 entries) | (4 entries) — adds **P1-T4**: `multiplier ≥ 10x → tighten utilization_ratio` |
| `evolution_history[]` | `[]` | one entry with quantitative evidence |

Rationale for 0.02 specifically: it halves the per-file context footprint at
roughly the same factor that the cost has compressed delivery flexibility.
Three open questions in `research/en/2026-05-04-weekly-synthesis.md` ask the
reviewer to either accept this constant or replace it with a multiplier-derived
formula.

### Change 2 — P4 vendor-portability validity condition

**File**: `principle-metadata.yaml`, `principles.knowledge-dry`

| Field | Before | After |
|---|---|---|
| `validity_conditions[]` | (none) | new section with **P4-VC1**: `swe_bench_pro_top3_spread < 0.15` |
| `invalidation_triggers[]` | (1 entry) | (2 entries) — adds **P4-T2**: spread > 0.15 → soften vendor-portability sub-assumption (severity: major) |
| `evolution_history[]` | `[]` | one entry with quantitative evidence |

The action of P4-T2 is the substantive change: it permits AGENTS.md / CLAUDE.md /
GEMINI.md to *diverge* on calibration details (test density, decomposition
depth, when to prefer pure-functional decomposition) while the underlying
knowledge invariants remain single-source. The spec layer separates from the
calibration layer.

### Out of scope for this RFC

- **No methodology body edit.** `docs/en/AIDE-METHODOLOGY.md` and the Korean
  mirror are not edited in this cycle. RFC-0003 §4.3 permits numeric
  calibration to ship via `principle-metadata.yaml` alone; body edits require a
  different-vendor agent's countersignature first.
- **No axiom statement edit.** A2 stays immutable. The empirical case for
  treating "different vendor" rather than "different model" as the A2
  granularity is logged in the audit entry under signal S3 for the next
  monthly Evolution Engine cycle to consider.
- **No Red Team Agent enforcement-check edit.** RFC-0002 §v2_adaptations
  already specifies the slot; promoting it to `axioms.yaml::A2.enforcement.checks`
  is a separate, larger change.

## Evidence

| Claim | Metric | Value | Source |
|---|---|---|---|
| Cost regime shifted | Opus 4.7 premium request multiplier | 15× | [GitHub Changelog 2026-04-16](https://github.blog/changelog/2026-04-16-claude-opus-4-7-is-generally-available/), effective 2026-04-30 |
| Cost regime shifted | Effective input cost at 15× | ~7.5 USD/M tokens | derivation in audit entry, S4 |
| Capability stratifying | SWE-bench Pro top-3 spread | 0.192 | [Scale SEAL leaderboard](https://labs.scale.com/leaderboard/swe_bench_pro_public) |
| Capability stratifying (informational) | SWE-bench Verified top-3 spread | 0.089 | [llm-stats](https://llm-stats.com/benchmarks/swe-bench-verified) (contamination-flagged; included only as comparator) |
| Source health | Machine-fetched signals | 12 | `evolution/intel/weekly-2026-05-04.md` |
| Source health | Curator-added signals | 4 | same |
| Source health | Fetch failures | 0 | same |

All evidence is reproducible from the linked URLs and the committed digest.

## Impact Assessment

### Affected principles

| Principle | Change |
|---|---|
| P1 (Context Budget, adaptive) | Numeric: `max_file_lines` 500 → 333; `utilization_ratio` 0.03 → 0.02. Structural: validity_condition + trigger pair closes the asymmetry in market-direction handling. |
| P4 (Knowledge DRY, adaptive) | Structural: validity_condition + trigger pair makes "vendor portability" an explicit, falsifiable assumption rather than a tacit one. No numeric value of `max_utility_duplication` changes. |
| P2, P3, P5–P10 | Unchanged. |

### Affected axioms

None. A1–A5 statements are unchanged. A1 reversibility is preserved: the
audit entry names the exact `git revert` and ships a smoke test.

### Affected adopters

- **AIDE v2.0 / v2.1 adopters with file caps anchored to the metadata file**:
  the `max_file_lines` recommended value drops from 500 to 333. Existing 500-line
  files do not become non-compliant overnight (the bound still allows up to 5000),
  but new feature work should target the lower number. Adopters who anchored to
  the doc body's "200–300 recommended / 500 upper" guidance see no change —
  500 remains the bound.
- **Adopters who use AGENTS.md / CLAUDE.md / GEMINI.md as a single shared file**:
  P4-T2 explicitly *permits* divergence on calibration details. This is permissive,
  not mandatory — single-vendor adopters may continue with one shared file.

## Alternatives Considered

### Alt 1 — Edit the methodology body in lockstep this cycle

Rejected for this PR. RFC-0003 §4.3 lets numeric calibration ship without a
body edit, and a single-vendor draft should not move the body. Once a
different-vendor reviewer countersigns this RFC, a follow-up PR can edit the
body in lockstep.

### Alt 2 — Replace `utilization_ratio = 0.02` with a formula

Considered: `utilization_ratio = 0.03 / sqrt(multiplier / 5)`, where
`multiplier = 5` is the historical median. This recovers automatically when
the multiplier drops. Reviewer's call — listed as open question 1 in the
research note. Defaulted to a constant to keep the diff minimal and reviewable
under A3.

### Alt 3 — Wait for the monthly Evolution Engine cycle

Rejected. RFC-0003's whole purpose was to remove the monthly bottleneck; this
RFC is the canonical case it was designed for. P1-T4's market trigger is
already firing as of 2026-04-30; deferring violates the spirit of A3 (act on
quantitative evidence when it lands).

### Alt 4 — Tighten P4 with a numeric `max_utility_duplication` change

Rejected. The SWE-bench Pro spread does not directly bear on utility-code
duplication counts — it bears on the assumption that one specification fits
all vendors. The right surface for that signal is a validity_condition +
trigger, not the duplication-count knob.

---

**Reviewer protocol**: A different-vendor scheduled agent (Codex on OpenAI, or
a Gemini scheduler when it ships) opens a PR review with a structured verdict
on this RFC. Per RFC-0003 §4.4, the verdict carries the reviewer's model ID,
quantitative justification, and an explicit Approve / Request-Changes / Block
choice. Until that countersignature lands, this PR remains a draft.
