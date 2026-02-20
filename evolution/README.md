# AIDE Evolution Engine

The Evolution Engine is AIDE v2.0's autonomous self-evolution system. It automatically monitors agent capability benchmarks, proposes principle adjustments through multi-agent deliberation, validates changes empirically, and applies updates — all without human intervention.

## Architecture

```
Evolution Engine Pipeline:

  SENSE ──> DELIBERATE ──> VALIDATE ──> APPLY
  (data)    (3-agent)     (empirical)  (auto-commit)
              debate        gate
```

## Directory Structure

```
evolution/
  scripts/              # Python scripts for each pipeline phase
    collect_benchmarks.py    # Phase 1: Benchmark data collection
    scan_models.py           # Phase 1: Model release scanning
    check_triggers.py        # Phase 1: Invalidation trigger checking
    compile_sense_report.py  # Phase 1: Sense report compilation
    deliberate_research.py   # Phase 2: Research Agent (Claude)
    deliberate_adversary.py  # Phase 2: Adversary Agent (GPT)
    deliberate_synthesis.py  # Phase 2: Synthesis Agent (Gemini)
    validate_baseline.py     # Phase 3: Baseline task execution
    validate_modified.py     # Phase 3: Modified task execution
    empirical_gate.py        # Phase 3: Metric comparison gate
    apply_changes.py         # Phase 4: Apply to principle-metadata.yaml
    update_docs.py           # Phase 4: Update EN/KO methodology docs
    record_history.py        # Phase 4: Record evolution history
    drift_detection.py       # Safeguard: Detect directional bias
  benchmarks/           # Collected benchmark data (auto-generated)
  deliberation/         # Agent deliberation artifacts (auto-generated)
  sandbox/              # Empirical validation results (auto-generated)
  history/              # Evolution audit trail (permanent record)
```

## Triggering the Engine

The engine runs automatically on:
- **Monthly schedule**: 1st of every month at 09:00 UTC
- **Model releases**: Via repository_dispatch event
- **Benchmark shifts**: When tracked benchmarks change by >10%

Manual trigger: `gh workflow run aide-evolution-engine.yml`

## Required Secrets

| Secret | Description |
|--------|-------------|
| `ANTHROPIC_API_KEY` | For Claude Code CLI (Research Agent) |
| `OPENAI_API_KEY` | For Codex CLI (Adversary Agent) |
| `GOOGLE_API_KEY` | For Gemini CLI (Synthesis Agent) |
| `AIDE_BOT_TOKEN` | GitHub PAT for auto-commits |

## Axiom Compliance

Every evolution cycle verifies compliance with the 5 Immutable Axioms:
- **A1 Reversibility**: All changes are git-backed and revertable
- **A2 Adversarial Separation**: 3 different-vendor models participate
- **A3 Empiricism**: Changes require quantitative evidence
- **A4 No Single Authority**: Consensus from 3 agents required
- **A5 Self-Observability**: Full audit trail in evolution/history/
