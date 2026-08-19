# RTOS `device_event` 기본틀 반영 현황과 다음 작업 가이드

> 작성일: 2026-08-19
> 대상: `ASAK-back`, `ASAK-Kiosk`, `ASAK-Admin`, `ASAK` 문서
> 기준: 현재 작업 트리의 코드와 `RTOS예제.zip`의 명령 polling 예제
> 상태: **백엔드 메모리 큐/API 골격 구현됨 · DB/React/FreeRTOS 실연결 미구현 · E2E 미검증**

## 1. 목적과 시연 범위

8월 21일 최소 시연 목표는 실제 프린터가 아니라 다음 흐름을 보이는 것이다.

```text
Kiosk 또는 Admin React
  -> Spring Boot에 영수증 출력 명령 등록(PENDING)
  -> RTOS가 처리 대기 명령을 polling하여 점유(PROCESSING)
  -> RTOS PRINT_RECEIPT Handler 실행
  -> RTOS가 처리 결과 보고(COMPLETED/FAILED)
  -> React가 이벤트 상태를 조회해 결과 표시
```

실제 프린터, 보드 펌웨어, UART/Serial 연결은 이번 기본틀의 완료 조건이 아니다. `ConsoleRtosGateway`의 로그는 개발 중 명령 payload 확인용이며, FreeRTOS가 실제로 호출하는 구현체는 아니다.

관련 문서 기준:

- [WBS](../../wiki/wbs.md)는 8/21 최소 완료선을 Spring Boot + React + 콘솔로 둔다.
- [Screen Bible](../../wiki/screen-design-figma.md)은 SCR-008 주문 완료 후 SCR-020 영수증 출력 여부 선택으로 분기하도록 정의한다.
- [DB 정의서](../../wiki/db-table-definition.md)는 아직 `device_event` 테이블을 포함하지 않는다.

## 2. 지금 반영된 코드

### 2.1 공통 장치 명령 모델

경로: `ASAK-back/src/main/java/com/asak/common/device`

| 파일 | 현재 반영 내용 | 상태 |
|---|---|---|
| `DevicePrintCommand.java` | RTOS 예제의 `DeviceCommand`에 대응하는 record. 이벤트·주문·payload·요청 출처·상태·시각을 보관 | 구현됨 |
| `CreateDeviceEventRequest.java` | React 요청 DTO. `eventType`, `payload`, `requestId` 모두 필수 | 구현됨 |
| `DeviceEventResponse.java` | React/RTOS가 보는 상태 응답 DTO | 구현됨 |
| `DeviceEventService.java` | 예제의 `CommandStore` 역할. 메모리 큐 생성·점유·완료·조회 | 구현됨 |
| `DeviceGateway.java` | 콘솔/실RTOS 구현체 교체용 인터페이스 | 기본틀 |
| `ConsoleRtosGateway.java` | `PRINT_RECEIPT` 명령의 식별자·payload를 Spring 로그로 출력 | 개발용 기본틀 |
| `DeviceEventMapper.java` | MyBatis Mapper 전환 위치 | 빈 interface |
| `DeviceEventMapper.xml` | MyBatis XML 파싱을 위한 namespace 골격 | SQL 미작성 |

상태값은 아래 네 가지다.

```text
PENDING -> PROCESSING -> COMPLETED
                      -> FAILED
```

`DeviceEventService.claimNextPendingEvent()`는 가장 오래된 `PENDING` 이벤트 한 건을 선택하고 서비스 인스턴스 내부 동기화로 `PROCESSING`으로 바꾼 뒤 돌려준다. 단, 현재는 한 Spring 인스턴스의 메모리 자료구조이므로 다중 서버/재기동 상황에는 사용할 수 없다.

### 2.2 역할별 Spring Boot API

