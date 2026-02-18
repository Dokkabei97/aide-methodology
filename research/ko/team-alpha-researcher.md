# Team Alpha 연구원 보고서: AIDE(Agent-Informed Development Engineering) 개발론 초안

**작성자**: Team Alpha 연구원 (통합파)
**기반 자료**: GPT 딥리서치, Claude 딥리서치, Gemini 딥리서치 보고서 3종
**관점**: 기존 개발론과 AI 에이전트 최적화의 균형 있는 통합

---

## 1. 3개 보고서 핵심 교차 분석

### 1.1 공통으로 언급하는 핵심 주장들

3개 보고서 모두 다음 주장에 대해 명확한 합의를 보인다.

#### (1) 컨텍스트 윈도우가 새로운 핵심 제약 조건이다
- **GPT**: "컨텍스트 예산을 설계 입력으로" (핵심 원칙 2번), 도구 정의/중간 결과가 토큰을 과점유하는 문제를 P0 요구사항으로 분류
- **Claude**: "컨텍스트 윈도우는 새로운 CPU" — 모든 아키텍처 결정이 이 제약을 중심으로 정렬되어야 한다고 선언. 파일당 200~300줄, 최대 500줄 합의 도출
- **Gemini**: "컨텍스트 공학이 새로운 희소 자원", Lost in the Middle 현상을 중심으로 정보 지역성(Locality) 극대화를 주장

**합의 수준**: 완전 합의. 3개 보고서 모두 컨텍스트 윈도우를 CPU/메모리에 비견되는 1급 설계 제약으로 다룬다.

#### (2) 기존 테스트 전략은 변형이 필요하다
- **GPT**: "평가 주도 개발(EED)" 제안 — 결정적 코드에는 TDD 유지, 모델 행위에는 Evals 기반 검증
- **Claude**: "Test-Driven Generation(TDG)" 제안 — TDD가 더 중요해졌으나 Property-Based Testing(PBT)이 핵심 보완재
- **Gemini**: "리플렉션 루프(Reflexion Pattern)" — 작성-검증-수정의 순환 루프를 자가 치유 메커니즘으로 제안

**합의 수준**: 높은 합의. TDD의 가치를 인정하되, 비결정적 AI 행위에 대한 새로운 검증 체계가 필요하다는 점에 동의.

#### (3) 메타 파일(AGENTS.md, CLAUDE.md)이 새로운 1급 산출물이다
- **GPT**: "프롬프트/스킬/정책도 코드처럼" — 버전관리, 리뷰, 회귀 테스트 대상으로 격상
- **Claude**: AGENTS.md가 60,000+ 오픈소스 프로젝트에서 사용, 3-Tier Progressive Disclosure 아키텍처 제안
- **Gemini**: "메타 제어 평면(Meta-Control Plane)" 개념 — 헌법(CLAUDE.md) + 기술서(AGENTS.md) + 가드레일(린터/테스트)

**합의 수준**: 완전 합의. 메타 파일을 문서가 아닌 런타임 구성요소로 다뤄야 한다.

#### (4) 보안 위협 모델이 근본적으로 달라졌다
- **GPT**: OWASP Top 10 기반 위협-통제 매핑 표 제시, Policy & Guardrails를 아키텍처 계층으로 포함
- **Claude**: AI 생성 코드의 45% 보안 결함, XSS 취약점 2.74배 등 구체적 통계 제시
- **Gemini**: MCP를 보안 게이트웨이로 활용, 권한 최소화 원칙 강조

**합의 수준**: 높은 합의. Prompt Injection, Excessive Agency가 새로운 1급 위협이라는 점에 동의.

#### (5) 관찰가능성(Observability)이 필수 인프라이다
- **GPT**: Observability를 아키텍처 계층에 포함, trace/span/이벤트 로그를 표준 인터페이스로 고정
- **Claude**: 트레이싱 기본 ON, 개발 단계부터 trace 필수
- **Gemini**: 시맨틱 로깅(JSON-LD)을 표준 채택, 에이전트 자체의 디버깅 성공률 향상 목적

**합의 수준**: 완전 합의.

#### (6) 인간의 역할이 구현자에서 아키텍트/검증자로 전환된다
- **GPT**: "인간 평가 의존도가 높다"는 산업 관찰, 휴먼 인 더 루프를 설계 기본값으로
- **Claude**: "인간은 구현자에서 아키텍트-리뷰어로" 전환, 스펙 우선 접근이 AI 코드 품질의 최대 예측 변수
- **Gemini**: "코더에서 스펙 작성자로, 리뷰어에서 아키텍트로" 역할 재정의

**합의 수준**: 완전 합의.

---

### 1.2 보고서 간 의견이 갈리는 지점들

#### (1) OOP에 대한 태도: 수용 vs 배제

