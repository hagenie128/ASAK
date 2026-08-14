# Order Edge Cases and QA

## P0 Edge Cases

### 1. 메뉴 가격 변경

- Cart 이후 서버 가격 변경
- 주문 생성 시 최신 가격 재계산
- 결제 전 사용자 확인

### 2. 메뉴 품절

- Menu Detail에서 담은 뒤 품절
- Order 생성 시 차단
- Cart에서 해당 항목 강조

### 3. 옵션 품절

- 선택 옵션만 품절된 경우
- 옵션 수정 유도

### 4. 중복 주문 생성

- 결제 버튼 연타
- isSubmitting
- server idempotency key 검토

### 5. 주문 생성 후 결제 실패

- Order와 Cart 유지
- 재결제 가능
- 중복 Order 생성 방지 정책 필요

### 6. Admin 중복 상태 변경

- 동일 주문 완료 버튼 연타
- idempotent response
- TTS 중복 차단

---

## QA Checklist

### Kiosk

- [ ] orderType 유지
- [ ] Cart item 누락 없음
- [ ] selected option 저장
- [ ] excluded ingredient 저장
- [ ] totalAmount 16,800원 일치
- [ ] sold-out 차단
- [ ] price changed UI
- [ ] create loading
- [ ] create error

### Admin

- [ ] 최신 주문 우선
- [ ] 상태 badge
- [ ] 상태 전이
- [ ] 완료 성공 후 TTS
- [ ] 완료 중복 요청 방지
- [ ] 상세 item/option 표시

### Backend

- [ ] transaction
- [ ] price recalculation
- [ ] validation order
- [ ] DTO only
- [ ] status transition
- [ ] idempotency
