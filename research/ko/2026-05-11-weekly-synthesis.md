# 주간 합성 — 2026-05-11

> **작성 에이전트**: Claude Code on web (claude-opus-4-7), 단일 벤더 초안. 공리 A2/A4에 따라 다른 벤더 리뷰어를 대기.
> **소스 디제스트**: `evolution/intel/weekly-2026-05-11.md`
> **회상 기간**: 2026-05-05 → 2026-05-11 (UTC).
> **렌즈**: *얼마나 많은 엔지니어링 작업을 자율 에이전트에게 안전하게 위임할 수 있는가*를 바꾸는 신호 — 일반 AI 뉴스가 아님.

이 연구 노트는 RFC-0003 §4(per-platform 스케줄링 계약)가 요구하는 합성 레이어다. 주간 인텔 디제스트가 원시 신호를 모으면, 이 노트가 그것을 에이전트 주도 개발의 아키텍처 주장으로 변환하고 뒤따를 principle-metadata 변경을 식별한다.

## 이번 주가 뒷받침하는 세 가지 아키텍처 주장

### 주장 1 — Verifier Isolation이 공리에서 벤더 프리미티브로 진급했다

AIDE는 16개월간 두 공리를 들고 있었지만, 그 실현은 구현자에게 맡겨져 있었다:
- **A2 (적대적 분리)** — "빌드 에이전트와 리뷰 에이전트는 같은 벤더/훈련 데이터 기반을 공유해서는 안 된다"
- **A4 (단일 권위 부재)** — "단일 에이전트의 판정은 구속력이 없다"

