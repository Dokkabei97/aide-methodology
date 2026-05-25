"""Weekly Intel — Phase G: CHANGELOG.md weekly entry.

Adds a dated bullet under the ``[Unreleased]`` section of ``CHANGELOG.md``
summarizing what this cycle produced (synthesis + optional RFC).

If ``[Unreleased]`` does not yet exist, it is created above the most
recent versioned section. The script is idempotent — re-running it on
the same date will not duplicate the entry.
"""

from __future__ import annotations

import json
import os
import re
from datetime import date


CHANGELOG_PATH = os.environ.get("CHANGELOG_PATH", "CHANGELOG.md")
INTEL_DIR = os.environ.get("INTEL_DIR", "evolution/intel")
RFC_DECISION_FILE = os.path.join(INTEL_DIR, "rfc-decision.json")
DISPATCH_FILE = os.path.join(INTEL_DIR, "dispatch.json")


def _load_json(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f) or {}


def _entry_text(today: str) -> str:
    dispatch = _load_json(DISPATCH_FILE)
    rfc_decision = _load_json(RFC_DECISION_FILE)

    parts = [f"Weekly intel synthesis for {today} drafted (en + ko)"]
    if rfc_decision.get("drafted"):
        rfc_path = rfc_decision.get("rfc_path") or ""
        parts.append(f"RFC #{rfc_decision.get('rfc_number'):04d} drafted at `{rfc_path}` — awaits different-vendor review")
    elif dispatch.get("should_dispatch"):
        parts.append("dispatch fired but evidence below RFC threshold — see synthesis only")
    else:
        parts.append("quiet cycle — no RFC drafted")
    return "- " + "; ".join(parts) + "."


def _ensure_unreleased(text: str, entry: str) -> str:
    """Insert ``entry`` under the [Unreleased] section, creating it if needed."""
    if entry in text:
        return text

    if "## [Unreleased]" in text:
        # Find the Unreleased header and put the entry under its first sub-section.
        pattern = re.compile(r"(## \[Unreleased\][^\n]*\n)((?:###[^\n]*\n)?)", re.MULTILINE)
        m = pattern.search(text)
        if m:
            head, sub = m.group(1), m.group(2)
            if sub:
                # Has a sub-section like "### Added" — append entry inside it.
                inject = f"{head}{sub}{entry}\n"
                return text.replace(m.group(0), inject, 1)
            # No sub-section — create one.
            inject = f"{head}\n### Added\n{entry}\n\n"
            return text.replace(m.group(0), inject, 1)

    # No [Unreleased] section yet. Insert it above the first versioned heading.
    versioned = re.search(r"^## \[\d", text, re.MULTILINE)
    block = f"## [Unreleased]\n\n### Added\n{entry}\n\n"
    if versioned:
        idx = versioned.start()
        return text[:idx] + block + text[idx:]
    # No versioned section either — append at end.
    sep = "" if text.endswith("\n") else "\n"
    return text + sep + "\n" + block


def main() -> None:
    today = date.today().isoformat()
    entry = _entry_text(today)

    if not os.path.exists(CHANGELOG_PATH):
        # Bootstrap a minimal changelog so the entry has a home.
        with open(CHANGELOG_PATH, "w") as f:
            f.write("# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n")

    with open(CHANGELOG_PATH) as f:
        original = f.read()

    updated = _ensure_unreleased(original, entry)
    if updated == original:
        print(f"CHANGELOG entry for {today} already present — no change.")
        return

    with open(CHANGELOG_PATH, "w") as f:
        f.write(updated)
    print(f"CHANGELOG updated: {entry}")


if __name__ == "__main__":
    main()
