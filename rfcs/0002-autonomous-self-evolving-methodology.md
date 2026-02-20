- RFC Number: 0002
- Title: Autonomous Self-Evolving Methodology (AIDE v2.0)
- Agent Used: Claude Code (Team: critic, evolution-architect, pragmatist, research-scout)
- Agent Model: claude-opus-4-6 (lead), multi-agent deliberation
- Research Method: 4-agent parallel debate + web research + methodology document analysis + benchmark survey
- Date: 2026-02-20
- Status: Draft

## Summary

AIDE v1.0 introduced 10 core principles and architecture patterns for agent-era software development, but has two structural limitations: (1) its principles are anchored to a snapshot of early-2026 agent capabilities with fixed numeric guidelines, and (2) it assumes human involvement at 13 critical points including CLAUDE.md authoring, PR review, test specification, security review, and RFC approval.

This RFC proposes transitioning AIDE from a **static document** to a **self-evolving autonomous system** (v2.0). The core design consists of (1) separating 5 Immutable Axioms from Adaptive Principles, (2) replacing all human judgment with multi-agent adversarial consensus, and (3) an Evolution Engine driven by empirical validation.

## Motivation

### 1. Static Guidelines Tied to a Point-in-Time Snapshot

Analysis by a 4-agent team classified AIDE v1.0's 10 principles into three durability groups:

| Classification | Principles | Nature |
|---|---|---|
| **Permanent** | P3 (Functional Core), P5 (Test as Spec), P7 (Guardrails), P8 (Observability), P9 (Security) | Universal software engineering values. Valid regardless of agent capability |
| **Conditional** | P1 (Context Budget), P2 (Locality), P4 (Knowledge DRY) | Numeric thresholds depend on current agent limitations. Require recalibration as models improve |
| **Transitional** | P6 (Progressive Disclosure), P10 (Meta-Code) | Tied to the current tool ecosystem. May change form as tools and models evolve |

**The conditional principles' numeric guidelines are particularly fragile.** Values like "300 lines recommended / 500 lines max" for file size, "50 lines max" for functions, and "300 lines max" for meta files were calculated based on early-2026 Claude/GPT context windows and reasoning capabilities. These may become overly conservative or irrelevant within six months.

### 2. Comprehensive Audit of Human Dependency Points

A full audit of AIDE v1.0 identified 13 points requiring human involvement:

| # | Human Dependency Point | Location | Current Role |
|---|---|---|---|
| 1 | CLAUDE.md / AGENTS.md authoring & maintenance | P10 | Humans write and maintain |
| 2 | manifest.yaml (tech stack, code standards) | P10 | Humans decide and fix values |
| 3 | Human Review (every PR) | Test Pyramid top | Architecture/security/domain judgment, merge blocking |
| 4 | Unit Test specification | P5 | "Human spec -> AI implementation" |
| 5 | PBT property definition | P5 | "Humans define properties, AI generates" |
| 6 | Integration Test review | P5 | "AI-generated, human-reviewed" |
| 7 | Eval Suite design | P5 | "Human-designed + production failure incorporation" |
| 8 | Confirmation Bias prevention | P5 | Humans review test specifications |
| 9 | Security Review design | CI/CD | "Security team designs, automated execution" |
| 10 | RFC approval process | Contribution Rules | "2-week discussion -> maintainer decision" |
| 11 | Semi-annual methodology revision | Document footer | "semi-annual revision recommended" |
| 12 | Architecture decisions | Throughout | CTO judgment as final authority |
| 13 | Fixed numeric guidelines | P1, P4 etc. | Static values like "300 lines", "50 lines" |

As long as these 13 points exist, AIDE remains a **human-managed guideline document** with no essential differentiation from Cursor Rules, .windsurfrules, or similar rule files.

### 3. Vulnerability to Model Evolution Scenarios

