# Weekly Synthesis — 2026-05-11

> **Authoring agent**: Claude Code on web (claude-opus-4-7), single-vendor draft. Awaits different-vendor reviewer per Axioms A2 / A4.
> **Source digest**: `evolution/intel/weekly-2026-05-11.md`
> **Lookback**: 2026-05-05 → 2026-05-11 (UTC).
> **Lens**: signals that change *how much engineering work can be safely delegated to an autonomous agent* — not generic AI news.

This research note is the synthesis layer required by RFC-0003 §4 (per-platform scheduling contract). The Weekly Intel digest assembles raw signals; this note converts them into architectural claims for agent-led development and identifies the principle-metadata changes that follow.

## Three architectural claims this week supports

### Claim 1 — Verifier Isolation has graduated from axiom to vendor primitive

For sixteen months AIDE has carried two axioms whose practical realization was left to the implementer:
- **A2 (Adversarial Separation)** — "the build agent and the review agent must not share a vendor / training-data substrate"
- **A4 (No Single Authority)** — "no single agent's verdict is binding"

Anthropic Outcomes (preview → public beta this week, see [9to5Mac coverage](https://9to5mac.com/2026/05/07/anthropic-updates-claude-managed-agents-with-three-new-features/) and [Rick's Cafe AI architectural analysis](https://cafeai.home.blog/2026/05/10/anthropic-shipped-outcomes-and-real-story-is-verification-becoming-a-sku/)) ships exactly that pattern as a vendor primitive: a separate grader agent in **its own independent context window** scores the working agent's output against a developer-supplied rubric. The grader has no knowledge of the working agent's reasoning path; this independence is the architectural reason for the **+10pp success on the hardest tasks** (and +8.4% on `.docx`, +10.1% on `.pptx`) that Anthropic published.

This is not an A2 / A4 *replacement*. The grader is still same-vendor, so it does not satisfy A2 at the vendor granularity AIDE requires. But it is the *intra-vendor* expression of the same principle — and now that it ships as a public-beta primitive, AIDE's methodology body should give it a name so feature designers can reference it without re-deriving it from axioms.

**Architectural implication**: introduce a named structural pattern, **Verifier Isolation**, sitting under A2 + A4 + P5 (Test as Specification). The pattern composes vertically: Verifier Isolation handles intra-vendor verification per task; A2's vendor-separation handles inter-vendor verification per RFC. RFC-0005 carries this proposal.

### Claim 2 — Subagent topology is now a vendor-native primitive across all three frontier vendors

Three independent vendor announcements this week made the same architectural choice:
- **Anthropic Multiagent Orchestration** (public beta) — lead agent decomposes, delegates to ≤20 specialists in parallel, shared filesystem ([Augment Code 7-frameworks survey](https://www.augmentcode.com/tools/multi-agent-orchestration-platforms-build-vs-buy)).
- **Gemini CLI Subagents** (now with `/agents refresh`, Skills install/uninstall in this week's release) — each subagent has its own context window, custom instructions, curated tools ([Gemini CLI changelog](https://geminicli.com/docs/changelogs/), [InfoQ April overview](https://www.infoq.com/news/2026/04/subagents-gemini-cli/)).
- **OpenAI Codex MultiAgentV2** — explicit configuration surface in Codex CLI for parallel specialist agents ([OpenAI Codex changelog](https://developers.openai.com/codex/changelog)).

The convergence is the signal. AIDE's P2 (Locality of Behavior) prescribes a feature-directory shape (`types.ts`, `logic.ts`, `handler.ts`, `store.ts`, `*.test.ts`, `AGENTS.md`) without prescribing how those features map to subagents. With subagent topology now a primitive across all three vendors, the missing link is explicit: **one feature directory should map to one subagent's working set**. The subagent's curated tools come from the feature's `handler.ts` boundary. The subagent's system prompt comes from the feature's `AGENTS.md`. The lead agent's job is to pick which feature directories to wake and synthesize their outputs.

**Architectural implication**: P2 stays permanent. RFC-0005 also adds a sub-clause specifying the feature-directory ↔ subagent mapping so AGENTS.md can be authored once and consumed by Anthropic Multiagent / Gemini CLI Subagents / Codex MultiAgentV2 alike. This is also where the P4-VC1 (vendor-portability) monitor pays off — a uniform AGENTS.md shape is *the* portability surface.

### Claim 3 — Agents are becoming event-driven repo citizens, not invocations

Two adjacent vendor releases collapse the "agent-as-CLI" mental model:
- **Claude Code Routines** ([devops.com](https://devops.com/claude-code-routines-anthropics-answer-to-unattended-dev-automation/)) — saved Claude Code config bound to triggers: schedule, API call, or **GitHub events** (PR, push, issue, check_run, workflow_run, discussion, release, merge_queue). Survives laptop closure, runs on Anthropic cloud.
- **Claude Code Auto Mode** ([InfoQ deep-dive](https://www.infoq.com/news/2026/05/anthropic-claude-code-auto-mode/)) — layered safety architecture with two-stage classification of tool outputs (file reads / shell / web responses) before they enter system context; warnings injected when content looks adversarial.

The combination means an agent can wake on a `pull_request.opened` event, inspect untrusted PR content under structural input-trust boundaries, run a Verifier-Isolation pass against the PR's stated intent, and post a verdict — **without any human in the loop until the gated approval**. AIDE's P10 (Meta-Code as First-Class) currently treats AGENTS.md / CLAUDE.md as configuration artifacts. With Routines + Auto Mode, Meta-Code needs an **Event/Trigger surface**: which repo events should wake which agent, what permission profile applies, what verifier should grade the result.

This is also the strongest exhibit yet for keeping P9 (Security by Structure) permanent. Auto Mode's two-stage classification is the *vendor-built* version of "deterministic guardrails on probabilistic generation" (P7). Two of AIDE's permanent principles are now empirically vindicated as production-grade primitives in the same vendor cycle.

**Architectural implication**: P9 and P7 stay permanent (already classified as such — this week is confirmation, not a re-classification). P10 needs an Event/Trigger sub-section in the methodology body, which RFC-0005 §Detailed Design enumerates.

## Signals that informed but did not move a numeric dial this cycle

- **DeepClaude (HN #1, 606 pts, 17× cheaper)** — [HN thread](https://news.ycombinator.com/item?id=48002136), [GitHub repo](https://github.com/aattaran/deepclaude). The strongest empirical exhibit for RFC-0004's cost-pressure + vendor-portability story since that RFC was drafted. The shell-script-thin layer between Claude Code's loop and a non-Anthropic brain is the operational form of P4-VC1 vendor-portability. Does not require new metadata changes (RFC-0004 already armed the triggers); does require a follow-up note logged in `principle-metadata.yaml::P4.evolution_history` next cycle.
- **Anthropic Dreaming (research preview)** — [VentureBeat](https://venturebeat.com/technology/anthropic-introduces-dreaming-a-system-that-lets-ai-agents-learn-from-their-own-mistakes), [The New Stack](https://thenewstack.io/anthropic-managed-agents-dreaming-outcomes/). Plain-text playbooks as the cross-session learning artifact mirror AIDE's choice to keep Meta-Code in-repo as text rather than encoding it in weights. Validates P10 as permanent. Not a metadata trigger this cycle because it is research-preview, not public-beta.
- **OpenAI dropping SWE-bench Verified reporting** — methodology-level signal. AIDE's `principle-metadata.yaml` does not currently encode benchmark source-tiers; this should be a follow-up RFC if the pattern holds for two cycles. Logged here as a deliberation candidate, not a trigger.
- **Terminal-Bench 2.0 +13.3pp swing (GPT-5.5 82.7% vs Opus 4.7 69.4%)** — RFC-0004's P4-VC1 monitor caught this and correctly did **not** trip, because Verified / SWE-bench Pro top-3 spreads remain inside the 15pp threshold. This is the monitor doing its job — it is calibrated to ignore single-benchmark divergence and only react to multi-benchmark vendor lockout. Confirmation, not change.
- **GPT-5.5 -52.5% hallucination on high-stakes prompts** — relevant to a future P5 / P9 calibration cycle as a high-stakes-task floor metric, but does not move a current threshold.
- **Anthropic 10 Finance Agent Templates** — vendor-distributed AGENTS-shaped artifacts. Industry exhibit for P10's "treat agent config as first-class versioned content" stance. No metadata change.

## What this cycle ships

| File | Change | Axiom enforced |
|---|---|---|
| `evolution/intel/weekly-2026-05-11.md` | Curator-merged digest with 31 cited sources; explicit machine-source health note; dispatch overridden from auto-suppress to YES with reasons | A5 (Self-Observability — suppression event preserved) |
| `evolution/intel/dispatch.json` | `should_dispatch=true`; client_payload tracks machine vs curator source counts and links to RFC + synthesis paths | A5 + A3 (curator override carries cited evidence) |
| `research/en/2026-05-11-weekly-synthesis.md` | This document. Three architectural claims; metadata-trigger discipline | A4 (single-vendor; awaits different-vendor reviewer) |
| `research/ko/2026-05-11-weekly-synthesis.md` | Korean mirror | bilingual contract |
| `rfcs/0005-verifier-isolation-and-subagent-topology.md` | Draft RFC introducing **Verifier Isolation** as a named pattern, **Subagent Topology** mapping (feature-dir ↔ vendor subagent), and **Event/Trigger surface** for P10 Meta-Code | A4 (awaits different-vendor consensus) |
| `tasks/todo.md` | This week's plan + review summary | A5 |
| `rfcs/README.md` | Add RFC-0005 row to the index | bookkeeping |

The English methodology document (`docs/en/AIDE-METHODOLOGY.md`) and its Korean mirror are **not** edited in this cycle. Body changes require different-vendor reviewer co-sign per RFC-0003 §4.3. `principle-metadata.yaml` is **not** edited in this cycle either — RFC-0005 is structural (introduces a named pattern + a Meta-Code surface), not numeric. If the next cycle's reviewer accepts the structural change, the principle-metadata patch (e.g., adding a `verifier_isolation` formula slot under P5, an `event_trigger_surface` slot under P10) follows.

## Open questions for the reviewer

A different-vendor reviewing agent should explicitly accept or reject:

1. **Is "Verifier Isolation" the right name?** Alternatives: *Independent Verifier*, *Grader Isolation*, *Adversarial Grader Loop*. The chosen name should make it obvious that the grader runs in a fresh context window and does not see the working agent's reasoning path.
2. **Should the feature-directory ↔ subagent mapping be 1:1 mandatory or 1:N permitted?** A 1:N reading lets one feature spawn parallel specialists for sub-tasks (e.g., one feature → one writing specialist + one test specialist), which is closer to how Anthropic Multiagent Orchestration is being adopted in practice.
3. **Should the Event/Trigger surface be a new top-level section in AGENTS.md, or a sub-section of an existing section?** A top-level section makes it discoverable by `gh` / GitHub Actions tooling without parsing prose; a sub-section keeps the file shorter.
4. **Does OpenAI dropping SWE-bench Verified justify a benchmark source-tier RFC now, or wait for a second confirming withdrawal?** Single-vendor withdrawal is an N=1 signal; a second confirming withdrawal would lift it above the noise floor.

These are intentionally framed as falsifiable choices — A3 (Empiricism) requires the reviewer's verdict to be backed by data, not preference.

---

**Next weekly cycle**: 2026-05-18. The CI-machine sense pass runs at 00:00 UTC; this curator session runs after. Source health from this run was machine-failure / curator-cited-31. Sensor remediation for the sandbox-egress case is a CI-only concern and does not need a sensor-level fix; the pipeline correctly auto-suppressed and the curator override is the documented escape hatch.
