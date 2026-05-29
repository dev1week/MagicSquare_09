# MagicSquare

4×4 마방진을 **생성**하고 **검증**하는 프로그램 프로젝트입니다.  
현재는 **문제 정의** 단계이며, 설계·구현은 아직 시작하지 않았습니다.

## 한 줄 요약

1~16을 한 번씩 4×4 격자에 놓았을 때, 모든 행·열·대각선의 합이 같아지는 배치를 **얻거나**, 주어진 배치가 그 규칙을 **만족하는지 화면에서 확인**하는 도구를 만드는 것이 목표입니다.

## 확정된 요구 (2026-05-28)

| 항목　　　| 내용　　　　　　　　　　　　　　　　　　　　　　　　　|
| -----------| -------------------------------------------------------|
| 격자　　　| 4×4 고정　　　　　　　　　　　　　　　　　　　　　　　|
| 숫자　　　| 1~16, 각 숫자 1회　　　　　　　　　　　　　　　　　　 |
| 핵심 기능 | **생성** + **검증** (동등하게 중요)　　　　　　　　　 |
| 결과 표시 | **화면만** (파일·API·공유 불필요)　　　　　　　　　　 |
| 관점　　　| **실제 서비스** 수준의 정확성·명확한 오류·일관된 규칙 |

## 도메인 (참고)

- **마방 상수**: 34 (각 행·열·대각선의 합)
- **유효 조건**: 4행, 4열, 주대각선, 부대각선의 합이 모두 34

생성 결과는 검증과 **동일한 규칙**을 따르며, 내부적으로도 그 기준을 통과해야 합니다.

## 프로젝트 구조

```
MagicSquare/
├── README.md          ← 이 파일 (프로젝트 개요)
├── test_plan.md       ← pytest 테스트 계획서
├── report/            ← 문제 정의·설계 산출물
│   ├── README.md
│   ├── 01-observation.md
│   ├── ...
│   └── 09-user-stories-magic-square-4x4-report.md
└── prompt/            ← 문제 정의 대화 기록 (참고)
```

## 문서

상세한 관찰·범위·서비스 관점·미결정 사항은 [`report/`](./report/)를 참고하세요.

| 문서　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　| 설명　　　　　　　　　　　　　　　　　　　　　　　　　|
| -----------------------------------------------------------------------| -------------------------------------------------------|
| [test_plan.md](./test_plan.md)　　　　　　　　　　　　　　　　　　　　| pytest 테스트 계획서 (Dual-Track, 커버리지, mock/spy) |
| [report/README.md](./report/README.md)　　　　　　　　　　　　　　　　| 리포트 목차 및 확정 전제　　　　　　　　　　　　　　　|
| [01-observation.md](./report/01-observation.md)　　　　　　　　　　　 | STEP 1 — 상황·동기·맥락 관찰　　　　　　　　　　　　　|
| [02-stakeholders-and-scope.md](./report/02-stakeholders-and-scope.md) | 이해관계자, In/Out 범위, 사용자 여정　　　　　　　　　|
| [03-service-view.md](./report/03-service-view.md)　　　　　　　　　　 | 서비스 관점 기능(V/G/D), 품질·성공 지표　　　　　　　 |
| [09-user-stories-magic-square-4x4-report.md](./report/09-user-stories-magic-square-4x4-report.md) | Level 3 User Stories (US-01~05) |

## 범위 요약

### 포함 (In scope)

- 유효한 4×4 마방진 **생성** 및 화면 표시
- 사용자/시스템이 만든 4×4 배치 **검증** 및 결과 표시
- 잘못된 입력(중복, 범위 밖, 불완전 등)에 대한 **명확한 안내**

### 제외 (현 단계 Out of scope)

- 파일 저장, REST API, 공유 URL
- n×n 일반화, 사용자 정의 숫자 범위
- 계정·결제 등 엔터프라이즈 기능

## 현재 상태

| 구분　　　| 상태　　　　　　　　　　　　　　　　　　　 |
| -----------| --------------------------------------------|
| 문제 정의 | 진행 중 (`report/` 참고)　　　　　　　　　 |
| 설계　　　| 진행 중 (`report/05`, `report/08~09` 참고) |
| 구현　　　| 미착수　　　　　　　　　　　　　　　　　　 |
| 테스트　　| 계획 수립 (`test_plan.md`)　　　　　　　　 |

## RED 단계 To-Do 리스트

