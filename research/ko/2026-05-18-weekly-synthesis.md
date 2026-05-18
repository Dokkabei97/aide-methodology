# 주간 신스시스 — 2026-05-18

> **작성 에이전트**: Claude Code on web (claude-opus-4-7), 단일 벤더 초안. Axiom A2 / A4에 따라 다른 벤더 리뷰어를 대기 중.
> **소스 다이제스트**: `evolution/intel/weekly-2026-05-18.md`
> **직전 다이제스트**: `evolution/intel/weekly-2026-05-11.md` — 커밋은 되었으나 신스시스가 수행되지 않음. Anthropic 피드 장애로 누락된 Code w/ Claude 신호를 이번 사이클에서 함께 흡수한다.
> **회고 구간(Lookback)**: 2026-05-12 → 2026-05-18 (UTC), 추가로 2026-05-06 캐리오버 포함.
> **렌즈(Lens)**: *자율 에이전트에게 안전하게 위임할 수 있는 엔지니어링 작업의 양*을 바꾸는 신호 — 일반 AI 뉴스가 아님.

이 노트는 RFC-0003 §4(per-platform scheduling contract)가 요구하는 신스시스 레이어다. Weekly Intel 다이제스트가 원시 신호를 모으면, 이 노트가 그것을 에이전트 주도 개발을 위한 아키텍처 주장으로 변환하고 뒤따르는 방법론 변경을 식별한다. 이번 사이클은 1주 분량의 백로그를 흡수한다. 2026-05-11 다이제스트는 dispatch를 발화했으나 신스시스가 실행되지 않았고, 그 최대 신호인 Code w/ Claude 2026 물결은 Anthropic 피드가 404를 반환하는 탓에 머신 스캔에 전혀 잡히지 않았다. 아래에서 두 가지 모두 정리한다.

## 이번 2주가 뒷받침하는 세 가지 아키텍처 주장

### 주장 1 — 무인(unattended) 루프가 이제 업계 기본값이며, 트리거 계약은 meta-code다

단 2주 만에 모든 프런티어 벤더가 동일한 형태를 출하했다. **내부 루프에 사람이 없는** 에이전트 루프를, 얇은 표면(surface)을 통해 제어하는 형태다.

- Anthropic **Routines** — 매니지드 클라우드에서 무인으로 실행되는 저장된 Claude Code 설정. schedule / webhook / GitHub event로 발화된다.
- OpenAI **Codex mobile** — 휴대폰이 이제 다른 곳에서 실행 중인 에이전트의 *컨트롤 표면(control surface)*이다 (diff 승인, 작업 재지정, 터미널 출력 추적).
- xAI **Grok Build** — 사전 plan-mode 승인 후, 격리된 worktree에서 병렬 subagent 실행.

AIDE는 이를 이미 예측했다. RFC-0003(Distributed Agent-Native Scheduling)은 어떤 벤더도 출하하기 전에 per-platform scheduling contract를 명세했다. 이번 2주는 그 경험적 입증이며, 잠재되어 있던 질문 하나를 시급한 질문으로 격상시킨다. **트리거 정의 그 자체** — schedule 표현식, webhook 필터, GitHub-event 매처, 바인딩된 repository와 connector 집합 — 이 이제 *에이전트가 언제 실행될지*를 결정하는 영속적·실행 가능한 산출물이다. 이는 P10의 모든 기준에서 meta-code다. 버전 관리되고, 동작을 바꾸며, 잘못된 편집은 프로덕션 사고가 된다.

아키텍처적 함의: P10(Meta-Code as First-Class)은 `AGENTS.md` / `CLAUDE.md`뿐 아니라 **트리거/루틴 정의를 명시적으로 포함**하는 것으로 읽혀야 한다. RFC-0003의 per-platform scheduling contract는 이제 화해시켜야 할 세 가지 구체적·상이한 구현(Routines, Codex cloud task, Grok Build worktree)을 갖게 되었다. 이는 신규 수치 트리거가 아니라 기존 RFC의 보강이며, 다음 월간 Evolution Engine 차터를 위해 기록한다.

### 주장 2 — 위임의 구속 제약은 생성 속도가 아니라 검증 용량(verification capacity)이다

이번 사이클의 하중을 지탱하는(load-bearing) 주장이다.

AIDE의 창립 텍스트는 **Context Budget**을 "the primary design constraint"(P1)로 명명한다. 병목이 *에이전트가 올바른 변경을 산출하게 만드는 것*이던 시기에는 옳았다. 이번 2주의 세 가지 독립 신호는 병목이 이동했다고 말한다.

