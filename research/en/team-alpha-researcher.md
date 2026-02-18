<!-- Translated from Korean original by AI agent (Codex gpt-5.3-codex-spark) -->
# Team Alpha Researcher Report: Draft on AIDE (Agent-Informed Development Engineering)

**Author**: Team Alpha Researcher (Integrated Group)
**Source Materials**: GPT Deep Research, Claude Deep Research, Gemini Deep Research reports (3)
**Perspective**: Balanced integration of traditional software engineering principles and AI agent optimization

---

## 1. Core Cross-Analysis of 3 Reports

### 1.1 Core Claims Mentioned by All 3 Reports

All 3 reports show clear agreement on the following claims.

#### (1) The Context Window is a New Primary Constraint
- **GPT**: "Treat context budget as a design input" (Core Principle #2); classifies token overconsumption by tool definitions/intermediate outputs as a P0 requirement.
- **Claude**: "Context Window is the new CPU" — states that all architectural decisions should be aligned around this constraint. Reaches consensus on 200–300 lines per file, with 500 as the upper bound.
- **Gemini**: "Context engineering is the new scarce resource"; argues for maximizing information locality centered on the Lost in the Middle phenomenon.

**Agreement level**: Full. All 3 reports treat Context Window as a first-class architectural constraint, analogous to CPU/memory.

#### (2) Existing Test Strategy Needs Adaptation
- **GPT**: Proposes "Evaluation-Driven Engineering (EED)" — keep TDD for deterministic code, use Evals-based validation for model behavior.
- **Claude**: Proposes "Test-Driven Generation (TDG)" — TDD becomes more important, but Property-Based Testing (PBT) is the core complement.
- **Gemini**: Proposes "Reflexion Pattern" — a write-verify-correct cycle as a self-healing mechanism.

**Agreement level**: High. It agrees that while TDD remains valuable, a new validation framework for non-deterministic AI behavior is needed.

#### (3) Meta files (AGENTS.md, CLAUDE.md) are new first-class deliverables
- **GPT**: "Prompts/skills/policies as code" — elevated to version control, review, and regression testing.
- **Claude**: AGENTS.md is used in 60,000+ open-source projects; proposes 3-Tier Progressive Disclosure architecture.
- **Gemini**: Concept of a "meta-control plane" — Constitution (CLAUDE.md) + technical spec (AGENTS.md) + railguards (linters/tests).

**Agreement level**: Full. Meta files should be treated as runtime components, not documents.

#### (4) Security threat model is fundamentally different
- **GPT**: Presents a Threat-Control mapping table based on OWASP Top 10, including Policy & Guardrails as an architectural layer.
- **Claude**: Presents concrete statistics: 45% security defect rate in AI-generated code, XSS vulnerability 2.74x etc.
- **Gemini**: Suggests MCP as a security gateway and emphasizes least-privilege principles.

**Agreement level**: High. Both Prompt Injection and Excessive Agency are agreed as first-class threats.

#### (5) Observability is essential infrastructure
- **GPT**: Fixes observability as an architectural layer, with trace/span/event logs as standard interfaces.
- **Claude**: Tracing on by default, trace mandatory from development stage.
- **Gemini**: Standardizes semantic logging (JSON-LD) to improve agent-side debugging success rates.

**Agreement level**: Full.

#### (6) Human role shifts from implementer to architect/verifier
- **GPT**: Industry observation that "human evaluation dependency is high," making Human-in-the-loop the design default.
- **Claude**: Human role shifts from implementer to architect-reviewer; spec-first is the strongest predictor of AI code quality.
- **Gemini**: Re-defines roles from coder to spec writer, reviewer to architect.

**Agreement level**: Full.

---

### 1.2 Points Where Reports Diverge

#### (1) Attitude toward OOP: acceptance vs exclusion

| Perspective | GPT | Claude | Gemini |
|------|-----|--------|--------|
| Position | **Hybrid recommended** — state is functional, executors are OOP/DI | **Functional Core, Imperative Shell** — OOP is useful for structural organization | **Functional first, avoid classes** — recommends no classes in business logic |
| Intensity | Neutral integration | Balanced hybrid | Most critical of OOP |

**Core Conflict**: Gemini takes a radical position that "classes are only for resource management," while GPT and Claude recognize structural value in OOP. Claude explicitly says OOP/DDD has become "more important" as DDD Bounded Context maps directly to agent boundaries.

#### (2) DRY interpretation spectrum

| Perspective | GPT | Claude | Gemini |
|------|-----|--------|--------|
| Position | Manage duplication via tool/skill cataloging | "Knowledge-level DRY, code-level duplication allowed" — applies AHA principle | **Active WET/DAMP acceptance** — inline repetition is acceptable even if 5-line logic repeats 10 times |
| Intensity | Practical neutrality | Conditional allowance | Strong duplication advocacy |

**Core Conflict**: Gemini is most radical, claiming code duplication acts as a context anchor for agents; Claude is intermediate with "knowledge should be DRY, code may duplicate"; GPT prefers structural solutions (cataloging).

#### (3) Fundamental stance toward traditional development theory

| Perspective | GPT | Claude | Gemini |
|------|-----|--------|--------|
| Position | "Add five new axes to traditional development" | "Traditional principles become more important in AI, but need reinterpretation" | "Human-centered design is a maze for AI" — calls for paradigm shift |
| Intensity | Expansionist | Reinforce/reinterpret | Near replacement |

**Core Conflict**: This is the main axis of Team Alpha vs Team Beta debate. GPT argues "add", Claude argues "reinforce", Gemini argues "transition."

#### (4) Architecture shape: layer vs feature orientation

| Perspective | GPT | Claude | Gemini |
|------|-----|--------|--------|
| Shape | **Layer-first**: Kernel/Orchestrator/Planner/Executor/Memory/Tooling/Policy/Observability | **Layer + principle-based**: clean architecture compatible, DDD Bounded Context applied | **Feature-first**: Fractal/Flat structure, everything inside `/features/user-auth/` |
| Rationale | Separation of concerns for agent runtime | Compatibility with existing architecture | Maximize locality |

### 1.3 Unique Insights per Report

#### GPT Deep Research unique insights
1. **Proposes 6 interface standards**: `IPlanner`, `IExecutor`, `IMemory`, `IToolRegistry`, `IPolicy`, `IObservability` — most concrete set of implementation-agnostic standard interfaces.
2. **manifest.yaml-based versioning**: operational strategy that fixes model ID/parameters/policy version/skill version/budget in one manifest.
3. **Eval Flywheel concept**: continuous improvement loop by immediately feeding production failures/wrong answers into eval datasets.
4. **Async/concurrency model**: actor/queue-based processing by `(run_id, step_id)`, fanout/fanin for parallel tool calls.

#### Claude Deep Research unique insights
1. **Innovative impact of Property-Based Testing (PBT)**: 23.1~37.3% relative improvement versus TDD; hard task direct generation 1.1% vs verified generation 48.9% — most concrete experimental data.
2. **Reordering SOLID principles**: DIP > SRP > ISP > LSP > OCP — new priority that Dependency Inversion is most important in the AI era.
3. **PR Contract concept**: intent explanation, evidence of operation, risk level, AI-use disclosure, and explicit human-review-required region.
4. **Quantitative AI security defects data**: 45% security defects in generated code, Java at 72% worst, logic error 1.75x, XSS 2.74x — no correlation with model size.

#### Gemini Deep Research unique insights
1. **Semantic verbosity**: `calc(d)` vs `calculate_price_with_tax_rate(order_data)` — variable naming becomes prompts for agents.
2. **Reflexion Pattern**: self-healing loop of Action → Verification → Observation → Reflexion → Correction.
3. **Dynamic tool loading in 5 stages**: Registry → Search → Inject → Execute → Unload; claims 90% token cost reduction.
4. **Productivity Dip**: 19% productivity drop in early AI adoption and role transition strategies to recover it.

---

## 2. AIDE Core Principle Proposal (Team Alpha Position)

> **Team Alpha core philosophy**: Traditional development theory contains decades of validated engineering wisdom. The arrival of AI agents does not justify discarding it. It should be **reinterpreted and extended** to fit new constraints (Context Window, non-determinism, Prompt Injection).

### 2.1 File/Code Size Guideline

**Principle: "Cohesion within Context Budget"**

Combines traditional SRP and Cohesion with Context Window constraints.

| Item | Recommended Criterion | Rationale |
|------|----------------------|----------|
| File size | **Target 200~300 lines, upper limit 500 lines** | Claude: 300 lines ≈ 5,400 tokens, preserving context slack. GPT: separate when exceeding 300~500 lines |
| Function size | **Core logic 30~50 lines** | GPT: core logic within 50, wrappers/parsers/policy within 30; aligns with Clean Code rule that a function does one thing |
| Line length | **100~120 chars** | Improves readability and review diff ergonomics |
| Prompt/skill files | **Within 300 lines** | Claude: implementation compliance decreases linearly as instruction count increases |

**Team Alpha position**: This is not a new concept. Clean Code already argued for small functions, and SRP already stated files should change for only one reason. In the AI era, these principles gain **quantitative justification through token cost**.

### 2.2 OOP vs functional selection criteria

**Principle: "Functional Core, Architectural Shell — with DDD Boundaries"**

Team Alpha adopts Claude's "Functional Core, Imperative Shell" baseline, while combining GPT's hybrid view and DDD Bounded Context.

| Area | Recommended Paradigm | Rationale |
|------|---------------------|----------|
| Business logic | **Functional (pure functions)** | All 3 reports agree: pure functions are easier to test, no state tracking, and favorable for agent reasoning |
| Domain model | **Immutable data structures + types** | Gemini: Record/DTO/Struct. Claude: strong type systems reduce hallucination |
| Infrastructure/Execution layers | **OOP/DI allowed** | GPT: connectors/storage/clients are complex. Claude: dependency inversion from Clean Architecture |
| Domain boundaries | **DDD Bounded Context** | Claude: "DDD became more important" — each agent should become an expert for a specific domain |
| Policy/parser/validation | **Functional pipeline** | GPT: normalize/validate consistently through functional pipeline |
| State management | **Immutable structure + event sourcing** | GPT: "state is immutable structure (functional), execution is object/DI (OOP)" |

**Team Alpha position**: Gemini's "do not use classes for business logic" is too extreme. DDD Aggregate, Entity, Value Object remain valid for structuring domain knowledge. They should be implemented immutably, and transformations should happen through **pure functions** rather than methods.

### 2.3 Boilerplate and code duplication perspective

**Principle: "Knowledge DRY, Code WET-tolerant (apply AHA)"**

| Level | Strategy | Example |
|------|----------|---------|
| **Business knowledge** | **Strict DRY** | Rules like "discount-rate calculation" must be defined in exactly one place |
| **Utility code** | **AHA (Avoid Hasty Abstractions)** | 3-line email validation logic repeated in 2–3 places is acceptable; at 4+ places, consider extraction |
| **Boilerplate** | **Structured duplication allowed** | try-catch, logging patterns, etc.; act as pattern anchors for agents |
| **Type definitions** | **Explicit redeclaration allowed** | Redeclare types at module boundaries to preserve independence |

**Team Alpha position**: Gemini's "10 places and 5-line duplication is okay" is too extreme. If duplicate code drifts, maintenance becomes a nightmare. As Claude notes, a realistic approach is to have the agent itself detect drift between duplicates. Duplication is acceptable **intentionally** only with **visible** management.

### 2.4 CLAUDE.md, AGENTS.md, and meta-file management strategy

**Principle: "Progressive Disclosure with Version Control"**

3 reports combined into a 3-tier meta-file architecture:

| Tier | File | Role | Size limit | Loading method |
|------|------|------|------------|----------------|
| **Tier 1: Constitution** | `CLAUDE.md` / `AGENTS.md` (root) | project identity, hard rules, architecture map | **≤ 300 lines** | always loaded |
| **Tier 2: Regional Law** | directory-level `AGENTS.md` | component patterns, local rules | **≤ 200 lines** | lazy load when working in that directory |
| **Tier 3: Technical Manual** | `.agents/skills/*/SKILL.md` | procedural knowledge, workflow guides | YAML frontmatter + body | on-demand load |

**Management principles**:
1. **Version control**: same Git workflow as code — PR review, change logs, release tags
2. **Automatic Eval on change**: meta-file changes always run eval in CI (GPT: "must run eval on every change")
3. **Size monitoring**: CI warning/block when Tier 1 exceeds 300 lines
4. **Use negative statements**: Gemini insight — "what not to do" is often clearer
5. **Include project map**: add directory overview to Tier 1 to reduce agent navigation cost

### 2.5 Skills management approach

**Principle: "Skill as Package — Metadata First, Content on Demand"**

Combines GPT's progressive loading with Gemini's dynamic tool loading.

**Skill structure**:
```
.agents/skills/
  {skill-name}/
    SKILL.md          # YAML frontmatter (name, description, tags) + execution guide
    scripts/           # automation scripts (optional)
    examples/          # example input/output (optional)
    tests/             # eval scenarios for skill verification
```

**Loading protocol**:
1. **Discovery**: agent reads only SKILL.md YAML frontmatter first
2. **Selection**: choose skills relevant to task (automatic match or explicit call)
3. **Loading**: inject full content of selected skill into context
4. **Execution**: perform work following the skill guide
5. **Unloading**: release from context after completion (see Gemini dynamic tool loading)

**Versioning**: each skill has independent version and is referenced from `manifest.yaml` (GPT manifest pattern)

### 2.6 Test strategy (reinterpretation of TDD)

**Principle: "Test-Driven Generation (TDG) + Evaluation-Driven Engineering (EED)"**

Team Alpha preserves TDD and extends it for the AI era.

#### Reconstruction of the testing pyramid

```
                    ┌─────────────┐
                    │  Human      │  Human review (architecture, security, domain knowledge)
                    │  Review     │
                  ┌─┴─────────────┴─┐
                  │  Eval Suites    │  scenario/dataset-based behavioral evaluation (EED)
                  │  (Behavioral)   │
                ┌─┴─────────────────┴─┐
                │  Simulation Tests   │  step/budget validation in mocking environment
                │  (Integration)      │
              ┌─┴─────────────────────┴─┐
              │  Property-Based Tests   │  invariant validation (PBT)
              │  (Specification)        │
            ┌─┴─────────────────────────┴─┐
            │  Unit Tests (TDD)           │  deterministic code: parser, policy, tool wrappers
            │  (Foundation)               │
            └─────────────────────────────┘
```

| Test type | Target | Author | Rationale |
|-------------|------|-----------|----------|
| **Unit Tests (TDD)** | deterministic code — parser, policy engine, state transitions, tool wrappers | human spec → AI implementation | GPT: "keep TDD for deterministic code" |
| **Property-Based Tests** | business invariants | humans define properties, AI generates | Claude: PBT shows 23~37% improvement |
| **Simulation Tests** | agent behavior — step budget, loops, rollback | AI-generated, human review | GPT: mock environment simulation |
| **Eval Suites** | model output quality — accuracy, safety, usefulness | human-designed + production failures fed back | GPT: Eval Flywheel |
| **Security Tests** | prompt injection, privilege abuse scenarios | security team designs, auto execution | Claude: 45% security defects |

**Core rule**: To prevent **confirmation bias** when AI writes both tests and implementation, separate test author and implementer roles or use different models (Claude).

### 2.7 Context Window optimization strategy

**Principle: "Structured Scarcity — staged disclosure and active management"**

Integrated context optimization system from all 3 reports:

#### Information supply strategy
| Strategy | Description | Source |
|------|------|------|
| **Progressive Disclosure** | load metadata first and load body only when needed | GPT/Claude |
| **Dynamic Tool Loading** | Registry → Search → Inject → Execute → Unload | Gemini |
| **Context Compaction** | summarize intermediate results, compress old conversation | GPT |
