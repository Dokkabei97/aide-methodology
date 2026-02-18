# AIDE (Agent-Informed Development Engineering) -- A Software Development Methodology for the Agentic Era v1.0

**Author**: CTO (20+ years of architecture experience, 3 years of hands-on AI agent experience)
**Based on**: GPT/Claude/Gemini triple deep research + Team Alpha (Integrationists) 2 reports + Team Beta (Radicals) 1 report
**Date**: 2026-02-18

---

## Part 3: Relationship with Existing Methodologies

### Preserve/Modify/Deprecate Classification Table

Based on Team Alpha senior developer's analysis, with CTO's final judgment added:

#### Architecture Patterns

| Principle | Core Value | Verdict | Reinterpretation in AIDE |
|-----------|-----------|---------|------------------------|
| **DDD - Bounded Context** | Managing complexity through domain boundaries | **Preserve (Strengthen)** | Each Feature directory corresponds to a Bounded Context. AGENTS.md includes a domain glossary. |
| **DDD - Ubiquitous Language** | Common language for the domain | **Preserve (Strengthen)** | Explicit documentation in AGENTS.md is mandatory. Agents have no implicit knowledge. |
| **DDD - Domain Events** | Loose coupling between domains | **Preserve (Strengthen)** | Foundation for cross-Feature communication and observability. |
| **DDD - Aggregate** | Transactional consistency boundary | **Modify** | Reimplemented with immutable data structures + event sourcing. |
| **Clean Architecture** | Dependency Rule | **Modify** | Dependency rule maintained, physical layers reduced to 2-3, transitioned to Feature-based structure. |
| **Hexagonal Architecture** | Ports & Adapters | **Modify** | Adapter value increases for external service/DB replacement. Minimize Port/Adapter file count. |
| **Layered Architecture** | Horizontal layer separation | **Modify (Reduce)** | Transitioned to Vertical Slices. Keep only the logical layer concept; remove physical layer folders. |

#### SOLID Principle Reprioritization

SOLID priorities in the AI agent era: **DIP > SRP > ISP > LSP > OCP**

| Principle | Traditional Rank | AIDE Rank | Reason |
|-----------|-----------------|----------|--------|
| **DIP (Dependency Inversion)** | 5th (last) | **1st** | LLMs/tools/infrastructure change on a months-long cycle. Depending on abstractions is necessary for survival. Inter-Feature interfaces are direct implementations of DIP. |
| **SRP (Single Responsibility)** | 1st | **2nd** | Limits the blast radius of AI modifications. Unit expands from file-level to Feature/Module-level. |
| **ISP (Interface Segregation)** | 4th | **3rd** | AI works better with focused, minimal interfaces. Preventing unnecessary interface exposure also contributes to security. |
| **LSP (Liskov Substitution)** | 3rd | **4th** | Foundation of type safety. Strong type systems serve as guardrails against hallucination. |
| **OCP (Open/Closed)** | 2nd | **5th** | Since AI can freely modify code, the premise of "closed to modification" is weakened. Still valid for Plugin/Strategy patterns. |

#### GoF Pattern Classification

| Classification | Patterns | Reason |
|---------------|----------|--------|
| **AI-Friendly (Actively Use)** | Strategy, Observer, Factory Method, Adapter, Command, Repository | Single responsibility, clear interfaces, easy replacement |
| **Situational (Use with Caution)** | Singleton, Template Method, State, Builder | Requires sufficient documentation in agent context when used |
| **AI-Unfriendly (Avoid)** | Visitor, deep Abstract Factory hierarchies, long Decorator chains, complex Mediator | Complex dispatch, implicit relationships across multiple files, forces multi-hop reasoning |

#### DDD Reinterpreted

DDD becomes **more important** in the AIDE era. However, the implementation approach changes:

| DDD Concept | Traditional Implementation | AIDE Implementation |
|-------------|--------------------------|-------------------|
| **Bounded Context** | Package/module boundaries | Feature directory + Tier 2 AGENTS.md |
| **Aggregate Root** | Class (mutable state) | Immutable type + pure functions (state transitions) |
| **Entity** | Class + ID | Immutable Record + ID field |
| **Value Object** | Immutable class | Immutable type literal |
| **Domain Event** | Event class | Type literal + Observability integration |
| **Ubiquitous Language** | Verbal + code | Explicit glossary included in AGENTS.md |
| **Repository** | Interface + implementation | Feature-internal store.ts (side-effect boundary) |

---



← Previous: [02-ARCHITECTURE-PATTERNS](./02-ARCHITECTURE-PATTERNS.md) | Next: [04-PRACTICAL-GUIDE](./04-PRACTICAL-GUIDE.md) →
