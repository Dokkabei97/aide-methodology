"""
AIDE Evolution Engine — Phase 4: Apply Changes

Applies validated principle changes to principle-metadata.yaml.
Records changes in evolution_history for each affected principle.
"""

import os
import yaml
from datetime import datetime, timezone

PROPOSAL = os.environ.get("PROPOSAL", "evolution/deliberation/final-proposal.yaml")
PRINCIPLE_METADATA = os.environ.get("PRINCIPLE_METADATA", "principle-metadata.yaml")


def load_yaml(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def apply_proposal(metadata: dict, proposal: dict) -> dict:
    """Apply accepted proposal changes to principle metadata."""
    decisions = proposal.get("decisions", [])
    proposals = proposal.get("proposals", [])

    changes_applied = 0

    for decision in decisions:
        if decision.get("verdict") not in ("accept", "modify"):
            continue

        idx = decision.get("proposal_index", -1)
        if idx < 0 or idx >= len(proposals):
            continue

        prop = proposals[idx]
        principle_id = prop.get("principle_id", "").lower().replace("p", "")
        field = prop.get("field", "")
        new_value = decision.get("final_value", prop.get("proposed_value"))

        # Find the principle in metadata
        for name, principle in metadata.get("principles", {}).items():
            if principle.get("id", "") == prop.get("principle_id", ""):
                # Update the value
                values = principle.get("current_values", {})
                if field in values:
                    old_value = values[field].get("value")
                    values[field]["value"] = new_value

                    # Record in evolution history
                    history = principle.get("evolution_history", [])
                    history.append({
                        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                        "change": f"{field}: {old_value} -> {new_value}",
                        "evidence": prop.get("evidence", {}),
                        "decided_by": "consensus(claude, gpt, gemini)",
                        "verdict": decision.get("verdict"),
                    })
                    principle["evolution_history"] = history
                    changes_applied += 1

                break

    # Update calibration timestamp
    metadata["last_global_calibration"] = datetime.now(timezone.utc).isoformat()

    return metadata, changes_applied


def main():
    metadata = load_yaml(PRINCIPLE_METADATA)
    proposal = load_yaml(PROPOSAL)

    updated_metadata, count = apply_proposal(metadata, proposal)

    with open(PRINCIPLE_METADATA, "w") as f:
        yaml.dump(updated_metadata, f, default_flow_style=False, allow_unicode=True)

    print(f"Applied {count} change(s) to {PRINCIPLE_METADATA}")


if __name__ == "__main__":
    main()
