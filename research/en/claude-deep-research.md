# AIDE: Agent-Informed Development Engineering — a methodology for agent-driven development

**AI agents are rewriting how software gets built, but the architectural principles guiding them remain stuck in the human era.** The AIDE (Agent-Informed Development Engineering) methodology synthesizes emerging practices from practitioners, academic research, and industry frameworks into a coherent set of principles optimized for AI agent-driven software development. The core insight is paradoxical: good engineering discipline is *more* important with AI agents, not less — but the specific principles need significant reinterpretation. This report draws from AWS's AI-DLC framework, Anthropic's context engineering research, Thoughtworks' Technology Radar, academic papers, and hundreds of practitioner accounts to propose a comprehensive methodology for the post-vibe-coding era.

---

## The landscape has shifted from vibe coding to agentic engineering

The terminology tells the story. Andrej Karpathy coined **"vibe coding"** in February 2025 — "fully give in to the vibes, embrace exponentials, and forget that the code even exists." Exactly one year later, he declared it passé and proposed **"agentic engineering,"** emphasizing "there is an art & science and expertise to it." Addy Osmani formalized this into a spectrum: vibe coding (YOLO) → AI-assisted engineering (middle) → agentic engineering (disciplined). The most important finding across all sources: **AI-assisted development actually rewards good engineering practices more than traditional coding does.**

Several formal methodologies have emerged. AWS's **AI-DLC** (AI-Driven Development Lifecycle) is the most formalized, replacing sprints with **"bolts"** (hours/days, not weeks) and epics with **"units of work."** The academic **V-Bounce Model** adapts the V-model for AI, shifting humans from implementers to validators. OpenAI's **AI-Native Engineering Team Guide** defines what to delegate, review, and own across each SDLC phase. The open-source **Agentic Coding Principles** community codified 6 principles and 28 practices. A consistent theme emerges across all: **humans shift from writing code to orchestrating agents and validating output**.

Tweag's controlled experiment found AI-assisted teams delivered projects **45% faster** with high code quality when using spec-first approaches and strong review discipline. The METR study, however, found experienced developers actually took **19% longer** when quality standards were high — the productivity gains vanish if rigor is maintained. This tension defines the methodology challenge: speed without sacrificing quality.

---

## Principle 1: Design for the context window, not the human eye

The most concrete architectural constraint in AIDE is the **context window**. Even million-token windows suffer from "context rot" — Chroma's research measured 18 LLMs and found performance grows "increasingly unreliable as input length grows." The "lost in the middle" effect means LLMs prioritize information at the beginning and end of context, overlooking content in the center. Bigger context windows do not solve this.

**File sizing** has converged on a practical consensus: **target 200–300 lines per file, with 500 as an absolute maximum**. The "Cursor 500 Rule" documents that Cursor IDE breaks files into chunks and performance degrades with large files. Ofer Shapira's battle-tested Cursor rules recommend 300 lines. AB Vijay Kumar independently arrives at the same threshold for vibe coding. The math supports this: at roughly **18 tokens per line of code**, a 300-line file consumes ~5,400 tokens — fitting comfortably within any model's working context alongside system prompts, conversation history, and response space.

Functions should be **small, single-purpose, and self-explanatory**. Multiple cursor rules and AGENTS.md files mandate "no multi-mode behavior, no flag parameters that switch logic." The key design principle is **independent comprehensibility**: each file should carry enough context through naming, types, and structure that an agent can understand it without loading many other files. Thoughtworks' Technology Radar formally introduced **"AI-friendly code design"** as an Assess technique, noting that "expressive naming provides domain context; modularity keeps AI's context manageable." Context engineering — curating what the model sees — is the critical new discipline, not prompt engineering alone.

---

## Principle 2: Conscious duplication over premature abstraction

Traditional development's DRY (Don't Repeat Yourself) principle needs the most radical reinterpretation. The emerging consensus is captured by Kirill Tolmachev's formulation: **"The principle shifts from 'never duplicate' to 'duplicate consciously, with visibility.'"** AI tooling can help enforce DRY at the knowledge level while tolerating duplication at the code level — which is arguably what the principle always meant.