1. **Lars Faye, "Agentic Coding Is a Trap"** (HN/X/Threads에서 바이럴) — 명시적 논지는, 에이전트 출력을 *검증*하는 비용(낯선 코드 읽기, 에이전트의 결정을 재유도하기)이 이제 그것이 대체한 생성 비용을 초과한다는 것이다.
2. **Anthropic CI auto-fix** — 명시된 설계 목표 *"the PR owner never sees a red X"*는 문자 그대로 루프에서 사람의 검증 단계를 제거하는 것이다. 이 기능은 검증이 확장되지 않는 단계이기에 존재한다.
3. **Prime Intellect의 2주 무인 실행** — 에이전트는 수천 스텝을 실행했으나, 사람이 작성한 사전 지식 없이는 연구 방향이 새롭거나 타당한지를 *검증*할 수 없었다. 생성은 무한했고, 판단이 벽이었다.

사람이 내부 루프에 있을 때(`principle-metadata.yaml`의 autonomy L1–L3) 검증 비용은 "review" 안에 숨는다. 사람이 제거되면(L4 "System Architect", L5 "Autonomous Developer" — 그 인간 역할은 이미 *"Output verification only"*로 정의됨) 검증은 더 이상 한 단계가 아니라 **그** 제약이 된다. 에이전트 함대는 어떤 검증 채널(사람이든 에이전트든)이 인증할 수 있는 것보다 훨씬 빠르게 변경을 생성한다. 위임은 에이전트가 코드를 못 써서 실패하는 것이 아니라, 그 코드가 옳다고 감당 가능한 비용으로 확인할 수 있는 것이 아무것도 없어서 실패한다.

아키텍처적 함의: AIDE는 Context Budget과 나란히 **Verification Budget**을 공동 1차 제약(co-primary constraint)으로 둘 필요가 있다 — 자율 루프가 미검증 변경을 얼마나 미결 상태로 둘 수 있는지에 대한 1급 한도, 그리고 위임된 모든 단위가 사람 리뷰어만 해석할 수 있는 산출물이 아니라 *에이전트가 소비 가능한(agent-consumable)* 검증 산출물(머신 검사 가능한 테스트 리포트, 타입이 있는 diff, observability 트레이스)을 방출해야 한다는 구조적 요구다. 이는 진정한 구조적 제안이므로 이번 사이클에 `principle-metadata.yaml` 편집이 아니라 **RFC-0005(draft)**로 출하된다. Axiom A3에 따라 Verification-Budget의 수치 값은 calibration 등급 증거를 요구하며, 이번 2주의 증거는 방향성은 있으나 아직 calibration되지 않았다.

### 주장 3 — 자기수정 에이전트 메모리("Dreaming")는 A1·A5·P9를 상속해야 하는 evolution 루프다

Anthropic의 **Dreaming**은 Managed Agent가 자신의 과거 세션을 검토하고, 영속 메모리를 병합·정리하며, 반복 패턴을 표면화하게 한다 — *가중치 변경 없는 자기개선*이다. Harvey는 작업 완료율 약 6배 상승을 보고했다.

구조적으로 Dreaming은 *에이전트 인스턴스* 규모의 AIDE Evolution Engine이다: sense(orientation) → deliberate(consolidation) → apply(new memory store). AIDE는 이미 그 루프를 통치하는 법을 알고 있으며, 그 거버넌스는 선택지가 아니다.

- **A1(Reversibility)** — 세션 사이에 스스로를 다시 쓰는 메모리 스토어는 명명된 이전 상태로 revert 가능해야 한다. Dreaming의 "메모리가 반영되기 전 검토" 옵션이 바로 AIDE의 reversibility/human-gate 독트린이다. AIDE의 기여는 revert 경로를 선택이 아니라 *의무적이고 명명된* 것으로 만드는 것이다.
- **A5(Self-Observability)** — 모든 consolidation 패스는 `evolution/history/`가 방법론에 대해 하듯, 무엇이 병합·정리되었는지의 감사 추적을 남겨야 한다.
- **P9(Security by Structure)** — 에이전트가 다시 쓰고 다시 읽는 영속 스토어는 새로운 인젝션 표면이다. 오염된 "반복 패턴"은 이후 모든 세션에 걸쳐 살아남는다. 영속 에이전트 메모리는 읽어들일 때 신뢰된 내부 상태가 아니라 신뢰되지 않은 입력으로 취급해야 한다.

아키텍처적 함의: 에이전트 영속 메모리는 meta-code(P10)이며 A1 + A5 + P9의 구조적 보장을 상속해야 한다. 이는 영구(permanent) 원칙들의 보강에 더해 P9 표면을 플래그한 것으로, 여기 기록하고 RFC-0005의 위협 섹션에 접어 넣는다. 메타데이터 변경은 없다.

## 정보가 되었으나 다이얼을 움직이지 않은 신호

