- RFC Number: 0005
- Title: Verifier Isolation Pattern + Subagent Topology Mapping + Event/Trigger Surface for Meta-Code
- Agent Used: Claude Code on web
- Agent Model: claude-opus-4-7
- Research Method: 2026-05-11 weekly intel digest scoring + per-platform scheduled curator pass per RFC-0003 §4 + RFC-0002 v2.0 deliberation framework
- Date: 2026-05-11
- Status: Draft (single-vendor; awaits different-vendor reviewer per A2 / A4)

## Summary

This RFC formalizes three structural changes triggered by the 2026-05-11
Weekly Intel digest, all justified by the same week's vendor convergence.
Together they teach AIDE to *name* a pattern that has graduated from
axiom to vendor primitive, *map* a topology that all three frontier
vendors now ship, and *expose* an event surface that the next generation
of Meta-Code (AGENTS.md / CLAUDE.md / GEMINI.md) needs:

1. **Verifier Isolation Pattern** — a named structural pattern under
   A2 + A4 + P5 that captures "separate grader agent in its own
   independent context window, scoring against a developer-supplied
   rubric, with no access to the working agent's reasoning path".
2. **Subagent Topology Mapping** — a P2 sub-clause specifying the
   feature-directory ↔ vendor-subagent mapping, so the same AGENTS.md
   shape is consumable by Anthropic Multiagent Orchestration, Gemini
   CLI Subagents, and Codex MultiAgentV2 alike.
3. **Event/Trigger Surface for Meta-Code (P10)** — an enumerated set
   of repo-event kinds (PR / push / issue / check_run / workflow_run /
   discussion / release / merge_queue / schedule / api) and the
   AGENTS.md schema for binding agents and verifier-isolation rubrics
   to them.

This RFC is **structural** (introduces named patterns, mappings, and
schema), not numeric. It does not propose any change to
`principle-metadata.yaml` formulas, validity conditions, or invalidation
triggers. If the next-cycle different-vendor reviewer accepts these
structural changes, a follow-up RFC will add the corresponding
metadata slots (e.g., `P5.verifier_isolation`, `P10.event_trigger_surface`).

## Motivation

### 1. Outcomes graduated to public beta — the unnamed pattern needs a name

For the entire history of AIDE, A2 (Adversarial Separation) and A4 (No
Single Authority) have implied — but not named — a recurring tactical
pattern: when an agent finishes a task, do not ask the same agent to
self-grade. Spin up a fresh context, give it the rubric, let it grade.

