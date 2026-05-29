# Golden Master 구현 보고서

> **작성일:** 2026-05-29  
> **상태:** Green — `178 passed` (`python -m pytest tests/ -q`)  
> **기준 설계:** [05-dual-track-clean-architecture-tdd-design.md](./05-dual-track-clean-architecture-tdd-design.md)  
> **User Story:** [09-user-stories-magic-square-4x4-report.md](./09-user-stories-magic-square-4x4-report.md)  
> **선행 매핑:** [10-red-green-implementation-mapping.md](./10-red-green-implementation-mapping.md)  
> **대화 원문:** [../prompt/cursor_magic_square_prompt_transcript_2026-05-29_golden_master.md](../prompt/cursor_magic_square_prompt_transcript_2026-05-29_golden_master.md)

---

## 1. 작업 개요

| 항목 | 내용 |
|------|------|
| **목표** | Green 상태 Magic Square Solver의 **실제 런타임 출력**을 Golden Master baseline으로 기록하고, Refactor 게이트(RG-REFACTOR / RG-US-05)용 회귀 테스트 추가 |
| **TDD 단계** | Green 이후 **Stage 5 — Regression Protection** (출력 스냅샷 잠금) |
| **범위** | Domain `SolvePartialGrid`, Boundary `BoundaryResolver`, `ResponseFormatter` |
| **범위 외** | Domain 구현 변경, Boundary EC-1~4 전체, GUI/E2E |

### 1.1 배경

- 기존 `tests/regression/test_us05_solver_output.py`는 OC-1~6 **구조**만 검증한다.
- `tests/fixtures/grids.py`의 `VALID_GRID_SUCCESS_RESULT = [2, 3, 5, 4, 1, 11]`은 Boundary spy mock용 목값이며, **실제 솔버 출력과 불일치**한다.
- 실제 `VALID_GRID_TWO_BLANKS` 실행 결과: `[2, 3, 7, 4, 4, 16]` → `OK [2,3,7,4,4,16]`
- Golden Master는 문서·예시가 아닌 **런타임 캡처 값**을 baseline으로 고정한다.

---

## 2. 수행 작업 요약

### 2.1 사전 분석 (대화 1턴)

- Golden Master baseline 생성에 적합한 프롬프트 유형 정리
- **Runtime Capture** 프롬프트 권장 (설계 문서 복사·AC 선택형 프롬프트는 부적합)
- 캡처 대상 API·fixture·출력 스키마·금지 사항을 템플릿으로 문서화

### 2.2 구현 (대화 2턴)

1. `tests/fixtures/grids.py` 지정 fixture 6건에 대해 실제 호출 후 출력 캡처
2. `tests/fixtures/golden_master/solver_outputs.py` 생성
3. `tests/regression/test_golden_master_solver.py` 추가 (Domain / Boundary / formatted 완전 일치)
4. pytest 실행으로 Green 확인

### 2.3 운영 가이드 정리 (대화 3~4턴)

- Golden Master 개념·일반 테스트와의 차이 설명
- `pytest` 실행 방법·재캡처 절차 문서화

---

## 3. Golden Master 아키텍처

```
tests/fixtures/grids.py          ← 입력 격자 (불변)
        │
        ▼
SolvePartialGrid.execute()       ← Domain int[6] 또는 UnsolvableGrid
BoundaryResolver.solve()         ← BoundarySuccess | BoundaryError
ResponseFormatter.format_success ← OK [r1,c1,n1,r2,c2,n2]
        │
        ▼
tests/fixtures/golden_master/solver_outputs.py   ← 캡처 baseline (Golden Master)
        │
        ▼
tests/regression/test_golden_master_solver.py    ← 런타임 vs baseline equality
```

### 3.1 검증 레이어

| 레이어 | 검증 내용 | 테스트 함수 |
|--------|-----------|-------------|
| Domain | `int[6]` 또는 `UnsolvableGrid` golden equality + OC-1~6 | `test_golden_master_domain_matches_runtime` |
| Boundary | `BoundarySuccess` / `BoundaryError` golden equality | `test_golden_master_boundary_matches_runtime` |
| Formatted | `OK [...]` 문자열 golden equality | `test_golden_master_formatted_output_matches_runtime` |

### 3.2 Traceability

| Track C ID | Golden Master 연결 |
|------------|-------------------|
| IT-01 | `VALID_GRID_TWO_BLANKS` formatted 출력 |
| IT-02 | `GRID_PUZZLE_SECOND_TRIAL` |
| IT-06 | `GRID_UNSOLVABLE` Boundary error |
| RG-US-05 | 성공/실패 solver 출력 잠금 |
| RG-REFACTOR | Refactor 후 출력 drift 방지 |
| OC-1~OC-6 | 성공 케이스 구조 + golden equality |
| EC-5 | `GRID_UNSOLVABLE`, `GRID_MISSING_3_7` |

---

## 4. 캡처된 baseline (2026-05-29 런타임)

