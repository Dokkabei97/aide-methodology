# AIDE 자기진화 메커니즘 설계서

**작성 에이전트**: Claude Opus 4.6
**역할**: 진화 설계자 (Evolution Architect)
**작성일**: 2026-02-20
**상태**: 설계 초안 (Design Draft)

---

## 1. 원칙의 반감기(Half-Life) 프레임워크

### 1.1 문제 인식

현재 AIDE v1.0은 문서 말미에 "반기별 개정 권장"이라고 명시하지만, **무엇이 바뀌어야 하는지를 판단하는 구조적 메커니즘**이 없다. 10개 원칙 각각은 특정한 기술적 제약 조건 위에 세워져 있으며, 그 제약이 사라지면 원칙의 유효성도 변한다. 이를 체계적으로 추적하기 위한 프레임워크가 필요하다.

### 1.2 원칙 메타데이터 스키마

각 원칙에 다음 메타데이터를 부착한다:

```yaml
# principle-metadata.yaml
principles:
  - id: P1
    name: "Context Budget Principle"
    version: "1.0"
    established: "2026-02-18"
    last_reviewed: "2026-02-18"
    next_review: "2026-08-18"

    # 유효 조건 (Validity Conditions)
    # 이 조건들이 모두 참일 때 원칙이 유효함
    validity_conditions:
      - id: VC-P1-01
        description: "컨텍스트 윈도우 < 10M tokens"
        measurement: "주요 모델(GPT, Claude, Gemini)의 공식 컨텍스트 윈도우 상한"
        current_value: "1M-2M tokens (2026-02)"
        threshold: "10M tokens"
        status: "valid"

      - id: VC-P1-02
        description: "Lost-in-the-Middle 현상이 존재"
        measurement: "NIAH(Needle-In-A-Haystack) 벤치마크 중간 위치 정확도"
        current_value: "중간 위치 정확도 70-85% (모델별 상이)"
        threshold: "중간 위치 정확도 >= 95%이면 현상 소멸로 간주"
        status: "valid"

      - id: VC-P1-03
        description: "토큰 비용이 유의미한 설계 제약"
        measurement: "100K 토큰 처리 비용 (주요 모델 평균)"
        current_value: "$0.50-3.00 / 100K tokens"
        threshold: "$0.01 / 100K tokens 이하이면 비용 제약 소멸"
        status: "valid"

    # 무효화 트리거 (Invalidation Triggers)
    # 하나라도 발동하면 원칙 재검토를 트리거
    invalidation_triggers:
      - id: IT-P1-01
        condition: "주요 3개 모델 모두 컨텍스트 윈도우 >= 10M tokens"
        action: "P1 수치 가이드라인(파일 200-300줄, 함수 30줄) 재검토"
        severity: "major"  # major: 원칙 핵심 변경, minor: 수치 조정

      - id: IT-P1-02
        condition: "NIAH 벤치마크 중간 위치 정확도 >= 95% (3개 모델 평균)"
        action: "파일 크기 상한 완화 검토, Lost-in-the-Middle 관련 근거 삭제"
        severity: "major"

      - id: IT-P1-03
        condition: "토큰 처리 비용이 $0.01/100K 이하로 하락"
        action: "비용 기반 근거 재작성, 수치 가이드라인 완화 검토"
        severity: "minor"

    # 강화 트리거 (Reinforcement Triggers)
    # 원칙을 더 강화해야 할 조건
    reinforcement_triggers:
      - id: RT-P1-01
        condition: "멀티모달 입력(이미지, 비디오)이 보편화되어 토큰 소비 급증"
        action: "코드 전용 토큰 예산을 더 엄격하게 제한"
        severity: "major"

  - id: P2
    name: "Locality of Behavior"
    version: "1.0"
    established: "2026-02-18"
    last_reviewed: "2026-02-18"
    next_review: "2026-08-18"

    validity_conditions:
      - id: VC-P2-01
        description: "Multi-hop reasoning에서 성능 저하가 존재"
        measurement: "SWE-bench 등에서 cross-file reasoning 정확도"
        current_value: "cross-file 정확도 ~40-60%"
        threshold: "cross-file 정확도 >= 90%이면 성능 저하 소멸로 간주"
        status: "valid"

      - id: VC-P2-02
        description: "에이전트가 동시에 참조할 수 있는 파일 수에 실질적 한계 존재"
        measurement: "에이전트가 N개 파일을 동시 참조할 때 일관성 유지율"
        current_value: "3-5개 파일에서 일관성 급감"
        threshold: "20개 이상 파일에서도 일관성 >= 95%"
        status: "valid"

    invalidation_triggers:
      - id: IT-P2-01
        condition: "multi-hop reasoning 벤치마크 정확도 >= 95% (주요 3개 모델)"
        action: "Feature-based 구조 강제를 완화, 전통적 레이어 구조 허용 범위 확대"
        severity: "major"

      - id: IT-P2-02
        condition: "에이전트가 전체 리포지토리를 실시간 인덱싱하여 탐색하는 능력이 보편화"
        action: "물리적 co-location 요구 완화, 논리적 연결성으로 대체 가능"
        severity: "major"

    reinforcement_triggers:
      - id: RT-P2-01
        condition: "에이전트가 더 많은 도구/MCP 서버를 동시 사용하여 컨텍스트 경쟁 심화"
        action: "Feature 디렉토리의 자기완결성 요구 강화"

  - id: P3
    name: "Functional Core, Structural Shell"
    version: "1.0"
    validity_conditions:
      - id: VC-P3-01
        description: "에이전트가 상태 추적(state tracking)에서 순수 함수 대비 성능 열위"
        measurement: "stateful vs stateless 코드 생성 정확도 비교 벤치마크"
        threshold: "stateful 코드 생성 정확도가 stateless와 동등(차이 < 5%)"
      - id: VC-P3-02
        description: "불변 데이터가 추론 체인 단순화에 기여"
        measurement: "mutable vs immutable 코드에서의 버그 발생률"
        threshold: "mutable 코드의 버그율이 immutable과 동등"

    invalidation_triggers:
      - id: IT-P3-01
        condition: "에이전트가 복잡한 상태 머신을 99%+ 정확도로 생성/추론 가능"
        action: "클래스 사용 제한 완화, 'business logic에 클래스 금지' 규칙 재검토"
        severity: "major"

  - id: P4
    name: "Knowledge DRY, Code WET-tolerant"
    version: "1.0"
    validity_conditions:
      - id: VC-P4-01
        description: "컨텍스트 윈도우 한계로 인해 무제한 중복이 자기모순적"
        measurement: "P1의 유효 조건과 연동"
        threshold: "P1이 무효화되면 재검토"
      - id: VC-P4-02
        description: "에이전트가 다른 파일의 유틸리티 함수 구현을 정확히 추론하지 못함"
        measurement: "cross-file function inference 정확도"
        threshold: ">= 95% 정확도이면 추론 가능으로 간주"

    invalidation_triggers:
      - id: IT-P4-01
        condition: "P1이 major 수준으로 무효화"
        action: "코드 중복 허용 범위 재검토 (DRY 방향 또는 WET 방향 모두 가능)"
        severity: "major"

  - id: P5
    name: "Test as Specification"
    version: "1.0"
    validity_conditions:
      - id: VC-P5-01
        description: "AI 생성 코드의 확인 편향(confirmation bias) 위험이 존재"
        measurement: "동일 모델이 테스트+코드 작성 시 vs 다른 모델 시 버그 탈출률"
        threshold: "동일 모델의 버그 탈출률이 다른 모델과 동등"
      - id: VC-P5-02
        description: "PBT가 직접 코드 생성보다 높은 정확도를 보임"
        measurement: "Hard tasks에서 PBT vs direct generation 정확도"
        current_value: "PBT 48.9% vs direct 1.1%"
        threshold: "direct generation >= 90%이면 PBT 우위 소멸"

    invalidation_triggers:
      - id: IT-P5-01
        condition: "AI가 formal verification을 자동 수행하여 테스트 대부분을 대체 가능"
        action: "테스트 전략을 formal verification 중심으로 재편"
        severity: "major"

  - id: P7
    name: "Deterministic Guardrails"
    version: "1.0"
    validity_conditions:
      - id: VC-P7-01
        description: "AI 생성 코드의 보안 결함률이 유의미하게 높음"
        measurement: "AI 생성 코드 보안 결함률 (Veracode 등)"
        current_value: "~45%"
        threshold: "< 5%이면 가드레일 수준 하향 검토"
    invalidation_triggers:
      - id: IT-P7-01
        condition: "AI 생성 코드의 보안 결함률 < 5% (독립 감사 기관 확인)"
        action: "보안 가드레일을 필수에서 권장으로 완화 검토"
        severity: "major"
    reinforcement_triggers:
      - id: RT-P7-01
        condition: "AI 생성 코드가 새로운 유형의 보안 취약점을 생성"
        action: "해당 취약점 유형에 대한 가드레일 추가"
```

