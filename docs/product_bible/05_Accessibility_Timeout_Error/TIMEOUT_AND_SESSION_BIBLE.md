# Timeout and Session Bible

> Status: `Canonical`
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `SESSION_RESET_POLICY.md`
- `TIMEOUT_SESSION_ARCHITECTURE.md`

---

## 원문: `SESSION_RESET_POLICY.md`

### Session Reset Policy

#### Reset 대상
- orderType
- menu draft
- cartItems
- totalQuantity
- totalAmount
- orderId/orderNo
- paymentStatus/orderStatus
- timeout state

#### Reset하지 않는 대상
- 접근성 설정
- 단말 설정
- 관리자 TTS 설정

#### 주문 완료 후
Complete 화면 노출 뒤 자동 복귀.
권장 5초.

#### 결제 실패
reset하지 않는다.

#### 새로고침
- 결제 전: Cart persistence 선택 가능
- 결제 PROCESSING: status 조회
- 주문 완료: session reset

---

## 원문: `TIMEOUT_SESSION_ARCHITECTURE.md`

### Timeout and Session Architecture

> Status: Current
> Figma: SCR-013

#### 목적
사용자가 키오스크를 떠났을 때 주문 정보를 안전하게 초기화하되, 사용 중인 작업을 갑자기 잃지 않게 한다.

#### 권장 정책
```text
idleThreshold = 30초
warningAt = 20초
warningCountdown = 10초
```

흐름:
```text
20초 무입력
→ Timeout Modal
→ 10초 countdown
→ 계속 주문 / 처음으로
→ 0초 시 자동 초기화
```

#### 계속 주문
- countdown 종료
- modal 닫기
- idle timer reset
- 현재 route/state 유지

#### 처음으로
- session reset
- cart reset
- order draft reset
- Home replace navigation

#### 결제 상태별 정책
- READY: 일반 timeout 가능
- PROCESSING: timeout 금지
- APPROVED: Complete 이동
- FAILED: retry 화면에서 warning 가능

#### Reset Reasons
```text
ORDER_COMPLETED
TIMEOUT_CONFIRMED
TIMEOUT_EXPIRED
USER_RESET
SESSION_EXPIRED
```

#### React 구조
```text
useIdleTimer
TimeoutModal
sessionStore
resetSession
```

#### 구현 체크리스트
- [ ] pointer/touch/keyboard reset
- [ ] warning modal
- [ ] countdown
- [ ] processing 예외
- [ ] reset reasons
- [ ] replace navigation
