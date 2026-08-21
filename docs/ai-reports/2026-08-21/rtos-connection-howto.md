# RTOS 실연결 방법 (2026-08-21 오전)

> 대상: `ASAK-back`(Windows) ↔ `ASAK-RTOS`(WSL Ubuntu, `~/ASAK-RTOS`)
> 참고: [asak-doc-sync-rtos-device-event-guide.md](../2026-08-19/asak-doc-sync-rtos-device-event-guide.md)

## 0. 현재 상태 확인 결과

- `ASAK-RTOS/src/main.c`, `http_client.c`에 polling(`GET /api/rtos/device-events/pending`) /
  결과보고(`PATCH /api/rtos/device-events/{eventId}/finish`) 로직이 이미 구현돼 있고,
  ASAK 공통 envelope의 `data.eventId/eventType/payload`를 파싱하도록 되어 있음.
- WSL에서 `make` 클린 빌드 성공 확인 (`asak_rtos` 바이너리 생성됨).
- FreeRTOS Kernel 경로: `~/rtos-kiosk-course/third_party/FreeRTOS-Kernel` (CMakeLists.txt가 자동 탐색).
- WSL → Windows 접근용 호스트 IP: `172.29.144.1` (환경마다 바뀔 수 있으니 아래 1-3 명령으로 매번 재확인).

## 1. Windows: Spring Boot 실행

```powershell
cd C:\ASAK-workspace\ASAK-back
.\gradlew.bat bootRun --no-daemon
```

- 로그에 `Tomcat started on port 8080`, `Started AsakBackendApplication` 뜨면 준비 완료.
- Windows 방화벽이 8080을 막고 있으면 WSL에서 연결이 안 되니, 필요하면 인바운드 규칙 확인.

## 2. WSL: 호스트 IP 확인

```bash
HOST_IP=$(ip route show default | awk '/default/ {print $3}')
echo $HOST_IP   # 예: 172.29.144.1
```

## 3. WSL: RTOS 클라이언트 빌드 & 실행

```bash
cd ~/ASAK-RTOS
export FREERTOS_KERNEL_PATH=~/rtos-kiosk-course/third_party/FreeRTOS-Kernel   # 필요시
make run SERVER_URL=http://$HOST_IP:8080
```

- 정상 시 콘솔에 `[ASAK-RTOS] polling 시작: http://172.29.144.1:8080` 출력 후 1초 간격 polling.
- `PENDING` 이벤트가 생기면 `[WorkerTask] eventId=...` → ASCII 영수증 출력 → `[RTOS -> Spring] eventId=..., status=COMPLETED` 순서로 로그가 찍혀야 정상.

## 4. Windows(또는 다른 터미널): 테스트 이벤트 생성

PowerShell 예시 (한글 payload는 `-Encoding utf8` 없이 보내면 깨질 수 있으니 아래처럼 UTF-8 바이트로 보낼 것):

```powershell
$body = '{"eventType":"PRINT_RECEIPT","payload":"ORDER-A1035|아메리카노 x 2|9000","requestId":"demo-001"}'

Invoke-RestMethod -Method Post `
  -Uri "http://localhost:8080/api/kiosk/orders/35/receipt-print" `
  -ContentType "application/json; charset=utf-8" `
  -Body ([System.Text.Encoding]::UTF8.GetBytes($body))