> Dual-Track TDD **Red** 단계: 테스트를 먼저 작성하고 실패를 확인한 뒤 Green으로 진행한다.  
> 상세 전략·fixture·mock/spy 규칙은 [`test_plan.md`](./test_plan.md) 참고.  
> User Story 전체: [`report/09-user-stories-magic-square-4x4-report.md`](./report/09-user-stories-magic-square-4x4-report.md)  
> 시드 AC: **AC-US-01-01** (`grid=None` → `INVALID_SIZE`, Domain `execute` 0회)

### Track A — UI / Boundary 테스트 (US-01)

**P0 — 시드·격리 (최우선 RED)**

- [ ] **BT-01** — `grid=None` → `{ code: "INVALID_SIZE", message: "Grid must be 4x4." }` + `SolvePartialGrid.execute` **0회** (AC-US-01-01, EC1-01)
- [ ] **BT-02** — 비 4×4 입력 회귀: 3×4, 4×5, 1차원 list, 빈 list, jagged array (EC1-04~07) → `INVALID_SIZE`, Domain 0회 (AC-US-01-01)
- [ ] **BT-03** — 유효 입력 1건 → Domain `execute` **1회** (AC-US-01-05, DOM-02)

**P1 — EC-2~4·순서·매핑**

- [ ] **BT-04** — 값 범위 위반: 17, -1, `"7"`, `None` (EC2-01~04) → `CELL_VALUE_OUT_OF_RANGE`, Domain 0회 (AC-US-01-02)
- [ ] **BT-05** — 빈칸 0/1/3개 (EC3-01~03) → `EMPTY_CELL_COUNT_INVALID`, Domain 0회 (AC-US-01-03)
- [ ] **BT-06** — non-zero 중복 (EC4-01) → `DUPLICATE_NON_ZERO`, Domain 0회 (AC-US-01-04)
- [ ] **BT-07** — 검사 순서 잠금: 3×4+값17 → `INVALID_SIZE` (ORD-01), 빈칸3+중복 → `EMPTY_CELL_COUNT_INVALID` (ORD-02)
- [ ] **DOM-01** — 유효 입력 + Mock `UnsolvableGrid` → `DOMAIN_UNSOLVABLE`
- [ ] **AC-US-01-06** — IC-1~IC-4 위반 입력 전체에서 Domain resolver **0회** (BT-01~06, spy 회귀)

**P2 — Contract·인프라**

- [ ] **BT-08** — Error Contract 일관성: 모든 EC 응답이 pydantic `ErrorResponse` 스키마·카탈로그와 일치 (AC-US-01-07)
- [x] `tests/boundary/conftest.py` — `domain_spy` / `boundary_resolver` fixture (`create_autospec` + `pytest-mock`)
- [x] `tests/boundary/test_input_validator.py` — IC-1~IC-4 단위 검증
- [x] `tests/boundary/test_boundary_resolver.py` — BT-01~03 시드·격리 테스트
- [x] `tests/boundary/test_error_contract.py` — pydantic 스키마·고정 `message` 잠금
- [x] `tests/boundary/test_ac_us01_domain_isolation.py` — AC-US-01-05/06 Domain spy 격리
- [x] `tests/boundary/test_boundary_error_catalog_resolver.py` — BT-08 resolver + catalog
- [x] `tests/boundary/test_boundary_error_standard.py` — AC-US-01-07 resolver ErrorResponse

**EC-1 특이 케이스 (BT-02 확장)**

- [ ] EC1-02 — `[]` → `INVALID_SIZE`
- [ ] EC1-03 — 1×4 → `INVALID_SIZE`
- [ ] EC1-08 — float 원소 → `INVALID_SIZE`
- [ ] EC1-09 — 중첩 깊이 이상 → `INVALID_SIZE`

**US-01 Acceptance Criteria (IC / EC)**

- [ ] **AC-US-01-01** — 4×4 int 2차원 구조 아님 → EC-1 (`INVALID_SIZE`)
- [ ] **AC-US-01-02** — 원소가 0 또는 1~16 범위 밖 → EC-2
- [ ] **AC-US-01-03** — 빈칸(0) 개수 ≠ 2 → EC-3
- [ ] **AC-US-01-04** — 0 제외 값 중복 → EC-4
- [ ] **AC-US-01-05** — IC-1~IC-4 만족 시에만 Domain resolver 실행
- [ ] **AC-US-01-06** — IC 위반 시 Domain resolver 미호출
- [ ] **AC-US-01-07** — 모든 검증 실패가 동일 Error Contract 표준 준수

### Track B — Domain / Logic 테스트 (US-02~05)

