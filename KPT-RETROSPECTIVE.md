# MagicSquare 프로젝트 KPT 회고

> **작성일:** 2026-05-29  
> **관점:** 프로젝트 진행자(학습자) 입장  
> **근거:** [`report/`](./report/) 단계별 보고서, [`prompt/`](./prompt/) 대화 원문, Cursor Agent 세션

*(작성중 초안)*

---

<details>
<summary><strong>회고 범위 요약 (8단계) — 펼치기</strong></summary>

| 단계 | 보고서 | 대화·프롬프트 (대표) |
|------|--------|----------------------|
| 1. 문제 정의 | `01`~`04` | [문제 정의 세션](prompt/cursor_4x4_magic_square_problem_definit.md) |
| 2. 설계 | `05` | [TDD 설계 프롬프트](prompt/cursor_magic_square_prompt_transcript_2026-05-28.md), [설계 실행](prompt/cursor_magic_square_prompt_transcript_2026-05-28_1538.md) |
| 3. 규칙·스캐폴드 | `06` | Cursor Rules·User 엔티티 대화 (5/28, Rules·mdc·User TDD) |
| 4. Epic → User Story | `07`~`09` | Epic·Journey·Story 대화 (5/28, [User Story 프롬프트](prompt/09-user-stories-magic-square-4x4-report_Prompt.md)) |
| 5. RED | README 체크리스트, `test_plan` | RED 테스트·플랜 대화 (5/28~29, [Green 전 transcript](prompt/cursor_magic_square_prompt_transcript_2026-05-29.md)) |
| 6. GREEN | `10` | Green·매핑·GUI·커밋 (위 5/29 transcript 동일 세션) |
| 7. Golden Master | `11` | [Golden Master transcript](prompt/cursor_magic_square_prompt_transcript_2026-05-29_golden_master.md) |
| 8. Refactor | `12` | [Refactor Phase 0~5 transcript](prompt/cursor_magic_square_prompt_transcript_2026-05-29_refactor-phase5.md) |

</details>

---

<details>
<summary><strong>1. 문제 정의</strong> (STEP 1~4, <code>01</code>~<code>04</code>)</summary>

### Keep

- `01-observation`처럼 **“마방진을 만든다”가 아니라 관찰 가능한 상황**으로 쓴 문장이 이후 Epic·Invariant·Contract로 자연스럽게 이어졌다.
- `04-open-questions`로 **아직 안 정한 것**을 분리해 두어, 설계 단계에서 소통 오류를 줄일 수 있었던 것이 유효했다.

### Problem

- 초반에는 대화 원문을 저장할 필요성을 크게 느끼지 못해서 저장이 잘안되었던 부분이 있다. 특히 readMe와 연동되는 부분이 꽤나 약했었는데 후반 단계로 갈수록 저장된 대화 기록을 참조하는 것이 생각보다 도움이 많이 되었다. 현업에서는 알려주신 agent를 활용해 간편하게 대화기록을 저장할 필요성이 있는 것 같다.

### Try

- 구현 금지를 좀더 간편하게 전달하기 위해 태그 파일같은 거를 만들어서 간편하게 해당 파일을 참조하게 하는 방식으로 개선해보고 싶다.

### Cursor 기능 (더 효율적으로)

| 지금 한 방식 | 추천 |
|--------------|------|
| 긴 문제 정의 프롬프트를 매번 새 채팅에 붙여넣기 | **`.cursor/rules`에 “문제 정의 단계: 코드·테스트·파일 생성 금지”** 규칙을 두고, `@report/01-observation.md`만 @-mention |
| 산출물을 채팅 안에만 두기 | **Composer에서 `report/xx.md` 생성 요청** + “기존 04와 모순 없게”처럼 **이전 report 파일을 @로 고정** |
| 대화가 길어지면 맥락 소실 | **채팅 Export** (`prompt/…`)를 단계 종료 루틴으로 고정 — 나중에 backup-agent·수동 Export 혼용을 줄임 |

</details>

<details>
<summary><strong>2. Dual-Track 설계</strong> (<code>05</code>)</summary>

### Keep

- **입력/출력 계약을 숫자·형식까지 고정**해 두어, 이후 US-01~05·RED 테스트 이름·AC ID가 설계 문서와 1:1로 맞았다.
- Domain Service를 **SRP 단위(빈칸·누락·판정·배치·유스케이스)**로 쪼개 둔 것이 Green 때 파일·테스트 슬라이스와 정확히 대응했다.
- Mermaid 시퀀스·Invariant 표가 **“왜 이 테스트가 있는가”**를 Refactor·Golden Master까지 설명하는 기준 문서가 됐다.

