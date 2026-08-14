# Timeout and Session Architecture

> Status: Current
> Figma: SCR-013

## 목적
사용자가 키오스크를 떠났을 때 주문 정보를 안전하게 초기화하되, 사용 중인 작업을 갑자기 잃지 않게 한다.

## 권장 정책
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

## 계속 주문
- countdown 종료
- modal 닫기
- idle timer reset
- 현재 route/state 유지

## 처음으로
- session reset
- cart reset
- order draft reset
- Home replace navigation

## 결제 상태별 정책
- READY: 일반 timeout 가능
- PROCESSING: timeout 금지
- APPROVED: Complete 이동
- FAILED: retry 화면에서 warning 가능

## Reset Reasons
```text
ORDER_COMPLETED
TIMEOUT_CONFIRMED
TIMEOUT_EXPIRED
USER_RESET
SESSION_EXPIRED
```

## React 구조
```text
useIdleTimer
TimeoutModal
sessionStore
resetSession
```

## 구현 체크리스트
- [ ] pointer/touch/keyboard reset
- [ ] warning modal
- [ ] countdown
- [ ] processing 예외
- [ ] reset reasons
- [ ] replace navigation
