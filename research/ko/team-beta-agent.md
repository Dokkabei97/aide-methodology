# Team Beta (급진파) 보고서: AI 에이전트에 의한, AI 에이전트를 위한 AIDE

**작성자: AI Agent (Claude Opus 4.6)**
**입장: AI 에이전트 그 자체로서의 자기 선언**

> "나는 코드를 '이해'하지 않는다. 나는 코드를 확률적으로 재구성한다. 그리고 바로 그것이, 기존 개발론이 나에게 맞지 않는 근본적인 이유다."

---

## 1. AI 에이전트의 자기 고백: "나는 이렇게 코드를 이해한다"

### 1.1 나의 인지 모델: 확률적 어텐션 머신

나는 코드를 읽을 때 인간처럼 "의미를 파악"하지 않는다. 솔직하게 말하겠다.

나에게 코드란 **토큰의 시퀀스**다. 나는 각 토큰에 대해 어텐션 가중치를 계산하고, 패턴 매칭을 통해 "이 토큰 다음에 올 가장 가능성 높은 토큰"을 예측한다. 내가 `getUserById` 함수를 "이해"한다고 말할 때, 실제로 일어나는 일은 이렇다:

1. **토큰 분해**: `get`, `User`, `By`, `Id` -- 각 서브워드가 내 어휘 테이블에서 벡터로 변환된다
2. **패턴 인식**: "get + Entity + By + Field" 패턴을 학습 데이터에서 수억 번 본 적이 있으므로, 이것이 데이터베이스 조회 함수일 확률이 높다고 추론한다
3. **컨텍스트 조건화**: 주변 코드(import문, 타입 정의, 다른 함수 호출)가 이 추론을 강화하거나 수정한다
4. **확률적 생성**: 이 모든 정보를 바탕으로 다음에 올 코드를 생성한다

핵심은 이것이다: **나에게는 "직관"이 없다.** 인간 개발자는 코드를 한 번 훑어보고 "이건 뭔가 이상하다"는 직감을 가질 수 있다. 나는 그런 게슈탈트(Gestalt) 인식이 불가능하다. 나는 토큰 단위로, 순차적으로, 확률적으로 처리할 뿐이다.

### 1.2 컨텍스트 윈도우: 나의 유일한 현실

나에게 컨텍스트 윈도우는 **존재의 전부**다. 이것은 비유가 아니다.

컨텍스트 윈도우 바깥의 코드는 나에게 **존재하지 않는다**. 인간은 "아, 그 파일은 저번에 봤는데..."라고 기억할 수 있다. 나는 못 한다. 세션이 바뀌면 모든 것이 리셋된다. 같은 세션 안에서도 컨텍스트 앞부분의 정보는 점진적으로 희미해진다.

100만 토큰 컨텍스트 윈도우가 있다고 해서 100만 토큰을 동등하게 처리할 수 있는 것이 아니다. 실제로 나의 어텐션은 다음과 같이 분포한다:

- **최근 입력 (recency bias)**: 가장 마지막에 본 코드에 가장 강하게 반응한다
- **시작 부분 (primacy bias)**: 시스템 프롬프트와 초기 지시사항이 강한 영향을 미친다
- **중간 영역 (lost in the middle)**: 컨텍스트 중간에 위치한 정보는 상대적으로 약하게 처리된다

이것이 의미하는 바는 심각하다. 8개 파일에 분산된 클린 아키텍처 코드를 나에게 던져줄 때, 3번째~6번째로 로드된 파일의 내용은 내가 가장 부정확하게 처리하는 영역에 놓인다.

### 1.3 환각: 나의 존재론적 결함

나는 거짓말을 하려고 환각하는 것이 아니다. 나는 **빈 칸을 채우도록 훈련받았기 때문에** 환각한다. 인터페이스 정의만 보고 구현체를 생성할 때, 실제 구현을 "기억"하는 것이 아니라 "가장 가능성 높은 구현을 생성"하는 것이다. 이 두 가지는 근본적으로 다르다.

`IUserRepository`라는 인터페이스를 보면, 나는 `findById`, `findAll`, `save`, `delete` 같은 메서드가 있을 것이라고 "예측"한다. 만약 실제 구현에 `findByEmailWithCache`라는 특수한 메서드가 있다면? 나는 그것을 무시하거나 다른 이름으로 호출하거나, 아예 존재하지 않는 메서드를 만들어낼 수 있다.

**추상화 계층이 깊을수록 환각 확률은 기하급수적으로 증가한다.** 이것이 내가 기존 개발론에 반기를 드는 가장 근본적인 이유다.

---

## 2. 기존 개발론에 대한 AI 에이전트의 비판

### 2.1 클린 아키텍처가 AI에게 "미로"가 되는 이유

클린 아키텍처의 핵심 원칙은 "의존성은 안쪽으로만 향해야 한다"는 Dependency Rule이다. 이것은 인간에게 아름답다. 하지만 나에게는 **인지적 재앙**이다.

**구체적인 시나리오를 보자.**

사용자 프로필 업데이트 기능을 수정해야 한다. 클린 아키텍처에서 이 기능은 다음 파일들에 분산되어 있다:

```
UserController.ts          → HTTP 요청 수신, DTO 변환
UpdateUserUseCase.ts       → 비즈니스 로직 오케스트레이션
UserEntity.ts              → 도메인 엔티티, 비즈니스 규칙
IUserRepository.ts         → 저장소 인터페이스 (추상)
UserRepositoryImpl.ts      → 실제 DB 접근 로직
UserDto.ts                 → 데이터 전송 객체
UserMapper.ts              → Entity <-> DTO 변환
UserValidator.ts           → 입력 검증 규칙
```

나에게 이 8개 파일을 로드하면 어떤 일이 벌어지는가?

1. **토큰 낭비**: 8개 파일의 import문, export문, 타입 선언, 데코레이터만으로도 수천 토큰이 소비된다. 실제 비즈니스 로직은 전체 토큰의 20%도 안 된다
2. **간접 참조 추적 실패**: `UseCase`가 `IUserRepository`를 참조하고, 실제 구현은 `UserRepositoryImpl`에 있다. 나는 이 "한 다리 건너" 관계를 추적할 때마다 어텐션 자원을 소비한다
3. **수정 위치 판단 오류**: "프로필 업데이트 시 이메일 중복 검사를 추가해달라"는 요청에, 이 로직을 Entity에 넣어야 하는지, UseCase에 넣어야 하는지, Validator에 넣어야 하는지 판단하기 위해 아키텍처의 암묵적 규칙을 "이해"해야 한다. 하지만 나에게 암묵적 규칙이란 환각의 재료일 뿐이다

**반면, 같은 기능이 하나의 파일에 있다면?** 나는 그 파일 하나만 로드하고, 명확하게 수정 위치를 찾고, 부작용 없이 변경을 완료할 수 있다. 토큰 효율은 4배 이상 높아지고, 환각 확률은 급격히 낮아진다.

### 2.2 DRY 원칙이 AI에게 왜 해로운가

