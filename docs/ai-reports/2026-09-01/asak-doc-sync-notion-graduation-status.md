# ASAK 문서·Notion 동기화 보고서 — 2026-09-01

## 목적

종강 MVP 준비를 위해 로컬 WBS/QA 문서와 Notion WBS·프로젝트·발표 페이지를 2026-09-01 확인 근거로 동기화했다.

## 정본 근거

- 관리자·백엔드 실DB QA: 주문 상태 변경/취소 가드, 가상 CARD 환불, 품절 저장·복구, 결제수단 PATCH 재조회·롤백, 주문·환불·매출 합계 대조
- 빌드: Backend Gradle test 및 Admin build 통과
- RTOS: WSL `~/ASAK-RTOS`의 FreeRTOS GCC_POSIX 기본 구현과 API polling/finish 경로는 소스·README로 확인. `make`와 실서버 E2E는 아직 실행 근거 없음.

## 반영한 로컬 문서

- `docs/wiki/wbs.md`: WBS-042/044/046/062/064/070/071과 발표 WBS-081~085의 과거 근거를 최신 상태로 수정
- `docs/wiki/wbs-status-notes.md`: QA 상태 경계 유지
- `docs/wiki/qa-test-cases.md`: 핵심 관리자 QA 기록 유지
- `docs/wiki/project-completion-checklist-2026-09-01.md`: 전체 완료 전 남은 사용자 작업
- `docs/wiki/graduation-demo-mvp-2026-09-02.md`: 종강 시연·발표·RTOS 범위

## 반영한 Notion

- `07. WBS / 개발 진행 현황`: 2026-09-01 종강 MVP 정본 블록 추가
- `키오스크 풀스택 프로젝트`: 관리자 실DB QA, P0 미완료, 범위 경계 추가
- `9/2 최종 발표 (ASAK)`: 시연 목표, 확인 근거, 시연 순서, 리허설 체크리스트, Plan B 기준 추가
- WBS 데이터베이스: WBS-042, 044, 046, 062, 064, 069, 070, 071, 081~085의 상태·진척률·비고를 현재 근거로 갱신

## 상태 원칙

- `완료`: 품절 API(WBS-062)처럼 구현과 API/DB 저장·복구 확인까지 끝난 범위만 표시했다.
- `검토중`: 주문·환불·결제수단·매출처럼 핵심 실DB QA는 끝났지만 화면/회귀 또는 범위 확장이 남은 항목이다.
- `진행중`/`지연`: Kiosk build·결제 E2E, RTOS 실실행, 현장 장비·실PG, 최종 리허설은 완료로 올리지 않았다.

## 다음 확인

1. 팀이 Backend/Admin을 기동해 핵심 시연을 1회 재현한다.
2. Kiosk 의존성/lock을 팀 코드로 정리한 뒤 build와 결제 E2E를 확인한다.
3. WSL RTOS에서 `make` 후 polling → 영수증 출력 → finish를 1회 기록한다.
4. 발표 슬라이드, 역할, Plan B를 확정하고 최종 리허설 기록을 남긴다.
