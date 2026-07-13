# QR/바코드 스캔 처리

API ID: API-020
Error: SCAN_INVALID, COUPON_EXPIRED
Method: POST
Request: scanType, code
Response: couponId, discountAmount, isValid
URL: /api/device/scan
관련 테이블: promotion (확장)
구분: 장치
사용 화면: 결제 화면
상태: 예정
설명: 모바일 쿠폰/멤버십 QR·바코드 인식 후 할인 적용
인증: N
처리 내용: 코드 유효성 검증 → 할인 금액 반환 → 결제 금액에 반영
Related to 테스트 시나리오 데이터베이스 (↔ API): 포인트·쿠폰 적립 및 QR 할인 적용 (../../09%20%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%98%A4%EB%A5%98%20%EA%B4%80%EB%A6%AC/%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4/%ED%8F%AC%EC%9D%B8%ED%8A%B8%C2%B7%EC%BF%A0%ED%8F%B0%20%EC%A0%81%EB%A6%BD%20%EB%B0%8F%20QR%20%ED%95%A0%EC%9D%B8%20%EC%A0%81%EC%9A%A9.md)
↔ 시나리오: QR/바코드로 쿠폰 인식 후 결제 (../../03%20%EC%82%AC%EC%9A%A9%EC%9E%90%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4/%EC%82%AC%EC%9A%A9%EC%9E%90%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4/QR%20%EB%B0%94%EC%BD%94%EB%93%9C%EB%A1%9C%20%EC%BF%A0%ED%8F%B0%20%EC%9D%B8%EC%8B%9D%20%ED%9B%84%20%EA%B2%B0%EC%A0%9C.md)

## 요청 예시

```json
POST /api/device/scan
{
  "scanType": "QR",
  "code": "COUPON-ASAK-2026"
}
```

## 성공 응답 예시

```json
{
  "success": true,
  "status": 200,
  "code": "DEVICE_SCAN_SUCCESS",
  "message": "스캔 인식 성공",
  "data": {
    "scanType": "QR",
    "couponId": "CPN-001",
    "discountAmount": 1000,
    "isValid": true
  }
}
```

> SC-016, RTOS-DEVICE-002. Week 5 MVP 범위에서 제외.
>