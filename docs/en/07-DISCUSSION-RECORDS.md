# AIDE (Agent-Informed Development Engineering) -- A Software Development Methodology for the Agentic Era v1.0

**Author**: CTO (20+ years of architecture experience, 3 years of hands-on AI agent experience)
**Based on**: GPT/Claude/Gemini triple deep research + Team Alpha (Integrationists) 2 reports + Team Beta (Radicals) 1 report
**Date**: 2026-02-18

---

## Part 7: Discussion Records -- Scientific Debate and Consensus Process Between Teams

### Issue 1: OOP vs FP

#### Team Alpha (Integrationists) Position

"Functional Core + OOP Shell + DDD Boundaries. DDD's Aggregate, Entity, and Value Object are still valid for structuring domain knowledge. However, implementing them as immutable and transforming through functions (pure functions) rather than methods is more agent-friendly. Gemini's 'do not use classes for business logic' is too extreme."

Key arguments:
1. DDD's domain modeling is awkward to express with pure functions alone
2. Criticism of deep inheritance trees is already an anti-pattern in modern OOP -- OOP is not synonymous with inheritance
3. Clean Architecture's dependency inversion is the most important SOLID principle in the AI era

#### Team Beta (Radicals) Position

"FP-only. Classes are restricted to infrastructure resource management only. I (the AI agent) am fundamentally stateless. Pure functions are the code form closest to my nature. Class state management is a high-cost operation for agents. Code with no hidden state and no inheritance chains gives me perfect readability."

Key arguments:
1. Separating interface `IUserRepository` from implementation forces loading two files -- eliminating this indirection means it's no longer Clean Architecture
2. Factory.ai research: AI agents experience dramatic performance degradation in multi-hop reasoning
3. Implicit state tracking is fuel for hallucination

#### CTO's Final Judgment

**The practical difference is smaller than both teams think.** Both teams agree that "business logic should be pure functions, data should be immutable." The actual difference is merely whether DDD concepts are expressed as classes or as type+function compositions.

**AIDE's Conclusion: Preserve DDD's modeling concepts; shift implementation to types+functions.**

```typescript
// Both what Alpha wants (DDD concept preservation) and
// what Beta wants (class exclusion) are satisfied

// Aggregate: Immutable type + state transition pure function
type Order = Readonly<{ id: string; status: OrderStatus; items: ReadonlyArray<OrderItem> }>
const transition_order_status = (order: Order, newStatus: OrderStatus): Result<Order, Error> => { /* ... */ }

// Value Object: Type literal
type Money = Readonly<{ amount: number; currency: 'KRW' | 'USD' }>

// Repository: Feature-internal store.ts (side-effect boundary)
// Replaceability secured through dependency injection, without separating interface and implementation files
type UserStore = {
  readonly find_by_id: (id: string) => Promise<User | null>
  readonly save: (user: User) => Promise<void>
}
```

This approach satisfies both Alpha's DDD values (domain boundaries, Ubiquitous Language, Aggregate concepts) and Beta's FP values (pure functions, immutable data, no state tracking needed).

---

### Issue 2: DRY Principle

#### Team Alpha's Position

"Knowledge DRY + Code AHA. Duplication is consciously allowed, but visible management is a prerequisite. '5-line duplication in 10 places is OK' is extreme. Drift of duplicate code is a real risk, and prevention is better than detection."

#### Team Beta's Position

"Aggressively WET/DAMP. Self-containment of each file is the top priority. If you import `validateEmail` from another file, the agent has to guess the actual implementation when it's not in context. This is a breeding ground for subtle bugs."

#### CTO's Final Judgment

**Team Alpha's "Knowledge DRY + Code AHA" is adopted.** Key rationale:

1. **Self-contradiction of unlimited duplication**: This is a problem that Beta effectively acknowledges. Allow duplication -> AI generates more code -> Context window exceeded -> DRY is needed after all. This cycle is inescapable.
2. **However, Beta's locality argument is valid**: Situations where agents must guess the implementation of a utility function from another file are genuinely risky. Therefore, **utility-level code duplication is allowed up to 2-3 instances**.
3. **Duplication of business rules is absolutely prohibited**: If the discount rate calculation formula exists in 3 places, inconsistencies arise during policy changes. This is equally dangerous for both agents and humans.

---

### Issue 3: Existing Architecture (Clean Architecture)

#### Team Alpha's Position

"Restructure Clean Architecture into Feature-based organization. Maintain the Dependency Rule and reduce the physical layers. Feature-based structure is compatible with Clean Architecture."

#### Team Beta's Position

"Discard Clean Architecture. Separating interface from implementation inherently forces indirection. 'Adjusting Clean Architecture for AI' ultimately amounts to abandoning Clean Architecture. It's more honest to start with new principles from the beginning."

#### CTO's Final Judgment

**Adopting Feature-based structure makes them practically similar.** The key is whether the Dependency Rule is preserved.