| 호출자 | Method / Path | 현재 Controller | 처리 |
|---|---|---|---|
| Kiosk React | `POST /api/kiosk/orders/{orderId}/receipt-print` | `UserReceiptController` | `requestSource=KIOSK`로 PENDING 명령 생성 |
| Kiosk React | `GET /api/kiosk/orders/device-events/{eventId}` | `UserReceiptController` | 이벤트 상태 조회 |
| Admin React | `POST /api/admin/orders/{orderId}/receipt-print` | `AdminDeviceEventController` | `requestSource=ADMIN`으로 재출력 명령 생성 |
| Admin React | `GET /api/admin/device-events` | `AdminDeviceEventController` | 현재 메모리의 이벤트 목록 조회 |
| FreeRTOS | `GET /api/rtos/device-events/pending` | `AdminDeviceEventController` | 다음 PENDING 한 건을 PROCESSING으로 점유 |
| FreeRTOS | `PATCH /api/rtos/device-events/{eventId}/finish` | `AdminDeviceEventController` | COMPLETED/FAILED 결과 반영 |

모든 응답은 기존 ASAK 공통 envelope를 사용한다.

```json
{
  "success": true,
  "status": 200,
  "code": "KIOSK_RECEIPT_PRINT_REQUESTED",
  "message": "영수증 출력 요청을 등록했습니다.",
  "data": { "...": "..." }
}
```

### 2.3 요청/응답 데이터

출력 요청 body:

```json
{
  "eventType": "PRINT_RECEIPT",
  "payload": "ORDER-A1035|아메리카노 x 2|9000",
  "requestId": "browser-uuid-001"
}
```

현재 `payload`는 RTOS 예제의 문자열형 계약에 맞춘 값이다. 실제 ASAK 구현에서는 RTOS C 코드의 JSON parser까지 같이 준비된 뒤 아래처럼 구조화 JSON 문자열로 변경하는 것을 권장한다.

```json
{
  "orderNo": "A1035",
  "totalAmount": 9000,
  "items": [{ "name": "아메리카노", "quantity": 2 }]
}
```

응답 `data`의 필드:

| 필드 | 의미 |
|---|---|
| `eventId` | 장치 이벤트 식별자 |
| `orderId` | 주문 식별자 |
| `eventType` | 현재 `PRINT_RECEIPT` 사용 |
| `payload` | RTOS Handler에 전달할 출력 정보 |
| `requestSource` | `KIOSK` 또는 `ADMIN` |
| `status` | `PENDING`, `PROCESSING`, `COMPLETED`, `FAILED` |
| `result` | RTOS Handler의 결과 문구. 처리 전에는 `null` |
| `requestedAt` | Spring이 명령을 만든 시각 |
| `completedAt` | RTOS 결과를 반영한 시각. 처리 전에는 `null` |

## 3. RTOS예제.zip과의 매핑

| 예제 구성 | ASAK 기본틀 | 차이 |
|---|---|---|
| `DeviceCommand` | `DevicePrintCommand` | ASAK은 주문 ID·요청 출처 추가 |
| `CommandStore` | `DeviceEventService` | 예제와 같이 메모리 저장. 향후 MyBatis DB 저장으로 교체 필요 |
| `POST /api/commands` | Kiosk/Admin `receipt-print` POST | 역할별 URL로 분리 |
| `GET /api/commands/pending` | `GET /api/rtos/device-events/pending` | 명령을 점유하며 PROCESSING 전환 |
| `PATCH /api/commands/{id}/finish` | `PATCH /api/rtos/device-events/{eventId}/finish` | 결과 상태를 공통 envelope로 반환 |
| React 상태 polling | Kiosk eventId 조회 API | Kiosk 코드에는 아직 미연결 |
| `handle_print_receipt` | FreeRTOS 측에 추후 작성 | ASAK repository에는 아직 C RTOS 클라이언트 없음 |

중요: 예제 React/RTOS 코드는 응답 객체 또는 배열을 직접 읽는다. ASAK API는 `data` 아래에 실제 값을 넣는다. FreeRTOS의 `parse_work()`와 React의 API 함수는 **반드시 `data` envelope를 해제하도록 수정**해야 한다. 그대로 복사하면 `eventId`, `status`를 찾지 못한다.

## 4. 화면·상태·데이터 연결 계획

### SCR-008 주문 완료

- Figma: node `75:9`
- 기존 화면: `ASAK-Kiosk/src/pages/kiosk/OrderCompletePage.jsx`
- 현재 상태: 주문번호가 `1225`로 하드코딩되어 있고, 영수증 버튼은 문구만 있으며 클릭 핸들러가 없다.
- 다음 연결: 결제 성공 데이터의 `orderId`, `orderNo`, `totalAmount`를 세션에 보관하고 SCR-020으로 전달한다.