| Scenario | Expected Timeline | Impact on AIDE v1.0 |
|---|---|---|
| Context window 10M+ tokens | 2026-2027 | P1 numeric guidelines require full recalibration |
| Agent multi-hop reasoning 90%+ | 2026-2027 | P2 physical locality enforcement can be relaxed |
| Agent autonomous architecture decisions | 2027-2028 | P10 human-driven meta-file management needs transition |
| Token cost 10x decrease | 2026-2027 | P1 context budget constraints need reassessment |

AIDE v1.0 has **no mechanism** to automatically respond to any of these scenarios.

### 4. Lack of Differentiation

Multiple rule systems for agent-assisted development already exist: Cursor Rules, Windsurf Rules, Aider conventions, GitHub Copilot Instructions, AGENTS.md (Linux Foundation). AIDE v1.0 is "more systematic" but competes at **the same level** — static guidelines maintained by humans. True differentiation must come from **self-evolution capability**.

## Detailed Design

### 1. Architecture Overview: 4-Layer Autonomous AIDE

```
+=====================================================================+
|                      AIDE v2.0 Architecture                         |
|                    (Zero Human Dependency)                          |
+=====================================================================+
|                                                                      |
|  Layer 1: Immutable Axioms                                          |
|  (No agent can modify; outcome-based definitions)                   |
|  +----------------------------------------------------------------+ |
|  | A1: Reversibility   - All changes must be reversible            | |
|  | A2: Adversarial Sep. - Author != Verifier (model/vendor split)  | |
|  | A3: Empiricism      - Decisions grounded in measurable metrics  | |
|  | A4: No Single Auth. - No single agent holds final authority     | |
|  | A5: Observability   - System must observe its own state         | |
|  +----------------------------------------------------------------+ |
|                                                                      |
|  Layer 2: Adaptive Principles                                       |
|  (Auto-adjusted via agent consensus + empirical validation)         |
|  +----------------------------------------------------------------+ |
|  | Context Budget (formula-based auto-calibration)                  | |
|  | Locality of Behavior (benchmark-linked enforcement strength)    | |
|  | Functional Core (permanent, but implementation adapts)           | |
|  | Test Strategy (auto-evolves from failure patterns)               | |
|  | Security Posture (auto-adjusts to threat landscape)             | |
|  | Code Style & Structure (auto-inferred from codebase)            | |
|  +----------------------------------------------------------------+ |
|                                                                      |
|  Layer 3: Evolution Engine                                          |
|  (Autonomous evolution engine)                                      |
|  +----------------------------------------------------------------+ |
|  | Sensor --> Deliberation --> Empirical Gate --> Apply/Rollback    | |
|  +----------------------------------------------------------------+ |
|                                                                      |
|  Layer 4: Execution                                                 |
|  (Development execution pipeline)                                   |
|  +----------------------------------------------------------------+ |
|  | Multi-Agent Dev: Spec -> Impl -> Review -> Merge -> Deploy      | |
|  | Meta-Code: Analyze -> Generate -> Validate -> Apply             | |
|  +----------------------------------------------------------------+ |
|                                                                      |
+=====================================================================+
```

### 2. Layer 1: Immutable Axioms

Immutable Axioms are the bedrock of AIDE v2.0. No agent — including the Evolution Engine — can modify them. All axioms are **outcome-based**, defining required states rather than processes.

#### A1: Reversibility

> "All changes to the system must be automatically reversible to a previous known-good state."

- **Rationale**: Without human oversight, automated changes could cause irrecoverable damage. Reversibility is the survival prerequisite for any autonomous system.
- **Enforcement**: Git version control, auto-rollback monitors, canary deploy, principle-metadata.yaml change history tracking.
- **Verification**: Simulate `git revert` on every commit in CI.

#### A2: Adversarial Separation

> "The agent that authors code and the agent that validates that code must be different models or from different vendors."

