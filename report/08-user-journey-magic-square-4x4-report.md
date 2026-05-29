# Level 2: User Journey — Magic Square 4x4

## 1. Persona

**이름:** 김학습 (가칭)  
**역할:** TDD와 Clean Architecture를 실습 중인 소프트웨어 개발 학습자

| 속성 | 설명 |
|------|------|
| **배경** | Python 기초는 갖추었으나, TDD·계층 분리·계약 설계를 실전 문제에 적용해 본 경험은 제한적 |
| **동기** | 알고리즘 정답 획득보다 **설계 → 테스트 → 구현 → 리팩토링** 흐름을 반복 훈련하고 싶음 |
| **과제 인식 전** | Magic Square를 "숫자 채우기 알고리즘 문제"로 볼 가능성이 높음 |
| **과제 인식 후** | Magic Square를 **불변식·계약·책임 분리를 훈련하는 Case Study**로 인식 |
| **성공 기준 (학습자 관점)** | 리팩토링 후에도 Contract Test가 Green이고, Invariant마다 추적 가능한 Test가 존재 |

---

## 2. Journey Goal

학습자는 4×4 Magic Square 문제를 한 번의 코딩 과제가 아니라 **5단계 학습 여정**으로 경험한다.

| # | Journey Goal |
|---|--------------|
| JG-1 | Magic Square를 **불변식 중심 설계 훈련 문제**로 인식한다 |
| JG-2 | **입력/출력/오류 계약**을 구현보다 먼저 정의한다 |
| JG-3 | BlankFinder, MissingNumberFinder, MagicSquareValidator, Solver로 **도메인 책임을 분리**한다 |
| JG-4 | **Dual-Track TDD**(UI/Boundary Track + Logic/Domain Track)를 분리하여 Red → Green → Refactor를 수행한다 |
| JG-5 | Edge case, Input error, Combination failure, Output format을 **회귀 테스트로 보호**한다 |

---

## 3. Journey Overview

| Stage | User Action | Thinking | Pain Point | Opportunity | Learning Outcome |
|-------|-------------|----------|------------|-------------|------------------|
| **1. Problem Recognition** | 과제 설명과 Magic Square 규칙을 읽고, "구현 문제" vs "설계 훈련 문제"를 구분한다 | "정답을 빨리 맞히는 것보다, 어떤 규칙이 항상 참이어야 하는가?" | 규칙(빈칸 2개, 0 허용, 1-index 좌표, 조합 시도 순서)이 많아 한 번에 구현하려는 충동 | 규칙을 Invariant 목록으로 정리하면 구현 순서가 자연스럽게 드러남 | Magic Square를 **Invariant 목록 + Contract 정의 문제**로 재정의 |
| **2. Contract Definition** | 입력 4×4 행렬, 출력 int[6], 오류 조건을 문서·테스트 명세로 먼저 작성한다 | "Boundary에서 무엇을 거부하고, Control/Entity에는 무엇만 전달하는가?" | 입력 검증과 Solver 로직을 한 테스트에 섞으면 실패 원인 분리가 어려움 | Contract-first 접근으로 Boundary Test와 Domain Test를 분리 가능 | **Input / Output / Error Contract**를 테스트 가능한 형태로 확정 |
| **3. Domain Separation** | BlankFinder → MissingNumberFinder → MagicSquareValidator → Solver 순으로 책임을 나눈다 | "이 함수는 '찾기'인가, '검증'인가, '시도'인가?" | 모든 로직을 Solver 하나에 넣으면 테스트 작성·리팩토링이 어려움 | 작은 단위로 나누면 Invariant별 테스트 매핑이 명확해짐 | **단일 책임 도메인 단위**로 분리하고 Invariant와 연결 |
| **4. Dual-Track TDD Progress** | UI/Boundary Track과 Logic Track을 각각 Red → Green → Refactor 한다 | "지금 실패하는 테스트는 Contract인가, Invariant인가?" | 두 Track을 동시에 Red로 만들면 어디서부터 Green을 만들지 혼란 | Track 분리로 **최소 구현(Green) 범위**를 명확히 제한 | Dual-Track TDD 사이클을 **의도적으로** 경험 |
| **5. Regression Protection** | Edge, Input error, Combination failure, Output format 케이스를 추가한다 | "리팩토링 후에도 계약과 불변식이 깨지지 않는가?" | Happy path만 테스트하면 리팩토링 시 조용히 회귀 | 회귀 테스트가 Refactor 단계의 **안전망** 역할 | **Contract + Invariant 회귀 보호** 체계 확립 |

