# MagicSquare

4×4 마방진을 **생성**하고 **검증**하는 프로그램 프로젝트입니다.  
Boundary·Domain **Green** 구현 완료, 통합·회귀·Golden Master baseline 잠금까지 진행된 상태입니다.

> **테스트:** `178 passed` (`python -m pytest tests/ -q`, 2026-05-29)

## 한 줄 요약

1~16을 한 번씩 4×4 격자에 놓았을 때, 모든 행·열·대각선의 합이 같아지는 배치를 **얻거나**, 주어진 배치가 그 규칙을 **만족하는지 화면에서 확인**하는 도구를 만드는 것이 목표입니다.

## 확정된 요구 (2026-05-28)

| 항목 | 내용 |
|------|------|
| 격자 | 4×4 고정 |
| 숫자 | 1~16, 각 숫자 1회 |
| 핵심 기능 | **생성** + **검증** (동등하게 중요) |
| 결과 표시 | **화면만** (파일·API·공유 불필요) |
| 관점 | **실제 서비스** 수준의 정확성·명확한 오류·일관된 규칙 |

## 도메인 (참고)

- **마방 상수**: 34 (각 행·열·대각선의 합)
- **유효 조건**: 4행, 4열, 주대각선, 부대각선의 합이 모두 34

생성 결과는 검증과 **동일한 규칙**을 따르며, 내부적으로도 그 기준을 통과해야 합니다.

## 빠른 시작

### 의존성 설치

```powershell
cd c:\dev\MagicSquare
pip install -e ".[dev]"
```

GUI 사용 시:

```powershell
pip install -e ".[gui]"
```

### 테스트 실행

```powershell
# 전체
python -m pytest tests/ -v

# 트랙별
python -m pytest tests/boundary/ -v    # 73
python -m pytest tests/domain/ -v      # 52
python -m pytest tests/integration/ -v # 7
python -m pytest tests/regression/ -v  # 42

# Golden Master만
python -m pytest tests/regression/test_golden_master_solver.py -v  # 16
```

### GUI 실행

```powershell
python main.py
```

## 프로젝트 구조

```
MagicSquare/
├── README.md
├── main.py                          ← PyQt6 GUI 진입점
├── pyproject.toml
├── docs/test_plan.md                ← pytest 테스트 계획서
├── src/
│   ├── boundary/                    ← US-01 입력 검증·위임·출력
│   │   ├── input_validator.py
│   │   ├── resolver.py
│   │   ├── response_formatter.py
│   │   └── ui/                      ← PyQt6 데스크톱 UI
│   └── domain/                      ← US-02~05 퍼즐 해결 로직
│       ├── empty_cell_locator.py
│       ├── missing_number_resolver.py
│       ├── magic_square_judge.py
│       ├── placement_trial_solver.py
│       └── solve_partial_grid.py
├── tests/
│   ├── boundary/                    ← Track A (73 tests)
│   ├── domain/                      ← Track B (52 tests)
│   ├── integration/                 ← Track C 통합 (7 tests)
│   ├── regression/                  ← Track C 회귀 (42 tests)
│   └── fixtures/
│       ├── grids.py
│       ├── error_catalog.py
│       └── golden_master/           ← Golden Master baseline
│           └── solver_outputs.py
├── report/                          ← 문제 정의·설계·구현 보고서
└── prompt/                          ← 대화·프롬프트 기록
```

## 문서

| 문서 | 설명 |
|------|------|
| [docs/test_plan.md](./docs/test_plan.md) | pytest Dual-Track 계획, mock/spy, 커버리지 |
| [report/README.md](./report/README.md) | 리포트 목차 |
| [report/09-user-stories-magic-square-4x4-report.md](./report/09-user-stories-magic-square-4x4-report.md) | US-01~05 User Stories |
| [report/10-red-green-implementation-mapping.md](./report/10-red-green-implementation-mapping.md) | RED ↔ Green 구현·테스트 매핑 |
| [report/11-golden-master-implementation-report.md](./report/11-golden-master-implementation-report.md) | Golden Master baseline 구현 보고서 |

## 범위 요약

### 포함 (In scope)

- 유효한 4×4 마방진 **생성** 및 화면 표시 (PyQt6 GUI)
- 사용자/시스템이 만든 4×4 배치 **검증** 및 결과 표시
- 잘못된 입력에 대한 **명확한 Boundary 오류** (`INVALID_SIZE` 등)
- 빈칸 2개 퍼즐 **Solver** → `int[6]` / `OK [r1,c1,n1,r2,c2,n2]`

### 제외 (현 단계 Out of scope)

- 파일 저장, REST API, 공유 URL
- n×n 일반화, 사용자 정의 숫자 범위
- 계정·결제 등 엔터프라이즈 기능

## 현재 상태 (2026-05-29)

