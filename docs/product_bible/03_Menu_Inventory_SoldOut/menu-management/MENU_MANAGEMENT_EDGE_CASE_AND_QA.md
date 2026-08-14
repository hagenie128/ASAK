# Menu Management Edge Cases and QA

## Edge Cases

### 수정 중 다른 관리자가 변경

updatedAt/version 비교.

### 재료 삭제가 알레르기·영양에 영향

재계산 경고.

### 추천 옵션 비활성화

추천 해제 또는 저장 차단.

### 필수 Option Group에 활성 옵션 없음

저장 차단.

### 메뉴 삭제 후 주문 이력

soft delete(`menu.deleted_at`)로 행 유지 → `order_item.menu_id` FK·history 유지.
목록/상세에서는 삭제 메뉴 미노출. (2026-08-11 코드 반영)

### 이미지 upload 실패

form draft 유지.

### Save 일부 실패

전체 transaction rollback 권장.

---

## Figma QA

- [ ] Add/Edit shared structure
- [ ] modal overlay
- [ ] ingredient label overlap 없음
- [ ] search copy
- [ ] cancel/add button
- [ ] SaveBar
- [ ] delete confirm
- [ ] validation message
- [ ] loading/error

## React QA

- [ ] original/draft 분리
- [ ] dirty fields
- [ ] no direct mutation
- [ ] reusable sections
- [ ] API payload mapping
- [ ] modal selection persistence

## Backend QA

- [ ] transaction
- [ ] duplicate validation
- [ ] relation save order
- [ ] orphan handling
- [x] soft delete (`deleted_at` — 코드 구현됨, 자동 테스트는 미검증)
- [x] history preservation (FK 유지 설계 — 주문 연동 E2E는 미검증)
