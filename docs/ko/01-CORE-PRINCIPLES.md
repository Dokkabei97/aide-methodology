# AIDE (Agent-Informed Development Engineering) -- 에이전트 시대의 소프트웨어 개발론 v1.0

**작성**: CTO (20년+ 아키텍처 경험, 3년 AI 에이전트 실전 경험)
**기반**: GPT/Claude/Gemini 3종 딥리서치 + Team Alpha(통합파) 보고서 2종 + Team Beta(급진파) 보고서 1종
**날짜**: 2026-02-18

---

## Part 1: AIDE 핵심 원칙 (10개)

### 원칙 1: Context Budget Principle -- 컨텍스트 예산은 1차 설계 제약이다

> **"메모리가 프로그래밍 언어를 결정했듯, 컨텍스트 윈도우가 아키텍처를 결정한다."**

#### 배경과 근거

3개 연구 보고서 모두 **완전 합의**한 유일한 1순위 원칙이다:
- GPT 보고서: "컨텍스트 예산을 설계 입력으로" (핵심 원칙 2번, P0 요구사항)
- Claude 보고서: "컨텍스트 윈도우는 새로운 CPU"
- Gemini 보고서: "컨텍스트 공학이 새로운 희소 자원"

100만 토큰 컨텍스트 윈도우라 해도 성능이 선형적으로 유지되지 않는다. Chroma의 연구에서 18개 LLM을 측정한 결과, 입력 길이 증가에 따라 성능이 불안정해지며, **Lost in the Middle** 현상으로 중간 위치 정보가 소실된다. 도구 정의만으로도 수만 토큰이 소비되며, 이것이 추론 품질과 비용 모두를 악화시킨다.

#### 구체적 가이드라인

| 항목 | 권장 기준 | 상한 | 근거 |
|------|-----------|------|------|
| 파일 크기 | 200~300줄 | 500줄 | 300줄 = ~5,400토큰, 시스템 프롬프트+대화 이력과 합쳐도 안전 |
| 함수 크기 | 30줄 (파서/정책/래퍼) | 50줄 | 단일 추론 턴에서 완전 이해 가능한 범위 |
| 라인 길이 | 100자 | 120자 | diff 리뷰 편의성 |
| 메타 파일 (CLAUDE.md) | 200줄 | 300줄 | 지시 수 증가 시 이행률 선형 감소 |
| 기능 수정 시 로드 파일 수 | 1~2개 | 3개 | 간접 참조 비용 최소화 |

#### Team Alpha/Beta 토론 과정

이 원칙에 대해서는 **양팀 완전 합의**했다. 유일한 차이는 구현 강도에 있었다:
- **Team Alpha**: "기존 SRP와 응집도 개념의 연장선. 토큰 비용이라는 정량적 근거가 추가되었을 뿐"
- **Team Beta**: "이것이 모든 아키텍처 결정의 출발점. 기능 수정 시 로드 파일 최대 3개, 간접 참조 깊이 최대 1단계"

**CTO 판단**: Team Beta의 구체적 지표(로드 파일 수, 간접 참조 깊이)를 **권장 기준**으로 채택하되, **상한**으로 강제하지는 않는다. 인프라 계층의 DIP 구현 등에서 간접 참조가 2단계까지 필요한 경우가 있기 때문이다.

---

### 원칙 2: Locality of Behavior -- 행위의 지역성이 추상화보다 우선한다

> **"하나의 기능에 관련된 모든 코드는 물리적으로 가까이 위치해야 한다."**

#### 배경과 근거

에이전트가 하나의 기능을 수정하기 위해 8개 파일(Controller, Service, Repository, Entity, DTO, Mapper, Interface, Validator)을 탐색해야 하는 전통적 계층 구조는 컨텍스트 파편화를 유발한다. Factory.ai의 연구는 AI 에이전트가 **multi-hop reasoning**(여러 파일 간 참조를 따라가는 추론)에서 극적으로 성능이 저하됨을 보여준다.

이 원칙은 "관심사의 분리(Separation of Concerns)"를 폐기하는 것이 아니다. **분리의 축을 바꾸는 것**이다:
- 기존: 기술적 역할별 분리 (presentation / business / data)
- AIDE: 기능/도메인별 분리 (user-auth / payment / order)

