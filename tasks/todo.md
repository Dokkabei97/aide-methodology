# Weekly AIDE Intel Review — 2026-05-18

## Plan

- [x] Read repository guidance, the established weekly cadence, and prior artifacts.
- [x] Research new models / agent features from Anthropic, OpenAI, Google (+ xAI) against official docs and primary reporting.
- [x] Scan benchmarks (SWE-bench Verified/Pro, Terminal-Bench 2.0) and community signals (HN, X, Threads).
- [x] Compile the weekly intel digest, absorbing the un-synthesised 2026-05-11 carryover.
- [x] Author the bilingual weekly synthesis (en + ko) with architectural claims.
- [x] Record the evolution-history audit entry with signal scoring and reversal path.
- [x] Draft RFC-0005 (Verification Budget) and register it in the RFC index.

## Review

- The fortnight's load-bearing signal: verification capacity — not generation
  speed — is now the binding constraint on agent-led delegation (HN essay,
  Anthropic CI auto-fix design goal, Prime Intellect's 2-week unattended run).
- Every frontier vendor shipped the unattended/triggered cloud-agent loop
  (Anthropic Routines, OpenAI Codex mobile, xAI Grok Build) — empirical
  vindication of RFC-0003; trigger/routine definitions confirmed as meta-code (P10).
- Anthropic "Dreaming" (self-modifying agent memory) logged as an evolution loop
  that must inherit A1 + A5 + P9; folded into RFC-0005's threat section.
- No `principle-metadata.yaml` change: no signal produced a calibration-grade
  quantitative threshold. P4-VC1 re-checked against official SWE-bench Pro
  (top-2 gap ~5.7pp << 15pp) and remains `true`.
- No methodology body edit: per RFC-0003 §4.3, body edits await a
  different-vendor countersignature. This cycle proposes (RFC-0005); it does
  not apply.
- Sensor health degraded: `vendor:anthropic/news` feed 404s; xAI untracked.
  Both queued as a separate sensor-remediation PR (kept out of this diff).

## Queued for next cycles

- [ ] Sensor PR: repair/replace the Anthropic news feed URL; add xAI as a vendor.
- [ ] Define a measurable verification-throughput metric so RFC-0005 can carry
      a calibrated number.
- [ ] Migrate `benchmark-history.yaml` cross-week comparison off the saturating
      SWE-bench Verified onto SWE-bench Pro (official) + Terminal-Bench 2.0.