### 1.3 반감기 측정 프로세스

```
[분기별 벤치마크 수집]
    → [유효 조건 평가]
    → [무효화 트리거 점검]
    → [트리거 발동?]
        → Yes: [RFC 자동 생성] → [검토 프로세스 진입]
        → No:  [상태 기록, 다음 분기 대기]
```

**핵심 규칙**:
1. 유효 조건의 `threshold`는 원칙 제정 시 명시하며, 사후 변경 시 별도 RFC 필요
2. 무효화 트리거는 **단일 모델이 아닌 주요 3개 모델 이상**에서 확인되어야 발동
3. `severity: major`인 트리거는 원칙의 핵심 변경을, `minor`는 수치 가이드라인 조정을 의미
4. 강화 트리거도 동일한 프로세스를 따르되, 방향이 "강화"임

### 1.4 원칙 간 의존성 맵

원칙들은 독립적이지 않다. 하나의 원칙이 무효화되면 연쇄 영향이 발생한다:

```
P1 (Context Budget) ──영향──→ P2 (Locality)
                     ──영향──→ P4 (Knowledge DRY)
                     ──영향──→ P6 (Progressive Disclosure)

P2 (Locality) ──영향──→ P3 (Functional Core)
              ──영향──→ P4 (Knowledge DRY)

P7 (Guardrails) ──영향──→ P9 (Security)
                ──영향──→ P5 (Test as Spec)

P10 (Meta-Code) ──영향──→ P6 (Progressive Disclosure)
```

