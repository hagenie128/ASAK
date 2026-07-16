# Logging and Security Rules

## 1. Logging

### INFO

- 주문 생성 성공
- 결제 상태 변경
- 관리자 상태 변경
- 품절 저장
- 주요 설정 변경

### WARN

- 잘못된 상태 전이
- 중복 요청
- TTS 미지원은 Frontend console/warn
- 가격 불일치
- 품절 주문 시도

### ERROR

- 예상하지 못한 서버 오류
- Transaction rollback
- DB 연결 오류
- 결제 처리 예외

---

## 2. 로그 금지

- 비밀번호
- 인증 token 전체
- 카드 정보
- 개인정보
- request body 전체 무분별 기록

---

## 3. Correlation

주문 관련 로그에는 가능하면:

```text
orderId
orderNo
paymentId
```

를 포함한다.

---

## 4. Security Scope

### Kiosk

- 공개 메뉴 조회
- 주문 생성
- 결제 시도
- 관리자 API 접근 불가

### Admin

- 로그인/세션
- 관리자 route 보호
- 메뉴·품절·매출 관리

---

## 5. Input Trust

Frontend 값은 신뢰하지 않는다.

특히:

- 가격
- 상태
- 권한
- 품절 여부
- 계산 결과

Backend가 검증한다.
