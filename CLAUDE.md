# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AIDE (Agent-Informed Development Engineering) is a methodology for software development in the age of agents. This repository is a **methodology document repository**, not a code project, and is the result of independent deep research by GPT/Claude/Gemini and a final consensus reached by a CTO agent after debate between Team Alpha (integration) and Team Beta (radical).

License: CC BY-SA 4.0

## Repository Structure

```
docs/
  en/AIDE-METHODOLOGY.md   -- full methodology (English, core document)
  ko/AIDE-METHODOLOGY.md   -- full methodology (Korean)
  translations.md          -- translation guide
axioms.yaml                -- v2.0 Immutable Axioms (5 axioms, cannot be modified by agents)
principle-metadata.yaml    -- v2.0 Adaptive Principles (self-calibrating parameters)
evolution/                 -- v2.0 Evolution Engine (autonomous self-evolution system)
  scripts/                 -- Python scripts for each pipeline phase
  benchmarks/              -- Collected benchmark data (auto-generated)
  deliberation/            -- Agent deliberation artifacts (auto-generated)
  sandbox/                 -- Empirical validation results (auto-generated)
  history/                 -- Evolution audit trail (permanent record)
research/                  -- 6 research reports (GPT/Claude/Gemini deep research + Team Alpha/Beta debate)
rfcs/                      -- RFC process (methodology change proposals)
  0000-template.md         -- RFC template
examples/                  -- example projects (currently empty)
.github/workflows/
  axiom-gate.yml           -- CI gate enforcing 5 Immutable Axioms
  aide-evolution-engine.yml -- Monthly autonomous evolution pipeline
```

## Key Methodology Concepts

To work on documents in this repository, the 10 core principles of AIDE must be understood:

1. **Context Budget Principle** -- Context Budget is the primary design constraint (files 200-300 lines, functions 30 lines recommended)
2. **Locality of Behavior** -- Place related code in the same physical location with a feature-oriented structure
3. **Functional Core, Structural Shell** -- pure function core + side-effect boundary
4. **Knowledge DRY, Code WET-tolerant** -- remove redundancy in knowledge, allow trade-offs for local code
5. **Test as Specification** -- use tests as a specification language
6. **Progressive Disclosure** -- progressive disclosure of information
7. **Deterministic Guardrails** -- deterministic guardrails for probabilistic generation
8. **Observability as Structure** -- observability as part of the structure
9. **Security by Structure** -- structural security validation
10. **Meta-Code as First-Class** -- treat AGENTS.md, CLAUDE.md, etc. as first-class metacode

AIDE proposes a Feature directory structure: `types.ts`, `logic.ts`, `handler.ts`, `store.ts`, `*.test.ts`, `AGENTS.md`

## v2.0 Architecture (Autonomous Self-Evolution)

AIDE v2.0 introduces a 4-layer autonomous architecture:

1. **Immutable Axioms** (axioms.yaml) -- 5 axioms that no agent can modify: Reversibility, Adversarial Separation, Empiricism, No Single Authority, Self-Observability
2. **Adaptive Principles** (principle-metadata.yaml) -- 10 principles with self-calibrating formulas, validity conditions, and invalidation triggers
3. **Evolution Engine** (evolution/) -- Monthly pipeline: Sense → Deliberate (3-agent) → Validate (empirical) → Apply
4. **Execution** -- Multi-agent review replacing human review, Eval Flywheel, Red Team Agent

Key concept: Principles are classified as **permanent** (P3, P5, P7, P8, P9) or **adaptive** (P1, P2, P4, P6, P10). Adaptive principles auto-calibrate based on agent benchmarks.

## Contribution Rules

This project follows an **Agent-Autonomous contribution model** (v2.0):

- Methodology evolution is handled by the Evolution Engine (multi-agent consensus + empirical validation)
- Manual PRs still accepted for typo fixes and structural improvements
- All agent-generated changes must comply with the 5 Immutable Axioms (enforced by axiom-gate.yml)
- PRs must include Agent, Agent Model, and Human Role fields
- RFC process: Evolution Engine auto-generates → multi-agent deliberation → empirical gate → auto-merge

## Bilingual Content

- All core documents are maintained in both English and Korean
- Translation is performed by AI agents following the Agent-First model
- README.md (English) ↔ README-KR.md (Korean) are managed as paired documents
- Technical terms remain in English, with short explanatory notes added at first occurrence when translating
- If one language is modified, the other language must be synchronized

## Working with This Repository

- `docs/en/AIDE-METHODOLOGY.md` is the most central document (full methodology)
- `axioms.yaml` defines the 5 Immutable Axioms — these CANNOT be modified by any agent
- `principle-metadata.yaml` contains self-calibrating principle parameters — modified by Evolution Engine only
- `evolution/` contains the autonomous evolution pipeline scripts and history
- Reports under `research/` are preserved as historical records and may differ from the final methodology
- Methodology changes must modify both English and Korean documents to keep consistency
- RFC template (`rfcs/0000-template.md`) must include Agent Used, Agent Model, Research Method fields