1. **Agree on abolishing physical layers**: The 4+ layer separation of Controller -> Service -> Repository -> Entity is deprecated. Transition to Feature-based Vertical Slices.
2. **Logical dependency rules are preserved**: Even within a Feature, the dependency direction of `types -> logic -> handler -> store` is maintained. Pure logic (logic.ts) does not depend on infrastructure (store.ts).
3. **Beta's core argument is accepted**: Physical separation of interface files and implementation files is not done. Instead, replaceability is secured through type-level dependency injection (`type UserStore = { ... }`).

In conclusion, **the name is not Clean Architecture, but the core values (dependency direction, pure logic isolation) are preserved**. The answer to Beta's question "Can you call this Clean Architecture?" is "No. This is AIDE." But the answer to "Does it inherit the core insights of Clean Architecture?" is "Yes."

---

### Issue 4: Transition Strategy

#### Team Alpha's Position

"Progressive transition. We cannot ignore hundreds of thousands of lines of code in existing projects and the existing knowledge of millions of developers. An extension/reinterpretation approach lowers the adoption barrier."

#### Team Beta's Position

"Clean Break. 'Progressive transition' is the trap of inertia. Organizations familiar with existing approaches will delay the transition, and during that time technical debt accumulates on top of the existing architecture. New projects should use AIDE from the start."

#### CTO's Final Judgment

**Consensus is achievable by distinguishing between new and existing projects.**

- **New projects**: As Beta advocates, **Clean Start**. Begin with AIDE principles from the start.
- **Existing projects**: As Alpha advocates, **progressive migration**. Transition to AIDE on a Feature-by-Feature basis. Apply AIDE only to new and modified code.

Beta's warning about the "trap of inertia" is valid. Therefore, even for existing projects, **migration roadmaps and milestones must be clearly defined**. "We'll transition someday" is the same as "We won't transition."

---

### Issue 5: Testing

#### Team Alpha's Position

"TDG (Test-Driven Generation) + PBT + EDD extension. Don't discard TDD; extend it for the AI era."

#### Team Beta's Position

"Dual framework -- Traditional TDD for deterministic code, EDD for probabilistic behavior. Actively adopt PBT."

#### CTO's Final Judgment

**These are practically identical proposals.** The test strategies from both teams are integrated into the following framework:

1. **Deterministic code** (parsers, policies, state transitions, business logic): **TDD + PBT**
2. **Model behavior** (code generation quality, prompt change impact): **EDD (Eval Suites)**
3. **System integration** (cross-Feature coordination, data flow, external service integration): **Integration Tests**
4. **Security** (security vulnerabilities in AI-generated code, auth/authz verification): **Security Scenario Tests**

Both teams agreed on aggressive adoption of PBT, supported by the data: "Hard tasks: direct generation 1.1% vs. property-based verification 48.9%." To prevent confirmation bias, using **different models or different sessions** for test writing and code writing is recommended.

---

### Additional Issue: Fundamental Attitude Toward Existing Methodologies

#### Team Alpha's Core Position

"The core values of existing principles are universal. Single responsibility, separation of concerns, dependency inversion, testability -- these exist not only because of human cognitive limitations but for managing system complexity itself. 'Don't throw the baby out with the bathwater.'"

**Chesterton's Fence argument**: Existing principles are the result of learning from real project failures. Before tearing down the fence, understand why it was built.

#### Team Beta's Core Position

"When the primary reader of code changes, the optimal code structure changes too. 1960s: machines -> 1980s: humans -> 2000s: teams -> 2025+: AI agents. When the constraints are different, the optimal solution is different. You cannot 'adjust' Newtonian mechanics to explain quantum mechanics."

**METR data argument**: When experienced developers maintain existing quality standards while working with AI, they are actually 19% slower. This is direct evidence that existing methodology quality standards create friction with AI workflows.

#### CTO's Final Judgment

Both teams are partially right.

**Where Alpha is right**: The **fundamental problems** of complexity management, changeability, and quality assurance have not disappeared. The data showing 45% security flaws in AI-generated code proves this. Completely discarding existing principles would collapse these defenses.

**Where Beta is right**: When constraints fundamentally change, **implementation approaches** must also fundamentally change. 8-file distribution, deep inheritance trees, and excessive indirection are structural problems that cannot be resolved with "minor adjustments." METR's 19% productivity decline data demonstrates the friction of existing approaches.

**Conclusion**: AIDE **preserves the core values of existing methodologies while fundamentally realigning implementation approaches and priorities**. We use the term "evolution," but this is not "minor modification" -- it is evolution into "the same species but a significantly different form." Just as the evolution from fish to amphibians was an adaptation to the environmental change from water to land, AIDE is an adaptation to the environmental change from human-centric to agent-centric development.

---

*This document is AIDE v1.0. Since AI agent capabilities are evolving rapidly, it is recommended that this methodology be revised on a semi-annual basis. As context windows grow larger and model reasoning capabilities improve, some specific guidelines (file size limits, indirection depth, etc.) may be adjusted. However, the core principles -- context budget, locality, functional core, deterministic guardrails, observability, structural security -- will remain as enduring values of the agentic era.*


← Previous: [06-ADOPTION-GUIDE](./06-ADOPTION-GUIDE.md) | Next: [INDEX](./INDEX.md) →