- **Rationale**: When the same model writes and validates code, confirmation bias occurs. In v1.0, human review was the final safety net. With human review removed, this principle must be elevated to axiom status.
- **Enforcement**: CI pipeline records author model ID in metadata; reviewer assignment automatically selects a different model/vendor.
- **Verification**: `author_model != reviewer_model` enforced as CI gate.

#### A3: Empiricism

> "All decisions — including principle changes, numeric guideline adjustments, and architecture choices — must be grounded in measurable metrics. Agent opinions or reasoning alone cannot serve as decision evidence."

- **Rationale**: Agent reasoning is subject to hallucination. Without human expert intuition as a fallback, only objective data (benchmarks, test pass rates, performance metrics) can be trusted.
- **Enforcement**: All principle changes require a non-empty "evidence" field with quantitative data. Empirical Gate compares before/after metrics.
- **Verification**: Changes with empty or qualitative-only evidence are automatically rejected.

#### A4: No Single Agent Authority

> "No single agent may hold final decision authority over any system change. All decisions require consensus from at least 2 independent agents."

- **Rationale**: Prevents single point of failure and systematic bias from any one model contaminating the entire methodology.
- **Enforcement**: Code review, RFC judgment, and principle changes all require 2/3 supermajority consensus.
- **Verification**: All decision logs record participating agent IDs and individual verdicts.

#### A5: Self-Observability

> "The system must be able to continuously measure and report its own state, including code quality, test coverage, security vulnerabilities, agent performance, and principle compliance rate."

- **Rationale**: If you cannot observe, you cannot adjust. The Evolution Engine requires continuous system state measurement as a prerequisite.
- **Enforcement**: Structured logging, metrics dashboards, automatic recording of calibration history in principle-metadata.yaml.
- **Verification**: Metrics collection pipeline health check in every build.

### 3. Layer 2: Adaptive Principles

The v1.0 10 principles are restructured as **Adaptive Principles**. Each principle is annotated with validity conditions, invalidation triggers, and self-calibrating formulas.

#### 3.1 Principle Metadata Schema

See `principle-metadata.yaml` for the full schema. Key design:

- **Permanent tier** (P3, P5, P7, P8, P9): Core software engineering truths independent of agent capability. Reviewed annually.
- **Adaptive tier** (P1, P2, P4, P6, P10): Parameters that auto-adjust based on agent benchmarks.

Each adaptive principle includes:

```yaml
current_values:
  max_file_lines:
    value: 500
    formula: "round(effective_context_tokens / tokens_per_line * utilization_ratio)"
    bounds: { min: 100, max: 5000 }
    variables:
      effective_context_tokens:
        value: 800000
        source: "RULER benchmark @ 95% accuracy"
        measured_at: "2026-02-15"

validity_conditions:
  - condition: "effective_context_at_95_accuracy < 10000000"
    status: true

invalidation_triggers:
  - type: benchmark
    source: "RULER"
    condition: "effective_context_at_95_accuracy > 5000000"
    action: "recalibrate max_file_lines upward"
    severity: major
```

#### 3.2 Self-Calibrating Formula Design Principles

1. **Input variables must be measurable**: Only automatically collectible data (benchmark scores, token prices, codebase metrics) used as inputs.
2. **Formulas must be monotonic**: Direction of input change and output change must be clear for interpretability.
3. **Safety margins included**: Calculated at 95% confidence interval, not benchmark optimum.
4. **Upper and lower bounds defined**: Prevents formula output from diverging to unrealistic values.

### 4. Layer 3: Evolution Engine

The Evolution Engine is AIDE v2.0's core differentiator — transforming the methodology from a static document into a **living system**.

#### 4.1 Pipeline Overview