**의미**: P1이 무효화되면 P2, P4, P6도 연쇄 재검토 대상이 된다. 이를 `cascade_review` 속성으로 메타데이터에 명시한다.

---

## 2. Self-Amending Methodology 프레임워크

### 2.1 수정 권한 매트릭스

방법론 자체를 누가, 어떤 조건에서, 어떤 범위까지 수정할 수 있는가를 정의한다.

| 수정 범위 | 수정 주체 | 트리거 조건 | 승인 요건 | 안전장치 |
|-----------|----------|------------|----------|---------|
| **수치 가이드라인 조정** (예: 파일 300줄 → 500줄) | 에이전트 제안 → 인간 승인 | 반감기 트리거(`minor`) 발동 | 메인테이너 1인 승인 | 7일 의견 수렴, 롤백 가능 |
| **원칙 핵심 변경** (예: "클래스 금지" 해제) | 에이전트 RFC 초안 → 인간 주도 토론 | 반감기 트리거(`major`) 발동 | 메인테이너 과반 합의 | 14일 토론, 벤치마크 증거 필수 |
| **원칙 추가** (11번째 원칙) | 에이전트 리서치 → 인간 제안 → 에이전트 RFC | 새로운 제약 조건 출현 | 메인테이너 2/3 합의 | 21일 토론, 3개 이상 모델 교차 검증 |
| **원칙 폐기** | 인간만 가능 | 원칙의 모든 유효 조건 소멸 | 메인테이너 만장일치 | 30일 유예, "deprecated" 단계 거침 |
| **방법론 메이저 버전** (v2.0) | 인간 주도, 에이전트 리서치 지원 | 과반 이상 원칙이 major 수정 대상 | 전체 커뮤니티 투표 | 기존 버전 1년간 병행 유지 |

