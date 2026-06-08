- RFC Number: 0005
- Title: Durable Agent Context as a First-Class Adaptive Surface
- Agent Used: Claude Code on web
- Agent Model: claude-opus-4-7
- Research Method: 2026-06-08 weekly intel synthesis covering 2026-05-11 → 2026-06-01 four-week back-catalog (no curator pass in that window) + 2026-06-08 machine digest
- Date: 2026-06-08
- Status: Draft (awaits different-vendor reviewer per Axioms A2 / A4)

## Summary

This RFC introduces a single structural change to `principle-metadata.yaml`: a monitored adaptive surface for **durable agent context** — the property that an agent's runtime state survives sessions, crashes, and human approval pauses without context loss. Three frontier-vendor releases over four weeks have promoted this property from a research-stage curiosity to a vendor-table-stakes assumption, but no existing AIDE principle names it.

The change is structural, not numeric. No `current_values` numeric is moved; one `validity_condition` and one `invalidation_trigger` are proposed for attachment to either P3 (Functional Core, Structural Shell) or P10 (Meta-Code as First-Class). The reviewer is asked to pick the attachment point in Open Question 1 of the accompanying research note.

This RFC remains draft until a different-vendor scheduled agent countersigns per RFC-0003 §4. No body edit to `docs/en/AIDE-METHODOLOGY.md` or its Korean mirror is proposed in this cycle.

## Motivation

### 1. The same architectural primitive shipped three times in four weeks

Across `evolution/intel/weekly-2026-05-11.md` → `weekly-2026-06-01.md`, Google ADK announced the same durability primitive in three distinct framings:

| Week | Title | URL |
|---|---|---|
| 2026-05-11 | Reduce friction and latency for long-running jobs with Webhooks in Gemini API | https://blog.google/innovation-and-ai/technology/developers-tools/event-driven-webhooks/ |
| 2026-05-18 / 05-25 / 06-01 | Build Long-running AI agents that pause, resume, and never lose context with ADK | https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/ |

OpenAI's enterprise Codex case-study series in the same window (Cisco, Endava, Braintrust, Virgin Atlantic, Ramp, Dell, Databricks, NVIDIA, Sea, Singular Bank, Parloa, Simplex, Tax-agents, Warp, plus the "Work with Codex from anywhere" / "Codex on Windows sandbox" pair) describes the same property from the deployment side — enterprise agent workflows now span weeks, not single sessions, and must survive infrastructure events.

A signal that appears in 3+ consecutive weekly digests across two vendors crosses AIDE's empirical bar for a structural surface change (per the back-catalog accounting in `research/en/2026-06-08-weekly-synthesis.md`, Claim 1).

### 2. No existing AIDE principle names durable runtime state

The structural gap, audited against the 10 principles:

| Principle | Does it cover durable agent runtime state? |
|---|---|
| P1 Context Budget | No — `effective_context_tokens` is a single-session quantity. |
| P2 Locality of Behavior | No — operates on source layout, not runtime state. |
| P3 Functional Core, Structural Shell | **Partially** — names the side-effect boundary but does not specify that boundary-state must be durable across sessions. |
| P4 Knowledge DRY | No. |
| P5 Test as Specification | No. |
| P6 Progressive Disclosure | No. |
| P7 Deterministic Guardrails | No. |
| P8 Observability as Structure | **Partially** — names the audit-trail surface but treats persistence as an emergent property of the logging layer, not as an enforced structural requirement. |
| P9 Security by Structure | No. |
| P10 Meta-Code as First-Class | **Partially** — covers AGENTS.md / CLAUDE.md / GEMINI.md / `manifest.yaml` as versioned *configuration*, but `manifest.yaml::ai_development` does not yet have a slot for *runtime state schema*. |

The closest existing landing is P10. The lighter-touch landing for this RFC is to add a P10 validity_condition that names runtime-state durability as an explicit assumption, monitored against the percentage of leading vendors that ship a first-class pause/resume primitive.

### 3. The cost of waiting

If durable context is promoted from "vendor-shipped feature" to "vendor-required architecture" and AIDE is silent, three consequences follow:

1. **L4 / L5 autonomy levels in `principle-metadata.yaml::autonomy_levels` become un-shippable.** L4 ("System Architect") and L5 ("Autonomous Developer") implicitly assume the agent's working memory survives between phases of the SDLC. Without a durable-state requirement, L4/L5 are checklist labels with no architectural backbone.
2. **AGENTS.md governance fragments.** Vendors will each invent their own runtime-state schema; the cost in P4 vendor-portability terms is concrete. RFC-0004 already opened P4-VC1 for this concern; the present RFC widens it from "knowledge spec portability" to include "runtime-state portability".
3. **Axiom A1 (Reversibility) becomes harder to enforce.** A revert is meaningful only over the unit the system treats as "state". If runtime state is implicit, revert semantics are ill-defined.

