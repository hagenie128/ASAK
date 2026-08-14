# Backend Engineering Rules

> Status: `Canonical`
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `BACKEND_ARCHITECTURE.md`
- `DTO_AND_MAPPER_RULES.md`
- `ENTITY_JPA_RULES.md`
- `LOGGING_AND_SECURITY_RULES.md`
- `SERVICE_TRANSACTION_RULES.md`
- `VALIDATION_AND_EXCEPTION_RULES.md`

---

## 원문: `BACKEND_ARCHITECTURE.md`

### Backend Architecture

> Status: Current
> Stack: Spring Boot 4.1.0 · Java 25

#### 1. 목적

Backend는 UI 데이터를 저장하는 단순 중계기가 아니라 ASAK의 비즈니스 규칙과 데이터 정합성을 보장한다.

---

#### 2. Layer

```text
Controller
→ Service
→ Repository
→ Entity
→ Database
```

DTO와 Mapper가 계층 사이의 데이터 계약을 담당한다.

---

#### 3. Controller

책임:

- HTTP request 수신
- DTO validation
- Service 호출
- HTTP response 반환

금지:

- Repository 직접 호출
- 가격 계산
- 품절 정책
- 상태 전이
- Transaction 비즈니스 흐름

##### 왜 Repository 직접 호출을 금지하는가

Controller가 DB 구조를 알게 되면:

- 비즈니스 규칙이 흩어진다.
- 재사용이 어렵다.
- 테스트가 복잡해진다.
- API 변경이 DB 변경으로 바로 이어진다.

---

#### 4. Service

책임:

- 비즈니스 규칙
- 상태 전이
- 트랜잭션
- 여러 Repository 조합
- 가격 재계산
- 품절 영향
- DTO 변환 orchestration

---

#### 5. Repository

책임:

- Entity 조회·저장
- 존재 여부
- 조건 검색
- 집계 query

금지:

- 사용자 문구
- UI 상태
- 복잡한 비즈니스 판단

---

#### 6. Entity

책임:

- DB persistence model
- 도메인 상태
- 최소한의 자기 상태 변경

Entity를 API Response로 직접 반환하지 않는다.

##### 이유

- lazy loading 노출
- 민감 필드 노출
- DB 변경이 API 변경이 됨
- 순환 참조
- serialization 문제

---

#### 7. DTO

```text
Request DTO
Response DTO
```

Entity와 분리한다.

---

#### 8. Mapper

Entity ↔ DTO 변환을 한 곳에 모은다.

작은 프로젝트에서는 static mapper도 가능하다.

Service 안에 수십 줄 변환 코드가 반복되면 분리한다.

---

#### 9. Package

현재 scaffold를 우선한다.

권장 domain-based 확장:

```text
com.asak
├─ order/
├─ menu/
├─ payment/
├─ ingredient/
├─ sales/
├─ dashboard/
└─ common/
```

프로젝트 구현 단계와 팀 합의를 무시하고 전면 이동하지 않는다.

---

## 원문: `DTO_AND_MAPPER_RULES.md`

### DTO and Mapper Rules

#### 1. DTO Naming

```text
OrderCreateRequest
OrderUpdateRequest
OrderDetailResponse
OrderListItemResponse
SalesSummaryResponse
```

`Dto` suffix를 쓸지 여부는 프로젝트 전체에서 하나로 통일한다.

현재 문서에서는 역할이 명확한 이름을 우선한다.

---

#### 2. Request와 Response 분리

같은 DTO 재사용 금지.

이유:

- 입력과 출력 필드가 다름
- Validation이 다름
- 보안·노출 정책이 다름

---

#### 3. Patch Request

변경 가능한 필드만 포함한다.

```java
public record OrderStatusUpdateRequest(
    @NotNull OrderStatus status
) {}
```

---

#### 4. List와 Detail 분리

List에는 필요한 최소 필드.

Detail에는 item·option 등 상세 포함.

---

#### 5. Mapper

```java
public final class OrderMapper {
    public static OrderDetailResponse toDetailResponse(Order order) {
    }
}
```

Mapper에 DB 조회나 비즈니스 검증을 넣지 않는다.

---

#### 6. Record

Java 25 환경에서 Request/Response DTO는 record 사용을 검토할 수 있다.

단, 팀 수업 방식과 Jackson/Validation 사용 패턴을 맞춘다.

---

## 원문: `ENTITY_JPA_RULES.md`

### Entity and JPA Rules

> Status: Current

#### 1. Entity Naming

```text
Order
OrderItem
OrderItemOption
Menu
Ingredient
OptionGroup
OptionItem
Payment
```

Class는 PascalCase.

DB는 snake_case.

---

#### 2. PK

권장:

```java
@Id
@GeneratedValue(strategy = GenerationType.IDENTITY)
private Long id;
```

기존 DB 전략이 있으면 우선한다.

---

#### 3. Fetch Type

To-One:

```text
LAZY 권장
```

Collection:

```text
LAZY
```

EAGER 남용 금지.

---

#### 4. Cascade

부모 lifecycle과 완전히 일치할 때만 사용한다.

적합 가능:

```text
Order → OrderItem
OrderItem → OrderItemOption
```

주의:

```text
Menu → Ingredient
```

Ingredient는 공유 자원이므로 remove cascade 금지.

---

#### 5. Setter

무분별한 public setter 금지.

권장:

```java
order.changeStatus(OrderStatus.PREPARING);
```

상태 변경 의도를 method 이름으로 표현한다.

---

#### 6. Constructor / Builder