```

> 주의: bash(WSL)의 `curl -d '...'`로 한글 payload를 보내면 로케일에 따라
> `Invalid UTF-8 start byte` 500 에러가 날 수 있음 (오늘 아침 실제로 재현됨).
> PowerShell + UTF-8 바이트 전송, 또는 `curl --data-binary @file.json` 방식을 권장.

## 5. 확인 포인트

- [ ] Spring Boot 로그에 `POST /api/kiosk/orders/{id}/receipt-print` 200 응답
- [ ] RTOS 콘솔에 polling → WorkerTask → ASCII 영수증 출력
- [ ] RTOS 콘솔에 `report_result` PATCH 성공 로그
- [ ] `GET /api/kiosk/orders/device-events/{eventId}` 또는 `GET /api/admin/device-events`로 최종 `COMPLETED` 상태 확인

## 6. 막히면 볼 곳

- 전체 배경·API 계약·다음 단계(Kiosk/Admin React 연결, DB 전환)는
  [asak-doc-sync-rtos-device-event-guide.md](../2026-08-19/asak-doc-sync-rtos-device-event-guide.md) 참고.
- `ASAK-RTOS/README.md`에 파일별 라인 위치 설명과 최신 상태 표가 있음.

## 7. 역할 분담

| 담당 | 범위 | 저장소 |
|---|---|---|
| 팀원 | Kiosk: 영수증 / 번호표 / 영수증+번호표 출력 | `ASAK-Kiosk` |
| 나 | Admin: 주문 상세에서 영수증(재)출력 | `ASAK-Admin` |

공통 계약: `eventType`은 백엔드에서 **plain String**(enum 아님, `CreateDeviceEventRequest.eventType`)이라
값 이름만 맞추면 서로 충돌 없이 각자 작업 가능. 현재 확정된 값은 `PRINT_RECEIPT` 하나뿐이므로,
팀원이 `번호표`/`영수증+번호표`용 값(예: `PRINT_TICKET`, `PRINT_RECEIPT_AND_TICKET`)을 새로 쓸 계획이면
이름을 미리 맞춰두는 게 좋음. RTOS C 클라이언트(`handle_print_receipt`)는 현재 `PRINT_RECEIPT`만
처리하므로, 새 이벤트 타입이 생기면 `main.c`의 `worker_task`에 분기 추가가 필요함(팀원 or 별도 조율).

### 7-1. Kiosk (팀원 담당, 참고용 연결점만 기록)

- `ASAK-Kiosk/src/pages/kiosk/OrderCompletePage.jsx`: 주문 완료 후 `orderId/orderNo/totalAmount`를
  세션에 보관해 SCR-020으로 전달.
- `ASAK-Kiosk/src/pages/kiosk/ReceiptPage.jsx`: 출력 여부 선택 화면(Default/Loading/Empty/Error/Success/Disabled).
- `ASAK-Kiosk/src/components/kiosk/ReceiptActions.jsx`: 현재 `return null`인 빈 스텁 — 실제 CTA 구현 필요.
- 호출 API: `POST /api/kiosk/orders/{orderId}/receipt-print`, `GET /api/kiosk/orders/device-events/{eventId}`.

### 7-2. Admin 영수증 출력 (내 담당 — 구체 진행 순서)

현재 상태: 버튼 UI와 훅 자리는 이미 있고, TODO 주석으로 연결 지점만 비워둔 상태.

1. **`ASAK-Admin/src/constants/api.js`** — `API_ENDPOINTS`에 엔드포인트 추가.
   ```js
   printReceipt: (orderId) => `${API_BASE_PATH}/orders/${orderId}/receipt-print`,
   deviceEvents: `${API_BASE_PATH}/device-events`,
   ```

2. **`ASAK-Admin/src/api/ordersApi.js`** — TODO-041 자리에 실제 함수 추가 (mock `printAdminOrderReceipt`
   대신 백엔드 호출로 교체).
   ```js
   printReceipt: (orderId) =>
     apiClient.post(API_ENDPOINTS.printReceipt(orderId), {
       eventType: "PRINT_RECEIPT",
       payload: `...`,      // 주문번호|메뉴요약|금액 형식 (RTOS 파서 계약)
       requestId: crypto.randomUUID(),
     }),
   listDeviceEvents: () => apiClient.get(API_ENDPOINTS.deviceEvents),
   ```
   - 응답 `data.eventId`, `data.status`를 그대로 씀 (envelope 해제는 `apiClient`가 이미 처리하는지 확인).
   - `payload` 문자열은 RTOS `handle_print_receipt`가 `|`로 3분할해서 읽으므로 순서·구분자 유지 필수.

3. **`ASAK-Admin/src/pages/admin/OrderManagePage.jsx` (94~158줄 근처)** — TODO-043 주석 해제하고 구현.
   - `handlePrintReceipt(orderId)`에서 `printAdminOrderReceipt` 대신 `ordersApi.printReceipt(orderId)` 호출.
   - 성공 시 `result.data.eventId`를 저장해뒀다가, `PENDING`/`PROCESSING`일 때는
     "출력 완료"로 표시하지 말 것 (가이드 문서 4절 경고 사항). 필요하면 1초 polling으로
     `COMPLETED`/`FAILED`를 확인.
   - `<OrderDetailPanel onPrintReceipt={handlePrintReceipt} />` 주석 해제 (247번째 줄 근처).

4. **`ASAK-Admin/src/components/admin/orders/OrderDetailPanel.jsx`** — 이미 `onPrintReceipt(selectedOrder.orderId)`
   버튼(185줄)이 연결되어 있으므로 추가 수정 불필요. `canPrintReceipt` 조건(46~47줄)만 재확인.

5. **테스트**: Admin에서 결제완료 주문 하나 골라 "영수증 출력" 클릭 → 위 1~6절 방식으로 띄운
   Spring Boot + WSL RTOS 클라이언트에서 실제로 polling → 콘솔 영수증 → `finish` PATCH까지
   찍히는지 확인. `GET /api/admin/device-events`로 최종 상태 재조회.

6. **주의**: `requestSource=ADMIN`으로 기록되는지 확인(`AdminDeviceEventController`가
   `createReceiptPrintEvent(orderId, request, "ADMIN")`로 고정 전달하므로 별도 처리 불필요, 백엔드 응답에서
   `requestSource` 필드로 재검증만).

## 8. 영수증 모양 설계 — Admin 상세 패널과 동일하게

목표: 지금 RTOS에 찍히는 영수증은 `주문번호|메뉴요약|금액` 3필드뿐인데, 이걸
`ASAK-Admin/src/components/admin/orders/OrderDetailPanel.jsx`(72~154줄)가 보여주는 정보
(주문번호/주문일시/결제수단, 메뉴명·수량·단가, 옵션, 제외 재료, 메뉴별 합계, 요청사항, 총 결제 금액)
와 동일하게 확장.

### 8-1. 방식: 사전 포맷팅된 텍스트 통째 전송 (채택)

구조화 JSON을 RTOS가 직접 파싱하게 하는 대신, **Admin(JS) 쪽에서 영수증 전체를 줄바꿈 포함
완성된 문자열로 조립**해서 `payload`에 그대로 넣는다. RTOS는 그 문자열을 분해하지 않고 통째로
출력만 하면 되므로 C 파서를 중첩 구조까지 확장할 필요가 없다.

```js
// ASAK-Admin/src/utils/receiptFormat.js (신규 제안)
// OrderDetailPanel.jsx의 getPositiveQuantity/getOptionLineAmount/getItemTotalAmount와
// 동일 계산 로직을 공용 유틸로 뽑아 여기서 재사용 (화면 표시와 출력물 금액이 어긋나지 않도록).
import { formatCurrency } from "./currency.js";
import { formatDateTime } from "./date.js";
import { PAYMENT_METHOD_LABEL } from "../constants/orderLabels.js";

