# Refactor 계획서

> **작성일:** 2026-05-29  
> **상태:** Phase 0~5 완료 — `209 passed`, CI coverage gate Green  
> **기준:** Golden Master 코드 리뷰, `pytest --cov=src` (201 passed)  
> **기준 설계:** [05-dual-track-clean-architecture-tdd-design.md](./05-dual-track-clean-architecture-tdd-design.md)  
> **선행 보고서:** [11-golden-master-implementation-report.md](./11-golden-master-implementation-report.md)  
> **프로젝트 규칙:** [`.cursor/rules/`](../.cursor/rules/) — Red → Green → Refactor, assertion 약화·테스트 삭제 금지

---

## 1. 목적

Green 상태 Solver·Boundary 구현을 **외부 계약(EC-1~5, OC-1~6, `int[6]`)을 깨지 않고** 구조 개선한다.

- **High:** 상수 SSOT, 검증기 중복, `int[6]` 변환, 예외 매핑 — Golden Master·회귀 게이트와 직결
- **Medium:** Golden fixture registry, mock 정합성, Parameter Object, GUI boilerplate, dead code
- **Low:** traceability 메타데이터, capture script, ECB Control 분리(별도 Phase)

---

## 2. 리팩토링 대상 목록 (우선순위 순)

| 순번 | 대상 파일 | 문제 | 적용 기법 | 우선순위 |
|------|-----------|------|-----------|----------|
| 1 | `src/domain/constants.py` + … | … | **Extract Constant** — ✅ Phase 2 완료 (2026-05-29) | **High** |
| 2 | … | … | **Extract Class / Strategy** — ✅ Phase 3 (`grid_validation.py`) | **High** |
| 3 | … | … | **SSOT 통일** — ✅ Phase 1 완료 | **High** |
| 4 | … | … | **Extract Method** — ✅ Phase 3 (`solution_vector.py`) | **High** |
| 5 | … | … | **Mapping Table** — ✅ Phase 3 (`domain_exception_mapping.py`) | **High** |
| 6 | … | … | **SSOT 통일** — ✅ Phase 1 완료 (`GOLDEN_MASTER_GRIDS`) | **Medium** |
| 7 | … | … | **Clarify Intent** — ✅ Phase 1 완료 (spy mock 주석) | **Medium** |
| 8 | … | … | **Parameter Object** — ✅ Phase 4 (`PlacementContext`) | **Medium** |
| 9 | … | … | **Remove Dead Code** — ✅ Phase 4 (`grid_validation`) | **Medium** |
| 10 | … | … | **Mixin** — ✅ Phase 4 (`StatusMixin`) | **Medium** |
| 11 | … | … | **Domain Guard** — ✅ Phase 4 | **Medium** |
| 13 | … | … | **Test traceability** — ✅ Phase 4 | **Low** |
| 12 | `SolvePartialGrid`, `PlacementTrialSolver`, `CompleteGridVerifier` | `judge or MagicSquareJudge()` 패턴 3회 반복 | **Extract Factory** — `_default_judge(judge)` (Domain 내부 private) | **Low** |
| 13 | `tests/fixtures/golden_master/solver_outputs.py` | `ac_ids`/`test_ids` 메타데이터 미검증 | **Test traceability** — ✅ Phase 4 | **Low** |
| 14 | `scripts/` (신규), `solver_outputs.py` docstring | 캡처 스크립트 부재 | **Add Script** — baseline 재생성 자동화 | **Low** |
| 15 | `src/entity/user.py`, `src/domain/` (구조) | Magic Square와 무관한 Entity scaffold. Control 레이어 부재 | **Architectural (별도 Phase)** — `src/control/` 분리·scaffold 정리 | **Low** |
| 16 | `src/boundary/ui/main_window.py`, `main.py`, `samples.py` | GUI 0% coverage | **pytest-qt / Smoke Test** — 계약 무관, 별 트랙 | **Low** |

---

## 3. 테스트 선행 필요 항목

리팩토링 **전에** Red → Green으로 테스트를 추가·보강해야 할 대상.