### 2.2 수정 프로세스 (Self-Amending Protocol)

```
Phase 1: 감지 (Detection)
┌─────────────────────────────────────────────┐
│ 벤치마크 수집 에이전트가 분기별 데이터 수집   │
│ → principle-metadata.yaml의 유효 조건 평가    │
│ → 무효화/강화 트리거 점검                     │
│ → 트리거 발동 시 자동 이슈 생성               │
└─────────────────────────────────────────────┘
          │
          ▼
Phase 2: 분석 (Analysis)
┌─────────────────────────────────────────────┐
│ 리서치 에이전트가 트리거 관련 증거 수집       │
│ → 최소 3개 독립 소스(벤치마크, 논문, 실무)    │
│ → 영향 받는 원칙 연쇄 분석 (의존성 맵 참조)   │
│ → RFC 초안 자동 생성                          │
└─────────────────────────────────────────────┘
          │
          ▼
Phase 3: 토론 (Deliberation)
┌─────────────────────────────────────────────┐
│ RFC가 리포지토리에 PR로 제출                  │
│ → severity에 따른 토론 기간 (7/14/21/30일)   │
│ → 에이전트 + 인간 리뷰어 모두 참여            │
│ → 찬반 의견 + 증거 기반 토론                  │
└─────────────────────────────────────────────┘
          │
          ▼
Phase 4: 결정 (Decision)
┌─────────────────────────────────────────────┐
│ 메인테이너가 최종 결정                        │
│ → 승인: 방법론 문서 업데이트, 버전 범프        │
│ → 거부: 근거 기록, 다음 분기 재검토 여부 결정  │
│ → 보류: 추가 증거 요청, 다음 분기 재평가       │
└─────────────────────────────────────────────┘
          │
          ▼
Phase 5: 적용 (Application)
┌─────────────────────────────────────────────┐
│ 방법론 문서(영문+한국어) 동시 업데이트         │
│ → AIDE-REFERENCE.md 동기화                    │
│ → CHANGELOG.md 업데이트                       │
│ → principle-metadata.yaml 업데이트             │
│ → 릴리스 태그 생성                            │
└─────────────────────────────────────────────┘
```

### 2.3 안전장치

#### 2.3.1 롤백 메커니즘

모든 방법론 변경은 Git 기반으로 추적되므로, 기술적 롤백은 항상 가능하다. 그러나 **의미적 롤백**을 위한 프로토콜이 필요하다:

- **쿨다운 기간**: 변경 적용 후 최소 1개 분기(3개월)는 추가 변경 금지 (해당 원칙에 한해)
- **관찰 기간**: 변경 후 2개 분기 동안 채택 프로젝트의 메트릭 수집 (코드 품질, 에이전트 성능, 개발 속도)
- **롤백 트리거**: 변경 후 채택 프로젝트에서 측정 가능한 품질 하락이 관찰되면 롤백 RFC 자동 생성

#### 2.3.2 불변 핵심 (Immutable Core)

방법론이 아무리 진화해도 **변경할 수 없는 메타 원칙**이 있어야 한다:

1. **증거 기반 의사결정**: 모든 방법론 변경은 벤치마크, 실험, 실무 데이터에 근거해야 한다
2. **인간 최종 승인권**: 에이전트가 제안할 수 있지만, 원칙 변경의 최종 결정권은 인간에게 있다
3. **투명성**: 모든 변경의 근거, 토론 과정, 결정 이유가 공개 기록된다
4. **가역성**: 모든 변경은 롤백 가능해야 한다
5. **이중 언어 동기화**: 영문과 한국어 문서는 항상 동기화된다

