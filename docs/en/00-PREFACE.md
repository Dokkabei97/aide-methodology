# AIDE (Agent-Informed Development Engineering) -- A Software Development Methodology for the Agentic Era v1.0

**Author**: CTO (20+ years of architecture experience, 3 years of hands-on AI agent experience)
**Based on**: GPT/Claude/Gemini triple deep research + Team Alpha (Integrationists) 2 reports + Team Beta (Radicals) 1 report
**Date**: 2026-02-18

---

## Preface: Why AIDE Is Needed

### The Limitations of Existing Methodologies and the New Constraints of the AI Agent Era

The last 50 years of software engineering have been a struggle to manage **human cognitive limitations**. The constraints of working memory, exemplified by Miller's "7 +/- 2" law, gave rise to modularization, abstraction, separation of concerns, and the DRY principle. DDD, Clean Architecture, SOLID, TDD -- everything we call "good software engineering" has been a defense mechanism against these biological constraints.

In 2025-2026, as AI agents have emerged as the primary producers of code, the constraints have fundamentally changed:

| Constraint Dimension | Human Developer | AI Agent |
|----------------------|-----------------|----------|
| Memory Capacity | Extremely small working memory (7+/-2 chunks) | Large context window (hundreds of thousands to millions of tokens), but **Lost in the Middle** phenomenon causes information loss in the middle |
| Repetitive Tasks | Fatigue, prone to errors | No fatigue, high-speed parallel processing |
| Reasoning Style | Deep logic, causal reasoning, gestalt perception | Probabilistic pattern matching, **performance degradation in multi-hop reasoning** |
| Vulnerabilities | Complexity, boredom | Hallucination, attention diffusion in long contexts, failure to infer implicit context |
| Cost Model | Labor cost (monthly basis) | Token cost (per-call basis), proportional to context size |

Existing methodologies do not address these new constraints:
- **Context window cost**: Clean Architecture code spread across 8 files causes context fragmentation for agents
- **Non-deterministic execution**: The same input can produce different outputs, shaking the premises of traditional TDD
- **New artifacts**: AGENTS.md, CLAUDE.md, and Skills files govern system behavior, but existing methodologies have no management framework for them
- **New threats**: Security flaws in AI-generated code (XSS, SQL Injection, logic errors) can infiltrate the codebase at rapid speed

### AIDE's Positioning: "Evolution," Not "Replacement"

To write this document, we reviewed reports from two teams: Team Alpha (Integrationists) and Team Beta (Radicals). The core disagreement between the two teams was as follows:

- **Team Alpha**: "Existing methodologies represent decades of proven engineering wisdom. We just need to reinterpret and extend them for the new participant: AI agents."
- **Team Beta**: "Existing methodologies were built for human cognitive limitations. They actually hinder AI agents. We need a new foundation."

**CTO's Final Judgment: AIDE is an "evolution."** The detailed rationale is covered in Part 7, but the core logic is this:

1. **The fundamental problems have not disappeared.** Complexity management, changeability, quality assurance -- these challenges remain valid in the AI agent era. In fact, as AI generates code faster, the rate of technical debt accumulation has also accelerated (24% increase in incidents per PR, 30% increase in change failure rate).
2. **However, the constraints have fundamentally changed.** Context windows, probabilistic generation, hallucination, and security vulnerabilities cannot be addressed with "minor adjustments." The data from Factory.ai showing that excessive abstraction and indirection increase agent hallucination probability cannot be ignored.
3. **Therefore, AIDE preserves the core values of existing principles while realigning implementation approaches and priorities to match the cognitive characteristics of AI agents.** This is not a "compromise" but a rational adaptation to changed constraints.

Tweag's controlled experiment supports this: an AI-assisted team using a spec-first approach (core of existing methodologies) with strong review discipline achieved **45% faster development speed**. Teams that applied existing principles well achieved better results with AI. At the same time, the fact that Karpathy abandoned "Vibe Coding" after just one year and pivoted to "Agentic Engineering" demonstrates that undisciplined AI usage quickly hits its limits.

---



← Previous: [INDEX](./INDEX.md) | Next: [01-CORE-PRINCIPLES](./01-CORE-PRINCIPLES.md) →
