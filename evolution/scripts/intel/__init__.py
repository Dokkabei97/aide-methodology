"""AIDE Weekly Intel Loop — external signal collectors.

Runs every Monday 09:00 KST (00:00 UTC) to scan the outside world for
signals relevant to agent-led development:
  * Vendor releases (Anthropic, OpenAI, Google)
  * Social discourse (HN, tech blogs, X, Threads)
  * Benchmarks (SWE-bench, Terminal-bench, etc.)

Output feeds the monthly Evolution Engine via repository_dispatch when
thresholds are crossed. Purely read-only; no API keys required.
"""