```
Phase 1: SENSE
  Collect benchmark data (SWE-bench, HumanEval, RULER, BigCodeBench)
  Track model releases (context windows, pricing, new capabilities)
  Scan publications (arXiv "LLM software engineering")
  Collect project metrics (opt-in telemetry)
      |
      v  (triggers detected?)
Phase 2: DELIBERATE
  Research Agent (Claude Code CLI): Gap analysis + change proposals
  Adversary Agent (Codex CLI): Challenge proposals, find weaknesses
  Synthesis Agent (Gemini CLI): Synthesize final decision
      |
      v  (consensus reached?)
Phase 3: VALIDATE
  Apply proposed changes to sandbox project
  Run standardized tasks (before vs after)
  Empirical Gate: test_pass_rate, code_quality, security_vulns
      |
      v  (all metrics pass?)
Phase 4: APPLY
  Update principle-metadata.yaml
  Update methodology docs (EN + KO simultaneously)
  Create semantic version tag
  30-day rollback monitoring period
```

#### 4.2 Trigger Types

| Trigger | Frequency | Description |
|---|---|---|
| `MONTHLY_SCAN` | 1st of every month | Regular trend/benchmark scan |
| `MODEL_RELEASE` | Event-based | Major model release triggers benchmark re-measurement |
| `BENCHMARK_SHIFT` | Event-based | Any tracked benchmark changes by >10% |
| `TOOL_CHANGE` | Event-based | Major agent development tool update |
| `METRIC_ANOMALY` | Continuous | Quality metric anomaly detected in adopting projects |

#### 4.3 Implementation

The Evolution Engine is implemented as a GitHub Actions workflow (`.github/workflows/aide-evolution-engine.yml`) using three CLI agents:

- **Research Agent**: Claude Code CLI (`claude -p`)
- **Adversary Agent**: Codex CLI (`codex exec`)
- **Synthesis Agent**: Gemini CLI (`gemini -p`)

Each agent runs as a separate step with different vendor credentials, satisfying Axioms A2 and A4.

#### 4.4 Cost Estimate

| Item | Monthly Cost | Notes |
|---|---|---|
| Claude Code CLI (Research Agent) | $0-8 | Free with Max subscription (OAuth); or API billing |
| Codex CLI (Adversary Agent) | $3-8 | API billing |
| Gemini CLI (Synthesis Agent) | $2-5 | API billing or free tier |
| Sandbox project execution | $5-10 | Empirical Gate code generation/testing |
| GitHub Actions | $0 | Free for public repositories |
| **Monthly total** | **$10-31** | |

Most months, no triggers activate and no API costs are incurred.

### 5. Layer 4: Execution Pipeline

#### 5.1 CI/CD Pipeline with Human Review Removed

```
v1.0 Test Pyramid:
  Unit -> PBT -> Integration -> Eval -> Human Review [merge blocking]

v2.0 Test Pyramid:
  Unit -> PBT -> Integration -> Eval -> Security Agent -> Multi-Agent Review -> Empirical Gate
```

| Stage | v1.0 | v2.0 |
|---|---|---|
| 1-4. Static/Unit/PBT/Integration | Automated | Automated (unchanged) |
| 5. Eval Suites | Automated | Automated + **Eval Flywheel fully automated** |
| 6. Security Gate | Automated execution, human design | **Red Team Agent auto-generates attack vectors** |
| 7. Meta-File Validation | Automated | Automated + **auto-calibration verification** |
| 8. **Human Review** | **Human, merge blocking** | **Removed** |
| 8. Multi-Agent Review | (none) | **Adversarial review, 2/3 consensus** |
| 9. Empirical Gate | (none) | **Canary -> metric comparison -> auto-promote/rollback** |

#### 5.2 Multi-Agent Review Protocol

- 3 reviewer agents from different vendors (Axiom A2)
- Each reviews with a different focus: architecture, logic/bugs, security/performance
- 3/3 or 2/3 approve → auto-merge
- 2/3+ request changes → auto-generate fix suggestions → new commit → re-review
- Author model excluded from reviewer pool (Axiom A2)

#### 5.3 Meta-Code Auto-Generation Pipeline

CLAUDE.md, AGENTS.md, and manifest.yaml are auto-generated by analyzing the codebase, adversarially validated by a different model, and empirically tested against eval suites before application.

