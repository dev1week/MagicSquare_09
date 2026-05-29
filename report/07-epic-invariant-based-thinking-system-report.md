# Level 1: Epic — Business Goal

## 1. Epic Title

**불변식 기반 사고 훈련 시스템 구축**

4x4 Magic Square 문제를 매개로, 도메인 불변식(Invariant)을 중심에 두고 Dual-Track UI + Logic TDD 방식으로 설계·검증·구현 역량을 체계적으로 훈련하는 학습 시스템을 구축한다.

---

## 2. Business Goal

Magic Square 4x4 문제를 **단순 퍼즐 풀이 도구**가 아니라 **설계·테스트·구현 역량을 동시에 훈련하는 교육용 시스템**으로 정의한다.

이 Epic의 비즈니스 목표는 다음과 같다.

- 학습자가 "기능 구현"보다 먼저 **도메인 불변식을 식별하고 설계에 반영**하는 습관을 갖도록 한다.
- UI 흐름과 도메인 로직을 분리하는 **Dual-Track 접근**으로, 사용자 경험과 비즈니스 규칙을 각각 독립적으로 검증할 수 있게 한다.
- 입력/출력 계약(Contract)을 명확히 정의하여, **경계(Boundary)에서의 검증 실패를 조기에 발견**할 수 있게 한다.
- 설계 → 테스트 → 구현 → 리팩토링의 TDD 사이클을 반복 가능한 **학습 루틴**으로 고정한다.
- Concept → Invariant → Contract → Test 간 **추적성(Traceability)** 을 확보하여, "왜 이 테스트가 존재하는가"를 항상 설명할 수 있게 한다.

궁극적으로, Magic Square 프로젝트는 **정답을 맞히는 결과**보다 **불변식 중심으로 올바르게 설계하고 검증하는 과정**을 성공으로 정의한다.

---

## 3. Learning Goal

이 Epic을 완료한 학습자는 다음 역량을 갖춘다.

| 영역 | 학습 목표 |
|------|-----------|
| **불변식 사고** | 4x4 Magic Square의 핵심 규칙을 Invariant로 명문화하고, 설계·테스트·코드에 일관되게 반영할 수 있다. |
| **Dual-Track TDD** | UI Track과 Logic Track을 분리하여, 각각에 맞는 테스트 전략을 선택하고 적용할 수 있다. |
| **계약 설계** | Boundary의 입력/출력 계약을 정의하고, 유효·무효 입력에 대한 검증 책임을 명확히 구분할 수 있다. |
| **TDD 사이클** | Red → Green → Refactor 흐름을 의도적으로 수행하며, 리팩토링 후에도 외부 계약이 유지됨을 확인할 수 있다. |
| **추적성** | Concept, Invariant, Contract, Test 간 연결 관계를 문서·테스트·코드에서 추적할 수 있다. |
| **도메인 표현** | 매직 넘버를 배제하고 `GRID_SIZE`, `MAX_VALUE`, `MAGIC_CONSTANT` 등 **의미 있는 상수**로 도메인을 표현할 수 있다. |

---

## 4. Problem Statement

4x4 Magic Square는 겉보기에는 단순한 숫자 배치 문제이지만, 실제 소프트웨어 설계 관점에서는 다음과 같은 복합 문제다.

- **도메인 규칙**이 명확하지 않으면 구현이 ad-hoc(임시방편)으로 흐르기 쉽다.
- **입력 검증**과 **핵심 로직**이 섞이면 테스트가 brittle(취약)해지고 리팩토링이 어려워진다.
- UI와 Logic을 동시에 개발하면 **어디서 실패했는지** 원인 분리가 어렵다.
- "정답을 맞힌다"는 목표만 두면 **설계 품질·테스트 품질·유지보수성**이 학습 범위에서 빠진다.

따라서 이 프로젝트는 Magic Square를 **도메인 불변식 훈련용 사례(Case Study)** 로 사용하여, 작지만 완결된 설계·테스트·구현 사이클을 경험하게 한다.

**핵심 문제 정의:**

