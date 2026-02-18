# AIDE (Agent-Informed Development Engineering) -- 에이전트 시대의 소프트웨어 개발론 v1.0

**작성**: CTO (20년+ 아키텍처 경험, 3년 AI 에이전트 실전 경험)
**기반**: GPT/Claude/Gemini 3종 딥리서치 + Team Alpha(통합파) 보고서 2종 + Team Beta(급진파) 보고서 1종
**날짜**: 2026-02-18

---

## Part 4: AIDE 실전 가이드

### 파일/코드 크기 지침

| 구분 | 권장 | 상한 | 토큰 추정 | 비고 |
|------|------|------|-----------|------|
| Feature 로직 (logic.ts) | 150-200줄 | 300줄 | ~5,400 | 핵심 비즈니스 로직 |
| 핸들러 (handler.ts) | 100-150줄 | 200줄 | ~3,600 | 각 핸들러 함수 30줄 이내 |
| 타입 정의 (types.ts) | 50-100줄 | 150줄 | ~2,700 | 타입은 밀도가 높으므로 짧아도 충분 |
| 테스트 (*.test.ts) | 200-300줄 | 500줄 | ~9,000 | 반복 구조이므로 약간 길어도 허용 |
| 메타 파일 (CLAUDE.md) | 100-200줄 | 300줄 | ~5,400 | 지시 이행률 유지를 위한 상한 |
| 도메인 컨텍스트 (AGENTS.md, Tier 2) | 50-100줄 | 200줄 | ~3,600 | 핵심 비즈니스 규칙만 압축 |
| 함수 크기 | 20-30줄 | 50줄 | ~900 | 단일 추론 턴 내 완전 이해 |

**"18토큰/줄" 경험법칙**: 평균적으로 코드 1줄 = 약 18토큰 (Cursor IDE 연구 기반)

### 네이밍 컨벤션 가이드

Gemini 보고서의 **의미론적 장황함(Semantic Verbosity)** 원칙을 적용하되, 실용적 균형을 유지한다:

| 구분 | 컨벤션 | 예시 | 반례 |
|------|--------|------|------|
| 파일명 | kebab-case | `user-auth.ts` | `ua.ts` |
| 함수명 | snake_case, 동사_목적어 | `calculate_order_total_in_krw` | `calc(d)` |
| 타입명 | PascalCase, 명사 | `OrderItem` | `OI` |
| 변수명 | snake_case, 의미 포함 | `active_user_id_list` | `ids` |
| 상수명 | UPPER_SNAKE, 출처 포함 | `MAX_LOGIN_ATTEMPTS_PER_POLICY` | `MAX` |
| 부작용 함수 | 접두사로 부작용 명시 | `persist_user_to_database` | `save` |

**핵심 원칙**: 변수명과 함수명은 에이전트에게 **추론의 입력**이다. 이름이 구체적일수록 에이전트가 잘못 사용할 확률이 기하급수적으로 낮아진다. 단, `calculated_total_price_with_discount_applied_in_krw` 수준의 극단적 장황함은 라인 길이 제한과 충돌하므로 실용적 범위를 유지한다.

### CLAUDE.md 작성 가이드 (템플릿)

```markdown
# Project: [프로젝트명]

## Identity
- Type: [프로젝트 타입, e.g. Next.js 14 Monorepo]
- Language: TypeScript (Strict Mode)
- Paradigm: Functional core, classes only for infrastructure
- State: [상태 관리 도구, e.g. Zustand]

## Absolute Rules (MUST FOLLOW)
- 비즈니스 로직에 class를 사용하지 말 것
- 모든 함수 매개변수와 반환값에 타입을 명시할 것
- any 타입을 사용하지 말 것
- features/ 외부에서 features/ 내부를 직접 import하지 말 것
- 새로운 npm 패키지 추가 전 반드시 확인을 받을 것
- [프로젝트 특화 규칙 추가]

## Architecture Map
features/: 기능별 독립 모듈 (types + logic + handler + store + test)
shared/:   전역 타입, 인프라 클라이언트, 공통 에러 (최소 유지)
evals/:    평가 데이터셋 및 시나리오
.agents/:  스킬 패키지

## Code Style
- 함수명: snake_case, 동사_목적어 형태
- 타입명: PascalCase
- 변수명: snake_case, 의미를 포함
- 파일: kebab-case
- 최대 파일 길이: 300줄 (경고), 500줄 (금지)
- 함수: 50줄 이내

## Workflow
1. types.ts 먼저 정의/수정
2. logic.ts에 순수 함수 구현
3. *.test.ts에 테스트 작성
4. handler.ts에서 부작용 통합
5. 린트 + 테스트 + 타입 체크 통과 확인

## Domain Glossary
- [도메인 용어1]: [정의]
- [도메인 용어2]: [정의]

## Examples
- Good pattern: src/features/user-auth/logic.ts
- Anti-pattern: (해당 없으면 생략)
```