| 관점 | GPT | Claude | Gemini |
|------|-----|--------|--------|
| 입장 | **혼합(Hybrid) 권장** — 상태는 함수형, 실행기는 OOP/DI | **Functional Core, Imperative Shell** — OOP는 구조적 조직에 유용 | **함수형 우선, 클래스 사용 자제** — 비즈니스 로직에 클래스 미사용 |
| 강도 | 중립적 통합 | 균형 잡힌 하이브리드 | OOP에 대해 가장 비판적 |

**핵심 갈등**: Gemini는 "클래스는 리소스 관리에만 제한"이라는 급진적 입장인 반면, GPT와 Claude는 OOP의 구조적 가치를 인정한다. 특히 Claude는 DDD의 Bounded Context가 에이전트 경계와 직접 매핑된다며 OOP/DDD가 "더 중요해졌다"고 평가.

#### (2) DRY 원칙에 대한 해석 스펙트럼

| 관점 | GPT | Claude | Gemini |
|------|-----|--------|--------|
| 입장 | 스킬/도구의 카탈로그화로 중복 관리 | "지식 수준 DRY, 코드 수준 중복 허용" — AHA 원칙 적용 | **WET/DAMP 적극 수용** — 5줄짜리 로직이 10곳에 반복되어도 인라인 유지 |
| 강도 | 실용적 중립 | 조건부 허용 | 적극적 중복 옹호 |

**핵심 갈등**: Gemini는 "코드 중복은 에이전트에게 컨텍스트 앵커 역할"이라며 가장 급진적이고, Claude는 "지식은 DRY, 코드는 중복 허용 가능"이라는 중간 입장, GPT는 구조적 해법(카탈로그화)을 선호.

#### (3) 기존 개발론에 대한 근본적 태도

| 관점 | GPT | Claude | Gemini |
|------|-----|--------|--------|
| 입장 | "기존 개발론 위에 5개 새 축 추가" | "기존 원칙이 AI에서 더 중요, 단 재해석 필요" | "인간 중심 설계는 AI에게 미로" — 패러다임 전환 필요 |
| 강도 | 확장론 | 재해석/강화론 | 대체론에 가까움 |

**핵심 갈등**: 이것이 Team Alpha와 Team Beta 논쟁의 핵심 축이 된다. GPT는 "추가", Claude는 "강화", Gemini는 "전환"을 주장.

#### (4) 아키텍처 구조: 계층 vs 기능 중심

| 관점 | GPT | Claude | Gemini |
|------|-----|--------|--------|
| 구조 | **계층(Layer) 중심**: Kernel/Orchestrator/Planner/Executor/Memory/Tooling/Policy/Observability | **계층 + 원칙 기반**: Clean Architecture 호환, DDD Bounded Context 활용 | **기능(Feature) 중심**: Fractal/Flat 구조, `/features/user-auth/` 안에 모든 것 |
| 근거 | 에이전트 런타임의 관심사 분리 | 기존 아키텍처와의 호환성 | 지역성(Locality) 극대화 |

---

### 1.3 각 보고서만의 독특한 통찰

#### GPT 딥리서치 고유 통찰
1. **인터페이스 규격 6종 제안**: `IPlanner`, `IExecutor`, `IMemory`, `IToolRegistry`, `IPolicy`, `IObservability` — 구현 언어와 무관한 표준 인터페이스를 가장 구체적으로 제시
2. **manifest.yaml 기반 버전관리**: 모델 ID/파라미터/정책 버전/스킬 버전/예산을 하나의 매니페스트로 고정하는 운영 전략
3. **Eval Flywheel 개념**: 프로덕션 장애/오답을 즉시 eval 데이터셋에 편입하는 순환 개선 루프
4. **비동기/동시성 모델**: Actor/Queue 기반 `(run_id, step_id)` 단위 작업 처리, 병렬 툴 호출 fanout/fanin

#### Claude 딥리서치 고유 통찰
1. **Property-Based Testing(PBT)의 혁신적 효과**: TDD 대비 23.1~37.3% 상대 향상, Hard 태스크에서 직접 생성 1.1% vs 검증 생성 48.9% — 가장 구체적인 실험 데이터
2. **SOLID 원칙 재정렬**: DIP > SRP > ISP > LSP > OCP — AI 시대에 Dependency Inversion이 가장 중요하다는 새로운 우선순위
3. **PR Contract 개념**: 의도 설명, 작동 증거, 위험 등급 + AI 사용 공개, 인간 리뷰 필요 영역 명시
4. **AI 보안 결함의 정량적 데이터**: 생성 코드 45% 보안 결함, Java 72% 최악, 로직 오류 1.75배, XSS 2.74배 — 모델 크기와 무관

