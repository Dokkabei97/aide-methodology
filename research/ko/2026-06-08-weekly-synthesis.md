# 주간 합성 — 2026-06-08

> **작성 에이전트**: Claude Code on web (claude-opus-4-7), 단일 벤더 초안. 공리 A2/A4에 따라 다른 벤더 리뷰어 서명 대기.
> **소스 디지스트**: `evolution/intel/weekly-2026-05-11.md` → `evolution/intel/weekly-2026-06-01.md` (4주 백로그) + `evolution/intel/weekly-2026-06-08.md`(`aide-weekly-intel.yml` 정기 실행분).
> **조회 구간**: 2026-05-05 → 2026-06-08 (UTC). 직전 합성이 2026-05-04였고 그 사이 4주의 디지스트가 큐레이터 패스 없이 지나갔으므로 조회 구간을 확장.
> **렌즈**: *자율 에이전트에 안전하게 위임 가능한 엔지니어링 작업의 양*을 바꾸는 신호만 수용. 일반 AI 뉴스는 제외.

본 합성 레이어는 RFC-0003 §4(per-platform scheduling) 가 요구하는 계약이다. Weekly Intel Loop는 4주 전부터 오늘 아침까지의 원시 신호를 모았다 — 본 노트는 지속성 있는 신호들을 **에이전트 주도 개발의 아키텍처 주장**으로 변환하고, 그에 따른 `principle-metadata.yaml` 수정을 식별한다.

조회 구간 부연: 2026-05-11 ~ 2026-06-01 디지스트는 매주 `Evolution Engine dispatch: YES`(주당 13~19건 벤더 후보)를 발사했지만 그 기간 동안 큐레이터 세션이 열리지 않았다. 본 합성은 4개의 디지스트를 단일 신호 스트림으로 취급한다 — 아키텍처 주장의 검증 기준은 단일 출시 헤드라인이 아니라 **다수 주차 간 지속성**이다.

## 이번 백로그가 뒷받침하는 세 가지 아키텍처 주장

### 주장 1 — durable 에이전트 컨텍스트가 벤더 table-stakes가 되어가는데, AIDE는 그 원칙적 거점이 없다

신호: 4주간 디지스트 전반에 걸쳐 Google ADK가 같은 아키텍처 프리미티브를 약간씩 다른 프레이밍으로 **세 번** 출하했다:

- 2026-05-11: ["Reduce friction and latency for long-running jobs with Webhooks in Gemini API"](https://blog.google/innovation-and-ai/technology/developers-tools/event-driven-webhooks/) — 단일 요청/응답을 넘어서는 작업의 완료 신호를 이벤트 기반으로.
- 2026-05-18, 2026-05-25, 2026-06-01: ["Build Long-running AI agents that pause, resume, and never lose context with ADK"](https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/) — 세션·크래시·휴먼 승인 사이에서 에이전트 상태의 1급 pause/resume.

같은 구간의 OpenAI 엔터프라이즈 Codex 사례들(Cisco, Endava, Braintrust, Virgin Atlantic, Ramp, Dell, Databricks, NVIDIA, Sea, Singular Bank, Parloa, Simplex, Tax-agents, Warp/GPT-5.5, 그리고 "Work with Codex from anywhere" / "Codex on Windows sandbox" 쌍)은 배포 관점에서 동일한 성질을 보강한다: 엔터프라이즈 에이전트 워크플로우는 더 이상 단일 세션 상호작용이 아니라, 인프라 이벤트를 넘어 살아남는다.

아키텍처적 함의: durable 에이전트 컨텍스트는 이제 모든 프로덕션 에이전트 플랫폼의 구조적 가정인데, **그것을 명명한 AIDE 원칙이 없다**. P3(Functional Core, Structural Shell)는 사이드 이펙트 경계를, P8(Observability)은 감사 추적을, P10(Meta-Code)은 AGENTS.md/CLAUDE.md를 버전 관리되는 설정으로 다룬다 — 하지만 어느 것도 *에이전트 런타임 상태* 자체가 코드와 동일한 엄격성으로 durable·resumable·versioned이어야 한다고 명세하지 않는다. 가장 가까운 기존 표면은 P10의 `manifest.yaml`이지만 이것은 *설정*이지 *런타임 상태*가 아니다.

이는 **RFC 가치가 있는 신호**다. RFC-0005를 열어 durable 에이전트 컨텍스트를 P3 v2_adaptation 또는 새 P10 validity_condition로 부착하는 감시 가능 적응 표면을 제안한다. 이번 사이클에 숫자 변경은 적용하지 않는다. 리뷰어의 역할은 부착 표면을 선택하고 임계값 형식을 수락/거부하는 것이다.

### 주장 2 — 미들웨어/인터셉션이 P8 + P9 강제의 구조적 거점으로 굳어진다

신호: 동일한 4주 구간 동안 Google은 ["Genkit Middleware: Intercept, extend, and harden your agentic apps"](https://developers.googleblog.com/announcing-genkit-middleware-intercept-extend-and-harden-your-agentic-apps/) 를 연속 3개 디지스트(2026-05-18, 2026-05-25, 2026-06-01)에 출하했다. 프레이밍은 세 개의 구조적 동사를 명명한다: *intercept*(관측성), *extend*(합성), *harden*(보안). 그 중 둘은 P8(Observability as Structure)·P9(Security by Structure)에 직접 매핑되지만, AIDE의 현재 문장은 이 원칙들을 *결과*로 기술한다(시스템 구조가 관측되어야 하고, 시스템 구조가 검증되어야 한다) — *거점*(인터셉션 레이어가 이 속성들이 사는 자리다)으로 명명하지는 않는다.

OpenAI의 "Building a safe, effective sandbox to enable Codex on Windows" (2026-05-18) 도 다른 어휘로 같은 아키텍처 선택을 한다 — 에이전트 동작이 *경계*에서 인터셉트·검증·제약되는 구조.

아키텍처적 함의: P8·P9는 공리 원칙상 영속이지만, **그 v2_adaptations 슬롯이 인터셉션 경계를 구조적 거점으로 명명하기에 적합한 자리**다. 이는 구조적 정련이지 숫자 보정이 아니다. 본 노트에 다음 심의 표면으로 기록하고 리뷰어 열린 질문 2로 제기한다.

### 주장 3 — CLI-as-meta-interface 수렴이 안정화됨; P10 표면이 넓어진다

신호: 이번 구간에 네 개 벤더가 "Agents CLI"를 에이전트 메타-설정의 정규 인터페이스로 수렴시켰다:

- Google: ["Agents CLI in Agent Platform: create to production in one CLI"](https://developers.googleblog.com/agents-cli-in-agent-platform-create-to-production-in-one-cli/) (2026-05-11 → 2026-06-01 반복).
- Google: ["An important update: Transitioning Gemini CLI to Antigravity CLI"](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/) (2026-05-25, 2026-06-01 반복) — CLI가 래퍼가 아니라 1급 제품 표면임을 벤더 측이 명시적으로 인정.
- Google: ["Subagents have arrived in Gemini CLI"](https://developers.googleblog.com/subagents-have-arrived-in-gemini-cli/) (2026-05-11, 2026-05-18) — 서브에이전트 토폴로지가 CLI 문법으로 표현됨.
- OpenAI: ["Work with Codex from anywhere"](https://openai.com/index/work-with-codex-from-anywhere) (2026-05-18) — Codex CLI가 크로스 환경 사용으로 정상화.

아키텍처적 함의: P10(Meta-Code as First-Class)는 이미 AGENTS.md/CLAUDE.md/GEMINI.md를 다루지만, *CLI* 자체가 이제 AIDE 의미의 메타-코드다 — 인자 스키마, 훅 표면, 서브에이전트 문법이 에이전트 동작을 실질적으로 바꾸는 설정이다. Antigravity 리브랜드는 CLI 바이너리가 메타-표면임을 벤더 측이 인정한 것이다.

이는 **이번 사이클의 메타데이터 변경은 아니다** — P10은 adaptive이며 보정값(`max_meta_file_lines`)을 움직일 증거가 아직 충분하지 않다. 다음 월간 Evolution Engine 차터의 지지 증거로 기록하고 리뷰어 열린 질문 3으로 제기한다.

## 정보는 주었지만 다이얼을 움직이지는 않은 신호

- **GPT-5.5 출시 파동** (2026-05-11) — Instant + Cyber 변형 + System Card. 능력 이동이지만 이를 반영한 SWE-bench Pro public/private 리더보드는 이번 주 큐레이터 샌드박스에서 도달 불가(아래 source-health). P4-VC1 격차 재확인 불가. **다음 사이클로 연기.**
- **I/O 2026 Gemini 3.5 + Gemini Omni** (2026-05-19, 2026-05-29) — 프런티어 능력 이동이지만 동일하게 오염 저항형 리더보드 delta 도달 불가. **다음 사이클로 연기.**
- **OpenAI Gartner 엔터프라이즈 코딩 에이전트 리더 선정** (2026-05-22) — `principle-metadata.yaml::autonomy_levels`의 L3/L4 자율 수준이 시장에서 정상화되었다는 전시물급 증거. 숫자 다이얼은 움직이지 않음.
- **OpenAI Dell 파트너십(Codex 하이브리드/온프레미스)** (2026-05-18) — AGENTS.md 상태 파일에 대한 새로운 컴플라이언스 표면. Dell이 설정 spec을 공개하면 재방문.
- **Gemini Embedding 2 — Agentic multimodal RAG** (2026-05-11 → 2026-06-01 반복) — 임베디드 동작에서 eval 스위트를 자동 생성하는 P5(Test as Specification) v2_adaptation을 뒷받침. 전시물급, 메타데이터 이동급은 아님.
- **Production-Ready AI Agents: 5 Lessons from Refactoring a Monolith** (반복) — 숫자 트리거 없이 P2(Locality of Behavior)를 강화.

이 신호들은 다음 월간 Evolution Engine 차터에 중요하지만, 이번 사이클에는 방어 가능한 정량 임계값을 만들지 못했다.

## 이번 사이클 산출물

| 파일 | 변경 | 강제하는 공리 |
|---|---|---|
| `research/en/2026-06-08-weekly-synthesis.md` | 본 합성(미큐레이팅 4주 + 2026-06-08) | A5 (감사 추적) |
| `research/ko/2026-06-08-weekly-synthesis.md` | 한글 미러 | A5 + paired-document 규칙 |
| `rfcs/0005-durable-agent-context-as-first-class-surface.md` | durable-context 구조적 표면을 정식화하는 draft RFC | A4 (다른 벤더 합의 대기) |
| `evolution/history/2026-06-08-weekly-synthesis.yaml` | 두 번째 audit 항목; 신호 스코어링 + 반전 경로 | A1(명명된 git revert) + A5(타임스탬프 + 소스 헬스) |
| `rfcs/README.md` | RFC 0005 행 추가 | A5 (감사 표면 인덱스) |

영문/한글 방법론 본문은 이번 사이클에서 **수정하지 않는다**. `principle-metadata.yaml`·`axioms.yaml`도 이번 사이클에서 **수정하지 않는다**. RFC-0003 §4.3에 따라 본문 변경과 숫자 보정은 다른 벤더 리뷰어 부서명 후에만 일어난다. 이번 사이클의 증거는 구조적(다수 주차에 걸친 벤더 신호의 지속성)이며, 적절한 대응은 RFC와 audit 항목을 먼저 안착시킨 뒤 리뷰어가 아래 열린 질문 1의 부착 표면을 수용하면 `principle-metadata.yaml` diff를 다시 여는 것이다.

## 리뷰어를 위한 열린 질문

다른 벤더 리뷰 에이전트는 다음을 명시적으로 수용/거부해야 한다:

1. **durable 에이전트 컨텍스트의 부착 표면**. 이 구조적 속성을 P3 v2_adaptation(durable 런타임 상태를 structural shell의 일부로 취급)으로 부착할 것인가, 아니면 새 P10 validity_condition(durable 상태를 일종의 versioned 메타-코드로 취급)으로 부착할 것인가? RFC-0005는 lighter-touch landing으로 P10을 제안한다.
2. **P8/P9 v2_adaptations의 인터셉션 경계**. 현재 비공식인 P8·P9의 `v2_adaptations` 블록에 구조화된 `interception_layer` 슬롯을 두어, 관측성과 보안 검증이 코드베이스 전반에 흩어지지 않고 에이전트 ↔ 도구 경계에 산다고 명세할 것인가?
3. **CLI를 메타-코드 표면으로**. `manifest.yaml`의 P10 `instruction_files` 슬롯을 넓혀 `cli_meta:`(훅 스크립트, 서브에이전트 문법, 플러그인 매니페스트)를 포함시킬 것인가, 아니면 Google만이 CLI를 메타-표면으로 공식 브랜드한 시점에서 시기상조인가?

이 질문들은 의도적으로 *반증 가능한 선택*으로 짜였다 — A3(Empiricism)는 리뷰어의 판정이 선호가 아니라 데이터로 뒷받침될 것을 요구한다. 각 질문에 관련된 데이터는 RFC-0005 본문에 인용된다.

## 소스 헬스 및 백로그 회계

- 2026-06-08 디지스트, 머신 페치: 큐레이터 샌드박스에서 **0/32 소스 도달**(모두 403 / nitter 도달 불가). 디지스트는 안전상의 이유로 dispatch를 올바르게 억제했다. 프로덕션 `aide-weekly-intel.yml`의 GitHub Actions 러너는 이 네트워크 정책을 공유하지 않으며, 그쪽의 독립 실행이 audit trail에 대한 정규 2026-06-08 디지스트다.
- 2026-05-11 → 2026-06-01 디지스트, 머신 페치: 주당 28/32 도달(Anthropic news/release_notes/eng + OpenAI api_changelog 엔드포인트의 영구적 fetch 오류 4건).
- 이번 사이클 큐레이터 추가 신호: 검토한 네 개 디지스트 외 없음 — 벤더 출시 분량이 충분히 많아 교차 주 일관성 검사(3주 이상 지속)가 커버리지가 아니라 결정적 필터였다.
- 센서 보수 큐: 만성 4xx 엔드포인트 4건(Anthropic news/release_notes/eng + OpenAI api_changelog)이 5주 이상 지속됨. 별도의 유지보수 PR이 canonical RSS / changelog URL을 재발견해야 한다.

---

**다음 주간 사이클**: 2026-06-15. 머신 sense pass는 월 00:00 UTC, 본 큐레이터 세션은 그 이후 실행. 만성 4xx 엔드포인트 4건의 소스 헬스 보수는 RFC-0005 리뷰어 프로토콜이 다루지 않는 유일한 후속 작업으로 큐에 들어간다.