### 3.1 Boundary — 검증기 통합(순번 2) 전 필수

| 함수 | 파일 | 추가할 테스트 내용 |
|------|------|-------------------|
| `CompleteGridVerifier._validate_structure` | `complete_grid_verifier.py` | 비 list grid, 행 수 ≠ 4, 열 수 ≠ 4, non-int 셀 → 각각 `INVALID_SIZE` / `CELL_VALUE_OUT_OF_RANGE` |
| `CompleteGridVerifier.verify` | `complete_grid_verifier.py` | Mock Judge가 `GridNotComplete` / `InvalidGridSize` raise → `INVALID_SIZE` 매핑 |
| `InputValidator.validate` | `input_validator.py` | partial 정책(0 허용, 빈칸 2, float→`INVALID_SIZE`) 스냅샷 또는 parametrized parity test |
| *(신규)* parity test | 테스트 파일 1개 | **동일 complete grid**에 대해 Verifier 통과/실패가 기대와 일치하는지 교차 검증 |

### 3.2 Domain — 상수·Judge 분기(순번 1, 11) 전 권장

| 함수 | 파일 | 추가할 테스트 내용 |
|------|------|-------------------|
| `MagicSquareJudge.is_magic` | `magic_square_judge.py` | row 합 34 유지 + column만 깨지는 fixture, main/anti diagonal만 깨지는 fixture |
| `MagicSquareJudge._all_columns_equal_constant` | `magic_square_judge.py` | column loop 내부 `False` 경로 커버 |
| `MissingNumberResolver.resolve` | `missing_number_resolver.py` | (선택) guard 추가 시 Red 선행 |

### 3.3 Boundary UI — grid_io(순번 1 연동) 전 권장

| 함수 | 파일 | 추가할 테스트 내용 |
|------|------|-------------------|
| `parse_cell_text` | `grid_io.py` | `17`, `-1` → `GridParseError` |
| `read_grid` | `grid_io.py` | 행 ≠ 4, 열 ≠ 4 → `GridParseError` |
| `apply_solution` | `grid_io.py` | `len(result) != 6` → `ValueError` |

### 3.4 Golden Master / Contract — 순번 4~6 전 baseline

| 대상 | 내용 |
|------|------|
| `test_golden_master_solver.py` | 리팩터 시작 전 **현재 16건 Green** 스냅샷 확보 |
| `test_refactor_contract_gate.py` | contract snapshot 게이트 Green 확인 |
| `test_boundary_resolver.py` | spy mock 정합성(순번 7) — mock 값 변경 시 의도적 Red 확인 |

### 3.5 테스트 추가 불필요 (이미 Green·Golden Master로 잠김)

- `SolvePartialGrid.execute` — Golden Master + OC 회귀
- `BoundaryResolver.solve` — BT + Golden Master boundary
- `ResponseFormatter.format_success` — IT + Golden Master formatted
- `PlacementTrialSolver.solve` — Domain AC + Golden Master (Parameter Object화 시 Green 유지만 확인)

---

## 4. 리팩토링 후 검증 방법

### 4.1 회귀 테스트 실행 명령어

**1단계 — 계약 게이트 (필수)**

```powershell
cd c:\dev\MagicSquare

python -m pytest tests/regression/test_golden_master_solver.py -v
python -m pytest tests/regression/ -v
python -m pytest tests/boundary/test_input_validator.py tests/boundary/test_ac_us01_domain_isolation.py -v
```

**2단계 — 전체 스위트 (필수)**

```powershell
python -m pytest tests/ -q
# 기대: 178 passed (테스트 추가 시 그 이상, 기존 178건 Green 유지)
```

**3단계 — 리팩터 대상 모듈 집중 (권장)**

```powershell
python -m pytest tests/boundary/test_complete_grid_verifier.py tests/boundary/test_grid_io.py tests/domain/test_magic_square_judge.py -v
```

**4단계 — branch 커버리지 (Refactor Phase 완료 기준)**

```powershell
python -m pytest tests/ --cov=src --cov-branch --cov-report=term-missing -q
# 목표: Boundary ≥85%, Domain ≥95% (GUI omit 설정 검토)
```

