# QR/바코드 스캔 처리

API ID: API-HOLD-003
Error: 404 QR_NOT_FOUND
Method: POST
Request: Body: {"scanValue": "ORDER-20260701-0001", "scanType": "QR"}
Response: {"success": true, "message": "스캔 처리 성공", "data": {"scanValue": "ORDER-20260701-0001", "targetType": "COUPON", "targetId": 1, "status": "VALID"}}
URL: /api/device/scan
관련 테이블: device_event, coupon, payment
구분: 장치
사용 화면: QR/바코드 입력 화면 / 장치 테스트 화면
상태: 보류
설명: 1차 발표 제외. QR/바코드는 쿠폰 또는 장치 연동 단계에서 확장한다.
인증: N
처리 내용: 현재 MVP에서는 구현하지 않음

## 요청 예시

```json
{
  "scanValue": "ORDER-20260701-0001",
  "scanType": "QR"
}
```

## 성공 응답 예시

```json
{
  "success": true,
  "message": "QR 스캔 처리 성공",
  "data": {
    "scanValue": "ORDER-20260701-0001",
    "targetType": "ORDER",
    "targetId": 1,
    "status": "VALID"
  }
}
```