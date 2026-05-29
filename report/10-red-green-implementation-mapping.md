# RED ↔ Green 구현 단위 매핑

> **작성일:** 2026-05-29  
> **상태:** Green — `154 passed` (`python -m pytest tests/ -v`)  
> **기준 설계:** [05-dual-track-clean-architecture-tdd-design.md](./05-dual-track-clean-architecture-tdd-design.md)  
> **User Story:** [09-user-stories-magic-square-4x4-report.md](./09-user-stories-magic-square-4x4-report.md)

---

## 1. 정리 원칙

구현·테스트를 **가장 적합한 단위**로 묶을 때 아래 4축을 동시에 맞춘다.

| 축 | 의미 |
|----|------|
| **ECB 레이어** | Boundary / Domain / Entity / Integration |
| **User Story** | US-01 ~ US-05 (기능 단위) |
| **TDD 슬라이스** | RED 테스트 파일 1벌 → Green 구현체 1~N 모듈 |
| **책임 단위** | SUT 1개(public API 1개) + 보조 모듈(상수·스키마·예외) |

한 **TDD 슬라이스** = RED 테스트(실패 확인) → Green 구현 → Refactor(계약 불변)  
회귀·통합 테스트는 슬라이스 위에 **Stage 4~5**로 쌓인다.

---

## 2. 전체 구조 한눈에

```
tests/fixtures/          ← RED 공유 데이터 (격자·에러 카탈로그)
        │
        ├─ Track A (Boundary) ── US-01 입력 검증·위임
        │     src/boundary/*
        │
        ├─ Track B (Domain) ─── US-02~05 퍼즐 해결 로직
        │     src/domain/*
        │
        ├─ Track C (Integration) ─ Boundary + 실제 Domain E2E
        │     tests/integration/*
        │
        └─ Regression ─────────── 계약 잠금·US 회귀
              tests/regression/*

Entity (별도 슬라이스)
  src/entity/user.py  ←  tests/entity/test_user.py
```

---

## 3. TDD 슬라이스별 매핑 (핵심 표)

### 3.1 Boundary — US-01 입력 검증·Domain 위임

| # | TDD 슬라이스 (단위) | Green 구현 | RED / Green 테스트 | 테스트 수 | AC / BT |
|---|---------------------|------------|------------------|-----------|---------|
| B-01 | **입력 검증기** `InputValidator.validate` | `src/boundary/input_validator.py` | `tests/boundary/test_input_validator.py` | 17 | IC-1~4, BT-02~06, EC-1~4 |
| B-02 | **에러 스키마** `ErrorResponse` | `src/boundary/schemas.py` | `tests/boundary/test_error_contract.py` | 7 | BT-08, AC-US-01-07 |
| B-03 | **에러 카탈로그** (고정 message) | `src/boundary/error_catalog.py` | ↑ + `tests/fixtures/error_catalog.py` | (공유) | AC-US-01-07 |
| B-04 | **리졸버** `BoundaryResolver.solve` | `src/boundary/resolver.py` | `tests/boundary/test_boundary_resolver.py` | 21 | BT-01~07, DOM-01~02, AC-US-01-01~06 |
| B-05 | **Domain 격리** (spy) | ↑ resolver + `tests/boundary/conftest.py` | `tests/boundary/test_ac_us01_domain_isolation.py` | 11 | AC-US-01-05/06 |
| B-06 | **Resolver + 카탈로그 일치** | ↑ | `tests/boundary/test_boundary_error_catalog_resolver.py` | 6 | BT-08 |
| B-07 | **Resolver ErrorResponse 준수** | ↑ | `tests/boundary/test_boundary_error_standard.py` | 3 | AC-US-01-07 |
| B-08 | **성공 출력 포맷** `ResponseFormatter` | `src/boundary/response_formatter.py` | `tests/integration/test_output_formatter.py` | 2 | IT-01, OC-1~2 |

**Boundary 검증 순서 (구현 계약):**  
`size` → `cell range` → `blank count` → `duplicate` → Domain 호출

**Boundary fixture:** `tests/boundary/conftest.py` — `domain_spy`, `boundary_resolver`  
**전역 등록:** `tests/conftest.py` — `pytest_plugins = ["tests.boundary.conftest"]`

---

### 3.2 Domain — US-02 ~ US-05

