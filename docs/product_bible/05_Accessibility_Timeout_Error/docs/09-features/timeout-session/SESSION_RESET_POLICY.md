# Session Reset Policy

## Reset 대상
- orderType
- menu draft
- cartItems
- totalQuantity
- totalAmount
- orderId/orderNo
- paymentStatus/orderStatus
- timeout state

## Reset하지 않는 대상
- 접근성 설정
- 단말 설정
- 관리자 TTS 설정

## 주문 완료 후
Complete 화면 노출 뒤 자동 복귀.
권장 5초.

## 결제 실패
reset하지 않는다.

## 새로고침
- 결제 전: Cart persistence 선택 가능
- 결제 PROCESSING: status 조회
- 주문 완료: session reset