#### 구체적 가이드라인

```
// AIDE 패턴: Feature-Based 구조
features/
  user-auth/
    types.ts          -- 이 기능 전용 타입/스키마 정의
    logic.ts          -- 순수 함수 비즈니스 로직
    handler.ts        -- HTTP/이벤트 핸들러 (부작용 경계)
    store.ts          -- 데이터 저장소 접근 (부작용 경계)
    user-auth.test.ts -- 이 기능의 모든 테스트
    AGENTS.md         -- 에이전트를 위한 도메인 컨텍스트 (Tier 2)
```

- 각 Feature 디렉토리는 **자가 완결적(Self-Contained)**: 에이전트가 해당 폴더만 읽으면 기능 전체를 파악 가능
- Feature 간 공유 코드는 `shared/`에 두되, **최소한으로 유지**
- Feature 내부에서 논리적 계층(순수 로직 / 부작용 경계)은 파일 단위로 분리

#### Team Alpha/Beta 토론 과정

- **Team Alpha**: "Feature 기반 구조는 Clean Architecture의 Vertical Slice Architecture와 호환 가능. 의존성 규칙은 유지하되 물리적 계층을 축소하면 된다."
- **Team Beta**: "아름다운 추상화보다 뚱뚱한 파일이 낫다. 인터페이스와 구현체를 분리하는 순간 에이전트는 두 파일을 로드해야 한다."

**CTO 판단**: Feature 기반 구조를 **기본으로 채택**한다. Team Alpha가 지적한 대로 이것은 Clean Architecture와 대립하지 않으며, Vertical Slice Architecture의 자연스러운 확장이다. 단, Feature 내부에서 types/logic/handler/store의 파일 분리는 유지한다 -- 하나의 300줄 파일이 모든 것을 담는 것보다 역할별 100줄 파일 3개가 에이전트에게도 더 명확하다. 핵심은 **Feature 경계 밖으로의 간접 참조를 최소화**하는 것이다.

---

### 원칙 3: Functional Core, Structural Shell -- 순수 함수 코어 + 구조적 쉘

> **"비즈니스 로직은 순수 함수로, 부작용은 명시적 경계에서 처리한다."**

#### 배경과 근거

3개 보고서 모두 함수형 패러다임이 AI 에이전트에게 구조적 우위를 가진다는 점에 동의했다:
- **순수 함수**는 입력이 같으면 출력이 항상 같으므로, 에이전트가 함수 블록 하나만으로 완벽한 추론이 가능하다
- **불변 데이터**는 상태 추적 없이 데이터 흐름을 체인 형태로 이해할 수 있게 한다
- **강력한 타입 시스템**은 에이전트의 환각을 컴파일 타임에 차단하는 가드레일 역할을 한다

```typescript
// [1] 데이터: 불변 구조체로 정의
type User = Readonly<{
  id: string
  email: string
  name: string
  role: 'admin' | 'member' | 'viewer'
}>

// [2] 순수 로직: 입력 -> 출력, 부작용 없음
const promote_user_to_admin = (user: User): User => ({
  ...user,
  role: 'admin'
})

// [3] 부작용 경계: 의존성 주입, 명시적 에러 핸들링
const handle_promote_user = async (
  userId: string,
  deps: { db: Database; logger: Logger }
): Promise<Result<User, Error>> => {
  const user = await deps.db.findUser(userId)
  if (!user) return err(new UserNotFoundError(userId))

  const promoted = promote_user_to_admin(user)
  await deps.db.saveUser(promoted)
  deps.logger.info({ event: 'user_promoted', userId })

  return ok(promoted)
}
```

#### 구체적 가이드라인

| 영역 | 권장 패러다임 | 클래스 사용 |
|------|--------------|------------|
| 비즈니스 로직 | 순수 함수 | 금지 |
| 도메인 모델 | 불변 데이터 구조 + 타입 | 불변 Record/Type으로 대체 |
| 인프라/IO 계층 | 함수 우선, 필요 시 클래스 | 허용 (DB 연결, 소켓 등 리소스 관리) |
| 정책/검증 | 함수형 파이프라인 | 금지 |
| 도메인 경계 정의 | DDD Bounded Context (타입 + 함수 조합) | 불요 |

