# Backend Delivery Plan

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `BACKEND_IMPLEMENTATION_ROADMAP.md`
- `VERTICAL_SLICE_ORDER.md`
- `BACKEND_CODEX_PROMPT.md`
- `BACKEND_DEFINITION_OF_DONE.md`

---

## 원문: `BACKEND_IMPLEMENTATION_ROADMAP.md`

### Backend Implementation Roadmap

#### 1단계 — 프로젝트 기반 확인

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

#### 2단계 — 공통 기반

- ApiResponse
- ErrorCode
- BusinessException
- GlobalExceptionHandler
- BaseTimeEntity
- Validation 정책
- 공통 Pagination 응답

---

#### 3단계 — Menu Read

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

#### 4단계 — Order Create

- Order
- OrderItem
- OrderItemOption
- 서버 가격 재계산
- orderNo 생성
- 주문 저장

---

#### 5단계 — Payment

- Payment
- PaymentMethod
- READY / APPROVED / FAILED
- 중복 결제 방지
- waitingOrderCount 반환

---

#### 6단계 — Admin Order

- active order list
- order list
- order detail
- status transition
- Dashboard 집계

---

#### 7단계 — Sold-out / Menu Management

- direct/derived sold-out
- ingredient role
- Menu CRUD
- batch save
- transaction rollback

---

#### 8단계 — Sales

- summary
- monthly
- daily
- Mock Data / seed
- 정합성 검증

---

#### 9단계 — 테스트·문서

- Service unit test
- Repository integration test
- Controller contract test
- seed 검수
- API 문서 갱신

---

## 원문: `VERTICAL_SLICE_ORDER.md`

### Vertical Slice Order

기능은 계층별로 한꺼번에 만들지 않고 세로로 완성한다.

#### 좋은 순서

```text
Menu List
→ DTO
→ Service
→ Repository
→ Controller
→ Test
→ Front 연결
```

그다음:

```text
Menu Detail
→ Order Create
→ Payment
→ Admin Order
```

#### 피해야 할 순서

```text
모든 Entity 작성
→ 모든 Repository 작성
→ 모든 Service 작성
→ 모든 Controller 작성
```

문제:

- 계약 불일치 발견이 늦음
- 사용하지 않는 Entity가 생김
- 프론트 연결이 마지막까지 막힘

---

## 원문: `BACKEND_CODEX_PROMPT.md`

### Backend Codex Prompt

ASAK-back의 현재 scaffold를 유지하며 구현한다.

반드시 먼저:

1. 실제 package 구조를 읽는다.
2. 기존 Controller/Service/Repository/DTO를 목록화한다.
3. Product Bible과 충돌을 보고한다.
4. 기존 파일을 삭제하지 않는다.

구현 순서:

- 공통 Response/Exception
- Menu Read
- Order Create
- Payment
- Admin Order
- Sold-out/Menu Management
- Dashboard/Sales
- Test

금지:

- Entity 직접 Response
- Controller에서 Repository 호출
- Client 가격 신뢰
- Spring/Java 버전 변경
- 전체 구조 일괄 리팩터링

---

## 원문: `BACKEND_DEFINITION_OF_DONE.md`

### Backend Definition of Done

- [ ] 앱 실행
- [ ] build
- [ ] DB migration/seed
- [ ] DTO 분리
- [ ] validation
- [ ] transaction
- [ ] price authority
- [ ] status transition
- [ ] error code
- [ ] API contract
- [ ] tests
- [ ] README
- [ ] Product Bible 갱신