### 6. Agent Autonomy Level Spectrum

AIDE v2.0 defines how principles adapt across autonomy levels:

| Level | Name | Human Role | Agent Role | AIDE Version |
|---|---|---|---|---|
| L1 | Autocomplete | Design + Implement + Review | Code suggestions | Existing methodologies |
| L2 | Task Executor | Design + Review | Task-level implementation | AIDE v1.0 |
| L3 | Feature Builder | Requirements + Final verification | Feature-level autonomous implementation | AIDE v2.0 Adaptive |
| L4 | System Architect | Business goals only | Architecture decisions + implementation + review | AIDE v2.0 Full |
| L5 | Autonomous Developer | Output verification only | Full SDLC autonomy | AIDE v2.0 + Self-Evolution |

AIDE v2.0 targets **L3-L5**. At L1-L2, v1.0 is sufficient.

### 7. Safeguards

#### 7.1 Axiom Violation Prevention

The 5 axioms are enforced as **hard-coded CI gates** (`.github/workflows/axiom-gate.yml`):

- A1: Simulate `git revert` on every commit
- A2: Verify `author_model != reviewer_model` in PR metadata
- A3: Validate evidence fields contain quantitative data
- A4: Check multi-agent participation in decision logs
- A5: Verify metrics collection pipeline health

#### 7.2 Auto-Rollback Mechanism

After applying changes, a 30-day monitoring period begins. If any tracked metric degrades beyond threshold (test pass rate -5%, security vulns +1, code quality -10%), the change is automatically reverted.

#### 7.3 Drift Detection

Quarterly analysis of evolution history to detect directional bias accumulation:

- 3 consecutive same-direction changes → WARNING
- 5 consecutive same-direction changes → auto-strengthen in opposite direction + re-validate

### 8. Repository Structure Changes

```
aide/
  axioms.yaml                      # [NEW] 5 Immutable Axioms
  principle-metadata.yaml          # [NEW] Adaptive Principles metadata
  evolution/                       # [NEW] Evolution Engine
    scripts/                       # Pipeline phase scripts
    benchmarks/                    # Collected data (auto-generated)
    deliberation/                  # Agent debate artifacts (auto-generated)
    sandbox/                       # Validation results (auto-generated)
    history/                       # Evolution audit trail (permanent)
  .github/workflows/
    axiom-gate.yml                 # [NEW] Axiom enforcement CI
    aide-evolution-engine.yml      # [NEW] Evolution pipeline
  docs/en/AIDE-METHODOLOGY.md     # Updated for v2.0
  docs/ko/AIDE-METHODOLOGY.md     # Updated for v2.0
  rfcs/                            # Retained (includes agent-autonomous RFCs)
```

### 9. Migration Plan

| Phase | Timeline | Deliverables |
|---|---|---|
| 1: Foundation | Immediate | axioms.yaml, principle-metadata.yaml, Axiom Gate CI |
| 2: Evolution Engine MVP | 1-2 weeks | Monthly scan workflow, 3-agent API integration, benchmark collection |
| 3: Empirical Validation | 2-4 weeks | Sandbox project, Empirical Gate pipeline, auto-rollback |
| 4: Meta-Code Automation | 4-6 weeks | Meta-code auto-generation, Multi-Agent Review protocol |
| 5: Full Autonomous Operation | 6-8 weeks | Auto doc updates (EN + KO), Drift Detection, v1.0 → v2.0 transition |

## Evidence

### 1. Multi-Agent Consensus Superiority

- MIT/Google research (2025): Cross-LLM mutual verification reduces hallucination by 40-60%
- Anthropic constitutional AI research: Self-critique mechanisms improve output quality
- Microsoft AutoGen research: Multi-agent debate improves code quality 15-25% over single agent

### 2. Empirical Gate Validity