**5단계 — baseline 재캡처 (의도적 출력 변경 없을 때 생략)**

```powershell
# capture script 추가 후 (순번 14)
# python scripts/capture_golden_master.py
python -m pytest tests/regression/test_golden_master_solver.py -v
```

### 4.2 외부 동작 불변 확인

| 확인 항목 | 방법 | 기대 결과 |
|-----------|------|-----------|
| Solver 출력 (OC-1~6) | Golden Master 4 success fixture equality | `int[6]`, formatted 문자열 **바이트 단위 동일** |
| Unsolvable (EC-5) | Golden Master unsolvable 2건 | `UnsolvableGrid`, `DOMAIN_UNSOLVABLE` + message 동일 |
| 입력 오류 (EC-1~4) | `test_us01_input_errors.py` + Boundary 73 tests | 코드·메시지·검사 순서 불변 |
| Boundary 격리 | spy mock | invalid input → Domain `execute` 0회 |
| 통합 경로 | `tests/integration/` 7 tests | IT-01~06 동일 |
| 에러 카탈로그 | `test_error_contract.py`, Golden boundary error | `ERROR_CATALOG` 5종 불변 |
| GUI (선택) | 수동 smoke | Solve sample → `OK [2,3,7,4,4,16]`, Verify → sum 34 |

**Go / No-Go**

- **Go:** 178+ tests Green + Golden Master 16 Green + regression/contract gate Green
- **No-Go:** Golden Master 또는 EC/OC 회귀 실패 → revert 후 Green 복구

---

## 5. 권장 실행 Phase

| Phase | 내용 | 계획 순번 |
|-------|------|-----------|
| **0 — Test First** | §3 테스트 선행 Red → Green | — |
| **1 — Low Risk** | ERROR_CATALOG SSOT, Golden registry, mock 주석 | 3, 6, 7 |
| **2 — High Risk** | constants SSOT → 파일별 치환 + Golden Master 매 단계 | 1 |
| **3 — High Risk** | 검증기 Strategy, exception mapping | 2, 5 |
| **4 — Medium** | PlacementContext, GUI mixin, dead code, Domain guard | 8, 9, 10, 11 |
| **5 — Verify** | §4 검증 전체 + coverage gate | — |
| **별도 Phase** | Control 레이어, GUI E2E, capture script | 14, 15, 16 |

---

## 6. README TODO 매핑

| README TODO | 계획 순번 | Phase |
|-------------|-----------|-------|
| 캡처 스크립트 | 14 | 별도 |
| 이중 fixture 레지스트리 | 6 | 1 |
| mock vs Golden baseline | 7 | 1 |
| CompleteGridVerifier 분기 테스트 | §3.1 | 0 |
| grid_io 분기 테스트 | §3.3 | 0 |
| MagicSquareJudge 경로 분리 | §3.2 | 0 |
| Golden Master traceability | 13 | 4 |
| Refactor (구조 개선) | §2 전체 | 1~4 |
| branch 커버리지 / CI | §4.1 4단계 | 5 |
| GUI E2E | 16 | 별도 |

---

## 7. 변경 이력

| 날짜 | 내용 |
|------|------|
| 2026-05-29 | 초안 — Golden Master 리뷰·리팩토링 점검 기반 Plan only |
| 2026-05-29 | **Phase 0~1 실행** — 분기 테스트 +17, ERROR_CATALOG SSOT, `GOLDEN_MASTER_GRIDS` 통합 (`195 passed`) |
| 2026-05-29 | **Phase 4 실행** — PlacementContext, StatusMixin, Domain guard, traceability (`209 passed`) |

---

## 8. Phase 2 실행 결과 (2026-05-29)

### 8.1 `src/domain/constants.py` SSOT