---

## 4. Detailed Journey

### Stage 1: Problem Recognition

- **Action:**
  - Magic Square 4×4 과제 설명, 입·출력 규칙, Magic Constant(34), Solver 시도 전략(작은 누락 숫자 → 첫 빈칸, 큰 누락 숫자 → 두 번째 빈칸, 실패 시 역조합)을 읽는다.
  - "구현해야 할 기능" 목록 대신 **"항상 참이어야 하는 규칙(Invariant)"** 목록을 작성한다.
  - Epic 목표(불변식 기반 사고 훈련)와 본 과제의 연결점을 메모한다.

- **Thinking:**
  - "이 문제의 핵심은 마방진을 '만드는 것'인가, '규칙을 지키며 채우는 것'인가?"
  - "빈칸 2개, 0의 의미, 1-index 좌표, int[6] 출력 — 이 중 어떤 것이 Invariant이고 어떤 것이 Contract인가?"
  - "Solver의 두 번 시도(정방향 조합 → 역조합)는 알고리즘 전략이지, Invariant가 아니다."

- **Emotion:**
  - 초기: 규칙이 많아 압도감 ("한 파일에 다 짜면 될 것 같은데…")
  - 전환: Invariant 목록 작성 후 안도감 ("구현 순서가 보인다")
  - 확신: "정답 하드코딩이 아니라 규칙 기반 설계가 과제의 본질"이라 인식

- **Pain Point:**
  - 규칙(0=빈칸, 정확히 2개, 1~16 중복 불가, 1-index, [r1,c1,n1,r2,c2,n2])을 한꺼번에 코드로 옮기려는 충동
  - Magic Constant 34, 조합 시도 순서를 Invariant와 혼동
  - "알고리즘 문제" 프레임에 갇혀 Contract 정의를 미루는 경향

- **Opportunity:**
  - 규칙을 INV-Grid, INV-BlankCount, INV-ValueRange, INV-Uniqueness, INV-MagicSum, INV-Coordinate, INV-OutputFormat 등으로 **명명·분류**
  - Solver 전략(작은/큰 누락 숫자 배치, 역조합)을 **별도 책임**으로 분리할 여지 확보
  - Epic의 Traceability Rule(Concept → Invariant → Contract → Test) 적용 시작점

- **Related Invariant:**
  - **INV-1 (Grid):** 입력은 4×4 int 행렬
  - **INV-2 (Blank):** 0은 빈칸, 빈칸은 정확히 2개
  - **INV-3 (Value Range):** 값은 0 또는 1~16
  - **INV-4 (Uniqueness):** 0을 제외한 숫자는 중복 불가
  - **INV-5 (Magic Sum):** 완성된 4×4 마방진의 행·열·대각선 합 = 34
  - **INV-6 (Coordinate):** 출력 좌표는 1-index
  - **INV-7 (Output Shape):** 출력은 int[6], 형식 [r1, c1, n1, r2, c2, n2]

- **Expected Learning Outcome:**
  - Magic Square를 **"불변식 + 계약 + Solver 전략"** 3층으로 인식
  - 구현 전 Invariant 목록을 작성하는 습관 형성
  - 정답 하드코딩·lookup table 접근을 스스로 거부

---

### Stage 2: Contract Definition

