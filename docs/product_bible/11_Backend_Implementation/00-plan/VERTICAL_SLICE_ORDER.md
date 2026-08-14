# Vertical Slice Order

기능은 계층별로 한꺼번에 만들지 않고 세로로 완성한다.

## 좋은 순서

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

## 피해야 할 순서

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