### Problem

- 설계 문서가 길어 **RED 체크리스트로 내릴 때 누락**이 생겼고, “체크가 안 된 부분은 왜 있어?” 같은 추가대화가 필요했다.
- 설계 단계 프롬프트 실행용 템플릿(`cursor_magic_square_prompt_transcript_2026-05-28`)과 **실제 산출 `05`의 생성 경로**가 한 README에 묶이지 않아, 나중에 “어느 프롬프트 버전이 05인가” 추적이 번거로웠다.

### Try

- `05` 확정 직후 **User Story 초안(09)의 AC ID 표만** 먼저 뽑아 README RED 섹션 골격을 만든다 (설계 전체를 한 번에 체크리스트화하지 않기).
- red 테스트 관련된 것을 굳이 readme에 넣어야할 필요가 있나란 생각이 있음. 각 plan 폴더를 만들어 각 단계별 체크리스트를 관리한다면 위와 같은 문제를 해결할 수 있을 것 같음.

### Cursor 기능

| 지금 | 추천 |
|------|------|
| 설계 전문 프롬프트를 수동 복붙 | **User Rule 또는 Skill**에 “Dual-Track 설계 출력 형식”을 저장해 `@skill`로 재사용 |
| 긴 설계를 한 턴에 요청 | **Plan 모드**(읽기 전용)로 설계만 검토·수정한 뒤, Agent 모드에서 `report/05` 파일화 — 설계 단계에서 실수로 `src/`가 생기는 일 방지 |
| Dual Track / ECB 개념 질문을 같은 세션에 섞음 | **Ask 모드**로 개념만 정리하고, 설계 산출은 별도 채팅 — 컨텍스트를 구현용으로 오염시키지 않음 |

</details>

<details>
<summary><strong>3. Cursor Rules · User 엔티티</strong> (<code>06</code>)</summary>

### Keep

- `.cursorrules` → **`.cursor/rules/*.mdc` 분할**으로 TDD·금지·아키텍처가 항상 적용되는 구조가 이후 Green·Refactor에서 **“테스트 약화 금지”**를 자동으로 상기시켰다.
- User 엔티티는 **RED(ModuleNotFound) → GREEN → REFACTOR** 순서를 짧게 경험해, 본편 Magic Square TDD 루틴의 리허설이 됐다.
- `code-reviewer` **커스텀 Agent**를 만든 것이 Golden Master·Refactor 전에 **mock vs baseline 불일치** 같은 함정을 미리 짚는 데 도움이 됐다.

### Problem

- User 엔티티는 Magic Square 도메인과 **무관한 scaffold**인데, 리포 구조상 `src/entity/`가 남아 **ECB Control 레이어 부재**와 함께 Refactor 백로그(순번 15)로 밀렸다.
- `.cursorrules` 제거 후 **mdc만 남았을 때** “어느 규칙이 우선인지”를 처음엔 스스로 헷갈릴 수 있었다.

### Try

- 학습용 scaffold는 `src/learning/` 또는 별도 브랜치로 두고, **메인 도메인 트리와 분리**한다.
- Rule 파일마다 **frontmatter `globs`**로 `src/domain/**`, `tests/**` 등 적용 범위를 좁혀 Magic Square 작업 시 노이즈를 줄인다.

### Cursor 기능

| 지금 | 추천 |
|------|------|
| 규칙 설계 → YAML 뼈대 → 섹션별 채우기를 여러 턴 | **create-rule Skill**로 `.mdc` 초안을 한 번에 생성 후, 사람이 `tdd_rules`만 검토 |
| `/code-reviewer`를 수동 호출 | Refactor·Golden Master **PR 직전에만** 호출하도록 README에 체크리스트화; 또는 **Bugbot**이 있다면 PR 단계에서 자동 |
| 규칙 검토를 채팅에만 의존 | **“문제점만 보고, 수정은 요청 시만”** 같은 메타 프롬프트를 Rule의 `ai_behavior`에 넣어 불필요한 대규모 수정 diff 방지 |

</details>

<details>
<summary><strong>4. Epic · User Journey · User Stories</strong> (<code>07</code>~<code>09</code>)</summary>

