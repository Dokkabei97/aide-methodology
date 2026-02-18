# AIDE (Agent-Informed Development Engineering) -- A Software Development Methodology for the Agentic Era v1.0

**Author**: CTO (20+ years of architecture experience, 3 years of hands-on AI agent experience)
**Based on**: GPT/Claude/Gemini triple deep research + Team Alpha (Integrationists) 2 reports + Team Beta (Radicals) 1 report
**Date**: 2026-02-18

---

## Part 6: AIDE Adoption Guide

### When to Adopt AIDE (Decision Matrix)

| Project Characteristics | Adoption Level | Core Principles |
|------------------------|---------------|-----------------|
| Projects where AI agents are the primary code producers | **Full Adoption** | All 10 principles |
| AI-assisted development + mid-size projects | **Core Adoption** | Principles 1 (Context Budget), 2 (Locality), 5 (Test), 7 (Guardrails), 10 (Meta-Code) |
| Simple Q&A chatbot / LLM-based projects | **Partial Adoption** | Principles 7 (Guardrails), 8 (Observability), 9 (Security) |
| Traditional software (no AI usage) | **Not Needed** | Maintain existing methodologies |

### New Projects vs. Existing Project Migration

#### New Projects: Clean Start

New projects **start with AIDE principles from the beginning**:

1. Define manifest.yaml (technology stack, code standards, testing tools)
2. Write CLAUDE.md + AGENTS.md (within 300 lines)
3. Set up Feature-based directory structure
4. Include Eval + Security Gate in CI/CD pipeline
5. Develop the first Feature in types -> logic -> test -> handler order

#### Existing Projects: Progressive Migration

Existing projects **transition progressively on a Feature-by-Feature basis**:

1. **Phase 1 (Immediately)**: Add CLAUDE.md + manifest.yaml, strengthen linting/type checking in CI
2. **Phase 2 (1-2 weeks)**: Begin developing new Features with AIDE structure (features/ directory)
3. **Phase 3 (Progressive)**: When modifying existing code, refactor that portion to Feature-based structure
4. **Phase 4 (Quarterly)**: Build Eval datasets, add Security Gate
5. **Phase 5 (Ongoing)**: Minimize shared/ code, simplify layer structure

**Key**: "Do not rewrite existing code all at once." By applying AIDE principles only to new and modified code, the transition happens naturally over time.

### Checklists

#### AIDE Minimum Requirements Checklist

- [ ] **Meta files**: CLAUDE.md/AGENTS.md exist at root and are within 300 lines
- [ ] **manifest.yaml**: Technology stack, code standards, and test configuration are locked down
- [ ] **Feature-based structure**: Independent directories per feature exist
- [ ] **Type safety**: TypeScript strict mode or equivalent type checking enabled
- [ ] **Deterministic guardrails**: Linter + type checker + pre-commit hook configured
- [ ] **Observability**: Structured log format, tracing enabled
- [ ] **Security verification**: Security linter configured, automated execution in CI
- [ ] **Testing**: Unit + PBT minimum, Eval Suite recommended
- [ ] **CI gates**: Automatic eval execution on meta file/code changes

#### AIDE Full Compliance Checklist (above items + the following)

- [ ] **Eval Flywheel**: Production failures automatically incorporated into eval datasets
- [ ] **Security Gate**: AI-generated code security scan + SCA automated execution
- [ ] **Cost Tracking**: Real-time monitoring of token usage, API response times
- [ ] **Skill packages**: Reusable skills defined in .agents/skills/
- [ ] **Duplication detection**: Automated detection of business-knowledge-level duplication in CI
- [ ] **Human Review PR Contract**: Intent explanation, proof of operation, risk rating, AI usage disclosure

---



← Previous: [05-CICD-PIPELINE](./05-CICD-PIPELINE.md) | Next: [07-DISCUSSION-RECORDS](./07-DISCUSSION-RECORDS.md) →