#### Team Alpha/Beta 토론 과정

이 원칙은 양팀 간 **가장 격렬한 논쟁**이 벌어진 지점이다:

- **Team Alpha**: "Functional Core + OOP Shell + DDD. DDD의 Aggregate, Entity, Value Object는 도메인 지식을 구조화하는 데 여전히 유효. 불변으로 구현하되 OOP 개념은 유지해야 한다."
- **Team Beta**: "FP-only. 클래스는 상태를 숨기고 에이전트의 인지 부하를 높인다. 비즈니스 로직에 클래스를 사용하지 말라."

**CTO 판단**: 실질적 차이는 생각보다 작다. 양팀 모두 "비즈니스 로직은 순수 함수, 데이터는 불변"에 동의한다. 차이는 DDD의 Aggregate Root 같은 개념을 클래스로 표현하느냐, 타입+함수 조합으로 표현하느냐에 있다. **AIDE는 타입+함수 조합을 권장**한다. DDD의 도메인 모델링 **개념**(Bounded Context, Aggregate, Value Object)은 보존하되, **구현 방식**은 불변 타입+순수 함수로 전환한다. 이렇게 하면 Alpha의 DDD 가치와 Beta의 FP 가치가 모두 충족된다.

상속은 최대 1단계로 제한하며, 깊은 상속 트리는 어떤 경우에도 허용하지 않는다. Composition over Inheritance는 AI 시대에 더욱 강하게 적용된다.

---

### 원칙 4: Knowledge DRY, Code WET-tolerant -- 지식은 DRY, 코드는 지역성과 트레이드오프

> **"비즈니스 규칙은 반드시 한 곳에. 유틸리티 코드의 중복은 지역성을 위해 허용한다."**

#### 배경과 근거

DRY 원칙의 재해석은 3개 보고서에서 가장 넓은 의견 스펙트럼을 보인 주제다:
- GPT: 구조적 해법(카탈로그화)으로 중복 관리
- Claude: "DRY is not dead but transformed" -- AHA(Avoid Hasty Abstractions) 원칙 적용
- Gemini: WET/DAMP 적극 수용, "5줄짜리 로직이 10곳에 반복되어도 OK"

Claude 보고서가 발견한 자기모순이 핵심이다: "중복 허용 -> AI가 더 많은 코드 생성 -> 컨텍스트 윈도우 초과 -> 결국 DRY 필요." 무한한 중복 허용은 자기 파괴적이다.

#### 구체적 가이드라인

| 수준 | 전략 | 예시 | 중복 허용 한도 |
|------|------|------|---------------|
| **비즈니스 규칙** | 엄격한 DRY | "할인율 계산 공식", "가격 정책" | 0 (반드시 단일 출처) |
| **도메인 타입** | Feature 경계에서 재선언 허용 | 공유 User 타입의 Feature-local subset | 인터페이스로 참조하거나 부분 재선언 |
| **유틸리티 코드** | AHA 원칙 | 이메일 검증, 날짜 포맷 | 2~3곳 중복 허용, 4곳 이상이면 추출 검토 |
| **보일러플레이트** | 구조화된 중복 허용 | try-catch 패턴, 로깅 패턴 | 제한 없음 (패턴 앵커 역할) |

**중복 관리 체계**:
- 의식적 중복(Conscious Duplication): 중복할 때 **그 이유를 주석으로 명시**
- 드리프트 감지: CI에서 에이전트 기반 중복 코드 드리프트 탐지를 자동화
- 정기 리뷰: 분기별로 중복 코드의 일관성을 검증

#### Team Alpha/Beta 토론 과정

- **Team Alpha**: "Knowledge DRY + Code AHA. 중복은 의식적으로 허용하되, 가시적 관리가 전제. Gemini의 '10곳에 5줄 중복도 OK'는 극단적."
- **Team Beta**: "적극적 WET/DAMP. 각 파일의 자가 완결성이 최우선. 추상화를 통한 공유는 간접 참조 비용을 수반하므로 최소화해야."

