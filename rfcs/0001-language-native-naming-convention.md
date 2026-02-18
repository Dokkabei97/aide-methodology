- RFC Number: 0001
- Title: Language-Native Naming Convention First
- Agent Used: Claude Code
- Agent Model: claude-opus-4-6
- Research Method: Conversation-driven analysis with cross-language ecosystem review
- Date: 2026-02-18
- Status: Draft

## Summary

The current AIDE naming convention guide uniformly recommends `snake_case` for function and variable names. While this aligns naturally with some languages (Python, Rust), it conflicts with the established conventions of most other languages — JavaScript/TypeScript (camelCase), Java/Kotlin (camelCase), C# (PascalCase/camelCase), Go (camelCase/PascalCase), and others.

This RFC proposes revising the naming guide to adopt a **"Language-Native Convention First"** principle, while preserving AIDE's core value of **Semantic Verbosity** as a case-style-independent rule.

## Motivation

### 1. Conflict with Language Ecosystems

Each programming language has official style guides and established conventions:

| Language | Functions/Methods | Variables | Official Guide |
|----------|-------------------|-----------|----------------|
| Python | snake_case | snake_case | PEP 8 |
| TypeScript/JavaScript | camelCase | camelCase | ESLint default, Google Style Guide |
| Java | camelCase | camelCase | Oracle Code Conventions |
| Kotlin | camelCase | camelCase | Kotlin Coding Conventions |
| Go | camelCase/PascalCase (exported) | camelCase | Effective Go |
| C# | PascalCase (method) / camelCase (local) | camelCase | .NET Naming Guidelines |
| Rust | snake_case | snake_case | Rust API Guidelines |
| Swift | camelCase | camelCase | Swift API Design Guidelines |

AIDE's uniform snake_case recommendation causes the following problems in most languages other than Python and Rust:

- **Linter/formatter conflicts**: Clashes with ESLint `camelcase` rule, ktlint, golint, etc.
- **Framework API inconsistency**: Style mismatch with React's `useState`, Spring's `getName()`, etc.
- **Third-party library integration friction**: Only project code uses snake_case while all external code uses camelCase

### 2. AI Agent Training Data Characteristics

AI code agents (Claude, GPT, Gemini, etc.) are trained on data written in each language's idiomatic style. Agents generate more accurate and consistent code when language-native conventions are followed. Enforcing snake_case can actually cause agents to produce inconsistent output, alternating between language norms and AIDE rules.

### 3. Need to Separate Core Value from Case Style

The true value of AIDE's naming guide is not the `snake_case` style itself, but the principle that **"the more specific a name is, the exponentially lower the probability of the agent misusing it"**. This Semantic Verbosity principle applies identically across all case styles:

```
# Semantic Verbosity is independent of case style
snake_case:  calculate_order_total_in_krw()   # Specific ✓
camelCase:   calculateOrderTotalInKrw()        # Equally specific ✓
Abbreviated: calc(d)                           # Ambiguous ✗ (any case)
```

## Detailed Design

### Change 1: Revise the Naming Convention Guide Section

**Current** (`docs/{en,ko}/AIDE-METHODOLOGY.md` and `docs/{en,ko}/04-PRACTICAL-GUIDE.md`)

A table prescribing snake_case as the default convention for function and variable names.

**Proposed**

Replace with a two-part structure: (1) Language-Native Convention First rule, (2) Semantic content rules with multi-language examples.

New table format:

| Rule | Description | Example (TS) | Example (Python) | Counter-Example |
|------|-------------|--------------|-------------------|-----------------|
| Verb-object for functions | Name describes action and target | `calculateOrderTotalInKrw()` | `calculate_order_total_in_krw()` | `calc(d)` |
| Meaningful variables | Name conveys purpose | `activeUserIdList` | `active_user_id_list` | `ids` |
| Explicit side effects | Prefix indicates side effect | `persistUserToDatabase()` | `persist_user_to_database()` | `save()` |
| Nouns for types | Type names are descriptive nouns | `OrderItem` | `OrderItem` | `OI` |
| Source in constants | Constant names include origin | `MAX_LOGIN_ATTEMPTS_PER_POLICY` | `MAX_LOGIN_ATTEMPTS_PER_POLICY` | `MAX` |
| File names | Follow language convention | `user-auth.ts` | `user_auth.py` | `ua.ts` |

### Change 2: Revise the CLAUDE.md Template Code Style Section

**Current**
```
- Function names: snake_case, verb_object form
- Variable names: snake_case, include meaning
```

**Proposed**
```
- Naming: Follow language-native convention (e.g., camelCase for TS, snake_case for Python)
- Naming content: verb_object for functions, meaningful nouns for variables, explicit side-effect prefixes
```

### Change 3: Synchronize Korean Documents

Apply equivalent translations of Changes 1 and 2 to `docs/ko/AIDE-METHODOLOGY.md` and `docs/ko/04-PRACTICAL-GUIDE.md`.

### Change 4: Synchronize Practical Guide

Apply identical principles to the naming convention sections in `docs/{en,ko}/04-PRACTICAL-GUIDE.md`.

## Evidence

### 1. Official Language Style Guides

- **PEP 8** (Python): Explicitly recommends snake_case for functions/variables
- **Google TypeScript Style Guide**: Uses camelCase for functions/variables
- **Kotlin Coding Conventions** (JetBrains official): Uses camelCase
- **Effective Go**: Uses MixedCaps (exported) / mixedCaps (unexported), discourages underscores

### 2. AI Agent Code Generation Quality

AI code agents are trained on each language's idiomatic style. Following language conventions results in:
- Higher consistency in generated code
- Natural integration with framework APIs
- Lint-free, immediately usable code output

### 3. Alignment with AIDE Principles

AIDE's **Principle 7: Deterministic Guardrails** encourages leveraging deterministic tools like linters and formatters. Following language-native conventions allows these tools to automatically enforce naming rules out of the box. Using non-standard conventions requires custom linter configuration, which actually conflicts with the Guardrails principle.

## Impact Assessment

### Effect on Existing Principles

- **Semantic Verbosity principle**: Preserved. Only the case style is decoupled; semantic content rules are strengthened.
- **Context Budget principle**: No impact. Name length and specificity guidance remains the same.
- **Deterministic Guardrails principle**: Strengthened. Language-default linters can be used as-is.

### Effect on Current Adopters

- **Python users**: No change (snake_case is already Python convention)
- **TypeScript/JavaScript users**: May transition to camelCase. Gradual migration recommended for existing snake_case codebases.
- **Other language users**: Explicit permission to follow their language's conventions.

### Compatibility

This change does not modify any of the 10 core principles. It is a Practical Guide-level revision only.

## Alternatives Considered

### Alternative A: Maintain Current State (Uniform snake_case)

- **Advantage**: Consistency across polyglot projects
- **Rejected because**: Conflicts with most language ecosystems and reduces AI agent code generation quality. The cost of ecosystem friction outweighs the benefit of cross-language consistency.

### Alternative B: Provide Per-Language Mapping Table

- **Advantage**: Can specify exact conventions for each language
- **Rejected because**: Ties the methodology to a specific list of languages. Requires document updates whenever a new language is added. The principle "follow language-native convention" is more universal and maintainable.

### Alternative C: Remove Naming Convention Section Entirely

- **Advantage**: Simplest solution
- **Rejected because**: The Semantic Verbosity principle is a valuable part of AIDE and should be preserved. The correct approach is to decouple it from case style, not to discard it.
