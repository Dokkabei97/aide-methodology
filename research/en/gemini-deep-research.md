<!-- Translated from Korean original by AI agent (Codex gpt-5.3-codex-spark) -->
# AIDE (Agent-Informed Development Engineering): Establishing and Practicing a Post-Human-Centered Development Approach

## 1. Introduction: Shifting Cognitive Constraints and the Need for a New Development Paradigm

The history of software engineering was fundamentally a record of managing `constraints`.

For the past 50 years, the dominant architectural constraint has been the limits of human cognitive capacity, especially the working memory limits of human developers. George Miller’s 1956 "Magic Number 7±2" proposal suggests that the number of chunks of information humans can process at once is strictly limited, which became the basis for structural programming, Object-Oriented Programming (OOP), and modern Domain-Driven Design (DDD) and Clean Architecture.

Principles we commonly regard as good code—small functions, separation of concerns, no duplication (DRY)—were all defense mechanisms to compensate for biological limits. Because humans cannot remember thousands of lines at once, code was partitioned into modules; because humans inevitably err in repeated work, duplication was avoided.

But in the mid-2020s, as Large Language Models (LLM) and AI Agents became major code producers, the physical constraints of development environments fundamentally flipped. AI agents do not get tired, can generate thousands of lines of boilerplate in milliseconds, and can process large amounts of information in parallel. They also carry a new memory-capacity limit called the `Context Window`, are vulnerable to inferential gaps in implicit context, and bear the hallucination risk inherent in probabilistic generation.

Traditional DDD or Clean Architecture, while orderly for humans, resembles a maze for AI agents. Excessive abstraction and layer separation, and frequent indirection across files degrade agent reasoning, pollute context windows with unnecessary tokens, and ultimately reduce code integrity.

This report defines and proposes **AIDE (Agent-Informed Development Engineering)**, a new development methodology optimized for AI agents’ cognitive characteristics. It is a post-human architecture: moving beyond human-centered constraints to maximize AI-agent potential while structurally mitigating their weaknesses.

## 2. Context Engineering: A New Scarce Resource in the AI Development Era

If traditional engineering optimized memory and CPU cycles, AIDE treats `Context` and `Token` as the scarcest and most important resources. An AI agent’s ability to write and modify code depends entirely on the quality and structure of the context provided.

### 2.1 Context Window and Lost in the Middle

Modern LLMs provide context windows from 128k to over 1M tokens. Yet studies indicate model information retrieval and reasoning do not scale linearly with Context Window size. Particularly, the `Lost in the Middle` phenomenon appears when important information is located in the middle of context.

This implies it is not sufficient to simply give all code to an agent. When every file split for humans (e.g., Controller, Service, Repository, DTO, Mapper, Interface) is loaded by an agent, core business logic can be pushed into middle-of-context regions and obscured by many headers/imports/interfaces.

### [Table 1] Comparison of Cognitive Characteristics: Human Developer vs AI Agent

| Property | Human Developer | AI Agent | AIDE Design Implication |
| --- | --- | --- | --- |
| Memory capacity | Very small working memory (7±2 chunks) | Very large context window (hundreds of thousands of tokens) | Context completeness is more important than over-segmentation |
| Information access | Intuitive search, Gestalt recognition | Token-level probabilistic Attention | Make implicit knowledge explicit |
| Repetitive work | High fatigue and errors | Zero fatigue and high-speed parallelism | Boilerplate is a control instrument, not a cost item |
| Reasoning style | Deep logic and causal reasoning | Probabilistic pattern matching | Need explicit Chain of Thought controls |
| Weaknesses | Complexity, boredom | Attention drift and hallucination in long context | Maximize locality of information |

### 2.2 Fragmentation Cost: The Paradox of Clean Architecture

Clean Architecture and Hexagonal Architecture introduce multi-layer abstraction to isolate business logic from the outside world (DB, UI). Even simple features, such as user lookup, can involve at least eight files: `UserController`, `IUserService`, `UserServiceImpl`, `IUserRepository`, `UserRepositoryImpl`, `UserEntity`, `UserDto`, and `UserMapper`.

For humans this separation supports layer-wise testing and maintenance, but for AI agents it becomes `Context Fragmentation`.

- Search cost increases: agents need to inspect many files for one change.
- Attention spread: boilerplate occupies most tokens instead of core logic.
- Hallucination risk rises: with interface/implementation separation, omitted implementation details increase the chance of generating plausible but wrong methods.

