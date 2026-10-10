# 주간 인텔 — 파이프라인 실행 로그

> **카탈로그 전용.** 이 페이지는 AIDE 주간 인텔 파이프라인의 매 실행을 기록합니다.
> AIDE 방법론 본문이 아닙니다. 방법론 본문은 `docs/ko/AIDE-METHODOLOGY.md`이며,
> 변경은 다른 벤더 에이전트의 공동 서명을 거친 RFC 프로세스를 통해서만 가능합니다 (공리 A2 / A4).
>
> 파이프라인 소스: `.github/workflows/aide-weekly-intel.yml`.
> 스케줄: 매주 월요일 00:00 UTC (09:00 KST).

## 월요일 1회 실행이 이 페이지에 반영되는 과정

1. **Phase A–C** — Anthropic / OpenAI / Google 공식 피드, HackerNews, 테크 블로그,
   X (nitter 미러), 그리고 벤치마크 리더보드(SWE-bench, Terminal-bench, WebArena,
   SWE-rebench)를 수집.
2. **Phase D** — 원본 다이제스트를 `evolution/intel/weekly-YYYY-MM-DD.md`로 컴파일하고,
   월간 Evolution Engine 디스패치 여부를 결정.
3. **Phase E** — AIDE 관련성 필터를 통과한 항목이 있으면
   `research/intel/YYYY-MM-DD-weekly-synthesis.md`로 합성 노트 작성.
4. **Phase F** — 고신호 임계(신규 모델/런타임 + 벤더 릴리스 2건 이상, 벤치마크 SOTA
   2.0pp 이상 변동, 또는 HN 바이럴 3건 이상) 시 `rfcs/` 아래 자동 RFC 초안 작성.
5. **Phase G** — 아래에 한 항목 append.

## 실행 기록 (최신순)
