# Level 3: User Stories — Magic Square 4x4

## Story Overview

| Story ID | Story Name | Layer | Protected Contract / Invariant |
|----------|------------|-------|--------------------------------|
| US-01 | 입력 검증 | **Boundary** | IC-1~IC-5, EC-1~EC-4 |
| US-02 | 빈칸 좌표 탐색 | **Domain (Entity)** | INV-2 (Blank Count), INV-6 (Coordinate — 내부 표현) |
| US-03 | 누락 숫자 탐색 | **Domain (Entity)** | INV-3 (Value Range), INV-4 (Uniqueness) |
| US-04 | 마방진 검증 | **Domain (Entity)** | INV-1 (Grid), INV-5 (Magic Sum = 34) |
| US-05 | 두 가지 조합 시도 | **Domain (Entity) + Control** | OC-1~OC-6, EC-5, INV-5, INV-7, Solver Strategy |

---

## Story 1 — 입력 검증

- **Layer:** Boundary

- **User Story:**

  As a learner,  
  I want the Boundary layer to validate the input matrix before calling Domain logic,  
  So that invalid data is never transmitted to the Domain layer.

- **Acceptance Criteria:**

  1. 입력이 4행 4열의 2차원 int 구조가 아니면, Boundary는 정의된 검증 실패(EC-1)를 반환하거나 발생시킨다.
  2. 입력 원소 중 0 또는 1~16 범위를 벗어난 값이 하나라도 있으면, Boundary는 정의된 검증 실패(EC-2)를 반환하거나 발생시킨다.
  3. 값이 0인 셀(빈칸)의 개수가 정확히 2개가 아니면, Boundary는 정의된 검증 실패(EC-3)를 반환하거나 발생시킨다.
  4. 0을 제외한 값 중 동일한 숫자가 2회 이상 등장하면, Boundary는 정의된 검증 실패(EC-4)를 반환하거나 발생시킨다.
  5. IC-1~IC-4를 모두 만족하는 입력에 대해서만 Domain resolver(Control/Entity 호출 체인)가 실행된다.
  6. IC-1~IC-4 중 하나라도 위반된 입력에 대해서는 Domain resolver가 **한 번도** 호출되지 않는다.
  7. 모든 검증 실패는 동일한 Error Contract 표준(예외 타입 또는 오류 코드)을 따른다.

- **Protected Contract:**

  | ID | 내용 |
  |----|------|
  | IC-1 | 입력은 4×4 int 행렬 |
  | IC-2 | 각 원소 ∈ {0} ∪ {1, …, 16} |
  | IC-3 | 0(빈칸) 개수 = 2 |
  | IC-4 | 0 제외 값 중복 없음 |
  | IC-5 | IC 위반 시 Domain 미호출 |
  | EC-1~EC-4 | 형식/범위/빈칸 수/중복 위반 시 Boundary 거부 |

- **Future RED Test Direction:**

  - 3×4, 4×5, 1차원 리스트 등 **비 4×4** 입력 → EC-1, Domain 미호출
  - 값 17, -1, "7" 등 **범위·타입 위반** → EC-2, Domain 미호출
  - 빈칸 0개, 1개, 3개 → EC-3, Domain 미호출
  - 0 제외 중복(예: 7이 두 번) → EC-4, Domain 미호출
  - **유효 입력 1건** → Domain resolver 호출 확인(mock/spy)

---

## Story 2 — 빈칸 좌표 탐색

- **Layer:** Domain (Entity) — `BlankFinder`

- **User Story:**

  As a learner,  
  I want to find the exact coordinates of the two blank cells,  
  So that candidate number combinations can be applied correctly.

- **Acceptance Criteria:**

  1. 값이 0인 셀만 빈칸으로 탐지한다; 0이 아닌 셀은 빈칸으로 처리하지 않는다.
  2. 유효 입력(빈칸 정확히 2개)이 주어지면, 정확히 **2개**의 빈칸 좌표를 반환한다.
  3. 반환 좌표는 **row-major 순서**(행 우선: 위→아래, 같은 행 내 왼→오)로 정렬된다.
  4. BlankFinder의 내부 좌표 기준은 **0-index** `(row, col)`이며, `0 ≤ row, col ≤ 3`이다.
  5. 첫 번째 빈칸 좌표 `(r1, c1)`과 두 번째 빈칸 좌표 `(r2, c2)`는 입력 행렬에서 값이 0인 위치와 **정확히 일치**한다.
  6. BlankFinder는 입력 검증(Boundary 책임)을 수행하지 않는다; **유효 입력이 전달되었다고 가정**한다.

- **Protected Invariant:**

  | ID | 내용 |
  |----|------|
  | INV-2 | 0 = 빈칸, 빈칸은 정확히 2개 |
  | INV-6 | 좌표 체계 명시 (Domain: 0-index; 최종 출력 1-index 변환은 US-05/Boundary 책임) |