**CTO 판단**: Team Alpha의 "Knowledge DRY + Code AHA"를 채택한다. 핵심 논거:
1. Beta가 인정하듯 중복 코드의 무한 허용은 결국 컨텍스트 윈도우를 초과시켜 자기 모순에 빠진다
2. 그러나 Alpha도 인정하듯 과도한 추상화(모든 3줄 유틸을 공통 모듈로 추출)는 에이전트에게 해로운 간접 참조를 만든다
3. 따라서 "비즈니스 지식은 DRY, 유틸리티 코드는 AHA 기준으로 의식적 중복 허용"이 균형점이다

---

### 원칙 5: Test as Specification -- 테스트는 사양 언어다

> **"테스트는 검증 도구가 아니라 에이전트에게 의도를 전달하는 사양서다. TDG + PBT + EDD의 삼중 체계를 적용한다."**

#### 배경과 근거

Claude 보고서의 핵심 통찰: "TDD는 AI 시대에 더 중요해진다. 테스트가 prompt engineering이 된다." Matthews & Nagappan의 학술 검증에서도 테스트와 함께 문제를 제시하면 GPT-4와 Llama 3 모두에서 코드 생성 품질이 향상됨을 확인했다.

Property-Based Testing(PBT)의 혁신적 효과 (Claude 보고서):
- TDD 대비 23.1~37.3% 상대 향상
- Hard 태스크에서 직접 코드 생성 1.1% 정확도 vs 속성 검증 생성 48.9% 정확도
- LLM은 정확한 코드보다 **정확성 속성(property)을 정의하는 데 훨씬 뛰어남**

#### 구체적 가이드라인

**삼중 테스트 체계:**

```
                     +------------------+
                     |   Human Review   |  아키텍처, 보안, 도메인 지식
                     +------------------+
                    +--------------------+
                    |  Eval Suites (EDD) |  시나리오/데이터셋 기반 행동 평가
                    +--------------------+
                  +------------------------+
                  | Integration Tests      |  AI 생성 코드의 통합 검증
                  +------------------------+
                +----------------------------+
                | Property-Based Tests (PBT) |  불변 속성 검증
                +----------------------------+
              +--------------------------------+
              | Unit Tests (TDD)               |  결정적 코드: 파서, 정책, 도구 래퍼
              +--------------------------------+
```

| 테스트 유형 | 대상 | 도구 | 작성 주체 |
|-------------|------|------|-----------|
| **Unit (TDD)** | 결정적 코드 -- 파서, 정책, 상태 전이, 도구 래퍼 | Jest/Vitest/pytest | 인간 스펙 -> AI 구현 |
| **PBT** | 비즈니스 불변 속성 -- "총액은 항상 >= 0", "정렬 후 순서 보존" | fast-check/Hypothesis | 인간이 속성 정의, AI가 생성 |
| **Integration** | AI가 생성한 코드의 통합 시나리오 -- Feature 간 연동, 데이터 흐름 검증 | 커스텀 테스트 프레임워크 | AI 생성, 인간 리뷰 |
| **Eval (EDD)** | 모델 출력 품질 -- 정확도, 안전성, 유용성 | 커스텀 eval 프레임워크 | 인간 설계 + 프로덕션 실패 편입 |
| **Security** | AI 생성 코드의 보안 취약점(XSS, SQL Injection, 로직 오류) | OWASP 기반 시나리오 + Security linters | 보안팀 설계, 자동 실행 |

**확인 편향 방지 필수**: AI가 테스트와 구현을 모두 작성할 때 "버그를 검증하는 테스트"가 만들어질 위험이 있다. 테스트 작성과 코드 작성에 **다른 모델을 사용**하거나, **인간이 테스트 사양을 리뷰**해야 한다.

#### Team Alpha/Beta 토론 과정

- **Team Alpha**: "TDG(Test-Driven Generation) + PBT + EDD 확장. TDD를 폐기하지 않고 AI 시대에 맞게 확장."
- **Team Beta**: "이중 체계 -- 결정론적 코드에는 Traditional TDD, 확률적 행동에는 EDD. PBT 적극 도입."

**CTO 판단**: 실질적으로 **거의 동일한 제안**이다. 양팀의 테스트 전략을 합쳐서 위의 삼중 체계를 확정한다. 유일한 차이는 명칭뿐이었다.

---

### 원칙 6: Progressive Disclosure -- 정보의 단계적 공개

