# Weekly AIDE Intel Review — 2026-05-11

## Plan

- [x] Run intel pipeline scripts (vendor / social / benchmarks); inspect source health.
- [x] Curator pass via WebSearch / WebFetch — Anthropic / OpenAI / Google releases for 2026-05-05 → 2026-05-11.
- [x] Curator pass — HN / tech blogs / SNS / SWE-bench / Terminal-bench leaderboards.
- [x] Compile curator-merged digest at `evolution/intel/weekly-2026-05-11.md` with explicit machine-source health note.
- [x] Override `dispatch.json` (machine pipeline auto-suppressed due to sandbox egress) with cited curator evidence.
- [x] Write English weekly synthesis at `research/en/2026-05-11-weekly-synthesis.md`.
- [x] Write Korean weekly synthesis at `research/ko/2026-05-11-weekly-synthesis.md`.
- [x] Draft `rfcs/0005-verifier-isolation-and-subagent-topology.md` — structural RFC, no metadata changes this cycle.
- [x] Update `rfcs/README.md` index with RFC-0005 row.
- [x] Commit + push to `claude/laughing-thompson-JUXk6` and open draft PR.

## Review

- **Machine pipeline source health**: 0 / 32 reached. Cause: sandboxed egress in this curator session, not an upstream outage. A5's auto-suppress fired correctly; curator pass restored dispatch with cited evidence. The next CI cron (2026-05-18 00:00 UTC) will refresh raw YAMLs unaffected.
- **Strongest signals this week**:
  1. Anthropic Code w/ Claude 2026 (5/6) — Outcomes / Multiagent Orchestration / Dreaming all moved preview → public beta in the same week. Three vendor-native realizations of patterns AIDE specified at axiom level.
  2. DeepClaude HN #1 (606 pts) — empirical exhibit for RFC-0004's cost-pressure + vendor-portability story.
  3. Terminal-Bench 2.0 +13.3pp swing to GPT-5.5 vs Opus 4.7 — RFC-0004's P4-VC1 monitor caught it and correctly did **not** trip (Verified / SWE-bench Pro top-3 spreads remain inside 15pp threshold).
  4. Claude Code Routines + Auto Mode — agents become repo-event-driven citizens; P10 needs an Event/Trigger surface.
  5. OpenAI dropping SWE-bench Verified reporting — methodology-level signal about benchmark source-tiering. Logged for next cycle as deliberation candidate (N=1 today).
- **What this cycle ships**: curator-merged weekly digest, dispatch override, en/ko synthesis notes, RFC-0005 (structural, no `principle-metadata.yaml` numeric changes), todo + RFC index updates.
- **What this cycle deliberately does NOT ship**:
  - No edits to `docs/en/AIDE-METHODOLOGY.md` or its Korean mirror — body changes require different-vendor reviewer co-sign per RFC-0003 §4.3.
  - No edits to `principle-metadata.yaml` — RFC-0005 is structural; metadata slots follow if the reviewer accepts.
  - No edits to `axioms.yaml` — axioms are immutable per A1 / A4.
- **Verification**: digest + dispatch + RFC + synthesis files all written; cross-referenced from each other; A5 audit chain preserves the auto-suppress event.

## Open follow-ups for next cycle (2026-05-18)

- Watch for a second confirming vendor withdrawal from SWE-bench Verified (would lift the source-tier RFC above N=1 noise floor).
- Monitor whether Anthropic Dreaming graduates from research-preview to public-beta (would justify a P10 sub-section on cross-session learning artifacts).
- Track Terminal-Bench 2.0 + SWE-bench Pro top-3 spreads weekly; if the multi-benchmark spread crosses 15pp, RFC-0004's P4-VC1 trips and a P4 metadata patch becomes warranted.
- Add intel script enhancement to optionally use a curator-cited evidence file (e.g., `evolution/intel/curator-evidence-YYYY-MM-DD.yaml`) so the override doesn't depend on prose alone.
