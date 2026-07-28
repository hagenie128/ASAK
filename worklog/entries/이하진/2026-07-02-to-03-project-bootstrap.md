# 2026-07-02~03 프로젝트·협업 기록 기반 구축

> 일일: [2026-07-02](../../daily/이하진/2026-07-02.md) · [2026-07-03](../../daily/이하진/2026-07-03.md)

## 1. 기본 정보

- 작업 날짜: 2026-07-02~03
- 담당자: 이하진
- 저장소: ASAK (당시 monorepo) / 이후 분리 저장소 운영 기준
- 브랜치: `main`
- 근거 커밋: `e235c43`(front/back/pipeline 영역 재구성), `16e3a1d`(팀 workflow·포트폴리오 템플릿), `406d817`(샘플 워크로그), `00883df`(monorepo 구조 보완)
- 작업 유형: `docs` / `project-setup`

## 2. 작업 목적

- 프로젝트 시작 시점에 코드·데이터·문서가 뒤섞여 책임 경계가 흐려지는 문제를 막는다.
- 팀원이 같은 Git 흐름, 작업 기록 형식, 포트폴리오 증거 기준을 사용하도록 최소 공통 문서를 만든다.

## 3. 직접 구현 영역

- 저장소를 `frontend`, `backend`, `data-pipeline` 역할로 나누고 각 영역에 README·ignore·기본 진입 구조를 만들었다.
- `TEAM_SETUP.md`와 팀 workflow를 보강해 팀원이 시작 전 확인할 설정·협업 순서를 정리했다.
- `WORK_LOG_TEMPLATE.md`, `SAMPLE_WORK_LOG_EXAMPLE.md`, `PERSONAL_PORTFOLIO_TEMPLATE.md`, PR 템플릿을 추가해 작업 사실·검증·협업 맥락을 남길 수 있게 했다.
- 데이터 파이프라인의 phase1 DB/스크립트와 프론트 viewer를 역할별 경로로 재배치하고, 데이터 동기화 진입점도 분리했다.

## 4. 구현 로직 / 적용한 방식

1. 코드 실행 영역(frontend/backend), 데이터 생성·적재 영역(data-pipeline), 프로젝트 운영 문서를 같은 폴더에 섞지 않는 원칙을 세웠다.
2. 팀 작업은 Issue/PR/작업 기록으로 연결하고, 작업 기록은 “무엇을 했는가”뿐 아니라 목적·검증·다음 일을 남기는 구조로 설계했다.
3. 문서에서 정한 저장소 분리는 이후 실제 독립 repository 운영으로 이어졌지만, 이 날짜에는 그 운영 규칙과 monorepo 초기 뼈대를 만든 범위다.

## 5. AI 도움 영역

- 사용한 AI: 사후 워크로그 정리 시 Git 커밋과 변경 파일을 대조하는 보조.
- 사람이 수행한 부분: 폴더 역할, 팀 workflow, 템플릿 내용과 적용 범위 결정.
- 주의: 이 기록은 과거 커밋을 근거로 재구성한 것이므로, 당시 명령 실행 로그나 팀원별 사용 여부까지 증명하지는 않는다.

## 6. 발생 이슈

- 증상: 문서, 코드, 데이터 산출물, 개인 작업 기록이 같은 수준에서 섞이면 책임자와 정본을 찾기 어렵다.
- 원인: 초기 프로젝트에는 확정된 폴더 경계·템플릿·협업 흐름이 없었다.
- 대응: 역할별 폴더와 README를 두고, setup/worklog/portfolio/PR 템플릿을 분리했다.

## 7. 디버깅 기록

- 이 작업은 기능 버그 수정이 아닌 구조·문서 기반 작업이다.
- 확인 근거: 각 커밋의 변경 파일에서 backend 기본 패키지, frontend 진입/동기화 파일, data-pipeline phase1, 팀 setup 및 worklog/portfolio 템플릿이 추가·이동된 사실을 확인했다.
- 다시 확인할 위치: `README.md`, `TEAM_SETUP.md`, `docs/guides/`, `worklog/`, `frontend/README.md`, `backend/README.md`, `data-pipeline/phase1/README.md`.

## 8. 이번 작업에서 배운 점

- 프로젝트의 첫 구조는 단순 폴더 정리가 아니라, 데이터가 어디서 생성되고 어느 코드가 소비하는지 정하는 계약이다.
- 포트폴리오용 기록은 나중에 기억으로 복원하기보다 작업 시작부터 템플릿과 연결해 두는 편이 신뢰도가 높다.

## 9. 개선사항 / TODO

- [ ] 실제 독립 저장소 운영 시 README의 경로·원격·브랜치 안내를 계속 갱신한다.
- [ ] 일일 요약과 상세 기록, Notion 동기화의 관계를 실제 팀 사용 흐름으로 검증한다.
- [ ] 초기 구조 변경이 기능별 ownership과 API 계약에 미친 영향을 별도 문서로 관리한다.

## 10. 검증 내용

- Git 로그와 네 개의 근거 커밋을 대조했다.
- 코드 빌드나 배포를 이 작업의 완료 조건으로 실행한 기록은 없다. 문서/구조 변경이므로 이후 각 저장소의 개별 build와 사용 검증이 필요하다.

## 11. 포트폴리오용 요약

- 프로젝트 초기에 frontend·backend·data pipeline의 역할과 팀 workflow·작업 기록 템플릿을 함께 정리해, 이후 기능 구현의 책임 경계와 증거를 추적할 기반을 만들었다.

## 12. 참고 자료

- `TEAM_SETUP.md`, `WORK_LOG_TEMPLATE.md`, `SAMPLE_WORK_LOG_EXAMPLE.md`, `PERSONAL_PORTFOLIO_TEMPLATE.md`
- `frontend/README.md`, `backend/README.md`, `data-pipeline/phase1/README.md`