### Keep

- **Epic → Journey → Story**로 층을 나누고, 매 Story에 **보호 Contract·Invariant**를 붙인 것이 RED 테스트의 `# AC-…` 주석과 traceability의 뼈대가 됐다.
- Boundary Story(US-01)와 Domain Story(US-02~05) **분리**가 spy mock·Domain 격리 테스트로 바로 연결됐다.
- “코드·테스트·파일 생성 금지”를 단계마다 반복한 덕분에 **문서만 쌓이는 구간**이 짧고 명확했다.

### Problem

- User Journey(`08`)와 User Story(`09`) 내용이 README·테스트 플랜으로 옮겨갈 때 **일부 AC가 체크리스트에 늦게 반영**됐다.

### Try

- `report/README.md`에 **Phase A(문제)·B(요구)·C(설계)·D(구현)** 타임라인 표를 추가한다.
- Story 확정 시 **AC ID ↔ Invariant ID 매핑 표** 1페이지를 `09` 맨 아래에 고정한다.

### Cursor 기능

| 지금 | 추천 |
|------|------|
| Epic/Journey/Story를 연속 채팅에서 생성 | **단계마다 새 채팅** + `@report/07-…`만 넘기기 — 이전 턴의 “구현해도 됨” 뉘앙스 차단 |
| `@report 에 정리해줘` 반복 | **Composer + 명시적 파일 경로** (`report/09-user-stories-….md`)와 “덮어쓰지 말고 §만 추가” 지시 |
| backup-agent로 report·prompt 동시 생성 | 번호 자동 증가 규칙을 **Skill에 문서화**해 `/backup-agent` 한 번에 1·2단계 완료 (3단계 push는 PAT 이슈 분리) |

</details>

<details>
<summary><strong>5. RED</strong> — 테스트·플랜 (<code>test_plan</code>, README 체크리스트)</summary>

### Keep

- **US-01 샘플 AC를 먼저 고른 뒤** 테스트 플랜·spy 전략·커버리지 목표를 잡은 순서가 Boundary RED의 품질을 높였다.
- Given-When-Then·`test_[조건]_[동작]_[검증]`·`# AC-…` 형식을 일찍 고정해, Green 이후에도 **테스트 이름만으로 요구 추적**이 가능했다.
- “소스 구현 금지, RED만”을 여러 번 강조해 **실패하는 테스트 베이스**가 확보됐다.

### Problem

- README 체크리스트와 실제 `tests/` **동기화가 한 번 어긋나** “체크 안 된 이유”를 따로 물어봐야 했다.
- `ModuleNotFoundError`·import 경로 이슈는 **환경(conftest) 문제**인데, 처음엔 도메인 실패로 느껴질 수 있다.
- RED가 커진 뒤 **한 번에 Green**을 요청하면서, 중간에 “슬라이스별 커밋” 계획이 Green 이후로 밀렸다.

### Try

- README RED 섹션은 **테스트 파일 경로 링크**까지 포함한 체크리스트로 유지하고, 테스트 추가 PR마다 같이 갱신한다.
- Track A( Boundary ) **1 US 완료 = 1 커밋**을 RED 단계에서도 적용한다.

### Cursor 기능

| 지금 | 추천 |
|------|------|
| README 구간을 @하고 “테스트만 작성” | **터미널 출력을 @** (`terminals/4.txt`)해 실패 로그 기반으로 conftest만 수정 요청 — 원인 설명만 원할 때는 “행동하지 말고 이유만” 명시 (잘 쓰임) |
| 커버리지 HTML 방법을 채팅으로 질문 | **터미널에서 `pytest --cov-report=html` 실행은 Agent에게 맡기고**, 결과 경로만 README에 고정 |
| 대량 RED 생성 | **`@report/09` + `@report/05` + “tests/boundary만”**처럼 **glob 범위를 프롬프트에 명시**해 domain 테스트가 섞이지 않게 |

</details>

<details>
<summary><strong>6. GREEN</strong> — 구현 · 매핑 · GUI (<code>10</code>, 154 passed)</summary>

### Keep

- Green 시 **설계 05·Epic 07·Rules 06을 동시에 @**한 덕분에 레이어 침범 없이 구현됐고, 이후 `10-red-green-implementation-mapping.md`로 **RED 슬라이스 ↔ 파일**이 정리됐다.
- Boundary 검증 순서·spy·integration·regression을 **단계적으로 쌓은 테스트 피라미드**가 154 passed의 기반이다.
- PyQt GUI는 **본 학습 목표와 분리**했지만, 실행 방법·커밋 단위 추천을 통해 “동작 확인 채널”을 확보했다.