export function buildReceiptText(order) {
  const lines = [];
  const W = 40;
  const rule = "-".repeat(W);

  lines.push("+" + "-".repeat(W - 2) + "+");
  lines.push(" ASAK RECEIPT".padEnd(W));
  lines.push("+" + "-".repeat(W - 2) + "+");
  lines.push(`주문번호: ${order.orderNo}`);
  lines.push(`주문일시: ${formatDateTime(order.createdAt)}`);
  lines.push(`결제수단: ${PAYMENT_METHOD_LABEL[order.paymentMethod] || "-"}`);
  lines.push(rule);

  for (const item of order.items ?? []) {
    lines.push(`${item.menuName} x${item.quantity}  ${formatCurrency(item.unitPrice)}`);
    for (const opt of item.optionItems ?? []) {
      lines.push(`  + ${opt.name}  ${formatCurrency(opt.price)}`);
    }
    for (const ex of item.excludedIngredients ?? []) {
      lines.push(`  - ${ex.name} 제외`);
    }
  }
  lines.push(rule);
  lines.push(`요청사항: ${order.requestNote || "없음"}`);
  lines.push(rule);
  lines.push(`총 결제 금액: ${formatCurrency(order.totalAmount)}`);
  lines.push("+" + "-".repeat(W - 2) + "+");

  return lines.join("\n");
}
```

`ordersApi.js`의 `printReceipt`에서 이 함수 결과를 `payload`로 사용:

```js
printReceipt: (order) =>
  apiClient.post(API_ENDPOINTS.printReceipt(order.orderId), {
    eventType: "PRINT_RECEIPT",
    payload: buildReceiptText(order),
    requestId: crypto.randomUUID(),
  }),
