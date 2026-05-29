# Magic Square Session Prompt Transcript
_Exported on 5/29/2026 — Full conversation export (no summary)_
_Paired report: report/09-user-stories-magic-square-4x4-report.md_

---

## Session Metadata

| Item | Value |
|------|-------|
| Project | MagicSquare 4x4 TDD Practice |
| Epic | 불변식 기반 사고 훈련 시스템 구축 |
| Export scope | Full User + Assistant turns |
| Related reports | 07 (Epic), 08 (User Journey), 09 (User Stories) |

---

## Turn 1 — Code Review

### User

/code-reviewer 전체 프로젝트 리뷰해줘

### Assistant

전체 프로젝트 리뷰 결과입니다. (버그/리스크/회귀 가능성/테스트 갭 우선)

## Findings

### High
- `src/entity/user.py` — `user_id`에 `bool`이 들어와도 통과될 수 있습니다.
  - `bool`은 Python에서 `int`의 서브클래스라 `True`가 `1`로 취급됩니다.
  - ID 무결성이 깨지면 권한/식별/저장 키에서 미묘한 버그를 유발할 수 있습니다.
  - `isinstance(user_id, int)` + `not isinstance(user_id, bool)` 형태로 타입을 먼저 강제하는 검증이 필요합니다.

- `src/entity/user.py` — `username`/`email`이 문자열이 아닐 때 도메인 검증 에러 대신 우발적 예외가 날 수 있습니다.
  - 예: `None.strip()`로 `AttributeError`, regex에 비문자열 전달 시 `TypeError`.
  - 상위 레이어에서 예외 계약이 흔들려 에러 처리 일관성이 깨집니다.
  - 먼저 문자열 타입 검증 후, `.strip()`/패턴 검증을 수행하고 일관된 `ValueError`(또는 도메인 예외)로 정리하는 게 안전합니다.

### Medium
- `tests/entity/test_user.py` — 입력 불변조건 경계 케이스 테스트가 부족합니다.
  - `user_id`의 `0/음수/bool/비정수`, `username`/`email` 비문자열 케이스가 비어 있습니다.
  - 현재 테스트가 통과해도 검증 회귀를 놓칠 수 있습니다.
  - 파라미터라이즈드 negative test 보강이 필요합니다.

- `tests/conftest.py` — `sys.path` 주입 방식에 의존합니다.
  - 로컬에선 통과해도 패키징/CI 환경의 import 문제를 가릴 수 있습니다.
  - 가능하면 프로젝트 설정(패키지 설치/pytest 설정) 기반으로 import 경로를 정리하는 편이 안정적입니다.

### Low
- `README.md` — “구현/테스트 미시작” 상태 설명과 실제 코드 상태가 불일치합니다.
  - 온보딩/리뷰 시 잘못된 전제를 만들 수 있습니다.

## Open Questions / Assumptions
- `User` 엔티티는 런타임 방어적 검증을 수행해야 한다는 전제로 리뷰했습니다.
- `user_id`는 `bool` 제외한 “엄격한 양의 정수”가 의도라고 가정했습니다.
- 예외 타입/메시지 일관성이 상위 계층 계약에 중요하다고 가정했습니다.

## Test Gaps (추가 권장)
- `user_id`: `0`, `-1`, `True/False`, `"1"`, `1.0`, `None` 실패 케이스
- `username`/`email`: `None`, 숫자 등 비문자열 실패 케이스
- 이메일 포맷 경계값(로컬/도메인/TLD 누락, 공백 포함 등) 회귀 세트

원하면 다음으로, 이 리뷰 기반으로 **Red → Green → Refactor** 순서로 실제 수정 + 테스트 추가까지 바로 진행하겠습니다.

---

## Turn 2 — Backup Agent 생성

### User

보고서 작성 및 기록, 깃 허브를 관리하는 백업Agent를 만들어줘.
.cursor/agent 에 생성
보고서 작성 및 백업 명령을 받으면
[1] 작업한 내용에 대한 보고서 작성 : Report 폴더에 xx(숫자 01부터 시작).적절한 보고서 이름_Report.md 파일로 작성
[2] 작업한 모든 대화내용 저장 : Prompting 폴더에 xx(report 숫자와 동일).적절한 보고서 이름_Prompt.md
[3] 깃허브에 모든 작업내용 올리기. <- 이 부분은 이슈가 있습니다.
이상 3단계의 명령을 루틴하게 수행하는 Agent야.
백업 Agent가 prompt를 백업할 때 요약하지 않고 내 Prompt와 AI답변 전체를 Export하도록 변경해줘.

### Assistant

요청한 백업 Agent를 생성했습니다.