### Problem

- `tests/fixtures/grids.py`의 **목(mock) 값**이 실제 솔버 출력과 달랐고, 이건 Golden Master 단계까지 **기술 부채**로 남았다 (`VALID_GRID_SUCCESS_RESULT` vs `[2,3,7,4,4,16]`).
- “테스트는 건드리지 말고 구현만” 요청이 **일부 환경·import 이슈**에서는 테스트 쪽 수정(conftest)이 필요해 규칙과 충돌할 수 있다.
- Green 직후 **단위별 커밋**을 나중에 요청해, diff 리뷰 단위가 커졌다.

### Try

- Green 진입 전 **fixture 1개를 먼저 실제 실행**해 기대 `int[6]`를 문서·fixture에 기록한다 (Golden Master를 Green 직후 필수 게이트로).
- 구현 프롬프트에 **“public API 시그니처는 05 고정, private는 자유”**를 한 줄 추가한다.

### Cursor 기능

| 지금 | 추천 |
|------|------|
| “전체 Green” 한 방 요청 | **US별 서브태스크**: Composer에서 `US-02만 Green` → pytest 해당 파일만 — 실패 범위 축소 |
| 커밋을 Agent에게 맡김 | **split-to-prs Skill** 또는 “B-01~B-04만 stage”처럼 **커밋 메시지 템플릿을 프롬프트에 포함** |
| 대화 전체를 prompt로 Export | 세션 종료 시 **`Export transcript`** + report 번호 맞추기 — PR 본문 작성 시 재사용 |

</details>

<details>
<summary><strong>7. Golden Master</strong> (<code>11</code>, 178 passed)</summary>

### Keep

- **Runtime Capture 프롬프트**로 설계 문서·README 예시가 아닌 **실제 호출 결과**를 baseline으로 고정한 것이 Refactor의 안전망이 됐다.
- Domain / Boundary / formatted **3레이어 equality**로 “어디서 깨졌는지” 분리가 쉬웠다.
- `GRID_MISSING_3_7`이 문서상 success였으나 런타임 `UnsolvableGrid`인 점을 **캡처로 정정**한 것이 큰 가치였다.

### Problem

- Golden Master 도입 전까지 **구조(OC) 테스트와 출력 스냅샷**이 혼재해, mock 값 불일치를 늦게 발견했다.
- 골든 마스터에 대한 이해가 제대로 되지 않아, 개념설명과 예시를 cursor에 요청했고 멀티턴으로 이어졌다.

### Try

- RED/Green 단계부터 **“대표 fixture 1개의 expected output”**을 `tests/fixtures/`에 “pending golden” 주석으로 두기.
- baseline 변경 시 **재캡처 스크립트**(report 12 순번 14)를 Phase 5 이전에 최소 버전으로라도 추가한다.

### Cursor 기능

| 지금 | 추천 |
|------|------|
| “어떤 프롬프트가 좋아?” 질문 후 구현 | **첫 턴: 프롬프트 템플릿만**, **둘째 턴: @grids.py @solver @resolver 실행 캡처** — 역할 분리가 잘 맞았음, 다음에도 유지 |
| Golden 후 `/code-reviewer` | **Task subagent `code-reviewer`**로 mock·SSOT·fixture 분산을 병렬 점검 (실제로 불일치 발견) |
| report 11 + prompt export | `@report` + “대화 @prompt로”를 **한 요청에 묶기** — 문서·원문 쌍 유지 |

</details>

<details>
<summary><strong>8. Refactor · CI</strong> (<code>12</code>, Phase 0~5, 209 passed)</summary>

### Keep

- **코드 수정 전 계획서(`12`)**에 우선순위·테스트 선행·회귀 명령·Go/No-Go를 적어 둔 것이 Phase 0(Test First) → 1~4 → 5(coverage·CI) 순서를 지키게 했다.
- Golden Master + contract gate를 **매 Phase마다** 돌린 방식이 “계약 깨짐”을 조기에 막았다.
- `code-reviewer` 지적(ERROR_CATALOG 이중, judge 분기, registry 분산)이 **계획서 항목과 README TODO**로 연결됐다.

