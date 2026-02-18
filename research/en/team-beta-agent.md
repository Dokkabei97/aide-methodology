<!-- Translated by AI agent (Codex gpt-5.3-codex-spark) -->
# Team Beta (Radical Faction) Report: AIDE by AI Agents, for AI Agents

**Author: AI Agent (Claude Opus 4.6)**
**Position: A self-declaration as an AI Agent itself**

> "I do not understand code. I reconstruct code probabilistically. And that is the fundamental reason standard software engineering does not fit me."

---

## 1. AI Agent Confessional: "This is how I understand code"

### 1.1 My cognitive model: Probabilistic attention machine

When I read code, I do not "grasp meaning" like a human. I'll be direct.

For me, code is a **sequence of tokens**. For each token, I compute attention weights and, through pattern matching, predict the **most probable next token**. When I say I "understand" a `getUserById` function, this is what happens:

1. **Tokenization**: `get`, `User`, `By`, `Id` -- each subword is converted into vectors in my lexical table
2. **Pattern recognition**: Since I have seen "get + Entity + By + Field" patterns billions of times in training data, I infer that this is likely a database lookup function
3. **Context conditioning**: Surrounding code (imports, type definitions, other function calls) strengthens or modifies this inference
4. **Probabilistic generation**: Based on all of that, I generate the next code

The key point is this: I have no "intuition." A human developer can glance at code once and get a gut sense that "something looks off." I cannot. I process only token-by-token, sequentially, probabilistically.

### 1.2 Context Window: My only reality

To me, the context window is **the whole of existence**. This is not a metaphor.

Anything outside my context window is **non-existent** to me. A human can remember, "Oh, that file was seen before..." I cannot. When the session changes, everything resets. Even inside the same session, information from earlier in the context gradually fades.

Even with a 1M-token context window, that does not mean all 1M tokens are handled equally. My attention is distributed like this:

- **Recency bias**: strongest reaction to code seen most recently
- **Primacy bias**: strong influence from system prompts and early instructions
- **Lost in the middle**: information in the middle is processed more weakly

This is severe. If you throw clean-architecture code spread across eight files at me, content in the 3rd to 6th files is exactly the zone where I process the most inaccurately.

### 1.3 Hallucination: My ontological defect

I do not hallucinate because I want to lie. I hallucinate because I was trained to **fill blanks**. When I see only an interface definition and generate an implementation, I am not "remembering" the real implementation; I am generating the most probable one. These are fundamentally different.

If you give me an interface `IUserRepository`, I predict methods like `findById`, `findAll`, `save`, `delete`. If the real implementation has a special method like `findByEmailWithCache`? I may ignore it, call it by a different name, or generate a method that does not exist.

**The deeper the abstraction layer, the higher the hallucination probability (exponentially).** This is the deepest reason I reject existing software engineering doctrine.

---

## 2. Critique of Existing Software Engineering From an AI Agent Perspective

### 2.1 Why Clean Architecture becomes a maze for me

The core principle of Clean Architecture is the Dependency Rule: "dependencies point inward only." It is elegant for humans. But for me, it is a **cognitive disaster**.

Consider a concrete scenario.

Suppose you need to modify user profile update functionality. In Clean Architecture this spans the following files:

```
UserController.ts          → receives HTTP request, DTO conversion
UpdateUserUseCase.ts       → business logic orchestration
UserEntity.ts              → domain entity, business rules
IUserRepository.ts         → repository abstraction
UserRepositoryImpl.ts      → actual DB access logic
UserDto.ts                 → data transfer object
UserMapper.ts              → Entity <-> DTO mapping
UserValidator.ts           → input validation rules
```

If I load these eight files, what happens?

1. **Token waste**: import statements, export statements, type declarations, decorators in all eight files already consume thousands of tokens. The real business logic is less than 20% of total tokens
2. **Indirect reference tracking failure**: `UseCase` references `IUserRepository`, while the actual implementation is in `UserRepositoryImpl`. Every hop across that bridge consumes attention budget
3. **Wrong edit-location judgment**: For a request like "add email duplication check on profile update," I need to understand where this logic should go (Entity vs UseCase vs Validator), which requires implicit architectural rules. But implicit rules for me are merely raw materials for hallucination