- 생성 파일: `.cursor/agent/backup-agent.md`
- 동작 루틴:
  1. `Report` 폴더에 `xx.보고서명_Report.md` 생성 (`01`부터 자동 증가)
  2. `Prompting` 폴더에 `xx.보고서명_Prompt.md` 생성 (동일 번호)
  3. GitHub 업로드 시도 + 실패 시 원인/재시도 방법 보고
- 핵심 반영사항: **Prompt 백업 시 요약 금지**, 사용자 Prompt와 AI 답변을 **전체 원문 그대로 Export**하도록 명시

추가로, 현재 프로젝트에 기존 에이전트는 `.cursor/agents` 경로에도 존재합니다.
원하면 동일 내용을 `.cursor/agents/backup-agent.md`로도 복제해서 Cursor 에이전트 목록에서 바로 인식되게 맞춰드릴게요.

---

## Turn 3 — Backup Agent 실행

### User

/backup-agent

### Assistant

`backup-agent` 루틴 실행을 시작했습니다.
완료되는 즉시 생성된 `Report`/`Prompting` 파일 경로와 GitHub 업로드 결과(성공/실패 및 후속 조치)를 바로 공유하겠습니다.

---

## Turn 4 — Skill vs Rule

### User

스킬과 룰의 차이는 뭐야?

### Assistant

좋은 질문입니다. 핵심은 **적용 방식과 목적**이 다릅니다.

- **룰(Rule)**: 에이전트가 작업할 때 **항상 지켜야 하는 제약/기준**
  - 예: 아키텍처 원칙, 코딩 금지사항, TDD 절차
  - 성격: 정책, 가드레일, 품질 기준
  - 효과: “무엇을 하면 안 되는지 / 반드시 지켜야 하는지”를 강제

- **스킬(Skill)**: 특정 작업을 잘 처리하기 위한 **재사용 가능한 실행 가이드/플레이북**
  - 예: PR 분할, Cursor 설정 변경, 훅 만들기 같은 전문 절차
  - 성격: 작업 방법론, 절차 템플릿
  - 효과: “이 작업을 어떻게 효율적으로 수행할지”를 제공

한 줄로 정리하면:
- **룰 = 행동 제약(정책)**
- **스킬 = 실행 레시피(방법)**

원하면 지금 프로젝트 기준으로 “항상 적용되는 룰”과 “자주 쓸 만한 스킬”을 1분 요약으로 뽑아드릴게요.

---

## Turn 5 — MCP JSON 설정

### User

mcp json 파일 설정하려면 어떻게 해야해?

### Assistant

`mcp.json` 설정은 이렇게 하면 됩니다.

- **프로젝트용(공유)**: `.cursor/mcp.json`
- **개인 전역용**: `C:\Users\<사용자명>\.cursor\mcp.json`
- 둘 다 있으면 병합되고, **같은 서버 이름이면 프로젝트 파일이 우선**됩니다.

```json
{
  "mcpServers": {
    "local-python-mcp": {
      "type": "stdio",
      "command": "python",
      "args": ["${workspaceFolder}/tools/mcp_server.py"],
      "env": {
        "API_KEY": "${env:API_KEY}",
        "MODE": "dev"
      }
    }
  }
}
```

적용/확인:

- 파일 저장 후 **Cursor 재시작**(또는 리로드)
- `Ctrl+Shift+J` → **Tools & MCP**에서 서버 상태 확인
- `Ctrl+Shift+U` → Output → **MCP Logs**에서 에러 확인

Windows에서 자주 막히는 포인트:

- `command`를 못 찾으면 절대경로로 지정
  - 예: `"command": "C:\\Python313\\python.exe"`
- JSON 문법 오류(쉼표/따옴표)
- env 값 미인식(앱 재시작 필요)
- 서버 이름 충돌(전역/프로젝트 동일 이름)

원하면 지금 프로젝트(`c:\dev\MagicSquare`) 기준으로 바로 쓸 수 있는 `mcp.json`을 내가 맞춤으로 작성해줄게요.

---

## Turn 6 — Gherkin 스타일

### User

걸킨 스타일 시나리오가 뭐야?

### Assistant

아마 **“거킨(Gherkin) 스타일 시나리오”**를 말한 것 같아요.

- **정의**: 사람이 읽기 쉬운 자연어 형식으로 요구사항/테스트를 쓰는 방식
- **목적**: 기획자-개발자-QA가 같은 문서로 동작을 합의
- **핵심 구조**: `Given(주어진 상태) - When(행동) - Then(기대 결과)`

예시:

```gherkin
Feature: 로그인

Scenario: 올바른 계정으로 로그인 성공
  Given 사용자가 로그인 페이지에 있다
  When 올바른 아이디와 비밀번호를 입력한다
  Then 대시보드 페이지로 이동한다
```

보통 BDD(Behavior Driven Development)에서 쓰고, `Scenario Outline`으로 데이터 기반 테스트도 쉽게 확장할 수 있어요.

---