#### Gemini 딥리서치 고유 통찰
1. **의미론적 장황함(Semantic Verbosity)**: `calc(d)` 대신 `calculate_price_with_tax_rate(order_data)` — 변수명이 에이전트를 위한 프롬프트가 된다
2. **리플렉션 패턴(Reflexion Pattern)**: Action → Verification → Observation → Reflexion → Correction의 자가 치유 루프
3. **동적 도구 로딩 5단계**: Registry → Search → Inject → Execute → Unload — 토큰 비용 90% 절감
4. **생산성 급감 구간(Productivity Dip)**: AI 도입 초기 19% 생산성 하락 현상과 이를 극복하기 위한 역할 전환 전략

---

## 2. AIDE 핵심 원칙 제안 (Team Alpha 관점)

> **Team Alpha의 기본 철학**: 기존 개발론은 수십 년간 검증된 공학적 지혜를 담고 있다. AI 에이전트라는 새로운 참여자가 등장했다고 해서 이 지혜를 폐기할 이유는 없다. 다만, 새로운 제약 조건(컨텍스트 윈도우, 비결정성, 프롬프트 인젝션 등)에 맞게 **재해석하고 확장**해야 한다.

### 2.1 파일/코드 크기 제한 가이드라인

**원칙: "컨텍스트 예산 내에서의 응집성(Cohesion within Context Budget)"**

기존 개발론의 "단일 책임 원칙(SRP)"과 "응집도(Cohesion)" 개념을 컨텍스트 윈도우 제약과 결합한다.

| 항목 | 권장 기준 | 근거 |
|------|-----------|------|
| 파일 크기 | **200~300줄 목표, 500줄 상한** | Claude 보고서: 300줄 = ~5,400 토큰, 컨텍스트 여유 확보. GPT 보고서: 300~500줄 초과 시 분리 |
| 함수 크기 | **핵심 로직 30~50줄** | GPT 보고서: 핵심 50줄 이내, 파서/정책/래퍼는 30줄. 기존 Clean Code의 "함수는 한 가지만" 원칙과 호환 |
| 라인 길이 | **100~120자** | 가독성과 diff 리뷰 편의성 |
| 프롬프트/스킬 파일 | **300줄 이내** | Claude 보고서: 지시 수가 늘수록 이행률 선형 감소 |

**Team Alpha 입장**: 이 기준은 새로운 것이 아니다. Clean Code가 이미 "함수는 작게"를 주장했고, SRP가 "파일은 한 가지 이유로만 변경되어야 한다"고 했다. AI 시대에 이 원칙들이 **토큰 비용이라는 정량적 근거**를 얻어 더 강하게 뒷받침될 뿐이다.

### 2.2 OOP vs 함수형 선택 기준

**원칙: "Functional Core, Architectural Shell — with DDD Boundaries"**

Team Alpha는 Claude 보고서의 "Functional Core, Imperative Shell" 접근을 기본으로 채택하되, GPT 보고서의 혼합(Hybrid) 관점과 DDD의 Bounded Context를 결합한다.

| 영역 | 권장 패러다임 | 근거 |
|------|---------------|------|
| 비즈니스 로직 | **함수형 (순수 함수)** | 3개 보고서 합의: 순수 함수는 테스트 용이, 상태 추적 불필요, 에이전트 추론에 유리 |
| 도메인 모델 | **불변 데이터 구조 + 타입** | Gemini: Record/DTO/Struct. Claude: 강한 타입 시스템이 환각 방지 |
| 인프라/실행 계층 | **OOP/DI 허용** | GPT: 복잡한 커넥터/스토리지/클라이언트는 OOP. Claude: Clean Architecture의 의존성 역전 |
| 도메인 경계 | **DDD Bounded Context** | Claude: "DDD가 더 중요해졌다" — 각 에이전트가 특정 도메인의 전문가가 되어야 함 |
| 정책/파서/검증 | **함수형 파이프라인** | GPT: 함수형 파이프로 검증/정규화 일관화 |
| 상태 관리 | **불변 구조 + 이벤트 소싱** | GPT: "상태는 불변 구조(함수형), 실행기는 객체/DI(OOP)" |

**Team Alpha 입장**: Gemini의 "클래스를 비즈니스 로직에 사용하지 말라"는 너무 극단적이다. DDD의 Aggregate, Entity, Value Object는 도메인 지식을 구조화하는 데 여전히 유효하다. 다만 이들을 **불변(immutable)으로 구현**하고, **행위(메서드)보다 함수(순수 함수)**를 통해 변환하는 것이 에이전트 친화적이다.

### 2.3 보일러플레이트/코드 중복에 대한 새로운 관점

**원칙: "Knowledge DRY, Code WET-tolerant (AHA 적용)"**

| 수준 | 전략 | 예시 |
|------|------|------|
| **비즈니스 지식** | **엄격한 DRY** | "할인율 계산 규칙"은 반드시 한 곳에만 정의 |
| **유틸리티 코드** | **AHA (Avoid Hasty Abstractions)** | 이메일 검증 같은 3줄짜리 로직이 2~3곳에서 반복되면 허용, 4곳 이상이면 추출 검토 |
| **보일러플레이트** | **구조화된 중복 허용** | try-catch, 로깅 패턴 등 — 에이전트에게 패턴 앵커 역할 |
| **타입 정의** | **명시적 재선언 가능** | 모듈 경계에서 타입을 재선언하여 독립성 확보 |