| # | TDD 슬라이스 (단위) | Green 구현 | RED / Green 테스트 | 테스트 수 | AC / DT |
|---|---------------------|------------|------------------|-----------|---------|
| D-00 | **도메인 인프라** | `src/domain/constants.py`<br>`src/domain/exceptions.py` | `tests/domain/test_domain_infrastructure.py` | 2 | AC-US-04-08, DM-E01~03 |
| D-01 | **빈칸 탐색** `EmptyCellLocator.locate` | `src/domain/empty_cell_locator.py` | `tests/domain/test_empty_cell_locator.py`<br>`tests/domain/test_ac_us02_no_boundary_validation.py` | 7 + 3 | DT-01, US-02, AC-US-02-01~06 |
| D-02 | **누락 숫자** `MissingNumberResolver.resolve` | `src/domain/missing_number_resolver.py` | `tests/domain/test_missing_number_resolver.py`<br>`tests/domain/test_ac_us03_missing_resolver.py` | 7 + 3 | DT-02, US-03, AC-US-03-01~05 |
| D-03 | **마방진 판정** `MagicSquareJudge.is_magic` | `src/domain/magic_square_judge.py` | `tests/domain/test_magic_square_judge.py`<br>`tests/domain/test_ac_us04_diagonals.py` | 10 + 3 | DT-03, US-04, AC-US-04-01~08, DM-E01~02 |
| D-04 | **배치 시도** `PlacementTrialSolver.solve` | `src/domain/placement_trial_solver.py` | `tests/domain/test_placement_trial_solver.py` | 5 | DT-04, AC-US-05-02~05, DM-E03 |
| D-05 | **오케스트레이션** `SolvePartialGrid.execute` | `src/domain/solve_partial_grid.py` | `tests/domain/test_solve_partial_grid.py`<br>`tests/domain/test_ac_us05_orchestration.py` | 6 + 6 | DT-05, AC-US-05-01~11, SV-01~05 |

**Domain fixture:** `tests/domain/conftest.py` — `magic_square_judge`  
**공유 격자:** `tests/fixtures/grids.py`

---

### 3.3 Integration — Track C (Boundary + 실제 Domain)

| # | TDD 슬라이스 | 관여 구현 | 테스트 | 테스트 수 | IT |
|---|-------------|-----------|--------|-----------|-----|
| C-01 | 유효 입력 E2E | `BoundaryResolver` + `SolvePartialGrid` | `tests/integration/test_boundary_to_domain.py` | 4 | IT-01, IT-02, IT-04, IT-06 |
| C-02 | 2차 시도 Validator 2회 | ↑ + `MagicSquareJudge` spy | `tests/integration/test_it02_validator_calls.py` | 1 | IT-02 |
| C-03 | OK 출력 문자열 | `ResponseFormatter` + resolver | `tests/integration/test_output_formatter.py` | 2 | IT-01 |

**Integration fixture:** `tests/integration/conftest.py` — `boundary_resolver_integration` (Domain spy 없음)

---

### 3.4 Regression — 계약 잠금

| # | TDD 슬라이스 | 테스트 | 테스트 수 | RG |
|---|-------------|--------|-----------|-----|
| R-01 | US-01 입력 오류 전체 | `tests/regression/test_us01_input_errors.py` | 9 | RG-US-01 |
| R-02 | US-01 resolver 경로 | `tests/regression/test_us01_boundary_resolver.py` | 8 | RG-US-01 |
| R-03 | US-05 출력·EC-5 | `tests/regression/test_us05_solver_output.py` | 2 | RG-US-05 |
| R-04 | Refactor 게이트 | `tests/regression/test_refactor_contract_gate.py` | 7 | RG-REFACTOR |

---

### 3.5 Entity (별도 슬라이스)

| TDD 슬라이스 | Green 구현 | RED / Green 테스트 | 테스트 수 |
|-------------|------------|------------------|-----------|
| User 엔티티 불변식 | `src/entity/user.py` | `tests/entity/test_user.py` | 4 |

> Entity는 마방진 US와 무관한 **ECB Entity 레이어 샘플** 구현이다.

---

## 4. User Story → 구현·테스트 묶음

| User Story | 구현 모듈 (Green) | RED 테스트 묶음 | 상태 |
|------------|-------------------|-----------------|------|
| **US-01** 입력 검증 | `input_validator`, `resolver`, `schemas`, `error_catalog` | `test_input_validator`, `test_boundary_resolver`, `test_ac_us01_*`, `test_error_contract`, `test_boundary_error_*` | Green |
| **US-02** 빈칸 좌표 | `empty_cell_locator` | `test_empty_cell_locator`, `test_ac_us02_*` | Green |
| **US-03** 누락 숫자 | `missing_number_resolver` | `test_missing_number_resolver`, `test_ac_us03_*` | Green |
| **US-04** 마방진 검증 | `magic_square_judge`, `constants` | `test_magic_square_judge`, `test_ac_us04_*`, `test_domain_infrastructure` | Green |
| **US-05** 조합 시도·해결 | `placement_trial_solver`, `solve_partial_grid` | `test_placement_trial_solver`, `test_solve_partial_grid`, `test_ac_us05_*` | Green |

---

## 5. 슬라이스별 실행 명령

각 TDD 단위를 **독립적으로** Green 확인할 때:

```powershell
cd c:\dev\MagicSquare

# Boundary 슬라이스
python -m pytest tests/boundary/test_input_validator.py -v      # B-01
python -m pytest tests/boundary/test_error_contract.py -v     # B-02
python -m pytest tests/boundary/test_boundary_resolver.py -v    # B-04
python -m pytest tests/boundary/ -v                             # Track A 전체 (55)

# Domain 슬라이스
python -m pytest tests/domain/test_domain_infrastructure.py -v  # D-00
python -m pytest tests/domain/test_empty_cell_locator.py -v     # D-01
python -m pytest tests/domain/test_missing_number_resolver.py -v # D-02
python -m pytest tests/domain/test_magic_square_judge.py -v     # D-03
python -m pytest tests/domain/test_placement_trial_solver.py -v # D-04
python -m pytest tests/domain/test_solve_partial_grid.py -v     # D-05
python -m pytest tests/domain/ -v                               # Track B 전체 (78)

# Integration + Regression
python -m pytest tests/integration/ -v                          # Track C (7)
python -m pytest tests/regression/ -v                           # 회귀 (26)

# 전체
python -m pytest tests/ -v                                      # 154
```

마커로 레이어 단위 실행:

```powershell
python -m pytest -m boundary -v
python -m pytest -m domain -v
python -m pytest -m integration -v
python -m pytest -m regression -v
```

---

## 6. 공유 Fixture 계약

| 파일 | 역할 | 사용 슬라이스 |
|------|------|---------------|
| `tests/fixtures/grids.py` | 유효/무효/퍼즐 격자 | D-01~05, C-01, R-03 |
| `tests/fixtures/error_catalog.py` | Boundary 에러 message 잠금 | B-02~07, R-04 |
| `tests/boundary/conftest.py` | `domain_spy` (Domain 0회/1회 검증) | B-04~07, R-02 |
| `tests/integration/conftest.py` | 실제 Domain 연결 resolver | C-01~03 |

### 주요 격자 fixture (Green 기준)

| Fixture | 용도 |
|---------|------|
| `VALID_GRID_TWO_BLANKS` | 1차 시도 성공 (missing 7, 16) |
| `GRID_PUZZLE_SECOND_TRIAL` | 2차 시도만 성공 (missing 3, 7) |
| `GRID_UNSOLVABLE` | 양쪽 시도 실패 → `UnsolvableGrid` |
| `KNOWN_MAGIC_SQUARE` | 완성 마방진 검증 |
| `GRID_CORNER_BLANK_0_0` | (0,0) 빈칸 1-index 변환 |

---

## 7. RED → Green 진행 요약

| Stage | 내용 | 산출물 |
|-------|------|--------|
| **Red** | Given-When-Then, `# AC-US-XX-YY`, fixture 선행 | `tests/**` 154케이스 |
| **Green** | ECB 레이어별 최소 구현 | `src/boundary/*`, `src/domain/*` |
| **Refactor** | 계약 불변 (카탈로그·OC·spy 격리) | `test_refactor_contract_gate`, 소스 리터럴 34 금지 |

**아직 없는 것:** CLI/UI 진입점 (`main.py`), `pyproject.toml`, 화면 출력 앱.

---

## 8. 파일 트리 (구현 + 테스트 대응)

```
src/
├── boundary/
│   ├── schemas.py              ← B-02
│   ├── error_catalog.py        ← B-03
│   ├── input_validator.py      ← B-01
│   ├── resolver.py             ← B-04~07
│   └── response_formatter.py   ← B-08
├── domain/
│   ├── constants.py            ← D-00
│   ├── exceptions.py             ← D-00
│   ├── empty_cell_locator.py   ← D-01
│   ├── missing_number_resolver.py ← D-02
│   ├── magic_square_judge.py   ← D-03
│   ├── placement_trial_solver.py ← D-04
│   └── solve_partial_grid.py   ← D-05
└── entity/
    └── user.py                 ← Entity 슬라이스

tests/
├── fixtures/                   ← 공유 RED 데이터
├── boundary/                   ← Track A (55)
├── domain/                     ← Track B (78)
├── integration/                ← Track C (7)
├── regression/                 ← 회귀 (26)
└── entity/                     ← Entity (4)
```

---

## 9. 참고 문서

| 문서 | 관계 |
|------|------|
| [test_plan.md](../test_plan.md) | Dual-Track 전략, mock/spy 규칙 |
| [05-dual-track-clean-architecture-tdd-design.md](./05-dual-track-clean-architecture-tdd-design.md) | ECB·Track 정의 |
| [06-cursorrules-user-entity-implementation-report.md](./06-cursorrules-user-entity-implementation-report.md) | Entity 슬라이스 패턴 |
| [07-epic-invariant-based-thinking-system-report.md](./07-epic-invariant-based-thinking-system-report.md) | INV-1~7 불변식 |
| [README.md](../README.md) | RED To-Do 체크리스트 (AC/BT 단위) |