## Turn 7 — Git Push SSH 타임아웃

### User

@c:\Users\usejen_id\.cursor\projects\c-dev-MagicSquare\terminals\4.txt:8-14

```
$ git push origin develop
ssh: connect to host github.com port 22: Connection timed out
fatal: Could not read from remote repository.
```

### Assistant

`git push`가 실패한 이유는 **권한 문제가 아니라 SSH(22번 포트) 연결 차단**입니다.

## 원인

- 현재 원격 URL: `git@github.com:dev1week/MagicSquare.git` (SSH)
- 에러: `ssh: connect to host github.com port 22: Connection timed out`
- 회사/방화벽 환경에서 **22번 포트가 막혀 있을 때** 흔히 발생합니다.
- HTTPS(`https://github.com`)는 정상(200)이라, **GitHub 접속 자체는 되지만 SSH만 막힌 상태**로 보입니다.

## 해결 방법 (추천 순)

### 1) HTTPS로 원격 URL 변경 (가장 간단)

```bash
git remote set-url origin https://github.com/dev1week/MagicSquare.git
git push origin develop
```

### 2) SSH를 443 포트로 우회 (SSH 유지하고 싶을 때)

`~/.ssh/config` (Windows: `C:\Users\usejen_id\.ssh\config`)에 추가:

```sshconfig
Host github.com
  HostName ssh.github.com
  Port 443
  User git
```

원하면 제가 바로 **원격 URL을 HTTPS로 바꾸고 push 재시도**까지 진행해드릴게요.

---

## Turn 8 — Git Push / 저장소 이동

### User

@c:\Users\usejen_id\.cursor\projects\c-dev-MagicSquare\terminals\4.txt:24-49

```
$ git push origin develop
Enumerating objects: 11, done.
...
remote: This repository moved. Please use the new location:
remote:   https://github.com/dev1week/MagicSquare_09.git
 * [new branch]      develop -> develop

$ git checkout -B main
Switched to and reset branch 'main'

$ git push origin main
fatal: unable to access 'https://github.com/dev1week/MagicSquare.git/': Failed to connect to github.com port 443 after 21130 ms: Could not connect to server
```

뭐가 문제야?

### Assistant

문제는 **두 가지**입니다.

## 1) 저장소 주소가 옛날 URL (중요)

`develop` push는 성공했지만, GitHub가 이렇게 알려줬습니다:

```text
This repository moved. Please use the new location:
  https://github.com/dev1week/MagicSquare_09.git
```

## 2) 네트워크 일시 장애 (443 포트)

`main` push 실패: `Failed to connect to github.com port 443`

## 지금 할 일

```bash
git remote set-url origin https://github.com/dev1week/MagicSquare_09.git
git remote -v
git push -u origin main
```

---

## Turn 9 — 커밋 취소 명령어

### User

커밋 취소 명령어 알려줘

### Assistant

커밋을 “취소”하는 방법은 **상황에 따라** 다릅니다.

## 1) 마지막 커밋만 취소, 변경사항은 유지 (가장 많이 씀)
```bash
git reset --soft HEAD~1
```

## 2) 마지막 커밋 취소, 변경사항은 작업 폴더에만 남김
```bash
git reset HEAD~1
```

## 3) 마지막 커밋 + 변경사항까지 전부 버림 (주의)
```bash
git reset --hard HEAD~1
```

## 4) 이미 push한 커밋을 되돌릴 때 (안전)
```bash
git revert HEAD
```

---

## Turn 10 — develop 커밋 취소

### User

developer, 푸시 안함

### Assistant

`develop` 브랜치에서 **아직 push 안 했다면** 이렇게 하면 됩니다.

## 커밋만 취소, 변경 내용은 유지 (추천)
```bash
git checkout develop
git reset --soft HEAD~1
```

## 커밋 취소 + 스테이징도 해제
```bash
git checkout develop
git reset HEAD~1
```

## 커밋 + 변경 내용까지 전부 버림 (주의)
```bash
git checkout develop
git reset --hard HEAD~1
```

보통은 첫 번째(`--soft`)를 씁니다.

---

## Turn 11 — Level 1 Epic 작성

### User

Magic Square 프로젝트의 User Journey를 다음 구조로 만들고 싶습니다.

Epic → User Story → Task

지금은 Level 1: Epic, 즉 Business Goal만 작성합니다.

중요:
- 구현 코드를 작성하지 마십시오.
- 테스트 코드를 작성하지 마십시오.
- 파일을 생성하지 마십시오.
- 아직 User Story나 Task로 세분화하지 마십시오.
- 오직 Epic 수준의 비즈니스 목표와 학습 목표만 정의하십시오.

프로젝트:
Magic Square 4x4 TDD Practice

Epic:
“불변식 기반 사고 훈련 시스템 구축”

목적:
4x4 Magic Square 문제를 사용하여 다음을 훈련합니다.