**Team Alpha 입장**: Gemini의 "10곳에 5줄 중복도 OK"는 극단적이다. 중복 코드가 드리프트(drift)하면 유지보수 악몽이 된다. Claude가 지적한 대로 "에이전트 자체를 활용하여 중복 코드 간 드리프트를 탐지"하는 것이 현실적 해법이다. 중복은 **의식적으로(consciously)** 허용하되, **가시적(visible)** 관리가 전제되어야 한다.

### 2.4 CLAUDE.md, AGENTS.md 등 메타 파일 관리 전략

**원칙: "Progressive Disclosure with Version Control"**

3개 보고서를 종합한 3-Tier 메타 파일 아키텍처:

| Tier | 파일 | 역할 | 크기 제한 | 로딩 방식 |
|------|------|------|-----------|-----------|
| **Tier 1: 헌법** | `CLAUDE.md` / `AGENTS.md` (루트) | 프로젝트 정체성, 절대 규칙, 아키텍처 맵 | **300줄 이내** | 항상 로딩 |
| **Tier 2: 지역법** | 하위 디렉토리의 `AGENTS.md` | 컴포넌트별 패턴, 로컬 규칙 | **200줄 이내** | 해당 디렉토리 작업 시 Lazy 로딩 |
| **Tier 3: 기술서** | `.agents/skills/*/SKILL.md` | 절차적 지식, 워크플로 가이드 | YAML frontmatter + 본문 | On-demand 로딩 |

**관리 원칙**:
1. **버전 관리**: 코드와 동일한 Git 워크플로 — PR 리뷰, 변경 로그, 릴리스 태그
2. **변경 시 자동 Eval**: 메타 파일 변경은 반드시 CI에서 eval 실행 (GPT의 "변경 시 반드시 eval 실행" 원칙)
3. **크기 감시**: Tier 1 파일이 300줄을 넘으면 CI에서 경고/차단
4. **부정 명령문 활용**: Gemini의 통찰 — "무엇을 하지 말라"가 종종 더 명확
5. **프로젝트 맵 포함**: 디렉토리 구조 개요를 Tier 1에 포함하여 에이전트의 탐색 비용 절감

### 2.5 Skills 관리 방안

**원칙: "Skill as Package — Metadata First, Content on Demand"**

GPT 보고서의 점진적 로딩과 Gemini의 동적 도구 로딩을 결합한다.

**스킬 구조**:
```
.agents/skills/
  {skill-name}/
    SKILL.md          # YAML frontmatter(이름, 설명, 태그) + 실행 가이드
    scripts/           # 자동화 스크립트 (선택)
    examples/          # 예제 입출력 (선택)
    tests/             # 스킬 검증용 eval 시나리오
```

**로딩 프로토콜**:
1. **Discovery**: 에이전트는 SKILL.md의 YAML frontmatter(메타데이터)만 먼저 읽음
2. **Selection**: 태스크와 관련된 스킬을 선택 (자동 매칭 또는 명시적 호출)
3. **Loading**: 선택된 스킬의 전체 내용을 컨텍스트에 주입
4. **Execution**: 스킬 가이드에 따라 작업 수행
5. **Unloading**: 작업 완료 후 컨텍스트에서 해제 (Gemini의 동적 도구 로딩 참고)

**버전 관리**: 각 스킬은 독립 버전을 가지며, `manifest.yaml`에서 참조 (GPT의 manifest 패턴)

### 2.6 테스트 전략 (TDD의 재해석)

**원칙: "Test-Driven Generation(TDG) + Eval-Driven Engineering(EED)"**

Team Alpha는 TDD를 폐기하지 않고, AI 시대에 맞게 **확장**한다.

#### 테스트 피라미드의 재구성

```
                    ┌─────────────┐
                    │  Human      │  인간 리뷰 (아키텍처, 보안, 도메인 지식)
                    │  Review     │
                  ┌─┴─────────────┴─┐
                  │  Eval Suites    │  시나리오/데이터셋 기반 행동 평가 (EED)
                  │  (Behavioral)   │
                ┌─┴─────────────────┴─┐
                │  Simulation Tests   │  모킹 환경에서 step/budget 검증
                │  (Integration)      │
              ┌─┴─────────────────────┴─┐
              │  Property-Based Tests   │  불변 속성 검증 (PBT)
              │  (Specification)        │
            ┌─┴─────────────────────────┴─┐
            │  Unit Tests (TDD)           │  결정적 코드: 파서, 정책, 도구 래퍼
            │  (Foundation)               │
            └─────────────────────────────┘
```

