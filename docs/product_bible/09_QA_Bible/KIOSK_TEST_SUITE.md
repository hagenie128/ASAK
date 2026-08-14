# Kiosk Test Suite

> Status: `Canonical`
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `CART_TESTS.md`
- `KIOSK_ORDER_FLOW_TESTS.md`
- `KIOSK_SMOKE_TEST.md`
- `PAYMENT_TESTS.md`
- `TIMEOUT_ACCESSIBILITY_TESTS.md`

---

## 원문: `CART_TESTS.md`

### Cart Tests

#### CART-001 — 동일 메뉴 동일 옵션

Expected:

- 정책에 따라 quantity 증가
- 중복 item 생성 여부 일관

#### CART-002 — 동일 메뉴 다른 옵션

Expected:

- 별도 cartItemId

#### CART-003 — 수량 증가

Expected:

- lineAmount와 totalAmount 갱신

#### CART-004 — 수량 1에서 감소

Expected:

- minus disabled
- 자동 삭제 금지

#### CART-005 — 옵션 수정

Expected:

- 기존 선택 preload
- 저장 전 original 불변
- 저장 후 해당 cartItemId만 갱신

#### CART-006 — 삭제 취소

Expected:

- item 유지

#### CART-007 — 마지막 항목 삭제

Expected:

- Empty state
- total 0

#### CART-008 — 품절 검증 실패

Expected:

- 문제 item 강조
- 수정/삭제 제공

#### CART-009 — 결제 실패 복귀

Expected:

- Cart 유지

---

## 원문: `KIOSK_ORDER_FLOW_TESTS.md`

### Kiosk Order Flow Tests

#### KSK-ORDER-001 — 주문 유형 유지

Priority: P0

1. Home에서 EAT_IN 선택
2. Menu → Detail → Cart → Payment 이동

Expected:

- 모든 단계에서 orderType 유지
- Order request에 EAT_IN 포함

---

#### KSK-ORDER-002 — 필수 옵션 미선택

Priority: P0

Expected:

- Cart 추가 차단
- 필수 옵션 위치에 오류
- 기존 선택 유지

---

#### KSK-ORDER-003 — 최대 선택 초과

Expected:

- 추가 선택 차단 또는 validation
- 최대 개수 안내

---

#### KSK-ORDER-004 — 옵션 품절

Expected:

- 품절 옵션 disabled
- 기존 선택이 품절되면 수정 안내

---

#### KSK-ORDER-005 — 뒤로가기 선택 유지

Expected:

- Detail draft 유지
- Cart item과 draft 혼동 없음

---

#### KSK-ORDER-006 — 주문 생성 실패

Expected:

- Cart 유지
- 다시 시도
- Home 강제 이동 없음

---

## 원문: `KIOSK_SMOKE_TEST.md`

### Kiosk Smoke Test

#### KSK-SMOKE-001

- 앱 실행
- Home 표시
- Console fatal error 없음

#### KSK-SMOKE-002

- 주문 유형 선택
- Menu List 이동

#### KSK-SMOKE-003

- 메뉴 상세 진입
- 옵션 표시

#### KSK-SMOKE-004

- Cart 담기
- 총액 표시

#### KSK-SMOKE-005

- Payment 이동
- 결제수단 표시

#### KSK-SMOKE-006

- 승인 처리
- Complete 표시

#### KSK-SMOKE-007

- 주문 완료 후 Home 자동복귀
- session reset

---

## 원문: `PAYMENT_TESTS.md`

### Payment Tests

#### PAY-001 — 승인 성공

Priority: P0

Expected:

- PaymentStatus APPROVED
- Complete 이동
- orderNo 표시
- waitingOrderCount 표시

#### PAY-002 — 버튼 연타

Priority: P0

Expected:

- 결제 요청 1회
- 중복 승인 없음

#### PAY-003 — 실패 후 재시도

Expected:

- Cart/Order 유지
- 재결제 가능

#### PAY-004 — 다른 수단 선택

Expected:

- enabled method만 선택

#### PAY-005 — maintenance 수단

Expected:

- disabled + 점검 중

#### PAY-006 — Processing 중 Timeout

Priority: P0

Expected:

- timeout 미적용
- session 유지

#### PAY-007 — 승인 후 응답 유실

Expected:

- 재조회 또는 idempotent 결과
- 중복 결제 금지

#### PAY-008 — 금액 정합성

Expected:

- Cart, Payment, Error, Timeout, Complete 모두 16,800원

---

## 원문: `TIMEOUT_ACCESSIBILITY_TESTS.md`

### Timeout and Accessibility Tests

#### TIMEOUT-001

20초 무입력 → Warning 표시

#### TIMEOUT-002

계속 주문 → Modal 닫힘, state 유지

#### TIMEOUT-003

처음으로 → session reset, Home replace

#### TIMEOUT-004

countdown 0 → 자동 reset

#### TIMEOUT-005

결제 Processing → timeout 없음

#### A11Y-001

글자 LARGE 적용 → 모든 Kiosk 화면 반영

#### A11Y-002

EXTRA_LARGE → overflow 없음

#### A11Y-003

고대비 → 상태 식별 가능

#### A11Y-004

색상 없이 선택·오류 구분

#### A11Y-005

접근성 설정은 session reset 후 유지
