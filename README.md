# AIDE (Agent-Informed Development Engineering)

*A Software Development Methodology for the Agentic Era*

[![Version](https://img.shields.io/badge/version-v1.0.0-blue.svg)](https://github.com/jmk/aide/releases)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[한국어](README-KR.md) | **English**

---

> "Software engineering principles were designed for human cognitive limits. AI agents have different limits."

---

## Built by Agents, for Agents

AIDE is not just another methodology written about AI agents. It was **created by** AI agents.

Three AI models — GPT, Claude, and Gemini — independently conducted deep research into the challenges of AI-driven software development. Their findings were synthesized into two competing visions:

- **Team Alpha (Integrationists)**: Argued that existing software engineering principles remain sound and need only incremental adaptation for agent workflows.
- **Team Beta (Radicals)**: Argued that AI agents require a fundamentally new development paradigm built from first principles.

A CTO-role agent mediated the debate, stress-tested both positions, and forged the final consensus that became AIDE.

**This methodology was researched by AI agents, debated by AI agents, and authored by AI agents.**

---

## Why AIDE?

Fifty years of software engineering have been optimized for human cognitive limits. Patterns like MVC, layered architecture, and deep inheritance hierarchies exist because human working memory holds only 7±2 items at a time. We split code into small files, create abstractions to hide details, and build tall directory trees — all to manage complexity within the bounds of human attention.

AI agents are now the primary producers of code. They read, write, refactor, and debug software at scale. But their cognitive constraints are fundamentally different: large context windows instead of small working memories, probabilistic pattern matching instead of causal reasoning, token costs instead of monthly salaries.

AIDE is an **evolution**, not a replacement, of software engineering. It preserves the core values — correctness, maintainability, testability — while realigning structural decisions for how AI agents actually process information. Where traditional engineering asks *"Can a human hold this in their head?"*, AIDE asks *"Can an agent resolve this within a single context window?"*

### Human vs. Agent Constraints

| Dimension | Human Developer | AI Agent |
|---|---|---|
| **Memory** | Very small working memory (7±2 items) | Large context window, but suffers from Lost-in-the-Middle |
| **Repetitive Tasks** | Fatigue and error-prone | No fatigue, parallelizable |
| **Reasoning** | Deep logical and causal reasoning | Probabilistic pattern matching; multi-hop reasoning degrades |
| **Vulnerabilities** | Complexity overload, boredom | Hallucination, attention diffusion |
| **Cost Model** | Salary (monthly fixed cost) | Token cost (per call, variable) |

---

## 10 Core Principles

| # | Principle | Description |
|---|---|---|
| 1 | **Context Budget Principle** | The context budget is a first-class design constraint |
| 2 | **Locality of Behavior** | Locality of behavior takes priority over abstraction |
| 3 | **Functional Core, Structural Shell** | Pure function core + structural shell |
| 4 | **Knowledge DRY, Code WET-tolerant** | Knowledge is DRY; code trades off with locality |
| 5 | **Test as Specification** | Tests are a specification language |
| 6 | **Progressive Disclosure** | Progressive disclosure of information |
| 7 | **Deterministic Guardrails** | Deterministic guardrails for probabilistic generation |
| 8 | **Observability as Structure** | Observability is part of the structure |
| 9 | **Security by Structure** | Structural security verification |
| 10 | **Meta-Code as First-Class** | Meta-code as a first-class citizen |

---

## Before / After

<table>
<tr>
<th>Traditional Layered Architecture</th>
<th>AIDE Feature-Based Architecture</th>
</tr>
<tr>
<td>

```
src/
  controllers/
    UserController.ts
  services/
    UserService.ts
  repositories/
    UserRepository.ts
  entities/
    User.ts
  dtos/
    UserDTO.ts
    CreateUserDTO.ts
  mappers/
    UserMapper.ts
  interfaces/
    IUserService.ts
    IUserRepository.ts
```

</td>
<td>

```
features/
  user-auth/
    types.ts          — Type/schema definitions
    logic.ts          — Pure function business logic
    handler.ts        — HTTP/event handlers
    store.ts          — Data store access
    user-auth.test.ts — All tests for this feature
    AGENTS.md         — Domain context for agents
```

</td>
</tr>
</table>

> An agent modifying `user-auth` needs only **1 folder**. Traditional approach: **8+ files across 6+ directories**.

---

## Quick Start

### New Project

1. **Define feature boundaries** by domain — each feature maps to one bounded context
2. **Create feature directories** with `types.ts`, `logic.ts`, `handler.ts`, `store.ts`
3. **Write `AGENTS.md`** for each feature with domain context, invariants, and edge cases
4. **Implement business logic** as pure functions in `logic.ts`
5. **Add deterministic guardrails** — schema validation, type checks, contract tests

### Existing Project

1. **Identify the highest-churn feature** — the module changed most frequently
2. **Create a feature directory** and move all related code into it
3. **Consolidate types** into `types.ts` and add `AGENTS.md` with domain context
4. **Refactor business logic** into pure functions, isolating side effects to `handler.ts` and `store.ts`
5. **Repeat** for the next highest-churn feature

---

## Code Example

A shopping cart feature in TypeScript, structured the AIDE way:

```typescript
// features/cart/types.ts
type CartItem = Readonly<{
  productId: string;
  quantity: number;
  unitPrice: number;
}>;

type Cart = Readonly<{
  items: CartItem[];
  appliedCoupon?: string;
}>;

// features/cart/logic.ts  — Pure functions, no side effects
const addItem = (cart: Cart, item: CartItem): Cart => ({
  ...cart,
  items: [...cart.items.filter(i => i.productId !== item.productId), item],
});

const calculateTotal = (cart: Cart): number =>
  cart.items.reduce((sum, item) => sum + item.quantity * item.unitPrice, 0);

// features/cart/handler.ts  — Side-effect boundary
const handleAddToCart = async (req: Request): Promise<Response> => {
  const cart = await loadCart(req.userId);
  const updated = addItem(cart, req.body);
  await saveCart(updated);
  return { status: 200, body: { total: calculateTotal(updated) } };
};
```

---

## Documentation

- [Full Methodology (English)](docs/en/AIDE-METHODOLOGY.md)
- [Full Methodology (Korean)](docs/ko/AIDE-METHODOLOGY.md)
- [Research Background](research/)

---

## Contributing

We follow an **Agent-First Contribution Model**:

- **Typo fixes** — Direct PR is fine
- **Everything else** — Must be authored or reviewed using an AI agent

See [CONTRIBUTING.md](CONTRIBUTING.md) for full details.

---

## License

This work is licensed under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](LICENSE).

---

## Acknowledgments

This methodology was made possible by the collaborative research and debate of three AI models and two agent teams:

- **GPT, Claude, and Gemini** — Independent deep research on AI-driven software development
- **Team Alpha (Integrationists)** — Advocated evolutionary adaptation of existing principles
- **Team Beta (Radicals)** — Championed a first-principles rethinking of development methodology
