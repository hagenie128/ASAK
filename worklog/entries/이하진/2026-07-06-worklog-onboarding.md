# 2026-07-06 워크로그·온보딩·디자인 시스템 운영 정리

> 일일: [2026-07-06](../../daily/이하진/2026-07-06.md)

## 1. 기본 정보

- 작업 날짜: 2026-07-06
- 담당자: 이하진
- 저장소: ASAK / ASAK-Kiosk
- 브랜치: `main`
- 근거 커밋: `42f6bd2`(개인 daily/entries 전환), `195c02e`(개인 entries와 `init_entry`), `06383e8`(DS-01~07·온보딩·디자인 문서), `3b4b831`·`b660896`(Windows/MCP/팀 문서)
- 작업 유형: `docs` / `worklog` / `onboarding`

## 2. 작업 목적

- 팀원이 Windows 환경에서 프로젝트를 시작하고, 작업을 daily와 상세 entry로 같은 방식으로 남기며, Figma 디자인 시스템 문서를 같은 기준으로 찾도록 한다.

## 3. 직접 구현 영역

- `worklog/daily/{이름}`과 `worklog/entries/{이름}`로 개인별 경로를 분리하고, 팀 요약용 daily와 12섹션 상세 entry의 역할을 정리했다.
- `init_entry.py`, `worklog_paths.py`와 템플릿을 추가·조정해 새 상세 기록을 같은 경로·형식으로 만들 수 있게 했다.
- 캘린더 데이터와 daily 동기화 스크립트가 개인별 경로를 읽도록 보완했다.
- Windows 설치/온보딩, MCP 설정 예시, Git setup, Figma 디자인 시스템 플러그인·DS-01~07 후보 문서, 팀 회의·시작 가이드를 정리했다.

## 4. 구현 로직 / 적용한 방식

- daily는 Notion 캘린더와 팀 공유를 위한 한 줄 요약·미니 카드, entries는 기능/이슈 단위의 목적·구현·AI·이슈·검증을 남기는 정본으로 분리했다.
- 경로를 사람 이름 기준으로 고정하고 `team_config.json`/Git 사용자 매핑을 통해 명시적 person 입력을 줄이는 방향을 택했다.
- 온보딩은 도구 설치만 나열하지 않고 Windows, Git, MCP, Figma 디자인 자료, 팀 문서를 어느 순서로 볼지 연결했다.

## 5. AI 도움 영역

- 사용한 AI: 과거 커밋·가이드·템플릿 간 경로 일치 여부를 확인하는 보조.
- 사람이 수행한 부분: 개인별 기록 구조, Notion 캘린더에 올릴 정보량, 팀 onboarding 문서의 실제 운영 기준 결정.
- 그대로 사용한 원칙: daily는 요약, entry는 재현 가능한 상세 기록이라는 분리.

## 6. 발생 이슈

### 이슈 1 — 기록 경로와 형식의 분산

- 증상: 팀원이 누구의 기록인지, 일일 요약과 상세 근거가 어디인지 빠르게 찾기 어려웠다.
- 원인: 공용 daily 경로와 개인 상세 기록의 기준이 섞여 있었다.
- 대응: 개인별 `daily/`·`entries/` 경로와 템플릿, 생성 스크립트를 같은 규칙으로 맞췄다.

### 이슈 2 — 도구 설정의 환경 의존성

- 증상: Windows 경로, Git 초기 설정, MCP/Figma 도구의 사전 조건이 문서마다 흩어져 있었다.
- 대응: `INSTALL_WINDOWS.md`, `MCP_SETUP.md`, setup 스크립트·예시 설정, 시작 문서를 연결했다.

## 7. 디버깅 기록

- 확인한 근거: worklog README·guide·템플릿·calendar/data·sync 스크립트가 개인 경로로 함께 변경된 커밋을 대조했다.
- 확인하지 못한 범위: 모든 팀원의 로컬 환경에서 init/sync/Notion 업로드가 성공했는지, Figma 플러그인이 실제 파일에서 동작했는지는 이 문서의 증거만으로 확인할 수 없다.
- 재발 시 우선 확인: `worklog/team_config.json`, `worklog/scripts/worklog_paths.py`, `init_daily.py`, `init_entry.py`, `sync_daily_to_notion.py`, `docs/INSTALL_WINDOWS.md`, `docs/MCP_SETUP.md`.

## 8. 이번 작업에서 배운 점

- 템플릿만 추가해도 팀 운영이 바뀌지 않는다. 생성 경로, 캘린더, 동기화 스크립트까지 같은 모델을 따라야 기록이 누락되지 않는다.
- 온보딩 문서는 도구 목록보다 “처음 무엇을 열고, 실패하면 어디를 확인하는가”가 더 중요하다.

## 9. 개선사항 / TODO

- [ ] 팀원별 실제 daily/entry 생성과 Notion 동기화를 주기적으로 확인한다.
- [ ] 작업 기록에 Screen ID, Figma node, API·DB·검증 범위를 남기는 기준을 강화한다.
- [ ] MCP/Figma 플러그인·Windows setup은 버전 변경 시 개별 실행 증거를 다시 확인한다.

## 10. 검증 내용

- Git 커밋에서 개인 경로 전환, entry 생성기 추가, 문서/스크립트 동시 변경을 확인했다.
- 템플릿과 가이드의 경로가 `worklog/daily/{이름}`, `worklog/entries/{이름}` 구조를 가리키는지 대조했다.
- 실제 Notion 업로드·각 팀원 환경의 설치/플러그인 실행은 이 날짜에 저장된 결과가 없어 완료로 기록하지 않는다.

## 11. 포트폴리오용 요약

- 팀 워크로그를 일일 공유와 기능별 상세 근거로 분리하고, 개인별 경로·생성 스크립트·Windows/MCP/Figma 온보딩 문서를 연결해 협업 운영 기반을 정리했다.

## 12. 참고 자료

- `worklog/README.md`, `worklog/guide-team-daily.md`, `worklog/guide-personal-worklog.md`
- `worklog/templates/`, `worklog/scripts/init_daily.py`, `worklog/scripts/init_entry.py`, `worklog/scripts/worklog_paths.py`
- `docs/INSTALL_WINDOWS.md`, `docs/MCP_SETUP.md`, `docs/GETTING_STARTED.md`