- **Future RED Test Direction:**

  - 빈칸이 (0,0), (3,3)인 4×4 → `[(0,0), (3,3)]` 반환
  - 빈칸이 (1,2), (2,1)인 4×4 → row-major 순 `[(1,2), (2,1)]` *(0-index 기준)*
  - 0이 아닌 셀 좌표가 결과에 포함되지 않음
  - 반환 좌표 개수가 항상 2

---

## Story 3 — 누락 숫자 탐색

- **Layer:** Domain (Entity) — `MissingNumberFinder`

- **User Story:**

  As a learner,  
  I want to find the two numbers missing from 1 through 16,  
  So that they can be used as candidates for the blank cells.

- **Acceptance Criteria:**

  1. 0은 빈칸 표식이므로, 누락 숫자 계산 대상에서 **제외**한다.
  2. 1부터 16까지의 정수 집합에서, 입력 행렬에 등장한(0 제외) 숫자를 제외한 **정확히 2개**의 누락 숫자를 반환한다.
  3. 반환되는 2개 숫자는 **오름차순** `[small, large]` 형식이다; `small < large`이다.
  4. 반환 숫자는 각각 1~16 범위에 속하며, 서로 다르다.
  5. MissingNumberFinder는 입력 검증(Boundary 책임)을 수행하지 않는다; **유효 입력이 전달되었다고 가정**한다.

- **Protected Invariant:**

  | ID | 내용 |
  |----|------|
  | INV-3 | 유효 값: 0 또는 1~16 |
  | INV-4 | 0 제외 숫자 중복 없음 → 누락 2개가 유일하게 결정됨 |

- **Future RED Test Direction:**

  - 1~14, 15·16이 빈칸(0)인 경우 → `[15, 16]`
  - 3, 7이 빈칸이고 나머지 1~16(3,7 제외)이 채워진 경우 → `[3, 7]`
  - 0이 계산에 포함되지 않음(0을 누락 숫자로 반환하지 않음)
  - 반환 배열 길이 = 2, 오름차순 보장

---

## Story 4 — 마방진 검증

- **Layer:** Domain (Entity) — `MagicSquareValidator`

- **User Story:**

  As a learner,  
  I want to verify whether a completed 4×4 grid satisfies the magic square invariant,  
  So that only valid magic square results are accepted.

- **Acceptance Criteria:**

  1. 입력 4×4 행렬에 0(빈칸)이 **하나도 없을 때만** 검증을 수행한다.
  2. 4개 행 각각의 원소 합이 `MAGIC_CONSTANT(34)`와 **같으면** 행 조건을 만족한다.
  3. 4개 열 각각의 원소 합이 `MAGIC_CONSTANT(34)`와 **같으면** 열 조건을 만족한다.
  4. 주대각선(top-left → bottom-right) 원소 합이 `34`와 **같으면** 주대각선 조건을 만족한다.
  5. 부대각선(top-right → bottom-left) 원소 합이 `34`와 **같으면** 부대각선 조건을 만족한다.
  6. 행 4개, 열 4개, 대각선 2개 **모든** 합이 34일 때만 `true`를 반환한다.
  7. 위 조건 중 **하나라도** 34가 아니면 `false`를 반환한다.
  8. 검증에 사용하는 상수는 `MAGIC_CONSTANT = 34`로 명명되어 있으며, 리터럴 34를 직접 사용하지 않는다.

- **Protected Invariant:**

  | ID | 내용 |
  |----|------|
  | INV-1 | 4×4 격자 |
  | INV-5 | 모든 행·열·대각선 합 = 34 |

- **Future RED Test Direction:**

  - 알려진 유효 4×4 Magic Square 1건 → `true`
  - 행 하나만 합 ≠ 34인 격자 → `false`
  - 열 하나만 합 ≠ 34인 격자 → `false`
  - 대각선 하나만 합 ≠ 34인 격자 → `false`
  - 0이 포함된 미완성 격자 → 검증 대상 아님(별도 Contract 또는 사전 조건 실패)

---

## Story 5 — 두 가지 조합 시도

- **Layer:** Domain (Entity) — `Solver` + Control (orchestration)

- **User Story:**

  As a learner,  
  I want the solver to try both possible missing-number combinations,  
  So that it can find the valid magic square result without hardcoding the answer.