- 불변식 중심 설계 사고
- Dual-Track UI + Logic TDD 적용
- 입력/출력 계약 명확화
- 설계 → 테스트 → 구현 → 리팩토링 흐름
- Concept → Invariant → Contract → Test 추적성

성공 기준:
- Domain Logic 테스트 커버리지 95% 이상
- Boundary 입력 검증 계약 테스트 100% 통과
- 설명 없는 매직 넘버 금지
- GRID_SIZE, MAX_VALUE, MAGIC_CONSTANT 같은 명명된 상수 사용
- 정답 하드코딩 금지
- 주요 Invariant는 최소 하나 이상의 테스트와 추적 가능해야 함
- 리팩토링 후에도 외부 입력/출력 계약은 변경되지 않아야 함

출력 형식:

# Level 1: Epic — Business Goal

## 1. Epic Title
## 2. Business Goal
## 3. Learning Goal
## 4. Problem Statement
## 5. Target Learners / Users
## 6. Scope
## 7. Non-Scope
## 8. Success Criteria
## 9. Key Invariants
## 10. Traceability Rule
## 11. Candidate User Stories for Level 2

주의:
- Epic 수준에서만 작성하십시오.
- 아직 세부 Task로 나누지 마십시오.
- 코드나 테스트 코드는 작성하지 마십시오.
- 다음 단계인 Level 2 User Story를 도출할 수 있도록 정리하십시오.

### Assistant

(Cursor 응답 전문)

# Level 1: Epic — Business Goal

## 1. Epic Title

**불변식 기반 사고 훈련 시스템 구축**

4x4 Magic Square 문제를 매개로, 도메인 불변식(Invariant)을 중심에 두고 Dual-Track UI + Logic TDD 방식으로 설계·검증·구현 역량을 체계적으로 훈련하는 학습 시스템을 구축한다.

---

## 2. Business Goal

Magic Square 4x4 문제를 **단순 퍼즐 풀이 도구**가 아니라 **설계·테스트·구현 역량을 동시에 훈련하는 교육용 시스템**으로 정의한다.

이 Epic의 비즈니스 목표는 다음과 같다.

- 학습자가 "기능 구현"보다 먼저 **도메인 불변식을 식별하고 설계에 반영**하는 습관을 갖도록 한다.
- UI 흐름과 도메인 로직을 분리하는 **Dual-Track 접근**으로, 사용자 경험과 비즈니스 규칙을 각각 독립적으로 검증할 수 있게 한다.
- 입력/출력 계약(Contract)을 명확히 정의하여, **경계(Boundary)에서의 검증 실패를 조기에 발견**할 수 있게 한다.
- 설계 → 테스트 → 구현 → 리팩토링의 TDD 사이클을 반복 가능한 **학습 루틴**으로 고정한다.
- Concept → Invariant → Contract → Test 간 **추적성(Traceability)** 을 확보하여, "왜 이 테스트가 존재하는가"를 항상 설명할 수 있게 한다.

궁극적으로, Magic Square 프로젝트는 **정답을 맞히는 결과**보다 **불변식 중심으로 올바르게 설계하고 검증하는 과정**을 성공으로 정의한다.

---

## 3. Learning Goal

이 Epic을 완료한 학습자는 다음 역량을 갖춘다.

| 영역 | 학습 목표 |
|------|-----------|
| **불변식 사고** | 4x4 Magic Square의 핵심 규칙을 Invariant로 명문화하고, 설계·테스트·코드에 일관되게 반영할 수 있다. |
| **Dual-Track TDD** | UI Track과 Logic Track을 분리하여, 각각에 맞는 테스트 전략을 선택하고 적용할 수 있다. |
| **계약 설계** | Boundary의 입력/출력 계약을 정의하고, 유효·무효 입력에 대한 검증 책임을 명확히 구분할 수 있다. |
| **TDD 사이클** | Red → Green → Refactor 흐름을 의도적으로 수행하며, 리팩토링 후에도 외부 계약이 유지됨을 확인할 수 있다. |
| **추적성** | Concept, Invariant, Contract, Test 간 연결 관계를 문서·테스트·코드에서 추적할 수 있다. |
| **도메인 표현** | 매직 넘버를 배제하고 `GRID_SIZE`, `MAX_VALUE`, `MAGIC_CONSTANT` 등 **의미 있는 상수**로 도메인을 표현할 수 있다. |

---

## 4. Problem Statement

4x4 Magic Square는 겉보기에는 단순한 숫자 배치 문제이지만, 실제 소프트웨어 설계 관점에서는 다음과 같은 복합 문제다.