> 4x4 Magic Square를 해결하는 시스템을 만들되, 정답 산출 자체보다 **불변식 기반 설계와 Dual-Track TDD를 통해 검증 가능한 소프트웨어를 만드는 능력**을 훈련한다.

---

## 5. Target Learners / Users

### Primary: 학습자 (Developer Trainee)

- TDD, Clean Architecture, ECB(Entity–Control–Boundary) 개념을 **실습 중심**으로 익히려는 개발자
- "코드는 짰는데 왜 테스트가 깨지는지", "리팩토링이 무서운지"를 경험한 초·중급 개발자
- Magic Square를 통해 **작은 도메인에서 설계 원칙을 반복 훈련**하려는 학습자

### Secondary: 리뷰어 / 멘토

- 학습자의 Concept → Invariant → Contract → Test 추적성을 검토하는 코드 리뷰어
- Domain Logic 커버리지, Boundary 계약 테스트, 불변식-테스트 매핑을 기준으로 피드백하는 교육 담당자

### Tertiary: 프로젝트 운영자

- Magic Square TDD Practice 커리큘럼을 운영·확장하는 관리자
- Epic → User Story → Task 구조로 학습 진행도를 관리하는 역할

---

## 6. Scope

Epic 수준에서 포함하는 범위는 **"불변식 기반 사고 훈련 시스템"을 정의하고, 그 성공 기준과 추적 규칙을 확립**하는 것이다.

### 포함

- 4x4 Magic Square 도메인에 대한 **비즈니스 목표·학습 목표** 정의
- Dual-Track(UI + Logic) TDD 적용 원칙 수립
- Boundary 입력/출력 **계약(Contract)** 정의 원칙
- Domain Logic과 Boundary 검증의 **책임 분리** 원칙
- Concept → Invariant → Contract → Test **추적성 규칙** 정의
- 성공 기준(커버리지, 계약 테스트, 상수 명명, 하드코딩 금지, 리팩토링 후 계약 유지) 확립
- Level 2 User Story 도출을 위한 **후보 영역** 식별

### 도메인 맥락 (Epic에서 전제하는 Magic Square 규칙)

- 격자 크기: 4×4 (`GRID_SIZE = 4`)
- 사용 숫자: 1부터 16까지 각각 한 번 (`MAX_VALUE = 16`)
- 모든 행, 열, 대각선의 합이 동일 (`MAGIC_CONSTANT = 34`)
- 위 규칙은 **Invariant**로 취급하며, Level 2 이후 User Story·Task로 세분화한다.

---

## 7. Non-Scope

Epic 단계에서는 다음을 **의도적으로 포함하지 않는다**.

| 제외 항목 | 사유 |
|-----------|------|
| 구체적 User Story 작성 | Level 2에서 수행 |
| Task 단위 작업 분해 | Level 3에서 수행 |
| 구현 코드 작성 | Epic은 목표·원칙 정의만 |
| 테스트 코드 작성 | Epic은 성공 기준·추적 규칙만 |
| UI 상세 화면 설계 | Dual-Track 원칙만 정의, 상세는 User Story |
| 4×4 이외 Magic Square 일반화 (3×3, n×n) | 학습 범위 집중 |
| 성능 최적화, 병렬 처리, 캐싱 | 교육 목적 범위 밖 |
| 인증/권한, 다중 사용자, 영속 저장소 | 도메인 훈련과 무관 |
| 정답 하드코딩 또는 lookup table 방식 | 학습 목표(불변식 기반 설계)와 상충 |
| 배포·CI/CD 파이프라인 구축 | Epic 범위 밖 (후속 Epic 가능) |

---

## 8. Success Criteria

Epic "불변식 기반 사고 훈련 시스템 구축"의 완료는 **기능 완성**이 아니라 **훈련 시스템의 검증 가능한 품질 기준 충족**으로 판단한다.

### 8.1 품질 기준