| 테스트 유형 | 대상 | 작성 주체 | 근거 |
|-------------|------|-----------|------|
| **Unit Tests (TDD)** | 결정적 코드 — 파서, 정책 엔진, 상태 전이, 도구 래퍼 | 인간 스펙 → AI 구현 | GPT: "결정적 코드에는 TDD 유지" |
| **Property-Based Tests** | 비즈니스 불변 속성 | 인간이 속성 정의, AI가 생성 | Claude: PBT로 23~37% 향상 |
| **Simulation Tests** | 에이전트 행위 — 스텝 예산, 루프, 롤백 | AI 생성, 인간 리뷰 | GPT: 모킹 환경 시뮬레이션 |
| **Eval Suites** | 모델 출력 품질 — 정확도, 안전성, 유용성 | 인간 설계 + 프로덕션 실패 편입 | GPT: Eval Flywheel |
| **Security Tests** | 프롬프트 인젝션, 권한 남용 시나리오 | 보안팀 설계, 자동 실행 | Claude: 45% 보안 결함 |

**핵심 규칙**: AI가 테스트와 구현 코드를 모두 작성할 때 발생하는 **확인 편향(Confirmation Bias)** 방지 — 테스트 작성자와 구현 작성자를 분리하거나 다른 모델을 사용 (Claude 보고서).

### 2.7 컨텍스트 윈도우 최적화 전략

**원칙: "Structured Scarcity — 정보의 단계적 공개와 능동적 관리"**

3개 보고서의 전략을 통합한 컨텍스트 최적화 체계:

#### 정보 공급 전략
| 전략 | 설명 | 출처 |
|------|------|------|
| **Progressive Disclosure** | 메타데이터 먼저 → 필요 시 본문 로딩 | GPT/Claude |
| **Dynamic Tool Loading** | Registry → Search → Inject → Execute → Unload | Gemini |
| **Context Compaction** | 중간 결과 요약, 오래된 대화 압축 | GPT |
| **Locality Maximization** | 관련 코드를 물리적으로 가까이 배치 | Gemini |

#### 정보 소비 최적화
| 전략 | 설명 | 출처 |
|------|------|------|
| **타입 우선 제공** | 전체 코드 전에 타입/인터페이스 정의를 먼저 제공 | Gemini |
| **의미론적 명명** | 긴 변수명/함수명으로 추가 문서 로딩 불필요하게 | Gemini |
| **아키텍처 맵** | 프로젝트 구조 개요를 Tier 1에 포함 | Claude/Gemini |
| **Lost in the Middle 방지** | 핵심 정보를 컨텍스트 시작과 끝에 배치 | Gemini |

---

## 3. AIDE 아키텍처 패턴 제안

### 3.1 계층 구조 제안

Team Alpha는 GPT 보고서의 계층 모델을 기반으로 하되, Claude의 Clean Architecture 호환성과 Gemini의 기능 중심 조직을 결합한 **"이중 축(Dual-Axis)"** 아키텍처를 제안한다.

#### 수직축: 에이전트 런타임 계층 (GPT 보고서 기반)

```
┌─────────────────────────────────────────────────────┐
│                    Orchestrator                      │  작업 분해, 역할 배정, 스텝 제어,
│               (Control Plane)                        │  휴먼 인 더 루프, 장애 복구
├─────────────┬──────────────┬────────────────────────┤
│   Planner   │   Executor   │     Memory             │  계획 생성 / 실행 / 상태 관리
│             │              │  (Working + Long-term)  │
├─────────────┴──────────────┴────────────────────────┤
│                    Kernel                            │  모델 클라이언트, 예산 관리,
│               (Runtime Foundation)                   │  실행 컨텍스트, 정책 평가
├──────────────────┬──────────────────────────────────┤
│    Policy &      │         Observability            │  권한/감사/가드레일 +
│    Guardrails    │    (Trace/Log/Metric/Replay)     │  트레이싱/모니터링/리플레이
├──────────────────┴──────────────────────────────────┤
│                    Tooling                           │  도구 카탈로그, 스킬, MCP 커넥터,
│               (Capability Layer)                     │  샌드박스, 동적 로딩
└─────────────────────────────────────────────────────┘
```

#### 수평축: 도메인/기능 조직 (Gemini 보고서 기반, DDD 호환)

각 도메인(Bounded Context)은 기능 중심 디렉토리로 구성되며, 자체적으로 응집적인 코드를 포함한다.

```
/features (또는 /domains)
  /user-auth/         ← Bounded Context
    actions.ts        ← 순수 함수 로직
    schema.ts         ← 타입/스키마 정의
    api.ts            ← 엔드포인트
    policy.ts         ← 도메인별 정책
    user-auth.test.ts ← 테스트
    AGENTS.md         ← Tier 2 지역법
```

**Team Alpha의 핵심 통합**: 수직축(런타임 관심사)과 수평축(도메인 관심사)이 독립적으로 변경 가능해야 한다. 이것은 Clean Architecture의 "의존성 규칙"과 DDD의 "Bounded Context"를 AI 에이전트 아키텍처에 적용한 것이다.