- **Action:**
  - Boundary 입·출력·오류 계약을 문서화한다 (코드 작성 전).
  - Input Contract: 4×4 int 행렬의 유효 조건 정의
  - Output Contract: 성공 시 int[6] 반환 형식 정의
  - Error Contract: 무효 입력·Solver 실패 시 동작 정의
  - Contract Test 명세(아직 코드 아님)를 Red 목록으로 작성

- **Thinking:**
  - "Boundary는 어디까지 검증하고, Domain으로 넘기는가?"
  - "빈칸이 2개가 아니면 Error Contract의 어떤 케이스인가?"
  - "Solver가 두 조합 모두 실패하면 Output Contract인가 Error Contract인가?"
  - "1-index 좌표와 0-based 내부 표현의 변환 책임은 Boundary인가 Control인가?"

- **Emotion:**
  - Contract 작성 중: 형식을 정해야 한다는 부담
  - Contract 확정 후: "테스트를 어디에 쓸지" 명확해져 자신감 상승
  - Boundary vs Domain 경계가 보일 때: 설계 이해도 증가

- **Pain Point:**
  - 입력 검증(형식·범위·빈칸 수)과 Solver 로직을 하나의 테스트에 섞는 실수
  - 오류 응답 형식(예외 타입, 메시지, 반환값)을 미정의 상태로 Green 진행
  - 1-index vs 0-index 혼용으로 Output Contract 테스트 불일치

- **Opportunity:**
  - Contract-first로 **Boundary Test Suite**와 **Domain Test Suite** 분리
  - Error Contract를 명시하여 Stage 5 회귀 테스트 설계의 기반 마련
  - Epic SC-2(Boundary 계약 테스트 100% 통과) 측정 가능한 기준 확보

- **Input Contract:**
  - **IC-1:** 입력은 4×4 2차원 int 배열(또는 동등 표현)
  - **IC-2:** 각 원소 값 ∈ {0} ∪ {1, 2, …, 16}
  - **IC-3:** 0(빈칸)의 개수 = 2 (정확히)
  - **IC-4:** 0을 제외한 값은 Set 크기 = (16 − 2) = 14 (중복 없음, 누락 숫자 2개 존재)
  - **IC-5:** IC-1~IC-4 위반 시 Boundary에서 거부, Domain 로직 미호출

- **Output Contract:**
  - **OC-1:** 성공 시 반환값은 길이 6의 int 배열
  - **OC-2:** 형식: `[r1, c1, n1, r2, c2, n2]`
  - **OC-3:** r1, c1, r2, c2는 1-index (1 ≤ r, c ≤ 4)
  - **OC-4:** n1, n2는 각 빈칸에 채울 누락 숫자 (1~16, 서로 다름)
  - **OC-5:** (r1,c1)과 (r2,c2)는 입력에서 0이었던 좌표와 일치
  - **OC-6:** 제안된 n1, n2 배치 후 INV-5(Magic Sum = 34) 만족

- **Error Contract:**
  - **EC-1:** 입력 형식 오류 (4×4 아님, int 아님) → Boundary 거부, 명시적 오류
  - **EC-2:** 값 범위 위반 (0, 1~16 외) → Boundary 거부
  - **EC-3:** 빈칸 개수 ≠ 2 → Boundary 거부
  - **EC-4:** 0 제외 숫자 중복 → Boundary 거부
  - **EC-5:** Solver 전략(작은→큰, 역조합) 모두 실패 → 명시적 실패 응답 (형식은 프로젝트 Error Contract 표준에 따름)
  - **EC-6:** 모든 오류는 **일관된 예외 타입 또는 오류 코드**로 표현 (구현 세부는 User Story에서 확정)

- **Expected Learning Outcome:**
  - **Contract-first** 설계: 구현 전 Input / Output / Error Contract 확정
  - Boundary Test와 Domain Test의 **범위·책임 분리** 이해
  - 테스트 가능한 계약 명세 작성 능력

---

### Stage 3: Domain Separation

