# 관리자 TODO 일정표 가독성 정리 (2026-08-20)

## 변경 문서

- `docs/planning/admin-todo-2026-08-05.md`

## 반영 내용

- 관리자 일정표의 긴 `의존 순서·완료 확인` 열을 `날짜·관리자 작업·짧은 완료 표시`로 축소했다.
- 8/20 매출 API·관리자 화면 TODO를 백엔드와 프런트엔드 단계로 분리했다.
- 8/21 RTOS 최소 시연 순서를 등록 → pending 조회 → finish 보고 → Admin 상태 표시로 명시했다.

## 확인 근거

- `ASAK-back/src/main/java/com/asak/admin/controller/AdminDeviceEventController.java`에 RTOS pending/finish endpoint가 있다.
- RTOS 저장소는 사용자 확인 기준 WSL 홈 `~/ASAK-RTOS`에 있다. 시연 전 WSL 경로에서 실행 확인이 필요하다.
- `git diff --check`를 통과했다.

## 미확정

- RTOS Admin 이벤트 상태를 표시할 React 컴포넌트와 API 번호는 팀 결정이 필요하다.
- 실제 DB View 적용과 RTOS 콘솔 시연은 실행 검증 전이다.
