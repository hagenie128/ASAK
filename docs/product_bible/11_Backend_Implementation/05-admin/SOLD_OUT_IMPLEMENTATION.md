# Sold-out Implementation

## Current Code Status (2026-08-06)

- `AdminSoldOutController`는 `@RequestMapping("/api/admin/soldOut")`만 있고 메서드는 없다.
- `AdminSoldOutService`, `AdminSoldOutMapper`, `AdminSoldOutMapper.xml`도 구현 스텁 상태다.
- 따라서 아래 규칙은 현재 실행 중인 서버 동작이 아니라 **구현 목표/설계 메모**로 봐야 한다.

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

## Decision Needed

- 실제 PATCH body를 `targetType/targetId/isSoldOut`로 확정할지 여부
- `OPTION_ITEM` 대신 프론트 탭 값 `OPTION`과 어떤 호환 계층을 둘지 여부
- 영향 메뉴 수를 API가 직접 계산해 줄지 여부
