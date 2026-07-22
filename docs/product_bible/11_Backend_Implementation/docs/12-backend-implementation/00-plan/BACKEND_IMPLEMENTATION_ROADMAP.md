# Backend Implementation Roadmap

## 1단계 — 프로젝트 기반 확인

- Java 25
- Spring Boot 4.0.7
- Gradle
- package root
- application profile
- DB 연결 여부
- 기존 Controller/Service/Repository scaffold
- 공통 Response 구조

완료 조건:

- 앱 실행
- health endpoint 또는 기본 endpoint 응답
- build 통과

---

## 2단계 — 공통 기반

- ApiResponse
- ErrorCode
- BusinessException
- GlobalExceptionHandler
- BaseTimeEntity
- Validation 정책
- 공통 Pagination 응답

---

## 3단계 — Menu Read

- Category
- Menu
- Ingredient
- OptionGroup
- OptionItem
- Kiosk Menu List
- Kiosk Menu Detail

이유:

주문·장바구니·가격 계산이 Menu 데이터에 의존한다.

---

## 4단계 — Order Create

- Order
- OrderItem
- OrderItemOption
- 서버 가격 재계산
- orderNo 생성
- 주문 저장

---

## 5단계 — Payment

- Payment
- PaymentMethod
- READY / APPROVED / FAILED
- 중복 결제 방지
- waitingOrderCount 반환

---

## 6단계 — Admin Order

- active order list
- order list
- order detail
- status transition
- Dashboard 집계

---

## 7단계 — Sold-out / Menu Management

- direct/derived sold-out
- ingredient role
- Menu CRUD
- batch save
- transaction rollback

---

## 8단계 — Sales

- summary
- monthly
- daily
- Mock Data / seed
- 정합성 검증

---

## 9단계 — 테스트·문서

- Service unit test
- Repository integration test
- Controller contract test
- seed 검수
- API 문서 갱신
