# 영수증 디지털 발송(SMS/MMS) 아키텍처 설계 — 2026-08-24

> Status: **DRAFT** — 설계·논의 단계 기록. **오늘(2026-08-24) 구현 착수하지 않음.** 오늘은 관리자
> 결제수단 API·주문/환불(`admin-todo-2026-08-24.md`)만 진행하고, 이 문서는 착수 시점을 위한
> 참고용이다. 관련 선행 문서: [`2026-08-21-digital-receipt-and-receipt-data-design.md`](../../worklog/entries/이하진/2026-08-21-digital-receipt-and-receipt-data-design.md).

## 1. 배경 — 왜 이 구조인가

실물 프린터가 없는 시연 환경에서 "프린터가 없어서 콘솔만 출력했다"보다, 실제 장치 명령을
RTOS가 polling하고 외부 I/O(SMS/MMS 발송)를 수행한 뒤 결과를 Spring에 보고하는 구조를
시연하는 편이 RTOS/IoT 학습 목적을 더 잘 보여준다는 판단(2026-08-21 선행 설계와 동일한 결론).

**핵심 원칙: Spring이 문자를 직접 보내는 게 아니라, RTOS가 발송 명령을 수행한다.**
그래야 발표에서 "Spring Boot는 장치 이벤트를 생성하고, FreeRTOS가 polling으로 명령을 수신해
WorkerTask에서 실제 외부 I/O를 수행한다"고 설명할 수 있다.

## 2. 최종 이벤트 타입 구성

| 이벤트 타입 | 역할 | 상태 |
|---|---|---|
| `PRINT_RECEIPT` | 기본 이미지, 기존 주문번호\|메뉴요약\|금액 3분할 방식 | 기존 유지, 영향 없음 |
| `PRINT_RECEIPT_TEXT` | 상세 텍스트 영수증(콘솔 시연용) | 기존 유지 |
| `SEND_RECEIPT_MMS` | 예쁜 PNG 영수증 이미지를 실제 휴대폰으로 발송 — **최종 목표** | 미구현 |

`SEND_RECEIPT_SMS`(전화번호+텍스트만 보내는 배선 테스트용 이벤트)도 중간 단계로 논의됐으나,
목표가 "실제 영수증처럼 꾸민 이미지가 휴대폰에 도착"이라 최종적으로는 `SEND_RECEIPT_MMS` 하나로
간다고 정리됐다. `SEND_RECEIPT_SMS` 관련 스니펫은 §5에 참고용으로만 남긴다.

향후 같은 구조로 `SEND_RECEIPT_DISCORD`, `SEND_RECEIPT_EMAIL`, (실물 프린터 확보 시)
`PRINT_RECEIPT_ESCPOS`까지 같은 패턴으로 확장 가능하다고 봤다(§6).

## 3. 최종 아키텍처

```text
React 주문/결제
      ↓
Spring Boot — 영수증 데이터 조회 → 예쁜 영수증 PNG 생성
      ↓
DeviceEvent 생성 (eventType = SEND_RECEIPT_MMS)
      ↓
FreeRTOS CommandPollTask (polling)
      ↓
WorkerTask
      ↓
MMS API 호출 (외부 메시징 서비스)
      ↓
📱 실제 휴대폰에 이미지 영수증 도착
      ↓
RTOS → Spring: COMPLETED / FAILED
```

**역할 분리**
- **Spring**: 주문 데이터 → 예쁜 영수증 PNG 이미지 생성. 디자인 책임.
- **RTOS**: `SEND_RECEIPT_MMS` 명령 수신 → MMS 서비스 호출 → 성공/실패 보고. 장치·외부 I/O 책임.

RTOS C 코드에서 PNG 디자인까지 만들려고 하면 임베디드 프로젝트가 그래픽 편집기가 되므로,
이미지 제작은 반드시 Spring 쪽 책임으로 고정한다.