| 구분 | 상태 |
|------|------|
| 문제 정의 | 완료 (`report/01~04`) |
| 설계 | 완료 (`report/05`, `08~09`) |
| 구현 | **Green** — Boundary + Domain + GUI |
| 테스트 | **178 passed** — Boundary 73 / Domain 52 / Integration 7 / Regression 42 |
| Golden Master | **16 passed** — solver 출력 baseline 잠금 |
| Refactor / 커버리지 게이트 | 진행 예정 (branch ≥85% / ≥95%) |

## 구현·테스트 현황

> Dual-Track TDD: **Red → Green 완료**, Stage 5 Regression·Golden Master 진행 중.  
> 상세: [`docs/test_plan.md`](./docs/test_plan.md), [`report/10-red-green-implementation-mapping.md`](./report/10-red-green-implementation-mapping.md)

### Track A — Boundary (US-01) — Green

**P0 — 시드·격리**

- [x] **BT-01** — `grid=None` → `INVALID_SIZE` + Domain `execute` 0회
- [x] **BT-02** — 비 4×4 입력 회귀 → `INVALID_SIZE`, Domain 0회
- [x] **BT-03** — 유효 입력 → Domain `execute` 1회

**P1 — EC-2~4·순서·매핑**

- [x] **BT-04** — 값 범위 위반 → `CELL_VALUE_OUT_OF_RANGE`
- [x] **BT-05** — 빈칸 0/1/3개 → `EMPTY_CELL_COUNT_INVALID`
- [x] **BT-06** — non-zero 중복 → `DUPLICATE_NON_ZERO`
- [x] **BT-07** — 검사 순서 잠금 (ORD-01, ORD-02)
- [x] **DOM-01** — 유효 입력 + `UnsolvableGrid` → `DOMAIN_UNSOLVABLE`
- [x] **AC-US-01-06** — IC 위반 시 Domain resolver 0회

**P2 — Contract·인프라**

- [x] **BT-08** — Error Contract 일관성 (pydantic + 카탈로그)
- [x] `tests/boundary/conftest.py` — `domain_spy` / `boundary_resolver`
- [x] `src/boundary/input_validator.py`, `resolver.py`, `schemas.py`, `error_catalog.py`
- [x] `src/boundary/response_formatter.py` — `OK [r1,c1,n1,r2,c2,n2]`
- [x] `tests/boundary/test_*` — Boundary 전체 Green

**US-01 Acceptance Criteria**

- [x] **AC-US-01-01** ~ **AC-US-01-07** — IC/EC 계약 + Domain 격리

### Track B — Domain (US-02~05) — Green

#### US-02 — `EmptyCellLocator`

- [x] **DT-01**, **AC-US-02-01** ~ **AC-US-02-06**
- [x] `src/domain/empty_cell_locator.py`

#### US-03 — `MissingNumberResolver`

- [x] **DT-02**, **AC-US-03-01** ~ **AC-US-03-05**
- [x] `src/domain/missing_number_resolver.py`

#### US-04 — `MagicSquareJudge`

- [x] **DT-03**, **AC-US-04-01** ~ **AC-US-04-08**, **DM-E01** ~ **DM-E02**
- [x] `src/domain/magic_square_judge.py`, `constants.py` (`MAGIC_CONSTANT = 34`)

#### US-05 — Solver + Orchestration

- [x] **DT-04**, **DT-05**, **AC-US-05-01** ~ **AC-US-05-11**, **DM-E03**
- [x] `src/domain/placement_trial_solver.py`, `solve_partial_grid.py`
- [x] `src/domain/exceptions.py` — `GridNotComplete`, `InvalidGridSize`, `UnsolvableGrid`

**공통 Domain 인프라**

- [x] `tests/fixtures/grids.py`, `error_catalog.py`
- [x] `tests/domain/test_ac_us02~05_*.py` — AC 회귀 Green

### Track C — 통합 / 회귀 (Stage 4~5)

**P2 — 통합**

- [x] **IT-01** — 유효 입력 → `int[6]` / `OK [r1,c1,n1,r2,c2,n2]`
- [x] **IT-02** — 1차 실패·2차 성공 → Validator 2회
- [x] **IT-04** — 3×4 → `INVALID_SIZE`, Domain 미호출
- [x] **IT-06** — unsolvable → `DOMAIN_UNSOLVABLE` / EC-5
- [x] `tests/integration/test_boundary_to_domain.py`
- [x] `tests/integration/test_output_formatter.py`
- [x] `tests/integration/test_it02_validator_calls.py`

**P3 — 회귀·리팩토링 게이트**

