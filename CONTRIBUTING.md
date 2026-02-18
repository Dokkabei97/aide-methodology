# Contributing to AIDE (Agent-Informed Development Engineering)

## Philosophy: Agent-First Contribution Model

AIDE was built by agents and evolves through agents.

This project follows an **Agent-First contribution model**. Unlike traditional open-source projects where humans write all code and documentation, AIDE recognizes that AI agents are not just tools — they are collaborators. The methodology itself was researched, debated, and authored by AI agents under human direction, and we expect contributions to follow the same model.

**Why?** Because AIDE is a methodology *about* agent-era development. If the methodology cannot be evolved using the very practices it describes, something is fundamentally wrong.

## Contribution Types

| Type | Human Direct? | Agent Required? | Description |
|------|:------------:|:---------------:|-------------|
| Typo/grammar fixes | Yes | No | Only type humans can directly PR |
| Methodology content changes | No | **Yes** | RFC proposal → Agent writes → Human reviews |
| New principles/sections | No | **Yes** | RFC + Agent research/writing required |
| Translations | No | **Yes** | Agent translates, human reviews |
| Example projects | Structure only | **Yes** | Agent implements, human validates |

### Why These Rules?

- **Typo fixes** are mechanical — no architectural reasoning needed.
- **Content changes** require deep understanding of methodology context, cross-referencing with research, and consistency checking — tasks where agents excel.
- **Translations** require maintaining technical nuance across languages — agents provide consistency that manual translation cannot.
- **Examples** must faithfully demonstrate AIDE principles — agents can ensure alignment with the methodology.

## Pull Request Requirements

Every PR must include the following fields:

- **`Agent`**: The agent used (e.g., Claude Code, Cursor, GitHub Copilot)
- **`Agent Model`**: The specific model (e.g., claude-opus-4-6, gpt-4o)
- **`Human Role`**: What the human did (e.g., "Direction and review", "Direct typo fix")

For typo/grammar fixes, the Human Role field is sufficient — agent fields can be marked as "N/A".

## RFC Process

For any change beyond typo fixes, an RFC (Request for Comments) is required:

### Step 1: Raise Direction
Human raises a direction or problem via a [GitHub Issue](../../issues/new?template=rfc-proposal.yml). Describe the problem or gap, not the solution.

### Step 2: Agent Drafts RFC
Using the [RFC template](rfcs/0000-template.md), an AI agent drafts the RFC document. The agent should research the topic, consider alternatives, and provide evidence.

### Step 3: Submit as PR
Submit the RFC as a Pull Request. Agent usage information is **required** — which agent, which model, what research method was used.

### Step 4: Community Discussion
A minimum 2-week discussion period allows the community to review, critique, and suggest improvements. The agent may be used to address feedback and revise the RFC.

### Step 5: Maintainer Decision
Project maintainers make the final decision to accept, reject, or request revisions.

## Why Agent-First?

The Agent-First model is not about excluding humans. It is about:

1. **Practicing what we preach** — AIDE describes agent-era development; contributions should demonstrate it.
2. **Quality through capability** — Agents can cross-reference the entire methodology, check consistency, and maintain voice/tone across thousands of words.
3. **Transparency** — By requiring agent disclosure, we build a contribution history that itself becomes research data for the methodology.
4. **Accessibility** — Non-native English speakers can contribute high-quality content by directing agents in their preferred language.
5. **Evolution** — As agents improve, the methodology improves. The contribution model creates a positive feedback loop.

## Getting Started

1. Read the [AIDE Methodology](README.md) thoroughly.
2. Check existing [Issues](../../issues) and [RFCs](rfcs/) for ongoing discussions.
3. For typo fixes: Fork, fix, and submit a PR.
4. For everything else: Open an Issue first, then work with an AI agent to draft your contribution.

## Code of Conduct

All contributors are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md).