### 3.2 디렉토리 구조 권장안

```
repo/
├── AGENTS.md                    # Tier 1: 프로젝트 헌법
├── CLAUDE.md                    # Tier 1: Claude 특화 규칙
├── manifest.yaml                # 모델/정책/스킬/예산 버전 고정
│
├── src/
│   ├── kernel/                  # 런타임 기반 — 모델 클라이언트, 예산, 컨텍스트
│   │   ├── interfaces.ts        # IPlanner, IExecutor, IPolicy 등 표준 인터페이스
│   │   ├── budget.ts
│   │   └── context.ts
│   │
│   ├── orchestrator/            # 제어 평면 — 작업 분해, 스텝 제어
│   │   ├── workflow.ts
│   │   └── handoff.ts
│   │
│   ├── features/                # 도메인/기능 모듈 (수평축)
│   │   ├── user-auth/
│   │   │   ├── actions.ts
│   │   │   ├── schema.ts
│   │   │   ├── api.ts
│   │   │   ├── user-auth.test.ts
│   │   │   └── AGENTS.md        # Tier 2
│   │   └── payment/
│   │       ├── actions.ts
│   │       ├── schema.ts
│   │       └── ...
│   │
│   ├── tooling/                 # 도구 계층 — MCP 커넥터, 샌드박스
│   │   ├── registry.ts
│   │   └── connectors/
│   │
│   ├── policy/                  # 정책/가드레일
│   │   ├── rules.ts
│   │   └── guardrails.ts
│   │
│   ├── observability/           # 관찰가능성
│   │   ├── tracer.ts
│   │   └── metrics.ts
│   │
│   └── shared/                  # 최소한의 공유 유틸 (엄격 관리)
│       ├── types.ts
│       └── errors.ts
│
├── .agents/
│   └── skills/                  # Tier 3: 스킬 패키지
│       └── search-assistant/
│           ├── SKILL.md
│           ├── scripts/
│           └── tests/
│
├── prompts/                     # 프롬프트 템플릿 (버전 관리)
│   ├── system/
│   └── tasks/
│
├── evals/                       # 평가 데이터셋 및 시나리오
│   ├── datasets/
│   └── scenarios/
│
└── tests/                       # 통합/시뮬레이션 테스트
    ├── unit/
    ├── simulation/
    └── security/
```

**설계 원칙**:
- `shared/`는 최소한으로 유지 — 비즈니스 지식 수준 DRY만 여기에 배치
- 각 `features/` 디렉토리는 자가 완결적 — 에이전트가 해당 폴더만 읽고 작업 가능
- `evals/`와 `prompts/`는 코드와 동일한 수준의 버전 관리

### 3.3 인터페이스 규격

GPT 보고서의 6종 인터페이스를 기반으로, Team Alpha가 추가 정제한 표준 인터페이스:

```typescript
// kernel/interfaces.ts — 구현 언어 무관한 개념적 규격

// === 공통 타입 ===
interface Budget {
  maxSteps: number;
  maxTokens: number;
  maxToolCalls: number;
  timeoutMs?: number;
}

interface PlanStep {
  id: string;
  intent: string;            // 무엇을 왜 하는지 (의미론적 설명)
  tool?: string;
  args?: Record<string, unknown>;
  riskLevel: 'low' | 'medium' | 'high';
}

interface Plan {
  goal: string;
  steps: PlanStep[];
  estimatedCost: { tokens: number; toolCalls: number };
}

interface StepResult {
  stepId: string;
  status: 'ok' | 'error' | 'blocked' | 'needs_approval';
  output: unknown;
  events: Event[];
  tokensUsed: number;
}

// === 핵심 인터페이스 6종 ===

// 1. Planner: 목표를 계획으로 분해
interface IPlanner {
  plan(goal: string, state: State, budget: Budget): Promise<Plan>;
}

// 2. Executor: 계획 단계를 실행
interface IExecutor {
  step(planStep: PlanStep, state: State, budget: Budget): Promise<StepResult>;
}

// 3. Memory: 상태/지식 읽기/쓰기
interface IMemory {
  read(scope: string, query: string): Promise<ContextChunk[]>;
  write(events: Event[]): Promise<void>;
  compact(strategy: 'summarize' | 'truncate'): Promise<void>;  // 컨텍스트 압축
}

// 4. Tool Registry & Invoker: 도구 관리 및 실행
interface IToolRegistry {
  list(metaOnly?: boolean): Promise<ToolMeta[]>;               // 메타데이터만 조회
  search(query: string): Promise<ToolMeta[]>;                  // 동적 검색
}
interface IToolInvoker {
  call(name: string, args: unknown, authzCtx: AuthContext): Promise<ToolResult>;
}

// 5. Policy: 행위 허용/거부 판단
interface IPolicy {
  evaluate(action: ActionContext): Promise<{
    decision: 'allow' | 'deny' | 'needs_approval';
    obligations: Obligation[];
    reasoning: string;                                          // 판단 근거 (감사용)
  }>;
}

// 6. Observability: 이벤트/트레이스 발행
interface IObservability {
  emit(event: Event): void;
  startSpan(name: string, parentId?: string): Span;
  endSpan(span: Span): void;
}
```