- **Action:**
  - Magic Square 문제를 4개 도메인 단위로 분리한다.
  - 각 단위의 **단일 책임**, **입력/출력**, **연관 Invariant**를 정의한다.
  - ECB 관점에서 Entity(도메인 규칙) vs Control(흐름 조율) vs Boundary(입출력) 배치를 논의한다.
  - Solver가 BlankFinder, MissingNumberFinder, MagicSquareValidator를 **조합**하는 흐름을 설계한다.

- **Thinking:**
  - "BlankFinder는 '0의 좌표'만 반환해야 하는가?"
  - "MissingNumberFinder는 1~16 중 입력에 없는 2개 숫자만 반환해야 하는가?"
  - "MagicSquareValidator는 채워진 4×4가 Magic Sum=34를 만족하는지만 판단해야 하는가?"
  - "Solver는 '작은 누락→첫 빈칸, 큰 누락→둘째 빈칸' 시도와 역조합만 담당해야 하는가?"

- **Emotion:**
  - 분리 설계 중: "이름 짓기와 경계 정하기"에 집중
  - 책임이 명확해질 때: 테스트 작성 자신감
  - Solver가 다른 단위를 orchestrate하는 그림이 보일 때: Control 계층 이해 증가

- **Pain Point:**
  - BlankFinder + MissingNumberFinder + Validator + Solver를 **하나의 함수**에 넣는 유혹
  - Validator가 "빈칸 찾기"까지 하려는 책임 침범
  - Solver가 입력 검증(Boundary 책임)까지 흡수

- **Opportunity:**
  - Invariant별로 **테스트 대상 단위** 1:1 매핑 가능
  - Solver 전략(정방향/역조합)만 교체·확장 가능한 구조
  - 리팩토링 시 단위 테스트로 **국소 회귀** 탐지

- **Responsibility Separation:**

  | Domain Unit | 단일 책임 | 입력 | 출력 | 연관 Invariant |
  |-------------|-----------|------|------|----------------|
  | **BlankFinder** | 4×4 격자에서 0(빈칸) 좌표 탐색 | 4×4 int 행렬 (유효 입력 가정) | 2개 좌표 (1-index: r1,c1,r2,c2 순서) | INV-2, INV-6 |
  | **MissingNumberFinder** | 1~16 중 입력에 없는 2개 숫자 탐색 | 4×4 int 행렬 (유효 입력 가정) | 2개 int (작은 값, 큰 값 순 정렬 권장) | INV-3, INV-4 |
  | **MagicSquareValidator** | 완성된 4×4가 Magic Square인지 판정 | 4×4 int 행렬 (0 없음 가정) | bool (valid / invalid) | INV-1, INV-5 |
  | **Solver** | 누락 숫자 2개를 빈칸 2개에 배치 시도 (정방향 → 역조합) | BlankFinder 출력 + MissingNumberFinder 출력 + 원본 격자 | OC-1~OC-6 형식의 int[6] 또는 실패 | INV-5, INV-7, Solver 전략 |

  **Control (흐름 조율):** Boundary 검증 통과 후 BlankFinder → MissingNumberFinder → Solver(내부에서 Validator 호출) 순서 orchestration

  **Boundary:** IC-1~IC-5 검증, 입·출력 형식 변환(필요 시), Error Contract 적용

- **Related Invariant:**
  - BlankFinder ↔ INV-2, INV-6
  - MissingNumberFinder ↔ INV-3, INV-4
  - MagicSquareValidator ↔ INV-1, INV-5
  - Solver ↔ INV-5, INV-7 + Solver 전략(작은/큰 배치, 역조합)

- **Expected Learning Outcome:**
  - **단일 책임** 도메인 단위 설계
  - ECB 계층 분리(Entity=규칙, Control=흐름, Boundary=Contract) 이해
  - Invariant ↔ Domain Unit **추적 가능한 매핑** 확립

---

### Stage 4: Dual-Track TDD Progress