필수값을 보장한다.

Builder가 유효하지 않은 Entity 생성을 허용하지 않도록 주의한다.

---

#### 7. equals/hashCode

연관관계를 포함하지 않는다.

JPA Entity에서는 ID 기반 구현을 신중하게 사용한다.

---

#### 8. Soft Delete

Menu·Ingredient처럼 과거 주문 이력에 참조되는 데이터는 soft delete를 우선한다.

필드 예:

```text
is_deleted
deleted_at
```

기존 `isActive`/status와 의미 중복 여부를 먼저 확인한다.

---

#### 9. N+1

해결 방법:

- fetch join
- EntityGraph
- DTO projection
- query 분리

모든 관계를 EAGER로 바꾸는 방식은 금지.

---

## 원문: `LOGGING_AND_SECURITY_RULES.md`

### Logging and Security Rules

#### 1. Logging

##### INFO

- 주문 생성 성공
- 결제 상태 변경
- 관리자 상태 변경
- 품절 저장
- 주요 설정 변경

##### WARN

- 잘못된 상태 전이
- 중복 요청
- TTS 미지원은 Frontend console/warn
- 가격 불일치
- 품절 주문 시도

##### ERROR

- 예상하지 못한 서버 오류
- Transaction rollback
- DB 연결 오류
- 결제 처리 예외

---

#### 2. 로그 금지

- 비밀번호
- 인증 token 전체
- 카드 정보
- 개인정보
- request body 전체 무분별 기록

---

#### 3. Correlation

주문 관련 로그에는 가능하면:

```text
orderId
orderNo
paymentId
```

를 포함한다.

---

#### 4. Security Scope

##### Kiosk

- 공개 메뉴 조회
- 주문 생성
- 결제 시도
- 관리자 API 접근 불가

##### Admin

- 로그인/세션
- 관리자 route 보호
- 메뉴·품절·매출 관리

---

#### 5. Input Trust

Frontend 값은 신뢰하지 않는다.

특히:

- 가격
- 상태
- 권한
- 품절 여부
- 계산 결과

Backend가 검증한다.

---

## 원문: `SERVICE_TRANSACTION_RULES.md`

### Service and Transaction Rules

#### 1. Transaction 위치

비즈니스 작업 단위의 Service method에 둔다.

```java
@Transactional
public OrderResponse createOrder(OrderCreateRequest request) {
}
```

---

#### 2. Read Only

조회:

```java
@Transactional(readOnly = true)
```

---

#### 3. 하나의 Transaction이 필요한 작업

- Order + OrderItem + Option 저장
- 품절 batch 변경
- Menu와 관계 데이터 저장
- Payment 승인 기록
- 상태 변경 + event 기록

---

#### 4. 외부 호출

실제 PG나 외부 TTS API가 생길 경우 DB Transaction 안에서 긴 외부 호출을 유지하지 않는다.

MVP 브라우저 TTS는 Backend 외부 호출 없음.

---

#### 5. Rollback

품절 일괄 저장 중 일부 실패:

- 전체 rollback 권장

메뉴 저장 중 관계 일부 실패:

- 전체 rollback

---

#### 6. 상태 전이 검증

Service에서 수행한다.

```text
RECEIVED → PREPARING
PREPARING → COMPLETED
```

---

#### 7. Idempotency

결제·완료 처리처럼 중복 위험이 큰 작업은 현재 상태를 확인한다.

이미 완료된 요청은:

- 현재 결과 반환
- 또는 명확한 Conflict

ASAK는 상태 변경에서 idempotent 반환을 우선 검토한다.

---

## 원문: `VALIDATION_AND_EXCEPTION_RULES.md`

### Validation and Exception Rules

#### 1. Validation Layer

##### Frontend

빠른 UX 피드백.

##### Bean Validation

형식·필수값.

##### Service Validation

비즈니스 규칙.

##### DB Constraint

최종 데이터 무결성.

---

#### 2. Bean Validation

```java
@NotBlank
@Size
@NotNull
@Positive
@PositiveOrZero
@Min
@Max
```

예:

```java
public record MenuCreateRequest(
    @NotBlank String menuName,
    @NotNull Long categoryId,
    @PositiveOrZero Integer basePrice
) {}
```

---

#### 3. Business Validation

Bean Validation으로 표현하기 어려운 규칙:

- 필수 option min/max
- 품절 메뉴 주문
- 상태 전이
- 가격 불일치
- 결제수단 비활성

Service에서 검증한다.

---

#### 4. Exception Structure

권장:

```text
BusinessException
NotFoundException
ConflictException
InvalidStateException
```

프로젝트 규모에 맞춰 하나의 BusinessException + ErrorCode로 단순화 가능.

---

#### 5. ErrorCode

```java
public enum ErrorCode {
    MENU_NOT_FOUND,
    MENU_SOLD_OUT,
    INVALID_OPTION_SELECTION,
    ORDER_PRICE_CHANGED,
    PAYMENT_FAILED
}
```

API 코드값은 UPPER_SNAKE_CASE.

---

#### 6. GlobalExceptionHandler

책임:

- Exception → HTTP Status
- 공통 Error Response
- Validation field error
- 로그 수준 결정

---

#### 7. HTTP Status

| Situation | Status |
|---|---|
| 성공 조회 | 200 |
| 생성 | 201 |
| 잘못된 입력 | 400 |
| 인증 필요 | 401 |
| 권한 없음 | 403 |
| 없음 | 404 |
| 상태 충돌 | 409 |
| 서버 오류 | 500 |