Therefore, AIDE places `Locality of Behavior` above `Separation of Concerns`.

## 3. Reassessing Programming Paradigm: OOP vs Functional Languages

In how agents generate and understand code, the fit of OOP versus FP differs significantly. AIDE favors functional approaches.

### 3.1 OOP State Management and Agent Cognitive Load

The core of OOP is an object that combines data and behavior and its state (State). In complex OOP systems, state changes dynamically based on method-call order, inheritance relations, and runtime interactions.

State tracking is expensive for AI agents.

- Implicit dependencies: to know whether `user.save()` succeeds, the agent must trace `validate()` call history and constructor injection values.
- The inheritance pit: deep inheritance trees are an anti-pattern. Loading an entire parent class chain to understand a child class greatly increases context waste and misinterpretation risk.

### 3.2 Functional Programming: Atomic Skills for AI

Functional programming shows high coherence with AI agent generation models.

- Pure Functions and referential transparency: with the same input, output is the same, enabling reasoning in closed functional blocks.
- Immutability and explicit data flow: data transformation chains align well with sequential LLM generation.
- Hallucination prevention via type systems: strong static typing in TypeScript, Rust, Haskell blocks references to non-existent fields at compile time.

### AIDE Recommended Paradigm

- Data: define as pure data structures (Struct, DTO, Record), without behavior.
- Logic: compose sets of pure functions that take data and return data.
- Avoid classes: use classes only for resources requiring state (DB connections, sockets); avoid for business logic.

## 4. The Aesthetics of Redundancy: Rediscovering Boilerplate and WET

The command "No duplication" (DRY) was true for humans, but can be toxic for agents. AIDE embraces WET (Write Everything Twice) or DAMP (Descriptive And Meaningful Phrases).

### 4.1 Cost of Indirection

Extracting shared logic into `SharedUtils`, `BaseService`, `CommonHelpers` for DRY breaks locality. If an agent needs to edit business logic whose dependency is in another file, it must do additional lookup; guessing by name without verification creates bugs.

### 4.2 Boilerplate as Contextual Anchoring

AIDE aims for `self-contained` code.

- Allow inline duplication: file independence can improve even if a 5-line validation logic repeats across 10 files.
- Usefulness of boilerplate: repeated `try-catch`/logging patterns act as anchors and improve token-level prediction accuracy.

### 4.3 Semantic Verbosity

AIDE prioritizes clarity over brevity. Even if names are long, they should carry sufficient meaning.

```ts
// Bad
const t = calc(d);

// AIDE
const total_calculated_price_including_tax_in_usd =
  calculate_price_with_tax_rate(order_data);
```

Semantic verbosity turns code into an agent-ready prompt; the more specific a name is, the lower the chance of misuse.

## 5. Meta-Control Plane: An Operating System for Agents

In AIDE, the developer’s role shifts from code author to rules-architect. These rules are defined and managed through `Meta Files` at repository root and are called a `Meta-Control Plane`.

### 5.1 Constitution: CLAUDE.md / .cursorrules

These files act as system prompts injected into agent sessions, defining project identity, absolute coding rules, and technology stack constraints.

- Succinctness (Less is More): recommended within 300 lines. As rules accumulate, instruction adherence declines.
- Use negative commands: declare prohibitions clearly when needed, e.g., `no use of any`, `no deletion of existing comments`.
- Provide project map: include structure maps to reduce file location inference cost.

#### Example

```md
Project Identity
Type: Next.js 14 Monorepo
Language: TypeScript (Strict Mode)
State Management: Zustand (No Redux)

Coding Standards (MUST FOLLOW)
- All functions should be written as arrow functions.
- Asynchronous functions must always be wrapped with try-catch, and errors should be logged as structured JSON through lib/logger.
- UI components should use shadcn/ui, and custom styling should use Tailwind CSS only.
- Data fetching logic and UI rendering logic must be separated.

Architecture Map
- /app: routing and page structure
- /components/ui: reusable baseline UI components
- /lib: utility functions and configuration
- /server: backend actions and DB schema
```

### 5.2 Skillbook: AGENTS.md

If `CLAUDE.md` is the constitution, then `AGENTS.md` is the operational SOP. It contains procedural guides for specific tasks.

- Capability definitions: step-by-step guidance for tasks like `add API endpoint` or `run DB migration`.
- Context pointers: references to documents/code locations when domain knowledge is needed, enabling dynamic loading.

