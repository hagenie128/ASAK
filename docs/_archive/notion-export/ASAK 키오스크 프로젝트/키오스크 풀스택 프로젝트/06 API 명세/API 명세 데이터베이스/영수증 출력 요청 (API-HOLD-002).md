# 영수증 출력 요청

API ID: API-HOLD-002
Error: 500 RECEIPT_PRINT_FAILED
Method: POST
Request: Path: orderId
Response: {"success": true, "message": "영수증 출력이 완료되었습니다.", "data": {"eventId": 10, "orderNo": "ORDER-20260701-0001", "deviceType": "RECEIPT_PRINTER", "eventType": "PRINT_RECEIPT", "status": "COMPLETED"}}
URL: /api/orders/{orderId}/receipt-print
관련 테이블: orders / order_item / payment / device_event
구분: 장치
사용 화면: 주문 완료 화면 / 영수증 출력 화면
상태: 보류
설명: 1차 발표 제외. 영수증/프린터는 장치 연동 단계에서 확장한다.
인증: N
처리 내용: 현재 MVP에서는 구현하지 않음

## 요청 예시

```
POST /api/orders/1/receipt-print
```

## 처리 흐름

```
키오스크 UI
→ Spring Boot
→ DB에서 영수증 데이터 조회
→ RTOS/모의 프린터로 출력 데이터 전달
→ 출력 결과 반환
→ device_event 기록
```

## 성공 응답 예시

```json
{
  "success": true,
  "message": "영수증 출력이 완료되었습니다.",
  "data": {
    "eventId": 10,
    "orderNo": "ORDER-20260701-0001",
    "deviceType": "RECEIPT_PRINTER",
    "eventType": "PRINT_RECEIPT",
    "status": "COMPLETED"
  }
}
```