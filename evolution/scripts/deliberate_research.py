"""
AIDE Evolution Engine — Phase 2: Research Agent (Claude Code CLI)

The Research Agent performs gap analysis between current principles
and collected benchmark data, then generates change proposals.

Runs via: claude -p "$PROMPT" --output-format json
Axiom A2: This agent's proposals will be challenged by a DIFFERENT model (Codex).
Axiom A4: This agent cannot make unilateral decisions.
"""

import os
import subprocess
import shutil
import yaml
from datetime import datetime, timezone

SENSE_REPORT = os.environ.get("SENSE_REPORT", "evolution/benchmarks/sense-report.yaml")
PRINCIPLE_METADATA = os.environ.get("PRINCIPLE_METADATA", "principle-metadata.yaml")
OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "evolution/deliberation/research-proposal.yaml")

RESEARCH_PROMPT_TEMPLATE = """You are the AIDE Evolution Engine's Research Agent.

Your role is to analyze benchmark data and propose principle adjustments.

RULES:
1. You may ONLY propose changes to "adaptive" tier principles, never "permanent" tier.
2. Every proposal MUST include quantitative evidence from the sense report.
3. You must respect the Immutable Axioms (A1-A5) — they cannot be changed.
4. Proposals must include specific new values AND the formula that produced them.
5. You must assess the risk level (low/medium/high) of each proposed change.

OUTPUT FORMAT: Respond with ONLY a YAML block (no markdown fences), structured as:

proposals:
  - principle_id: "P1"
    field: "max_file_lines"
    current_value: 500
    proposed_value: 700
    formula_with_new_inputs: "round(1200000 / 18 * 0.03)"
    evidence:
      benchmark: "RULER"
      metric: "effective_context_at_95_accuracy"
      old_value: 800000
      new_value: 1200000
    risk_level: "low"
    rationale: "..."
summary: "..."

---

## Current Principles
{principles}

## Sense Report (Latest Benchmark Data)
{sense}

Analyze the data and propose any needed principle adjustments.
If no changes are needed, return an empty proposals list with a summary explaining why.
"""


def run_claude(prompt: str) -> str:
    """Run Claude Code CLI and return response text."""
    result = subprocess.run(
        ["claude", "-p", prompt, "--output-format", "text"],
        capture_output=True, text=True, timeout=300,
    )
    if result.returncode != 0:
        raise RuntimeError(f"claude CLI failed (exit {result.returncode}): {result.stderr}")
    return result.stdout.strip()


def main():
    if not shutil.which("claude"):
        print("WARNING: claude CLI not found. Generating placeholder proposal.")
        proposal = {
            "schema_version": "1.0",
            "agent": "research",
            "tool": "claude-code-cli",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": "placeholder — install claude CLI to enable",
            "proposals": [],
            "summary": "Claude Code CLI not installed.",
        }
    else:
        try:
            with open(SENSE_REPORT) as f:
                sense_data = f.read()
            with open(PRINCIPLE_METADATA) as f:
                principles_data = f.read()

            prompt = RESEARCH_PROMPT_TEMPLATE.format(
                principles=principles_data,
                sense=sense_data,
            )

            response_text = run_claude(prompt)

            proposal = {
                "schema_version": "1.0",
                "agent": "research",
                "tool": "claude-code-cli",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "raw_response": response_text,
            }

            # Parse YAML from response
            clean = response_text.strip()
            if clean.startswith("```"):
                clean = clean.split("```yaml")[-1].split("```")[0] if "```yaml" in clean else clean.split("```")[1].split("```")[0]
            parsed = yaml.safe_load(clean)
            if isinstance(parsed, dict):
                proposal.update(parsed)

        except Exception as e:
            proposal = {
                "schema_version": "1.0",
                "agent": "research",
                "tool": "claude-code-cli",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "error": str(e),
                "proposals": [],
            }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        yaml.dump(proposal, f, default_flow_style=False, allow_unicode=True)

    print(f"Research proposal generated -> {OUTPUT_PATH}")
    print(f"Proposals: {len(proposal.get('proposals', []))}")


if __name__ == "__main__":
    main()
