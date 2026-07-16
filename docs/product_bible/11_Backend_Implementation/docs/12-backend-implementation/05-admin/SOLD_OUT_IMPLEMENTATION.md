# Sold-out Implementation

## 대상

```text
MENU
INGREDIENT
OPTION_ITEM
```

## Service Flow

1. 변경 목록 검증
2. 대상 조회
3. direct sold-out 변경
4. 영향 메뉴 계산
5. derived sold-out 갱신
6. 전체 transaction commit

## 핵심 규칙

- CORE → 메뉴 품절
- BASE 일부 → 대체 가능성 확인
- BASE 전체 → 메뉴 품절
- STANDARD → 제거 가능 시 메뉴 유지
- OPTIONAL → 옵션만 disabled
- Required group 전체 불가 → 메뉴 품절

## 복구

원인이 모두 해소되면 derived sold-out 해제.
directSoldOut이 true면 계속 품절.