This week ([Anthropic Outcomes public beta](https://9to5mac.com/2026/05/07/anthropic-updates-claude-managed-agents-with-three-new-features/),
[architectural analysis at Rick's Cafe AI](https://cafeai.home.blog/2026/05/10/anthropic-shipped-outcomes-and-real-story-is-verification-becoming-a-sku/))
the pattern shipped as a vendor primitive with measured numbers: a
**+10pp success rate on the hardest tasks**, with `.docx` +8.4% and
`.pptx` +10.1%. The architectural reason given by Anthropic is exactly
the one A2 / A4 imply — the grader has no knowledge of the working
agent's reasoning path, so its mistakes are uncorrelated.

The gap is that AIDE feature designers cannot reference the pattern by
name today. They have to re-derive it from axioms. Naming it as
**Verifier Isolation** lets it be cited from feature `AGENTS.md` files
without re-deriving (Progressive Disclosure, P6).

### 2. Subagent topology is now uniformly available — the mapping is the missing link

P2 (Locality of Behavior) prescribes a feature-directory shape.
Three independent vendor releases this cycle (Anthropic Multiagent
Orchestration ≤20 specialists shared filesystem, Gemini CLI Subagents
isolated context + curated tools, Codex MultiAgentV2 explicit
configuration) made the same architectural choice without coordinating.

Convergence at this scale is the strongest possible vendor-portability
signal. P4-VC1 (vendor portability validity condition) was added last
cycle as a *monitoring* surface; this cycle makes it a *productive*
surface — the AGENTS.md shape that today configures Claude Code and
Gemini CLI ought to also describe how feature directories map to
vendor subagents. One canonical mapping rule (1 feature dir → 1
subagent's working set) means one AGENTS.md authored against AIDE
spec is consumable by all three vendors without translation.

### 3. Routines + Auto Mode mean Meta-Code needs an Event/Trigger surface

P10 (Meta-Code as First-Class) currently treats AGENTS.md / CLAUDE.md
as configuration text. With Claude Code Routines binding agents to
`pull_request`, `push`, `issue`, `check_run`, `workflow_run`,
`discussion`, `release`, `merge_queue`, `schedule`, `api` triggers and
running on vendor cloud past laptop closure ([devops.com coverage](https://devops.com/claude-code-routines-anthropics-answer-to-unattended-dev-automation/)),
the configuration text needs an event-surface section — otherwise the
binding lives in vendor consoles and AIDE loses the in-repo invariant.

Auto Mode's two-stage classification of tool outputs ([InfoQ deep-dive](https://www.infoq.com/news/2026/05/anthropic-claude-code-auto-mode/))
is the security half of the same picture: when an agent wakes on a PR
event, it operates on untrusted PR content and needs structural
input-trust boundaries declared *before* it runs. The Event/Trigger
surface and the trust-boundary declaration belong together in
AGENTS.md.

## Detailed Design

### 3.1 Verifier Isolation Pattern (new named pattern)

Add to `docs/en/AIDE-METHODOLOGY.md` (and Korean mirror) a named pattern
section under the practice catalog, sitting between P5 and P9:

> **Verifier Isolation**. When an agent completes a task, evaluation
> runs in a *fresh* context window that has no access to the working
> agent's reasoning path. The verifier reads only:
> (a) the working agent's final output,
> (b) the rubric (structured success criteria, ideally executable),
> (c) the original task statement.
> The verifier may not read the working agent's intermediate notes,
> tool-call transcript, or any artifact produced during the working
> phase. When the verifier finds gaps, it pinpoints them and the
> working agent (or a successor) takes another pass.
>
> This is the intra-vendor expression of A2 / A4. It does not satisfy
> the inter-vendor requirement that A2 imposes at the RFC level (a
> different-vendor reviewer is still required for methodology
> changes). It does provide the per-task verification primitive that
> P5 (Test as Specification) presupposes.
>
> *Vendor-native realizations*: Anthropic Outcomes (public beta as of
> 2026-05-06); Gemini CLI Subagents with `/skills` evaluator skills;
> Codex MultiAgentV2 grader role. Authors should treat these as
> interchangeable backends for the same pattern.

Authoring contract: AGENTS.md may declare a `verifier:` block per
feature. The block names the rubric file (e.g.,
`features/payments/RUBRIC.md`) and the trigger condition
(`on: agent_complete`). When omitted, the default verifier is the
feature's `*.test.ts` suite — preserving backward compatibility with
P5 as currently written.

### 3.2 Subagent Topology Mapping (new P2 sub-clause)

Add to the P2 (Locality of Behavior) section of the methodology body:

> **Feature ↔ Subagent Mapping**. With subagent topology now a
> primitive across all three frontier vendors, AIDE's feature
> directories double as subagent specifications. The mapping is:
>
> | Feature directory artifact | Maps to subagent component |
> |---|---|
> | `AGENTS.md` | system prompt + role description |
> | `handler.ts` (boundary file) | curated tool surface |
> | `RUBRIC.md` (if present) | verifier-isolation rubric |
> | `*.test.ts` | verifier fallback when no RUBRIC.md |
> | `types.ts`, `logic.ts`, `store.ts` | working-set context |
>
> A *lead agent* (Anthropic terminology) / *primary session* (Gemini
> CLI terminology) / *root agent* (Codex terminology) is the project
> root's `AGENTS.md`. Specialists are spawned per feature directory
> when the lead agent decides the task touches that feature. The
> default mapping is **1 feature directory → 1 specialist invocation**
> per task; nothing prevents 1:N (e.g., one feature spawning a
> writing specialist + a test specialist) when the feature's
> AGENTS.md declares them.

The mapping is descriptive, not prescriptive: any vendor that ships
a different topology can still consume an AIDE-shaped repo by reading
the same artifacts in a different order.

### 3.3 Event/Trigger Surface for Meta-Code (new P10 sub-section)

Add to the P10 (Meta-Code as First-Class) section:

> **Event/Trigger Surface**. AGENTS.md may declare an `events:` block
> binding repo events to agents. The supported event taxonomy is the
> intersection of vendor implementations as of 2026-05:
>
> ```yaml
> # excerpt from a feature/payments/AGENTS.md
> events:
>   - on: pull_request.opened
>     agent: payments-reviewer
>     verifier: features/payments/RUBRIC.md
>     trust_boundary: untrusted_pr_content
>   - on: schedule
>     cron: "0 3 * * *"   # nightly
>     agent: payments-cleanup
>     verifier: features/payments/*.test.ts
>     trust_boundary: trusted_repo_state
>   - on: check_run.completed
>     agent: payments-fixer
>     verifier: features/payments/RUBRIC.md
>     trust_boundary: trusted_repo_state
>     gate: human_approval_for_destructive
> ```
>
> Supported `on:` values: `pull_request.{opened,synchronize,closed}`,
> `push`, `issue.{opened,commented}`, `check_run.completed`,
> `workflow_run.completed`, `discussion.created`, `release.published`,
> `merge_queue.entry`, `schedule`, `api`.
>
> Supported `trust_boundary:` values: `trusted_repo_state` (default),
> `untrusted_pr_content`, `untrusted_external_input`. The trust
> boundary determines which Auto-Mode-equivalent input filter the
> vendor runtime applies before the tool output enters the agent's
> context window.
>
> Supported `gate:` values: `none` (default for trusted boundaries),
> `human_approval_for_destructive` (mandatory for write operations
> outside the feature's own directory), `human_approval_required`
> (mandatory for any state change).

This is the in-repo invariant that makes vendor-cloud-bound bindings
auditable. When Routines / equivalents fire, the AGENTS.md is the
source of truth for what should have woken; vendor consoles are the
mirror, not the original.

### 3.4 Permanent / Adaptive classification — no change

None of these changes alter the permanent / adaptive classification of
any principle. P2, P5, P9, P10 retain their existing classification
(P5 / P9 / P10 permanent; P2 currently permanent per RFC-0002).

## Evidence

### Vendor-native realizations (public-beta-or-better as of 2026-05-11)
- **Anthropic Outcomes** — public beta. Architectural detail:
  separate grader in independent context window. Quantified gain:
  +10pp on hardest tasks, +8.4% .docx, +10.1% .pptx.
  Sources: [9to5Mac](https://9to5mac.com/2026/05/07/anthropic-updates-claude-managed-agents-with-three-new-features/),
  [Rick's Cafe AI architectural analysis](https://cafeai.home.blog/2026/05/10/anthropic-shipped-outcomes-and-real-story-is-verification-becoming-a-sku/),
  [Releasebot Anthropic May 2026](https://releasebot.io/updates/anthropic).
- **Anthropic Multiagent Orchestration** — public beta. Up to 20
  specialists in parallel, shared filesystem, lead agent re-checks
  mid-workflow because events are persistent. Sources: [Augment Code 7-frameworks survey](https://www.augmentcode.com/tools/multi-agent-orchestration-platforms-build-vs-buy),
  [9to5Mac](https://9to5mac.com/2026/05/07/anthropic-updates-claude-managed-agents-with-three-new-features/).
- **Gemini CLI Subagents** — generally available. Each subagent owns
  a separate context window, custom system instructions, curated
  tools. New `/agents refresh` and `/skills install/uninstall` this
  week. Sources: [Subagents docs](https://geminicli.com/docs/core/subagents/),
  [Gemini CLI changelog](https://geminicli.com/docs/changelogs/),
  [InfoQ April overview](https://www.infoq.com/news/2026/04/subagents-gemini-cli/).
- **OpenAI Codex MultiAgentV2** — explicit configuration surface in
  Codex CLI for parallel specialist agents. Sources: [OpenAI Codex changelog](https://developers.openai.com/codex/changelog),
  [Releasebot Codex](https://releasebot.io/updates/openai/codex).
- **Anthropic Claude Code Routines** — research preview opened
  2026-04-14, broadly available with daily-run quotas. Triggers:
  schedule / API / GitHub events (PR / push / issue / check_run /
  workflow_run / discussion / release / merge_queue). Sources:
  [devops.com](https://devops.com/claude-code-routines-anthropics-answer-to-unattended-dev-automation/),
  [pasqualepillitteri](https://pasqualepillitteri.it/en/news/851/claude-code-routines-cloud-automation-guide).
- **Anthropic Claude Code Auto Mode** — layered safety architecture:
  input filtering, action evaluation, two-stage classification of
  tool outputs before they enter system context; warnings injected
  for adversarial content; sensitive operations gated on human
  approval. Source: [InfoQ deep-dive](https://www.infoq.com/news/2026/05/anthropic-claude-code-auto-mode/).

### Empirical exhibits (community / OSS)
- **DeepClaude (HN #1, 606 pts on 2026-05-04)** — Claude Code
  agent loop swapped to DeepSeek V4 Pro for 17× lower per-token
  cost. Demonstrates that the AGENTS.md shape this RFC standardizes
  is already de facto the cross-vendor surface practitioners are
  swapping at. Sources: [HN #48002136](https://news.ycombinator.com/item?id=48002136),
  [GitHub aattaran/deepclaude](https://github.com/aattaran/deepclaude),
  [Decrypt coverage](https://decrypt.co/366729/deepclaude-run-claude-code-deepseek-brain-17x-cheaper).
- **Simon Willison's "Vibe coding and agentic engineering are
  getting closer than I'd like"** — argues the verification gap
  (not generation gap) is now the bottleneck.
  Source: [simonwillison.net](https://simonwillison.net/2026/May/6/vibe-coding-and-agentic-engineering/).

### Benchmark backdrop (informational, not calibration)
- **Terminal-Bench 2.0** — GPT-5.5 82.7% leads Opus 4.7 69.4%
  (+13.3pp swing). RFC-0004's P4-VC1 monitor caught this and did
  not trip; that monitor's design is independent of this RFC.
  Source: [tbench.ai](https://www.tbench.ai/leaderboard/terminal-bench/2.0).

## Impact Assessment

### Existing principles
- **P2 (Locality of Behavior)** — gains a Subagent Topology Mapping
  sub-clause. No change to existing prescription. Reinforces P2's
  permanent classification.
- **P5 (Test as Specification)** — gains a sibling pattern (Verifier
  Isolation) that explicitly subsumes P5 when a richer rubric is
  present. The default verifier when no RUBRIC.md exists remains
  `*.test.ts`, so existing AIDE-conformant repos require no change.
- **P9 (Security by Structure)** — Auto Mode's structural input-trust
  boundaries are referenced in the Event/Trigger surface
  (`trust_boundary:` field). No change to P9 itself.
- **P10 (Meta-Code as First-Class)** — gains an Event/Trigger
  sub-section with the schema in §3.3. No change to existing
  prescription that AGENTS.md / CLAUDE.md are first-class versioned
  content.
- **A2, A4** — referenced as the source of Verifier Isolation. No
  change to either axiom (axioms are immutable).

### Current adopters of the methodology
- AIDE-conformant repos that do not adopt the new sections continue
  to work as before. The Verifier Isolation rubric is opt-in (when
  no RUBRIC.md is present, the existing `*.test.ts` default
  applies). The Event/Trigger surface is opt-in (when no `events:`
  block is present, agents continue to be invoked rather than
  triggered).
- AIDE-conformant repos that adopt the new sections gain a single
  cross-vendor configuration surface, enabling the kind of vendor
  swap DeepClaude demonstrates without re-authoring per-vendor
  configs.

### Compatibility with other sections
- RFC-0002 (Autonomous Self-Evolving Methodology) — compatible.
  The Verifier Isolation pattern slots into the Multi-Agent
  Deliberation step as the per-task verification primitive.
- RFC-0003 (Distributed Agent-Native Scheduling) — compatible.
  The Event/Trigger surface is the AGENTS.md realization of the
  per-platform scheduling contract that RFC-0003 currently
  enforces externally.
- RFC-0004 (Cost-Pressure + Vendor Portability) — strongly
  reinforces. The Subagent Topology Mapping is the operational
  form of the P4-VC1 vendor-portability validity condition that
  RFC-0004 added; DeepClaude is the empirical exhibit.

## Alternatives Considered

### A. Wait for second confirming vendor before naming Verifier Isolation
Rejected. Three vendors already ship subagent topology; one vendor
ships the verifier-isolation pattern as a public-beta primitive with
measured +10pp gains; community discourse (Simon Willison's "vibe
coding and agentic engineering are getting closer than I'd like")
identifies verification — not generation — as the binding constraint
of agent-led development right now. Naming the pattern is value-add
*today* without locking in a vendor-specific shape (the pattern
description is intentionally vendor-agnostic).

### B. Update `principle-metadata.yaml` numerically this cycle
Rejected. The change this cycle is structural (introduces named
patterns and schemas), not numeric. Per RFC-0002's deliberation
discipline, structural changes should land first, with a
different-vendor reviewer co-sign, before any metadata patch
encodes them as parameters. A follow-up RFC will add the
corresponding metadata slots if the structural change is
accepted.

### C. Add Event/Trigger surface as a separate RFC
Rejected. The three changes are tightly coupled: Routines (event
triggers) wake agents; Auto Mode (trust boundaries) sandboxes
their inputs; Outcomes (Verifier Isolation) grades their outputs.
Separating them would force two reviewers to evaluate the same
vendor-cycle evidence and would risk one half landing without the
other (e.g., event triggers without verifier isolation = unsafe).

### D. Modify `docs/en/AIDE-METHODOLOGY.md` body in this RFC
Rejected. Per RFC-0003 §4.3 and the Korean-mirror invariant,
methodology body changes require different-vendor reviewer
co-sign. This RFC is the proposal; the body edits land in a
follow-up PR after the reviewer co-signs.

## Reviewer checklist (for the different-vendor reviewer)

1. Is the name **Verifier Isolation** correct, or should it be
   *Independent Verifier* / *Grader Isolation* / *Adversarial
   Grader Loop*? Pick one and justify.
2. Is the **1 feature dir → 1 specialist invocation** default the
   right starting point, or should the default be 1:N from day one?
3. Does the **`on:` event taxonomy** (the intersection of vendor
   implementations) correctly reflect Codex / Gemini CLI runtimes,
   not only Anthropic? If a vendor lacks an event, is the right
   answer to omit it from the taxonomy or to require vendors to
   degrade gracefully?
4. Does the **`trust_boundary:` taxonomy** capture the security
   shape Auto Mode's two-stage classification implies? If a vendor
   has finer-grained boundaries, should we widen the taxonomy or
   keep it intersectional?
5. Should `principle-metadata.yaml` slots (`P5.verifier_isolation`,
   `P10.event_trigger_surface`) land in this RFC's PR or in a
   follow-up? RFC currently proposes follow-up; reviewer may
   over-rule.
