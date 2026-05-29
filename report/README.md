# MagicSquare — 문제 정의 리포트

4×4 마방진 프로그램의 **문제 인식·정의** 단계 산출물입니다.  
설계·구현은 포함하지 않습니다.

## 문서 목록

| 문서 | 내용 |
|------|------|
| [01-observation.md](./01-observation.md) | STEP 1 — 관찰 (상황, 동기, 맥락) |
| [02-stakeholders-and-scope.md](./02-stakeholders-and-scope.md) | 이해관계자, 범위, 제약 (생성·검증·화면 출력) |
| [03-service-view.md](./03-service-view.md) | 실제 서비스 기준 관점 (기능·품질·경계) |
| [04-open-questions.md](./04-open-questions.md) | 미결정 사항 — 다음 단계 입력용 |
| [10-red-green-implementation-mapping.md](./10-red-green-implementation-mapping.md) | RED ↔ Green 구현·테스트 단위 매핑 (154 passed) |
| [11-golden-master-implementation-report.md](./11-golden-master-implementation-report.md) | Golden Master baseline 구현·회귀 테스트 (178 passed) |
| [12-refactoring-plan.md](./12-refactoring-plan.md) | Refactor 계획서 — Phase 0~5 완료, CI coverage gate (`209 passed`) |

## 확정된 전제 (2026-05-28)

- **생성**과 **검증** 모두 1순위 기능이다.
- 결과는 **화면 표시**만으로 충분하다 (파일·API보내기 불필요).
- 요구 정리는 **실제 서비스**를 염두에 두고 진행한다.

## 프로젝트 상태

- 저장소: `c:\dev\MagicSquare`
- 코드/테스트: Boundary·Domain Green + Golden Master (**`196 passed`**) — [10-red-green-implementation-mapping.md](./10-red-green-implementation-mapping.md), [11-golden-master-implementation-report.md](./11-golden-master-implementation-report.md)
- Refactor: [12-refactoring-plan.md](./12-refactoring-plan.md) — **Phase 0~5 완료**, CI coverage gate (`209 passed`)