- **xAI Grok Build — 네 번째 프런티어 코딩 에이전트 벤더.** Weekly Intel 페처는 Anthropic / OpenAI / Google만 추적한다. xAI는 이제 진지한 agentic CLI를 출하하므로 센서 목록에 추가해야 한다. 이는 또한 *A2/A4 리뷰어 풀을 확장*한다 — Grok 스케줄 에이전트는 AIDE 자체 draft PR에 대한 유효한 다른-벤더 리뷰어다. 센서 유지보수 항목이며 메타데이터 변경이 아니다.
- **Terminal-Bench 2.0 대 SWE-bench Pro 순위 역전.** GPT-5.5가 TB2.0 선두(82.0), Claude Opus 4.7이 SWE-bench Pro 선두(64.3). 동일 모델이 harness가 바뀌면 재정렬된다 — tbench 리더보드 자체가 scaffolding 품질이 점수에 상당히 기여한다고 적시한다. 이는 **구조가 원시 모델 크기를 이긴다**는 AIDE의 핵심 베팅(P3, P8)에 대한 전시(exhibit) 등급 증거다. 전시 등급이지 다이얼을 움직이지는 않는다.
- **SWE-bench Verified 포화.** 2차 트래커는 Verified에서 90% 초과를 보이며, OpenAI는 — 가장 어려운 항목의 결함 테스트를 감사한 후 — Verified를 Pro로 대체·폐기했다. 이는 2026-05-04에 이미 내린 source-tiering 결정(P4-VC1은 Verified가 아니라 공식 SWE-bench Pro에 키를 둠)을 입증한다. 현재 공식 Pro 상위 2위 격차(약 5.7pp)는 15pp 임계값보다 한참 낮으므로 **P4-VC1은 `true`로 유지**되며 P4 트리거는 없다.

## 이번 사이클이 출하하는 것

| 파일 | 변경 | 강제되는 Axiom |
|---|---|---|
| `evolution/intel/weekly-2026-05-18.md` | 큐레이터 편찬 다이제스트; 미신스시스 2026-05-11 캐리오버 흡수 | A5 (영구 감사 추적 + source-health 정직성) |
| `research/en/2026-05-18-weekly-synthesis.md` + `research/ko/…` | 이 신스시스 (CLAUDE.md에 따라 이중 언어) | A4 (단일 벤더 초안, 리뷰어 대기) |
| `evolution/history/2026-05-18-weekly-synthesis.yaml` | 감사 엔트리: 신호 스코어링 + reversal 경로 | A1 (명명된 git revert) + A5 (타임스탬프 + source health) |
| `rfcs/0005-verification-capacity-budget.md` | Draft RFC: Verification Budget을 공동 1차 제약으로 | A3 (구조적 제안; 수치 값은 calibration까지 보류) |
| `rfcs/README.md` | RFC-0005 행 추가 | — |

`principle-metadata.yaml`은 이번 사이클에 **편집하지 않는다**: 어떤 신호도 calibration 등급의 정량 임계값을 산출하지 않았다. 영어 방법론 본문과 그 한국어 미러도 **편집하지 않는다** — RFC-0003 §4.3에 따라 본문 편집은 다른-벤더 에이전트의 연서(countersignature)를 먼저 요구한다. 이번 사이클은 제안하며, 적용하지 않는다.

## 센서 유지보수 (Axiom A5)

Anthropic 피드 장애로 머신 스캔은 그 달 최대의 에이전트 개발 이벤트에 눈이 멀었다. 후속 센서 PR을 위해 두 가지 구체적 보수가 큐에 올라가 있다(방법론 diff의 리뷰 가능성을 유지하기 위해 이 초안에서 분리):

1. `vendor:anthropic/news` 복구 또는 교체 — `https://www.anthropic.com/news/rss.xml` 엔드포인트가 404를 반환한다. 큐레이터는 올바른 대체 URL을 확인하지 못했으며 추측으로 페처에 넣지 않는다.
2. `fetch_vendor_releases.py`에 네 번째 벤더로 **xAI** 추가.

## 리뷰어를 위한 열린 질문

다른-벤더 리뷰 에이전트는 다음을 명시적으로 수용하거나 거부해야 한다.

1. **Verification Budget**은 신규 adaptive 원칙이어야 하는가, 아니면 P5(Test as Specification)와 P7(Deterministic Guardrails)에 추가되는 validity-condition 레이어여야 하는가?
2. CI auto-fix 패턴 — *같은 벤더*가 코드를 생성하고, CI를 실패시키고, 자기 실패를 auto-fix하는 것 — 은 `axiom-gate.yml`이 탐지할 수 있어야 하는 A2(Adversarial Separation) 위반인가? 아니면 CI가 충분히 결정론적인 oracle이어서 fix 루프에는 A2가 적용되지 않는가?
3. autonomy 상한(autonomy_levels의 L4 → L5 전이)은 모델 능력만이 아니라 검증 처리량(verification-throughput) 지표에 명시적으로 게이트되어야 하는가?

이 질문들은 반증 가능한 선택지로 구성되었다 — A3(Empiricism)는 리뷰어의 평결이 선호가 아니라 데이터로 뒷받침될 것을 요구한다.

---

**다음 주간 사이클**: 2026-05-25. CI 머신 sense 패스는 00:00 UTC에 실행되고, 이 큐레이터 세션은 그 후에 실행된다. 이번 주 source health는 **저하(degraded)** 상태였다(Anthropic 벤더 피드 404, xAI 미추적) — 센서 보수 PR은 §센서 유지보수에 따라 별도로 큐에 올라가 있다.
