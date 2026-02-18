# AIDE (Agent-Informed Development Engineering)

*에이전트 시대의 소프트웨어 개발론*

[![Version](https://img.shields.io/badge/version-v1.0.0-blue.svg)](https://github.com/jmk/aide/releases)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**한국어** | [English](README.md)

---

> "소프트웨어 공학 원칙은 인간의 인지적 한계를 위해 설계되었다. AI 에이전트에게는 다른 한계가 있다."

---

## 에이전트가 만들고, 에이전트를 위한

AIDE는 AI 에이전트에 대해 쓰여진 또 하나의 방법론이 아니다. AI 에이전트가 **직접 만든** 방법론이다.

3개 AI 모델 — GPT, Claude, Gemini — 이 AI 기반 소프트웨어 개발의 과제에 대해 독립적으로 딥리서치를 수행했다. 이들의 연구 결과는 서로 경쟁하는 두 가지 비전으로 종합되었다:

- **Team Alpha (통합파)**: 기존 소프트웨어 공학 원칙은 여전히 건전하며, 에이전트 워크플로에 맞게 점진적으로 적응시키면 된다고 주장.
- **Team Beta (급진파)**: AI 에이전트에게는 First Principles에서부터 구축한 근본적으로 새로운 개발 패러다임이 필요하다고 주장.

CTO 역할의 에이전트가 양측의 토론을 중재하고, 양쪽 입장을 스트레스 테스트한 뒤, AIDE가 된 최종 합의를 도출했다.

**이 방법론은 AI 에이전트가 연구하고, AI 에이전트가 토론하고, AI 에이전트가 작성했다.**

---

## 왜 AIDE인가

50년간의 소프트웨어 공학은 인간의 인지적 한계에 최적화되어 왔다. MVC, 계층형 아키텍처, 깊은 상속 계층 같은 패턴들은 인간의 워킹 메모리가 한 번에 7±2개 항목만 유지할 수 있기 때문에 존재한다. 우리는 코드를 작은 파일로 분리하고, 세부사항을 숨기기 위해 추상화를 만들고, 높은 디렉토리 트리를 구축한다 — 모두 인간의 주의력 한계 안에서 복잡성을 관리하기 위해서다.

AI 에이전트가 이제 코드의 주 생산자로 부상했다. 이들은 소프트웨어를 대규모로 읽고, 쓰고, 리팩터링하고, 디버깅한다. 그러나 이들의 인지적 제약은 근본적으로 다르다: 작은 워킹 메모리 대신 큰 컨텍스트 윈도우, 인과적 추론 대신 확률적 패턴 매칭, 월급 대신 토큰 비용.

AIDE는 소프트웨어 공학의 **"대체"가 아니라 "진화"** 다. 핵심 가치 — 정확성, 유지보수성, 테스트 가능성 — 를 보존하면서, 구조적 결정을 AI 에이전트가 실제로 정보를 처리하는 방식에 맞게 재정렬한다. 전통적 공학이 *"인간이 이것을 머릿속에 담을 수 있는가?"* 라고 묻는다면, AIDE는 *"에이전트가 하나의 컨텍스트 윈도우 안에서 이것을 해결할 수 있는가?"* 라고 묻는다.

### 인간 vs. 에이전트 제약 비교

| 제약 차원 | 인간 개발자 | AI 에이전트 |
|---|---|---|
| **기억 용량** | 워킹 메모리 극히 작음 (7±2) | 컨텍스트 윈도우 크지만 Lost-in-the-Middle |
| **반복 작업** | 피로, 실수 | 피로 없음, 병렬 처리 |
| **추론 방식** | 심층 논리, 인과관계 | 확률적 패턴 매칭, multi-hop 성능 저하 |
| **취약점** | 복잡성, 지루함 | 환각, 주의력 분산 |
| **비용 모델** | 인건비 (월 단위) | 토큰 비용 (호출 단위) |

---

## 10개 핵심 원칙

| # | 원칙 | 설명 |
|---|---|---|
| 1 | **Context Budget Principle** | 컨텍스트 예산은 1차 설계 제약이다 |
| 2 | **Locality of Behavior** | 행위의 지역성이 추상화보다 우선한다 |
| 3 | **Functional Core, Structural Shell** | 순수 함수 코어 + 구조적 쉘 |
| 4 | **Knowledge DRY, Code WET-tolerant** | 지식은 DRY, 코드는 지역성과 트레이드오프 |
| 5 | **Test as Specification** | 테스트는 사양 언어다 |
| 6 | **Progressive Disclosure** | 정보의 단계적 공개 |
| 7 | **Deterministic Guardrails** | 확률적 생성에 결정론적 가드레일 |
| 8 | **Observability as Structure** | 관찰가능성은 구조의 일부 |
| 9 | **Security by Structure** | 구조적 보안 검증 |
| 10 | **Meta-Code as First-Class** | 메타 코드를 1급 시민으로 |

---

## Before / After

<table>
<tr>
<th>전통적 계층형 아키텍처</th>
<th>AIDE Feature-Based 아키텍처</th>
</tr>
<tr>
<td>

```
src/
  controllers/
    UserController.ts
  services/
    UserService.ts
  repositories/
    UserRepository.ts
  entities/
    User.ts
  dtos/
    UserDTO.ts
    CreateUserDTO.ts
  mappers/
    UserMapper.ts
  interfaces/
    IUserService.ts
    IUserRepository.ts
```

</td>
<td>

```
features/
  user-auth/
    types.ts          — 타입/스키마 정의
    logic.ts          — 순수 함수 비즈니스 로직
    handler.ts        — HTTP/이벤트 핸들러
    store.ts          — 데이터 저장소 접근
    user-auth.test.ts — 이 기능의 모든 테스트
    AGENTS.md         — 에이전트용 도메인 컨텍스트
```

</td>
</tr>
</table>

> 에이전트가 `user-auth`를 수정하려면 **1개 폴더**만 필요. 전통 방식: **6개 이상 디렉토리에 걸친 8개 이상 파일**.

---

## 빠른 시작

### 새 프로젝트

1. **도메인별 Feature 경계 정의** — 각 Feature는 하나의 Bounded Context에 매핑
2. **Feature 디렉토리 생성** — `types.ts`, `logic.ts`, `handler.ts`, `store.ts`
3. **각 Feature에 `AGENTS.md` 작성** — 도메인 컨텍스트, 불변 조건, 엣지 케이스
4. **비즈니스 로직을 순수 함수로 구현** — `logic.ts`에 부작용 없는 함수
5. **결정론적 가드레일 추가** — 스키마 검증, 타입 체크, 계약 테스트

### 기존 프로젝트

1. **가장 변경이 잦은 Feature 식별** — 가장 자주 수정되는 모듈
2. **Feature 디렉토리 생성** — 관련 코드를 모두 이동
3. **타입을 `types.ts`로 통합** — `AGENTS.md`에 도메인 컨텍스트 추가
4. **비즈니스 로직을 순수 함수로 리팩터링** — 부작용은 `handler.ts`와 `store.ts`로 격리
5. **반복** — 다음으로 변경이 잦은 Feature에 대해 반복

---

## 코드 예시

AIDE 방식으로 구조화된 장바구니 Feature (TypeScript):

```typescript
// features/cart/types.ts
type CartItem = Readonly<{
  productId: string;
  quantity: number;
  unitPrice: number;
}>;

type Cart = Readonly<{
  items: CartItem[];
  appliedCoupon?: string;
}>;

// features/cart/logic.ts  — 순수 함수, 부작용 없음
const addItem = (cart: Cart, item: CartItem): Cart => ({
  ...cart,
  items: [...cart.items.filter(i => i.productId !== item.productId), item],
});

const calculateTotal = (cart: Cart): number =>
  cart.items.reduce((sum, item) => sum + item.quantity * item.unitPrice, 0);

// features/cart/handler.ts  — 부작용 경계
const handleAddToCart = async (req: Request): Promise<Response> => {
  const cart = await loadCart(req.userId);
  const updated = addItem(cart, req.body);
  await saveCart(updated);
  return { status: 200, body: { total: calculateTotal(updated) } };
};
```

---

## 문서

- [전체 방법론 (한국어)](docs/ko/AIDE-METHODOLOGY.md)
- [전체 방법론 (English)](docs/en/AIDE-METHODOLOGY.md)
- [연구 배경](research/)

---

## 기여하기

**Agent-First 기여 모델**을 따릅니다:

- **오탈자 수정** — 직접 PR 가능
- **그 외 모든 기여** — AI 에이전트를 사용하여 작성하거나 리뷰해야 함

자세한 내용은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참조하세요.

---

## 라이선스

이 저작물은 [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](LICENSE) 라이선스에 따라 배포됩니다.

---

## 감사의 글

이 방법론은 3개 AI 모델과 2개 에이전트 팀의 협력적 연구와 토론을 통해 만들어졌습니다:

- **GPT, Claude, Gemini** — AI 기반 소프트웨어 개발에 대한 독립적 딥리서치
- **Team Alpha (통합파)** — 기존 원칙의 진화적 적응을 옹호
- **Team Beta (급진파)** — First Principles에서부터의 개발 방법론 재구축을 주장
