# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2026-06-01

### Added
- Weekly Intel pipeline Phase E/F/G: AIDE-relevance synthesis writer
  (`research/intel/YYYY-MM-DD-weekly-synthesis.md`), conditional auto-draft RFC
  generator (`rfcs/NNNN-weekly-intel-*.md`), and append-only docs catalog
  (`docs/{en,ko}/recent-intel.md`).
- New scripts: `evolution/scripts/intel/synthesize_research_note.py`,
  `draft_rfc_if_threshold.py`, `update_docs_recent_intel.py`.
- All new writes are isolated to safe paths; the methodology body
  (`docs/en/AIDE-METHODOLOGY.md`, `principle-metadata.yaml`, `axioms.yaml`) is
  never touched by the weekly pipeline, preserving Axioms A2 / A4.

## [1.0.0] - 2026-02-18

### Added
- AIDE (Agent-Informed Development Engineering) Methodology v1.0
- 10 Core Principles for agent-era software development
- Full methodology document (English and Korean)
- Research reports from 3 AI models (GPT, Claude, Gemini)
- Team debate reports (Team Alpha and Team Beta)
- Agent-First contribution model
- RFC process for methodology evolution
