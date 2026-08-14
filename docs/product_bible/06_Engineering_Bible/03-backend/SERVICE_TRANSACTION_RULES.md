# Service and Transaction Rules

## 1. Transaction 위치

비즈니스 작업 단위의 Service method에 둔다.

```java
@Transactional
public OrderResponse createOrder(OrderCreateRequest request) {
}
```

---

## 2. Read Only

조회:

```java
@Transactional(readOnly = true)
```

---

## 3. 하나의 Transaction이 필요한 작업

- Order + OrderItem + Option 저장
- 품절 batch 변경
- Menu와 관계 데이터 저장
- Payment 승인 기록
- 상태 변경 + event 기록

---

## 4. 외부 호출

실제 PG나 외부 TTS API가 생길 경우 DB Transaction 안에서 긴 외부 호출을 유지하지 않는다.

MVP 브라우저 TTS는 Backend 외부 호출 없음.

---

## 5. Rollback

품절 일괄 저장 중 일부 실패:

- 전체 rollback 권장

메뉴 저장 중 관계 일부 실패:

- 전체 rollback

---

## 6. 상태 전이 검증

Service에서 수행한다.

```text
RECEIVED → PREPARING
PREPARING → COMPLETED
```

---

## 7. Idempotency

결제·완료 처리처럼 중복 위험이 큰 작업은 현재 상태를 확인한다.

이미 완료된 요청은:

- 현재 결과 반환
- 또는 명확한 Conflict

ASAK는 상태 변경에서 idempotent 반환을 우선 검토한다.