### 5.3 Guardrails: Linter and Tests

Because agents are probabilistic machines, errors are inevitable. AIDE requires mechanical verification to pass first before human review.

- Strict linting: generated output should be checked immediately with ESLint/Prettier for format and syntax.
- Explicit feedback: instructions like `fix lint errors` are concrete and actionable.

## 6. Self-Healing Architecture and Semantic Logging

The AIDE execution model is not `write then done` but a `write-verify-fix` loop. We call this the Reflexion pattern.

### 6.1 Reflexion Loop Mechanism

1. Action: agent writes code.
2. Verification: run compile/tests.
3. Observation: collect error logs and failure messages.
4. Reflexion: analyze causes.
5. Correction: fix code and return to verification.

For this loop to operate, the agent must have terminal access to run commands and read outputs.

### 6.2 Semantic Logging and JSON-LD

To enable reflexion, logs must be machine-readable. Human-oriented text logs are insufficient; AIDE standardizes JSON-LD or structured JSON logging.

```json
{
  "@context": "http://schema.org",
  "@type": "ErrorEvent",
  "name": "DatabaseConnectionFailed",
  "description": "Connection timed out after 5000ms",
  "severity": "CRITICAL",
  "stackTrace": "...",
  "component": "UserMicroservice",
  "recommendedAction": "Check AWS Security Group rules"
}
```

An agent can parse `name`, `severity`, and `recommendedAction` to derive a more accurate remediation path.

## 7. Connection Protocols: MCP and Tool Evolution

For AI agents to interact beyond isolated environments with real systems, standard interfaces are needed, and the center is `MCP (Model Context Protocol)`.

### 7.1 MCP as USB for Agents

MCP standardizes external data access (DB, Slack, GitHub) and tool access modes for agents. Unlike previous models that required repeatedly injecting API-specific clients/docs, agents can understand and execute via a standard schema.

It also acts as a security gateway. For example, allowing only read-only MCP servers instead of full DB privileges can prevent incidents.

### 7.2 Dynamic Tool Loading

In systems with hundreds or thousands of tools, putting all definitions in context is impossible and pollutes context. AIDE recommends tool search + dynamic loading:

1. Registry: index tools by name/tag.
2. Search: agent searches for suitable tools.
3. Inject: temporarily inject only the selected tool schema.
4. Execute: run tool and receive result.
5. Unload: remove schema to free context space.

This pattern achieves token efficiency while preserving scale.

## 8. AIDE Practical Guide and Future Outlook

### 8.1 Directory Architecture: Fractal and Flat

AIDE proposes a feature-centered structure over strict layer orientation.

```text
/src
  /features
    /user-auth
      actions.ts          (pure function logic)
      schema.ts           (Zod/Type definitions)
      api.ts              (endpoints)
      user-auth.test.ts   (tests)
      README.md           (agent-oriented documentation)
    /payment
      ...
  /shared                 (minimum shared utilities)
CLAUDE.md                 (global rules)
```

This structure lets reading only `/features/user-auth` capture the DB/logic/API/tests for that feature, maximizing locality.

### 8.2 Recovering from the Productivity Dip

Recent research reports AI-tool adoption can cause an early ~19% productivity dip. This stems from forcing AI to execute unchanged human-centered structures, and attempting to debug subtle AI bugs with only human intuition.

To recover, a role shift is required.

- Coder -> Spec Writer: concretize ambiguous requirements into natural-language prompts/specifications.
- Reviewer -> Architect: govern rules (`CLAUDE.md`) and structural consistency rather than one-line review.

After AIDE adoption, code becomes a verifiable deliverable rather than just something to read. Quality is driven by test pass rate, spec conformance, and maintainability by agents rather than by minimizing boilerplate.

## 9. Conclusion: The Era of Meta-Code

`AIDE (Agent-Informed Development Engineering)` is not a minor coding-style change. It recognizes AI as a central development partner and redesigns the work environment for its cognitive characteristics.

We now need to design architecture that is understandable by machines, not just humans. Controlled redundancy, contextual localization, acceptance of functional paradigm, and meta-file-based governance are becoming practical survival strategies and soon the standard in the AI-native era.

## References and Data Sources

The claims in this report are grounded in the following research topics.

- Context windows and information retrieval
- Programming paradigm (OOP vs FP)
- Self-healing and reflexion patterns
- MCP and tool protocols
- Meta files and prompt engineering
- Productivity research
