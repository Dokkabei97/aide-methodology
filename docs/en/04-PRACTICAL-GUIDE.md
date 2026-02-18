# AIDE (Agent-Informed Development Engineering) -- A Software Development Methodology for the Agentic Era v1.0

**Author**: CTO (20+ years of architecture experience, 3 years of hands-on AI agent experience)
**Based on**: GPT/Claude/Gemini triple deep research + Team Alpha (Integrationists) 2 reports + Team Beta (Radicals) 1 report
**Date**: 2026-02-18

---

## Part 4: AIDE Practical Guide

### File/Code Size Guidelines

| Category | Recommended | Upper Limit | Token Estimate | Notes |
|----------|-------------|-------------|----------------|-------|
| Feature logic (logic.ts) | 150-200 lines | 300 lines | ~5,400 | Core business logic |
| Handler (handler.ts) | 100-150 lines | 200 lines | ~3,600 | Each handler function within 30 lines |
| Type definitions (types.ts) | 50-100 lines | 150 lines | ~2,700 | Types are dense, so short is sufficient |
| Tests (*.test.ts) | 200-300 lines | 500 lines | ~9,000 | Repetitive structure, slightly longer is acceptable |
| Meta files (CLAUDE.md) | 100-200 lines | 300 lines | ~5,400 | Upper limit to maintain instruction compliance rate |
| Domain context (AGENTS.md, Tier 2) | 50-100 lines | 200 lines | ~3,600 | Compress to core business rules only |
| Function size | 20-30 lines | 50 lines | ~900 | Fully comprehensible within a single reasoning turn |

**"18 tokens/line" rule of thumb**: On average, 1 line of code = ~18 tokens (based on Cursor IDE research)

### Naming Convention Guide

Apply the **Semantic Verbosity** principle from the Gemini report, while maintaining practical balance:

| Category | Convention | Example | Counter-Example |
|----------|-----------|---------|-----------------|
| File names | kebab-case | `user-auth.ts` | `ua.ts` |
| Function names | snake_case, verb_object | `calculate_order_total_in_krw` | `calc(d)` |
| Type names | PascalCase, nouns | `OrderItem` | `OI` |
| Variable names | snake_case, include meaning | `active_user_id_list` | `ids` |
| Constant names | UPPER_SNAKE, include source | `MAX_LOGIN_ATTEMPTS_PER_POLICY` | `MAX` |
| Side-effect functions | Prefix to indicate side effect | `persist_user_to_database` | `save` |

**Core Principle**: Variable and function names are **inputs to the agent's reasoning**. The more specific a name is, the exponentially lower the probability of the agent misusing it. However, extreme verbosity like `calculated_total_price_with_discount_applied_in_krw` conflicts with line length limits, so maintain a practical range.

### CLAUDE.md Writing Guide (Template)

```markdown
# Project: [Project Name]

## Identity
- Type: [Project type, e.g. Next.js 14 Monorepo]
- Language: TypeScript (Strict Mode)
- Paradigm: Functional core, classes only for infrastructure
- State: [State management tool, e.g. Zustand]

## Absolute Rules (MUST FOLLOW)
- Do not use classes for business logic
- Explicitly type all function parameters and return values
- Do not use the any type
- Do not directly import from features/ outside of features/
- Must get approval before adding new npm packages
- [Add project-specific rules]

## Architecture Map
features/: Independent modules per feature (types + logic + handler + store + test)
shared/:   Global types, infrastructure clients, common errors (keep minimal)
evals/:    Evaluation datasets and scenarios
.agents/:  Skill packages

## Code Style
- Function names: snake_case, verb_object form
- Type names: PascalCase
- Variable names: snake_case, include meaning
- Files: kebab-case
- Max file length: 300 lines (warning), 500 lines (prohibited)
- Functions: within 50 lines

## Workflow
1. Define/modify types.ts first
2. Implement pure functions in logic.ts
3. Write tests in *.test.ts
4. Integrate side effects in handler.ts
5. Verify lint + test + type check pass

## Domain Glossary
- [Domain term 1]: [Definition]
- [Domain term 2]: [Definition]

## Examples
- Good pattern: src/features/user-auth/logic.ts
- Anti-pattern: (omit if none)
```

