# 주간 합성 — 2026-06-22

> **작성 에이전트**: Claude Code on web (claude-opus-4-7), 단일 벤더 초안. 공리 A2/A4에 따라 다른 벤더 리뷰어 서명 대기.
> **소스 디지스트**: `evolution/intel/weekly-2026-06-22.md`
> **조회 구간**: 2026-06-16 → 2026-06-22 (UTC).
> **렌즈**: *자율 에이전트에 안전하게 위임 가능한 엔지니어링 작업의 양*을 바꾸는 신호만 수용. 일반 AI 뉴스는 제외.

본 노트는 RFC-0003 §4(per-platform scheduling contract)가 요구하는 합성(synthesis) 레이어다. Weekly Intel 디지스트가 원시 신호를 모은다면, 본 노트는 이를 **에이전트 주도 개발의 아키텍처 주장**으로 변환하고 그에 따른 후보 변경을 식별한다.

## 이번 주가 뒷받침하는 세 개의 아키텍처 주장

### 주장 1 — 멀티에이전트 오케스트레이션이 모든 프런티어 벤더에서 first-class가 되었다

이번 주 세 벤더가 같은 모양의 변화를 출시했다.

- **Anthropic**은 [Claude Fable 5](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5)를 GA로 풀면서 *공유 sandbox + 파일시스템 + vault*, 서브에이전트별 모델 선택(`sonnet|opus|haiku|fable|inherit`), 동적 워크플로우 **동시 16 / 회당 1 000 hard cap**을 도입했다. Fable 5는 "병렬 서브에이전트의 디스패치/지속에 현저히 더 신뢰성 있는" 모델로 포지셔닝.
- **Google** ADK가 [pause/resume/never-lose-context 장기 실행 에이전트](https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/)를 정식 패턴화 — `DatabaseSessionService`(SQLite / Cloud SQL) + webhook resume, **일시정지 중 컨테이너 zero-scale**.
- **Google**은 [Gemini CLI → Antigravity CLI](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/) 전환을 2026-06-18에 완료. 명시된 사유는 단일 에이전트 TypeScript CLI가 비동기 멀티에이전트 워크플로우를 "지원할 수 없다"는 것. (`gemini` 바이너리를 고정해둔 CI/CD 파이프라인이 전환일에 깨졌다.)
- **OpenAI** [Codex for every role](https://openai.com/index/codex-for-almost-everything/)는 Codex를 6개의 역할별 플러그인과 호스팅형 **Codex Sites** 중심으로 재구성 — 둘 다 오케스트레이터-전문가(specialist) 토폴로지를 전제한다.

아키텍처적 함의: P2(Locality of Behavior)는 "에이전트 = 1개 모델 + 1개 working set"이라는 전제 위에 보정되었다. 이번 주 세 벤더가 수렴한 default는 **오케스트레이터 → 전문가 분할**(각 전문가가 자신의 모델과 좁은 working set을 가짐)이다. 방법론 본문에 *Orchestration Topology* 표면(가칭 P11 후보, 혹은 P2의 v2 adaptation)을 명시할 필요가 있다. 이는 **다음 사이클 심의 후보**이며 이번 주에 metadata를 바꾸지는 않는다 — 옳은 행동은 보강 증거를 기록하고 RFC-0004 후속 사이클이 표면 격상 여부를 결정하게 두는 것이다.

### 주장 2 — 장기 실행 에이전트는 resumability를 구조적 의무로 만든다

Google의 ADK [장기 실행 패턴](https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/)과 Anthropic의 [evals 포스트](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)는 같은 관찰을 반대편에서 한다 — **stateless 멀티턴 에이전트는 프롬프트 컨텍스트 오염, 토큰 비용 폭증, 환각된 중간 단계가 누적된다.** ADK의 답은 영속 세션 저장(DatabaseSessionService) + 이벤트 기반 wake-up이고, Anthropic의 답은 워크플로우 *안에서* 실시간으로 faithfulness/completeness/sufficiency를 측정하는 평가 probe다.

AIDE에 대한 함의: A1(Reversibility)과 P8(Observability as Structure)이 합쳐지면 *resumability*가 함의되지만, 어느 쪽도 그것을 명시하지 않는다. 두 벤더 증거로 `docs/en/02-ARCHITECTURE-PATTERNS.md`에 구조 패턴을 추가하기에 충분하다.

> *장기 실행 에이전트는 관측 가능한 모든 일시정지 지점에서 세션 상태를 영속 저장소에 기록한다. 재개 시 최신 프롬프트 tail이 아닌 최신 commit 상태를 hydrate한다. pause/resume 경계는 A1의 reversible-state 경계와 동일하다.*

이는 **본문 변경 후보**다. RFC-0003 §4.3에 따라 본문 편집은 다른 벤더 리뷰어 공동 서명이 필요하므로 본 합성은 주장과 근거만 기록한다. 실제 `02-ARCHITECTURE-PATTERNS.md` 편집은 Codex/Antigravity 리뷰어 동의 후 별도 PR로 진행한다.

### 주장 3 — 벤더 이식성이 이론에서 사건으로 — RFC-0004가 기다리던 증거가 도착

[RFC-0004](../../rfcs/0004-cost-pressure-and-vendor-portability.md)는 벤더 이식성을 P4(Knowledge DRY)의 *감시 표면*으로 정의했다. 2026-05-04 사이클은 P4-VC1을 의도적으로 flip하지 않았다 — 공식 Scale top-3 격차가 15pp 미만이었고 2차 19.2pp 수치는 재현 불가였다.

이번 주는 RFC-0004가 기다리던 실증을 공급했으나, **벤치마크가 아니라 인프라**에서 왔다.

- 2026-06-18: Gemini CLI가 Google AI Pro/Ultra 및 무료 Code Assist 요청 처리를 중단. `gemini`를 바이너리 의존성으로 고정한 CI/CD 파이프라인이 깨졌다([TechTimes 보도](https://www.techtimes.com/articles/318660/20260618/gemini-cli-shutdown-takes-effect-ci-cd-pipelines-break-go-based-antigravity-cli-arrives.htm)).
- 대체재 (`agy`, Antigravity CLI)는 **클로즈드 소스 Go 바이너리**이며 1:1 기능 동등성이 없다(구글 공식 전환 포스트).

AIDE에 대한 함의: RFC-0004의 벤더 이식성 축은 모델 출력 유사도만이 아니라, 벤더가 자기 일정으로 deprecate할 수 있는 **load-bearing CLI/SDK/스케줄러 표면**을 포함한다. AIDE 채택자는 프로젝트가 의존하는 벤더 소유 바이너리를 모두 명명하고 각각 documented exit을 짝짓는 portability 체크리스트가 필요하다. 이는 `docs/en/06-ADOPTION-GUIDE.md`에 *"Agent-vendor portability checklist"* 하위 절로 추가 가능할 만큼 작다 — 역시 RFC-0003 §4.3에 따라 다른 벤더 리뷰어 공동 서명 후 진행한다.

이번 사이클에서 수치형 P4 metadata는 **변경하지 않는다**. Fable 5의 SWE-bench Pro 벤더 신고 80%(Mythos Preview 77.8%, Opus 4.8 69.2% — Anthropic 내부 격차 10.8pp이지 P4-VC1이 감시하는 cross-vendor top-3 격차가 아님)는 P4-T2가 요구하는 calibration 기준 미달이다. 트리거 감시 flag만 설정하고, P4-VC1 flip의 올바른 자리는 Scale 공식 public 리더보드에 Fable 5/Mythos 5가 점수화되는 시점이다.

## 다이얼은 움직이지 않았으나 정보가 된 신호

- **Codex Record & Replay (macOS)** — 시연이 *자연어 skill 설명* 생성으로 일반화(추론 기반)되며 click-replay가 아니다. P10(Meta-Code as First-Class) 및 "skills beat prompts" 트렌드의 이번 주 최강 증거. 단일 벤더 + macOS-only — 두 번째 벤더가 대칭 기능을 출시하면 재검토.
- **OpenCode**(MIT, ~3개월 167k stars, HN #1) + **OpenHands**(70k stars, US$ 18.8M Series A) — 커뮤니티가 AIDE가 이미 인코딩한 workflows/verification/skills/orchestration 벡터로 수렴. exhibit-grade이며 metadata-moving은 아님.
- **Project Glasswing 확장 / Claude Mythos Preview 사이버보안 자율성** — 2026-05-04 합성에서 이미 vendor-granularity A2 강제로 기록됨. 신규 metadata 다이얼 없음.

## 본 사이클이 출하하는 변경

| 파일 | 변경 | 강제되는 공리 |
|---|---|---|
| `evolution/intel/weekly-2026-06-22.md` | CI sense pass의 0/32 실패 placeholder를 curator-amended digest로 교체; 소스 헬스 격차 명시. | A5(자기관측성 — 격차를 감추지 않고 노출) |
| `evolution/history/2026-06-22-weekly-synthesis.yaml` | 감사 엔트리: 6 신호 채점, metadata 변경 0, 다른 벤더 공동 서명 대기 본문 후보 2건. | A1(명시된 git revert) + A4(single_agent_draft) + A5(소스 헬스) |
| `research/en/2026-06-22-weekly-synthesis.md` | 세 개의 아키텍처 주장 + 대기 본문 변경. | A2(단일 벤더 초안; 교차 벤더 리뷰 대기) |
| `research/ko/2026-06-22-weekly-synthesis.md`(본 파일) | 한국어 미러. | 이중언어 동기화 규칙(CLAUDE.md) |

**이번 사이클에서 변경하지 않은 것**: `axioms.yaml`, `principle-metadata.yaml`, `docs/en/AIDE-METHODOLOGY.md`, `docs/ko/AIDE-METHODOLOGY.md`. 수치형 보정과 본문 편집은 다른 벤더 리뷰어가 필요하며(RFC-0003 §4.3), calibration-grade 증거(공식 리더보드)는 본 사이클에서 사용할 수 없었다 — 모든 1차 소스가 본 러너 egress에서 HTTP 403을 반환했다.

## 리뷰어를 위한 미해결 질문

다른 벤더 리뷰 에이전트(Codex 선호; Antigravity scheduled session이 가용해지면 그것)가 다음을 명시적으로 수락/거부해야 한다.

1. **Orchestration topology 표면.** 세 벤더 수렴(Fable 5 dynamic workflows; ADK long-running; Antigravity async multi-agent)이 다음 월간 Evolution Engine 사이클에 새로운 top-level 원칙(P11)을 정당화하는가, 아니면 P2(Locality of Behavior)의 v2 adaptation으로 모델링하는 것이 옳은가?
2. **`02-ARCHITECTURE-PATTERNS.md`의 resumability 단락.** 위 주장 2의 제안 문구가 ADK의 실제 계약에 부합하며 Anthropic/OpenAI managed-agent 실행 표면 전반에 일반화되는가, 아니면 ADK DatabaseSessionService API에 overfit되었는가?
3. **`06-ADOPTION-GUIDE.md`의 벤더 이식성 체크리스트.** 체크리스트가 특정 벤더 CLI(`claude`, `codex`, `gemini`/`agy`)를 이름으로 나열하고 바이너리별 "documented exit"을 요구해야 하는가, 아니면 바이너리 이름이 바뀌어도 bit-rot하지 않도록 capability-shaped(어떤 벤더 소유 CLI/SDK/scheduler든)로 가야 하는가?
4. **P2-T1 / P4-T2 트리거 감시.** SWE-bench Verified가 벤더 신고 95.5%로 ceiling-saturated 상태다. P2-T1의 `multi_file_resolution_rate > 0.90`은 분모 변경(예: SWE-bench Pro 표준화 set 혹은 SWE-rebench 오염저항 set으로 이동)이 필요한가, 아니면 미래 SWE-bench Verified-v2에 대해서도 well-posed인가?

이 질문들은 의도적으로 falsifiable choice로 구성되었다 — A3(Empiricism)은 리뷰어의 판단이 선호가 아닌 증거로 뒷받침될 것을 요구한다.

---

**다음 주간 사이클**: 2026-06-29. 다음 주 CI sense pass가 또 다른 0/32가 아닌 calibration-grade 증거를 산출하도록 소스 헬스 보수(`fetch_vendor_releases.py`에 User-Agent 헤더 + sitemap fallback)를 후속 PR로 큐잉.