## 4. 착수 시 구현 순서 (최종 합의 — 이 순서를 지킬 것)

> 한 번에 여러 단계를 붙였다가 어디서 죽었는지 찾는 디버깅은 하지 않는다. 아래 순서대로 하나씩
> 성공을 확인하고 다음으로 넘어간다.

```text
① 예쁜 영수증 PNG 생성 (Spring)          ← 착수 시 여기부터 시작
      ↓
② 주문 데이터로 PNG 내용 채우기
      ↓
③ Spring에 SEND_RECEIPT_MMS DeviceEvent 생성
      ↓
④ RTOS에 SEND_RECEIPT_MMS Handler 추가
      ↓
⑤ RTOS → 실제 MMS API 연결
      ↓
⑥ 휴대폰으로 이미지 영수증 수신 확인
```

### ①의 구체적인 첫 작업 (합의된 시작점)

> "지금 할 일은 딱 하나 — `ReceiptData` + `ReceiptImageRenderer` +
> `/api/test/receipt-image` 이 세 개 만들어서 브라우저에 PNG 한 장 띄우기.
> 그거 성공하기 전에는 `SEND_RECEIPT_MMS`도 SMS 업체도 RTOS Handler도 건드리지 않는다."

패키지 위치 제안: `com.asak.common.receipt` 하위에 `ReceiptData`(영수증에 들어갈 데이터 모델),
`ReceiptImageRenderer`(PNG 렌더러). 확인용 테스트 컨트롤러로 `GET /api/test/receipt-image`를
추가해 브라우저에서 PNG가 바로 뜨는지부터 확인한다. 이 단계가 끝나기 전에는 §4의 ③~⑥(SEND_RECEIPT_MMS
DeviceEvent, RTOS Handler, 실제 MMS API)에 손대지 않는다.

## 5. 참고 스니펫 — SEND_RECEIPT_SMS 배선 테스트안 (중간 단계, 참고용)

최종 목표는 §2대로 `SEND_RECEIPT_MMS`(이미지)이지만, DeviceEvent → RTOS → WorkerTask → 외부
호출의 배선 자체를 먼저 텍스트로만 검증해보자는 중간 단계 논의가 있었다. 착수 시 반드시 거쳐야
하는 단계는 아니고, 배선을 텍스트로 먼저 확인하고 싶을 때 참고한다.

**payload 포맷** — JSON을 payload 안에 또 넣지 않고 구분자로 단순화:

```text
전화번호|문자내용
```

```json
{
  "eventType": "SEND_RECEIPT_SMS",
  "payload": "01012345678|[ASAK 영수증]\n주문번호: ASAK2608210063\n총 결제금액: 18,000원",
  "requestId": "sms-test-001"
}
```

`strtok()` 대신 `strchr()`를 쓰는 이유: 문자 내용 안에 나중에 `|`가 또 나올 수 있어서, "전화번호 |
나머지 전체"처럼 **첫 번째 구분자 하나만** 분리해야 안전하다.

원문에 있던 핸들러 스니펫은 앞부분이 대화 중 잘려서 불완전하다 — 그대로 옮기며 표시만 해둔다
(착수 시 새로 작성 필요, 아래를 그대로 붙여넣지 말 것):

```c
/* 원문 누락: snprintf 등으로 result 버퍼를 채우는 앞부분이 잘려 있음 */
result,
result_size,
"sms ready: %s",
phone
);
return 0;
}
```

**기대 콘솔 출력** (배선이 맞으면 이렇게 나와야 한다는 기준):

```text
[WorkerTask] eventId=4, eventType=SEND_RECEIPT_SMS
========== SMS SEND ==========
TO: 01012345678
------------------------------
[ASAK 영수증]
주문번호: ASAK2608210063
총 결제금액: 18,000원
==============================
[RTOS -> Spring]
eventId=4,status=COMPLETED,result=sms ready: 01012345678
```

