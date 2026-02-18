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
research/                  -- 6 research reports (GPT/Claude/Gemini deep research + Team Alpha/Beta debate)
rfcs/                      -- RFC process (methodology change proposals)
  0000-template.md         -- RFC template
examples/                  -- example projects (currently empty)
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

## Contribution Rules

This project follows an **Agent-First contribution model**:

- Human contributors can directly submit PRs only for **typo-only fixes**
- All other changes must be written or reviewed by an AI agent
- PRs must include Agent, Agent Model, and Human Role fields
- Changes other than typo fixes require RFC process: Issue → Agent drafts RFC → PR → 2-week discussion → maintainer decision

## Bilingual Content

- All core documents are maintained in both English and Korean
- Translation is performed by AI agents following the Agent-First model
- README.md (English) ↔ README-KR.md (Korean) are managed as paired documents
- Technical terms remain in English, with short explanatory notes added at first occurrence when translating
- If one language is modified, the other language must be synchronized

## Working with This Repository

- `docs/en/AIDE-METHODOLOGY.md` is the most central document (full methodology)
- Reports under `research/` are preserved as historical records and may differ from the final methodology
- Methodology changes must modify both English and Korean documents to keep consistency
- RFC template (`rfcs/0000-template.md`) must include Agent Used, Agent Model, Research Method fields