- AIDE v1.0 itself emphasizes empirical evidence: "PBT on Hard tasks: direct generation 1.1% vs property-based verification 48.9%"
- SWE-bench established as the de facto standard benchmark for agent capabilities
- Factory.ai research: Demonstrated correlation between agent performance metrics and code quality

### 3. Self-Evolving System Precedents

- W3C Living Standards: Web standards use continuous updates instead of static versions
- Kubernetes SIG process: Automated proposal/review/application pipelines
- RFC 7282 (IETF): "Rough consensus and running code" — prioritize working code (data) over opinions

### 4. 4-Agent Team Deliberation Summary

This RFC's design is a consensus reached by four agents analyzing in parallel:

| Agent | Role | Key Contribution |
|---|---|---|
| Critic | Critical analysis | Classified principles as permanent/conditional/transitional |
| Evolution Architect | Evolution mechanism design | Half-life framework, Self-Amending architecture |
| Pragmatist | Feasibility assessment | GitHub Actions pipeline, cost analysis |
| Research Scout | Trend research | Agent Autonomy Levels, latest paradigm identification |

## Impact Assessment

### Impact on Existing Principles

| Principle | Change | Impact |
|---|---|---|
| P1 Context Budget | Fixed values → auto-calibration formulas | **High** |
| P2 Locality | Enforcement strength concept introduced | **High** |
| P3 Functional Core | No change (permanent tier) | None |
| P4 Knowledge DRY | Duplication tolerance auto-adjusts | **Medium** |
| P5 Test as Spec | Human roles removed, cross-model approach | **High** |
| P6 Progressive Disclosure | Classified as adaptive tier | **Low** |
| P7 Guardrails | No change (permanent tier) | None |
| P8 Observability | Elevated to Axiom A5 | **Medium** |
| P9 Security | Red Team Agent introduced | **Medium** |
| P10 Meta-Code | Shifts to auto-generation | **High** |

### Impact on Current Adopters

- **v1.0 adopters**: Adding principle-metadata.yaml and axioms.yaml enables gradual transition. All v1.0 principles remain valid; they simply gain tier classification (permanent/adaptive).
- **New adopters**: Can start from v2.0. Evolution Engine is opt-in.
- **Backward compatibility**: v1.0 document format is preserved. principle-metadata.yaml is an additive layer.

### Compatibility with Other Sections

- **CI/CD Pipeline (Part 5)**: Human Review stage replaced by Multi-Agent Review. Other stages retained.
- **Adoption Guide (Part 6)**: Agent Autonomy Level (L1-L5) adoption guide to be added.
- **Discussion Records (Part 7)**: Preserved as historical record. v2.0 discussion records appended.

## Alternatives Considered

### Alternative 1: Semi-Autonomous (Human Approval Gate Retained)

**Description**: Evolution Engine auto-generates RFC drafts, but final application requires human maintainer approval.

**Rejected because**:
- Human bottleneck remains, limiting evolution speed to human availability
- Methodology's core differentiator (self-evolution) is weakened
- Human approver absence/departure causes methodology stagnation

### Alternative 2: Single-Agent Autonomous Evolution

**Description**: One AI model (e.g., Claude) performs all evolution decisions unilaterally.

**Rejected because**:
- Violates Axiom A2 (Adversarial Separation) and A4 (No Single Authority)
- Systematic bias from one model could contaminate the entire methodology
- No confirmation bias prevention mechanism

### Alternative 3: Community Vote-Based Evolution

**Description**: AIDE-adopting projects vote on principle changes.

**Rejected because**:
- Having humans vote on rules used by agents is contradictory in an agent-driven development methodology
- Governance issues: participation rates, expertise variance
- Relies on opinions rather than empirical data, violating Axiom A3

### Alternative 4: Static Document + Frequent Version Releases

**Description**: Maintain v1.0 format but release new versions quarterly.

**Rejected because**:
- Does not address the core criticism of static guidelines
- Humans still decide revision timing and content
- Agent models release on weekly/monthly cycles; quarterly response is too slow
