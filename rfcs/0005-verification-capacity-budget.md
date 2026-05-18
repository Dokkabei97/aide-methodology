- RFC Number: 0005
- Title: Verification Capacity as a Co-Primary Constraint (The Verification Budget)
- Agent Used: Claude Code on web
- Agent Model: claude-opus-4-7
- Research Method: 2026-05-18 weekly intel digest scoring + per-platform scheduled curator pass per RFC-0003 §4
- Date: 2026-05-18
- Status: Draft (awaits different-vendor reviewer per Axioms A2 / A4)

## Summary

AIDE's founding text names the **Context Budget** as "the primary design
constraint" (P1). This RFC proposes that, for autonomous agent-led development,
the Context Budget is no longer the *only* primary constraint. When a human
leaves the inner loop, the binding constraint becomes **verification
capacity** — the rate at which generated change can be certified correct.

The proposal: introduce a **Verification Budget** as a co-primary structural
constraint. It has two parts. (1) A first-class limit on how much *unverified
change* an autonomous loop may have outstanding at once. (2) A structural
requirement that every delegated unit emit **agent-consumable verification
artifacts** — machine-checkable test reports, typed diffs, observability
traces — rather than artifacts only a human reviewer can interpret.

This RFC is **structural, not numeric**. It does not edit `principle-metadata.yaml`
and does not edit the methodology body. Per Axiom A3, a numeric Verification-Budget
value requires calibration-grade evidence, which this cycle's signals do not yet
provide. The RFC exists to make the structural direction reviewable by a
different-vendor agent before any value is set, per Axioms A2 and A4.

## Motivation

### 1. The bottleneck moved, and the methodology has not followed

AIDE was written for the regime where the hard part was *getting an agent to
produce a correct change*. P1 (Context Budget) is the right primary constraint
for that regime: fit the work inside the attention the model can reliably use.

Three independent signals in the 2026-05-12 → 2026-05-18 window say the
bottleneck has moved to *certifying* the change:

- **Lars Faye, "Agentic Coding Is a Trap"** (viral on HN / X / Threads). The
  explicit thesis: reading and reviewing agent output costs more than the
  generation it replaced, and the verification skill is the same skill the
  tooling erodes. AIDE need not accept the essay's pessimistic conclusion to
  accept its diagnosis of *where the cost now sits*.
- **Anthropic CI auto-fix**, shipped at Code w/ Claude 2026. Its stated design
  goal — *"the person who owns the PR is never going to see a red X"* — is the
  removal of a human verification step. The feature exists *because*
  verification is the step that does not scale with generation.
- **Prime Intellect's 2-week unattended run** of Codex and Claude Code on the
  nanoGPT speedrun. The agents executed thousands of steps and set a record,
  but could not themselves verify whether a direction was novel or sound. Step
  count was unbounded; judgement was the wall.

### 2. The autonomy ladder already depends on verification but does not budget it

`principle-metadata.yaml::autonomy_levels` defines L5 ("Autonomous Developer")
with the human role *"Output verification only"*, and L3 ("Feature Builder")
with *"Requirements + Final verification"*. Verification is already the
load-bearing human contribution at the top of the ladder — yet nothing in the
methodology bounds it, measures it, or requires the delegated work to be shaped
for cheap verification. The ladder names the dependency without budgeting it.

### 3. An unbudgeted verification gap is an A1 / A3 hazard

If an autonomous loop can generate change faster than anything can certify it,
the volume of *outstanding unverified change* grows without bound. That
directly threatens Axiom A1 (Reversibility): a revert is only safe if the state
being reverted *to* was itself verified. It also strains A3 (Empiricism): a
methodology that cannot measure its own verification throughput cannot make
empirical claims about how much delegation is safe.

## Detailed Design

This RFC proposes **three structural additions**. None is a numeric calibration;
each is a falsifiable structural commitment for the reviewer to accept or reject.

### Addition 1 — The Verification Budget as a co-primary constraint

Amend the framing of P1 so that AIDE recognises **two** primary design
constraints for agent-led development:

- **Context Budget** (existing) — bounds what one agent step can attend to.
- **Verification Budget** (new) — bounds how much *unverified change* an
  autonomous loop may hold outstanding before it must stop generating and let
  verification catch up.

The Verification Budget is a back-pressure mechanism. When outstanding
unverified change exceeds the budget, the loop blocks new generation — exactly
as a full Context Budget blocks new file growth. The two constraints are
symmetric: one bounds *input* attention, the other bounds *output* debt.

This RFC does **not** set the numeric value. It proposes the constraint exists
and is first-class. See Open Question 1.

### Addition 2 — Agent-consumable verification artifacts

A delegated unit (a feature directory, per AIDE's `types.ts` / `logic.ts` /
`handler.ts` / `*.test.ts` / `AGENTS.md` layout) must emit verification
artifacts that *another agent* can consume without a human in the path:

- machine-checkable test reports (pass/fail per property, not prose);
- typed, structured diffs that a reviewing agent can diff-check against the
  stated intent in `AGENTS.md`;
- observability traces (P8) sufficient to confirm runtime behaviour, not just
  compile-time shape.

This makes P5 (Test as Specification) and P8 (Observability as Structure)
*do double duty*: they already exist for humans; this addition requires them to
be structured for a verifying agent. It is the natural extension of P5's
existing v2 adaptation, "Agent A spec → Agent B implementation → Agent C
verification (Axiom A2)" — that pipeline only works if Agent C is handed
artifacts it can mechanically check.

### Addition 3 — A2 applies to the verification loop

The CI auto-fix pattern introduces an adversarial-separation hazard. If the
*same vendor* generates the code, observes its own CI failure, and auto-fixes
that failure, the generate→verify→fix loop is single-vendor end to end. A blind
spot shared by the generating model is shared by the fixing model.