> **"에이전트에게 모든 정보를 한꺼번에 주지 말라. 필요할 때 필요한 만큼만 제공하라."**

#### 배경과 근거

GPT 보고서의 스킬 점진적 로딩, Claude 보고서의 3-Tier Progressive Disclosure, Gemini 보고서의 동적 정보 로딩이 모두 같은 원리를 말한다: **운영체제의 가상 메모리처럼, 모든 것을 물리 메모리에 올리지 않고 필요할 때 로드한다.**

#### 구체적 가이드라인

**메타 파일 3-Tier 체계:**

| Tier | 파일 | 역할 | 크기 제한 | 로딩 방식 |
|------|------|------|-----------|-----------|
| **Tier 1: 헌법** | `CLAUDE.md` / `AGENTS.md` (루트) | 프로젝트 정체성, 절대 규칙, 아키텍처 맵 | 300줄 이내 | 항상 로딩 |
| **Tier 2: 지역법** | 하위 디렉토리의 `AGENTS.md` | 컴포넌트별 패턴, 도메인 컨텍스트 | 200줄 이내 | 해당 디렉토리 작업 시 Lazy 로딩 |
| **Tier 3: 기술서** | `.agents/skills/*/SKILL.md` | 절차적 지식, 워크플로 가이드 | YAML frontmatter + 본문 | On-demand 로딩 |

**의존성/라이브러리 정보의 단계적 제공:**

프로젝트에서 사용하는 외부 라이브러리와 내부 공유 모듈의 정보를 에이전트에게 전달할 때도 단계적 접근이 필요하다:

| 단계 | 제공 정보 | 용도 |
|------|-----------|------|
| **요약** | 라이브러리 이름 + 버전 + 한 줄 용도 설명 | 에이전트가 프로젝트 전체 기술 스택을 파악 |
| **API 시그니처** | 사용 중인 함수/타입의 시그니처만 | 에이전트가 해당 라이브러리와 연동하는 코드를 작성할 때 |
| **상세 문서** | 예제 코드, 설정 방법, 주의사항 | 에이전트가 새로운 연동을 구축하거나 트러블슈팅할 때 |

핵심은 "모든 라이브러리의 전체 문서를 컨텍스트에 로드하지 않는 것"이다. 필요한 깊이의 정보만 필요한 시점에 제공하면 컨텍스트 예산을 효율적으로 사용할 수 있다.

#### Team Alpha/Beta 토론 과정

**양팀 완전 합의**. 구현 세부사항도 거의 동일했다. 3-Tier 메타 파일 체계와 단계적 정보 제공 원칙을 결합하여 위 체계를 확정했다.

---

### 원칙 7: Deterministic Guardrails -- 확률적 생성에 결정론적 가드레일

> **"AI 에이전트를 믿되, 검증하라. 그리고 검증은 반드시 결정론적이어야 한다."**

#### 배경과 근거

AI 생성 코드의 보안 실태 (Claude 보고서, Veracode 2025):
- 생성 코드의 **약 45%에 보안 결함** 포함
- 로직 에러 발생률 인간 대비 **1.75배**
- XSS 취약점 **2.74배**
- **모델 크기와 무관** -- 더 똑똑한 모델이 더 안전한 코드를 만드는 것이 아님

이 데이터는 "에이전트에게 '잘 하라'고 프롬프트하는 것"이 불충분함을 명확히 보여준다. 결정론적 도구가 에이전트의 출력을 검증해야 한다.

#### 구체적 가이드라인

```
확률적 생성(AI)  ──→  결정론적 검증  ──→  통과/실패
                        │
                        ├── TypeScript strict mode (타입 검증)
                        ├── ESLint/Prettier (스타일 강제)
                        ├── Zod/io-ts (런타임 타입 검증)
                        ├── Pre-commit hooks (자동 실행)
                        ├── Security linters (보안 검증)
                        └── CI test suite (회귀 방지)
```

**절대 규칙**: "린터가 할 수 있는 일을 프롬프트에 맡기지 말라" (Claude 보고서: "never send an LLM to do a linter's job"). 스타일 강제, 타입 검증, 보안 패턴 탐지는 모두 결정론적 도구에 위임한다.

