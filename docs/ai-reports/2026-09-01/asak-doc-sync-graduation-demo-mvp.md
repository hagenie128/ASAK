# 종강 시연 MVP 문서화 (2026-09-01)

## 작성 문서

- `docs/wiki/graduation-demo-mvp-2026-09-02.md`

## 문서 구성

- 내일 시연할 고객 주문·관리자 운영·품절·결제수단·매출 MVP 범위
- P0/P1 QA 표와 사전조건·실행·기대 결과
- 발표 5분 흐름, 코드 설명 분담, 예상 질문 답변
- 가상 PG/실물 프린터 등 범위 제외와 Plan B

## 현재 근거와 제한

- Admin/backend에서 주문 상태 전이, 승인 결제 취소 차단, 가상 CARD 환불, 재료 품절 저장/복구, 결제수단 active 복구, 환불 후 매출 합계는 실제 QA 근거가 있다.
- Kiosk production build의 `uuid` 의존성 문제와 Kiosk E2E는 아직 통과 근거가 없으므로 P0로 남겼다.
- WSL `~/ASAK-RTOS`의 FreeRTOS POSIX polling·콘솔 영수증·finish PATCH 구현과 backend의 device event API를 확인해, RTOS 기본 콘솔 시연 절차를 추가했다.
- 실제 PG·실물 프린터·실물 RTOS 장비·영구 이벤트 큐는 완료로 표현하지 않는다.
