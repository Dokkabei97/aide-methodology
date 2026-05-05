# Codex Adversarial Review — 2026-05-04 Weekly Synthesis

> Reviewer: Codex app scheduled automation (`gpt-5.5`)
> Reviewed artifacts: `evolution/intel/weekly-2026-05-04.md`, `research/en/2026-05-04-weekly-synthesis.md`, `research/ko/2026-05-04-weekly-synthesis.md`, `rfcs/0004-cost-pressure-and-vendor-portability.md`, `principle-metadata.yaml`
> Verdict: **Approve P1; request correction for P4 current status**

## Official Evidence Checked

| Signal | Source | Review outcome |
|---|---|---|
| Claude Opus 4.7 availability, agentic coding gains, task budgets, `/ultrareview`, auto mode | Anthropic official announcement, 2026-04-16 | Supports P1/P8/P10 discussion. |
| Opus 4.7 premium request multiplier moved to 15x after promotional pricing ended | GitHub Changelog editor note, 2026-05-01 | Supports P1 cost-pressure trigger. |
| GPT-5.5 in ChatGPT/Codex and agentic coding benchmark claims | OpenAI official GPT-5.5 page and Help Center | Supports P1/P10 discussion; confirms GPT-5.5 is not API-launched on day one. |
| OpenAI models, Codex, and Bedrock Managed Agents on AWS | OpenAI official announcement, 2026-04-28 | Supports P10 cross-cloud managed-agent state discussion. |
| Gemini CLI subagents | Google Developers Blog, 2026-04-15 | Supports subagent topology as first-class architecture. |
| Google Agents CLI | Google Developers Blog, 2026-04-22 | Supports machine-readable agent platform control plane. |
| Google ADK Skills | Google Developers Blog, 2026-04-01 | Supports progressive disclosure and runtime skills. |
| SWE-bench Pro public/private spreads | Scale official leaderboards, checked 2026-05-04 | Does **not** support the draft's 19.2pp P4 trigger. |

## Finding

P1 is acceptable. A 15x premium request multiplier is official GitHub Copilot evidence, and the proposed cost-pressure trigger is directionally correct. The constant `utilization_ratio = 0.02` is still a heuristic; the next refinement should make it formula-derived, but the immediate change is reversible and bounded.

P4 needs correction. The draft cites a 19.2pp SWE-bench Pro top-3 spread, but the official Scale public leaderboard currently shows 59.10 / 55.00 / 51.90, a 7.2pp spread. The official private leaderboard shows 47.10 / 44.70 / 43.40, a 3.7pp spread. Therefore `P4-VC1` should remain as a useful validity condition, but its current `status` should be `true`, not `false`.

## Architecture Conclusion

This week's durable methodology update is not "vendor portability is broken"; the official benchmark evidence does not prove that yet. The stronger, source-backed conclusion is:

1. Agent-led development now needs an explicit **control plane**: budget policy, permission policy, context partitioning, task routing, and audit trails should be versioned as meta-code.
2. Subagents should be treated as **context-isolated workers**, not just parallel chat sessions. Google describes separate context windows, tools, MCP servers, and instructions; this matches AIDE's P2/P6/P10 direction.
3. Review capacity is becoming the bottleneck. HN discussion around agentic coding repeatedly points to review planning, mental-model synchronization, and recoverability. AIDE should optimize for reviewable work packets, not only faster generation.
4. Benchmark claims must be tiered by source: official vendor claims, official benchmark leaderboards, secondary trackers, and community reports should not carry equal calibration authority.

## Verdict

- P1 cost-pressure change: **Approve**.
- P4 validity condition/triggers: **Approve as a monitoring surface**.
- P4 current invalidation status and 19.2pp claim: **Request correction**.
- RFC-0004 merge readiness: **Draft remains valid after the P4 correction is reflected in research/RFC/history text**.