**Team Alpha 추가 사항**:
- `StepResult`에 `needs_approval` 상태 추가 — 휴먼 인 더 루프 지원
- `PlanStep`에 `riskLevel` 추가 — 위험 기반 승인 체계
- `IMemory`에 `compact()` 추가 — 컨텍스트 압축 전략 지원
- `IPolicy`의 반환값에 `reasoning` 추가 — 감사 추적 강화

---

## 4. Team Beta(급진파)에 대한 예상 반론 준비

> Team Beta의 예상 핵심 주장: "기존 개발론(DDD, Clean Architecture, TDD, SOLID, DRY)은 인간의 인지적 한계를 위해 만들어졌다. AI 에이전트에게는 이것이 오히려 방해가 된다. 완전히 새로운 패러다임이 필요하다."

### 반론 1: "추상화/계층 분리가 AI에게 미로가 된다"는 주장에 대해

**Beta 예상 주장**: 클린 아키텍처의 다층 추상화(Controller → Service → Repository → Entity)는 에이전트의 컨텍스트를 파편화시키고, 환각을 유발한다. (Gemini 보고서의 "8개 파일" 논거)

**Alpha 반론**:
1. **문제는 '추상화 자체'가 아니라 '과도한 추상화'이다.** Gemini가 비판한 8개 파일 패턴은 Clean Architecture의 원칙이 아니라 **과잉 적용(over-engineering)**의 결과이다. Clean Architecture의 Robert C. Martin 본인도 "모든 프로젝트에 4개 계층이 필요한 것은 아니다"라고 했다.
2. **추상화 없는 코드는 변경에 취약하다.** LLM 벤더/모델이 빠르게 바뀌는 환경에서, 구체 구현에 직접 의존하면 벤더 교체 시 코드 전체를 수정해야 한다. Claude 보고서가 지적한 대로 "Dependency Inversion은 AI 시대에 가장 중요한 SOLID 원칙"이다.
3. **Feature-based 구조는 Clean Architecture와 양립 가능하다.** Gemini가 제안한 기능 중심 디렉토리 구조는 Hexagonal Architecture의 "포트와 어댑터"를 모듈 수준에서 적용한 것과 동일한 효과를 낸다. 둘은 대립이 아니라 결합이다.

### 반론 2: "DRY를 완전히 포기하고 WET/DAMP로 가야 한다"는 주장에 대해

**Beta 예상 주장**: 에이전트에게 코드 지역성이 더 중요하다. 중복은 비용이 아니라 앵커이다. (Gemini 보고서의 "보일러플레이트는 패턴 앵커" 논거)

**Alpha 반론**:
1. **Claude 보고서가 지적한 자기모순**: "중복 허용 → AI가 더 많은 코드 생성 → 컨텍스트 윈도우 초과 → 결국 DRY 필요." 무한한 중복 허용은 자기 파괴적이다.
2. **중복 코드의 드리프트는 실재하는 위험이다.** 10곳에 복사된 이메일 검증 로직 중 3곳만 업데이트되면 일관성이 깨진다. 에이전트가 이를 자동 탐지할 수 있다고 해도, **예방이 탐지보다 낫다.**
3. **"의식적 중복(Conscious Duplication)"이 해법이다.** 중복을 완전히 금지하자는 것이 아니라, 중복할 때 그 이유를 문서화하고, 드리프트 감지 체계를 갖추자는 것이다. 이것이 Claude 보고서의 AHA(Avoid Hasty Abstractions) 원칙이다.

### 반론 3: "TDD는 비결정적 AI 출력에 무의미하다"는 주장에 대해

**Beta 예상 주장**: 동일 입력에도 다른 출력이 나오는 AI에게 입력→출력 매핑 기반의 TDD는 작동하지 않는다.

**Alpha 반론**:
1. **에이전트 시스템의 모든 코드가 비결정적인 것은 아니다.** 파서, 정책 엔진, 상태 전이, 도구 래퍼 — 이들은 완전히 결정적이며, 기존 TDD가 완벽하게 적용된다. GPT 보고서가 명확히 구분한다.
2. **PBT가 비결정성 문제를 해결한다.** Claude 보고서의 데이터: PBT는 정확한 입출력이 아니라 **불변 속성(invariant)**을 검증한다. "결과가 항상 양수여야 한다", "정렬 후 첫 원소가 가장 작아야 한다" 같은 속성은 비결정적 출력에서도 검증 가능하다.
3. **"테스트가 사양 언어"라는 Claude의 통찰이 핵심이다.** TDD를 "회귀 방지 도구"로만 보면 비결정성 앞에서 무력해 보이지만, "에이전트에게 의도를 전달하는 사양 언어"로 보면 오히려 더 중요해진다. 테스트 없이 에이전트에게 "잘 만들어줘"라고 하면 결과를 통제할 수 없다.