| # | 기준 | 측정 방법 |
|---|------|-----------|
| SC-1 | Domain Logic 테스트 커버리지 **95% 이상** | Logic Track 단위 테스트 커버리지 리포트 |
| SC-2 | Boundary 입력 검증 계약 테스트 **100% 통과** | Contract Test Suite 전체 Green |
| SC-3 | 설명 없는 매직 넘버 **금지** | 코드 리뷰 + 정적 점검 |
| SC-4 | `GRID_SIZE`, `MAX_VALUE`, `MAGIC_CONSTANT` 등 **명명된 상수** 사용 | 도메인 상수 정의 및 참조 확인 |
| SC-5 | 정답 **하드코딩 금지** | 구현이 Invariant 기반 알고리즘/규칙으로 도출되는지 검증 |
| SC-6 | 주요 Invariant마다 **최소 1개 이상의 테스트** 존재 | Invariant ↔ Test 매핑표 |
| SC-7 | 리팩토링 후 **외부 입력/출력 계약 불변** | Contract Test 회귀 Green |

### 8.2 프로세스 기준

| # | 기준 | 확인 방법 |
|---|------|-----------|
| SC-8 | Dual-Track(UI + Logic) TDD 사이클 준수 | Red → Green → Refactor 이력 |
| SC-9 | Concept → Invariant → Contract → Test 추적성 확보 | 추적 매트릭스 작성 |
| SC-10 | ECB 책임 분리 준수 | Entity에 I/O·프레임워크 의존 없음 |

### 8.3 Epic 완료 판정

다음이 모두 충족되면 Epic Level 1을 완료한 것으로 본다.

- [ ] Business Goal과 Learning Goal가 팀/학습자에게 공유·합의됨
- [ ] Scope / Non-Scope 경계가 명확함
- [ ] Success Criteria가 측정 가능함
- [ ] Key Invariant 목록이 정의됨
- [ ] Traceability Rule이 확립됨
- [ ] Level 2 User Story 후보가 식별됨

---

## 9. Key Invariants

Epic 수준에서 식별하는 **핵심 불변식**. Level 2 User Story에서 각 Invariant를 검증·구현 책임으로 분배한다.

### INV-1: Grid Dimension Invariant

> Magic Square 격자는 항상 4×4이다.

- 상수: `GRID_SIZE = 4`
- 의미: 입력·출력·내부 표현 모두 4×4 구조를 전제로 한다.

### INV-2: Value Range & Uniqueness Invariant

> 격자 각 칸의 값은 1 이상 16 이하의 정수이며, 1~16은 정확히 한 번씩만 등장한다.

- 상수: `MAX_VALUE = 16`
- 의미: 중복·누락·범위 초과는 유효한 Magic Square가 아니다.

### INV-3: Magic Sum Invariant

> 모든 행, 모든 열, 두 대각선의 합은 동일하다.

- 상수: `MAGIC_CONSTANT = 34`
- 의미: Magic Square의 본질적 규칙. 개별 합 검증과 전체 일치 검증으로 분해 가능.

### INV-4: Input Validity Invariant (Boundary)

> Boundary에 들어오는 모든 외부 입력은 계약(Contract)에 정의된 형식·범위·타입을 만족해야 하며, 위반 시 도메인 로직으로 전달되지 않는다.

- 의미: Boundary가 "문지기" 역할. Entity/Control은 유효 입력만 처리한다.

### INV-5: Contract Stability Invariant

> 리팩토링은 내부 구현만 변경할 수 있으며, Boundary의 외부 입력/출력 계약은 변경되지 않는다.

- 의미: TDD Refactor 단계의 안전망. Contract Test가 회귀 방지 역할.

### INV-6: Traceability Invariant

> 모든 주요 Invariant는 Concept에서 출발하여, Contract와 Test에 추적 가능해야 한다.

- 의미: "왜 이 테스트가 있는가"에 항상 답할 수 있어야 한다.

---

## 10. Traceability Rule

Epic 수준에서 확립하는 **추적성 규칙**. Level 2 User Story 작성 시 각 Story가 이 규칙을 따르도록 한다.

### 10.1 추적 체인

```
Concept → Invariant → Contract → Test → Implementation
```

| 단계 | 정의 | 산출물 예시 |
|------|------|-------------|
| **Concept** | 비즈니스/도메인 개념 | "4×4 격자에 1~16을 배치한다" |
| **Invariant** | 항상 참이어야 하는 규칙 | INV-1 ~ INV-6 |
| **Contract** | Boundary 입·출력 명세 | 입력 형식, 오류 응답, 성공 응답 |
| **Test** | Invariant/Contract 검증 | 단위 테스트, 계약 테스트 |
| **Implementation** | 테스트를 통과하는 코드 | Entity, Control, Boundary |