### SCR-020 영수증 출력 여부 선택

- Figma Frame/Node: 미확정
- 필요한 입력: `orderId`, `orderNo`, `paymentStatus`, `totalAmount`
- 기존 UI 골격: `ASAK-Kiosk/src/pages/kiosk/ReceiptPage.jsx`
- 화면 상태:

| 상태 | 표시/동작 |
|---|---|
| Default | 영수증 출력 여부와 출력 버튼 표시 |
| Loading | POST 요청 중 버튼 비활성화, “출력 요청 중…” 표시 |
| Empty | `orderId` 또는 `orderNo`가 없으면 출력 불가 문구와 비활성 버튼 |
| Error | POST 또는 polling 실패 시 재시도 버튼과 오류 문구 |
| Success | `COMPLETED`와 `result` 표시 후 완료 화면 또는 홈으로 이동 |
| Disabled | 요청 진행 중 또는 결과 확정 후 중복 출력 방지 |

### Admin 주문 상세

- 기존 출력 버튼 연결점: `ASAK-Admin/src/components/admin/orders/OrderDetailPanel.jsx`
- 다음 연결: `onPrintReceipt(orderId)`에서 Admin POST API를 호출하고, `eventId` 결과를 주문 상세 또는 운영 로그에 표시한다.
- Admin이 출력 요청을 만들었을 뿐 실제 출력 완료를 뜻하지 않으므로, `PENDING`/`PROCESSING`을 “출력 완료”로 표시하면 안 된다.

## 5. 다음 구현 순서

### 1단계 — 서버 골격 수동 확인

1. Spring Boot를 실행한다.
2. Kiosk 또는 Admin POST로 이벤트를 하나 만든다.
3. RTOS pending API를 한 번 호출해 `PENDING -> PROCESSING`을 확인한다.
4. finish API로 `COMPLETED` 또는 `FAILED`를 보고한다.
5. Kiosk event 조회 또는 Admin 목록 조회로 최종 상태를 확인한다.

예시 PowerShell 요청:

```powershell
$body = '{"eventType":"PRINT_RECEIPT","payload":"ORDER-A1035|아메리카노 x 2|9000","requestId":"demo-001"}'

Invoke-RestMethod -Method Post `
  -Uri "http://localhost:8080/api/kiosk/orders/35/receipt-print" `
  -ContentType "application/json" `
  -Body $body

Invoke-RestMethod -Method Get `
  -Uri "http://localhost:8080/api/rtos/device-events/pending"

$finish = '{"status":"COMPLETED","result":"receipt print handler completed"}'
Invoke-RestMethod -Method Patch `
  -Uri "http://localhost:8080/api/rtos/device-events/1/finish" `
  -ContentType "application/json" `
  -Body $finish