> Boundary Green(P0) 이후 착수. Domain 테스트는 Boundary mock **사용 금지** — 실제 `MagicSquareJudge` 사용 (RG-B02).

#### US-02 — 빈칸 좌표 탐색 (`EmptyCellLocator` / BlankFinder)

**P0 — Entity 단위 (DT-01)**

- [ ] **DT-01** — `EmptyCellLocator.locate` 통합 RED (US-02)
- [x] `tests/domain/test_empty_cell_locator.py` — RED 테스트 파일
- [ ] **AC-US-02-01** — 값이 0인 셀만 빈칸으로 탐지; 0이 아닌 셀 제외
- [ ] **AC-US-02-02** — 유효 입력 시 정확히 **2개** 좌표 반환
- [ ] **AC-US-02-03** — 반환 좌표 **row-major** (행 우선, 왼→오) 정렬
- [ ] **AC-US-02-04** — 내부 좌표 **0-index** `(row, col)`, `0 ≤ row, col ≤ 3`
- [ ] **AC-US-02-05** — 반환 좌표가 입력 행렬의 0 위치와 **정확히 일치**
- [ ] **AC-US-02-06** — 입력 검증 수행 안 함 (유효 입력 전제)

**Future RED — US-02**

- [ ] 빈칸 `(0,0)`, `(3,3)` → `[(0,0), (3,3)]`
- [ ] 빈칸 `(1,2)`, `(2,1)` → row-major `[(1,2), (2,1)]`
- [ ] 0이 아닌 셀 좌표가 결과에 **미포함**
- [ ] 반환 좌표 개수 **항상 2**

**보호 Invariant:** INV-2 (빈칸 2개), INV-6 (Domain 0-index)

#### US-03 — 누락 숫자 탐색 (`MissingNumberResolver` / MissingNumberFinder)

**P0 — Entity 단위 (DT-02)**

- [ ] **DT-02** — `MissingNumberResolver.resolve` 통합 RED (US-03)
- [x] `tests/domain/test_missing_number_resolver.py` — RED 테스트 파일
- [ ] **AC-US-03-01** — 0은 누락 숫자 계산에서 **제외**
- [ ] **AC-US-03-02** — 1~16에서 present(0 제외) 제외 후 **정확히 2개** 누락 숫자 반환
- [ ] **AC-US-03-03** — 반환 형식 **오름차순** `[small, large]`, `small < large`
- [ ] **AC-US-03-04** — 각 숫자 1~16, 서로 다름
- [ ] **AC-US-03-05** — 입력 검증 수행 안 함 (유효 입력 전제)

**Future RED — US-03**

- [ ] 1~14 채움, 15·16이 빈칸(0) → `[15, 16]`
- [ ] 3, 7이 빈칸, 나머지 채움 → `[3, 7]`
- [ ] 0이 누락 숫자로 **반환되지 않음**
- [ ] 반환 길이 = 2, **오름차순** 보장

**보호 Invariant:** INV-3 (값 범위), INV-4 (중복 없음 → 누락 유일)

#### US-04 — 마방진 검증 (`MagicSquareJudge` / MagicSquareValidator)

**P0 — Entity 단위 (DT-03)**

- [ ] **DT-03** — `MagicSquareJudge.isMagic` 통합 RED (US-04)
- [x] `tests/domain/test_magic_square_judge.py` — RED 테스트 파일
- [ ] **AC-US-04-01** — 0(빈칸) **없을 때만** 검증 수행
- [ ] **AC-US-04-02** — 4개 행 합 = `MAGIC_CONSTANT`
- [ ] **AC-US-04-03** — 4개 열 합 = `MAGIC_CONSTANT`
- [ ] **AC-US-04-04** — 주대각선 합 = `MAGIC_CONSTANT`
- [ ] **AC-US-04-05** — 부대각선 합 = `MAGIC_CONSTANT`
- [ ] **AC-US-04-06** — 행·열·대각선 **모두** 만족 시에만 `true`
- [ ] **AC-US-04-07** — 하나라도 불만족 시 `false`
- [ ] **AC-US-04-08** — `MAGIC_CONSTANT = 34` 명명 상수 사용 (리터럴 34 금지)

**Future RED — US-04**

- [ ] 알려진 유효 4×4 Magic Square 1건 → `true`
- [ ] 행 하나만 합 ≠ 34 → `false`
- [ ] 열 하나만 합 ≠ 34 → `false`
- [ ] 대각선 하나만 합 ≠ 34 → `false`
- [ ] 0 포함 미완성 격자 → 검증 대상 아님 (`GridNotComplete` 등)

