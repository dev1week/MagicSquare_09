# Refactor 계획서

> **작성일:** 2026-05-29  
> **상태:** 계획 — 코드 변경 전 (Plan only)  
> **기준:** Golden Master 코드 리뷰, 리팩토링 점검 항목 분석, `pytest --cov=src` (178 passed, line cov. 59%)  
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
| 1 | `src/domain/constants.py` + `input_validator.py`, `complete_grid_verifier.py`, `magic_square_judge.py`, `missing_number_resolver.py`, `grid_io.py` | `4`, `16`, `34`, `6` 등 매직 넘버가 4곳 이상 분산. SSOT 없이 치환 시 EC-2(0~16 vs 1~16) 혼동 위험 | **Extract Constant** — `GRID_SIZE`, `MIN/MAX_CELL_VALUE`, `BLANK_CELL`, `SOLUTION_VECTOR_LENGTH`, `MAGIC_CONSTANT`를 Domain constants에 집약 후 import 치환 | **High** |
| 2 | `src/boundary/input_validator.py`, `src/boundary/complete_grid_verifier.py` | 4×4 크기·타입·중복 검사 로직 중복. partial(0 허용·빈칸 2) vs complete(1~16·16개) 정책 차이가 묵시적 | **Extract Class / Strategy** — 공통 `GridStructureValidator` + `PartialGridPolicy` / `CompleteGridPolicy` 분리. 기존 public API·에러 코드 유지 | **High** |
| 3 | `tests/fixtures/error_catalog.py`, `src/boundary/error_catalog.py` | ERROR_CATALOG 이중 SSOT. 메시지 1글자 변경 시 BT-08·Golden Master 불일치 | **SSOT 통일** — tests는 `src.boundary.error_catalog` import만 사용 | **High** |
| 4 | `src/domain/solve_partial_grid.py` | 0-index → 1-index 변환·`int[6]` 조립이 유일 지점. 리팩터 시 OC-1~6·Golden Master 전체 영향 | **Preserve + Extract Method** — `to_solution_vector(...)` 등 의미 단위 추출만 허용, 시그니처·순서 불변 | **High** |
| 5 | `src/boundary/resolver.py`, `src/boundary/complete_grid_verifier.py` | `UnsolvableGrid`→`DOMAIN_UNSOLVABLE`, `GridNotComplete`/`InvalidGridSize`→`INVALID_SIZE` 매핑 분산 | **Extract Method / Mapping Table** — `_map_domain_exception(exc)` 단일 함수로 통합 (동작 동일) | **High** |
| 6 | `tests/regression/test_golden_master_solver.py`, `tests/fixtures/golden_master/solver_outputs.py`, `tests/fixtures/grids.py` | `_FIXTURE_GRIDS`와 `GOLDEN_MASTER_SOLVER_OUTPUTS` 키 이중 관리. 키 불일치 시 `KeyError` | **SSOT 통일** — golden record에 grid 참조 키만 두거나, grids dict를 golden에서 derive | **Medium** |
| 7 | `tests/fixtures/grids.py`, `tests/boundary/test_boundary_resolver.py` | `VALID_GRID_SUCCESS_RESULT` mock 목값 ≠ 실제 Golden `[2,3,7,4,4,16]` | **Clarify Intent** — mock 전용 alias·주석 명시 또는 golden baseline으로 통일 | **Medium** |
| 8 | `src/domain/placement_trial_solver.py` | `solve`/`_trial` 매개변수 5개. `_trial` 반환 grid는 caller에서 미사용(dead return) | **Introduce Parameter Object** — `PlacementContext` dataclass. `_trial`은 `bool` 반환으로 단순화 | **Medium** |
| 9 | `src/boundary/complete_grid_verifier.py` | L71–72 `len(seen) != 16` 분기 — 도달 불가에 가까운 dead branch | **Remove Dead Code** — 분기 제거 전 테스트로 “절대 호출 안 됨” 증명 | **Medium** |
| 10 | `src/boundary/ui/main_window.py` | `SolveTab`/`VerifyTab` `_set_status`·탭 boilerplate 중복. Verify blank 선차단으로 Verifier 에러 경로와 GUI 메시지 diverge | **Extract Superclass / Mixin** — `StatusMixin`, `TabShell` 추출. Verify blank 검사는 Verifier 위임 검토 | **Medium** |
| 11 | `src/domain/empty_cell_locator.py`, `src/domain/missing_number_resolver.py` | Boundary 전제(빈칸 2·누락 2) 미검증 → 직접 호출 시 `IndexError` | **Precondition Assert / Domain Guard** — 명시 예외 또는 docstring+private guard | **Medium** |
| 12 | `SolvePartialGrid`, `PlacementTrialSolver`, `CompleteGridVerifier` | `judge or MagicSquareJudge()` 패턴 3회 반복 | **Extract Factory** — `_default_judge(judge)` (Domain 내부 private) | **Low** |
| 13 | `tests/fixtures/golden_master/solver_outputs.py` | `ac_ids`/`test_ids` 메타데이터 미검증 | **Test or Remove** — traceability assert 추가 또는 fixture 단순화 | **Low** |
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
