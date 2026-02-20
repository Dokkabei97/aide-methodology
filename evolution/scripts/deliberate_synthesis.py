"""
AIDE Evolution Engine — Phase 2: Synthesis Agent (Gemini CLI)

The Synthesis Agent reviews both the Research Agent's proposals and the
Adversary Agent's critiques, then makes a final consensus decision.

Runs via: gemini -m gemini-3-pro-preview -p "$PROMPT" --output-format stream-json
Axiom A2: This MUST be a different vendor from both Research (Claude) and Adversary (Codex).
Axiom A4: Decision requires that all 3 agents participated.
"""

import json
import os
import subprocess
import shutil
import yaml
from datetime import datetime, timezone

RESEARCH_PROPOSAL = os.environ.get(
    "RESEARCH_PROPOSAL", "evolution/deliberation/research-proposal.yaml"
)
ADVERSARY_CRITIQUE = os.environ.get(
    "ADVERSARY_CRITIQUE", "evolution/deliberation/adversary-critique.yaml"
)
OUTPUT_PATH = os.environ.get(
    "OUTPUT_PATH", "evolution/deliberation/final-proposal.yaml"
)

SYNTHESIS_PROMPT_TEMPLATE = """You are the AIDE Evolution Engine's Synthesis Agent.

You have received:
1. A Research Agent's proposals for principle changes (with evidence)
2. An Adversary Agent's critiques of those proposals

Your role is to make the FINAL decision on each proposal:
- ACCEPT: Evidence is strong, risks are manageable, Adversary's concerns addressed
- REJECT: Evidence is weak, risks too high, or Adversary raised valid fatal concerns
- MODIFY: Accept with modifications addressing Adversary's concerns
- DEFER: Need more data; postpone to next Evolution Engine cycle

RULES:
- You CANNOT override the Immutable Axioms (A1-A5)
- Every decision must cite specific evidence (Axiom A3)
- If in doubt, DEFER — it's better to wait than to make a bad change

OUTPUT FORMAT: Respond with ONLY a YAML block (no markdown fences), structured as:

decisions:
  - proposal_index: 0
    verdict: "accept"
    final_value: 700
    rationale: "..."
    evidence_cited: "..."
consensus_agents:
  - "claude-code (research)"
  - "codex (adversary)"
  - "gemini (synthesis)"
summary: "..."
proceed_to_validation: true

---

## Research Proposals
{proposal}

## Adversary Critiques
{critique}

Make your final decisions on each proposal.
"""


def run_gemini(prompt: str) -> str:
    """Run Gemini CLI and return response text."""
    result = subprocess.run(
        ["gemini", "-m", "gemini-3-pro-preview", "-p", prompt],
        capture_output=True, text=True, timeout=300,
    )
    if result.returncode != 0:
        raise RuntimeError(f"gemini CLI failed (exit {result.returncode}): {result.stderr}")
    return result.stdout.strip()


def parse_gemini_stream_json(output: str) -> str:
    """Parse Gemini stream-json output into plain text."""
    lines = output.strip().split("\n")
    text_parts = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                # Extract text from various possible structures
                text = obj.get("text", obj.get("content", obj.get("message", "")))
                if text:
                    text_parts.append(text)
        except json.JSONDecodeError:
            # Not JSON, treat as plain text
            text_parts.append(line)
    return "\n".join(text_parts) if text_parts else output


def main():
    if not shutil.which("gemini"):
        print("WARNING: gemini CLI not found. Generating placeholder synthesis.")
        synthesis = {
            "schema_version": "1.0",
            "agent": "synthesis",
            "tool": "gemini-cli",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": "placeholder — install gemini CLI to enable",
            "decisions": [],
            "consensus_agents": [],
            "summary": "Gemini CLI not installed.",
            "proceed_to_validation": False,
        }
    else:
        try:
            with open(RESEARCH_PROPOSAL) as f:
                proposal_data = f.read()
            with open(ADVERSARY_CRITIQUE) as f:
                critique_data = f.read()

            prompt = SYNTHESIS_PROMPT_TEMPLATE.format(
                proposal=proposal_data,
                critique=critique_data,
            )
            raw_output = run_gemini(prompt)
            response_text = parse_gemini_stream_json(raw_output)

            synthesis = {
                "schema_version": "1.0",
                "agent": "synthesis",
                "tool": "gemini-cli",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "raw_response": response_text,
            }

            clean = response_text.strip()
            if clean.startswith("```"):
                clean = clean.split("```yaml")[-1].split("```")[0] if "```yaml" in clean else clean.split("```")[1].split("```")[0]
            parsed = yaml.safe_load(clean)
            if isinstance(parsed, dict):
                synthesis.update(parsed)

        except Exception as e:
            synthesis = {
                "schema_version": "1.0",
                "agent": "synthesis",
                "tool": "gemini-cli",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "error": str(e),
                "decisions": [],
                "proceed_to_validation": False,
            }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        yaml.dump(synthesis, f, default_flow_style=False, allow_unicode=True)

    # Write consensus flag if proceeding
    if synthesis.get("proceed_to_validation", False):
        flag_dir = os.path.dirname(OUTPUT_PATH)
        with open(os.path.join(flag_dir, "consensus.flag"), "w") as f:
            f.write(f"Consensus reached at {synthesis['generated_at']}\n")
        print("CONSENSUS REACHED — proceeding to validation")
    else:
        print("NO CONSENSUS — deferring to next cycle")

    print(f"Synthesis decision -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
