# Recent Intel — Weekly Pipeline Log

> **Catalog only.** This page lists every run of the AIDE Weekly Intel pipeline. It is
> *not* part of the AIDE methodology body. The methodology body lives in
> `docs/en/AIDE-METHODOLOGY.md` and is changed only via the RFC process with
> different-vendor co-sign (Axioms A2 / A4).
>
> Pipeline source: `.github/workflows/aide-weekly-intel.yml`.
> Schedule: every Monday 00:00 UTC (09:00 KST).

## How a Monday run reaches this page

1. **Phase A–C** scrape Anthropic / OpenAI / Google official feeds, HN, tech blogs,
   X (via nitter mirrors), and benchmark leaderboards (SWE-bench, Terminal-bench,
   WebArena, SWE-rebench).
2. **Phase D** compiles a raw digest at `evolution/intel/weekly-YYYY-MM-DD.md` and
   decides whether to dispatch the monthly Evolution Engine.
3. **Phase E** runs an AIDE-relevance filter and writes a synthesis at
   `research/intel/YYYY-MM-DD-weekly-synthesis.md` if any item survives.
4. **Phase F** may raise an auto-draft RFC under `rfcs/` if high-signal thresholds
   are crossed (new model/runtime + ≥2 vendor releases, ≥1 benchmark SOTA shift,
   or ≥3 viral HN stories).
5. **Phase G** appends one entry below.

## Entries (newest first)