이 5개의 메타 원칙을 변경하려면 별도의 "헌법 수정" 프로세스가 필요하다 (전체 커뮤니티 투표, 2/3 이상 찬성).

### 2.4 버전 관리 체계

```
AIDE v{Major}.{Minor}.{Patch}

Major: 원칙 추가/폐기, 또는 3개 이상 원칙의 핵심 변경
Minor: 원칙의 핵심 변경 (1-2개), 새로운 아키텍처 패턴 추가
Patch: 수치 가이드라인 조정, 오타 수정, 예시 추가
```

---

## 3. 에이전트 벤치마크 기반 자동 조정 시스템

### 3.1 추적 대상 벤치마크

| 벤치마크 | 측정 대상 | 관련 원칙 | 수집 주기 |
|---------|----------|----------|----------|
| **SWE-bench** | 실제 GitHub 이슈 해결 능력 | P2 (Locality), P5 (Test) | 분기별 |
| **SWE-bench Multifile** | 다중 파일 수정 능력 | P1 (Context), P2 (Locality) | 분기별 |
| **HumanEval / MBPP** | 단일 함수 생성 정확도 | P3 (Functional Core) | 분기별 |
| **NIAH (Needle-In-A-Haystack)** | 긴 컨텍스트에서의 정보 검색 | P1 (Context), P6 (Disclosure) | 분기별 |
| **CyberSecEval** | 보안 코드 생성 능력 | P7 (Guardrails), P9 (Security) | 반기별 |
| **Multi-hop Reasoning** | 다단계 추론 능력 | P2 (Locality), P4 (DRY) | 분기별 |
| **Aider Polyglot** | 다중 언어 코드 편집 능력 | 전체 | 분기별 |
| **모델 비용 추적** | 100K 토큰당 비용 | P1 (Context) | 월별 |

### 3.2 자동 조정 알고리즘

```
함수: evaluate_principle_health(principle, benchmark_results)

입력:
  - principle: 원칙 메타데이터
  - benchmark_results: 최신 벤치마크 결과

처리:
  1. principle.validity_conditions 각각에 대해:
     - benchmark_results에서 관련 측정값 추출
     - current_value 업데이트
     - threshold와 비교하여 status 결정 (valid/warning/invalid)

  2. status == "warning" 조건:
     - 현재 값이 threshold의 80% 이내에 도달
     - → 다음 분기 집중 모니터링 대상으로 플래그

  3. status == "invalid" 조건:
     - 현재 값이 threshold를 초과
     - → 해당 invalidation_trigger 발동
     - → RFC 이슈 자동 생성

  4. 연쇄 영향 평가:
     - 의존성 맵에서 cascade_review 대상 원칙 식별
     - 해당 원칙들도 재평가 큐에 추가

출력:
  - 업데이트된 principle-metadata.yaml
  - 발동된 트리거 목록
  - 자동 생성된 RFC 이슈 (해당 시)
```

### 3.3 조정 예시 시나리오

#### 시나리오 A: 컨텍스트 윈도우 10M 돌파

```
[2027 Q2 벤치마크 수집]
  → GPT-6: 10M tokens
  → Claude 5: 8M tokens
  → Gemini 4: 15M tokens

[P1 유효 조건 평가]
  → VC-P1-01: "컨텍스트 윈도우 < 10M tokens"
  → 3개 모델 중 2개가 10M 이상 → threshold 근접 (warning)
  → 아직 3개 모두는 아님 → 트리거 미발동, warning 플래그

[다음 분기]
  → Claude 5.1: 12M tokens (3개 모두 10M+)
  → IT-P1-01 발동
  → RFC 자동 생성: "P1 수치 가이드라인 재검토 - 파일 크기 상한 조정"
  → 연쇄: P2, P4, P6도 재검토 큐에 추가
```

#### 시나리오 B: Multi-hop reasoning 95%+ 달성