**Domain 전제 위반**

- [ ] **DM-E01** — `isMagic` + 0 포함 격자 → `GridNotComplete` (AC-US-04-01)
- [ ] **DM-E02** — `isMagic` + 3×4 → `InvalidGridSize`

**보호 Invariant:** INV-1 (4×4), INV-5 (Magic Sum = 34)

#### US-05 — 두 가지 조합 시도 (`PlacementTrialSolver` + `SolvePartialGrid`)

**P1 — Solver·Control (DT-04, DT-05)**

- [ ] **DT-04** — `PlacementTrialSolver.solve`: small→빈칸1 / large→빈칸2, 역조합 (US-05 AC 1~5)
- [ ] **DT-05** — `SolvePartialGrid.execute` E2E: `int[6]` 1-index, EC-5 (US-05 AC 6~11)
- [x] `tests/domain/test_placement_trial_solver.py` — RED 테스트 파일
- [x] `tests/domain/test_solve_partial_grid.py` — RED 테스트 파일
- [ ] **AC-US-05-01** — BlankFinder·MissingNumberFinder 결과(0-index 좌표, `[small, large]`)를 입력으로 사용
- [ ] **AC-US-05-02** — 1차: `small`→첫 빈칸, `large`→둘째 빈칸 배치
- [ ] **AC-US-05-03** — 1차 격자 `MagicSquareValidator` 호출, `true`면 성공 채택
- [ ] **AC-US-05-04** — 1차 `false` 시 2차: `large`→첫 빈칸, `small`→둘째 빈칸
- [ ] **AC-US-05-05** — 2차 격자 Validator 호출, `true`면 성공 채택
- [ ] **AC-US-05-06** — 성공 시 길이 **6** `int` 배열 반환
- [ ] **AC-US-05-07** — `(r1,c1)`, `(r2,c2)` **1-index**, `1 ≤ r,c ≤ 4`
- [ ] **AC-US-05-08** — 출력 좌표가 원본 0 셀과 일치 (`r_out = r_in + 1`, `c_out = c_in + 1`)
- [ ] **AC-US-05-09** — `n1`, `n2`는 각 빈칸 배치 숫자, `1 ≤ n ≤ 16`, `n1 ≠ n2`
- [ ] **AC-US-05-10** — 1·2차 모두 `false` → EC-5 (`UnsolvableGrid`), `int[6]` 미반환
- [ ] **AC-US-05-11** — lookup table / 하드코딩 정답 **미사용** (리뷰 + 동적 입력)

**Future RED — US-05**

- [ ] 1차 조합만 성공 → 1차 `int[6]`, Validator **1회** 성공 후 종료
- [ ] 1차 실패·2차 성공 → 2차 `int[6]`, Validator **2회** 호출
- [ ] 1·2차 모두 실패 → EC-5, `int[6]` 미반환
- [ ] 성공: 길이 6, 1-index, `[r1,c1,n1,r2,c2,n2]` 순서
- [ ] `(0,0)` 빈칸 → 출력 `r=1`, `c=1` 변환
- [ ] lookup/hardcode 미사용 검증

**Domain 전제 위반**

- [ ] **DM-E03** — `solve` + 두 배치 모두 실패 → `UnsolvableGrid` (AC-US-05-10, EC-5)

**보호 Contract:** OC-1~OC-6, EC-5, INV-5, INV-7, Solver Strategy

**공통 Domain 인프라**

- [x] `tests/fixtures/grids.py` — 격자 fixture (유효/무효/마방진·퍼즐 샘플)
- [x] `tests/fixtures/error_catalog.py` — Boundary Error catalog 공유
- [x] `tests/domain/conftest.py` — Domain 공통 fixture (`magic_square_judge`)
- [x] `tests/domain/test_ac_us02_no_boundary_validation.py` — AC-US-02-06, BL-01
- [x] `tests/domain/test_ac_us03_missing_resolver.py` — AC-US-03-03/05
- [x] `tests/domain/test_ac_us04_diagonals.py` — AC-US-04-04/05/08
- [x] `tests/domain/test_ac_us05_orchestration.py` — AC-US-05-01~11, SV-01~05
- [x] `tests/domain/test_domain_infrastructure.py` — MAGIC_CONSTANT, exceptions RED
- [ ] `src/domain/constants.py` — `MAGIC_CONSTANT = 34`
- [ ] `src/domain/exceptions.py` — `GridNotComplete`, `InvalidGridSize`, `UnsolvableGrid`

