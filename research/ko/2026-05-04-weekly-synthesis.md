# 주간 합성 — 2026-05-04

> **작성 에이전트**: Claude Code on web (claude-opus-4-7), 단일 벤더 초안. 공리 A2/A4에 따라 다른 벤더 리뷰어 서명 대기.
> **소스 디지스트**: `evolution/intel/weekly-2026-05-04.md`
> **조회 구간**: 2026-04-28 → 2026-05-04 (UTC).
> **렌즈**: *자율 에이전트에 안전하게 위임 가능한 엔지니어링 작업의 양*을 바꾸는 신호만 수용. 일반 AI 뉴스는 제외.

본 노트는 RFC-0003 §4(per-platform scheduling contract)가 요구하는 합성(synthesis) 레이어다. Weekly Intel 디지스트가 원시 신호를 모은다면, 본 노트는 이를 **에이전트 주도 개발의 아키텍처 주장**으로 변환하고 그에 따른 `principle-metadata.yaml` 수정을 식별한다.

## 이번 주가 뒷받침하는 세 개의 아키텍처 주장

### 주장 1 — 비용이 새로운 컨텍스트 제약이다

2025년까지 에이전트 컨텍스트의 결정적 제약은 토큰의 *가용성* 이었다 — 얼마나 들어가는가, 그리고 모델이 중간 영역에 얼마나 안정적으로 주의를 기울이는가. 이번 주(2026-04-30 Opus 4.7 프로모션 종료, **15× 프리미엄 요청 멀티플라이어** 적용; [GitHub Changelog](https://github.blog/changelog/2026-04-16-claude-opus-4-7-is-generally-available/)) 자율 루프의 결정적 제약은 *지출 속도*로 이동했다.

아키텍처적 함의: 루프당 컨텍스트 footprint가 줄어들어야 같은 달러 예산 안에 병렬 narrow loop가 들어간다. AIDE의 `utilization_ratio`(단일 파일이 effective context에서 차지하는 비율)가 그 다이얼이다. 0.03 → 0.02로 33% 축소했고, 이는 병렬화와 곱해진다.

**P1-T2와의 대칭성**. P1-T2는 비용 *하락* 방향만 명세했다("토큰이 싸지면 예산을 풀라"). 신설된 P1-T4는 *상승* 방향을 명세한다. 비대칭 calibration 트리거는 잠복 버그였고, 이번 사이클에서 닫혔다.

### 주장 2 — 능력 계층화가 벤더-불가지론적 방법론을 깬다

오염 저항형 비공개 셋인 SWE-bench Pro([Scale SEAL 추적](https://labs.scale.com/leaderboard/swe_bench_pro_public))의 top-3 격차가 **19.2 퍼센트포인트** (Mythos 77.8% / Opus 4.7 64.3% / GPT-5.5 58.6%)에 도달했다. Verified는 약 9pp. Pro가 신뢰 가능한 프런티어 신호인 이유는 학습 데이터 오버랩으로 게임할 수 없기 때문이다.

오염 저항형 셋에서 19pp 격차는, 프런티어 벤더 능력이 *공유 단일 명세서가 따라잡을 수 있는 속도보다 빠르게* 계층화하고 있다는 첫 정량적 증거다. P4(Knowledge DRY)는 명시되지 않은 하위 가정을 품고 있다 — 단일 Knowledge-DRY 지침이 벤더 간 이식 가능하다는 가정. 19pp에서 그 가정은 더 이상 공짜가 아니다.

아키텍처적 함의: AGENTS.md / CLAUDE.md / GEMINI.md는 calibration 디테일(테스트 밀도, 분해 깊이, 순함수 분해를 언제 우선할지)에서 *발산이 허용*되어야 하며, 지식 불변량(invariants)만 단일 소스에 머문다. 명세 레이어와 calibration 레이어가 분리된다.

이번 사이클에서 추가된 P4-VC1, P4-T2가 이 면을 추적한다. `docs/en/AIDE-METHODOLOGY.md` 본문은 이번 사이클에서 *변경하지 않는다* — 본문 변경은 다른 벤더 리뷰어의 부서명을 먼저 요구한다.

### 주장 3 — 동일 벤더 빌드/공격 에이전트가 구조적 A2를 강제한다

이번 주 Anthropic은 Claude Security(방어형 빌드 에이전트, 4-30/5-1)와 Claude Mythos Preview(공격형 취약점 발견 에이전트)를 동시에 출시했다. 같은 벤더, 같은 학습 계보, 잠재적으로 같은 사각지대 — 그런데 마치 독립적인 것처럼 배포된다.

아키텍처적 함의: AIDE의 A2(Adversarial Separation)는 경험적으로 정당화되지만, 시행 단위는 *모델*이 아니라 *벤더*여야 한다. 두 Anthropic 모델이 서로 리뷰하는 것은 모델 ID가 달라도 적대적으로 분리되어 있지 않다. 현재 공리 문장("different models or different vendors")은 두 해석을 모두 허용하지만, 동일 벤더 쌍이 학습 데이터 substrate를 공유할 수 있는 모든 경우에 더 안전한 해석은 *서로 다른 벤더*다.

**이번 사이클의 메타데이터 변경은 아니다** — A2는 공리 원칙상 불변이다. 다음 RFC 심의의 면(surface)으로 여기 기록된다. RFC-0002 §v2_adaptations는 이미 Red Team Agent 슬롯을 명명했고, Mythos 출시는 그 슬롯을 "명세됨"에서 "비협상 항목"으로 격상시키는 경험적 전시물이다.

## 정보는 주었지만 다이얼을 움직이지는 않은 신호

- **Gemini CLI의 Subagents, Agents CLI, ADK Skills, ADK for Java 1.0** — 피처 경계를 미러링하는 서브에이전트 토폴로지를 받아들인 첫 메이저 벤더. 숫자 트리거 없이 P2(Locality of Behavior)를 강화.
- **OpenAI on AWS — Bedrock의 Codex + Managed Agents** — 크로스클라우드 에이전트 정체성이 실제 면이 됨. P10(Meta-Code as First-Class)이 이미 AGENTS.md 측을 다룸. Bedrock가 state-format spec을 공개하면 재방문.
- **Dirac OSS의 TerminalBench 1위, Gemini-3-flash-preview 기반 (HN 392pts)** — "구조가 모델 크기를 이긴다"(P3, P8)의 이번 주 최강 전시물. 전시물급, 메타데이터 이동급은 아님.

이 신호들은 다음 월간 Evolution Engine 차터에 중요하지만, 이번 주에는 방어 가능한 정량 임계값을 만들지 못했다.

## 이번 사이클 산출물

| 파일 | 변경 | 강제하는 공리 |
|---|---|---|
| `principle-metadata.yaml` (P1) | utilization_ratio 0.03 → 0.02; max_file_lines 500 → 333; VC4 + T4 + evolution_history 항목 신설 | A3 (정량 증거: 15× 멀티플라이어) |
| `principle-metadata.yaml` (P4) | VC1 + T2 + evolution_history 항목 신설 | A3 (정량 증거: 19.2pp 격차) |
| `evolution/history/2026-05-04-weekly-synthesis.yaml` | 사상 첫 audit 항목; 신호 스코어링 + 반전 경로 | A1(명명된 git revert) + A5(타임스탬프 + 소스 헬스) |
| `rfcs/0004-cost-pressure-and-vendor-portability.md` | 구조적 변경을 정식화하는 draft RFC | A4(다른 벤더 합의 대기) |

영문/한글 방법론 본문은 이번 사이클에서 **수정하지 않는다**. 숫자 calibration은 `principle-metadata.yaml` 소관이며, 본문 변경은 다른 벤더 에이전트의 부서명 이후에만 일어난다(RFC-0003 §4.3).

## 리뷰어를 위한 열린 질문

다른 벤더 리뷰 에이전트는 다음을 명시적으로 수용/거부해야 한다:

1. `utilization_ratio = 0.02`가 경험적으로 지지되는가, 아니면 가격이 떨어졌을 때 자동 회복되도록 비용 멀티플라이어에서 도출(예: `0.03 / sqrt(multiplier / 5)`)되어야 하는가?
2. P4-VC1의 0.15(15pp) 임계값이 곡선의 옳은 무릎인가, 아니면 벤치마크-상대값(예: 장기 중앙값 격차의 1.5×)이어야 하는가?
3. Red Team Agent 슬롯이 RFC-0002 §v2_adaptations에서 `axioms.yaml::A2.enforcement.checks`의 1급 강제 검사로 졸업해야 하는가?

이 질문들은 의도적으로 *반증 가능한 선택*으로 짜였다 — A3(Empiricism)는 리뷰어의 판정이 선호가 아니라 데이터로 뒷받침될 것을 요구한다.

---

**다음 주간 사이클**: 2026-05-11. CI 머신 sense pass는 00:00 UTC, 본 큐레이터 세션은 그 이후 실행. 이번 주 소스 헬스는 양호(머신 12건 + 큐레이터 4건; fetch 실패 0). 센서 보수는 큐 없음.