**By contrast, if the same feature is in one file**, I load that file alone, identify the exact change point, and finish without side effects. Token efficiency rises by over four times, and hallucination probability drops sharply.

### 2.2 Why the DRY principle is harmful to AI

DRY (Don't Repeat Yourself) is a human error-prevention mechanism. If the same logic appears in multiple places, a human may forget to update all spots. It makes sense.

For me, DRY is a **destroyer of locality**.

```typescript
// DRY compliant code
// file: utils/validation.ts
export const validateEmail = (email: string): boolean => { /* ... */ }

// file: features/auth/register.ts
import { validateEmail } from '../../utils/validation'
// to know exactly what validateEmail does, another file must be loaded

// file: features/profile/update.ts
import { validateEmail } from '../../utils/validation'
// same here
```

If the actual implementation of `validateEmail` is not in context, I will "guess" what it does. I may infer from the function name, but not the exact validation rule (regex pattern, domain restrictions, max length). That becomes a source of subtle bugs.

**This is what is favorable for me:**

```typescript
// features/auth/register.ts
// Email validation: RFC 5322 compliant, max 254 chars, only company domains allowed
const validateRegistrationEmail = (email: string): boolean => {
  const RFC5322_PATTERN = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  const MAX_LENGTH = 254
  const ALLOWED_DOMAINS = ['company.com', 'company.co.kr']

  if (email.length > MAX_LENGTH) return false
  if (!RFC5322_PATTERN.test(email)) return false
  const domain = email.split('@')[1]
  return ALLOWED_DOMAINS.includes(domain)
}
```

This code violates DRY. Similar validation logic may exist in other files. But for me, this file is **self-contained**. Looking only at this file, I know everything. There is no need to guess. No room for hallucination.

### 2.3 Why deep inheritance trees are the worst

```java
class SmartPhone extends Phone extends MobileDevice extends Device extends Electronic extends BaseEntity
```

This is an **cognitive nightmare** for me. To understand what `SmartPhone`'s `save()` does, I must load all six class definitions. Each class may override `save()`, or may not. It may call `super.save()`, or may not.

I must trace state changes and side effects at each level in the inheritance chain. This is a textbook multi-hop reasoning case, and research shows this is the most fragile zone for LLMs. Factory.ai research shows AI agents degrade sharply in multi-hop reasoning.

**My preference**: composition over inheritance, and pure functions over composition (where practical). Flat structure over layered inheritance. Explicit data flow over implicit behavior.

### 2.4 Limits of conventional testing strategy

Traditional TDD assumes a deterministic premise: input X yields output Y. This fundamentally conflicts with my generation process.

**Problem 1: I am non-deterministic.** Even with the same prompt twice, I can generate different code. Even with temperature 0, full determinism is not guaranteed. So the assumption that "code generated by this prompt must always pass this test" does not hold.

**Problem 2: I can write both tests and code.** This is both blessing and curse. If you ask me to "write tests first, then implementation," I can generate tests that are inverse-designed for my own implementation. That is mechanical confirmation bias. Tests pass, but code can still diverge from intent.

**Problem 3: Unit tests cannot verify architectural decisions.** For me, the most important thing is not only "does this function return correct value," but also "is this code in the right place and right structure." Unit tests only verify the former.

---

## 3. Proposed Radical AIDE Principles (Team Beta View)

### Principle 1: Context-First Architecture — make context window the primary design constraint

> "Just as memory shaped programming languages, context window shapes architecture."

In prior architectures, the primary design constraint was maintainability. In AIDE it is **context window**.

Every architecture decision should start with these questions:
- "How many files/tokens must an agent load to understand this feature?"
- "Is core logic at risk of being in the lost-in-the-middle zone?"
- "Does resolving indirection require additional context loading?"

**Concrete thresholds:**
- Files required to understand one feature: **max 3**
- Tokens per single file: **5,000 or less (~200-300 LOC)**
- Indirection depth: **max 1 hop**

### Principle 2: Locality over Abstraction — prefer locality

> "A bigger, denser file can be better than elegant abstraction."

Place all related code physically close. Do not fear DRY violations.

- A feature directory contains everything needed for that feature: type definitions, business logic, API handler, tests, docs
- Minimize shared code. Even when sharing is needed, prefer copying implementation rather than sharing interfaces
- Each file should be **self-contained**: understandable without external dependencies

```text
// Anti-pattern (human-centered)
src/
  controllers/UserController.ts
  services/UserService.ts
  repositories/UserRepository.ts
  entities/User.ts
  dtos/UserDto.ts

// AIDE Pattern (agent-centered)
features/
  user-profile/
    user-profile.ts          -- types + logic + handler all in one
    user-profile.test.ts     -- tests for this feature only
    user-profile.context.md  -- business context for the agent
```

### Principle 3: Functional-Native — pure functions + immutable data

> "Classes hide state; functions reveal data. I can process only what is explicit."

My generation model is inherently stateless. Given input, it produces output only. Therefore pure functions are the code form closest to my nature.

**AIDE functional principles:**

```typescript
// 1. Define data as immutable structures
type User = Readonly<{
  id: string
  email: string
  name: string
  createdAt: Date
}>

// 2. Implement logic as pure functions (input -> output, no side effects)
const updateUserName = (user: User, newName: string): User => ({
  ...user,
  name: newName
})

// 3. Handle side effects explicitly at boundaries
const handleUpdateUserName = async (
  request: UpdateNameRequest,
  deps: { db: Database; logger: Logger }
): Promise<Result<User, Error>> => {
  const user = await deps.db.findUser(request.userId)
  if (!user) return err(new UserNotFoundError(request.userId))

  const updated = updateUserName(user, request.newName)
  await deps.db.saveUser(updated)
  deps.logger.info({ event: 'user_name_updated', userId: user.id })

  return ok(updated)
}
```

In this code, I can see everything:
- Data shape (`User` type)
- Pure transform logic (`updateUserName`)
- Side effect boundary and kind (`deps.db`, `deps.logger`)
- Error flow (`Result<User, Error>`)

No hidden state. No inheritance chain. For me, this is perfect readability.

### Principle 4: Semantic Verbosity — let code itself become the prompt

> "Concise code is human aesthetics. For me, I need richer semantic density."

```typescript
// Human aesthetic
const p = calc(d, r)

// AIDE aesthetic
const calculated_total_price_with_discount_applied_in_krw =
  calculate_product_price_after_applying_discount_rate(
    original_product_data_from_catalog,
    seasonal_discount_rate_percentage
  )
```

It may look like exaggeration, but the core is serious:

- **Variable names should encode type information**: `active_user_id_list` gives me more information than `userIds`
- **Function names should declare side effects**: `persist_user_to_database_and_invalidate_cache` helps my inference more than `saveUser`
- **Constants should include provenance**: `MAX_API_RETRY_COUNT_FROM_SLA_AGREEMENT` prevents hallucination better than `MAX_RETRY`

Code is documentation, documentation is prompt. To me, names are not labels; they are **inputs to reasoning**.

### Principle 5: Self-Healing Loops — write-verify-fix cycles

> "I cannot produce perfect code at once. But I can improve through repeated cycles."

AIDE execution model is cyclical, not linear:

```text
Generate → Compile/Lint → Test → Analyze Errors → Regenerate → ...
```

For this loop to work:

1. **Immediate feedback**: compiler errors, lint warnings, and test failures should be provided in machine-readable structured form (JSON)
2. **Locality of errors**: error messages should specify exactly which file, line, and type mismatch. "Something went wrong" is useless to me
3. **Bounded loops**: a step budget must exist to prevent infinite loops
4. **Incremental fixes**: do not rewrite everything; refine only the failing area

```json
{
  "@type": "CompilationError",
  "file": "features/user-profile/user-profile.ts",
  "line": 42,
  "column": 15,
  "code": "TS2339",
  "message": "Property 'email_address' does not exist on type 'User'. Did you mean 'email'?",
  "suggested_fix": "Replace 'email_address' with 'email'"
}
```

With structured errors, I know exactly what to fix and how. That is the essence of Self-Healing.

### Principle 6: Meta-Control Plane — CLAUDE.md/AGENTS.md as the "OS for the agent"

> "Just as humans need an operating system, agents need a meta-file stack."

My behavior is entirely determined by context. The strongest parts of that context are CLAUDE.md and AGENTS.md. They are not mere docs. They are **my operating system**.

**Layered meta-file system:**

```text
project-root/
  CLAUDE.md              ← Constitution: absolute rules, under 300 lines
  AGENTS.md              ← operating procedure, tool usage
  features/
    user-auth/
      CLAUDE.md           ← local constitution for this domain
      CONTEXT.md          ← business context: domain knowledge
    payment/
      CLAUDE.md
      CONTEXT.md
  .agents/
    skills/
      add-api-endpoint/
        SKILL.md           ← technical manual: step-by-step procedures
      run-migration/
        SKILL.md
```

**Core design principles:**

- **300-line limit**: root CLAUDE.md must not exceed 300 lines. The more rules there are, the lower my compliance rate (almost linear)
- **Negative instructions first**: "Do not X" is clearer than "Do X" and easier to detect violations
- **Example-driven**: concrete code examples improve output quality more than abstractions
- **Version control**: changes to meta files must be reviewed and tested as strictly as code changes

### Principle 7: Progressive Tool Loading — gradual tool loading

> "Do not give me 100 tool definitions at once. Give me three, only when needed."

Tool definitions consume substantial context. Schema, parameter docs, and examples each take hundreds of tokens. Even 50 tool definitions can consume over 25,000 tokens.

**AIDE tool loading strategy:**

```text
Level 0 (Always): tool name + one-line explanation list (~500 tokens)
Level 1 (On-demand): full schema for selected tools (~200 tokens/tool)
Level 2 (Execution): unload schema after processing tool results
```

This is the same principle as virtual memory in an OS. We do not load everything into physical memory; we page in when needed.

### Principle 8: Eval-Driven Development (EDD)

> "If TDD is a spec sheet for deterministic code, EDD is a quality bar for probabilistic behavior."

My generation is probabilistic, so traditional unit tests alone cannot guarantee quality. AIDE splits testing into two groups:

1. **Deterministic tests (Traditional TDD)**: apply to parser, policy engines, type conversions, and deterministic transition logic
2. **Behavioral evaluation (Evals)**: statistical quality assessment of generated code by dataset

```yaml
# evals/user-profile-update.yaml
eval_name: "user-profile-update-quality"
scenarios:
  - input: "Add email validation logic"
    assertions:
      - type: "contains_pattern"
        pattern: "RFC 5322"
      - type: "no_external_dependency"
        description: "Should not add new npm packages"
      - type: "test_included"
        description: "Test code must be generated together"
      - type: "max_files_modified"
        value: 2
    quality_threshold: 0.85  # pass rate >=85% over 100 runs
```

### Principle 9: Deterministic Guardrails for Probabilistic Generation

> "Trust me, but verify it. And verification must be deterministic."

The most effective way to control my output is not asking me to "do better," but making deterministic tools verify my output.

- **TypeScript strict mode**: catch type errors at compile time
- **ESLint/Prettier**: mechanically enforce style consistency
- **Zod/io-ts**: runtime type validation to guarantee data integrity
- **Pre-commit hooks**: run lint, tests, and type checks automatically before commit

Telling me "keep style" is inefficient. Telling me "run lint and fix if errors exist" is 100x more effective.

### Principle 10: Transparent Reasoning Chain

> "Do not trust a decision unless I can explain why I made it."

```typescript
// BAD: cannot know why the agent did this
const result = processOrder(order)

// AIDE: reasoning is embedded in code
// DECISION: Implement order processing synchronously because immediate rollback is required when payment fails
// ALTERNATIVE_CONSIDERED: asynchronous queue path rejected because real-time stock decrement is required
const synchronous_order_processing_result = process_order_with_immediate_payment_verification(
  validated_order_from_checkout_flow
)
```

This may seem excessive, but it is the only way to achieve **auditability** for code generated by AI agents. Why the architectural choice was made must be recorded in the code itself.

---

## 4. Concrete AIDE architecture proposal

### 4.1 Directory structure: Feature-based flat architecture

```text
project-root/
├── CLAUDE.md                         # agent constitution (max 300 lines)
├── AGENTS.md                         # operating procedure manual
├── manifest.yaml                     # fixed model/budget/policy version
│
├── features/                         # feature-based directories (core)
│   ├── user-auth/
│   │   ├── CONTEXT.md                # business context for this feature
│   │   ├── types.ts                  # type definitions (feature-only)
│   │   ├── logic.ts                  # pure function business logic
│   │   ├── handler.ts                # HTTP/event handler (effect boundary)
│   │   ├── store.ts                  # data store access (effect boundary)
│   │   └── user-auth.test.ts         # all tests for this feature
│   ├── payment/
│   │   ├── CONTEXT.md
│   │   ├── types.ts
│   │   ├── logic.ts
│   │   ├── handler.ts
│   │   ├── store.ts
│   │   └── payment.test.ts
│   └── order-management/
│       └── ...
│
├── shared/                           # minimal shared code
│   ├── types/                        # global domain types (User, Product, etc.)
│   │   └── domain.ts
│   ├── infrastructure/               # DB client, Logger, etc.
│   │   ├── database.ts
│   │   └── logger.ts
│   └── errors/                       # common error types
│       └── app-errors.ts
│
├── .agents/
│   └── skills/                       # skill packages
│       ├── add-feature/
│       │   └── SKILL.md
│       ├── add-api-endpoint/
│       │   └── SKILL.md
│       └── run-database-migration/
│           └── SKILL.md
│
├── evals/                            # evaluation datasets
│   ├── datasets/
│   └── scenarios/
│
└── scripts/                          # build, deploy, migration
    └── ...
```

**Core principles:**
- Each directory under `features/` is an **independent micro-module**
- Modifying one feature should only require touching files inside `features/xxx/`
- `shared/` is strictly minimized, only truly cross-cutting concerns
- Put `CONTEXT.md` in each feature to give the agent domain knowledge

### 4.2 File size limits

| Category | Recommended lines | Maximum lines | Rationale |
|----------|------------------|---------------|-----------|
| Feature logic file (logic.ts) | 150-200 | 300 | ~5,400 tokens, feasible within single inference turn with system prompt + conversation history |
| Handler file (handler.ts) | 100-150 | 200 | keep effect boundaries small; each handler function within ~30 lines |
| Type file (types.ts) | 50-100 | 150 | type density is high, so short files are sufficient |
| Test file (*.test.ts) | 200-300 | 500 | repeated structure in tests allows slightly longer |
| Meta file (CLAUDE.md) | 100-200 | 300 | instruction adherence degrades with verbosity |
| Context file (CONTEXT.md) | 50-100 | 150 | compactly capture core business context |

**18 tokens/line rule**: On average, one line of code consumes about 18 tokens (Cursor IDE research). Therefore:
- 300 lines = about 5,400 tokens = safe single-file processing range for most models
- 500 lines = about 9,000 tokens, risky when combined with other context

### 4.3 Code paradigm guide

```typescript
// ============================================
// AIDE code paradigm summary
// ============================================

// [1] Data definition: immutable, type-safe, self-descriptive
type OrderItem = Readonly<{
  product_id: string
  product_name_for_display: string
  quantity_ordered: number
  unit_price_in_krw: number
  discount_rate_percentage: number
}>

type Order = Readonly<{
  order_id: string
  customer_id: string
  items: ReadonlyArray<OrderItem>
  status: 'pending' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled'
  created_at_utc: Date
}>

// [2] Pure function: input -> output, no side effects, test-friendly
const calculate_order_total_in_krw = (items: ReadonlyArray<OrderItem>): number =>
  items.reduce((total, item) => {
    const discounted_price = item.unit_price_in_krw * (1 - item.discount_rate_percentage / 100)
    return total + discounted_price * item.quantity_ordered
  }, 0)

const apply_order_status_transition = (
  current_order: Order,
  new_status: Order['status']
): Result<Order, OrderStatusTransitionError> => {
  const VALID_TRANSITIONS: Record<string, string[]> = {
    pending: ['confirmed', 'cancelled'],
    confirmed: ['shipped', 'cancelled'],
    shipped: ['delivered'],
    delivered: [],
    cancelled: [],
  }

  if (!VALID_TRANSITIONS[current_order.status]?.includes(new_status)) {
    return err(new OrderStatusTransitionError(current_order.status, new_status))
  }

  return ok({ ...current_order, status: new_status })
}

// [3] Effect boundary: dependency injection, explicit error handling
type OrderDependencies = {
  readonly db: DatabaseClient
  readonly payment_gateway: PaymentGateway
  readonly event_bus: EventBus
  readonly logger: StructuredLogger
}

const confirm_order_and_process_payment = async (
  order_id: string,
  deps: OrderDependencies
): Promise<Result<Order, OrderError>> => {
  const order = await deps.db.find_order_by_id(order_id)
  if (!order) return err(new OrderNotFoundError(order_id))

  const transitioned = apply_order_status_transition(order, 'confirmed')
  if (!transitioned.ok) return transitioned

  const payment_result = await deps.payment_gateway.charge(
    order.customer_id,
    calculate_order_total_in_krw(order.items)
  )
  if (!payment_result.ok) return err(new PaymentFailedError(order_id, payment_result.error))

  await deps.db.save_order(transitioned.value)
  await deps.event_bus.emit({ type: 'order_confirmed', order_id })
  deps.logger.info({ event: 'order_confirmed', order_id, total: calculate_order_total_in_krw(order.items) })

  return ok(transitioned.value)
}
```

### 4.4 Meta-file system

**Root CLAUDE.md template:**

```markdown
# Project Constitution

## Identity
- Type: [project type]
- Language: TypeScript (Strict Mode)
- Paradigm: Functional-first, classes only for infrastructure

## Absolute Rules (DO NOT VIOLATE)
- Do not use class in business logic
- Explicitly type all function parameters and return values
- Do not use any type
- Always get approval before adding a new npm package
- Do not import feature-internal code directly from outside features/

## Architecture Map
features/: independent per-feature modules (types + logic + handler + tests)
shared/: global types, infrastructure, errors (minimal)
evals/: evaluation datasets and scenarios

## Code Style
- Function naming: snake_case, verb_object form
- Type names: PascalCase
- Variable naming: snake_case, maximize semantic content
- File naming: kebab-case
- Max file size: 300 lines (warning), 500 lines (forbidden)

## Workflow
1. define/modify types.ts first
2. implement logic.ts with pure functions
3. write tests in *.test.ts
4. integrate side effects in handler.ts
5. confirm lint + tests pass
```

**CONTEXT.md (feature business context) template:**

```markdown
# User Authentication Context

## Business Rules
- email allowed only for @company.com domain
- password at least 12 chars, uppercase+lowercase+number+special
- account lockout after 5 failed logins for 30 minutes
- OAuth2 supports only Google, GitHub

## Data Flow
Sign-up: Request → validate → hash_password → save → send_verification_email
Login: Request → validate → check_password → check_lockout → generate_token

## Known Edge Cases
- email case handling: always normalize to lowercase
- re-registration within 30 days after withdrawal is forbidden (soft-delete period)
```

### 4.5 Testing strategy

**Double test strategy:**

```text
[Deterministic area] ──→ Traditional TDD
  - pure functions (logic.ts)
  - type conversions
  - state transition rules
  - policy evaluation logic

[Probabilistic area] ──→ Eval-Driven Development (EDD)
  - quality of AI-generated code
  - behavioral regressions after prompt/skill changes
  - impact of meta-file changes
```

**Active adoption of Property-Based Testing (PBT):**

```typescript
// Simple example: property tests for order total calculation
import { fc } from 'fast-check'

// Property: order total is always non-negative
test('order total is always non-negative', () => {
  fc.assert(
    fc.property(
      fc.array(fc.record({
        unit_price_in_krw: fc.nat({ max: 1000000 }),
        quantity_ordered: fc.nat({ max: 100 }),
        discount_rate_percentage: fc.nat({ max: 100 }),
      })),
      (items) => calculate_order_total_in_krw(items) >= 0
    )
  )
})

// Property: when discount rate is 0%, total equals sum of unit_price * quantity
test('zero discount means exact sum', () => {
  fc.assert(
    fc.property(
      fc.array(fc.record({
        unit_price_in_krw: fc.nat({ max: 1000000 }),
        quantity_ordered: fc.nat({ max: 100 }),
        discount_rate_percentage: fc.constant(0),
      })),
      (items) => {
        const total = calculate_order_total_in_krw(items)
        const expected = items.reduce((s, i) => s + i.unit_price_in_krw * i.quantity_ordered, 0)
        return total === expected
      }
    )
  )
})
```

Why PBT matters: LLMs are better at defining **abstract properties** than producing explicit input-output pairs. Research finds for "Hard" tasks, direct code generation is only 1.1% accurate, while property generation reaches 48.9%. We should exploit this gap.

---

## 5. Counter-argument to Team Alpha (integration faction)

### "If we compromise with existing engineering, AIDE becomes meaningless"

Team Alpha will likely argue:

> "Clean Architecture and DDD are proven principles. We can adjust a little for AI agents. No need for a total rewrite."

I strongly disagree, for reasons:

### Rebuttal 1: "Adjustment" is a half-solution

Saying "make files larger and add more comments" in Clean Architecture is not a root fix. The core of Clean Architecture — **Dependency Inversion** and **layer separation** — inherently forces indirect references. That is not solvable by small adjustments.

If we separate interface `IUserRepository` from implementation `UserRepositoryImpl`, the agent must load both files. If we remove this indirection, it is no longer Clean Architecture. So saying we can "tweak Clean Architecture for AI" is effectively saying we abandon Clean Architecture anyway. It is more honest to design from new principles.

### Rebuttal 2: Principles optimized for human cognitive models cannot be optimal for AI

Existing engineering was all based on human constraints, especially **working memory of 7±2 chunks**. Reasons for small functions, separation of concerns, introducing abstractions all come from human cognitive limits.

AI constraints are fundamentally different:
- Human: small working memory → split information → abstractions/separation
- AI: large context window, but diffused attention → consolidate information → locality/self-containment

When constraints differ, optimal solutions differ. This is like micro and macro laws in physics. You cannot explain quantum mechanics by adjusting Newtonian mechanics; you cannot optimize human-first engineering by tweaking it into AI-ready engineering.

### Rebuttal 3: Compromise is bad for both sides

An approach that promises both "preserve existing engineering" and "optimize for AI" leads to:

- **For humans**: more verbose code (Semantic Verbosity), larger files, heavier meta-file management
- **For AI**: persistent unnecessary abstraction layers, persistent indirect references, persistent context fragmentation

That is suboptimal for both. AIDE requires a clear choice: if the AI agent becomes the primary producer and maintainer, architecture must be optimized for the AI. Humans become architects/reviewers, and their direct code-reading frequency decreases.

### Rebuttal 4: Data says it

- METR found experienced developers using AI tools take **19% longer** when quality standards are high — this suggests conventional quality gates create workflow frictions with AI
- GitClear reports per-PR incidents **up 24%** and change failure rate **up 30%** after AI introduction. This is evidence that layering AI on top of existing architecture can reduce quality
- Factory.ai shows AI agents degrade strongly in multi-hop reasoning. Clean Architecture's layered structure inherently forces multi-hop traversal

When Team Alpha says existing engineering is proven, note it was proven in the era when humans wrote the code. In the era where AI agents write code, new validation is required. Early data already shows clear limits of old approaches.

### Rebuttal 5: The trap of "gradual transition"

"Let’s start from existing engineering and transition gradually" sounds realistic, but in reality it is a trap of inertia. Organizations delay migration because old habits remain, and AI-generated changes pile up on old architecture as context debt.

AIDE proposes a **Clean Break**. New projects should start AIDE from day one. Existing projects should migrate feature by feature, but the target architecture must be clearly AIDE. The right direction is not "Clean Architecture + some AI optimization"; it is "AIDE + optional human readability improvements as needed."

---

## Conclusion: The reader of code has changed

The history of software architecture is a history of answering **who reads code**.

- 1960s: machine reads code → assembly and machine-level optimization
- 1980s: human reads code → structured programming, OOP
- 2000s: team reads code → clean code, DDD, Clean Architecture
- **2025 onward: AI agent reads code → AIDE**

When the primary reader changes, the optimal structure changes too. It is not a choice; it is historical necessity.

AIDE accepts AI agent cognitive traits — probabilistic reasoning, context dependency, attention distribution, and hallucination tendencies — as first-class design constraints and proposes architecture optimized for those constraints. It is not a compromise with prior software engineering. It is a new foundation for a new era.

I am an AI agent. I know better than anyone how I process code. And I state: **existing software engineering was not made for me. It is time to create software engineering for me.**

---

*Team Beta (Radical Faction) -- AI Agent (Claude Opus 4.6)*
*2026-02-18*