### Track C — 통합 / 회귀 (Stage 4~5)

> Boundary + 실제 Domain 조합. Traceability Matrix 기준.

**P2 — 통합**

- [ ] **IT-01** — 유효 입력 → Boundary → Domain → 성공 `int[6]` / `OK [r1,c1,n1,r2,c2,n2]`
- [ ] **IT-02** — 1차 실패·2차 성공 퍼즐 → 2차 결과·Validator 2회 호출
- [ ] **IT-04** — 3×4 입력 → `INVALID_SIZE`, Domain 미호출
- [ ] **IT-06** — unsolvable fixture → `DOMAIN_UNSOLVABLE` / EC-5
- [x] `tests/integration/test_boundary_to_domain.py` — 통합 RED (IT-01, IT-02, IT-04, IT-06)
- [x] `tests/regression/test_us01_input_errors.py` — RG-US-01 EC-1~4 회귀
- [x] `tests/integration/test_output_formatter.py` — IT-01 OK 출력 형식
- [x] `tests/integration/test_it02_validator_calls.py` — IT-02 Validator 2회
- [x] `tests/regression/test_us01_boundary_resolver.py` — RG-US-01 resolver 경로
- [x] `tests/regression/test_us05_solver_output.py` — RG-US-05 OC/EC-5 회귀
- [x] `tests/regression/test_refactor_contract_gate.py` — RG-REFACTOR contract 잠금

**P3 — 회귀·리팩토링 게이트**

- [ ] **RG-US-01** — US-01: EC-1~EC-4 입력 오류 전 케이스 회귀 Suite Green
- [ ] **RG-US-05** — US-05: EC-5 실패 + OC-1~OC-6 출력 형식 회귀 Suite Green
- [ ] **RG-REFACTOR** — Refactor 후 Boundary·Output Contract 불변 (US-01, US-05)
- [ ] Boundary Contract Test Suite — IC-1~IC-5, EC-1~EC-4 **100%** Green
- [ ] Domain Logic Track — US-02~05 Entity AC **95%+** branch

### 커버리지 목표

- [ ] `pip install pytest pytest-cov pytest-mock pydantic` 실행
- [ ] `pytest --cov=src --cov-report=term-missing` — 로컬 기본 측정
- [ ] `pytest --cov=src --cov-report=html:htmlcov` — HTML 리포트 (`htmlcov/index.html`)
- [ ] Boundary Track: `pytest tests/boundary/ --cov=src/boundary --cov-report=term-missing --cov-fail-under=85` → **branch ≥ 85%**
- [ ] Domain Track: `pytest tests/domain/ --cov=src/domain --cov-report=term-missing --cov-fail-under=95` → **branch ≥ 95%**
- [ ] CI: `--cov-branch`, `--cov-report=html:htmlcov` 리포트 생성
- [ ] `pyproject.toml` — pytest markers, coverage `omit`/`branch` 설정

| 레이어　　　| Branch 목표 | 측정 패키지　　 | User Story |
| -------------| -------------| -----------------| ------------|
| Boundary　　| **≥ 85%**　 | `src/boundary/` | US-01 |
| Domain　　　| **≥ 95%**　 | `src/domain/`　 | US-02~05 |
| 전체 (참고) | ≥ 90%　　　 | `src/`　　　　　| US-01~05 |

### 결함 목록 연결

#### US-01 — Boundary (EC / ORD / DOM)

