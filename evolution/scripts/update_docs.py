"""
AIDE Evolution Engine — Phase 4: Update Methodology Documents

Updates docs/en/AIDE-METHODOLOGY.md and docs/ko/AIDE-METHODOLOGY.md
to reflect principle changes. Both languages updated simultaneously.
"""

import os
import yaml
from datetime import datetime, timezone

PROPOSAL = os.environ.get("PROPOSAL", "evolution/deliberation/final-proposal.yaml")


def main():
    """
    In production, this script:
    1. Reads the final proposal with accepted changes
    2. Identifies which sections of the methodology doc need updates
    3. Uses Claude API to generate updated text for EN and KO simultaneously
    4. Applies changes to both docs/en/ and docs/ko/ versions
    5. Ensures bilingual consistency

    Currently a placeholder that logs what would be updated.
    """
    try:
        with open(PROPOSAL) as f:
            proposal = yaml.safe_load(f) or {}
    except FileNotFoundError:
        print("No proposal file found. Skipping doc update.")
        return

    decisions = proposal.get("decisions", [])
    accepted = [d for d in decisions if d.get("verdict") in ("accept", "modify")]

    if not accepted:
        print("No accepted changes. No doc updates needed.")
        return

    print(f"Doc update needed for {len(accepted)} accepted change(s):")
    for d in accepted:
        print(f"  - Proposal #{d.get('proposal_index')}: {d.get('verdict')}")
        print(f"    Rationale: {d.get('rationale', 'N/A')}")

    print()
    print("NOTE: Full doc update requires ANTHROPIC_API_KEY for bilingual generation.")
    print("Sections that would be updated:")
    print("  - docs/en/AIDE-METHODOLOGY.md (numeric guidelines, specific guidelines tables)")
    print("  - docs/ko/AIDE-METHODOLOGY.md (same sections, Korean)")


if __name__ == "__main__":
    main()