Anthropic Outcomes(이번 주 preview → public beta, [9to5Mac 보도](https://9to5mac.com/2026/05/07/anthropic-updates-claude-managed-agents-with-three-new-features/), [Rick's Cafe AI 아키텍처 분석](https://cafeai.home.blog/2026/05/10/anthropic-shipped-outcomes-and-real-story-is-verification-becoming-a-sku/))은 정확히 그 패턴을 벤더 프리미티브로 출시했다: 별도의 grader 에이전트가 **자체적인 독립 컨텍스트 창**에서 개발자가 제공한 루브릭에 대해 작동 에이전트의 출력을 채점한다. grader는 작동 에이전트의 추론 경로를 알지 못한다 — 이 독립성이 Anthropic이 발표한 **하드 태스크 +10pp 성공률**(`.docx` +8.4%, `.pptx` +10.1%)의 아키텍처적 이유다.

이는 A2/A4의 *대체*가 아니다. grader는 여전히 같은 벤더이므로 AIDE가 요구하는 벤더 단위 A2를 만족하지 않는다. 그러나 이는 같은 원리의 *벤더 내부* 표현이다 — 그리고 이것이 public-beta 프리미티브로 출시된 이상, AIDE 방법론 본문은 feature 설계자가 공리에서 다시 유도하지 않고도 참조할 수 있도록 이 패턴에 이름을 붙여야 한다.

**아키텍처적 함의**: 명명된 구조적 패턴 **Verifier Isolation**을 도입하고, A2 + A4 + P5(Test as Specification) 아래에 둔다. 패턴은 수직으로 합성된다: Verifier Isolation은 태스크 단위의 벤더 내부 검증을 처리하고, A2의 벤더 분리는 RFC 단위의 벤더 간 검증을 처리한다. RFC-0005가 이 제안을 담는다.

### 주장 2 — Subagent topology가 세 frontier 벤더 모두에서 벤더 네이티브 프리미티브가 됐다

이번 주 세 개의 독립적인 벤더 발표가 같은 아키텍처 선택을 했다:
- **Anthropic Multiagent Orchestration** (public beta) — 리드 에이전트가 분해해서 ≤20개 specialist에 병렬 위임, 공유 파일시스템 ([Augment Code 7-frameworks 비교](https://www.augmentcode.com/tools/multi-agent-orchestration-platforms-build-vs-buy)).
- **Gemini CLI Subagents** (이번 주 릴리스에서 `/agents refresh`, Skills install/uninstall 추가) — 각 subagent는 자체 컨텍스트 창, 커스텀 지시, 큐레이트된 도구 ([Gemini CLI changelog](https://geminicli.com/docs/changelogs/), [InfoQ 4월 개요](https://www.infoq.com/news/2026/04/subagents-gemini-cli/)).
- **OpenAI Codex MultiAgentV2** — Codex CLI의 명시적 설정 표면으로 병렬 specialist 에이전트 구성 ([OpenAI Codex changelog](https://developers.openai.com/codex/changelog)).

수렴 자체가 신호다. AIDE의 P2(Locality of Behavior)는 feature 디렉토리 형태(`types.ts`, `logic.ts`, `handler.ts`, `store.ts`, `*.test.ts`, `AGENTS.md`)를 규정하지만, 그 feature가 어떻게 subagent에 매핑되는지는 규정하지 않는다. subagent topology가 이제 세 벤더 모두의 프리미티브가 된 이상, 빠진 연결은 명시적이다: **하나의 feature 디렉토리는 하나의 subagent의 작업 셋에 매핑되어야 한다**. subagent의 큐레이트된 도구는 feature의 `handler.ts` 경계에서 온다. subagent의 시스템 프롬프트는 feature의 `AGENTS.md`에서 온다. 리드 에이전트의 일은 어떤 feature 디렉토리를 깨우고 그 출력을 합성할지 선택하는 것이다.

**아키텍처적 함의**: P2는 영구로 유지된다. RFC-0005는 또한 feature-디렉토리 ↔ subagent 매핑을 명시하는 sub-clause를 추가하므로, AGENTS.md가 한 번 작성되어 Anthropic Multiagent / Gemini CLI Subagents / Codex MultiAgentV2 모두에 동일하게 소비될 수 있다. 이것은 또한 P4-VC1(벤더 이식성) 모니터가 결실을 보는 지점이다 — 통일된 AGENTS.md 형태가 *바로 그* 이식성 표면이다.

### 주장 3 — 에이전트가 호출이 아닌 이벤트 기반 레포 시민이 되고 있다

두 개의 인접한 벤더 릴리스가 "에이전트 = CLI" 멘탈 모델을 무너뜨린다:
- **Claude Code Routines** ([devops.com](https://devops.com/claude-code-routines-anthropics-answer-to-unattended-dev-automation/)) — 트리거에 바인드된 저장된 Claude Code 설정: schedule, API 호출, 또는 **GitHub 이벤트**(PR, push, issue, check_run, workflow_run, discussion, release, merge_queue). 노트북 종료에도 살아남고, Anthropic 클라우드에서 실행.
- **Claude Code Auto Mode** ([InfoQ 심층 분석](https://www.infoq.com/news/2026/05/anthropic-claude-code-auto-mode/)) — 도구 출력(파일 읽기 / shell / 웹 응답)이 시스템 컨텍스트에 들어가기 전에 2단계 분류를 적용하는 계층화된 안전 아키텍처; 적대적으로 보이는 콘텐츠에는 경고가 주입됨.

이 조합은 에이전트가 `pull_request.opened` 이벤트로 깨어나, 구조적 입력 신뢰 경계 아래에서 신뢰할 수 없는 PR 콘텐츠를 검사하고, PR이 명시한 의도에 대해 Verifier Isolation 패스를 실행하고, 판정을 게시할 수 있음을 의미한다 — **게이트된 승인까지 사람이 루프에 없다**. AIDE의 P10(Meta-Code as First-Class)은 현재 AGENTS.md / CLAUDE.md를 설정 아티팩트로만 다룬다. Routines + Auto Mode와 함께라면 Meta-Code는 **Event/Trigger 표면**이 필요하다: 어떤 레포 이벤트가 어떤 에이전트를 깨워야 하는지, 어떤 권한 프로파일이 적용되는지, 어떤 verifier가 결과를 채점하는지.

이는 또한 P9(Security by Structure)를 영구로 유지하는 가장 강력한 exhibit이다. Auto Mode의 2단계 분류는 "확률적 생성에 대한 결정적 가드레일"(P7)의 *벤더 빌트인* 버전이다. 같은 벤더 사이클에서 AIDE의 영구 원칙 두 개가 production-grade 프리미티브로 경험적으로 입증된 것이다.

**아키텍처적 함의**: P9, P7는 영구로 유지된다(이미 그렇게 분류됨 — 이번 주는 재분류가 아니라 확인이다). P10에는 방법론 본문에 Event/Trigger sub-section이 필요하며, RFC-0005 §Detailed Design이 이를 열거한다.

## 정보를 줬지만 이번 사이클에 수치 다이얼을 움직이지 않은 신호들

- **DeepClaude (HN #1, 606pts, 17× 저렴)** — [HN 스레드](https://news.ycombinator.com/item?id=48002136), [GitHub 저장소](https://github.com/aattaran/deepclaude). RFC-0004의 비용압박 + 벤더 이식성 스토리에 대해 그 RFC가 작성된 이래 가장 강력한 경험적 exhibit. Claude Code의 루프와 비-Anthropic 두뇌 사이의 shell-script 얇은 레이어는 P4-VC1 벤더 이식성의 작동 형태다. 이번 사이클에 새 메타데이터 변경이 필요하지는 않으며(RFC-0004가 이미 트리거를 무장), 다음 사이클에 `principle-metadata.yaml::P4.evolution_history`에 후속 노트로 기록한다.
- **Anthropic Dreaming (research preview)** — [VentureBeat](https://venturebeat.com/technology/anthropic-introduces-dreaming-a-system-that-lets-ai-agents-learn-from-their-own-mistakes), [The New Stack](https://thenewstack.io/anthropic-managed-agents-dreaming-outcomes/). 세션 간 학습 아티팩트로서의 평문 playbook은 가중치에 인코딩하지 않고 in-repo 텍스트로 Meta-Code를 유지한다는 AIDE의 선택을 거울처럼 반영한다. P10을 영구로 검증한다. 메타데이터 트리거가 아닌 이유는 research-preview이지 public-beta가 아니기 때문.
- **OpenAI가 SWE-bench Verified 보고를 중단** — 방법론 차원의 신호. AIDE의 `principle-metadata.yaml`은 현재 벤치마크 source-tier를 인코딩하지 않는다; 패턴이 두 사이클간 유지되면 후속 RFC가 필요하다. 트리거가 아니라 심의 후보로 여기 기록.
- **Terminal-Bench 2.0 +13.3pp 스윙 (GPT-5.5 82.7% vs Opus 4.7 69.4%)** — RFC-0004의 P4-VC1 모니터가 이를 잡았으나 정확히 트립하지 **않았다**. Verified / SWE-bench Pro top-3 격차가 15pp 임계 안에 있기 때문. 이는 모니터가 의도대로 작동한 것 — 단일 벤치마크 다이버전스를 무시하고 다중 벤치마크 벤더 lockout에만 반응하도록 보정됨. 변경이 아닌 확인.
- **GPT-5.5 고위험 프롬프트 환각 -52.5%** — 미래 P5 / P9 보정 사이클에서 고위험 태스크 floor 메트릭으로 관련. 현재 임계는 움직이지 않음.
- **Anthropic 10개 Finance Agent 템플릿** — 벤더 배포 AGENTS-형 아티팩트. P10의 "에이전트 설정을 일급 버전 콘텐츠로 다룬다" 입장에 대한 산업 exhibit. 메타데이터 변경 없음.

## 이번 사이클이 출시하는 것

| 파일 | 변경 | 강제되는 공리 |
|---|---|---|
| `evolution/intel/weekly-2026-05-11.md` | 31개 출처 인용된 큐레이터 통합 디제스트; 명시적 머신 소스 헬스 노트; auto-suppress에서 dispatch=YES로 사유와 함께 오버라이드 | A5 (자기관측성 — suppression 이벤트 보존) |
| `evolution/intel/dispatch.json` | `should_dispatch=true`; client_payload가 머신 vs 큐레이터 소스 카운트를 추적하고 RFC + synthesis 경로를 링크 | A5 + A3 (큐레이터 오버라이드는 인용된 증거를 동반) |
| `research/en/2026-05-11-weekly-synthesis.md` | 영문 합성 노트. 세 가지 아키텍처 주장; 메타데이터 트리거 규율 | A4 (단일 벤더; 다른 벤더 리뷰어 대기) |
| `research/ko/2026-05-11-weekly-synthesis.md` | 본 문서 (한국어 미러) | bilingual 계약 |
| `rfcs/0005-verifier-isolation-and-subagent-topology.md` | **Verifier Isolation**을 명명된 패턴으로 도입하고, **Subagent Topology** 매핑(feature-디렉토리 ↔ 벤더 subagent), P10 Meta-Code의 **Event/Trigger 표면**을 추가하는 RFC 초안 | A4 (다른 벤더 합의 대기) |
| `tasks/todo.md` | 이번 주 계획 + 리뷰 요약 | A5 |
| `rfcs/README.md` | 인덱스에 RFC-0005 행 추가 | bookkeeping |

영문 방법론 문서(`docs/en/AIDE-METHODOLOGY.md`)와 한국어 미러는 이번 사이클에 **편집되지 않는다**. 본문 변경은 RFC-0003 §4.3에 따라 다른 벤더 리뷰어 공동서명이 필요하다. `principle-metadata.yaml`도 이번 사이클에 **편집되지 않는다** — RFC-0005는 구조적(명명된 패턴 + Meta-Code 표면 도입)이지 수치적이지 않다. 다음 사이클의 리뷰어가 구조적 변경을 수용하면, principle-metadata 패치(예: P5 아래 `verifier_isolation` 공식 슬롯, P10 아래 `event_trigger_surface` 슬롯 추가)가 뒤따른다.

## 리뷰어를 위한 열린 질문

다른 벤더 리뷰 에이전트는 다음을 명시적으로 수용하거나 거부해야 한다:

1. **"Verifier Isolation"이 적절한 이름인가?** 대안: *Independent Verifier*, *Grader Isolation*, *Adversarial Grader Loop*. 선택된 이름은 grader가 새 컨텍스트 창에서 실행되며 작동 에이전트의 추론 경로를 보지 않는다는 점을 명백히 해야 한다.
2. **feature-디렉토리 ↔ subagent 매핑이 1:1 의무인가, 1:N 허용인가?** 1:N 해석은 한 feature가 sub-task를 위해 병렬 specialist를 spawn할 수 있게 한다(예: 한 feature → 작성 specialist + 테스트 specialist 하나씩). 이는 Anthropic Multiagent Orchestration이 실무에서 채택되는 방식에 더 가깝다.
3. **Event/Trigger 표면이 AGENTS.md의 새 top-level 섹션이어야 하는가, 기존 섹션의 sub-section이어야 하는가?** top-level 섹션은 prose 파싱 없이 `gh` / GitHub Actions 도구로 발견 가능하게 만든다; sub-section은 파일을 짧게 유지한다.
4. **OpenAI가 SWE-bench Verified를 떨어뜨린 것이 지금 벤치마크 source-tier RFC를 정당화하는가, 아니면 두 번째 확인 철수를 기다려야 하는가?** 단일 벤더 철수는 N=1 신호; 두 번째 확인 철수가 noise floor 위로 밀어 올린다.

이들은 의도적으로 falsifiable 선택으로 프레임됐다 — A3(Empiricism)는 리뷰어의 판정이 선호가 아니라 데이터로 뒷받침될 것을 요구한다.

---

**다음 주간 사이클**: 2026-05-18. CI 머신 sense 패스는 00:00 UTC에 실행되고, 큐레이터 세션은 그 후에 실행된다. 이번 런의 source health는 머신-실패 / 큐레이터-인용-31. sandbox-egress 케이스에 대한 sensor 개선은 CI 전용 관심사이며 sensor-level 수정이 필요하지 않다; 파이프라인이 정확히 auto-suppress했고 큐레이터 오버라이드가 문서화된 escape hatch다.
