# AIDE (Agent-Informed Development Engineering) -- A Software Development Methodology for the Agentic Era v1.0

**Author**: CTO (20+ years of architecture experience, 3 years of hands-on AI agent experience)
**Based on**: GPT/Claude/Gemini triple deep research + Team Alpha (Integrationists) 2 reports + Team Beta (Radicals) 1 report
**Date**: 2026-02-18

---

## Part 1: AIDE Core Principles (10)

### Principle 1: Context Budget Principle -- The Context Budget Is a First-Class Design Constraint

> **"Just as memory determined programming languages, the context window determines architecture."**

#### Background and Rationale

This is the only Tier-1 principle on which all three research reports reached **complete consensus**:
- GPT report: "Context budget as a design input" (Core Principle #2, P0 requirement)
- Claude report: "The context window is the new CPU"
- Gemini report: "Context engineering is the new scarce resource"

Even with a 1-million-token context window, performance does not scale linearly. In Chroma's study measuring 18 LLMs, performance became unstable as input length increased, and the **Lost in the Middle** phenomenon caused information loss at middle positions. Tool definitions alone consume tens of thousands of tokens, degrading both reasoning quality and cost.

#### Specific Guidelines

| Item | Recommended | Upper Limit | Rationale |
|------|-------------|-------------|-----------|
| File size | 200-300 lines | 500 lines | 300 lines = ~5,400 tokens, safe even combined with system prompt + conversation history |
| Function size | 30 lines (parsers/policies/wrappers) | 50 lines | Fully comprehensible within a single reasoning turn |
| Line length | 100 characters | 120 characters | Diff review convenience |
| Meta files (CLAUDE.md) | 200 lines | 300 lines | Instruction compliance rate decreases linearly as instruction count increases |
| Files loaded per feature modification | 1-2 | 3 | Minimize indirection cost |

#### Team Alpha/Beta Discussion

Both teams reached **complete consensus** on this principle. The only difference was in implementation intensity:
- **Team Alpha**: "This is an extension of existing SRP and cohesion concepts. The quantitative basis of token cost has simply been added."
- **Team Beta**: "This should be the starting point for all architectural decisions. Maximum 3 files loaded per feature modification, maximum 1 level of indirection."

**CTO Judgment**: Team Beta's specific metrics (file load count, indirection depth) are adopted as **recommended guidelines**, but not enforced as **upper limits**. This is because infrastructure-layer DIP implementations may require up to 2 levels of indirection in some cases.

---

### Principle 2: Locality of Behavior -- Locality of Behavior Takes Priority Over Abstraction

> **"All code related to a single feature should be physically co-located."**

#### Background and Rationale

The traditional layered structure where an agent must navigate 8 files (Controller, Service, Repository, Entity, DTO, Mapper, Interface, Validator) to modify a single feature causes context fragmentation. Factory.ai's research shows that AI agents experience **dramatic performance degradation in multi-hop reasoning** (reasoning that follows references across multiple files).

This principle does not abolish "Separation of Concerns." It **changes the axis of separation**:
- Traditional: Separation by technical role (presentation / business / data)
- AIDE: Separation by feature/domain (user-auth / payment / order)

#### Specific Guidelines

```
// AIDE Pattern: Feature-Based Structure
features/
  user-auth/
    types.ts          -- Feature-specific type/schema definitions
    logic.ts          -- Pure function business logic
    handler.ts        -- HTTP/event handlers (side-effect boundary)
    store.ts          -- Data store access (side-effect boundary)
    user-auth.test.ts -- All tests for this feature
    AGENTS.md         -- Domain context for agents (Tier 2)
```

- Each Feature directory is **self-contained**: an agent can understand the entire feature by reading only that folder
- Code shared across Features goes in `shared/`, kept to a **minimum**
- Logical layers within a Feature (pure logic / side-effect boundaries) are separated at the file level

#### Team Alpha/Beta Discussion

- **Team Alpha**: "Feature-based structure is compatible with Clean Architecture's Vertical Slice Architecture. Keep the dependency rule but reduce the physical layers."
- **Team Beta**: "A fat file is better than beautiful abstraction. The moment you separate interface from implementation, the agent must load two files."

**CTO Judgment**: Feature-based structure is adopted as the **default**. As Team Alpha pointed out, this does not conflict with Clean Architecture and is a natural extension of Vertical Slice Architecture. However, the file separation of types/logic/handler/store within a Feature is maintained -- three 100-line files with distinct roles are clearer for agents than a single 300-line file containing everything. The key is to **minimize indirection crossing Feature boundaries**.

---

### Principle 3: Functional Core, Structural Shell -- Pure Function Core + Structural Shell

> **"Business logic in pure functions, side effects handled at explicit boundaries."**

#### Background and Rationale

All three reports agreed that the functional paradigm provides structural advantages for AI agents:
- **Pure functions** always produce the same output for the same input, enabling agents to reason perfectly from a single function block
- **Immutable data** allows understanding data flow as a chain without tracking state
- **Strong type systems** serve as guardrails that catch agent hallucinations at compile time

```typescript
// [1] Data: Defined as immutable structs
type User = Readonly<{
  id: string
  email: string
  name: string
  role: 'admin' | 'member' | 'viewer'
}>

// [2] Pure logic: Input -> Output, no side effects
const promote_user_to_admin = (user: User): User => ({
  ...user,
  role: 'admin'
})

// [3] Side-effect boundary: Dependency injection, explicit error handling
const handle_promote_user = async (
  userId: string,
  deps: { db: Database; logger: Logger }
): Promise<Result<User, Error>> => {
  const user = await deps.db.findUser(userId)
  if (!user) return err(new UserNotFoundError(userId))

  const promoted = promote_user_to_admin(user)
  await deps.db.saveUser(promoted)
  deps.logger.info({ event: 'user_promoted', userId })

  return ok(promoted)
}
```

#### Specific Guidelines

| Area | Recommended Paradigm | Class Usage |
|------|---------------------|-------------|
| Business logic | Pure functions | Prohibited |
| Domain model | Immutable data structures + types | Replaced with immutable Record/Type |
| Infrastructure/IO layer | Functions first, classes when necessary | Allowed (DB connections, sockets, resource management) |
| Policies/Validation | Functional pipelines | Prohibited |
| Domain boundary definition | DDD Bounded Context (type + function composition) | Not needed |

#### Team Alpha/Beta Discussion

This principle was the point of **most heated debate** between the two teams:

- **Team Alpha**: "Functional Core + OOP Shell + DDD. DDD's Aggregate, Entity, and Value Object are still valid for structuring domain knowledge. Implement them as immutable, but keep the OOP concepts."
- **Team Beta**: "FP-only. Classes hide state and increase agent cognitive load. Do not use classes for business logic."

**CTO Judgment**: The practical difference is smaller than it seems. Both teams agree that "business logic should be pure functions, data should be immutable." The difference lies in whether DDD concepts like Aggregate Root are expressed as classes or as type+function compositions. **AIDE recommends the type+function composition approach**. DDD's domain modeling **concepts** (Bounded Context, Aggregate, Value Object) are preserved, but the **implementation** is shifted to immutable types + pure functions. This satisfies both Alpha's DDD values and Beta's FP values.

Inheritance is limited to a maximum of 1 level, and deep inheritance trees are not allowed under any circumstances. Composition over Inheritance applies even more strongly in the AI era.

---

### Principle 4: Knowledge DRY, Code WET-tolerant -- Knowledge Is DRY, Code Trades Off with Locality

> **"Business rules must live in exactly one place. Duplication of utility code is tolerated for the sake of locality."**

#### Background and Rationale

The reinterpretation of the DRY principle showed the widest spectrum of opinions across the three reports:
- GPT: Manage duplication through structural solutions (cataloging)
- Claude: "DRY is not dead but transformed" -- Apply AHA (Avoid Hasty Abstractions) principle
- Gemini: Actively embrace WET/DAMP, "5 lines of logic repeated in 10 places is OK"

The self-contradiction discovered by the Claude report is the key insight: "Allow duplication -> AI generates more code -> Context window exceeded -> DRY is needed after all." Unlimited duplication tolerance is self-defeating.

#### Specific Guidelines

| Level | Strategy | Example | Duplication Tolerance |
|-------|----------|---------|-----------------------|
| **Business rules** | Strict DRY | "Discount rate calculation formula," "pricing policy" | 0 (must have a single source of truth) |
| **Domain types** | Allow re-declaration at Feature boundaries | Feature-local subset of shared User type | Reference via interface or partial re-declaration |
| **Utility code** | AHA principle | Email validation, date formatting | 2-3 duplications allowed; review extraction at 4+ |
| **Boilerplate** | Structured duplication allowed | try-catch patterns, logging patterns | Unlimited (serves as pattern anchors) |

**Duplication Management Framework**:
- Conscious Duplication: When duplicating, **state the reason in a comment**
- Drift Detection: Automate agent-based duplicate code drift detection in CI
- Periodic Review: Verify consistency of duplicate code on a quarterly basis

#### Team Alpha/Beta Discussion

- **Team Alpha**: "Knowledge DRY + Code AHA. Duplication is consciously allowed, but visible management is a prerequisite. Gemini's '5-line duplication in 10 places is OK' is extreme."
- **Team Beta**: "Aggressively WET/DAMP. Self-containment of each file is the top priority. Sharing through abstraction carries indirection costs that should be minimized."

**CTO Judgment**: Team Alpha's "Knowledge DRY + Code AHA" is adopted. Key arguments:
1. Beta effectively acknowledges that unlimited code duplication eventually exceeds the context window, creating a self-contradiction
2. However, as Alpha also acknowledges, excessive abstraction (extracting every 3-line utility into a shared module) creates harmful indirection for agents
3. Therefore, "Business knowledge is DRY, utility code allows conscious duplication under AHA guidelines" is the balance point

---

### Principle 5: Test as Specification -- Tests Are a Specification Language

> **"Tests are not verification tools but specification documents that communicate intent to agents. Apply the triple framework of TDG + PBT + EDD."**

#### Background and Rationale

Key insight from the Claude report: "TDD becomes more important in the AI era. Tests become prompt engineering." Academic validation by Matthews & Nagappan confirmed that presenting problems alongside tests improves code generation quality for both GPT-4 and Llama 3.

The revolutionary effect of Property-Based Testing (PBT) (Claude report):
- 23.1-37.3% relative improvement over TDD
- On Hard tasks: direct code generation 1.1% accuracy vs. property-based verification 48.9% accuracy
- LLMs are **far better at defining correctness properties than generating correct code**

#### Specific Guidelines

**Triple Test Framework:**

```
                     +------------------+
                     |   Human Review   |  Architecture, security, domain knowledge
                     +------------------+
                    +--------------------+
                    |  Eval Suites (EDD) |  Scenario/dataset-based behavioral evaluation
                    +--------------------+
                  +------------------------+
                  | Integration Tests      |  Integration verification of AI-generated code
                  +------------------------+
                +----------------------------+
                | Property-Based Tests (PBT) |  Invariant property verification
                +----------------------------+
              +--------------------------------+
              | Unit Tests (TDD)               |  Deterministic code: parsers, policies, tool wrappers
              +--------------------------------+
```

| Test Type | Target | Tools | Author |
|-----------|--------|-------|--------|
| **Unit (TDD)** | Deterministic code -- parsers, policies, state transitions, tool wrappers | Jest/Vitest/pytest | Human spec -> AI implementation |
| **PBT** | Business invariant properties -- "total is always >= 0," "order preserved after sort" | fast-check/Hypothesis | Humans define properties, AI generates |
| **Integration** | Integration scenarios of AI-generated code -- cross-Feature coordination, data flow verification | Custom test framework | AI-generated, human-reviewed |
| **Eval (EDD)** | Model output quality -- accuracy, safety, usefulness | Custom eval framework | Human-designed + production failure incorporation |
| **Security** | Security vulnerabilities in AI-generated code (XSS, SQL Injection, logic errors) | OWASP-based scenarios + Security linters | Security team designs, automated execution |

**Confirmation Bias Prevention Is Mandatory**: When AI writes both tests and implementation, there is a risk of creating "tests that verify bugs." Use **different models for test writing and code writing**, or have **humans review the test specifications**.

#### Team Alpha/Beta Discussion

- **Team Alpha**: "TDG (Test-Driven Generation) + PBT + EDD extension. Don't discard TDD; extend it for the AI era."
- **Team Beta**: "Dual framework -- Traditional TDD for deterministic code, EDD for probabilistic behavior. Actively adopt PBT."

**CTO Judgment**: These are **practically identical proposals**. The test strategies from both teams are merged into the triple framework above. The only difference was in naming.

---

### Principle 6: Progressive Disclosure -- Progressive Disclosure of Information

> **"Do not give agents all information at once. Provide only what is needed, when it is needed."**

#### Background and Rationale

GPT report's progressive skill loading, Claude report's 3-Tier Progressive Disclosure, and Gemini report's dynamic information loading all express the same principle: **Like virtual memory in an operating system, do not load everything into physical memory; load it when needed.**

#### Specific Guidelines

**Meta File 3-Tier System:**

| Tier | File | Role | Size Limit | Loading Method |
|------|------|------|------------|----------------|
| **Tier 1: Constitution** | `CLAUDE.md` / `AGENTS.md` (root) | Project identity, absolute rules, architecture map | 300 lines max | Always loaded |
| **Tier 2: Local Laws** | `AGENTS.md` in subdirectories | Component-specific patterns, domain context | 200 lines max | Lazy loaded when working in that directory |
| **Tier 3: Technical Manuals** | `.agents/skills/*/SKILL.md` | Procedural knowledge, workflow guides | YAML frontmatter + body | On-demand loading |

**Progressive Provision of Dependency/Library Information:**

When conveying information about external libraries and internal shared modules used in the project to agents, a progressive approach is also needed:

| Level | Information Provided | Purpose |
|-------|---------------------|---------|
| **Summary** | Library name + version + one-line purpose description | Agent grasps the overall technology stack |
| **API Signatures** | Only signatures of functions/types in use | Agent writes code that integrates with the library |
| **Detailed Documentation** | Example code, configuration methods, caveats | Agent builds new integrations or troubleshoots |

The key is to "never load the full documentation of every library into the context." Providing only the needed depth of information at the needed time allows efficient use of the context budget.

#### Team Alpha/Beta Discussion

**Both teams reached complete consensus.** Implementation details were also nearly identical. The 3-Tier meta file system and the progressive information provision principle were combined to establish the system above.

---

### Principle 7: Deterministic Guardrails -- Deterministic Guardrails for Probabilistic Generation

> **"Trust the AI agent, but verify. And verification must be deterministic."**

#### Background and Rationale

Security status of AI-generated code (Claude report, Veracode 2025):
- **Approximately 45% of generated code contains security flaws**
- Logic error rate **1.75x** that of humans
- XSS vulnerabilities **2.74x**
- **Independent of model size** -- smarter models do not produce safer code

This data clearly demonstrates that "prompting agents to 'do well'" is insufficient. Deterministic tools must verify agent output.

#### Specific Guidelines

```
Probabilistic Generation (AI)  -->  Deterministic Verification  -->  Pass/Fail
                                      |
                                      +-- TypeScript strict mode (type verification)
                                      +-- ESLint/Prettier (style enforcement)
                                      +-- Zod/io-ts (runtime type verification)
                                      +-- Pre-commit hooks (automatic execution)
                                      +-- Security linters (security verification)
                                      +-- CI test suite (regression prevention)
```

**Absolute Rule**: "Never send an LLM to do a linter's job" (Claude report). Style enforcement, type verification, and security pattern detection are all delegated to deterministic tools.

**Self-Healing Loop** (Gemini report's Reflexion Pattern):
```
Generate -> Compile/Lint -> Test -> Analyze Errors -> Regenerate -> ...
```

For this loop to work effectively, error messages must be provided in a **machine-readable structured format (JSON)**.

#### Team Alpha/Beta Discussion

**Both teams reached complete consensus.** Team Beta emphasized this principle most strongly, presenting the intuitive expression "trust me but verify," and Team Alpha agreed.

---

### Principle 8: Observability as Structure -- Observability Is Part of the Structure

> **"AI-generated code must include structured logging and tracing by default. Observability is a first-class citizen."**

#### Background and Rationale

All three reports reached **complete consensus**: If you cannot trace "why this behaves this way" for code that AI generates rapidly, operations and debugging become impossible. AI agents must structurally embed observability when generating code.

- GPT report: Include Observability as a cross-cutting concern in architecture
- Claude report: Tracing ON by default, traces mandatory from development stage
- Gemini report: Adopt semantic logging (JSON-LD) standard

#### Specific Guidelines

```typescript
// Structured log format -- Must be included in all code generated by AI
type StructuredLog = {
  level: 'info' | 'warning' | 'error' | 'critical'
  timestamp: string       // ISO 8601
  service: string         // Service/Feature identifier
  event: string           // Business event name
  trace_id: string        // Distributed tracing ID
  span_id: string         // Current work unit ID
  data: Record<string, unknown>  // Structured supplementary data
}

// Usage example: E-commerce payment processing
const handle_payment = async (
  order_id: string,
  deps: { db: Database; pg: PaymentGateway; logger: Logger }
): Promise<Result<PaymentResult, Error>> => {
  deps.logger.info({
    event: 'payment_initiated',
    data: { order_id }
  })

  const result = await deps.pg.charge(order_id)

  if (result.success) {
    deps.logger.info({
      event: 'payment_completed',
      data: { order_id, transaction_id: result.transaction_id }
    })
  } else {
    deps.logger.error({
      event: 'payment_failed',
      data: { order_id, reason: result.error }
    })
  }

  return result
}
```

**Key Guidelines:**
- **Distributed tracing by default**: Track request flow with `trace_id` -> `span_id`. Leverage standards such as OpenTelemetry
- **ON by default from the development stage**: Activate structured logging not only in production but also in local development
- **Cost/performance metrics**: Track API response time, DB query count, and external API call count in real time
- **Mandate observability in AI-generated code**: When requesting code from agents, specify in CLAUDE.md: "Include structured logging in all handlers"

#### Team Alpha/Beta Discussion

**Both teams reached complete consensus.** There was no disagreement that observability is fundamental to software operations and becomes even more critical in AI-generated code.

---

### Principle 9: Security by Structure -- Structural Security Verification

> **"45% of AI-generated code has security flaws. Security verification must be structurally embedded."**

#### Background and Rationale

As AI has become the primary producer of code, the nature of security threats has changed. Security vulnerabilities in AI-generated code itself are the core threat:

- Veracode 2025: Approximately 45% of AI-generated code contains security flaws
- XSS vulnerabilities 2.74x humans, logic errors 1.75x
- Model size does not correlate with security quality

#### Specific Guidelines

**Threat-Control Mapping:**

| Threat | Representative Scenario | Defense Point | Recommended Control |
|--------|------------------------|---------------|---------------------|
| SQL Injection | AI generates string concatenation instead of parameterized queries | Security linter + Code review | Linter rules to detect raw query usage, enforce ORM/Query Builder |
| XSS | AI omits user input escaping | Security linter + Template engine | Enforce auto-escaping frameworks, DOMPurify, etc. |
| Logic errors | Missing authorization checks, unhandled boundary conditions | PBT + Integration test | Verify invariant properties with Property-Based Testing |
| Auth/AuthZ flaws | AI omits authentication middleware | Architecture enforcement | Apply authentication middleware by default at router level, allow explicit opt-out only |
| Dependency vulnerabilities | AI adds packages with vulnerable versions | SCA (Software Composition Analysis) | Automated scanning with npm audit, Snyk, etc. |

**Three Security Principles:**
1. **Automated security verification**: Automatically run security linters in CI for all AI-generated code
2. **Mandatory security review**: Code changes involving authentication, payments, and personal data must undergo security review
3. **Audit trail**: All sensitive data access and state changes are recorded in structured logs

#### Team Alpha/Beta Discussion

**Both teams reached complete consensus.** Security is an area with no room for compromise.

---

### Principle 10: Meta-Code as First-Class -- Meta-Code as a First-Class Citizen

> **"AGENTS.md, CLAUDE.md, and Skills files are version-controlled and tested with the same rigor as source code."**

#### Background and Rationale

- AGENTS.md is used in **60,000+ open-source projects** (managed by the Agentic AI Foundation under the Linux Foundation)
- Research shows that practices failing to preserve prompts/context weaken reproducibility
- A single-line change in a meta file can alter the agent's entire behavior, meaning it can have **higher impact than code**

#### Specific Guidelines

**Meta-Code Management Principles:**
1. **Version control**: Same workflow as code in Git -- PR, code review, changelogs, release tags
2. **Run evals on change**: Meta file changes automatically trigger eval suite execution in CI (behavioral regression detection)
3. **Size monitoring**: CI warns/blocks when Tier 1 files exceed 300 lines
4. **Use negative instructions**: "Do not do X" is often clearer and easier to detect violations
5. **Example-based instructions**: Concrete code examples dramatically improve agent output quality over abstract principles

**Lock Down Full Configuration with manifest.yaml:**

```yaml
# manifest.yaml
spec_version: "1.0"
project_name: "my-ecommerce"
project_type: "backend"

tech_stack:
  language: "typescript"
  runtime: "node"
  framework: "express"
  database: "postgresql"
  cache: "redis"

ai_development:
  primary_model: "claude-opus-4-6"
  instruction_files:
    tier1: ["CLAUDE.md", "AGENTS.md"]
    tier2_pattern: "src/features/*/AGENTS.md"

code_standards:
  max_file_lines: 300
  max_function_lines: 50
  paradigm: "functional-core"
  type_strictness: "strict"

testing:
  unit: "vitest"
  property: "fast-check"
  e2e: "playwright"

observability:
  logging: "structured_json"
  tracing: true
```

#### Team Alpha/Beta Discussion

**Both teams reached complete consensus.** Both teams accepted Gemini's "Meta-Control Plane" concept.

---



← Previous: [00-PREFACE](./00-PREFACE.md) | Next: [02-ARCHITECTURE-PATTERNS](./02-ARCHITECTURE-PATTERNS.md) →
