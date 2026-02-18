# AIDE (Agent-Informed Development Engineering) -- 에이전트 시대의 소프트웨어 개발론 v1.0

**작성**: CTO (20년+ 아키텍처 경험, 3년 AI 에이전트 실전 경험)
**기반**: GPT/Claude/Gemini 3종 딥리서치 + Team Alpha(통합파) 보고서 2종 + Team Beta(급진파) 보고서 1종
**날짜**: 2026-02-18

---

## Part 3: 기존 개발론과의 관계

### 보존/변경/폐기 분류표

Team Alpha 시니어 개발자의 분석을 기반으로, CTO가 최종 판단을 추가한 분류표:

#### 아키텍처 패턴

| 원칙 | 핵심 가치 | 판정 | AIDE에서의 재해석 |
|------|-----------|------|-----------------|
| **DDD - Bounded Context** | 도메인 경계로 복잡성 관리 | **보존 (강화)** | 각 Feature 디렉토리가 하나의 Bounded Context에 대응. AGENTS.md에 도메인 용어집 포함. |
| **DDD - Ubiquitous Language** | 도메인 공통 언어 | **보존 (강화)** | AGENTS.md에 명시적 문서화 필수. 에이전트는 암묵적 지식이 없으므로. |
| **DDD - Domain Events** | 도메인 간 느슨한 결합 | **보존 (강화)** | Feature 간 통신, 관찰가능성의 기반. |
| **DDD - Aggregate** | 트랜잭션 일관성 경계 | **변경** | 불변 데이터 구조 + 이벤트 소싱으로 재구현. |
| **Clean Architecture** | Dependency Rule | **변경** | 의존성 규칙은 유지, 물리적 계층을 2~3개로 축소, Feature 기반 구조로 전환. |
| **Hexagonal Architecture** | Ports & Adapters | **변경** | 외부 서비스/DB 교체에 Adapter 가치 높아짐. Port/Adapter 파일 수 최소화. |
| **Layered Architecture** | 수평적 계층 분리 | **변경 (축소)** | Vertical Slice로 전환. 논리적 계층 개념만 유지, 물리적 계층 폴더 제거. |

#### SOLID 원칙 재정렬

AI 에이전트 시대의 SOLID 우선순위: **DIP > SRP > ISP > LSP > OCP**

| 원칙 | 기존 순위 | AIDE 순위 | 이유 |
|------|-----------|----------|------|
| **DIP (Dependency Inversion)** | 5번째 (마지막) | **1위** | LLM/도구/인프라가 수개월 단위로 교체. 추상에 의존해야 생존 가능. Feature 간 인터페이스가 DIP의 직접 구현. |
| **SRP (Single Responsibility)** | 1번째 | **2위** | AI 수정의 blast radius를 제한. 단위는 파일이 아닌 Feature/Module 수준으로 확대. |
| **ISP (Interface Segregation)** | 4번째 | **3위** | AI는 focused, minimal interface에서 더 잘 작동. 불필요한 인터페이스 노출 방지가 보안에도 기여. |
| **LSP (Liskov Substitution)** | 3번째 | **4위** | 타입 안전성의 기본. 강한 타입 시스템이 환각 방지 가드레일 역할. |
| **OCP (Open/Closed)** | 2번째 | **5위** | AI가 코드를 자유롭게 수정하므로 "변경에 닫혀야"라는 전제 약화. Plugin/Strategy에서는 여전히 유효. |

#### GoF 패턴 분류

| 분류 | 패턴 | 이유 |
|------|------|------|
| **AI 친화 (적극 활용)** | Strategy, Observer, Factory Method, Adapter, Command, Repository | 단일 책임, 명확한 인터페이스, 교체 용이성 |
| **상황적 (주의하여 사용)** | Singleton, Template Method, State, Builder | 사용 시 에이전트 컨텍스트에 충분한 문서화 필요 |
| **AI 비친화 (사용 자제)** | Visitor, 깊은 Abstract Factory 계층, 긴 Decorator 체인, 복잡한 Mediator | 복잡한 dispatch, 다중 파일 간 암묵적 관계, multi-hop reasoning 강제 |

#### DDD의 재해석

DDD는 AIDE 시대에 **더 중요해진다**. 다만 구현 방식이 변한다:

| DDD 개념 | 기존 구현 | AIDE 구현 |
|----------|-----------|----------|
| **Bounded Context** | 패키지/모듈 경계 | Feature 디렉토리 + Tier 2 AGENTS.md |
| **Aggregate Root** | 클래스 (가변 상태) | 불변 타입 + 순수 함수 (상태 전이) |
| **Entity** | 클래스 + ID | 불변 Record + ID 필드 |
| **Value Object** | 불변 클래스 | 불변 타입 리터럴 |
| **Domain Event** | 이벤트 클래스 | 타입 리터럴 + Observability 연동 |
| **Ubiquitous Language** | 구두 + 코드 | AGENTS.md에 명시적 용어집 포함 |
| **Repository** | 인터페이스 + 구현체 | Feature 내 store.ts (부작용 경계) |

---



← Previous: [02-ARCHITECTURE-PATTERNS](./02-ARCHITECTURE-PATTERNS.md) | Next: [04-PRACTICAL-GUIDE](./04-PRACTICAL-GUIDE.md) →