This RFC proposes that AIDE state explicitly: **the agent that certifies a
change must be from a different vendor than the agent that generated it**,
whenever the verification is *judgement-based* (e.g. "is this the right fix?").
Where verification is a *deterministic oracle* (a type checker, a passing test
suite — P7's domain), A2 does not bind, because a deterministic oracle has no
training-data substrate to share. The line between the two is the substance of
Open Question 2.

### Out of scope for this RFC

- **No methodology body edit.** `docs/en/AIDE-METHODOLOGY.md` and the Korean
  mirror are not edited. RFC-0003 §4.3 requires a different-vendor
  countersignature before a body edit.
- **No `principle-metadata.yaml` edit.** No numeric Verification-Budget value
  is set; no validity condition or trigger is added. Per A3, that waits for a
  calibration-grade metric (Open Question 1).
- **No axiom statement edit.** A2 stays immutable. Addition 3 is a *reading* of
  A2's existing "different models or different vendors" clause, surfaced for
  the next monthly Evolution Engine cycle — consistent with how the 2026-05-04
  audit entry handled the same clause under signal S3.

## Evidence

| Claim | Metric / Evidence | Source |
|---|---|---|
| Verification is the cost centre | Viral essay; explicit thesis that review cost exceeds generation cost | [Agentic Coding Is a Trap — HN](https://news.ycombinator.com/item?id=48002442) · [essay](https://larsfaye.com/articles/agentic-coding-is-a-trap) |
| Vendors are engineering verification *out* of the loop | CI auto-fix design goal: "the PR owner never sees a red X" | [Code w/ Claude 2026 live blog](https://simonwillison.net/2026/May/6/code-w-claude-2026/) |
| Unattended loops out-generate judgement | 2-week run; record step count; no self-verified novelty | Prime Intellect nanoGPT speedrun (reported 2026-05) |
| Harness, not model, decides outcome | TB2.0 leader (GPT-5.5 82.0) ≠ SWE-bench Pro leader (Opus 4.7 64.3) | [tbench.ai](https://www.tbench.ai/leaderboard/terminal-bench/2.0) · [Scale SWE-bench Pro](https://labs.scale.com/leaderboard/swe_bench_pro_public) |
| Source health | Curator-verified signals: 9; machine-fetched: 0; fetch failures: 1 | `evolution/intel/weekly-2026-05-18.md` |

The HN essay's secondary "47% debugging decline" figure is **not** used as a
calibration input — it is an opinion-grade claim. It is cited only as evidence
that the *direction* of concern is shared widely enough to be a real signal.

## Impact Assessment

### Affected principles

| Principle | Effect |
|---|---|
| P1 (Context Budget, adaptive) | Reframed: from "the primary constraint" to "one of two co-primary constraints." No numeric value changes. |
| P5 (Test as Specification, permanent) | Reinforced: verification artifacts must be agent-consumable. Extends the existing v2 "Agent C verification" adaptation. |
| P7 (Deterministic Guardrails, permanent) | Reinforced: deterministic oracles are the A2-exempt verification path (Addition 3). |
| P8 (Observability as Structure, permanent) | Reinforced: traces become a required verification artifact, not only an ops aid. |
| P10 (Meta-Code as First-Class, adaptive) | Trigger/routine definitions are confirmed in-scope as meta-code (carried from the 2026-05-18 synthesis, Claim 1). |
| P2, P3, P4, P6, P9 | Unchanged. |

### Affected axioms

None edited. A1 (Reversibility) is *strengthened* in spirit — an unbudgeted
verification gap is identified as an A1 hazard. A2's existing clause is read,
not amended.

### Affected adopters

- Adopters at autonomy L1–L2 (human in the inner loop): no change — verification
  cost is still absorbed in human review.
- Adopters at L3–L5: the Verification Budget becomes a structural concern.
  Once a numeric value is set in a follow-up cycle, autonomous loops should
  apply back-pressure when outstanding unverified change exceeds it.
- Adopters running same-vendor CI auto-fix: Addition 3 recommends a
  different-vendor certifier for judgement-based verification. This is a
  recommendation in this draft, not an enforced gate.

## Alternatives Considered

### Alt 1 — Set a numeric Verification-Budget value now

Rejected for this cycle. Axiom A3 requires calibration-grade evidence before a
number enters `principle-metadata.yaml`. This fortnight's evidence is
directional. Setting a number now would repeat the mistake the 2026-05-04 cycle
caught and corrected (the secondary 19.2pp SWE-bench Pro claim). The structural
proposal can be reviewed without a number; the number follows once a metric
exists (Open Question 1).

### Alt 2 — Fold verification entirely into P5, with no new constraint

Rejected. P5 (Test as Specification) governs *how* a unit is specified and
verified. It does not govern *how much unverified change may accumulate across
units*. The Verification Budget is a system-level back-pressure limit; P5 is a
unit-level authoring discipline. They are complementary, not substitutes — but
the reviewer may disagree (Open Question 1).

### Alt 3 — Treat CI as a sufficient verifier and drop Addition 3

Rejected as stated, but partially correct. A *deterministic* CI oracle (types,
tests) genuinely needs no A2 separation. The hazard is specifically
*judgement-based* verification ("is this the right fix?"), which CI auto-fix
blends with the deterministic kind. Addition 3 draws that line rather than
discarding it. The reviewer is asked to confirm or move the line.

## Open Questions for the Reviewer

A different-vendor reviewing agent (Codex on OpenAI, a Gemini CLI scheduled
subagent, or — newly eligible this cycle — a Grok Build scheduled session)
should return a structured verdict on:

1. **Metric.** What measurable quantity should the Verification Budget bound —
   outstanding unverified diff lines, unverified feature-directories, unverified
   merged-but-unaudited PRs? The answer determines whether this becomes a new
   adaptive principle or a validity-condition layer on P5/P7.
2. **A2 line.** Where exactly is the boundary between deterministic verification
   (A2-exempt) and judgement-based verification (A2-bound)? Should
   `axiom-gate.yml` be able to detect a single-vendor generate→verify→fix loop?
3. **Autonomy gate.** Should the L4 → L5 transition in `autonomy_levels` be
   explicitly gated on a verification-throughput metric, rather than on model
   capability alone?

Per RFC-0003 §4.4, the verdict carries the reviewer's model ID, quantitative
justification, and an explicit Approve / Request-Changes / Block choice. Until
that countersignature lands, this PR remains a draft.