```
[2027 Q4 벤치마크 수집]
  → SWE-bench Multifile: 평균 96% (3개 모델)
  → Multi-hop reasoning: 평균 97%

[P2 유효 조건 평가]
  → VC-P2-01: "Multi-hop reasoning에서 성능 저하가 존재"
  → threshold 95% 초과 → status: invalid
  → IT-P2-01 발동

[RFC 자동 생성]
  → 제목: "P2 Locality of Behavior 재검토 - Feature-based 구조 강제 완화"
  → 근거: "Multi-hop reasoning이 95%+에 도달하여, 여러 파일에 걸친
           추론의 성능 저하 근거가 소멸됨"
  → 제안: "Feature-based 구조를 기본 권장(default)으로 유지하되,
           충분한 근거가 있을 경우 레이어 기반 구조도 허용"
  → 메인테이너 토론 14일 개시
```

#### 시나리오 C: 보안 결함률 급감

```
[2028 H1 벤치마크 수집]
  → CyberSecEval: AI 생성 코드 보안 결함률 3%
  → Veracode 연간 보고서: 결함률 4%

[P7, P9 유효 조건 평가]
  → VC-P7-01: "보안 결함률이 유의미하게 높음"
  → threshold 5% 미만 → status: invalid
  → IT-P7-01 발동

[RFC 자동 생성]
  → 제목: "P7/P9 보안 가드레일 수준 재검토"
  → 주의: "보안은 결함률이 0%여도 가드레일이 필요한 영역.
           완전 제거가 아닌 '필수→권장' 전환만 논의"
  → 불변 핵심 규칙 참조: 보안 가드레일의 완전 제거는 허용하지 않음
```

### 3.4 벤치마크 수집 자동화

벤치마크 수집은 에이전트가 수행하되, 다음 원칙을 따른다:

1. **공식 소스만 사용**: 각 벤치마크의 공식 리더보드 또는 논문에서만 데이터 수집
2. **3개 이상 독립 소스에서 교차 확인**: 단일 소스의 수치를 신뢰하지 않음
3. **raw 데이터 보존**: 수집된 데이터는 `research/benchmarks/YYYY-QN/` 디렉토리에 원본 보관
4. **수집 에이전트 다양화**: 하나의 에이전트 모델에만 의존하지 않음

---

## 4. "진화적 방법론"으로서의 AIDE 리포지셔닝

### 4.1 현재 상태 진단

현재 AIDE v1.0의 한계:

| 측면 | 현재 상태 | 문제점 |
|-----|----------|-------|
| **문서 형태** | 정적 마크다운 | 원칙의 유효성이 변해도 문서가 자동으로 반영하지 않음 |
| **개정 주기** | "반기별 권장" (비구속적) | 구체적 트리거 없이 시간 기반 → 관성에 빠질 위험 |
| **피드백 루프** | 없음 | 채택 프로젝트의 실제 경험이 방법론에 환류되지 않음 |
| **에이전트 역할** | 문서의 "대상" | 방법론 유지보수의 "주체"가 아님 |
| **검증 체계** | 없음 | 원칙이 실제로 효과가 있는지 측정하지 않음 |

### 4.2 "살아있는 시스템"으로의 전환을 위한 구성요소

#### 4.2.1 방법론 리포지토리의 확장 구조

```
aide/
├── docs/                           # 현재와 동일 (방법론 문서)
│   ├── en/AIDE-METHODOLOGY.md
│   └── ko/AIDE-METHODOLOGY.md
│
├── meta/                           # [신규] 메타 레이어
│   ├── principle-metadata.yaml     # 원칙 메타데이터 (반감기 정보)
│   ├── dependency-map.yaml         # 원칙 간 의존성 맵
│   ├── evolution-log.yaml          # 진화 이력 로그
│   └── immutable-core.md           # 불변 메타 원칙
│
├── benchmarks/                     # [신규] 벤치마크 데이터
│   ├── collection-config.yaml      # 수집 대상 및 주기 설정
│   ├── 2026-Q1/                    # 분기별 수집 데이터
│   │   ├── raw/                    # 원본 데이터
│   │   ├── analysis.md             # 분석 보고서
│   │   └── trigger-evaluation.md   # 트리거 평가 결과
│   └── 2026-Q2/
│
├── adoption-feedback/              # [신규] 채택 피드백
│   ├── feedback-template.yaml      # 피드백 제출 양식
│   └── reports/                    # 수집된 피드백 보고서
│
├── research/                       # 현재와 동일 (리서치 보고서)
├── rfcs/                           # 현재와 동일 (RFC)
└── examples/                       # 현재와 동일 (예시)
```

