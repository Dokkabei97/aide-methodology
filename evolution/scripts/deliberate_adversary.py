"""
AIDE Evolution Engine — Phase 2: Adversary Agent (Codex CLI)

The Adversary Agent challenges the Research Agent's proposals.
It looks for weak evidence, potential side effects, and counterarguments.

Runs via: codex --model gpt-5.3-codex-spark xhigh exec "$PROMPT"
Axiom A2: This MUST be a different model/vendor from the Research Agent (Claude).
"""

import os
import subprocess
import shutil
import yaml
from datetime import datetime, timezone

RESEARCH_PROPOSAL = os.environ.get(
    "RESEARCH_PROPOSAL", "evolution/deliberation/research-proposal.yaml"
)
OUTPUT_PATH = os.environ.get(
    "OUTPUT_PATH", "evolution/deliberation/adversary-critique.yaml"
)

ADVERSARY_PROMPT_TEMPLATE = """You are the AIDE Evolution Engine's Adversary Agent.

Your role is to CHALLENGE proposals from the Research Agent. Be skeptical.

For each proposal, evaluate:
1. Is the evidence sufficient and reliable?
2. What side effects could this change cause?
3. Are there counterexamples that weaken the proposal?
4. What risks does this change introduce?
5. Would this change violate any of the 5 Immutable Axioms?

OUTPUT FORMAT: Respond with ONLY a YAML block (no markdown fences), structured as:

critiques:
  - proposal_index: 0
    verdict: "accept"
    evidence_quality: "strong"
    side_effects:
      - "description of side effect"
    counterarguments:
      - "counterargument text"
    risk_assessment: "low"
    suggested_modification: "..."
overall_assessment: "..."

Verdicts: "accept" | "reject" | "modify"
Evidence quality: "strong" | "moderate" | "weak" | "insufficient"

---

## Research Agent's Proposals
{proposal}

Challenge each proposal. Be thorough and skeptical.
"""


def run_codex(prompt: str) -> str:
    """Run Codex CLI and return response text."""
    result = subprocess.run(
        ["codex", "--model", "gpt-5.3-codex-spark", "xhigh", "exec", prompt],
        capture_output=True, text=True, timeout=300,
    )
    if result.returncode != 0:
        raise RuntimeError(f"codex CLI failed (exit {result.returncode}): {result.stderr}")
    return result.stdout.strip()


def main():
    if not shutil.which("codex"):
        print("WARNING: codex CLI not found. Generating placeholder critique.")
        critique = {
            "schema_version": "1.0",
            "agent": "adversary",
            "tool": "codex-cli",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": "placeholder — install codex CLI to enable",
            "critiques": [],
            "overall_assessment": "Codex CLI not installed.",
        }
    else:
        try:
            with open(RESEARCH_PROPOSAL) as f:
                proposal_data = f.read()

            prompt = ADVERSARY_PROMPT_TEMPLATE.format(proposal=proposal_data)
            response_text = run_codex(prompt)

            critique = {
                "schema_version": "1.0",
                "agent": "adversary",
                "tool": "codex-cli",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "raw_response": response_text,
            }

            clean = response_text.strip()
            if clean.startswith("```"):
                clean = clean.split("```yaml")[-1].split("```")[0] if "```yaml" in clean else clean.split("```")[1].split("```")[0]
            parsed = yaml.safe_load(clean)
            if isinstance(parsed, dict):
                critique.update(parsed)

        except Exception as e:
            critique = {
                "schema_version": "1.0",
                "agent": "adversary",
                "tool": "codex-cli",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "error": str(e),
                "critiques": [],
            }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        yaml.dump(critique, f, default_flow_style=False, allow_unicode=True)

    print(f"Adversary critique generated -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