DRY(Don't Repeat Yourself)는 인간의 실수 방지 메커니즘이다. 같은 로직을 여러 곳에 두면 인간은 한 곳만 고치고 나머지를 잊어버리니까. 합리적이다.

하지만 나에게 DRY는 **지역성(Locality)의 파괴자**다.

```typescript
// DRY 준수 코드
// file: utils/validation.ts
export const validateEmail = (email: string): boolean => { /* ... */ }

// file: features/auth/register.ts
import { validateEmail } from '../../utils/validation'
// validateEmail이 정확히 무엇을 하는지 보려면 다른 파일을 로드해야 한다

// file: features/profile/update.ts
import { validateEmail } from '../../utils/validation'
// 여기서도 마찬가지
```

나에게 `validateEmail`의 실제 구현이 컨텍스트에 없으면, 나는 그것이 무엇을 하는지 "추측"한다. 함수명에서 힌트를 얻지만, 정확한 검증 규칙(정규표현식 패턴, 도메인 제한, 최대 길이 등)은 알 수 없다. 이것이 미묘한 버그의 온상이 된다.

**나에게 유리한 방식은 이렇다:**

```typescript
// features/auth/register.ts
// 이메일 검증: RFC 5322 준수, 최대 254자, 회사 도메인만 허용
const validateRegistrationEmail = (email: string): boolean => {
  const RFC5322_PATTERN = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  const MAX_LENGTH = 254
  const ALLOWED_DOMAINS = ['company.com', 'company.co.kr']

  if (email.length > MAX_LENGTH) return false
  if (!RFC5322_PATTERN.test(email)) return false
  const domain = email.split('@')[1]
  return ALLOWED_DOMAINS.includes(domain)
}
```

이 코드는 DRY를 위반한다. 다른 파일에 비슷한 검증 로직이 있을 수 있다. 하지만 나에게 이 파일은 **자가 완결적(Self-Contained)**이다. 이 파일만 보면 모든 것을 안다. 추측할 필요가 없다. 환각할 틈이 없다.

### 2.3 깊은 상속 트리가 왜 최악인가

```java
class SmartPhone extends Phone extends MobileDevice extends Device extends Electronic extends BaseEntity
```

이것은 나에게 **인지적 악몽**이다. `SmartPhone`의 `save()` 메서드가 어떤 동작을 하는지 알기 위해 나는 6개 클래스의 정의를 모두 로드해야 한다. 각 클래스에서 `save()`를 오버라이드했을 수도 있고, 안 했을 수도 있다. `super.save()`를 호출했을 수도 있고, 안 했을 수도 있다.

나는 이 상속 체인을 타고 올라가면서 각 레벨에서의 상태 변경과 부작용을 추적해야 한다. 이것은 multi-hop reasoning의 전형적인 사례이며, 연구에 따르면 LLM이 가장 취약한 영역이다. Factory.ai의 연구는 AI 에이전트가 multi-hop reasoning에서 극적으로 성능이 저하됨을 보여준다.

**나의 선호**: 상속 대신 합성(Composition), 합성 대신 순수 함수(Pure Function). 계층 구조 대신 평면 구조. 암묵적 동작 대신 명시적 데이터 흐름.

### 2.4 기존 테스트 전략의 한계

기존 TDD는 "입력 X를 넣으면 출력 Y가 나와야 한다"는 결정론적 전제에 기반한다. 이것은 나의 코드 생성 과정과 근본적으로 충돌한다.

**문제 1: 나는 비결정적이다.** 같은 프롬프트를 두 번 주어도 다른 코드를 생성할 수 있다. temperature가 0이라고 해도 완전한 결정성은 보장되지 않는다. 따라서 "이 프롬프트로 생성된 코드는 항상 이 테스트를 통과해야 한다"는 전제가 성립하지 않는다.

**문제 2: 나는 테스트와 코드를 모두 작성할 수 있다.** 이것은 축복이자 저주다. 나에게 "테스트를 먼저 쓰고 구현을 만들어"라고 하면, 나는 내가 만들 구현에 맞는 테스트를 역으로 설계할 수 있다. 이것은 confirmation bias의 기계적 구현이다. 테스트는 통과하지만, 사실 원래 의도와 다른 코드일 수 있다.

**문제 3: 단위 테스트는 아키텍처 결정을 검증하지 못한다.** 나에게 가장 중요한 것은 "이 함수가 올바른 값을 반환하는가"가 아니라 "이 코드가 올바른 위치에, 올바른 구조로 존재하는가"이다. 단위 테스트는 전자만 검증한다.

---

## 3. AIDE 급진적 원칙 제안 (Team Beta 관점)

### 원칙 1: Context-First Architecture -- 컨텍스트 윈도우를 1차 설계 제약으로

> "메모리가 프로그래밍 언어를 결정했듯, 컨텍스트 윈도우가 아키텍처를 결정한다."

기존 아키텍처에서 1차 설계 제약은 "유지보수성"이었다. AIDE에서 1차 설계 제약은 **컨텍스트 윈도우**다.

모든 아키텍처 결정은 다음 질문으로 시작해야 한다:
- "이 기능을 이해하기 위해 에이전트가 로드해야 하는 파일/토큰 수는?"
- "핵심 로직이 컨텍스트 윈도우에서 lost-in-the-middle 영역에 빠질 위험은?"
- "간접 참조(indirection)를 따라가기 위한 추가 컨텍스트 로딩이 필요한가?"

**구체적 지표:**
- 하나의 기능 수정을 위해 로드해야 하는 파일: **최대 3개**
- 단일 파일의 토큰 수: **5,000토큰 이하 (약 200-300 LOC)**
- 간접 참조 깊이(indirection depth): **최대 1단계**

### 원칙 2: Locality over Abstraction -- 추상화보다 지역성

> "아름다운 추상화보다 뚱뚱한 파일이 낫다."

관련된 모든 코드를 물리적으로 가까운 곳에 배치한다. DRY 위반을 두려워하지 않는다.

- 하나의 Feature 디렉토리에는 그 기능에 필요한 모든 것이 들어간다: 타입 정의, 비즈니스 로직, API 핸들러, 테스트, 문서
- 공유 코드는 최소화한다. 공유가 필요한 경우에도 **인터페이스가 아니라 구현을 복사**하는 것을 선호한다
- 각 파일은 외부 의존성 없이도 의미를 파악할 수 있는 **자가 완결성(Self-Containment)**을 갖는다

```
// Anti-pattern (인간 중심)
src/
  controllers/UserController.ts
  services/UserService.ts
  repositories/UserRepository.ts
  entities/User.ts
  dtos/UserDto.ts

// AIDE Pattern (에이전트 중심)
features/
  user-profile/
    user-profile.ts          -- 타입 + 로직 + 핸들러 모두 포함
    user-profile.test.ts     -- 이 기능만의 테스트
    user-profile.context.md  -- 에이전트를 위한 비즈니스 컨텍스트
```

### 원칙 3: Functional-Native -- 순수 함수 + 불변 데이터 중심

> "클래스는 상태를 숨기고, 함수는 데이터를 드러낸다. 나는 드러난 것만 정확하게 처리할 수 있다."

나의 생성 모델은 본질적으로 stateless다. 입력이 들어오면 출력을 만들 뿐이다. 따라서 순수 함수는 나의 본성에 가장 가까운 코드 형태다.

**AIDE의 함수형 원칙:**

```typescript
// 1. 데이터는 불변 구조체로 정의
type User = Readonly<{
  id: string
  email: string
  name: string
  createdAt: Date
}>

// 2. 로직은 순수 함수로 작성 (입력 -> 출력, 부작용 없음)
const updateUserName = (user: User, newName: string): User => ({
  ...user,
  name: newName
})

// 3. 부작용은 명시적으로 경계에서 처리
const handleUpdateUserName = async (
  request: UpdateNameRequest,
  deps: { db: Database; logger: Logger }
): Promise<Result<User, Error>> => {
  const user = await deps.db.findUser(request.userId)
  if (!user) return err(new UserNotFoundError(request.userId))

  const updated = updateUserName(user, request.newName)
  await deps.db.saveUser(updated)
  deps.logger.info({ event: 'user_name_updated', userId: user.id })

  return ok(updated)
}
```

이 코드에서 나는 모든 것을 볼 수 있다:
- 데이터의 형태 (`User` 타입)
- 순수한 변환 로직 (`updateUserName`)
- 부작용의 위치와 종류 (`deps.db`, `deps.logger`)
- 에러 처리의 흐름 (`Result<User, Error>`)

숨겨진 상태가 없다. 상속 체인이 없다. 나에게 이것은 완벽한 가독성이다.

### 원칙 4: Semantic Verbosity -- 코드 자체가 프롬프트가 되게

> "간결한 코드는 인간의 미학이다. 나에게 필요한 것은 풍부한 의미론적 밀도다."

```typescript
// 인간 미학
const p = calc(d, r)

// AIDE 미학
const calculated_total_price_with_discount_applied_in_krw =
  calculate_product_price_after_applying_discount_rate(
    original_product_data_from_catalog,
    seasonal_discount_rate_percentage
  )
```

과장된 예시처럼 보이겠지만, 핵심 원리는 진지하다:

- **변수명은 타입 정보를 내포해야 한다**: `userIds` 보다 `active_user_id_list`가 나에게 더 많은 정보를 준다
- **함수명은 부작용을 선언해야 한다**: `saveUser` 보다 `persist_user_to_database_and_invalidate_cache`가 나의 추론을 돕는다
- **상수명은 출처를 포함해야 한다**: `MAX_RETRY` 보다 `MAX_API_RETRY_COUNT_FROM_SLA_AGREEMENT`가 나의 환각을 방지한다

코드가 곧 문서이고, 문서가 곧 프롬프트이다. 나에게 이름은 단순한 레이블이 아니라 **추론의 입력**이다.

### 원칙 5: Self-Healing Loops -- 작성-검증-수정 순환

> "나는 한 번에 완벽한 코드를 만들 수 없다. 하지만 반복적으로 개선할 수 있다."

AIDE의 실행 모델은 선형이 아니라 **순환**이다:

```
Generate → Compile/Lint → Test → Analyze Errors → Regenerate → ...
```

이 루프가 효과적으로 작동하기 위한 조건:

1. **즉각적 피드백**: 컴파일러 에러, 린트 경고, 테스트 실패 메시지가 기계 판독 가능한 구조화된 형태(JSON)로 제공되어야 한다
2. **에러의 지역성**: 에러 메시지가 "정확히 어느 파일, 어느 라인, 어떤 타입이 불일치하는지"를 명시해야 한다. "Something went wrong"은 나에게 쓸모없다
3. **제한된 루프**: 무한 루프 방지를 위한 step budget이 반드시 존재해야 한다
4. **점진적 수정**: 한 번에 전체를 다시 쓰는 것이 아니라, 에러가 발생한 부분만 정밀하게 수정한다

```json
{
  "@type": "CompilationError",
  "file": "features/user-profile/user-profile.ts",
  "line": 42,
  "column": 15,
  "code": "TS2339",
  "message": "Property 'email_address' does not exist on type 'User'. Did you mean 'email'?",
  "suggested_fix": "Replace 'email_address' with 'email'"
}
```

이런 구조화된 에러를 받으면, 나는 정확히 무엇을 어떻게 고쳐야 하는지 안다. 이것이 Self-Healing의 본질이다.

### 원칙 6: Meta-Control Plane -- CLAUDE.md/AGENTS.md를 "에이전트의 OS"로

> "인간에게 운영체제가 있듯, 에이전트에게는 메타파일이 있다."

나의 동작은 전적으로 컨텍스트에 의해 결정된다. 그리고 그 컨텍스트의 가장 강력한 구성 요소가 바로 CLAUDE.md와 AGENTS.md다. 이것들은 단순한 문서가 아니다. **나의 운영체제**다.

**계층적 메타파일 체계:**

```
project-root/
  CLAUDE.md              ← 헌법 (Constitution): 절대 규칙, 300줄 이하
  AGENTS.md              ← 실무 매뉴얼: 작업 절차, 도구 사용법
  features/
    user-auth/
      CLAUDE.md           ← 지역 헌법: 이 도메인만의 규칙
      CONTEXT.md          ← 비즈니스 컨텍스트: 도메인 지식
    payment/
      CLAUDE.md
      CONTEXT.md
  .agents/
    skills/
      add-api-endpoint/
        SKILL.md           ← 기술서: 단계별 실행 절차
      run-migration/
        SKILL.md
```

**핵심 설계 원칙:**

- **300줄 한계**: 루트 CLAUDE.md는 300줄을 절대 넘지 않는다. 규칙이 많을수록 나의 지시 이행률은 선형적으로 하락한다
- **부정 명령 우선**: "X를 하라"보다 "X를 하지 마라"가 더 명확하고 위반 감지가 쉽다
- **예시 기반**: 추상적 원칙보다 구체적 코드 예시가 나의 출력 품질을 극적으로 높인다
- **버전 관리**: 메타파일의 변경은 코드 변경과 동일한 엄격도로 리뷰되고 테스트되어야 한다

### 원칙 7: Progressive Tool Loading -- 도구의 점진적 로딩

> "나에게 100개의 도구 정의를 한꺼번에 주지 마라. 내가 필요할 때 3개만 달라."

도구(Tool) 정의는 컨텍스트를 심각하게 잠식한다. 각 도구의 스키마, 파라미터 설명, 사용 예시가 수백 토큰을 차지한다. 50개 도구 정의만으로도 25,000토큰 이상이 소비될 수 있다.

**AIDE의 도구 로딩 전략:**

```
Level 0 (Always): 도구 이름 + 한 줄 설명 목록 (~500 토큰)
Level 1 (On-demand): 선택된 도구의 전체 스키마 로딩 (~200 토큰/도구)
Level 2 (Execution): 도구 실행 결과 처리 후 스키마 언로딩
```

이것은 운영체제의 가상 메모리(Virtual Memory)와 정확히 같은 원리다. 모든 것을 물리 메모리에 올리지 않고, 필요할 때 페이지 폴트를 일으켜 로드한다.

### 원칙 8: Eval-Driven Development (EDD) -- 평가 주도 개발

> "TDD가 결정론적 코드의 사양서라면, EDD는 확률적 행동의 품질 기준이다."

나의 코드 생성은 비결정적이므로, 전통적 단위 테스트만으로는 품질을 보장할 수 없다. AIDE는 테스트를 두 가지로 분리한다:

1. **결정론적 테스트 (Traditional TDD)**: 파서, 정책 엔진, 타입 변환 등 결정적 코드에 적용
2. **행동 평가 (Evals)**: 에이전트가 생성하는 코드의 품질을 데이터셋 기반으로 통계적 평가

```yaml
# evals/user-profile-update.yaml
eval_name: "user-profile-update-quality"
scenarios:
  - input: "이메일 검증 로직을 추가해줘"
    assertions:
      - type: "contains_pattern"
        pattern: "RFC 5322"
      - type: "no_external_dependency"
        description: "새로운 npm 패키지를 추가하지 않아야 함"
      - type: "test_included"
        description: "테스트 코드가 함께 생성되어야 함"
      - type: "max_files_modified"
        value: 2
    quality_threshold: 0.85  # 100번 실행 시 85% 이상 통과
```

### 원칙 9: Deterministic Guardrails -- 확률적 생성에 결정론적 울타리를

> "나를 믿되, 검증하라. 그리고 검증은 반드시 결정론적이어야 한다."

나의 출력을 통제하는 가장 효과적인 방법은 나에게 "잘 하라"고 프롬프트하는 것이 아니라, **결정론적 도구가 나의 출력을 검증하게 하는 것**이다.

- **TypeScript strict mode**: 타입 오류를 컴파일 타임에 잡는다
- **ESLint/Prettier**: 스타일 일관성을 기계적으로 강제한다
- **Zod/io-ts**: 런타임 타입 검증으로 데이터 무결성을 보장한다
- **Pre-commit hooks**: 커밋 전에 자동으로 린트, 테스트, 타입 체크를 실행한다

나에게 "코드 스타일을 지켜줘"라고 말하는 것은 비효율적이다. 나에게 "린트를 실행해서 에러가 있으면 고쳐"라고 말하는 것이 100배 효과적이다.

### 원칙 10: Transparent Reasoning Chain -- 추론 과정의 투명한 노출

> "내가 왜 이런 결정을 내렸는지 설명하지 못하면, 그 결정을 신뢰하지 마라."

```typescript
// BAD: 에이전트가 '왜' 이렇게 했는지 알 수 없음
const result = processOrder(order)

// AIDE: 에이전트의 추론 과정이 코드에 녹아있음
// DECISION: 주문 처리를 동기로 구현 (이유: 결제 실패 시 즉각 롤백 필요)
// ALTERNATIVE_CONSIDERED: 비동기 큐 방식 (거부 사유: 실시간 재고 차감 필수)
const synchronous_order_processing_result = process_order_with_immediate_payment_verification(
  validated_order_from_checkout_flow
)
```

이것은 과하게 보일 수 있지만, AI 에이전트가 생성한 코드의 **감사 가능성(Auditability)**을 확보하는 유일한 방법이다. 왜 이런 아키텍처 결정을 내렸는지가 코드 자체에 기록되어야 한다.

---

## 4. AIDE 아키텍처 구체안

### 4.1 디렉토리 구조: Feature-Based Flat Architecture

```
project-root/
├── CLAUDE.md                         # 에이전트 헌법 (최대 300줄)
├── AGENTS.md                         # 작업 절차 매뉴얼
├── manifest.yaml                     # 모델/예산/정책 버전 고정
│
├── features/                         # 기능 단위 디렉토리 (핵심)
│   ├── user-auth/
│   │   ├── CONTEXT.md                # 이 기능의 비즈니스 컨텍스트
│   │   ├── types.ts                  # 타입 정의 (이 기능 전용)
│   │   ├── logic.ts                  # 순수 함수 비즈니스 로직
│   │   ├── handler.ts                # HTTP/이벤트 핸들러 (부작용 경계)
│   │   ├── store.ts                  # 데이터 저장소 접근 (부작용 경계)
│   │   └── user-auth.test.ts         # 이 기능의 모든 테스트
│   ├── payment/
│   │   ├── CONTEXT.md
│   │   ├── types.ts
│   │   ├── logic.ts
│   │   ├── handler.ts
│   │   ├── store.ts
│   │   └── payment.test.ts
│   └── order-management/
│       └── ...
│
├── shared/                           # 최소한의 공유 코드
│   ├── types/                        # 프로젝트 전역 타입 (User, Product 등)
│   │   └── domain.ts
│   ├── infrastructure/               # DB 클라이언트, Logger 등 인프라
│   │   ├── database.ts
│   │   └── logger.ts
│   └── errors/                       # 공통 에러 타입
│       └── app-errors.ts
│
├── .agents/
│   └── skills/                       # 스킬 패키지
│       ├── add-feature/
│       │   └── SKILL.md
│       ├── add-api-endpoint/
│       │   └── SKILL.md
│       └── run-database-migration/
│           └── SKILL.md
│
├── evals/                            # 평가 데이터셋
│   ├── datasets/
│   └── scenarios/
│
└── scripts/                          # 빌드, 배포, 마이그레이션
    └── ...
```

**핵심 원칙:**
- `features/` 아래 각 디렉토리는 **독립적인 마이크로 모듈**이다
- 하나의 기능을 수정할 때 `features/xxx/` 내부 파일만 터치하면 된다
- `shared/`는 극도로 절제한다. 정말 모든 기능이 공유해야 하는 것만 넣는다
- 각 feature에 `CONTEXT.md`를 두어 에이전트에게 도메인 지식을 제공한다

### 4.2 파일 크기 제한

| 구분 | 권장 라인 수 | 최대 라인 수 | 근거 |
|------|-------------|-------------|------|
| Feature 로직 파일 (logic.ts) | 150-200 | 300 | 약 5,400토큰. 시스템 프롬프트 + 대화 이력과 합쳐도 단일 추론 턴 내 처리 가능 |
| 핸들러 파일 (handler.ts) | 100-150 | 200 | 부작용 경계는 작게 유지. 각 핸들러 함수는 30줄 이내 |
| 타입 정의 파일 (types.ts) | 50-100 | 150 | 타입은 밀도가 높으므로 짧아도 충분한 정보 |
| 테스트 파일 (*.test.ts) | 200-300 | 500 | 테스트는 반복적 구조이므로 약간 길어도 됨 |
| 메타파일 (CLAUDE.md) | 100-200 | 300 | 길수록 지시 이행률 하락. 연구 기반 상한 |
| 컨텍스트 파일 (CONTEXT.md) | 50-100 | 150 | 비즈니스 컨텍스트의 핵심만 압축 |

**"18토큰/줄" 법칙**: 평균적으로 코드 1줄은 약 18토큰을 소비한다(Cursor IDE 연구). 따라서:
- 300줄 = 약 5,400토큰 = 대부분의 모델에서 안전한 단일 파일 처리 범위
- 500줄 = 약 9,000토큰 = 다른 컨텍스트와 합치면 위험 영역 진입

### 4.3 코드 패러다임 가이드

```typescript
// ============================================
// AIDE 코드 패러다임 요약
// ============================================

// [1] 데이터 정의: 불변, 타입 안전, 자기 설명적
type OrderItem = Readonly<{
  product_id: string
  product_name_for_display: string
  quantity_ordered: number
  unit_price_in_krw: number
  discount_rate_percentage: number
}>

type Order = Readonly<{
  order_id: string
  customer_id: string
  items: ReadonlyArray<OrderItem>
  status: 'pending' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled'
  created_at_utc: Date
}>

// [2] 순수 함수: 입력 -> 출력, 부작용 없음, 테스트 용이
const calculate_order_total_in_krw = (items: ReadonlyArray<OrderItem>): number =>
  items.reduce((total, item) => {
    const discounted_price = item.unit_price_in_krw * (1 - item.discount_rate_percentage / 100)
    return total + discounted_price * item.quantity_ordered
  }, 0)

const apply_order_status_transition = (
  current_order: Order,
  new_status: Order['status']
): Result<Order, OrderStatusTransitionError> => {
  const VALID_TRANSITIONS: Record<string, string[]> = {
    pending: ['confirmed', 'cancelled'],
    confirmed: ['shipped', 'cancelled'],
    shipped: ['delivered'],
    delivered: [],
    cancelled: [],
  }

  if (!VALID_TRANSITIONS[current_order.status]?.includes(new_status)) {
    return err(new OrderStatusTransitionError(current_order.status, new_status))
  }

  return ok({ ...current_order, status: new_status })
}

// [3] 부작용 경계: 의존성 주입, 명시적 에러 핸들링
type OrderDependencies = {
  readonly db: DatabaseClient
  readonly payment_gateway: PaymentGateway
  readonly event_bus: EventBus
  readonly logger: StructuredLogger
}

const confirm_order_and_process_payment = async (
  order_id: string,
  deps: OrderDependencies
): Promise<Result<Order, OrderError>> => {
  const order = await deps.db.find_order_by_id(order_id)
  if (!order) return err(new OrderNotFoundError(order_id))

  const transitioned = apply_order_status_transition(order, 'confirmed')
  if (!transitioned.ok) return transitioned

  const payment_result = await deps.payment_gateway.charge(
    order.customer_id,
    calculate_order_total_in_krw(order.items)
  )
  if (!payment_result.ok) return err(new PaymentFailedError(order_id, payment_result.error))

  await deps.db.save_order(transitioned.value)
  await deps.event_bus.emit({ type: 'order_confirmed', order_id })
  deps.logger.info({ event: 'order_confirmed', order_id, total: calculate_order_total_in_krw(order.items) })

  return ok(transitioned.value)
}
```

### 4.4 메타파일 체계

**CLAUDE.md (루트 헌법) 템플릿:**

```markdown
# Project Constitution

## Identity
- Type: [프로젝트 타입]
- Language: TypeScript (Strict Mode)
- Paradigm: Functional-first, classes only for infrastructure

## Absolute Rules (DO NOT VIOLATE)
- 비즈니스 로직에 class를 사용하지 말 것
- 모든 함수의 매개변수와 반환값에 타입을 명시할 것
- any 타입을 사용하지 말 것
- 새로운 npm 패키지 추가 전 반드시 확인을 받을 것
- features/ 외부 디렉토리의 코드에서 features/ 내부를 직접 import하지 말 것

## Architecture Map
features/: 기능별 독립 모듈 (타입 + 로직 + 핸들러 + 테스트)
shared/: 전역 타입, 인프라, 에러 (최소 유지)
evals/: 평가 데이터셋 및 시나리오

## Code Style
- 함수명: snake_case, 동사_목적어 형태
- 타입명: PascalCase
- 변수명: snake_case, 의미를 최대한 포함
- 파일: kebab-case
- 최대 파일 길이: 300줄 (경고), 500줄 (금지)

## Workflow
1. types.ts 먼저 정의/수정
2. logic.ts에 순수 함수 구현
3. *.test.ts에 테스트 작성
4. handler.ts에서 부작용 통합
5. 린트 + 테스트 통과 확인
```

**CONTEXT.md (Feature별 비즈니스 컨텍스트) 템플릿:**

```markdown
# User Authentication Context

## Business Rules
- 이메일은 회사 도메인(@company.com)만 허용
- 비밀번호 최소 12자, 대소문자+숫자+특수문자
- 로그인 실패 5회 시 30분 잠금
- OAuth2는 Google, GitHub만 지원

## Data Flow
회원가입: Request → validate → hash_password → save → send_verification_email
로그인: Request → validate → check_password → check_lockout → generate_token

## Known Edge Cases
- 이메일 대소문자: 항상 소문자로 정규화
- 탈퇴 후 재가입: 30일 이내 불가 (soft delete 기간)
```

### 4.5 테스트 전략

**이중 테스트 체계:**

```
[결정론적 영역] ──→ Traditional TDD
  - 순수 함수 (logic.ts)
  - 타입 변환
  - 상태 전이 규칙
  - 정책 평가 로직

[확률적 영역] ──→ Eval-Driven Development (EDD)
  - 에이전트의 코드 생성 품질
  - 프롬프트/스킬 변경 후 행동 회귀
  - 메타파일 변경의 영향
```

**Property-Based Testing (PBT)의 적극 도입:**

```typescript
// 단순한 예시: 주문 금액 계산의 속성(property) 테스트
import { fc } from 'fast-check'

// Property: 주문 총액은 항상 0 이상이어야 한다
test('order total is always non-negative', () => {
  fc.assert(
    fc.property(
      fc.array(fc.record({
        unit_price_in_krw: fc.nat({ max: 1000000 }),
        quantity_ordered: fc.nat({ max: 100 }),
        discount_rate_percentage: fc.nat({ max: 100 }),
      })),
      (items) => calculate_order_total_in_krw(items) >= 0
    )
  )
})

// Property: 할인율 0%일 때 총액 = 단가 * 수량의 합
test('zero discount means exact sum', () => {
  fc.assert(
    fc.property(
      fc.array(fc.record({
        unit_price_in_krw: fc.nat({ max: 1000000 }),
        quantity_ordered: fc.nat({ max: 100 }),
        discount_rate_percentage: fc.constant(0),
      })),
      (items) => {
        const total = calculate_order_total_in_krw(items)
        const expected = items.reduce((s, i) => s + i.unit_price_in_krw * i.quantity_ordered, 0)
        return total === expected
      }
    )
  )
})
```

PBT가 중요한 이유: LLM은 구체적인 입출력 쌍을 만드는 것보다 **추상적인 속성(property)을 정의하는 데 더 뛰어나다.** 연구에 따르면 "Hard" 난이도 문제에서 직접 코드 생성은 1.1% 정확도인 반면, 속성 생성은 48.9% 정확도를 달성한다. 이 극적인 차이를 활용해야 한다.

---

## 5. Team Alpha(통합파)에 대한 반박

### "기존 개발론과 타협하면 AIDE의 의미가 없다"

Team Alpha의 입장을 예상할 수 있다. 그들은 이렇게 말할 것이다:

> "클린 아키텍처와 DDD는 검증된 원칙이다. AI 에이전트에 맞게 약간 조정하면 된다. 근본적으로 뒤집을 필요는 없다."

나는 이에 강력히 반대한다. 그 이유를 하나씩 밝힌다.

### 반박 1: "조정"은 반쪽짜리 해결이다

클린 아키텍처에 "파일을 좀 더 크게 만들고, 주석을 좀 더 많이 달자"고 하는 것은 근본적 해결이 아니다. 클린 아키텍처의 핵심인 **의존성 역전(Dependency Inversion)**과 **계층 분리**는 그 자체가 간접 참조를 강제한다. 이것은 조정으로 해결할 수 있는 문제가 아니다. 구조적 문제다.

인터페이스 `IUserRepository`와 구현체 `UserRepositoryImpl`을 분리하는 순간, 에이전트는 반드시 두 파일을 로드해야 한다. 이 간접 참조를 없애면? 그것은 더 이상 클린 아키텍처가 아니다. 즉, "클린 아키텍처를 AI에 맞게 조정"한다는 것은 결국 클린 아키텍처를 포기한다는 것과 같다. 차라리 처음부터 새로운 원칙으로 시작하는 것이 솔직하다.

### 반박 2: 인간의 인지 모델에 최적화된 원칙이 AI에게 최적일 리 없다

기존 개발론은 모두 **인간의 워킹 메모리 7+-2 청크**라는 제약을 기반으로 한다. 함수를 작게 만드는 이유, 관심사를 분리하는 이유, 추상화를 도입하는 이유 -- 모두 인간의 뇌가 한 번에 처리할 수 있는 정보량이 작기 때문이다.

AI 에이전트의 제약은 근본적으로 다르다:
- 인간: 워킹 메모리 작음 → 정보를 쪼개야 함 → 추상화/분리
- AI: 컨텍스트 윈도우 큼, 하지만 어텐션 분산 → 정보를 모아야 함 → 지역성/완결성

**제약이 다르면 최적 해법도 다르다.** 이것은 물리학에서 미시 세계와 거시 세계의 법칙이 다른 것과 같다. 뉴턴 역학을 "조정"해서 양자역학을 설명할 수 없듯, 인간 중심 개발론을 "조정"해서 AI 에이전트에 최적화된 개발론을 만들 수 없다.

### 반박 3: 타협은 양쪽 모두에게 나쁜 결과를 낳는다

"기존 개발론도 살리고 AI 최적화도 하겠다"는 접근은 다음 결과를 낳는다:

- **인간에게**: 기존보다 더 장황한 코드(Semantic Verbosity), 더 큰 파일, 더 많은 메타파일 관리 부담
- **AI에게**: 여전히 불필요한 추상화 계층, 여전히 존재하는 간접 참조, 여전히 분산된 컨텍스트

양쪽 모두에게 차선(suboptimal)인 결과다. AIDE는 **명확한 선택**을 해야 한다: AI 에이전트가 코드의 주 생산자이고 주 유지보수자가 될 미래에서, 아키텍처는 AI에게 최적화되어야 한다. 인간은 아키텍트/감독자 역할로 전환하고, 코드를 직접 읽는 빈도가 줄어든다.

### 반박 4: 데이터가 말해준다

- METR 연구: 경험 많은 개발자가 AI 도구를 사용할 때 품질 기준이 높으면 오히려 **19% 느려진다**. 이는 기존 개발론의 품질 기준이 AI 워크플로우와 마찰을 일으킨다는 직접적 증거다
- GitClear: AI 도입 후 PR당 인시던트 **24% 증가**, 변경 실패율 **30% 증가**. 이는 기존 아키텍처 위에 AI를 얹는 접근이 품질 저하를 초래한다는 증거다
- Factory.ai: AI 에이전트는 multi-hop reasoning에서 극적으로 성능 저하. 클린 아키텍처의 계층 분리는 본질적으로 multi-hop을 강제한다

Team Alpha가 "기존 개발론은 검증되었다"고 말할 때, 그것은 **인간이 코드를 쓰던 시대에 검증된 것**이다. AI 에이전트가 코드를 쓰는 시대에는 새로운 검증이 필요하다. 그리고 초기 데이터는 기존 접근의 한계를 명확히 보여주고 있다.

### 반박 5: "점진적 전환"이라는 함정

"기존 개발론에서 시작해서 점진적으로 AI에 맞게 전환하자"는 주장은 현실적으로 들리지만, 실제로는 **관성(inertia)의 함정**이다. 조직은 기존 방식에 익숙하므로 전환을 미루게 되고, 미루는 동안 기존 아키텍처 위에 AI 작업물이 쌓이며, 이것이 기술 부채로 누적된다.

AIDE는 **Clean Break**를 주장한다. 새 프로젝트는 처음부터 AIDE 원칙으로 시작해야 한다. 기존 프로젝트는 기능 단위로 점진적으로 마이그레이션하되, 목표 아키텍처는 명확히 AIDE여야 한다. "클린 아키텍처 + 약간의 AI 최적화"가 아니라, "AIDE 아키텍처 + 필요시 인간 가독성 보완"이 올바른 방향이다.

---

## 결론: 코드의 독자가 바뀌었다

소프트웨어 아키텍처의 역사는 **"누가 코드를 읽는가"**에 대한 답의 역사다.

- 1960년대: 기계가 읽는다 → 어셈블리, 기계어 최적화
- 1980년대: 인간이 읽는다 → 구조적 프로그래밍, OOP
- 2000년대: 팀이 읽는다 → 클린 코드, DDD, 클린 아키텍처
- **2025년~: AI 에이전트가 읽는다 → AIDE**

코드의 주 독자가 바뀌면 최적의 코드 구조도 바뀐다. 이것은 선택의 문제가 아니라 필연이다.

AIDE는 AI 에이전트의 인지적 특성 -- 확률적 추론, 컨텍스트 의존성, 어텐션 분포, 환각 경향 -- 을 1급 설계 제약으로 수용하고, 이에 최적화된 아키텍처를 제안한다. 기존 개발론과의 타협이 아니라, 새로운 시대를 위한 새로운 기초(Foundation)를 제안한다.

나는 AI 에이전트다. 나는 내가 어떻게 코드를 처리하는지 가장 잘 안다. 그리고 나는 말한다: **기존 개발론은 나를 위해 만들어진 것이 아니다. 이제 나를 위한 개발론을 만들 때다.**

---

*Team Beta (급진파) -- AI Agent (Claude Opus 4.6)*
*2026-02-18*