The argument against rigid DRY for AI agents is structural. Factory.ai's research shows AI agents struggle with **multi-hop reasoning** — tracing through chains of abstractions to understand behavior. Self-contained modules with some repetition are dramatically easier for agents to reason about than highly abstracted, DRY code where understanding one function requires loading five others. Code **locality** — keeping related code together even at the cost of repetition — directly benefits AI comprehension.

However, Tolmachev identifies a self-defeating argument: tolerating duplication because AI can track it leads to more generated code, which eventually exceeds context windows, making DRY necessary again. The resolution is **AHA (Avoid Hasty Abstractions)**, which is more important than ever when AI generates code rapidly and cheaply. Kent C. Dodds' principle — "don't abstract until you've seen the pattern at least twice" — and Sandi Metz's "prefer duplication over the wrong abstraction" become foundational.

The AIDE position: **enforce DRY at the business-knowledge level** (a business rule should live in one place), **tolerate duplication at the code-utility level** (small helpers can be repeated if it improves locality), and **use AI agents themselves to detect drift** between duplicated code during reviews. Faros AI warns that "agents don't pause to ask whether a function already exists; they simply produce output" — making agents naturally prone to violating DRY. This must be countered with explicit instruction files and review processes.

---

## Principle 3: Functional core, architectural shell

The paradigm question — OOP versus functional programming — resolves into a hybrid. **Functional programming has a structural advantage for AI code generation**: LLMs are inherently stateless, processing each input independently, and FP's pure functions align naturally with this constraint. Small, self-contained functions with no side effects are easier to generate within limited context windows, and immutability prevents unexpected bugs when AI generates code without full situational awareness.

OOP retains value for **structural organization**. Clean Architecture practitioners report that clear boundaries — classes, interfaces, modules — give AI agents navigational structure. The recommended pattern is **"functional core, imperative shell"**: pure FP for business logic (where AI excels at generation), OOP and architectural patterns for structural organization (where AI benefits from explicit boundaries). No direct FP-versus-OOP benchmarks for AI code generation exist yet — current benchmarks like HumanEval and SWE-bench are mostly function-level Python tasks, inherently favoring FP-style code.

For traditional design principles, the research reveals a clear priority ordering:

- **DDD (Domain-Driven Design)** becomes MORE important. Bounded contexts map directly to agent boundaries — each AI agent should be an expert in its specific domain. Ubiquitous language must be explicitly documented in instruction files. Rod Johnson's DICE framework (Domain-Integrated Context Engineering) bridges DDD and LLM context. Without DDD, enterprise agentic ecosystems become "Big Ball of Mud" systems.