- **Acceptance Criteria:**

  1. Solver는 BlankFinder가 반환한 2개 빈칸 좌표(0-index)와 MissingNumberFinder가 반환한 `[small, large]`를 입력으로 받는다.
  2. **1차 시도:** `small`을 첫 번째 빈칸에, `large`를 두 번째 빈칸에 배치한 완성 격자를 구성한다.
  3. 1차 시도 격자에 대해 MagicSquareValidator를 호출하고, `true`이면 해당 결과를 성공으로 채택한다.
  4. 1차 시도가 `false`이면 **2차 시도:** `large`를 첫 번째 빈칸에, `small`을 두 번째 빈칸에 배치한다.
  5. 2차 시도 격자에 대해 MagicSquareValidator를 호출하고, `true`이면 해당 결과를 성공으로 채택한다.
  6. 성공 시 반환값은 길이 **6**의 int 배열 `[r1, c1, n1, r2, c2, n2]`이다.
  7. `(r1, c1)`, `(r2, c2)`는 **1-index** 좌표이며, `1 ≤ r, c ≤ 4`이다.
  8. `(r1, c1)`, `(r2, c2)`는 원본 입력에서 0이었던 위치와 **일치**한다(0-index → 1-index 변환: `r_out = r_in + 1`, `c_out = c_in + 1`).
  9. `n1`, `n2`는 각각 첫 번째·두 번째 빈칸에 배치된 누락 숫자이며, `1 ≤ n1, n2 ≤ 16`, `n1 ≠ n2`이다.
  10. 1차·2차 시도 **모두** Validator `false`이면, Solver는 정의된 실패(EC-5)를 반환하거나 발생시킨다; 성공 형식 `[r1,c1,n1,r2,c2,n2]`를 반환하지 않는다.
  11. Solver는 정답 lookup table, 하드코딩된 Magic Square, 또는 미리 계산된 정답 배열을 사용하지 않는다.

- **Protected Contract / Invariant:**

  | ID | 내용 |
  |----|------|
  | OC-1 | 성공 시 int[6] 반환 |
  | OC-2 | 형식 `[r1, c1, n1, r2, c2, n2]` |
  | OC-3 | 좌표 1-index |
  | OC-4~OC-5 | n1, n2 및 좌표-빈칸 일치 |
  | OC-6 | 배치 후 Magic Sum = 34 (Validator 통과) |
  | EC-5 | 두 조합 모두 실패 시 명시적 실패 |
  | INV-5 | Magic Sum = 34 |
  | INV-7 | 출력 형식 불변 |
  | Solver Strategy | small→빈칸1, large→빈칸2 → 실패 시 역조합 |

- **Future RED Test Direction:**

  - 1차 조합만 성공하는 입력 → 1차 결과 int[6], Validator 1회 성공 후 종료
  - 1차 실패·2차 성공하는 입력 → 2차 결과 int[6], Validator 2회 호출
  - 1·2차 모두 실패 → EC-5, int[6] 미반환
  - 성공 결과: 배열 길이 = 6, 좌표 1-index, `[r1,c1,n1,r2,c2,n2]` 순서
  - (0,0) 빈칸 → 출력 r=1, c=1 변환 검증
  - lookup/hardcode 미사용(구현 리뷰 + 동적 입력 케이스)

---

## Traceability Matrix

| Epic Goal | Journey Stage | User Story | Acceptance Criteria (요약) | Future Test Target |
|-----------|---------------|------------|---------------------------|-------------------|
| 입력/출력 계약 명확화 | Stage 2: Contract Definition | US-01 | 4×4·범위·빈칸2·중복 검증, Domain 미호출 | Boundary Contract Test (IC/EC) |
| Domain / Boundary 분리 | Stage 3: Domain Separation | US-02 | 0 탐지, 2좌표, row-major, 0-index | BlankFinder Domain Test |
| Domain / Boundary 분리 | Stage 3: Domain Separation | US-03 | 0 제외, 누락 2개, 오름차순 | MissingNumberFinder Domain Test |
| 불변식 중심 설계 | Stage 3: Domain Separation | US-04 | 행·열·대각선 합=34, true/false | MagicSquareValidator Domain Test |
| 정답 하드코딩 금지 | Stage 4: Dual-Track TDD | US-05 | 2조합 시도, int[6] 1-index 출력 | Solver + Validator Integration Test |
| Dual-Track UI + Logic TDD | Stage 4: Dual-Track TDD | US-01 | Boundary Red→Green (Contract) | UI/Boundary Track |
| Dual-Track UI + Logic TDD | Stage 4: Dual-Track TDD | US-02~05 | Domain Red→Green (Invariant) | Logic Track |
| 회귀 테스트로 품질 보호 | Stage 5: Regression Protection | US-01 | Input error 전 케이스 | EC-1~EC-4 회귀 Suite |
| 회귀 테스트로 품질 보호 | Stage 5: Regression Protection | US-05 | Combination failure, Output format | EC-5, OC-1~OC-6 회귀 Suite |
| Concept→Invariant→Contract→Test | Stage 1~5 | US-01~05 | Story별 Contract/Invariant 명시 | 추적성 매트릭스 (C→INV→BC→T) |
| Boundary 계약 테스트 100% | Stage 2, 5 | US-01 | IC-1~IC-5, EC-1~EC-4 | Contract Test Suite Green |
| Domain Logic 커버리지 95%+ | Stage 4~5 | US-02~05 | Entity 단위 AC 전체 | Logic Track Coverage Report |
| 리팩토링 후 Contract 불변 | Stage 4~5 | US-01, US-05 | Refactor 후 Boundary·Output Contract 유지 | Refactor 게이트 Test |

---

**Level 3 User Stories 완료.**  
다음 단계(Level 4)에서는 각 User Story의 Acceptance Criteria를 **Task** 단위(Red Test 작성, Green 최소 구현, Refactor 항목)로 분해한다.