- **Action:**
  - **Track A (UI/Boundary):** Input/Output/Error Contract Test를 Red → Green → Refactor
  - **Track B (Logic/Domain):** BlankFinder, MissingNumberFinder, MagicSquareValidator, Solver 단위 Test를 Red → Green → Refactor
  - 두 Track을 **병렬이 아닌 순차적 우선순위**로 진행 (Boundary Contract Green 후 Domain Green)
  - 각 Green 단계에서 **최소 구현**만 작성
  - Refactor 단계에서 중복 제거·명명 상수 도입(`GRID_SIZE`, `MAX_VALUE`, `MAGIC_CONSTANT`)

- **Thinking:**
  - "지금 Red 테스트는 Contract 위반인가, Invariant 위반인가?"
  - "UI Track Green: Boundary만 통과시키면 되는가?"
  - "Logic Track Green: Solver 없이 BlankFinder만 Green 가능한가?"
  - "Refactor 후 Boundary Contract Test가 여전히 Green인가?"

- **Emotion:**
  - Red: "실패가 설계를 가리킨다"는 TDD 감각 체득
  - Green: 최소 구현으로 통과할 때 성취감
  - Refactor: Contract Test가 Green 유지될 때 설계 신뢰 증가

- **Pain Point:**
  - UI Track과 Logic Track 테스트를 **동시에 Red**로 만들어 Green 범위 모호
  - Green 단계에서 Solver 전체를 한 번에 구현하려는 과잉 구현
  - Refactor 시 Contract Test를 실행하지 않고 내부만 변경

- **Opportunity:**
  - Dual-Track으로 **실패 원인 분리** (Boundary vs Domain)
  - Epic SC-8(Red → Green → Refactor) 프로세스 기준 충족
  - `GRID_SIZE=4`, `MAX_VALUE=16`, `MAGIC_CONSTANT=34` 명명 상수 도입 (SC-3, SC-4)

- **UI RED Focus:**
  - IC-1~IC-5 위반 입력 → Boundary 거부 (EC-1~EC-4)
  - 유효 입력 + Solver 성공 → OC-1~OC-6 형식
  - Solver 실패 → EC-5
  - 1-index 좌표 출력 검증 (OC-3)

- **Logic RED Focus:**
  - BlankFinder: 0 정확히 2개 좌표 반환 (1-index)
  - MissingNumberFinder: 누락 2개 숫자 반환 (작은/큰 순)
  - MagicSquareValidator: Magic Sum=34 만족/불만족 판정
  - Solver: (작은→빈칸1, 큰→빈칸2) 성공 / 실패 시 역조합 시도

- **GREEN Minimal Implementation Principle:**
  - **Boundary Green:** Contract Test 통과에 필요한 **최소 검증·형식 변환**만
  - **BlankFinder Green:** 0 좌표 2개 반환만 (Validator/Solver 미구현)
  - **MissingNumberFinder Green:** 1~16 Set 차집합 2개 반환만
  - **Validator Green:** 행·열·대각선 합=34 비교만
  - **Solver Green:** 정방향 조합 1회 + Validator 호출 + 실패 시 역조합 1회만
  - **금지:** 정답 lookup table, Magic Square 전체 하드코딩

- **REFACTOR Principle:**
  - 매직 넘버 → `GRID_SIZE`, `MAX_VALUE`, `MAGIC_CONSTANT` 치환
  - BlankFinder / MissingNumberFinder / Validator / Solver **중복 로직 추출**
  - **Refactor 후 필수:** Boundary Contract Test Suite 전체 재실행 (INV-5 Contract Stability)
  - Domain Test와 Contract Test **모두 Green** 확인 후 Refactor 완료

- **Expected Learning Outcome:**
  - Dual-Track TDD **의도적 분리** 경험
  - Red → Green → Refactor **단계별 목적** 이해
  - 최소 구현(Green)과 과잉 구현 방지
  - Refactor 시 Contract Test를 **회귀 게이트**로 사용

---

### Stage 5: Regression Protection

- **Action:**
  - Stage 4 Green 이후, **회귀 테스트 세트**를 추가한다.
  - Edge case, Input error, Combination failure, Output format 케이스를 Red → Green
  - 리팩토링 전후 Contract Test + Domain Test **전체 Green** 확인
  - Invariant ↔ Test 매핑표 최종 점검 (SC-6)

