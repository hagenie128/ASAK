# 2026-08-21 RTOS 영수증·공용 코드 조율·태블릿 연결 — 이하진

## 1. 작업 목적

기존 기본 영수증 출력은 보존하면서 옵션·제외·결제·요청사항까지 포함하는 상세 출력 경로를 추가하고, RTOS·Spring·태블릿 연결에서 발생하는 계층별 위험을 분리한다.

## 2. 공용 코드와 팀 조율

- 기존 `PRINT_RECEIPT`는 기본 이미지 출력으로 유지하고, `PRINT_RECEIPT_TEXT`를 상세 텍스트 출력 이벤트로 분리했다.
- 주문·결제 DB 데이터를 버리는 것이 아니라, RTOS가 `|`로 세 필드를 다시 조립하지 않고 완성된 출력 문자열을 payload로 받는 방식임을 팀원에게 명확히 설명했다.
- 같은 `main.c`를 함께 쓰는 상황에서 기존 Handler를 덮어쓰지 않고 eventType별 병행 지원을 우선했다.

## 3. RTOS 안정성 점검

- 상세 영수증에 맞춰 payload·HTTP response 용량을 늘리고 JSON escape(`\n`, `\r`, `\t`, `\"`, `\\`, `\/`) 복원 방향을 적용했다.
- 큰 로컬 버퍼와 `work_t` 복사를 줄이며 Worker/Poll task의 stack, heap pointer 생명주기, `vPortFree(work)` 위치를 점검했다.
- 상세 텍스트 출력과 `COMPLETED / receipt text printed` 결과 보고 흐름은 확인했지만, 반복 처리에서 heap·stack 안정성은 WSL 빌드와 회귀 검증이 더 필요하다.

## 4. 태블릿 LAN 문제를 분해해 분석

```text
Browser secure context
→ API URL / localhost 의미
→ Vite host·proxy
→ Spring bind address
→ CORS·Firewall
→ RTOS polling·Worker
```

태블릿의 `localhost`는 개발 PC가 아니며, LAN HTTP에서는 `crypto.randomUUID()`가 secure context 제약을 받을 수 있음을 분리해 확인했다. `/api` 상대 경로와 Vite proxy, 외부 bind, 방화벽·CORS를 각각 확인해야 한다는 점을 정리했다.

## 5. 범위 통제

별도 `receipt` 테이블은 현재 시연에 필수는 아니며, 주문·상품·옵션·결제 데이터로 영수증을 조합할 수 있다고 판단했다. 이미지 영수증, `SEND_RECEIPT_MMS`, 실제 메시징 API, 바코드/QR은 장기 확장 설계이며 구현 완료로 기록하지 않는다.

## 6. AI 활용과 성장

AI로 RTOS C 코드와 Spring DeviceEvent 흐름을 검토했지만, 공용 코드 영향·실제 eventType 전달·메모리 생명주기·검증 범위는 코드와 실행 근거를 기준으로 직접 판단했다. 기술적으로 가능한 구조보다 팀원의 기존 흐름을 깨지 않는 병행 지원을 우선한 작업이다.
