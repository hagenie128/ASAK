# Menu Management Implementation

## Create

```text
validate basic fields
→ category 조회
→ ingredient 관계 검증
→ option group 검증
→ nutrition/allergen 계산 또는 저장
→ Menu 저장
→ 관계 저장
```

## Update

- original entity 조회
- 변경 가능한 필드만 반영
- 연관관계 orphan 정책 확인
- transaction 내 처리

## Delete

soft delete 권장.

```text
isDeleted = true
deletedAt = now
```

기존 order history를 보존한다.

## Validation

- menuName required
- price >= 0
- minSelection <= maxSelection
- recommended option active
- duplicate ingredient policy