### 반론 4: "OOP/클래스를 완전히 배제해야 한다"는 주장에 대해

**Beta 예상 주장**: 클래스의 상태 관리는 에이전트에게 고비용이다. 순수 함수만 사용해야 한다. (Gemini 보고서의 "상속의 늪" 논거)

**Alpha 반론**:
1. **비판 대상을 정확히 하자.** Gemini가 비판한 "깊은 상속 트리"는 이미 모던 OOP에서도 안티패턴이다. "상속보다 합성(Composition over Inheritance)"은 GoF 이래의 원칙이다. OOP = 상속이 아니다.
2. **DDD의 도메인 모델링은 순수 함수로 대체하기 어렵다.** 복잡한 비즈니스 도메인에서 Aggregate Root, Entity, Value Object의 개념은 순수 함수만으로는 표현이 어색하다. Claude 보고서: "DDD는 AI 시대에 더 중요해졌다."
3. **하이브리드가 현실적이다.** Team Alpha는 "비즈니스 로직은 함수형, 인프라는 OOP"라는 절충안을 제시한다. 이것은 Gemini도 "리소스 관리에만 클래스 사용"이라고 했으므로, 범위의 차이일 뿐 근본적 불일치가 아니다.

### 반론 5: "기존 개발론을 폐기하고 백지에서 시작해야 한다"는 총론에 대해

**Alpha 핵심 반론**:

1. **기존 원칙의 핵심 가치는 보편적이다.** 단일 책임, 관심사 분리, 의존성 역전, 명시적 계약, 테스트 가능성 — 이 원칙들은 "인간의 인지 한계" 때문만이 아니라 **시스템의 복잡성 관리** 자체를 위해 존재한다. AI 에이전트도 복잡성 관리가 필요하다.

2. **새로운 제약은 "추가"이지 "대체"가 아니다.** 컨텍스트 윈도우, 비결정성, 프롬프트 인젝션은 기존 제약(변경 용이성, 테스트 가능성, 보안)에 **추가**된 것이다. 기존 제약이 사라진 것이 아니다. GPT 보고서: "AIDE는 기존 개발론을 대체하기보다, 행동/컨텍스트/권한/관찰/평가라는 5개의 새로운 1급 설계 축을 추가한다."

3. **산업적 검증이 이를 뒷받침한다.** Claude 보고서의 Tweag 실험: 스펙 우선 접근(기존 개발론의 핵심)을 사용한 팀이 45% 더 빠르게 완료했다. 기존 원칙을 잘 적용한 팀이 AI와 함께 더 좋은 결과를 낸다.

4. **급진적 전환의 리스크가 크다.** 수십만 개의 기존 프로젝트와 수백만 명의 개발자가 기존 패러다임에 익숙하다. "완전히 새로운 방식"은 채택 장벽이 극도로 높다. Team Alpha의 "확장/재해석" 접근이 점진적 도입에 유리하다.

---

## 부록: 3개 보고서 특성 비교표

| 특성 | GPT 딥리서치 | Claude 딥리서치 | Gemini 딥리서치 |
|------|-------------|----------------|----------------|
| **분량/깊이** | 가장 방대, 산업 조사 + 아키텍처 설계 + 운영까지 | 중간, 학술 연구 + 실무 가이드 균형 | 가장 집중적, 철학적 선언 + 실전 가이드 |
| **기조** | 체계적/포괄적 — "5개 새 축 추가" | 균형적/실증적 — "기존 원칙 강화+재해석" | 선언적/급진적 — "패러다임 전환" |
| **기존 개발론** | 존중하며 확장 | 강화하며 재해석 | 비판하며 대체 |
| **OOP 입장** | 하이브리드 권장 | FP Core + OOP Shell | FP 우선, OOP 최소화 |
| **DRY 입장** | 구조적 해법 (카탈로그) | AHA 원칙 (조건부 허용) | WET/DAMP 적극 수용 |
| **고유 강점** | 인터페이스 규격, manifest, CI/CD 파이프라인 | PBT 데이터, SOLID 재정렬, 보안 정량 데이터 | 의미론적 장황함, 리플렉션 루프, 동적 도구 로딩 |
| **Team Alpha 활용** | 아키텍처 프레임워크 기반 | 테스트 전략 및 원칙 재해석 기반 | 컨텍스트 최적화 전략 기반 |

---

*이 보고서는 Team Alpha(통합파) 연구원이 3개 딥리서치 보고서를 교차 분석하여 작성한 초안입니다. Team Beta의 보고서와 함께 CTO 검토를 거쳐 최종 AIDE 합의 문서로 발전될 예정입니다.*