- **도메인 규칙**이 명확하지 않으면 구현이 ad-hoc(임시방편)으로 흐르기 쉽다.
- **입력 검증**과 **핵심 로직**이 섞이면 테스트가 brittle(취약)해지고 리팩토링이 어려워진다.
- UI와 Logic을 동시에 개발하면 **어디서 실패했는지** 원인 분리가 어렵다.
- "정답을 맞힌다"는 목표만 두면 **설계 품질·테스트 품질·유지보수성**이 학습 범위에서 빠진다.

따라서 이 프로젝트는 Magic Square를 **도메인 불변식 훈련용 사례(Case Study)** 로 사용하여, 작지만 완결된 설계·테스트·구현 사이클을 경험하게 한다.

**핵심 문제 정의:**

> 4x4 Magic Square를 해결하는 시스템을 만들되, 정답 산출 자체보다 **불변식 기반 설계와 Dual-Track TDD를 통해 검증 가능한 소프트웨어를 만드는 능력**을 훈련한다.

---

## 5. Target Learners / Users

### Primary: 학습자 (Developer Trainee)

- TDD, Clean Architecture, ECB(Entity–Control–Boundary) 개념을 **실습 중심**으로 익히려는 개발자
- "코드는 짰는데 왜 테스트가 깨지는지", "리팩토링이 무서운지"를 경험한 초·중급 개발자
- Magic Square를 통해 **작은 도메인에서 설계 원칙을 반복 훈련**하려는 학습자

### Secondary: 리뷰어 / 멘토

- 학습자의 Concept → Invariant → Contract → Test 추적성을 검토하는 코드 리뷰어
- Domain Logic 커버리지, Boundary 계약 테스트, 불변식-테스트 매핑을 기준으로 피드백하는 교육 담당자

### Tertiary: 프로젝트 운영자

- Magic Square TDD Practice 커리큘럼을 운영·확장하는 관리자
- Epic → User Story → Task 구조로 학습 진행도를 관리하는 역할

---

## 6. Scope

Epic 수준에서 포함하는 범위는 **"불변식 기반 사고 훈련 시스템"을 정의하고, 그 성공 기준과 추적 규칙을 확립**하는 것이다.

### 포함

- 4x4 Magic Square 도메인에 대한 **비즈니스 목표·학습 목표** 정의
- Dual-Track(UI + Logic) TDD 적용 원칙 수립
- Boundary 입력/출력 **계약(Contract)** 정의 원칙
- Domain Logic과 Boundary 검증의 **책임 분리** 원칙
- Concept → Invariant → Contract → Test **추적성 규칙** 정의
- 성공 기준(커버리지, 계약 테스트, 상수 명명, 하드코딩 금지, 리팩토링 후 계약 유지) 확립
- Level 2 User Story 도출을 위한 **후보 영역** 식별

### 도메인 맥락 (Epic에서 전제하는 Magic Square 규칙)

- 격자 크기: 4×4 (`GRID_SIZE = 4`)
- 사용 숫자: 1부터 16까지 각각 한 번 (`MAX_VALUE = 16`)
- 모든 행, 열, 대각선의 합이 동일 (`MAGIC_CONSTANT = 34`)
- 위 규칙은 **Invariant**로 취급하며, Level 2 이후 User Story·Task로 세분화한다.

---

## 7. Non-Scope

Epic 단계에서는 다음을 **의도적으로 포함하지 않는다**.

| 제외 항목 | 사유 |
|-----------|------|
| 구체적 User Story 작성 | Level 2에서 수행 |
| Task 단위 작업 분해 | Level 3에서 수행 |
| 구현 코드 작성 | Epic은 목표·원칙 정의만 |
| 테스트 코드 작성 | Epic은 성공 기준·추적 규칙만 |
| UI 상세 화면 설계 | Dual-Track 원칙만 정의, 상세는 User Story |
| 4×4 이외 Magic Square 일반화 (3×3, n×n) | 학습 범위 집중 |
| 성능 최적화, 병렬 처리, 캐싱 | 교육 목적 범위 밖 |
| 인증/권한, 다중 사용자, 영속 저장소 | 도메인 훈련과 무관 |
| 정답 하드코딩 또는 lookup table 방식 | 학습 목표(불변식 기반 설계)와 상충 |
| 배포·CI/CD 파이프라인 구축 | Epic 범위 밖 (후속 Epic 가능) |

---

## 8. Success Criteria

Epic "불변식 기반 사고 훈련 시스템 구축"의 완료는 **기능 완성**이 아니라 **훈련 시스템의 검증 가능한 품질 기준 충족**으로 판단한다.

### 8.1 품질 기준