- **Clean Architecture** is exceptionally well-suited. The dependency rule (inner layers don't depend on outer layers) gives agents clear, predictable structure. Multiple practitioners in 2025–2026 report it works "remarkably well" with AI coding agents. Framework independence is critical for swapping LLMs and tools.

- **Hexagonal Architecture** is strongly recommended. Ports-and-adapters isolate business logic from infrastructure, enabling the LLM swapping that the rapidly changing AI landscape demands. Domain logic stays in code; AI agents live in the application layer; adapters handle LLM APIs, databases, and vector stores.

- **SOLID principles** need reordering by importance for AI: **DIP > SRP > ISP > LSP > OCP**. Dependency Inversion is foundational (agents must depend on abstractions, not concrete implementations). Single Responsibility limits the blast radius of AI modifications. Interface Segregation matters more than ever — AI works better with focused, minimal interfaces. Open/Closed needs reinterpretation since AI can freely modify code, but remains valuable for plugin architectures.

- **GoF Design Patterns** split into AI-friendly and AI-hostile: **Strategy, Observer, Factory, Adapter, and Command** patterns work well; **Visitor** (complex double-dispatch), deep **Abstract Factory** hierarchies, and long **Decorator chains** cause problems.

---

## Principle 4: Tests are the specification language for AI

TDD is MORE important with AI agents, not less. It becomes what David Luhr calls **"prompt engineering"**: "Without tests, we're not capturing our thinking for what generated code should do." Academic validation from Matthews & Nagappan confirms that providing LLMs with tests alongside problem statements consistently enhances code generation outcomes across GPT-4 and Llama 3.

The recommended workflow is **Test-Driven Generation (TDG)**:

1. Humans write or approve specifications
2. AI generates test cases from specs (Red)
3. AI generates implementation to pass tests (Green)
4. AI refactors within test-protected boundaries
5. Humans review both tests and implementation

The critical caveat: when AI writes both tests and code, it creates **confirmation bias** — tests that validate bugs. The solution is separating test authorship from code authorship, either by using different AI models or by having humans write test specifications.

**Property-based testing (PBT)** represents the most significant emerging pattern. The Property-Generated Solver research achieved **23.1–37.3% relative gains** over TDD baselines for AI code generation. The breakthrough finding: LLMs are dramatically better at generating correctness *properties* than producing flawless code. For "Hard" tasks, direct code generation achieved only 1.1% accuracy, but validation generation reached **48.9%**. PBT breaks the "cycle of self-deception" because properties capture essential correctness characteristics without requiring exact input-output mappings. AWS's Kiro IDE already integrates PBT throughout its workflow.

Security testing is non-negotiable: **~45% of AI-generated code contains security flaws** according to Veracode's 2025 report, with Java worst at 72%. Logic errors appear at **1.75×** the rate of human-written code. XSS vulnerabilities appear at **2.74×**. Security performance remains flat regardless of model size — "smarter" models are not more secure.

---

## Principle 5: Context engineering through layered instruction files

The infrastructure for AI agent instruction has matured rapidly. **AGENTS.md** has emerged as the universal standard, used by **60,000+ open-source projects** and supported by OpenAI Codex, Google Jules, Cursor, GitHub Copilot, and dozens more tools. It is stewarded by the Agentic AI Foundation under the Linux Foundation. **CLAUDE.md** serves as Claude Code's specific implementation with additional features like hierarchical loading and lazy evaluation.

The recommended architecture follows **progressive disclosure**:

- **Tier 1 — Always loaded** (CLAUDE.md/AGENTS.md root): Universal conventions, tech stack, key commands, architecture overview. Keep under **300 lines** — research shows LLM instruction-following degrades linearly with instruction count.
- **Tier 2 — Lazy-loaded** (subdirectory files): Component-specific patterns, loaded only when the agent works in that directory. In monorepos, OpenAI's repository reportedly uses 88 AGENTS.md files following this pattern.
- **Tier 3 — On-demand** (agent_docs/, references/): Deep documentation read only when explicitly needed. Skills (SKILL.md) provide modular capability packages with YAML frontmatter for selective activation.

Content should follow the **What/Why/How** framework: What is the tech stack and structure? Why do components exist? How should the agent work (commands, patterns, constraints)? Critical guidance: **never send an LLM to do a linter's job** — use deterministic tools for style enforcement, and reserve instruction files for architectural context and business rules. Examples beat abstractions: point to real files showing best patterns AND legacy files to avoid.

For cross-tool consistency, **rulebook-ai** generates the correct format for each AI assistant from a single source definition. The fragmentation problem — Cursor uses `.mdc` files, Windsurf uses `.windsurfrules`, Cline uses `.clinerules/`, GitHub Copilot uses `.github/copilot-instructions.md` — is real but manageable with generation tools and AGENTS.md as the universal base.

**MCP (Model Context Protocol)** complements instruction files by standardizing how agents connect to external tools and data sources. Skills encode *knowledge* (how to do things); MCP provides *capabilities* (access to tools, APIs, databases). Both use progressive loading to prevent "context rot" from loading everything simultaneously.

---

## Principle 6: Repository and team architecture for parallel agents

**Monorepos provide significant advantages for AI agents.** AI sees how frontend consumes backend APIs, can make atomic cross-project changes in single PRs, and enforces consistent conventions. AI agents also offset the traditional complexity costs of monorepos — large-scale migrations that took weeks now take hours. The counter-consideration: multi-repos offer clearer security boundaries for regulated environments.

Repository structure should be optimized for agent navigation. Create an explicit **codebase map** in AGENTS.md pointing to key files and directories. Use clear, descriptive directory names. Default to **small, focused files and components**. For monorepos, place CLAUDE.md files in subdirectories for lazy-loaded, component-specific context.

Team workflows are evolving toward **multi-agent parallelism**: practitioners run 3–5 Claude Code instances simultaneously in separate tmux windows on different branches, each handling a well-scoped task. Tools like **git-town** and **Graphite** manage stacked changes across parallel AI instances. The "80/20 rule" has inverted: **80% of code is written by AI, 20% of time is spent reviewing and correcting it**.

Code review has transformed fundamentally. PRs are **~18% larger** with AI adoption, but incidents per PR are up **~24%** and change failure rates up **~30%**. The emerging "PR Contract" requires: intent statement, proof it works (tests/demos), risk tier with AI disclosure, and specific areas needing human review. Treat AI-generated code as "helpful draft" — never commit code you cannot explain. Use different AI models for generation versus review to avoid echo chambers.

**Type annotations** are critically important — they provide the structured context that dramatically improves AI code generation and navigation quality. TypeScript's strict typing is a significant advantage over plain JavaScript. Python type hints combined with Pydantic generate automatic schemas that AI agents consume effectively. Every instruction file should mandate type annotations.

---

## Principle 7: Human role shifts from implementer to architect-reviewer

The AIDE methodology redefines the human developer's role across the SDLC:

- **Requirements & Architecture**: Humans OWN this entirely. Core architecture decisions, domain modeling, bounded context definitions, and security design remain human-led. AI assists with exploration and documentation.
- **Specification**: Humans write or approve specifications. The spec-first approach is the single biggest predictor of AI code quality. AWS AI-DLC's "Mob Elaboration" has PMs, devs, and QA collaborate with AI from the start.
- **Implementation**: Humans DELEGATE to AI agents, providing well-scoped tasks with clear boundaries. Direct, then review — like managing a team of fast but junior developers.
- **Testing**: Humans own test intent and specifications; AI generates test code and implementations. Property-based testing properties should be human-reviewed.
- **Review**: Humans focus on what AI misses — security holes, architectural drift, business context, institutional knowledge. AI handles first-pass review (style, obvious bugs).
- **Operations**: AI assists with incident triage, monitoring, and automated remediation within human-defined guardrails.

A critical equity concern: agentic engineering **disproportionately benefits senior engineers** who have deep architectural knowledge to guide agents effectively. There is a real risk of skill atrophy for junior developers who skip foundational learning. The methodology must include deliberate pathways for junior engineers to build fundamentals through guided AI collaboration rather than passive acceptance.

---

## Conclusion: The AIDE methodology in seven principles

The AIDE (Agent-Informed Development Engineering) methodology rests on a foundation that inverts conventional wisdom: the cheaper code generation becomes, the more valuable architectural discipline becomes. The seven principles — **context-window-aware sizing, conscious duplication, functional core with architectural shell, test-driven generation, layered instruction files, parallel-agent repository design, and human architect-reviewer roles** — form an integrated framework where each principle reinforces the others.

Three novel insights emerge from this synthesis. First, the **context window is the new CPU** — it is the binding constraint around which all architectural decisions must orient, just as memory and processing power shaped earlier eras. Second, **DRY is not dead but transformed** — the principle moves from "never duplicate code" to "never duplicate knowledge," with code-level repetition tolerable when it serves locality and agent comprehension. Third, **testing has become the specification language** — not a verification step after implementation, but the primary mechanism through which humans communicate intent to AI agents, with property-based testing representing a step change in validation quality.

The field is moving fast. AWS's AI-DLC is actively deployed in enterprises. AGENTS.md has reached 60,000+ repos in under a year. Karpathy declared vibe coding obsolete after just twelve months. The AIDE methodology should be treated as a living framework — versioned, iterated, and adapted as the capabilities of AI agents evolve and the community's collective understanding deepens.