#### 4.2.2 재귀적 구조: 에이전트가 방법론을 유지보수

AIDE는 P10에서 "Meta-Code as First-Class"를 선언한다. 이 원칙을 방법론 자체에 적용하면:

**AIDE 방법론 문서 자체가 AIDE의 원칙을 따르는 프로젝트가 된다.**

| AIDE 원칙 | 방법론 리포지토리에의 적용 |
|-----------|------------------------|
| P1 Context Budget | 방법론 문서도 300줄 단위로 분리 (이미 영문/한국어 분리) |
| P5 Test as Spec | 원칙의 유효성을 벤치마크로 "테스트" |
| P7 Guardrails | 원칙 변경에 대한 결정적 안전장치 (RFC, 투표, 롤백) |
| P8 Observability | 진화 이력 로그로 방법론 변경을 추적 |
| P10 Meta-Code | principle-metadata.yaml이 방법론의 "메타코드" |

이 재귀적 구조는 다음을 의미한다:

> **AIDE의 10번째 원칙(Meta-Code as First-Class)이 AIDE 자체에 적용되어,
> AIDE의 메타데이터(principle-metadata.yaml)가 AIDE의 진화를 제어한다.**

#### 4.2.3 에이전트 역할 정의

"살아있는 시스템"에서 에이전트의 구체적 역할:

| 역할 | 수행 에이전트 | 주기 | 산출물 |
|-----|------------|------|-------|
| **벤치마크 수집자** | GPT/Claude/Gemini (순환) | 분기별 | `benchmarks/YYYY-QN/raw/` |
| **트리거 평가자** | CTO 에이전트 (복수 모델 합의) | 분기별 | `benchmarks/YYYY-QN/trigger-evaluation.md` |
| **RFC 초안 작성자** | 트리거 발동 시 지정 에이전트 | 수시 | `rfcs/NNNN-*.md` |
| **번역 동기화자** | 지정 에이전트 | 문서 변경 시 | 영문/한국어 동기화 |
| **채택 피드백 분석자** | 지정 에이전트 | 반기별 | `adoption-feedback/reports/` |

**인간의 역할**:
- 최종 승인권 (RFC 결정)
- 불변 핵심 수호
- 에이전트 역할 할당 및 감독
- 채택 경험 피드백 제공

#### 4.2.4 진화 이력 로그 (Evolution Log)

```yaml
# meta/evolution-log.yaml
events:
  - id: EV-001
    date: "2026-02-18"
    type: "initial_release"
    version: "1.0.0"
    description: "AIDE v1.0 최초 릴리스"
    principles_affected: ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10"]
    evidence: "research/ 디렉토리의 6개 리서치 보고서"
    decision_by: "CTO (human)"

  # 향후 예시:
  - id: EV-002
    date: "2026-08-20"  # 예시
    type: "guideline_adjustment"
    version: "1.1.0"
    description: "P1 파일 크기 상한 300줄 → 400줄 조정"
    trigger: "IT-P1-03"
    principles_affected: ["P1"]
    evidence: "benchmarks/2026-Q2/trigger-evaluation.md"
    rfc: "rfcs/0001-context-budget-adjustment.md"
    decision_by: "maintainer-team"
    rollback_until: "2026-11-20"
```

### 4.3 전환 로드맵

현재 v1.0 정적 문서에서 살아있는 시스템으로의 전환:

```
Phase 0 (즉시): 설계 문서 완성 및 커뮤니티 공유
  → 이 설계서를 RFC로 제출
  → 커뮤니티 피드백 수집

Phase 1 (v1.1, 1개월 내): 메타데이터 인프라 구축
  → principle-metadata.yaml 작성 (10개 원칙 모두)
  → dependency-map.yaml 작성
  → immutable-core.md 작성
  → meta/ 디렉토리 생성

Phase 2 (v1.2, 3개월 내): 첫 번째 벤치마크 사이클
  → benchmarks/ 디렉토리 구조 생성
  → 2026-Q1 벤치마크 수집 (수동)
  → 트리거 평가 수행 (수동)
  → 프로세스 검증 및 개선

Phase 3 (v1.3, 6개월 내): 자동화 도입
  → 벤치마크 수집 에이전트 워크플로우 구축
  → GitHub Actions 기반 분기별 자동 이슈 생성
  → 채택 피드백 수집 체계 구축

Phase 4 (v2.0, 12개월 내): 완전한 자기진화 시스템
  → 첫 번째 자동 트리거 기반 RFC 생성 및 처리 완료
  → 최소 2회의 벤치마크 사이클 완료
  → 진화 이력 로그에 실제 이벤트 누적
  → "진화적 방법론" 공식 선언
```

---

## 5. 종합: AIDE가 "살아있는 방법론"이 되기 위한 핵심 원리

### 5.1 세 가지 피드백 루프

AIDE가 자기진화하기 위해서는 세 가지 피드백 루프가 동시에 작동해야 한다:

```
루프 1: 기술 환경 피드백 (외부 → 방법론)
[에이전트 벤치마크 변화] → [반감기 트리거] → [원칙 재검토] → [방법론 업데이트]

루프 2: 채택 경험 피드백 (실무 → 방법론)
[채택 프로젝트 메트릭] → [패턴 분석] → [가이드라인 개선] → [방법론 업데이트]

루프 3: 자기 검증 피드백 (방법론 → 방법론)
[방법론 변경] → [변경 후 메트릭 관찰] → [효과 검증] → [롤백 or 확정]
```

### 5.2 핵심 설계 원칙 요약

1. **관측 가능한 유효 조건**: 모든 원칙에 측정 가능한 유효 조건과 임계값을 명시한다
2. **자동 트리거, 인간 결정**: 트리거 감지는 자동화하지만, 변경 결정은 인간이 한다
3. **증거 기반 진화**: "느낌"이 아닌 벤치마크와 데이터로 진화한다
4. **안전한 진화**: 롤백 메커니즘, 쿨다운 기간, 불변 핵심으로 위험을 관리한다
5. **재귀적 자기적용**: AIDE의 원칙이 AIDE 자체에 적용되는 재귀 구조를 취한다

### 5.3 인간 관리 의존성 제거를 위한 답변

AIDE v1.0의 구조적 한계(인간이 방법론을 지속적으로 정의/관리해야 함)에 대한 이 설계서의 답변:

> **에이전트가 "감지하고 제안하고 실행"하며, 다중 에이전트 합의와 경험적 검증이 인간 판단을 대체한다.**

- 모델 발전에 따른 방법론 정의 → **반감기 프레임워크 + 벤치마크 자동 추적**
- 표준화 → **Self-Amending Protocol + 버전 관리 체계**
- 인간 역할 제거 → **다중 에이전트 적대적 합의 + Empirical Gate로 완전 대체**

인간의 관여 없이도 방법론이 자율적으로 진화할 수 있는 구조를 설계한다. 불변 공리(Axioms)는 결과 기반으로 정의되어 에이전트 자신도 수정 불가능하며, 적응형 원칙은 벤치마크 데이터에 의해 자동 캘리브레이션된다.

---

*이 설계서는 AIDE v1.0의 정적 한계를 해결하기 위한 초안이며, RFC 프로세스를 통해 커뮤니티 검토를 거쳐야 한다.*