| # | 기준 | 측정 방법 |
|---|------|-----------|
| SC-1 | Domain Logic 테스트 커버리지 **95% 이상** | Logic Track 단위 테스트 커버리지 리포트 |
| SC-2 | Boundary 입력 검증 계약 테스트 **100% 통과** | Contract Test Suite 전체 Green |
| SC-3 | 설명 없는 매직 넘버 **금지** | 코드 리뷰 + 정적 점검 |
| SC-4 | `GRID_SIZE`, `MAX_VALUE`, `MAGIC_CONSTANT` 등 **명명된 상수** 사용 | 도메인 상수 정의 및 참조 확인 |
| SC-5 | 정답 **하드코딩 금지** | 구현이 Invariant 기반 알고리즘/규칙으로 도출되는지 검증 |
| SC-6 | 주요 Invariant마다 **최소 1개 이상의 테스트** 존재 | Invariant ↔ Test 매핑표 |
| SC-7 | 리팩토링 후 **외부 입력/출력 계약 불변** | Contract Test 회귀 Green |

### 8.2 프로세스 기준

| # | 기준 | 확인 방법 |
|---|------|-----------|
| SC-8 | Dual-Track(UI + Logic) TDD 사이클 준수 | Red → Green → Refactor 이력 |
| SC-9 | Concept → Invariant → Contract → Test 추적성 확보 | 추적 매트릭스 작성 |
| SC-10 | ECB 책임 분리 준수 | Entity에 I/O·프레임워크 의존 없음 |

### 8.3 Epic 완료 판정

다음이 모두 충족되면 Epic Level 1을 완료한 것으로 본다.

- [ ] Business Goal과 Learning Goal가 팀/학습자에게 공유·합의됨
- [ ] Scope / Non-Scope 경계가 명확함
- [ ] Success Criteria가 측정 가능함
- [ ] Key Invariant 목록이 정의됨
- [ ] Traceability Rule이 확립됨
- [ ] Level 2 User Story 후보가 식별됨

---

## 9. Key Invariants

Epic 수준에서 식별하는 **핵심 불변식**. Level 2 User Story에서 각 Invariant를 검증·구현 책임으로 분배한다.

### INV-1: Grid Dimension Invariant

> Magic Square 격자는 항상 4×4이다.

- 상수: `GRID_SIZE = 4`
- 의미: 입력·출력·내부 표현 모두 4×4 구조를 전제로 한다.

### INV-2: Value Range & Uniqueness Invariant

> 격자 각 칸의 값은 1 이상 16 이하의 정수이며, 1~16은 정확히 한 번씩만 등장한다.

- 상수: `MAX_VALUE = 16`
- 의미: 중복·누락·범위 초과는 유효한 Magic Square가 아니다.

### INV-3: Magic Sum Invariant

> 모든 행, 모든 열, 두 대각선의 합은 동일하다.

- 상수: `MAGIC_CONSTANT = 34`
- 의미: Magic Square의 본질적 규칙. 개별 합 검증과 전체 일치 검증으로 분해 가능.

### INV-4: Input Validity Invariant (Boundary)

> Boundary에 들어오는 모든 외부 입력은 계약(Contract)에 정의된 형식·범위·타입을 만족해야 하며, 위반 시 도메인 로직으로 전달되지 않는다.

- 의미: Boundary가 "문지기" 역할. Entity/Control은 유효 입력만 처리한다.

### INV-5: Contract Stability Invariant

> 리팩토링은 내부 구현만 변경할 수 있으며, Boundary의 외부 입력/출력 계약은 변경되지 않는다.

- 의미: TDD Refactor 단계의 안전망. Contract Test가 회귀 방지 역할.

### INV-6: Traceability Invariant

> 모든 주요 Invariant는 Concept에서 출발하여, Contract와 Test에 추적 가능해야 한다.

- 의미: "왜 이 테스트가 있는가"에 항상 답할 수 있어야 한다.

---

## 10. Traceability Rule

Epic 수준에서 확립하는 **추적성 규칙**. Level 2 User Story 작성 시 각 Story가 이 규칙을 따르도록 한다.

### 10.1 추적 체인

```
Concept → Invariant → Contract → Test → Implementation
```

| 단계 | 정의 | 산출물 예시 |
|------|------|-------------|
| **Concept** | 비즈니스/도메인 개념 | "4×4 격자에 1~16을 배치한다" |
| **Invariant** | 항상 참이어야 하는 규칙 | INV-1 ~ INV-6 |
| **Contract** | Boundary 입·출력 명세 | 입력 형식, 오류 응답, 성공 응답 |
| **Test** | Invariant/Contract 검증 | 단위 테스트, 계약 테스트 |
| **Implementation** | 테스트를 통과하는 코드 | Entity, Control, Boundary |

### 10.2 추적성 매트릭스 (Epic 템플릿)

| Concept ID | Invariant ID | Contract ID | Test ID | 비고 |
|------------|--------------|-------------|---------|------|
| C-01 | INV-1 | BC-01 | T-01 | Grid 4×4 |
| C-02 | INV-2 | BC-02 | T-02 | Value 1~16 unique |
| C-03 | INV-3 | BC-03 | T-03 | Sum = 34 |
| C-04 | INV-4 | BC-04 | T-04 | Boundary validation |
| C-05 | INV-5 | BC-05 | T-05 | Contract regression |
| C-06 | INV-6 | — | — | Meta-rule |