**Self-Healing Loop** (Gemini 보고서의 Reflexion Pattern):
```
Generate -> Compile/Lint -> Test -> Analyze Errors -> Regenerate -> ...
```

이 루프가 효과적으로 작동하려면 에러 메시지가 **기계 판독 가능한 구조화된 형태(JSON)**로 제공되어야 한다.

#### Team Alpha/Beta 토론 과정

**양팀 완전 합의**. Team Beta가 이 원칙을 가장 강조하며 "나를 믿되 검증하라"는 직관적 표현을 제시했고, Team Alpha도 이에 동의했다.

---

### 원칙 8: Observability as Structure -- 관찰가능성은 구조의 일부

> **"AI가 생성한 코드에는 구조화된 로깅과 트레이싱이 기본 포함되어야 한다. 관찰가능성은 1급 시민이다."**

#### 배경과 근거

3개 보고서 **완전 합의**: AI가 빠르게 생성하는 코드의 "왜 이렇게 동작하는지"를 추적할 수 없으면 운영과 디버깅이 불가능하다. AI 에이전트가 코드를 생성할 때 관찰가능성을 구조적으로 내장하도록 해야 한다.

- GPT 보고서: Observability를 아키텍처의 횡단 관심사로 포함
- Claude 보고서: 트레이싱 기본 ON, 개발 단계부터 trace 필수
- Gemini 보고서: 시맨틱 로깅(JSON-LD) 표준 채택

#### 구체적 가이드라인

```typescript
// 구조화된 로그 포맷 -- AI가 생성하는 모든 코드에 포함되어야 함
type StructuredLog = {
  level: 'info' | 'warning' | 'error' | 'critical'
  timestamp: string       // ISO 8601
  service: string         // 서비스/Feature 식별
  event: string           // 비즈니스 이벤트명
  trace_id: string        // 분산 트레이싱 ID
  span_id: string         // 현재 작업 단위 ID
  data: Record<string, unknown>  // 구조화된 부가 데이터
}

// 사용 예시: 이커머스 결제 처리
const handle_payment = async (
  order_id: string,
  deps: { db: Database; pg: PaymentGateway; logger: Logger }
): Promise<Result<PaymentResult, Error>> => {
  deps.logger.info({
    event: 'payment_initiated',
    data: { order_id }
  })

  const result = await deps.pg.charge(order_id)

  if (result.success) {
    deps.logger.info({
      event: 'payment_completed',
      data: { order_id, transaction_id: result.transaction_id }
    })
  } else {
    deps.logger.error({
      event: 'payment_failed',
      data: { order_id, reason: result.error }
    })
  }

  return result
}
```

**핵심 가이드라인:**
- **분산 트레이싱 기본 적용**: `trace_id` -> `span_id`로 요청 흐름을 추적. OpenTelemetry 등 표준 활용
- **개발 단계부터 기본 ON**: 프로덕션에서만이 아니라 로컬 개발에서도 구조화된 로그 활성화
- **비용/성능 메트릭**: API 응답 시간, DB 쿼리 수, 외부 API 호출 수를 실시간 추적
- **AI 생성 코드의 관찰가능성 필수화**: 에이전트에게 코드를 요청할 때, CLAUDE.md에 "모든 handler에 구조화된 로깅을 포함할 것"을 명시

#### Team Alpha/Beta 토론 과정

**양팀 완전 합의**. 관찰가능성은 소프트웨어 운영의 기본이며, AI가 생성하는 코드에서 더욱 중요해진다는 데 이견이 없었다.

---

### 원칙 9: Security by Structure -- 구조적 보안 검증

> **"AI가 생성한 코드의 45%에 보안 결함이 있다. 보안 검증은 구조적으로 내장되어야 한다."**

#### 배경과 근거

AI가 코드의 주 생산자가 되면서 보안 위협의 양상이 달라졌다. AI 생성 코드 자체의 보안 취약점이 핵심 위협이다:

- Veracode 2025: AI 생성 코드의 약 45%에 보안 결함 포함
- XSS 취약점 인간 대비 2.74배, 로직 에러 1.75배
- 모델 크기와 보안 품질은 비례하지 않음

#### 구체적 가이드라인

**위협-통제 매핑:**

