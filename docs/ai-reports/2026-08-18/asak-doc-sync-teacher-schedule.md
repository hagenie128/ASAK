# ASAK 문서 동기화 근거 — 선생님 일정 (2026-08-18)

> Status: **HISTORY**

## 1. 대상 저장소와 기준 커밋

- 저장소: `ASAK` (문서만)
- 기준 커밋: 이 작업 시점의 로컬 `main` (원격 반영은 별도 깃반영)
- 소스코드·DB·Figma·DevCopilot 원격은 수정하지 않음

## 2. 확인한 코드·문서

- 사용자 제공: 원 일정표 + 선생님 2026-08-18 채널 메시지
- `docs/wiki/wbs.md` 9주 로드맵(구) · `START_HERE.md` 8/7 허브 재조정
- `docs/wiki/future-scope.md` RTOS OUT_OF_SCOPE
- `docs/wiki/db-table-definition.md` 22테이블 — `device_event` 없음
- `ASAK-back` grep: `device_event` / `DeviceEvent` **없음**
- `docs/wiki/rest-api-spec.md` API-019 receipt-print (Week 5 MVP 제외), API-020 scan (EXCLUDED)
- `docs/00-presentation` RTOS 금지 키워드

## 3. 갱신한 문서

- `docs/wiki/wbs.md` — 이번 주 우선, 남은 일정, 제외 범위
- `docs/wiki/wbs-status-notes.md`
- `docs/wiki/future-scope.md` — 8/21 최소 IN_SCOPE vs 실하드웨어 FUTURE
- `docs/START_HERE.md`
- `docs/wiki/index.md`
- `docs/operations/meeting-minutes/2026-w34.md` (신규)
- `docs/operations/meeting-minutes/README.md` · `2026-w32.md` 다음 링크
- `docs/wiki/meeting-minutes-weekly.md` 주차 표
- `worklog/weekly/2026-w34.md` (신규) · `worklog/weekly/README.md` · `docs/wiki/worklog-index.md`

## 4. 변경 근거

선생님 지시가 8/7 허브 재조정(품질검증 8/18~21, 문서~8/28)보다 최신이다. 원 일정표의 **08/17~08/21 장치 이벤트/RTOS**를 이번 주 정본으로 되돌리되, 8/18 문구대로 **적어도 Spring+React**를 최소 완료선으로 적었다.

## 5. 실행 또는 검증 결과

- 백엔드 `device_event` 미구현 — grep 0건
- RTOS 연동 QA·태블릿 테스트 **미실행**

## 6. 남은 불일치

- PPT 초안 RTOS 금지 vs 선생님 RTOS 연동 지시
- API-019가 명세상 MVP 제외
- `device_event`가 DB 22테이블에 없음

## 7. 결정 필요 사항

- 발표 슬라이드에 RTOS를 넣을지
- 8/21 슬라이스가 API-019(영수증 출력 요청)인지, 별도 `device_event` 로그 API인지
- QR/멤버십 스캔은 EXCLUDED 유지(권고)

## 8. 수정하지 않은 범위

- Product Bible Pack 본문
- 백엔드·키오스크·관리자 소스
- PPT 본문 (충돌만 기록)
- DevCopilot Hub 원격 업로드
