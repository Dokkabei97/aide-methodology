# RFCs (Requests for Comments)

This directory contains RFCs for proposed changes to the AIDE methodology.

## What is an RFC?

An RFC is a design document that describes a proposed change to the AIDE methodology. RFCs provide a consistent and controlled path for changes, ensuring that all stakeholders have an opportunity to review and discuss proposals before they are accepted.

## How to Submit an RFC

1. **Open an Issue** — Start by opening an [RFC Proposal Issue](../../issues/new?template=rfc-proposal.yml) describing the problem or direction.
2. **Draft with an Agent** — Use an AI agent to draft the RFC using the [template](0000-template.md). Agent usage is required.
3. **Submit a PR** — Create a pull request adding your RFC to this directory. Name it `NNNN-short-title.md` (number will be assigned).
4. **Discussion** — The community has a minimum 2-week window to provide feedback.
5. **Decision** — Maintainers will accept, reject, or request revisions.

### Auto-drafts from the Weekly Intel pipeline

The Weekly Intel pipeline (`.github/workflows/aide-weekly-intel.yml`) may
auto-generate a draft RFC under the filename
`NNNN-weekly-intel-<slug>-YYYY-MM-DD.md` when the external sensor crosses a
high-signal threshold (new model/runtime + ≥2 vendor releases, ≥1 benchmark
SOTA shift ≥ 2.0pp, or ≥3 viral HN stories on tracked queries).

Auto-drafts are explicitly marked **single-vendor draft, awaits
different-vendor co-sign**. They do not propose body changes; they request
that a different-vendor reviewing agent perform the deliberation and either
promote the draft to a concrete change or close it with a written rejection
reason. This keeps Axioms A2 (Adversarial Separation) and A4 (No Single
Authority) honest even when the originating signal is automated.

## RFC Lifecycle

```
Draft → Discussion (2 weeks min) → Accepted / Rejected / Revision Requested
```

- **Draft**: Initial submission via PR.
- **Discussion**: Open for community review and feedback.
- **Accepted**: Merged into the methodology. Implementation begins.
- **Rejected**: Closed with explanation. May be re-proposed with significant changes.
- **Revision Requested**: Author revises based on feedback and re-submits for review.

## Current RFCs

| RFC | Title | Status | Date |
|-----|-------|--------|------|
| [0001](0001-language-native-naming-convention.md) | Language-Native Naming Convention First | Draft | 2026-02-18 |
| [0002](0002-autonomous-self-evolving-methodology.md) | Autonomous Self-Evolving Methodology (AIDE v2.0) | Draft | 2026-02-20 |
| [0003](0003-distributed-agent-native-scheduling.md) | Distributed Agent-Native Scheduling (AIDE v2.1) | Draft | 2026-05-04 |
| [0004](0004-cost-pressure-and-vendor-portability.md) | Cost-Pressure Variable in P1 + Vendor-Portability Validity Condition in P4 | Draft | 2026-05-04 |
