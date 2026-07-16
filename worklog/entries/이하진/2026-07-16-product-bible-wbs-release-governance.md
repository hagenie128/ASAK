# 2026-07-16 Product Bible·WBS·릴리스 거버넌스 정리 — 이하진

> **템플릿:** [03-work-log-template.md](../../../docs/guides/03-work-log-template.md) · **일일:** [2026-07-16.md](../../daily/이하진/2026-07-16.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-07-16
- 담당자: 이하진
- 저장소: ASAK
- 브랜치: `docs/notion-web-audit-v1` (워크로그 작성 시점 확인)
- 관련 이슈/PR: PR #5 병합, PR #6 Cleanup Draft, PR #8 Frontend 80% Plan Draft
- 작업 유형: `docs`

## 2. 작업 목적

- 팀 문서가 구현 완료 주장, 설계안, 레거시 참고 자료를 혼동하지 않도록 정본 구조를 세우고, 프론트엔드 80% 구현과 데모·릴리스 준비에 필요한 판단 기준을 만든다.

## 3. 직접 구현 영역

- Kiosk/Admin 화면 문서, Product Bible, Component Bible, QA Bible, AI Master Bible, Frontend/Backend Implementation 문서의 위치와 역할을 정리했다.
- 문서 구조 재정리, 구버전 문서 아카이브, generated report/script 정리, canonical repository documentation structure 정의를 수행했다.
- DevCopilot baseline·WBS 2.0·WBS 지표·legacy WBS 중복·release/demo readiness를 순서대로 점검하고, 문서·화면·구현의 우선순위를 프론트엔드 80% 계획으로 정리했다.

## 4. 구현 로직 / 적용한 방식

- 문서의 정보 가치를 정본, 구현 계획, 참고/레거시, 생성 산출물로 구분했다.
- Screen ID·Product Bible·Figma·현재 코드의 근거 순서를 문서 탐색 규칙으로 정해, 한 화면을 구현할 때 출처를 역추적할 수 있게 했다.
- WBS는 단순 작업 목록 대신 구현 가능한 Vertical Slice, QA·릴리스 조건, 담당자 확인 항목과 연결했다.

## 5. AI 도움 영역

- 사용한 AI 도구: Codex, ChatGPT
- 어떤 질문/요청을 했는지: 실제 Git 커밋과 문서 폴더를 기준으로 변경 목적을 묶고, 문서 간 중복·누락·정본 혼선 후보를 찾는 데 도움을 요청했다.
- AI가 도움 준 내용: 문서 분류, 구현 순서 초안, WBS/릴리스 점검표, 파일 간 연결 관계를 정리했다.
- 그대로 사용한 부분: Git 커밋 제목·시각·변경 경로, 문서 폴더 구조처럼 저장소에서 확인되는 사실.
- 수정해서 사용한 부분: 어떤 문서를 정본으로 보관할지, 아카이브 전환과 구현 우선순위, 팀에 공유할 문구는 직접 판단했다.

## 6. 발생 이슈

- 이슈 1:
  - 증상: 문서가 많아 같은 기능의 계획·설계·구현 상태를 한 번에 판단하기 어려움.
  - 원인: 이전 자료, 생성 보고서, Product Bible 확장본, 화면 문서가 같은 위치 또는 유사한 이름으로 섞여 있었음.
  - 해결: canonical 문서 구조·아카이브 기준·구현 가이드 진입점을 분리하고, WBS 감사와 release/demo readiness 문서를 별도 관리했다.

## 7. 디버깅 기록

- 확인한 로그/에러 메시지: 7월 16일 Git 기록에서 문서 구조화, WBS 감사, 릴리스/데모 분리, Notion 감사, 프론트엔드 계획 관련 커밋이 연속으로 확인됐다.
- 의심했던 지점: 문서 추가가 실제 기능 구현으로 오해될 수 있는지, 아카이브가 정본 문서를 가리는지, WBS 수치가 중복 집계되는지.
- 실제 원인: 문서 수명주기와 구현 근거의 구분이 문서 안에서 충분히 드러나지 않았다.
- 다시 같은 문제가 생기면 먼저 볼 파일/명령어: `docs/governance/PRODUCT_BIBLE_INDEX.md`, `docs/planning/IMPLEMENTATION_PRIORITY.md`, `docs/planning/CURRENT_IMPLEMENTATION_MAP.md`, Git log의 변경 단위.

## 8. 이번 작업에서 배운 점

- 문서를 많이 만드는 것보다, 구현자가 “지금 무엇을 믿고 어떤 순서로 만들지”를 1분 안에 찾게 하는 구조가 더 중요하다.
- WBS 완료 표시는 코드·테스트·화면 근거와 분리해 관리해야 팀이 현재 위험을 과소평가하지 않는다.

## 9. 개선사항 / TODO

- 구현 시작 전 각 담당자가 Screen ID·Figma Frame·데이터 필드·상태·재사용 컴포넌트를 가이드에 따라 확인한다.
- 문서상 완료/통과 표기는 실제 실행 근거가 없으면 `미확인` 또는 `계획`으로 유지한다.
- 아카이브 문서를 참조할 때는 정본 문서와의 관계를 링크로 명시한다.

## 10. 검증 내용

- 실행한 명령어: Git log 및 문서 경로 확인.
- 테스트한 시나리오: Product Bible/Screen/Component/QA/Implementation 문서가 역할별로 탐색 가능한지, WBS·릴리스 관련 기록이 구현 계획과 충돌하지 않는지 확인.
- 확인 결과: 7월 16일에 문서 구조, WBS, 릴리스 준비 기준을 단계적으로 정리한 Git 이력이 확인됐다. 애플리케이션 기능 테스트는 이 문서 작업에서 수행하지 않았다.

## 11. 포트폴리오용 요약

프로젝트 문서와 WBS를 정본·계획·레거시·검증 근거로 구분해, Figma와 코드 구현이 같은 우선순위로 움직일 수 있는 문서 거버넌스를 구축했다.

## 12. 첨부하면 좋은 자료

- [현재 구현 맵](../../../docs/planning/CURRENT_IMPLEMENTATION_MAP.md)
- [구현 우선순위](../../../docs/planning/IMPLEMENTATION_PRIORITY.md)
- [구현 가이드 시작점](../../../docs/implementation_guide/00_START_HERE.md)
