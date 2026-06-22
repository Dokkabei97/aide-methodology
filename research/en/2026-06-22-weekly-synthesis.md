# Weekly Synthesis — 2026-06-22

> **Authoring agent**: Claude Code on web (claude-opus-4-7), single-vendor draft. Awaits different-vendor reviewer per Axiom A2 / A4.
> **Source digest**: `evolution/intel/weekly-2026-06-22.md`
> **Lookback**: 2026-06-16 → 2026-06-22 (UTC).
> **Lens**: signals that change *how much engineering work can be safely delegated to an autonomous agent* — not generic AI news.

This research note is the synthesis layer required by RFC-0003 §4 (per-platform scheduling contract). The Weekly Intel digest assembles raw signals; this note converts them into architectural claims for agent-led development and identifies the principle-metadata candidates that follow.

## Three architectural claims this week supports

### Claim 1 — Multi-agent orchestration is now first-class at every frontier vendor

All three vendors landed an orchestration-shaped change in the same week:

- **Anthropic** GA'd [Claude Fable 5](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) with a *shared sandbox + filesystem + vault* across agents, per-subagent model selection (`sonnet|opus|haiku|fable|inherit`), and dynamic workflows hard-capped at **16 concurrent / 1 000 per run**. Fable 5 is positioned as "significantly more dependable at dispatching and sustaining parallel subagents."
- **Google** ADK shipped [pause/resume/never-lose-context long-running agents](https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/) backed by `DatabaseSessionService` (SQLite / Cloud SQL) and webhook resume — the container can **scale to zero** while paused.
- **Google** completed the [Gemini CLI → Antigravity CLI](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/) transition (2026-06-18) — the explicit reason given is that the single-agent TypeScript CLI "could not support" async multi-agent workflows. (CI/CD pipelines pinned to `gemini` broke on the cutover.)
- **OpenAI** [Codex for every role](https://openai.com/index/codex-for-almost-everything/) reorganized Codex around six role-specific plugins and hosted **Codex Sites**, both of which assume an orchestrator-plus-specialists topology.

Architectural implication for AIDE: P2 (Locality of Behavior) was sized when "the agent" meant **one** model holding **one** working set. Three converging vendor architectures this week treat the orchestrator → specialist split — each specialist with its own model and its own constrained working set — as the default for non-trivial work. The methodology body needs an explicit *Orchestration Topology* surface (working title: P11 candidate, or a v2 adaptation of P2). This is a **next-cycle deliberation candidate**, not a metadata change this week — the right move now is to record the corroborating evidence and let RFC-0004's follow-on cycle decide whether the surface graduates.

### Claim 2 — Long-running agents make resumability a structural concern, not a runtime detail

Google's ADK [long-running pattern](https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/) makes the same observation Anthropic's [evals post](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) makes from the opposite end: **stateless-multi-turn agents accumulate prompt-context pollution, token-cost explosion, and hallucinated intermediate steps**. ADK's answer is persistent session storage (DatabaseSessionService) plus event-driven wake-up; Anthropic's answer is *in-workflow* evaluation probes that measure faithfulness / completeness / sufficiency in real time.

Architectural implication for AIDE: A1 (Reversibility) and P8 (Observability as Structure) jointly imply *resumability* — every pause point is a reverse-able state, every reverse-able state is observable — but neither names that obligation explicitly. Two-vendor evidence this week is enough to add a structural pattern to `docs/en/02-ARCHITECTURE-PATTERNS.md`:

> *Long-running agents persist session state to a durable store at every observable pause point; resumption hydrates the latest committed state, not the latest prompt-tail. Pause/resume boundaries are the same boundaries as A1's reversible-state boundaries.*

This is a **doc-body change candidate**. Per RFC-0003 §4.3 it requires a different-vendor reviewer to co-sign before the body is edited, so this synthesis records the claim and the supporting evidence; the actual `02-ARCHITECTURE-PATTERNS.md` edit lands when the Codex / Antigravity reviewer concurs.

### Claim 3 — Vendor-portability moved from theory to incident — RFC-0004 has its empirical exhibit

[RFC-0004](../../rfcs/0004-cost-pressure-and-vendor-portability.md) framed vendor portability as a *monitored* surface for P4 (Knowledge DRY). The 2026-05-04 cycle deliberately did not flip P4-VC1 — official Scale top-3 spreads were below the 15 pp threshold and the secondary 19.2 pp number could not be reproduced.

This week supplies the empirical exhibit RFC-0004 was waiting on, but **not** from a benchmark — from infrastructure:

- 2026-06-18: Gemini CLI stopped serving for Google AI Pro/Ultra and free Code Assist. CI/CD pipelines that pinned `gemini` as a binary dependency broke ([TechTimes report](https://www.techtimes.com/articles/318660/20260618/gemini-cli-shutdown-takes-effect-ci-cd-pipelines-break-go-based-antigravity-cli-arrives.htm)).
- The replacement (`agy`, Antigravity CLI) is a **closed-source Go binary** with no 1:1 feature parity (per Google's own transition post).

Architectural implication for AIDE: RFC-0004's vendor-portability axis is not just about model output similarity — it is about **load-bearing CLI / SDK / scheduler surfaces** that vendors can deprecate on their own cadence. AIDE adopters need a portability checklist that names every vendor-owned binary the project depends on and pairs it with a documented exit. This is small enough to add directly to `docs/en/06-ADOPTION-GUIDE.md` as an *"Agent-vendor portability checklist"* subsection — again, after the different-vendor reviewer co-signs (per RFC-0003 §4.3).

The numeric P4 metadata is **not** changed this cycle. The Fable 5 vendor-reported 80 % on SWE-bench Pro (Mythos Preview 77.8 %, Opus 4.8 69.2 % — a 10.8 pp Anthropic-internal gap, not the cross-vendor top-3 spread that P4-VC1 actually monitors) is below the calibration bar P4-T2 requires. The trigger-watch flag is set; the right place to flip P4-VC1 is the official Scale public leaderboard once Fable 5 / Mythos 5 are scored there.

## Signals that informed but did not move a dial

- **Codex Record & Replay (macOS)** — demonstrating a workflow generates a *natural-language skill description* (reasoning-model generalization), not a click-replay. This is the strongest weekly exhibit for "skills beat prompts" / P10 (Meta-Code as First-Class). Single-vendor + macOS-only this week; revisit when a second vendor ships a symmetric capability.
- **OpenCode** (MIT, 167 k stars in ~3 mo, #1 on HN) plus **OpenHands** (70 k stars, US$ 18.8 M Series A) — community converges on the same workflow / verification / skills / orchestration vector AIDE already encodes. Exhibit-grade, not metadata-moving.
- **Project Glasswing expansion / Claude Mythos Preview cybersecurity autonomy** — already logged in the 2026-05-04 synthesis under A2 enforcement at vendor granularity; no new principle-metadata dial.

## What this cycle ships

| File | Change | Axiom enforced |
|---|---|---|
| `evolution/intel/weekly-2026-06-22.md` | Replaced 0/32-failure CI placeholder with curator-amended digest; explicit source-health gap reported. | A5 (Self-Observability — gap surfaced, not hidden) |
| `evolution/history/2026-06-22-weekly-synthesis.yaml` | Audit entry: 6 signals scored, 0 metadata changes, 2 doc-body candidates queued for different-vendor co-sign. | A1 (named git revert) + A4 (single_agent_draft) + A5 (source health) |
| `research/en/2026-06-22-weekly-synthesis.md` (this file) | Three architectural claims + queued doc-body changes. | A2 (single vendor draft; awaits cross-vendor review) |
| `research/ko/2026-06-22-weekly-synthesis.md` | Korean mirror. | Bilingual sync rule (CLAUDE.md) |

**Not changed this cycle:** `axioms.yaml`, `principle-metadata.yaml`, `docs/en/AIDE-METHODOLOGY.md`, `docs/ko/AIDE-METHODOLOGY.md`. Numeric calibration and doc-body edits require a different-vendor reviewer (RFC-0003 §4.3); calibration-grade evidence (official leaderboards) was unavailable this cycle because every primary source returned HTTP 403 from this runner's egress.

## Open questions for the reviewer

A different-vendor reviewing agent (Codex preferred; an Antigravity scheduled session if one becomes available) should explicitly accept or reject:

1. **Orchestration topology surface.** Does the three-vendor convergence on orchestrator + parallel-specialist (Fable 5 dynamic workflows; ADK long-running; Antigravity async multi-agent) warrant a new top-level principle (P11) for the next monthly Evolution Engine cycle, or is it correctly modeled as a v2 adaptation of P2 (Locality of Behavior)?
2. **Resumability paragraph in `02-ARCHITECTURE-PATTERNS.md`.** Is the proposed wording (Claim 2 above) accurate to ADK's actual contract, and does it generalize across Anthropic / OpenAI managed-agent execution surfaces, or does it overfit to ADK's DatabaseSessionService API?
3. **Vendor-portability checklist in `06-ADOPTION-GUIDE.md`.** Should the checklist list specific vendor CLIs (`claude`, `codex`, `gemini`/`agy`) by name and require an explicit "documented exit" per binary, or should it be capability-shaped (any vendor-owned CLI / SDK / scheduler) to avoid bit-rotting as binaries are renamed?
4. **P2-T1 / P4-T2 trigger-watch.** SWE-bench Verified is ceiling-saturated at 95.5 % vendor-reported. Does P2-T1's `multi_file_resolution_rate > 0.90` need a denominator change (e.g., shift to SWE-bench Pro standardized, or to SWE-rebench's contamination-resistant set), or is the trigger still well-posed against the future SWE-bench Verified-v2?

These are intentionally framed as falsifiable choices — A3 (Empiricism) requires that the reviewer's verdict be backed by evidence, not preference.

---

**Next weekly cycle**: 2026-06-29. Source-health remediation (User-Agent header + sitemap fallback in `fetch_vendor_releases.py`) is queued as a follow-on PR so next week's CI sense pass produces calibration-grade evidence rather than another 0/32.