> Test ID, Contract ID는 Level 2 User Story 작성 시 구체화한다.

### 10.3 Dual-Track 추적 규칙

| Track | 책임 | 추적 대상 |
|-------|------|-----------|
| **Logic Track** | Domain Invariant 검증 | INV-1, INV-2, INV-3 |
| **UI Track** | 사용자 흐름·표현 | 입력 수집, 결과 표시, 오류 피드백 |
| **Boundary Track** | Contract 검증 | INV-4, INV-5 |

Logic Track과 Boundary Track은 **독립적으로 테스트**하되, Contract를 통해 연결한다.

### 10.4 금지 규칙

- Invariant 없이 Test를 작성하지 않는다.
- Contract 없이 Boundary 검증 Test를 작성하지 않는다.
- Test 없이 Invariant를 "완료"로 표시하지 않는다.
- Concept → Implementation 직행(중간 단계 생략)을 허용하지 않는다.

---

## 11. Candidate User Stories for Level 2

Epic을 User Story로 세분화할 때 참고할 **후보 영역**이다.  
아직 Story 문장·AC·Task는 작성하지 않는다.

| # | 후보 영역 | 관련 Invariant | Track | Level 2에서 다룰 내용 (예고) |
|---|-----------|----------------|-------|------------------------------|
| US-CAND-01 | **격자 구조 정의** | INV-1 | Logic | 4×4 Grid 표현, `GRID_SIZE` 상수 |
| US-CAND-02 | **값 범위·유일성 검증** | INV-2 | Logic | 1~16 중복/누락/범위 검증 |
| US-CAND-03 | **매직 합 검증** | INV-3 | Logic | 행·열·대각선 합 = `MAGIC_CONSTANT` |
| US-CAND-04 | **Magic Square 유효성 판정** | INV-1,2,3 | Logic | 전체 Invariant 통합 판정 |
| US-CAND-05 | **Magic Square 생성/완성** | INV-1,2,3 | Logic | Invariant를 만족하는 배치 도출 (하드코딩 금지) |
| US-CAND-06 | **Boundary 입력 계약 정의** | INV-4 | Boundary | 입력 형식·타입·범위 Contract |
| US-CAND-07 | **Boundary 오류 응답 계약** | INV-4 | Boundary | 무효 입력 시 일관된 오류 Contract |
| US-CAND-08 | **Contract 회귀 테스트** | INV-5 | Boundary | 리팩토링 후 Contract 불변 검증 |
| US-CAND-09 | **사용자 입력 UI 흐름** | INV-4 | UI | 입력 수집·피드백·재시도 |
| US-CAND-10 | **결과 표시 UI** | INV-3 | UI | Magic Square 결과 시각화 |
| US-CAND-11 | **추적성 매트릭스 관리** | INV-6 | Process | Concept-Invariant-Test 매핑 유지 |
| US-CAND-12 | **TDD 사이클 실습 루틴** | INV-5,6 | Process | Red→Green→Refactor 학습 가이드 |

---

**Epic Level 1 완료.**  
다음 단계(Level 2)에서는 위 Candidate User Stories를 **"As a … I want … So that …"** 형식의 User Story로 구체화하고, Acceptance Criteria와 Invariant 매핑을 추가한다.


---

## Turn 12 — Epic report 저장

### User

이 내용 @report 에 정리해줘

### Assistant

Epic 내용을 `report` 폴더에 정리했습니다.

- **파일**: `report/07-epic-invariant-based-thinking-system-report.md`
- **내용**: Level 1 Epic — Business Goal 전체 (11개 섹션)

---

## Turn 13 — Level 2 User Journey 작성

### User

Magic Square 프로젝트의 User Journey를 다음 구조로 작성해 주세요.

현재 단계:
Level 2: User Journey

상위 Epic:
“불변식 기반 사고 훈련 시스템 구축”

중요:
- 구현 코드를 작성하지 마십시오.
- 테스트 코드를 작성하지 마십시오.
- 파일을 생성하지 마십시오.
- 아직 Task 수준으로 세분화하지 마십시오.
- 오직 User Journey 수준에서 작성하십시오.
- 이 User Journey는 다음 단계인 User Story와 Task로 분해될 수 있어야 합니다.

프로젝트:
Magic Square 4x4 TDD Practice

Persona:
- TDD를 학습 중인 소프트웨어 개발 학습자
- Clean Architecture의 계층 분리를 이해하려는 학습자
- 알고리즘 정답보다 설계, 계약, 테스트, 리팩토링 흐름을 훈련하려는 학습자

