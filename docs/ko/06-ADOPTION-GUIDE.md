# AIDE (Agent-Informed Development Engineering) -- 에이전트 시대의 소프트웨어 개발론 v1.0

**작성**: CTO (20년+ 아키텍처 경험, 3년 AI 에이전트 실전 경험)
**기반**: GPT/Claude/Gemini 3종 딥리서치 + Team Alpha(통합파) 보고서 2종 + Team Beta(급진파) 보고서 1종
**날짜**: 2026-02-18

---

## Part 6: AIDE 도입 가이드

### 언제 AIDE를 채택해야 하는가 (결정 매트릭스)

| 프로젝트 특성 | 도입 수준 | 핵심 원칙 |
|-------------|-----------|-----------|
| AI 에이전트가 코드의 주 생산자인 프로젝트 | **전면 도입** | 10개 원칙 모두 |
| AI 보조 개발 + 중간 규모 프로젝트 | **핵심 도입** | 원칙 1(Context Budget), 2(Locality), 5(Test), 7(Guardrails), 10(Meta-Code) |
| 단순 Q&A 챗봇 / LLM 활용 프로젝트 | **부분 도입** | 원칙 7(Guardrails), 8(Observability), 9(Security) |
| 전통적 소프트웨어 (AI 비사용) | **불필요** | 기존 개발론 유지 |

### 새 프로젝트 vs 기존 프로젝트 마이그레이션

#### 새 프로젝트: Clean Start

새 프로젝트는 **처음부터 AIDE 원칙으로 시작**한다:

1. manifest.yaml 정의 (기술 스택, 코드 표준, 테스트 도구)
2. CLAUDE.md + AGENTS.md 작성 (300줄 이내)
3. Feature 기반 디렉토리 구조 설정
4. CI/CD 파이프라인에 Eval + Security Gate 포함
5. 첫 Feature부터 types -> logic -> test -> handler 순서로 개발

#### 기존 프로젝트: 점진적 마이그레이션

기존 프로젝트는 **Feature 단위로 점진적 전환**한다:

1. **Phase 1 (즉시)**: CLAUDE.md + manifest.yaml 추가, CI에 린트/타입체크 강화
2. **Phase 2 (1~2주)**: 새 Feature를 AIDE 구조로 개발 시작 (features/ 디렉토리)
3. **Phase 3 (점진적)**: 기존 코드 수정 시 해당 부분을 Feature 기반으로 리팩토링
4. **Phase 4 (분기별)**: Eval 데이터셋 구축, 보안 게이트 추가
5. **Phase 5 (지속적)**: shared/ 코드 최소화, 계층 구조 단순화

**핵심**: "기존 코드를 한꺼번에 다시 쓰지 않는다." 새 코드와 수정되는 코드만 AIDE 원칙을 적용하면, 시간이 지나면서 자연스럽게 전환된다.

### 체크리스트

#### AIDE 최소 요건 체크리스트

- [ ] **메타 파일**: CLAUDE.md/AGENTS.md 루트에 존재하며 300줄 이내
- [ ] **manifest.yaml**: 기술 스택, 코드 표준, 테스트 설정이 고정되어 있음
- [ ] **Feature 기반 구조**: 기능별 독립 디렉토리 존재
- [ ] **타입 안전성**: TypeScript strict mode 또는 동등한 타입 체크 활성
- [ ] **결정론적 가드레일**: 린터 + 타입 체커 + Pre-commit hook 설정
- [ ] **관찰가능성**: 구조화된 로그 포맷, 트레이싱 활성화
- [ ] **보안 검증**: Security linter 설정, CI에서 자동 실행
- [ ] **테스트**: Unit + PBT 최소, Eval Suite 권장
- [ ] **CI 게이트**: 메타 파일/코드 변경 시 자동 eval 실행

#### AIDE 완전 준수 체크리스트 (위 항목 + 아래 추가)

- [ ] **Eval Flywheel**: 프로덕션 실패가 eval 데이터셋에 자동 편입
- [ ] **보안 게이트**: AI 생성 코드 보안 스캔 + SCA 자동 실행
- [ ] **비용 추적**: 토큰 사용량, API 응답 시간 실시간 모니터링
- [ ] **스킬 패키지**: .agents/skills/ 에 재사용 가능한 스킬 정의
- [ ] **중복 감지**: CI에서 비즈니스 지식 수준 중복 자동 탐지
- [ ] **Human Review PR Contract**: 의도 설명, 작동 증거, 위험 등급, AI 사용 공개

---



← Previous: [05-CICD-PIPELINE](./05-CICD-PIPELINE.md) | Next: [07-DISCUSSION-RECORDS](./07-DISCUSSION-RECORDS.md) →
