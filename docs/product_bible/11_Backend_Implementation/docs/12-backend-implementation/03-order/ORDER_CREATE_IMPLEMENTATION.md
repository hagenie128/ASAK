# Order Create Implementation

## Endpoint

```http
POST /api/kiosk/orders
```

## Service Flow

1. items 존재 확인
2. menuId 일괄 조회
3. active / sold-out 검증
4. option group 규칙 검증
5. option sold-out 검증
6. ingredient 영향 검증
7. 서버 가격 계산
8. orderNo 생성
9. Order 저장
10. OrderItem 저장
11. OrderItemOption 저장
12. response 반환

## 서버 가격 계산

```text
unitAmount = menu.basePrice + selectedOptionAmount
lineAmount = unitAmount × quantity
totalAmount = sum(lineAmount)
```

클라이언트 totalAmount는 신뢰하지 않는다.

## Transaction

Order + Item + Option 전체 저장은 하나의 transaction.