- **Thinking:**
  - "빈칸 2개가 아닌 입력은 Boundary에서만 처리되는가?"
  - "두 조합 모두 Magic Sum 불만족이면 EC-5가 일관되게 적용되는가?"
  - "1-index (1,1)과 (4,4) corner case 출력 형식이 OC-2를 만족하는가?"
  - "리팩토링 후에도 이 테스트들이 Green인가?"

- **Emotion:**
  - 회귀 테스트 추가 후: Refactor에 대한 **심리적 안전감**
  - Edge case 실패 발견 시: "Stage 4에서 놓쳤다"는 학습
  - 전체 Green 유지: Epic Success Criteria 달성에 근접했다는 확신

- **Pain Point:**
  - Happy path만 있어 Refactor 시 **조용한 회귀**
  - Combination failure 케이스 미테스트 → Solver 역조합 로직 방치
  - Output format (int[6], 1-index) 오류가 Integration에서만 발견

- **Opportunity:**
  - Epic SC-6(Invariant마다 ≥1 Test), SC-7(리팩토링 후 Contract 불변) 충족
  - Stage 5 완료 = **Epic Level 2 Journey 완료**, User Story/Task 분해 준비 완료

- **Regression Test Target:**

  | Category | 대표 케이스 (명세 수준) |
  |----------|------------------------|
  | **Edge case** | 빈칸이 (1,1)과 (4,4) corner; 누락 숫자가 (1,16) 최소·최대; Magic Sum=34 경계 |
  | **Input error case** | 4×4 아님; 빈칸 0개/1개/3개; 값 17, -1; 0 제외 중복 (예: 두 개의 7) |
  | **Combination failure case** | 정방향(작은→빈칸1, 큰→빈칸2) Validator 실패 → 역조합 성공; **양쪽 모두 실패** → EC-5 |
  | **Output format case** | int[6] 길이; [r1,c1,n1,r2,c2,n2] 순서; 1-index 범위; n1≠n2; 좌표가 입력 0 위치와 일치 |

- **Protected Contract or Invariant:**
  - IC-1~IC-5, OC-1~OC-6, EC-1~EC-6 (Contract 전체)
  - INV-2 (빈칸 2개), INV-4 (중복 없음), INV-5 (Magic Sum=34), INV-6/INV-7 (좌표·출력 형식)
  - Solver 전략: 정방향 → 역조합 순서

- **Expected Learning Outcome:**
  - **회귀 테스트 = Refactor 안전망** 체득
  - Edge / Error / Combination failure / Output format **4류 보호** 경험
  - Epic Traceability(Concept → Invariant → Contract → Test) **완결**

---

## 5. Journey to User Story Mapping