이 배선이 성공하면, `handle_send_receipt_sms()` 안의 `printf("%s\n", message);` 자리를 실제
SMS API HTTP 호출로 바꾸는 식으로 확장한다. RTOS는 이미 Spring polling(`GET
/api/rtos/device-events/pending`)과 결과 보고(`PATCH /api/rtos/device-events/{id}/finish`)에
쓰는 HTTP client 구조가 있으므로 SMS/MMS REST 호출도 같은 구조를 재사용할 수 있다.

## 6. 더 나중 — 실물 프린터 확보 시 ESC/POS 확장 경로 (참고용, 오늘·이번 스프린트 범위 아님)

프린터가 생기면 같은 영수증 데이터 계층을 ESC/POS 출력 Adapter로 확장할 수 있다는 방향도
검토됐다. Epson ESC/POS 명령 체계 기준으로: 바코드 출력 `GS k`, 바코드 하단 숫자 표시 `GS H`,
용지 컷 `GS V`, 그래픽/로고 출력용 별도 명령. 프린터 모델마다 지원 명령이 달라 실제 연결할
프린터가 정해지면 그 기준으로 로고 출력 방식(NV 메모리에 로고 등록 후 호출 등)을 확정해야 한다.
참고: [Epson TM-L90 커맨드 레퍼런스](https://download4.epson.biz/sec_pubs/pos/reference_ja/escpos/tml90.html)

이벤트 타입은 `PRINT_RECEIPT_ESCPOS`로 추가:

```java
package com.asak.common.device.receipt;

public final class EscPos {
    private EscPos() {}
    public static final byte ESC = 0x1B;
    public static final byte GS = 0x1D;
    // 원문에서 나머지 상수 정의가 대화 중 끊김 — 착수 시 새로 정의 필요
}
```

Spring에서 렌더링 후 Base64로 감싸 DeviceEvent payload로 전달:

```java
byte[] escPosData = escPosReceiptRenderer.render(receipt);
String payload = Base64.getEncoder().encodeToString(escPosData);

new CreateDeviceEventRequest(
    "PRINT_RECEIPT_ESCPOS",
    payload,
    UUID.randomUUID().toString());
```

RTOS 쪽 분기 예:

```c
else if (strcmp(work->event_type, "PRINT_RECEIPT_ESCPOS") == 0) {
    handle_print_receipt_escpos(work, result, sizeof(result));
}
```

로고 bitmap을 Base64로 매번 실어 보내면 크기가 급격히 커지므로, 현재 `payload[2048]` 버퍼는
ESC/POS + Base64 + 로고까지 들어가면 부족할 수 있다. 실제 ESC/POS로 갈 경우
`#define PAYLOAD_CAPACITY 16384` 정도로 늘리거나, 동적 할당/스트리밍 방식으로 바꾸는 편이 맞다.
로고는 매번 보내는 대신 프린터 NV 메모리에 한 번 등록해두고 출력 시 호출하는 방식이 더 실무적이다.

이메일 채널도 같은 패턴으로 후보에 있었다(Spring이 직접 발송, RTOS 경유 아님):

```java
public void sendReceipt(String email, String orderNumber, String receiptHtml) {
    MimeMessage message = mailSender.createMimeMessage();
    MimeMessageHelper helper = new MimeMessageHelper(message, "UTF-8");
    helper.setTo(email);
    helper.setSubject("[ASAK] 주문 영수증 " + orderNumber);
    helper.setText(receiptHtml, true);
    mailSender.send(message);
}
```

## 7. 영수증 디자인 레이아웃 (최종안)

텍스트로 흉내 내지 않고 실제 PNG로 디자인한다 — 로고는 진짜 이미지, 바코드는 진짜 CODE128,
QR도 진짜 QR(주문 상세/이벤트/리뷰/영수증 조회 URL 중 하나로 연결).

```text
┌──────────────────────────┐
          [ ASAK LOGO ]
        ASAK RECEIPT
      FRESH & HEALTHY

  ASAK 성수점
  서울특별시 성동구 ○○로 00
  TEL 02-0000-0000
  사업자번호 000-00-00000
────────────────────────────
 RECEIPT   R260821-0063
 ORDER     ASAK2608210063
 DATE      2026.08.21 20:10
 카카오페이 · 결제완료
────────────────────────────
 랜치 콥 샐러디 × 1      9,600
   + 저당 랜치               0
   + 토마토                700
   + 카사바칩                0
 곡물랩 × 1              8,400
   + 들기름소이              0
   + 코크제로                0
────────────────────────────
 요청사항
 없음
────────────────────────────
          TOTAL        18,000원
────────────────────────────
        ASAK EVENT
   다음 방문 음료 1,000원 할인

          [ BARCODE ]
       R2608210063

            [ QR ]

   THANK YOU FOR YOUR ORDER
└──────────────────────────┘
```

이 PNG 한 장을 MMS·이메일·Discord·관리자 화면·(나중에) 실물 프린터까지 전부 재사용하는 것이
핵심이다 — 영수증 데이터/디자인은 한 번만 만들고 출력 대상만 바꾼다.

## 8. store_cfg(매장 공통 설정) — 오늘 결제수단 작업과의 접점

오늘 결제수단 API 작업 중 확인된 것: `receiptMessage`(영수증 안내 문구)는 결제수단(`pay_method_cfg`)
row가 아니라 **매장 전체에 하나뿐인 설정**이다 — `PaymentMethodPage.jsx`의 정적 `POLICIES` 배열에
결제수단별이 아니라 페이지당 하나로 박혀 있는 게 근거. `failureRetentionMinutes`(결제 실패 시
장바구니 5분 유지)도 같은 성격.

이 문서의 발송 채널(SMS/MMS/이메일) 구현 시 필요해질 발신자 정보 — 매장명, 주소, 전화번호,
사업자번호, 발신 전화번호(MMS 발신 프로필) 등 — 도 결제수단 테이블이 아니라 같은 매장 공통
설정에 들어갈 후보다. 다만 이번 receipt/MMS 구조는 오늘 범위가 아니므로, `store_cfg` 실제
스키마/컬럼 확정은 결제수단 쪽 `receiptMessage` 처리 방향이 정해질 때 함께 검토한다 (백엔드에
아직 이런 테이블 없음 — `store_cfg`/`shop_cfg` 류 검색 결과 없음, 신규 생성 필요).

## 9. 오늘(2026-08-24) 시점 상태

- 이 문서에 적힌 내용은 전부 설계·논의 단계이며 **구현되지 않았다.**
- `DeviceEventMapper.xml`은 여전히 SQL 없이 비어 있다(`device_event DDL 확정 후 추가` TODO만 존재).
- 오늘 실제로 진행하는 작업은 [`admin-todo-2026-08-24.md`](admin-todo-2026-08-24.md)의 관리자
  결제수단 API·주문/환불이다.
- 착수 시 §4의 순서(① PNG Renderer부터)를 따른다.

## 10. 참고 자료

- [2026-08-21 영수증 데이터 저장 범위·디지털 영수증 확장 설계](../../worklog/entries/이하진/2026-08-21-digital-receipt-and-receipt-data-design.md)
- [2026-08-21 RTOS 영수증 병행 구조·팀 조율](../../worklog/entries/이하진/2026-08-21-rtos-receipt-dual-format-collaboration.md)
- [Epson TM-L90 ESC/POS 커맨드 레퍼런스](https://download4.epson.biz/sec_pubs/pos/reference_ja/escpos/tml90.html)
- SOLAPI 메시징 API: [SMS](https://solapi.com/developers/api/messages-sms), [MMS](https://solapi.com/developers/api/messages-mms), [메시지 발송](https://solapi.com/developers/api/messages), [메시징 서비스 개요](https://solapi.com/message-types)