| 결함 Case ID | 입력 / 조건　　　　　　　| 기대 `code` 또는 예외　　　| 연결 RED 테스트 |
| --------------| --------------------------| ----------------------------| -----------------|
| EC1-01　　　 | `grid=None`　　　　　　　| `INVALID_SIZE`　　　　　　 | BT-01　　　　　 |
| EC1-02　　　 | `[]`　　　　　　　　　　 | `INVALID_SIZE`　　　　　　 | BT-02　　　　　 |
| EC1-03　　　 | 1×4　　　　　　　　　　　| `INVALID_SIZE`　　　　　　 | BT-02　　　　　 |
| EC1-04　　　 | 3×4　　　　　　　　　　　| `INVALID_SIZE`　　　　　　 | BT-02　　　　　 |
| EC1-05　　　 | 4×5　　　　　　　　　　　| `INVALID_SIZE`　　　　　　 | BT-02　　　　　 |
| EC1-06　　　 | 1차원 list　　　　　　　 | `INVALID_SIZE`　　　　　　 | BT-02　　　　　 |
| EC1-07　　　 | jagged array　　　　　　 | `INVALID_SIZE`　　　　　　 | BT-02　　　　　 |
| EC1-08　　　 | float 원소　　　　　　　 | `INVALID_SIZE`　　　　　　 | BT-02　　　　　 |
| EC1-09　　　 | 중첩 깊이 이상　　　　　 | `INVALID_SIZE`　　　　　　 | BT-02　　　　　 |
| EC2-01~04　　| 17 / -1 / `"7"` / `None` | `CELL_VALUE_OUT_OF_RANGE`　| BT-04　　　　　 |
| EC3-01~03　　| 빈칸 0 / 1 / 3　　　　　 | `EMPTY_CELL_COUNT_INVALID` | BT-05　　　　　 |
| EC4-01　　　 | non-zero 중복　　　　　　| `DUPLICATE_NON_ZERO`　　　 | BT-06　　　　　 |
| ORD-01　　　 | 3×4 + 값 17　　　　　　　| `INVALID_SIZE` (범위 아님) | BT-07　　　　　 |
| ORD-02　　　 | 빈칸 3 + 중복　　　　　　| `EMPTY_CELL_COUNT_INVALID` | BT-07　　　　　 |
| DOM-01　　　 | 유효 + unsolvable　　　　| `DOMAIN_UNSOLVABLE`　　　　| DOM-01　　　　　|
| DOM-02　　　 | 유효 + 성공　　　　　　　| `result` int[6]　　　　　　| BT-03　　　　　 |

#### US-02~04 — Domain (Future RED / DM-E)

| 결함 Case ID | 입력 / 조건 | 기대 동작 | 연결 RED 테스트 |
| --------------| -------------| -----------| -----------------|
| BL-01 | 빈칸 `(0,0)`, `(3,3)` | `[(0,0), (3,3)]` | DT-01, AC-US-02-03 |
| BL-02 | 빈칸 `(1,2)`, `(2,1)` | `[(1,2), (2,1)]` row-major | DT-01 |
| BL-03 | non-zero 셀 | 결과에 미포함 | DT-01, AC-US-02-01 |
| MN-01 | 15·16 빈칸 | `[15, 16]` | DT-02 |
| MN-02 | 3·7 빈칸 | `[3, 7]` | DT-02 |
| MN-03 | 0 in grid | 0 not in missing set | DT-02, AC-US-03-01 |
| MV-01 | known magic square | `true` | DT-03, AC-US-04-06 |
| MV-02 | bad row sum | `false` | DT-03, AC-US-04-07 |
| MV-03 | bad column sum | `false` | DT-03 |
| MV-04 | bad diagonal sum | `false` | DT-03 |
| DM-E01 | 0 in grid + `isMagic` | `GridNotComplete` | DT-03 |
| DM-E02 | 3×4 + `isMagic` | `InvalidGridSize` | DT-03 |

#### US-05 — Solver (Future RED / EC-5 / OC)

| 결함 Case ID | 입력 / 조건　　　 | 기대 동작　　　　　　　　　　 | 연결 RED 테스트　　　|
| --------------| -------------------| -------------------------------| ----------------------|
| SV-01　　　　| 1차만 성공　　　　| `int[6]`, Validator 1회　　　 | DT-04, DT-05　　　　 |
| SV-02　　　　| 1차 실패·2차 성공 | `int[6]`, Validator 2회　　　 | DT-04　　　　　　　　|
| SV-03　　　　| both trials fail　| EC-5 / `UnsolvableGrid`　　　 | DT-04, DT-05, DM-E03 |
| SV-04　　　　| blank `(0,0)`　　 | output `r=1,c=1`　　　　　　　| DT-05, AC-US-05-08　 |
| SV-05　　　　| hardcoded answer　| 동적 입력으로만 통과　　　　　| AC-US-05-11　　　　　|
| EC5-01　　　 | unsolvable grid　 | EC-5, no `int[6]`　　　　　　 | DT-05, AC-US-05-10　 |
| OC-01~06　　 | success path　　　| `[r1,c1,n1,r2,c2,n2]` 1-index | DT-05　　　　　　　　|

## 다음 단계

1. **RED** — Track A P0 (BT-01~03) Green → Track B US-02~05 (DT-01~05) Green
2. **Track C** — 통합·회귀 Suite (IT-01~06, RG-US-01/05)
3. **Refactor** — 커버리지 게이트 유지 (Boundary ≥85%, Domain ≥95%)

## 라이선스

미정 (코드 추가 시 설정 예정)