### 10.2 추적성 매트릭스 (Epic 템플릿)

| Concept ID | Invariant ID | Contract ID | Test ID | 비고 |
|------------|--------------|-------------|---------|------|
| C-01 | INV-1 | BC-01 | T-01 | Grid 4×4 |
| C-02 | INV-2 | BC-02 | T-02 | Value 1~16 unique |
| C-03 | INV-3 | BC-03 | T-03 | Sum = 34 |
| C-04 | INV-4 | BC-04 | T-04 | Boundary validation |
| C-05 | INV-5 | BC-05 | T-05 | Contract regression |
| C-06 | INV-6 | — | — | Meta-rule |

> Test ID, Contract ID는 Level 2 User Story 작성 시 구체화한다.

### 10.3 Dual-Track 추적 규칙

| Track | 책임 | 추적 대상 |
|-------|------|-----------|
| **Logic Track** | Domain Invariant 검증 | INV-1, INV-2, INV-3 |
| **UI Track** | 사용자 흐름·표현 | 입력 수집, 결과 표시, 오류 피드백 |
| **Boundary Track** | Contract 검증 | INV-4, INV-5 |

Logic Track과 Boundary Track은 **독립적으로 테스트**하되, Contract를 통해 연결한다.

### 10.4 금지 규칙

- Invariant 없이 Test를 작성하지 않는다.
- Contract 없이 Boundary 검증 Test를 작성하지 않는다.
- Test 없이 Invariant를 "완료"로 표시하지 않는다.
- Concept → Implementation 직행(중간 단계 생략)을 허용하지 않는다.

---

## 11. Candidate User Stories for Level 2

Epic을 User Story로 세분화할 때 참고할 **후보 영역**이다.  
아직 Story 문장·AC·Task는 작성하지 않는다.

| # | 후보 영역 | 관련 Invariant | Track | Level 2에서 다룰 내용 (예고) |
|---|-----------|----------------|-------|------------------------------|
| US-CAND-01 | **격자 구조 정의** | INV-1 | Logic | 4×4 Grid 표현, `GRID_SIZE` 상수 |
| US-CAND-02 | **값 범위·유일성 검증** | INV-2 | Logic | 1~16 중복/누락/범위 검증 |
| US-CAND-03 | **매직 합 검증** | INV-3 | Logic | 행·열·대각선 합 = `MAGIC_CONSTANT` |
| US-CAND-04 | **Magic Square 유효성 판정** | INV-1,2,3 | Logic | 전체 Invariant 통합 판정 |
| US-CAND-05 | **Magic Square 생성/완성** | INV-1,2,3 | Logic | Invariant를 만족하는 배치 도출 (하드코딩 금지) |
| US-CAND-06 | **Boundary 입력 계약 정의** | INV-4 | Boundary | 입력 형식·타입·범위 Contract |
| US-CAND-07 | **Boundary 오류 응답 계약** | INV-4 | Boundary | 무효 입력 시 일관된 오류 Contract |
| US-CAND-08 | **Contract 회귀 테스트** | INV-5 | Boundary | 리팩토링 후 Contract 불변 검증 |
| US-CAND-09 | **사용자 입력 UI 흐름** | INV-4 | UI | 입력 수집·피드백·재시도 |
| US-CAND-10 | **결과 표시 UI** | INV-3 | UI | Magic Square 결과 시각화 |
| US-CAND-11 | **추적성 매트릭스 관리** | INV-6 | Process | Concept-Invariant-Test 매핑 유지 |
| US-CAND-12 | **TDD 사이클 실습 루틴** | INV-5,6 | Process | Red→Green→Refactor 학습 가이드 |

---

**Epic Level 1 완료.**  
다음 단계(Level 2)에서는 위 Candidate User Stories를 **"As a … I want … So that …"** 형식의 User Story로 구체화하고, Acceptance Criteria와 Invariant 매핑을 추가한다.