```

### 2단계 — FreeRTOS C 클라이언트 연결

1. 예제의 `command_poll_task`가 호출하는 URL을 `/api/rtos/device-events/pending`으로 변경한다.
2. 예제의 `parse_work()`가 ASAK envelope의 `data.eventId`, `data.eventType`, `data.payload`, `data.status`를 읽도록 변경한다.
3. `PRINT_RECEIPT` Handler가 payload를 출력하고 성공/실패 결과를 만든다.
4. 예제의 `report_result()` URL을 `/api/rtos/device-events/{eventId}/finish`로 바꾸고, body를 `{"status":"COMPLETED","result":"..."}`로 보낸다.
5. WSL에서 RTOS를 실행한다면 Windows Spring Boot의 실제 호스트 IP와 포트를 사용한다. WSL의 `localhost`가 Windows 서버를 항상 가리킨다고 가정하지 않는다.

### 3단계 — Kiosk React 연결

1. `src/constants/api.js`에 receipt-print와 event status endpoint를 추가한다.
2. `src/api/deviceEvent.js`에서 Axios + `unwrapResponse`로 POST/GET 함수를 만든다.
3. `OrderCompletePage`의 영수증 출력 버튼에 `orderId`를 전달한다.
4. `ReceiptPage`에서 POST 성공 후 받은 `eventId`를 state에 저장한다.
5. `status === PENDING || PROCESSING`일 때 1초 간격으로 GET polling한다.
6. `COMPLETED`면 성공 문구, `FAILED`면 `result`를 오류 문구로 표시한다.
7. unmount 때 interval을 반드시 정리하고, 처리 중 중복 클릭을 막는다.

### 4단계 — Admin React 연결

1. `ordersApi.js`에 Admin receipt-print POST와 device-events GET을 추가한다.
2. `OrderDetailPanel`의 기존 `onPrintReceipt(orderId)`에 실제 API 함수를 연결한다.
3. 재출력 요청은 `requestSource=ADMIN`으로 저장되는지 확인한다.
4. 주문 상세 또는 별도 운영 영역에서 상태와 결과 문구를 표시한다.

### 5단계 — DB/MyBatis 전환

메모리 큐 검증이 끝난 뒤 다음을 확정한다.

- `device_event` DDL: `event_id`, `order_id`, `event_type`, `payload`, `request_id`, `request_source`, `status`, `result`, `requested_at`, `completed_at`
- `request_id` unique 제약조건: Kiosk 연속 클릭/네트워크 재시도 중복 방지
- `order_id` FK 및 존재 주문 검증
- Mapper SQL: insert, eventId 조회, 목록, 원자적 claim, finish
- 다중 RTOS 또는 다중 서버 대비: `SELECT ... FOR UPDATE SKIP LOCKED` 또는 조건부 UPDATE로 `PENDING -> PROCESSING` 원자성 보장
- 서버 재기동 후에도 PENDING 이벤트를 재처리할 정책

## 6. 현재 제한과 결정 필요 사항

| 항목 | 현재 상태 | 다음 결정/작업 |
|---|---|---|
| DB 저장 | 메모리만 사용 | `device_event` DDL·Mapper SQL 승인 및 작성 |
| 중복 요청 | `requestId`를 받지만 중복 검사 없음 | unique 제약 + service/mapper 확인 추가 |
| 주문 검증 | `orderId` 존재 여부를 확인하지 않음 | 주문 Mapper/Service와 연결 |
| 예외 응답 | `IllegalArgumentException`은 현재 공통 500 처리로 갈 수 있음 | 404/409 ErrorCode 설계 |
| RTOS 인증 | 모든 API가 임시 permitAll 정책 | RTOS 전용 secret 또는 네트워크 제한 확정 |
| RTOS Controller 위치 | 임시로 `AdminDeviceEventController`에 RTOS endpoint 포함 | 인증 정책 확정 뒤 `RtosDeviceEventController` 분리 |
| Console Gateway | Bean은 있지만 Service에서 호출하지 않음 | 개발용 simulator로 쓸지, FreeRTOS만 시연할지 결정 |
| API 명세 | 기존 API-019 의미가 문서 내부에서 충돌 | 새로운 API ID와 최종 path 확정 |
| Screen ID | SCR-020 Figma Node 미확정 | Frame·문구·상태 디자인 확정 |

## 7. 검증 결과

- 실행: `ASAK-back`에서 `./gradlew.bat compileJava --no-daemon`
- 결과: **BUILD SUCCESSFUL**
- 확인 범위: 새 Java 기본틀의 컴파일
- 미실행: Spring Boot 기동, MyBatis 실제 DB 연결, HTTP API 수동 호출, Kiosk/Admin 브라우저 연결, FreeRTOS C polling, 실제 프린터/보드 연결

## 8. 시연 때 정확한 표현

사용 가능한 표현:

> React의 영수증 출력 요청을 Spring Boot가 장치 명령으로 등록하고, RTOS polling API를 통해 명령을 가져가 Handler 결과를 다시 Spring Boot에 반영하도록 기본 연결했습니다. 현재 저장소는 시연용 메모리 큐이며, 실제 프린터와 DB 영속화는 다음 단계입니다.

사용하면 안 되는 표현:

> 실제 프린터 출력이 완료되었습니다.

현재 코드에는 실제 FreeRTOS 클라이언트 실행과 장치 ACK 검증이 없으므로, 완료 상태는 RTOS 결과 보고 API가 호출된 경우에만 의미가 있다.