Journey Goal:
- 4x4 Magic Square 문제를 통해 불변식 중심 사고를 훈련한다.
- 입력/출력 계약을 먼저 정의한다.
- Domain Logic과 UI/Boundary 책임을 분리한다.
- Dual-Track UI + Logic TDD 흐름을 경험한다.
- 설계 → 테스트 → 구현 → 리팩토링 → 회귀 보호 흐름을 학습한다.

MagicSquare 기본 규칙:
- 입력은 4x4 int 행렬이다.
- 0은 빈칸을 의미한다.
- 빈칸은 정확히 2개여야 한다.
- 값의 범위는 0 또는 1~16이다.
- 0을 제외한 숫자는 중복될 수 없다.
- 출력은 int[6]이다.
- 좌표는 1-index 기준이다.
- 출력 형식은 [r1, c1, n1, r2, c2, n2]이다.
- 4x4 마방진 상수는 34이다.
- 먼저 작은 누락 숫자를 첫 번째 빈칸에, 큰 누락 숫자를 두 번째 빈칸에 넣어 시도한다.
- 실패하면 반대 조합을 시도한다.

User Journey는 다음 5단계로 작성하십시오:
Stage 1: Problem Recognition
Stage 2: Contract Definition
Stage 3: Domain Separation
Stage 4: Dual-Track TDD Progress
Stage 5: Regression Protection

출력 형식:
# Level 2: User Journey — Magic Square 4x4
## 1. Persona
## 2. Journey Goal
## 3. Journey Overview
## 4. Detailed Journey
## 5. Journey to User Story Mapping
## 6. Traceability Link

### Assistant

(Cursor 응답 전문)

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


---

## Turn 14 — User Journey report 저장

### User

@report 여기에 정리해줘

### Assistant

Level 2 User Journey 내용을 `report` 폴더에 정리했습니다.

- **파일**: `report/08-user-journey-magic-square-4x4-report.md`

---

## Turn 15 — Level 3 User Stories 작성

### User

Level 3: Magic Square 프로젝트의 User Stories를 작성해 주세요.

맥락:
이 작업은 다음 흐름의 일부입니다.
Epic → User Journey → User Story → Task

상위 Epic:
“불변식 기반 사고 훈련 시스템 구축”

상위 User Journey:
학습자는 문제를 인식하고, 입력/출력 계약을 정의하고, 도메인 책임을 분리하고,
Dual-Track UI + Logic TDD를 적용하며, 회귀 테스트로 품질을 보호합니다.

중요:
- 구현 코드를 작성하지 마십시오.
- 테스트 코드를 작성하지 마십시오.
- 파일을 생성하지 마십시오.
- 아직 Task 수준으로 세분화하지 마십시오.
- 오직 User Story와 Acceptance Criteria만 작성하십시오.
- 모든 Acceptance Criteria는 테스트 가능한 문장으로 작성하십시오.
- Boundary Story와 Domain Story를 분리하십시오.
- 각 Story마다 보호하는 Contract 또는 Invariant를 명시하십시오.

프로젝트:
Magic Square 4x4 TDD Practice

도메인 규칙:
- 입력은 4x4 int 행렬입니다.
- 0은 빈칸을 의미합니다.
- 빈칸은 정확히 2개여야 합니다.
- 유효한 값은 0 또는 1부터 16까지입니다.
- 0을 제외한 숫자는 중복될 수 없습니다.
- 4x4 마방진 상수는 34입니다.
- 출력은 int[6]입니다.
- 최종 출력 좌표는 1-index 기준입니다.
- 출력 형식은 [r1, c1, n1, r2, c2, n2]입니다.

Story 1 — 입력 검증 (Boundary)
Story 2 — 빈칸 좌표 탐색 (Domain)
Story 3 — 누락 숫자 탐색 (Domain)
Story 4 — 마방진 검증 (Domain)
Story 5 — 두 가지 조합 시도 (Domain + Control)

출력 형식:
# Level 3: User Stories — Magic Square 4x4
## Story Overview
## Story 1~5 (Layer, User Story, Acceptance Criteria, Protected Contract/Invariant, Future RED Test Direction)
## Traceability Matrix

### Assistant

(Cursor 응답 전문)

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


---

## Turn 16 — User Stories report 저장

### User

@report 에 정리해줘

### Assistant

Level 3 User Stories 내용을 `report` 폴더에 정리했습니다.

- **파일**: `report/09-user-stories-magic-square-4x4-report.md`

---

## Turn 17 — Prompt 대화 백업

### User

@prompt 대화 내용 여기에 정리해줘

### Assistant

전체 대화 원문을 `prompt/09-user-stories-magic-square-4x4-report_Prompt.md`에 Export했습니다.
요약 없이 User/Assistant 턴 순서대로 기록했으며, Epic/Journey/User Stories Cursor 응답 전문을 포함합니다.