## Detailed Design

### Proposal A (preferred, lighter-touch) — Attach to P10

**File**: `principle-metadata.yaml`, `principles.meta-code`

Add a `validity_conditions` block (P10 currently has none) and an `invalidation_triggers` block (also currently empty):

```yaml
  meta-code:
    id: P10
    # ... unchanged fields above ...

    validity_conditions:
      - id: "P10-VC1"
        condition: "vendors_with_first_class_pause_resume <= 1"
        description: |
          P10 currently treats AGENTS.md / CLAUDE.md / GEMINI.md / manifest.yaml as
          the meta-code surface. The implicit assumption is that *runtime state* is
          an emergent artifact of the agent platform, not part of the meta-code that
          the methodology must specify. That assumption holds while at most one
          frontier vendor ships pause/resume as a first-class primitive.
        status: false  # 2026-06-08: Google ADK shipped pause/resume (3 weekly digests); OpenAI enterprise Codex case studies require equivalent persistence
        last_checked: "2026-06-08"

    invalidation_triggers:
      - id: "P10-T1"
        type: vendor_release
        source: "Anthropic / OpenAI / Google agent SDK releases"
        condition: "vendors_with_first_class_pause_resume >= 2"
        action: |
          Widen P10's meta-code surface to include a runtime-state schema slot.
          Concretely: extend manifest.yaml::ai_development to include a
          runtime_state: section specifying (a) state durability boundary, (b)
          resumption protocol, (c) state schema version. Treat AGENTS.md / CLAUDE.md
          updates that change runtime-state-affecting instructions with the same CI
          eval-suite enforcement that already gates Tier 1 meta files.
        severity: major
```

`current_values` are NOT modified by this RFC. `instruction_compliance_inflection_point` (300) is unchanged.

### Proposal B (alternative, structural) — Attach to P3 v2_adaptations

**File**: `principle-metadata.yaml`, `principles.functional-core`

P3 is permanent (tier: permanent) and has no `v2_adaptations` block today. The proposal would add one:

```yaml
  functional-core:
    id: P3
    tier: permanent
    # ... unchanged fields above ...

    v2_adaptations:
      structural_shell:
        v1: "Side-effect boundary is a logical structure (handlers, repositories)."
        v2: |
          Side-effect boundary is also a *durability* boundary. Agent runtime state
          at the boundary must be: (1) serializable, (2) versioned, (3) resumable.
          Concretely, store/handler functions that participate in long-running flows
          must expose a state-snapshot interface compatible with the platform's
          pause/resume primitive.
      durability_invariant:
        v1: "Implicit — process state lives in memory."
        v2: |
          Explicit — every long-running agent flow has a named state surface that
          can survive crashes, sessions, and approval pauses. The structural shell
          is responsible for marshaling this state across the boundary; the pure
          core remains unaware of persistence.
```

Proposal B is heavier — it modifies a permanent principle's adaptation block — but is structurally cleaner because durability *is* a property of the side-effect boundary, not of the meta-code.

### Out of scope for this RFC

- **No `axioms.yaml` change.** A1–A5 statements unchanged.
- **No methodology body edit.** `docs/en/AIDE-METHODOLOGY.md` and the Korean mirror are not edited. Body edits await a different-vendor reviewer's countersignature on this RFC (RFC-0003 §4.3).
- **No new principle (P11).** A durable-context principle on its own could be defensible long-term, but a single curator pass should not introduce a new top-level principle; the existing adaptive surface of P10 (Proposal A) or the v2_adaptation surface of P3 (Proposal B) is sufficient to monitor the signal.
- **No `current_values` numeric change.** The signal is structural, not numeric. The reviewer is invited to accept the validity_condition/trigger pair; numeric calibration follows in a later cycle once a benchmark for "runtime-state durability under crash" exists.

## Evidence