### AGENTS.md Writing Guide (Feature Tier 2 Template)

```markdown
# [Feature Name] Domain Context

## Business Rules
- [Rule 1: Specific and clear]
- [Rule 2: Understandable by agents without needing inference]
- [Rule 3: Include exception cases]

## Data Flow
[Main flow]: Request -> validate -> [pure logic] -> [side effects] -> Response

## Known Edge Cases
- [Edge case 1]: [Handling method]
- [Edge case 2]: [Handling method]

## Dependencies
- shared/ modules this Feature depends on: [list]
- Other Features that reference this Feature: [list]
```

### Skills Management Guide

```
.agents/skills/
  {skill-name}/
    SKILL.md          # YAML frontmatter (name, description, tags) + execution guide
    scripts/           # Automation scripts (optional)
    examples/          # Example inputs/outputs (optional)
    tests/             # Eval scenarios for skill verification
```

**SKILL.md Example:**

```markdown
---
name: add-api-endpoint
description: "Add a new REST API endpoint to the features/ directory"
tags: [api, feature, crud]
version: "1.2.0"
---

## Steps
1. Check features/{feature-name}/ directory (create if it doesn't exist)
2. Define Request/Response types in types.ts
3. Implement business logic pure functions in logic.ts
4. Add HTTP handler in handler.ts
5. Add tests in {feature-name}.test.ts
6. Document business rules in Tier 2 AGENTS.md
7. Run lint + test + type check

## Guardrails
- Do not modify shared/ (define new types inside the feature if needed)
- Do not change signatures of existing handlers
- Do not commit code without tests
```

**Skill Loading Protocol:**
1. **Discovery**: Read only the YAML frontmatter of SKILL.md (~50 tokens)
2. **Selection**: Select the skill relevant to the task
3. **Loading**: Inject the full content of the selected skill into context
4. **Execution**: Perform work according to the skill guide
5. **Unloading**: Release from context after task completion

### Test Strategy Guide

```mermaid
graph TB
    subgraph TestPyramid["AIDE Test Pyramid"]
        HR["Human Review<br/>Architecture · Security · Domain Knowledge"]
        ES["Eval Suites (EDD)<br/>Scenario/Dataset-Based Behavioral Evaluation"]
        IT["Integration Tests<br/>Cross-Feature Coordination · Data Flow Verification"]
        PBT["Property-Based Tests<br/>Invariant Property Verification (fast-check/Hypothesis)"]
        UT["Unit Tests (TDD)<br/>Deterministic Code: Parsers · Policies · Business Logic"]
    end

    UT --> PBT --> IT --> ES --> HR

    style UT fill:#4CAF50,color:#fff
    style PBT fill:#8BC34A,color:#fff
    style IT fill:#FFC107,color:#000
    style ES fill:#FF9800,color:#fff
    style HR fill:#F44336,color:#fff
```

**Role of Each Layer:**

| Layer | Frequency | Execution Timing | Blocking Authority |
|-------|-----------|-------------------|-------------------|
| Unit Tests | Every commit | Pre-commit + CI | Merge blocking |
| Property-Based | Every commit | CI | Merge blocking |
| Integration | Every PR | CI | Merge blocking |
| Eval Suites | Every PR + on meta file changes | CI | Warning (blocking if below threshold) |
| Human Review | Every PR | PR review | Merge blocking |
| Security Tests | Daily + on meta file/policy changes | CI + scheduled execution | Merge blocking |

---



← Previous: [03-EXISTING-METHODOLOGIES](./03-EXISTING-METHODOLOGIES.md) | Next: [05-CICD-PIPELINE](./05-CICD-PIPELINE.md) →