| 위협 | 대표 시나리오 | 방어 지점 | 권장 통제 |
|------|-------------|-----------|-----------|
| SQL Injection | AI가 parameterized query 대신 문자열 결합 생성 | Security linter + Code review | 린터 규칙으로 raw query 사용 탐지, ORM/Query Builder 강제 |
| XSS | AI가 사용자 입력 이스케이프 누락 | Security linter + 템플릿 엔진 | 자동 이스케이프 프레임워크 사용 강제, DOMPurify 등 |
| 로직 오류 | 권한 검증 누락, 경계 조건 미처리 | PBT + Integration test | Property-Based Testing으로 불변 속성 검증 |
| 인증/인가 결함 | AI가 인증 미들웨어 적용을 누락 | 아키텍처 강제 | 인증 미들웨어를 라우터 수준에서 기본 적용, 명시적 opt-out만 허용 |
| 의존성 취약점 | AI가 취약한 버전의 패키지 추가 | SCA (Software Composition Analysis) | npm audit, Snyk 등 자동 스캔 |

**보안 3원칙:**
1. **자동화된 보안 검증**: AI가 생성한 모든 코드에 대해 security linter를 CI에서 자동 실행
2. **보안 리뷰 필수화**: 인증, 결제, 개인정보 관련 코드 변경은 반드시 보안 리뷰를 거침
3. **감사 추적(Audit Trail)**: 민감한 데이터 접근과 상태 변경은 모두 구조화된 로그에 기록

#### Team Alpha/Beta 토론 과정

**양팀 완전 합의**. 보안은 타협의 여지가 없는 영역이다.

---

### 원칙 10: Meta-Code as First-Class -- 메타 코드를 1급 시민으로

> **"AGENTS.md, CLAUDE.md, Skills 파일은 소스 코드와 동등한 엄격도로 버전 관리하고 테스트한다."**

#### 배경과 근거

- AGENTS.md가 **60,000+ 오픈소스 프로젝트**에서 사용 (Linux Foundation 산하 Agentic AI Foundation이 관리)
- 연구에 따르면 프롬프트/컨텍스트가 보존되지 않는 관행이 재현성을 약화시킴
- 메타 파일의 한 줄 변경이 에이전트의 전체 행동을 바꿀 수 있으므로, **코드보다 더 높은 영향력**을 가질 수 있음

#### 구체적 가이드라인

**메타 코드 관리 원칙:**
1. **버전 관리**: Git에서 코드와 동일한 워크플로 -- PR, 코드 리뷰, 변경 로그, 릴리스 태그
2. **변경 시 Eval 실행**: 메타 파일 변경은 CI에서 자동으로 eval suite 실행 (행동 회귀 감지)
3. **크기 감시**: Tier 1 파일이 300줄을 넘으면 CI에서 경고/차단
4. **부정 명령문 활용**: "무엇을 하지 말라"가 종종 더 명확하고 위반 감지가 쉬움
5. **예시 기반 지시**: 추상적 원칙보다 구체적 코드 예시가 에이전트의 출력 품질을 극적으로 높임

**manifest.yaml로 전체 구성 고정:**

```yaml
# manifest.yaml
spec_version: "1.0"
project_name: "my-ecommerce"
project_type: "backend"

tech_stack:
  language: "typescript"
  runtime: "node"
  framework: "express"
  database: "postgresql"
  cache: "redis"

ai_development:
  primary_model: "claude-opus-4-6"
  instruction_files:
    tier1: ["CLAUDE.md", "AGENTS.md"]
    tier2_pattern: "src/features/*/AGENTS.md"

code_standards:
  max_file_lines: 300
  max_function_lines: 50
  paradigm: "functional-core"
  type_strictness: "strict"

testing:
  unit: "vitest"
  property: "fast-check"
  e2e: "playwright"

observability:
  logging: "structured_json"
  tracing: true
```

#### Team Alpha/Beta 토론 과정

**양팀 완전 합의**. Gemini의 "메타 제어 평면(Meta-Control Plane)" 개념을 양팀 모두 수용했다.

---



← Previous: [00-PREFACE](./00-PREFACE.md) | Next: [02-ARCHITECTURE-PATTERNS](./02-ARCHITECTURE-PATTERNS.md) →
