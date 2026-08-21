# 2026-08-21 RTOS 기본 이미지·상세 텍스트 영수증 병행 구조와 팀 조율 — 이하진

> **템플릿:** [03-work-log-template.md](../../../docs/guides/03-work-log-template.md) · **일일:** [2026-08-21.md](../../daily/이하진/2026-08-21.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-08-21
- 담당자: 이하진
- 저장소: ASAK-RTOS, ASAK-back
- 관련 커밋: 없음 — daily 기준 RTOS 코드는 이 시점까지 **미커밋(코드 수정·구조 검토 진행 중)**. 아래 내용은 대화·코드 검토 기반 판단 기록이며, 최종 빌드·실기기 검증은 남아 있다.
- 작업 유형: `feat` / `fix` / `collaboration`

## 2. 작업 목적

- 기존 `PRINT_RECEIPT`(주문번호|메뉴요약|금액 중심 기본 이미지 출력)를 유지한 채, 옵션·제외·결제·요청사항을 포함한 상세 텍스트 영수증 출력 경로를 추가한다.
- 같은 `main.c`를 공유하는 팀원(나연님)의 기존 기능을 깨지 않고 새 기능을 병행 지원한다.

## 3. 직접 구현 영역

- 기존 `PRINT_RECEIPT`는 **기본 이미지 출력**으로 그대로 유지하고, 신규 `PRINT_RECEIPT_TEXT` 이벤트 타입을 추가해 이미 완성된 상세 영수증 문자열을 RTOS가 다시 분해하지 않고 그대로 출력하도록 Handler를 분리했다.
- `work_t.payload` 버퍼를 `PAYLOAD_CAPACITY 2048`로, HTTP 응답 버퍼를 `RESPONSE_CAPACITY 4096`으로 확대했다.
- `json_string()`에 `\n`, `\r`, `\t`, `\"`, `\\`, `\/` escape 복원 로직을 추가해, React `JSON.stringify()`로 만든 여러 줄 영수증 payload가 RTOS에서 실제 줄바꿈으로 복원되도록 했다.
- Spring 쪽(`CreateDeviceEventRequest`, `DevicePrintCommand`, `DeviceEventService#createReceiptPrintEvent()`, `AdminDeviceEventController`)을 직접 확인해, `eventType`/`payload`가 모두 String 기반으로 변환 없이 저장·전달되므로 신규 eventType 추가에 Spring enum이나 DB 구조 변경이 필요 없다는 결론을 확인했다.

## 4. 구현 로직 / 적용한 방식

- 데이터 흐름: `CommandPollTask`가 `GET /api/rtos/device-events/pending`으로 polling → `WorkerTask`가 `eventType`/`payload` 기준으로 Handler 실행 → `PATCH /api/rtos/device-events/{eventId}/finish`로 `COMPLETED/FAILED` 보고. 이 파이프라인은 기본 이미지·상세 텍스트 두 eventType이 동일하게 공유한다.
- 왜 이 방식을 선택했는지: eventType으로 Handler를 분리하면 같은 공용 코드에서 팀원의 기존 기본 이미지 기능을 건드리지 않고 새 기능을 얹을 수 있기 때문이다. 기술적으로는 payload 포맷을 통합할 수도 있었지만, 다른 팀원이 이미 사용 중인 흐름을 깨는 것이 더 큰 위험이라고 판단했다.

## 5. AI 도움 영역

- 사용한 AI 도구: ChatGPT
- 어떤 질문/요청을 했는지: RTOS C 코드(payload 파서, Task stack/heap 구조)와 Spring `DeviceEvent` 연동 구조를 코드 단위로 리뷰해 신규 eventType 추가 시 백엔드 변경이 필요한지 확인해 달라고 요청.
- 그대로 사용한 부분: escape 처리 대상 문자 목록, 버퍼 용량 확대 방향 같은 기술적 제안.
- 수정해서 사용한 부분: 실제로 어떤 구조를 채택할지(공용 코드 병행 지원 여부, 기존 Handler 보존 여부)는 팀원 영향 범위를 직접 판단해 결정했다.

## 6. 발생 이슈

- 증상: 대화 중 "통메시지로 보낸다"는 표현이 DB 데이터를 쓰지 않고 통짜 텍스트만 보내는 것처럼 오해될 수 있었다.
- 원인: 표현이 "RTOS가 `|` 기준으로 필드를 다시 조립하지 않는다"는 의미였는데, 이것이 "DB 데이터를 안 쓴다"는 의미로 들릴 여지가 있었다.
- 해결: 주문/결제 데이터는 그대로 원본으로 사용하되, RTOS가 필드를 재조립하는 대신 이미 완성된 출력 문자열을 payload로 받는다는 점을 다시 설명해 오해를 정정했다. 나연님이 기본 이미지를 유지하고 싶다면 기존 Handler는 그대로 두고 새 eventType만 추가하는 방향으로 조정했다.

## 7. 이번 작업에서 배운 점

- 기술적으로 가능한 설계보다, 공용 코드에서 다른 팀원의 기능을 깨지 않는 병행 지원을 우선하는 것이 협업에서 더 중요하다.
- 설명이 한 번에 전달되지 않았을 때 상대가 이해하지 못했다고 넘기지 않고, 데이터 흐름과 출력 포맷의 차이를 다시 구체적으로 설명해야 오해가 풀린다는 것을 확인했다.

## 8. 개선사항 / TODO

- RTOS `PRINT_RECEIPT`(기본 이미지)/`PRINT_RECEIPT_TEXT`(상세 영수증) 각각 회귀 테스트.
- 여러 줄·따옴표·역슬래시·한글 옵션이 섞인 payload의 JSON escape 복원 검증.
- WSL 클린 빌드와 반복 이벤트 처리에서 heap/stack 안정성 재확인 후 커밋.

## 9. 검증 내용

- 실제 RTOS 로그에서 `PRINT_RECEIPT_TEXT` 이벤트가 순차 처리되고 `COMPLETED / receipt text printed` 결과가 Spring으로 보고되는 흐름은 확인했다.
- 반복 처리 시 heap/stack 안정성, 최종 빌드, 실기기 회귀 검증은 아직 남아 있다(daily 기준 미완료).
- 자세한 코드 변경 내역(payload 확장, static buffer 전환, `vPortFree` 위치 등)은 [2026-08-21 daily](../../daily/이하진/2026-08-21.md)의 "RTOS 영수증 payload 확장 및 출력 방식 분리", "FreeRTOS WorkerTask 메모리·스택 구조 보강" 카드 참조.

## 10. 포트폴리오용 요약

RTOS 공용 `main.c`에서 팀원의 기존 기본 이미지 출력을 보존하면서 상세 텍스트 영수증 출력을 eventType 분리로 병행 지원했다. 설계가 팀원에게 오해를 살 수 있는 지점(통메시지 표현)을 다시 설명해 정정하고, 완성된 구조가 Spring 쪽 DeviceEvent 구조 변경 없이도 동작함을 코드로 확인했다.

## 11. 참고 자료

- [2026-08-21 daily](../../daily/이하진/2026-08-21.md) — RTOS 관련 카드 3건(payload 확장, 메모리·스택 보강, Spring DeviceEvent 구조 점검)
- [2026-08-21 태블릿 LAN 연결 디버깅](2026-08-21-tablet-lan-connectivity-debug.md)
- [2026-08-21 영수증 데이터·디지털 확장 설계](2026-08-21-digital-receipt-and-receipt-data-design.md)