```

- `OrderDetailPanel.jsx`의 `getPositiveQuantity`/`getOptionLineAmount`/`getItemTotalAmount`는 현재
  파일 내부 비공개 함수라, `receiptFormat.js`와 공유하려면 별도 유틸(예:
  `src/utils/orderAmount.js`)로 뽑아 두 곳에서 import하는 걸 권장 (금액 계산 두 벌 유지 방지).

### 8-2. RTOS(`ASAK-RTOS/src/main.c`) 쪽 필수 수정 — 공유 코드, 팀원과 조율 필요

사전 포맷 텍스트 방식이어도 아래 세 가지는 고쳐야 함. 안 고치면 잘리거나 깨짐.

1. **버퍼 크기 부족**: `work_t.payload`가 `char payload[256]`로 고정(main.c 상단 struct 정의).
   옵션·제외·요청사항까지 들어간 영수증 텍스트는 256바이트를 쉽게 넘김 →
   `payload[256]` → 최소 `payload[1024]` 이상으로 확장, `RESPONSE_CAPACITY`(현재 2048)도 여유
   있는지 같이 확인.
2. **이스케이프 미처리**: `json_string()`(main.c 51-78행 근처)은 백슬래시 이스케이프를 전혀
   처리하지 않고 `"`를 만나면 바로 문자열 끝으로 판단함. JS `JSON.stringify`가 payload 안의
   줄바꿈을 `\n`으로, `"`가 있으면 `\"`로 이스케이프해서 보내는데, 지금 파서는:
   - `\n`을 실제 줄바꿈이 아니라 문자 그대로 `\`+`n`으로 복사해버림 (영수증이 한 줄로 붙어버림)
   - payload 안에 `\"`가 있으면 그 지점에서 문자열이 끝난 걸로 오판해 뒷부분이 잘림
   → `json_string()`에 `\n`→개행, `\"`→`"`, `\\`→`\` 최소 이스케이프 해제 로직 추가 필요.
3. **`handle_print_receipt` 단순화**: 지금은 `strtok(payload, "|")`로 3분할해서 찍는데,
   통짜 텍스트를 받으면 분할하지 말고 `printf("%s\n", work->payload)`로 그대로 출력하도록 교체.
   (요구되는 코드 자체는 오히려 지금보다 간단해짐.)

이 세 가지는 `ASAK-RTOS`가 팀원의 번호표/영수증+번호표 처리와 같은 `main.c`를 공유하므로,
건드리기 전에 팀원과 "영수증 payload를 통짜 텍스트로 바꾼다" 합의만 짧게 해두는 걸 권장.

## 9. TTS 개선 — 보이스 선택 + 주문번호 뒤 4자리만 읽기 (적용 완료)

관련 파일: `ASAK-Admin/src/utils/ttsMessages.js` (수정 완료),
호출부 `ASAK-Admin/src/components/admin/LiveOrderBoard.jsx` 293~299줄(수정 불필요, 함수 내부만 바뀜).

### 9-1. 보이스 선택 개선 (적용 완료)

기존엔 `ko-KR` lang만 지정하고 보이스는 브라우저 기본값에 맡기고 있었음. `speechSynthesis.getVoices()`로
설치된 한국어 보이스 목록을 받아 Google → Microsoft Neural(Heami/SunHi/InJoon) → 그 외 순으로
선택하도록 `pickKoreanVoice()`를 추가하고, `speak()`에서 `utterance.voice`로 지정하도록 반영함.
`getVoices()`가 비동기라 첫 로드 시 빈 배열일 수 있어 `window.speechSynthesis.onvoiceschanged`에서
캐시를 갱신하는 초기화 코드도 같이 넣음.

**시연 PC 실측 결과** (2026-08-21, 콘솔에서 `speechSynthesis.getVoices().filter(v=>v.lang.startsWith('ko'))`로 확인):

| 보이스 | lang | localService |
|---|---|---|
| `Microsoft Heami - Korean (Korean)` | ko-KR | true (오프라인) |
| `Google 한국의` | ko-KR | false (네트워크 필요) |

`pickKoreanVoice()`가 `Google 한국의`를 1순위로 골라서, 코드 수정 없이 이미 이 보이스가 선택됨.

**남은 리스크**: `Google 한국의`는 `localService: false`라 인터넷 연결이 필요함. 시연장 와이파이가
불안정하면 재생이 끊기거나 실패할 수 있으므로, 시연 직전 실제 네트워크 환경에서 한 번 더
들어보고 문제 있으면 Heami(오프라인)로 강제 전환하는 옵션도 고려.

### 9-2. 주문번호 뒤 4자리만 읽기 (적용 완료)

실제 `orderNo` 형식은 `ASAKyyMMddNNNN`(접두사+날짜+4자리 순번, `UserOrderService.generateOrderNo`
425~444줄 참고). 단, Admin mock 데이터(`asak-admin-data.json`)는 `ASAK-20260720-060`처럼
대시가 섞인 다른 형식이라, 단순 `slice(-4)`는 mock에서 대시까지 포함될 수 있음. 숫자만 추출해서
뒤 4자리를 뽑는 `extractLastDigits`로 두 형식 모두 안전하게 처리하도록 반영함.

### 9-3. 뒤 4자리를 사이노-한자어로 읽기 (적용 완료)

`extractLastDigits`로 뽑은 숫자를 그대로 텍스트에 넣으면(`"1234번"`), 브라우저 TTS 엔진이 자체
판단으로 34를 고유어 "서른네"로 읽어 "천이백서른네번"처럼 한자어(천이백)와 고유어(서른네)가
섞여버리는 문제가 실제로 발생함. 숫자를 미리 한글 단어로 완전히 변환해서("천이백삼십사") 텍스트에
박아 넣으면 엔진은 그 글자를 그대로 읽기만 하므로 이 문제가 사라짐.

```js
const DIGIT_WORDS = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"];
const UNIT_WORDS = ["", "십", "백", "천"];