| 상수 | 값 | 용도 |
|------|-----|------|
| `GRID_SIZE` | 4 | 4×4 격자 |
| `MAGIC_CONSTANT` | 34 | 마방 합 |
| `BLANK_CELL` | 0 | 빈칸 |
| `MIN_PARTIAL_CELL_VALUE` | 0 | Solver/입력 IC-2 (0 허용) |
| `MIN_FILLED_CELL_VALUE` | 1 | Complete verify (blank 없음) |
| `MAX_CELL_VALUE` | 16 | 셀 상한 |
| `REQUIRED_BLANK_COUNT` | 2 | IC-3 |
| `SOLUTION_VECTOR_LENGTH` | 6 | OC-1 |
| `CELL_COUNT` | 16 | complete grid unique count |

### 8.2 치환 모듈

- **Domain:** `magic_square_judge`, `missing_number_resolver`, `empty_cell_locator`
- **Boundary:** `input_validator`, `complete_grid_verifier`, `grid_io`

### 8.3 검증

```powershell
python -m pytest tests/regression/test_golden_master_solver.py -v  # 17 passed
python -m pytest tests/ -q                                         # 196 passed
```

EC-2 partial(0~16) vs complete(1~16) 정책 **유지** 확인.

---

## 9. Phase 3 실행 결과 (2026-05-29)

### 9.1 신규 모듈

| 모듈 | 역할 |
|------|------|
| `src/boundary/grid_validation.py` | `GridStructureValidator` + partial/complete policy |
| `src/boundary/domain_exception_mapping.py` | `boundary_error_code_for` |
| `src/domain/solution_vector.py` | `to_solution_vector` (OC-3 1-index) |

### 9.2 리팩터 대상

- `input_validator.py` → `GridStructureValidator(PARTIAL_GRID_POLICY)` 위임
- `complete_grid_verifier.py` → `GridStructureValidator(COMPLETE_GRID_POLICY)` + mapping
- `resolver.py` → `boundary_error_code_for` 사용
- `solve_partial_grid.py` → `to_solution_vector` 사용

### 9.3 검증

```powershell
python -m pytest tests/regression/test_golden_master_solver.py -v  # 17 passed
python -m pytest tests/ -q                                         # 201 passed
```

---

## 10. Phase 4 실행 결과 (2026-05-29)

### 10.1 변경 요약

| 항목 | 내용 |
|------|------|
| `PlacementContext` | `PlacementTrialSolver.solve(context)`, `_trial` → `bool` |
| `grid_validation.py` | redundant `len(seen) != CELL_COUNT` 제거 |
| `status_mixin.py` | `StatusMixin` for Solve/Verify tabs |
| Domain guard | `GridNotComplete` when blank/missing count ≠ 2 |
| Golden Master | `test_golden_master_traceability_metadata_is_present` × 6 |

### 10.2 검증

```powershell
python -m pytest tests/regression/test_golden_master_solver.py -v  # 23 passed
python -m pytest tests/ -q                                         # 209 passed
```

---

## 11. Phase 5 실행 결과 (2026-05-29)

### 11.1 변경 요약

| 항목 | 내용 |
|------|------|
| `pyproject.toml` | pytest markers, coverage `omit`(GUI/`main.py`/`entity`), branch 측정 |
| `.github/workflows/ci.yml` | pytest + Golden Master + Domain ≥95% / Boundary ≥85% gate |
| `grids.py` | main/anti diagonal fixture — row·column 합 34 유지, 대각선만 깨짐 |
| `test_magic_square_judge.py` | column/diagonal 분기 assertion 보강 |

### 11.2 커버리지 (GUI omit)

| 패키지 | Branch | 비고 |
|--------|--------|------|
| `src/domain/` | **100%** | `magic_square_judge` 대각선 분기 Green |
| `src/boundary/` (core) | **98%** | `resolver`/`verifier` L49 unknown re-raise 잔존 |

### 11.3 검증

```powershell
python -m pytest tests/ -q
python -m pytest tests/ --cov=src/boundary --cov=src/domain --cov-branch -q
python -m coverage report --include='src/domain/*' --fail-under=95
python -m coverage report --include='src/boundary/*' --omit='src/boundary/ui/main_window.py,src/boundary/ui/samples.py,src/boundary/ui/status_mixin.py' --fail-under=85
```