### Problem

- Phase 5까지 README·report의 **passed 숫자(178 → 196 → 209)**가 여러 파일에 흩어져 동기화 부담이 있다.
- Refactor 범위가 넓어 **한 세션에 Phase 0~5**를 진행하면서, 중간 커밋 단위는 나중에 “적합한 커밋으로만” 정리했다.

### Try

- CI 워크플로는 **main 머지 직전 브랜치**에서만 추가하거나, push 전 `git diff --name-only`로 workflow 포함 여부 확인.
- Refactor는 **Phase당 브랜치 또는 커밋 1개**를 기본으로.

### Cursor 기능

| 지금 | 추천 |
|------|------|
| “진행해줘”로 Phase 연속 실행 | **Phase N만** + “Golden Master 먼저 실행하고 통과 보고”를 매번 붙이기 |
| 리팩터 계획 → report 저장 → README TODO | **Plan 모드**로 계획만 작성·승인 후 Agent 실행 — 계획 없이 코드부터 가지 않기 |
| babysit Skill 미사용 | PR·CI가 생기면 **`babysit` Skill**로 실패 로그 @하고 수정 루프 — workflow scope 오류는 문서화된 체크리스트로 |
| coverage gate | 터미널에서 `pytest --cov`는 Agent 실행, **Multitask/백그라운드 터미널**로 긴 실행 시 알림 패턴 사용 가능 |

</details>

---

## 전체 KPT (프로젝트 단위)

### Keep

- 관찰 문장으로 시작한 것(`01-observation`)이 이후 Epic·Invariant·Contract와 같은 말투로 이어졌다. “마방진을 만든다”가 아니라 “16칸 배치·합 일치·제시/판별”처럼 **검증 가능한 상황**으로 쓴 게 핵심이었다.
- **`04-open-questions`**로 기획 단계에서 아직 안 정한 것을 분리해 두어, 설계 단계에서 **소통 오류·범위 밀림**을 줄일 수 있었다.

### Problem

- 초반에는 **대화 원문 저장**의 필요성을 크게 느끼지 못해, 기록이 잘 안 됐다. **README와의 연동**도 약했다.
- 후반으로 갈수록 저장된 대화·프롬프트를 참조하는 게 **생각보다 훨씬 도움**이 됐다. 현업에서는 **backup-agent** 같은 방식으로 “단계 끝 = transcript 저장”을 루틴화하는 편이 맞아 보인다.

### Try

- **구현 금지**를 매번 긴 프롬프트로 말하지 않고, `@phase-0-problem-definition.md` 같은 **태그/앵커 파일** 하나를 두고 `@`만으로 단계 제약을 전달한다.
- 단계 종료 시 **Export transcript → `prompt/`** (또는 backup-agent 1·2단계)를 고정 루틴으로 둔다.
- **`plan/`** 폴더를 따로 만들어 README가 지나치게 길어져 대화 시 불필요하게 추가되는 **멀티턴을 줄여** 본다.

---

## Cursor 기능 치트시트 (단계별 한 줄)

실수했던 것들 중 Cursor 기능으로 대체할 수 있는 목록.  
나중에 이 표를 바탕으로 현업에 적용해 볼 예정.

| 단계 | 가장 잘 맞았던 것 | 다음에 쓸 것 |
|------|-------------------|--------------|
| 문제 정의 | 구현 금지 프롬프트 | Plan 모드 + `@report/01` |
| 설계 | 긴 구조화 프롬프트 → `05` | create-rule / Skill로 출력 형식 고정 |
| Rules | `.mdc` 분할 + forbidden | `globs`로 domain/tests만 |
| Epic/Story | 단계별 “파일 생성만” | 채팅 분리 + Composer 경로 명시 |
| RED | README 체크리스트 드리븐 | 터미널 @ + 범위 제한 프롬프트 |
| GREEN | 다중 @ 설계 문서 | US 단위 Green + 조기 fixture 실행 |
| Golden Master | Runtime Capture 2턴 | code-reviewer subagent 필수 |
| Refactor | 계획서 선행 + Phase 게이트 | Plan 승인 → Phase별 Agent + babysit |

---

## 참고 링크

- 보고서 인덱스: [report/README.md](./report/README.md)
- 대화 원문 예시: [prompt/](./prompt/)
- 프로젝트 규칙: [.cursor/rules/](./.cursor/rules/)

---