// 숫자를 사이노-한자어로 읽어준다 (예: 1234 -> "천이백삼십사").
function toSinoKoreanNumber(num) {
  if (num === 0) return "영";

  const str = String(num);
  let result = "";

  for (let i = 0; i < str.length; i += 1) {
    const digit = Number(str[i]);
    const unitIndex = str.length - i - 1;

    if (digit === 0) continue;

    result += digit === 1 && unitIndex > 0 ? UNIT_WORDS[unitIndex] : DIGIT_WORDS[digit] + UNIT_WORDS[unitIndex];
  }

  return result;
}

const extractLastDigits = (orderNo, count = 4) =>
  String(orderNo ?? "").replace(/\D/g, "").slice(-count);

export const createOrderCompletedMessage = (orderNo) => {
  const spokenNumber = toSinoKoreanNumber(Number(extractLastDigits(orderNo)) || 0);
  return `주문번호 ${spokenNumber}번, 주문이 완료되었습니다.`;
};
```

- 지원 범위는 0~9999 (4자리 순번 형식에 맞춤). `UNIT_WORDS`가 `십/백/천`까지만 있어서 그 이상
  자리수가 필요해지면(`만` 단위) 배열 확장 필요.
- 자리 앞의 "일"은 관용적으로 생략(`일십` ✗ → `십` ✓, `일백` ✗ → `백` ✓, `일천` ✗ → `천` ✓).

## 10. 다음 작업 — RTOS 컨트롤러 분리

### 지금 상태

RTOS 전용 컨트롤러가 없다. `AdminDeviceEventController.java`(`com.asak.admin.controller`) 안에
Admin API와 RTOS API가 같이 들어있고, 클래스 상단 주석에 "RTOS 인증 정책이 정해지면 별도
Controller로 분리 / 임시 코드"라고 명시돼 있다.

```text
AdminDeviceEventController (com.asak.admin.controller)
├─ POST  /api/admin/orders/{orderId}/receipt-print   [Admin]
├─ GET   /api/admin/device-events                    [Admin]
├─ GET   /api/rtos/device-events/pending              [RTOS] ← 여기 섞여 있음
└─ PATCH /api/rtos/device-events/{eventId}/finish     [RTOS] ← 여기 섞여 있음
```

인증도 확인했음 — `SecurityConfig.java` 39행 `.authorizeHttpRequests(auth -> auth.anyRequest().permitAll())`로
지금은 `/api/admin/**`, `/api/rtos/**` 구분 없이 전부 무인증 허용 중 (34~38행 TODO-030:
"JWT 인증 구현 전까지 모든 API를 임시 허용한다").

### 분리해야 하는 이유

`admin`/`user`는 이미 각자 `controller/dto/mapper/service` 패키지로 나뉘어 있는데
(`com.asak.admin.*`, `com.asak.user.*`), RTOS도 사실상 세 번째 호출 주체(Admin/Kiosk/RTOS)라
같은 모양으로 떼는 게 자연스럽다. 더 중요한 이유는 **인증 정책이 서로 다를 수밖에 없다는 것**:

- `/api/admin/**` → TODO-030에서 예고한 대로 나중에 JWT 로그인 인증으로 바뀔 예정.
- `/api/rtos/**` → 사람이 로그인하는 게 아니라 WSL의 FreeRTOS 클라이언트가 호출하는 경로라서,
  JWT가 아니라 별도 API 키/시크릿이나 IP 제한 같은 다른 방식이 필요함.

한 Controller에 같이 있으면 `SecurityConfig`에서 두 경로를 다른 규칙으로 매칭하기 번거롭고,
나중에 Admin 로그인 붙일 때 실수로 `/api/rtos/**`까지 인증을 요구해버리는 회귀가 생기기 쉽다.

### 분리 계획

`com.asak.rtos.controller` 패키지 신설 (admin/user와 같은 레벨). RTOS는 별도 DB 접근이나
서비스 로직이 없고 기존 `common.device.DeviceEventService`를 그대로 재사용하므로,
`rtos.dto`/`rtos.mapper`/`rtos.service`는 필요 없고 `controller`만 추가하면 된다.

```java
// com.asak.rtos.controller.RtosDeviceEventController
package com.asak.rtos.controller;

import com.asak.common.device.DeviceEventResponse;
import com.asak.common.device.DeviceEventService;
import com.asak.common.device.DevicePrintCommand;
import com.asak.common.response.ApiResponse;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@RestController
@RequiredArgsConstructor
public class RtosDeviceEventController {
  private final DeviceEventService deviceEventService;

  /** RTOS CommandPollTask가 PENDING 한 건을 가져간다. */
  @GetMapping("/api/rtos/device-events/pending")
  public ApiResponse<DeviceEventResponse> claimNextPendingEvent() {
    return deviceEventService
        .claimNextPendingEvent()
        .map(response -> ApiResponse.success("RTOS_DEVICE_EVENT_CLAIMED", "처리할 장치 이벤트입니다.", response))
        .orElseGet(() -> ApiResponse.success("RTOS_DEVICE_EVENT_EMPTY", "처리할 장치 이벤트가 없습니다.", null));
  }

  /** RTOS WorkerTask가 실제 Handler 실행 결과를 Spring Boot에 보고한다. */
  @PatchMapping("/api/rtos/device-events/{eventId}/finish")
  public ApiResponse<DeviceEventResponse> finishEvent(
      @PathVariable long eventId, @Valid @RequestBody FinishRequest request) {
    DeviceEventResponse response =
        deviceEventService.finishEvent(eventId, request.status(), request.result());
    return ApiResponse.success("RTOS_DEVICE_EVENT_FINISHED", "RTOS 처리 결과를 반영했습니다.", response);
  }

  public record FinishRequest(@NotNull DevicePrintCommand.Status status, @NotBlank String result) {}
}
```

`AdminDeviceEventController`에는 Admin 전용 2개(`receipt-print`, `device-events`)만 남기고,
`claimNextPendingEvent`/`finishEvent`/`FinishRequest`와 그 import는 제거. 클래스 상단 주석의
"RTOS polling 결과 보고를 임시로 함께 둔다" 문구도 더 이상 사실이 아니게 되므로 같이 정리.

### 분리 후에 같이 하면 좋은 것 (지금은 범위 밖)

- `SecurityConfig.java`에 `/api/rtos/**` 전용 매처를 추가해, Admin 인증(JWT, TODO-030)과
  RTOS 인증(API 키/IP 제한 등)을 서로 다른 규칙으로 관리.
- RTOS 인증 방식 자체는 아직 미정 — 이 문서 6절 "현재 제한과 결정 필요 사항"의 "RTOS 인증"
  항목과 같은 미해결 지점이다.

### 주의

컨트롤러만 옮기는 단순 리팩터라 컴파일은 잘 될 가능성이 높지만, 지금까지처럼 실제로는
`compileJava`뿐 아니라 Spring Boot 기동 + WSL RTOS 클라이언트로 `GET /api/rtos/device-events/pending`
실호출까지 확인해야 진짜 끝난 것이다 (URL 문자열 자체는 안 바뀌므로 RTOS C 클라이언트
쪽은 수정 불필요).