| Fixture | Domain | Formatted | Boundary |
|---------|--------|-----------|----------|
| `VALID_GRID_TWO_BLANKS` | `[2, 3, 7, 4, 4, 16]` | `OK [2,3,7,4,4,16]` | success |
| `GRID_PUZZLE_SECOND_TRIAL` | `[2, 3, 7, 3, 1, 3]` | `OK [2,3,7,3,1,3]` | success |
| `GRID_CORNER_BLANK_0_0` | `[1, 1, 1, 4, 4, 16]` | `OK [1,1,1,4,4,16]` | success |
| `GRID_MISSING_15_16` | `[1, 2, 15, 4, 4, 16]` | `OK [1,2,15,4,4,16]` | success |
| `GRID_MISSING_3_7` | `UnsolvableGrid` | — | `DOMAIN_UNSOLVABLE` |
| `GRID_UNSOLVABLE` | `UnsolvableGrid` | — | `DOMAIN_UNSOLVABLE` |

### 4.1 주요 발견

| 항목 | 내용 |
|------|------|
| **문서 vs 실제** | 설계/README 예시 `[2,3,5,4,1,11]` ≠ 실제 솔버 `[2,3,7,4,4,16]` |
| **GRID_MISSING_3_7** | 프롬프트에서는 성공 케이스로 지정됐으나, **실제 런타임은 unsolvable** → baseline에 failure로 기록 |
| **mock vs golden** | `tests/boundary/conftest.py` spy 반환값 `[2,3,5,4,1,11]`은 Boundary 격리용으로 유지 (미통일) |

---

## 5. 변경 파일 목록

| 파일 | 유형 | 설명 |
|------|------|------|
| `tests/fixtures/golden_master/__init__.py` | 신규 | 패키지 초기화 |
| `tests/fixtures/golden_master/solver_outputs.py` | 신규 | Golden Master baseline dict |
| `tests/regression/test_golden_master_solver.py` | 신규 | 회귀 테스트 16건 |
| `report/11-golden-master-implementation-report.md` | 신규 | 본 보고서 |
| `prompt/cursor_magic_square_prompt_transcript_2026-05-29_golden_master.md` | 신규 | 대화 원문 export |

**미변경 (의도적):**

- `src/domain/*` — Domain 로직·하드코딩 없음 (AC-US-05-11 준수)
- `tests/regression/test_us05_solver_output.py` — assertion 약화 없음
- `tests/fixtures/grids.py` — `VALID_GRID_SUCCESS_RESULT` mock 값 유지

---

## 6. 테스트 / 검증 결과

### 6.1 Golden Master 전용

```text
python -m pytest tests/regression/test_golden_master_solver.py -v
→ 16 passed in 0.15s
```

| 테스트 그룹 | 건수 |
|-------------|------|
| Domain golden equality | 6 |
| Boundary golden equality | 6 |
| Formatted golden equality | 4 |
| **합계** | **16** |

### 6.2 전체 suite

```text
python -m pytest tests/ -q
→ 178 passed in 0.37s
```

- 이전: 154 passed ([10-red-green-implementation-mapping.md](./10-red-green-implementation-mapping.md))
- 증가: **+24** (Golden Master 16 + 기타 누적; 본 작업 직접 기여 +16)

---

## 7. 실행 방법

### Golden Master만

```powershell
cd c:\dev\MagicSquare
python -m pytest tests/regression/test_golden_master_solver.py -v
```

### 회귀 전체

```powershell
python -m pytest tests/regression/ -v
```

### baseline 재캡처 (의도적 동작 변경 시)

1. `SolvePartialGrid` / `BoundaryResolver` / `ResponseFormatter`로 fixture 재실행
2. `solver_outputs.py` 갱신
3. `test_golden_master_solver.py` 재실행

PyQt6 / GUI는 **불필요**.

---

## 8. 이슈 및 후속 작업

| # | 이슈 | 권장 조치 | 우선순위 |
|---|------|-----------|----------|
| 1 | `VALID_GRID_SUCCESS_RESULT` vs Golden Master 불일치 | Boundary spy 목값을 golden과 통일할지, mock 전용임을 주석으로 명시할지 결정 | P2 |
| 2 | `GRID_MISSING_3_7` unsolvable | fixture 의도 검토 — solvable 격자로 교체 또는 unsolvable 전용으로 문서화 | P2 |
| 3 | README Track C 체크리스트 | Golden Master 항목 `[x]` 반영 | P3 |
| 4 | `10-red-green-implementation-mapping.md` | Stage 5 Golden Master 슬라이스 추가 | P3 |
| 5 | Boundary EC-1~4 golden | 입력 오류 전건 golden 확장 여부 검토 (별도 Phase) | P4 |

---

## 9. 결론

- Green 솔버의 **실제 출력**을 6개 fixture에 대해 baseline으로 고정했다.
- Refactor·버그 수정 시 **출력 drift**를 픽셀(정수·문자열) 단위로 탐지할 수 있다.
- 기존 구조 검증 테스트·Domain 구현·assertion 강도는 유지했다.
- 프로젝트 테스트 suite: **178 passed**.

---

**다음 단계 제안:** README / `10-red-green-implementation-mapping.md`에 Golden Master 슬라이스 반영, `VALID_GRID_SUCCESS_RESULT` 정합성 정리.