### AGENTS.md 작성 가이드 (Feature Tier 2 템플릿)

```markdown
# [Feature명] Domain Context

## Business Rules
- [규칙 1: 구체적이고 명확하게]
- [규칙 2: 에이전트가 추론할 필요 없이 이해할 수 있게]
- [규칙 3: 예외 케이스도 포함]

## Data Flow
[주요 플로우]: Request -> validate -> [순수 로직] -> [부작용] -> Response

## Known Edge Cases
- [엣지 케이스 1]: [처리 방법]
- [엣지 케이스 2]: [처리 방법]

## Dependencies
- 이 Feature가 의존하는 shared/ 모듈: [목록]
- 이 Feature를 참조하는 다른 Feature: [목록]
```

### Skills 관리 가이드

```
.agents/skills/
  {skill-name}/
    SKILL.md          # YAML frontmatter(이름, 설명, 태그) + 실행 가이드
    scripts/           # 자동화 스크립트 (선택)
    examples/          # 예제 입출력 (선택)
    tests/             # 스킬 검증용 eval 시나리오
```

**SKILL.md 예시:**

```markdown
---
name: add-api-endpoint
description: "새로운 REST API 엔드포인트를 features/ 디렉토리에 추가"
tags: [api, feature, crud]
version: "1.2.0"
---

## Steps
1. features/{feature-name}/ 디렉토리 확인 (없으면 생성)
2. types.ts에 Request/Response 타입 정의
3. logic.ts에 비즈니스 로직 순수 함수 구현
4. handler.ts에 HTTP 핸들러 추가
5. {feature-name}.test.ts에 테스트 추가
6. Tier 2 AGENTS.md에 비즈니스 규칙 문서화
7. 린트 + 테스트 + 타입 체크 실행

## Guardrails
- shared/ 수정 금지 (새 타입이 필요하면 feature 내부에 정의)
- 기존 핸들러의 시그니처 변경 금지
- 테스트 없는 코드 커밋 금지
```

**스킬 로딩 프로토콜:**
1. **Discovery**: SKILL.md의 YAML frontmatter만 읽음 (~50토큰)
2. **Selection**: 태스크와 관련된 스킬 선택
3. **Loading**: 선택된 스킬의 전체 내용을 컨텍스트에 주입
4. **Execution**: 스킬 가이드에 따라 작업 수행
5. **Unloading**: 작업 완료 후 컨텍스트에서 해제

### 테스트 전략 가이드

```mermaid
graph TB
    subgraph TestPyramid["AIDE 테스트 피라미드"]
        HR["Human Review<br/>아키텍처 · 보안 · 도메인 지식"]
        ES["Eval Suites (EDD)<br/>시나리오/데이터셋 기반 행동 평가"]
        IT["Integration Tests<br/>Feature 간 연동 · 데이터 흐름 검증"]
        PBT["Property-Based Tests<br/>불변 속성 검증 (fast-check/Hypothesis)"]
        UT["Unit Tests (TDD)<br/>결정적 코드: 파서 · 정책 · 비즈니스 로직"]
    end

    UT --> PBT --> IT --> ES --> HR

    style UT fill:#4CAF50,color:#fff
    style PBT fill:#8BC34A,color:#fff
    style IT fill:#FFC107,color:#000
    style ES fill:#FF9800,color:#fff
    style HR fill:#F44336,color:#fff
```

**각 레이어별 역할:**

| 레이어 | 빈도 | 실행 시점 | 차단 권한 |
|--------|------|-----------|-----------|
| Unit Tests | 매 커밋 | Pre-commit + CI | 머지 차단 |
| Property-Based | 매 커밋 | CI | 머지 차단 |
| Integration | 매 PR | CI | 머지 차단 |
| Eval Suites | 매 PR + 메타파일 변경 시 | CI | 경고 (임계값 이하 시 차단) |
| Human Review | 매 PR | PR 리뷰 | 머지 차단 |
| Security Tests | 매일 + 메타파일/정책 변경 시 | CI + 정기 실행 | 머지 차단 |

---



← Previous: [03-EXISTING-METHODOLOGIES](./03-EXISTING-METHODOLOGIES.md) | Next: [05-CICD-PIPELINE](./05-CICD-PIPELINE.md) →