- [x] **RG-US-01** — EC-1~4 입력 오류 회귀 Suite Green
- [x] **RG-US-05** — EC-5 + OC-1~6 출력 형식 회귀 Green
- [x] **RG-REFACTOR** — contract snapshot 게이트 (`test_refactor_contract_gate.py`)
- [x] `tests/regression/test_us01_input_errors.py`
- [x] `tests/regression/test_us05_solver_output.py`

#### Golden Master (출력 baseline 잠금)

Green 솔버의 **실제 런타임 출력**을 fixture별로 고정합니다. 구조 검증(`test_us05_solver_output.py`)과 달리 **정확한 숫자·문자열** equality를 검사합니다.

| Fixture | Domain baseline | Formatted |
|---------|-----------------|-----------|
| `VALID_GRID_TWO_BLANKS` | `[2, 3, 7, 4, 4, 16]` | `OK [2,3,7,4,4,16]` |
| `GRID_PUZZLE_SECOND_TRIAL` | `[2, 3, 7, 3, 1, 3]` | `OK [2,3,7,3,1,3]` |
| `GRID_CORNER_BLANK_0_0` | `[1, 1, 1, 4, 4, 16]` | `OK [1,1,1,4,4,16]` |
| `GRID_MISSING_15_16` | `[1, 2, 15, 4, 4, 16]` | `OK [1,2,15,4,4,16]` |
| `GRID_MISSING_3_7` | `UnsolvableGrid` | — |
| `GRID_UNSOLVABLE` | `UnsolvableGrid` | — |

- [x] `tests/fixtures/golden_master/solver_outputs.py` — baseline dict
- [x] `tests/regression/test_golden_master_solver.py` — 16 tests Green
- 상세: [report/11-golden-master-implementation-report.md](./report/11-golden-master-implementation-report.md)

> **참고:** `grids.py`의 `VALID_GRID_SUCCESS_RESULT = [2,3,5,4,1,11]`은 Boundary **spy mock**용 목값이며, 실제 솔버 Golden baseline과 다릅니다.

### 커버리지 목표 (미측정)

- [ ] `pytest --cov=src --cov-report=term-missing` — 로컬 측정
- [ ] Boundary branch **≥ 85%** (`src/boundary/`)
- [ ] Domain branch **≥ 95%** (`src/domain/`)
- [ ] `pyproject.toml` — pytest markers, coverage `omit`/`branch` 설정
- [ ] CI 파이프라인

| 레이어 | Branch 목표 | 측정 패키지 | User Story |
|--------|-------------|-------------|------------|
| Boundary | **≥ 85%** | `src/boundary/` | US-01 |
| Domain | **≥ 95%** | `src/domain/` | US-02~05 |
| 전체 (참고) | ≥ 90% | `src/` | US-01~05 |

### 결함 목록 연결 (Traceability)

#### US-01 — Boundary

| Case ID | 입력 / 조건 | 기대 | 테스트 |
|---------|-------------|------|--------|
| EC1-01 | `grid=None` | `INVALID_SIZE` | BT-01 |
| EC1-02~09 | 크기·형식 위반 | `INVALID_SIZE` | BT-02 |
| EC2-01~04 | 17 / -1 / `"7"` / `None` | `CELL_VALUE_OUT_OF_RANGE` | BT-04 |
| EC3-01~03 | 빈칸 0 / 1 / 3 | `EMPTY_CELL_COUNT_INVALID` | BT-05 |
| EC4-01 | non-zero 중복 | `DUPLICATE_NON_ZERO` | BT-06 |
| ORD-01~02 | 검사 순서 | 고정 순서 | BT-07 |
| DOM-01~02 | Domain 위임 | error / success | BT-03, DOM-01 |

#### US-02~04 — Domain

| Case ID | 기대 | 테스트 |
|---------|------|--------|
| BL-01~03 | 빈칸 탐색 | DT-01, AC-US-02 |
| MN-01~03 | 누락 숫자 | DT-02, AC-US-03 |
| MV-01~04 | 마방진 판정 | DT-03, AC-US-04 |
| DM-E01~02 | 전제 위반 예외 | DT-03 |

#### US-05 — Solver

| Case ID | 기대 | 테스트 |
|---------|------|--------|
| SV-01~05 | 1차/2차 시도, 좌표, no hardcode | DT-04~05, AC-US-05 |
| EC5-01 | unsolvable | DT-05, Golden Master |
| OC-01~06 | `int[6]` 1-index | DT-05, Golden Master |

## 다음 단계

1. **Refactor** — 구조 개선, Golden Master·contract 게이트 Green 유지
2. **커버리지 게이트** — Boundary ≥85%, Domain ≥95% 측정·CI 연동
3. **정합성 정리** — `VALID_GRID_SUCCESS_RESULT`(mock) vs Golden baseline 통일 여부 결정
4. **Data 레이어** — Repository 패턴 (설계 `report/05` §3, 별도 Phase)

## 라이선스

미정 (코드 추가 시 설정 예정)