| Claim | Metric | Value | Source |
|---|---|---|---|
| Google ADK shipped pause/resume as a first-class primitive | Weekly digests featuring the announcement | 3 (2026-05-18, 2026-05-25, 2026-06-01) | `evolution/intel/weekly-2026-05-{18,25}.md`, `weekly-2026-06-01.md` |
| Google complemented with event-driven webhooks for long-running jobs | Weekly digest 2026-05-11 | 1 mention | `evolution/intel/weekly-2026-05-11.md` |
| OpenAI enterprise Codex cases describing multi-day / multi-session workflows | Distinct case studies across 4 weeks | 14 enterprise stories | `evolution/intel/weekly-2026-05-{11,18,25}.md`, `weekly-2026-06-01.md` |
| OpenAI deployment surface for durable agent work | "Work with Codex from anywhere" + "Codex on Windows sandbox" pair | 2026-05-18 | `evolution/intel/weekly-2026-05-18.md` |
| Vendors with first-class pause/resume in this window | count | 1 (Google) explicitly; 1 (OpenAI) implied through enterprise architecture | derived from sources above |
| Source health | Sources reached per week (2026-05-11 → 06-01) | 28/32 | weekly digest source-health blocks |
| Source health | Sources reached on 2026-06-08 (curator sandbox) | 0/32 — production runner is canonical | `evolution/intel/weekly-2026-06-08.md` |

All evidence is reproducible from the linked weekly digests, which are permanent audit artifacts under `evolution/intel/`.

## Impact Assessment

### Affected principles

| Principle | Change under Proposal A | Change under Proposal B |
|---|---|---|
| P3 (Functional Core, permanent) | Unchanged | New `v2_adaptations` block (structural_shell, durability_invariant) |
| P10 (Meta-Code, adaptive) | New VC1 + T1; `current_values` unchanged | Unchanged |
| P1, P2, P4, P5, P6, P7, P8, P9 | Unchanged | Unchanged |

### Affected axioms

None. A1 (Reversibility) is *strengthened* in spirit by either proposal: naming the runtime-state surface makes revert semantics well-defined.

### Affected adopters

- **AIDE v2.0 / v2.1 adopters using single-session agent flows**: no immediate change. Both proposals are monitoring surfaces; today they record an assumption, they do not yet require a runtime-state schema.
- **AIDE adopters running L4 / L5 autonomy levels in production**: see this RFC as an early signal that L4/L5 will eventually require an explicit runtime-state schema in `manifest.yaml`. Begin treating long-running agent state as Tier 1 meta-code.
- **Tooling integrators (Genkit / ADK / Codex / Claude Code)**: under Proposal A, the eventual `runtime_state:` slot in `manifest.yaml::ai_development` becomes the documented integration point.

## Alternatives Considered

### Alt 1 — Do nothing this cycle, defer to monthly Evolution Engine

Rejected. The whole purpose of RFC-0003 was to remove the monthly bottleneck. The signal has now persisted 3+ weeks across two vendors, which is the empirical bar (per `research/en/2026-06-08-weekly-synthesis.md`). Deferring would replicate the failure pattern RFC-0003 §1 documented.

### Alt 2 — Introduce a new principle P11 (Durable Context)

Rejected for this cycle. A new top-level principle is a larger structural commitment than a single curator pass can responsibly make. Proposal A's lighter-touch landing on P10 is enough to monitor the signal; the upgrade path to a P11 remains open if Proposal A's VC1 trips and the response action proves too narrow.

### Alt 3 — Numerically tighten P1's `utilization_ratio` to model state survival overhead

Rejected. The signal does not describe a context-budget pressure — it describes a *structural property* of the agent runtime. Pushing it onto P1's numeric dial would be a category error.

### Alt 4 — Promote durability into `axioms.yaml`

Rejected. Axioms are immutable per A4 doctrine. The whole point of the adaptive principle layer is to absorb structural signals like this without touching axiom statements.

## Reviewer Protocol

Per RFC-0003 §4.4, a different-vendor scheduled agent (Codex on OpenAI, or a Gemini scheduler when one ships) opens a PR review with a structured verdict on this RFC, carrying model ID, quantitative justification, and an explicit Approve / Request-Changes / Block choice on **each of the three Open Questions** in `research/en/2026-06-08-weekly-synthesis.md`. Specifically:

1. Reviewer must pick **Proposal A vs Proposal B** for this RFC's attachment surface.
2. Reviewer must Accept / Request-Changes / Block the proposed VC1 + T1 (Proposal A) or v2_adaptations block (Proposal B) wording.
3. Reviewer must comment on the "vendors_with_first_class_pause_resume >= 2" threshold — is "2 vendors" the right knee in the curve, or should it be "any one of the top-3 frontier vendors", or a stronger criterion?

Until the countersignature lands, this PR remains a draft. Per A4, a 1:1 vendor split blocks the change with no auto-resolution.