| Journey Stage | Candidate User Story | Acceptance Criteria Direction |
|---------------|---------------------|------------------------------|
| **Stage 1** | US-01: Invariant 목록 정의 및 문서화 | 4×4, 빈칸2, 0/1~16, 중복 없음, Magic Sum=34, 1-index, int[6] 출력이 Invariant ID와 매핑됨 |
| **Stage 1** | US-02: Solver 전략(정방향/역조합)을 Invariant와 분리하여 명시 | Solver 전략이 INV가 아닌 "알고리즘 정책"으로 문서화됨 |
| **Stage 2** | US-03: Input Contract 정의 및 Boundary 검증 | IC-1~IC-5 위반 시 Domain 미호출, EC-1~EC-4 적용 |
| **Stage 2** | US-04: Output Contract 정의 | 성공 시 OC-1~OC-6 만족하는 int[6] 반환 |
| **Stage 2** | US-05: Error Contract 정의 | EC-1~EC-6 일관된 오류 표현 |
| **Stage 3** | US-06: BlankFinder — 빈칸 좌표 탐색 | 0 정확히 2개, 1-index (r1,c1,r2,c2) 반환 |
| **Stage 3** | US-07: MissingNumberFinder — 누락 숫자 탐색 | 1~16 중 2개 누락 숫자 반환 (작은/큰 순) |
| **Stage 3** | US-08: MagicSquareValidator — Magic Square 판정 | 행·열·대각선 합=MAGIC_CONSTANT(34) |
| **Stage 3** | US-09: Solver — 조합 시도 및 결과 반환 | 작은→빈칸1, 큰→빈칸2 시도; 실패 시 역조합; 성공 시 OC 형식, 실패 시 EC-5 |
| **Stage 3** | US-10: Control — Domain Unit orchestration | Boundary 검증 후 BlankFinder → MissingNumberFinder → Solver 순서 |
| **Stage 4** | US-11: Boundary Track TDD (Contract Test) | IC/OC/EC Contract Test Red→Green→Refactor |
| **Stage 4** | US-12: Logic Track TDD (Domain Test) | BlankFinder, MissingNumberFinder, Validator, Solver 각각 Red→Green→Refactor |
| **Stage 4** | US-13: 명명 상수 도입 (GRID_SIZE, MAX_VALUE, MAGIC_CONSTANT) | 매직 넘버 0개, SC-3/SC-4 충족 |
| **Stage 5** | US-14: Edge case 회귀 테스트 | Corner 빈칸, 최소/최대 누락 숫자 등 |
| **Stage 5** | US-15: Input error case 회귀 테스트 | IC/EC 위반 전 케이스 |
| **Stage 5** | US-16: Combination failure case 회귀 테스트 | 정방향 실패→역조합 성공; 양쪽 실패→EC-5 |
| **Stage 5** | US-17: Output format case 회귀 테스트 | int[6], 1-index, 좌표·숫자 일치 |
| **Stage 5** | US-18: Refactor 후 Contract 회귀 게이트 | Refactor 후 Boundary Contract Test 100% Green |

---

## 6. Traceability Link

| Epic Goal | Journey Stage | Invariant / Contract | Future Test Target |
|-----------|---------------|----------------------|-------------------|
| 불변식 중심 설계 사고 | Stage 1 | INV-1~INV-7 | Invariant 목록 ↔ Test ID 매핑표 |
| 입력/출력 계약 명확화 | Stage 2 | IC-1~IC-5, OC-1~OC-6, EC-1~EC-6 | Boundary Contract Test Suite |
| Domain Logic / UI·Boundary 분리 | Stage 3 | BlankFinder, MissingNumberFinder, Validator, Solver | Domain Unit Test (Logic Track) |
| Dual-Track UI + Logic TDD | Stage 4 | INV-5 Contract Stability | UI Track Test + Logic Track Test, Refactor 게이트 |
| 설계→테스트→구현→리팩토링 | Stage 4 | Red→Green→Refactor | TDD 사이클 이력 + Green 최소 구현 |
| Concept→Invariant→Contract→Test 추적 | Stage 1~5 | INV-6 (Traceability) | 추적성 매트릭스 (C-xx → INV-xx → BC-xx → T-xx) |
| Domain Logic 커버리지 95%+ | Stage 4~5 | INV-1~INV-5 | Logic Track 커버리지 리포트 |
| Boundary 계약 테스트 100% | Stage 2, 5 | IC, OC, EC | Contract Test Suite 전체 Green |
| 매직 넘버 금지, 명명 상수 | Stage 4 | GRID_SIZE, MAX_VALUE, MAGIC_CONSTANT | 정적 점검 + 코드 리뷰 |
| 정답 하드코딩 금지 | Stage 3~4 | Solver 전략 | Validator+Solver 조합 Test (lookup 없음) |
| 리팩토링 후 Contract 불변 | Stage 4~5 | INV-5 | Refactor 전후 Contract Test 비교 |

---

**Level 2 User Journey 완료.**  
다음 단계(Level 3)에서는 위 Candidate User Story를 **"As a … I want … So that …"** 형식과 Acceptance Criteria로 구체화하고, Task 단위로 분해한다.
