# Cart Edge Cases and QA

## Edge Cases

### 동일 메뉴, 다른 옵션

두 개의 Cart Item으로 유지.

### 동일 메뉴, 동일 옵션

정책 선택:

- quantity 증가
- 별도 item 유지

MVP 권장: quantity 증가.

### 옵션 수정 중 품절

저장 시 validation.
품절 option은 선택 불가.

### 마지막 항목 삭제

Empty state 이동.

### 결제 실패 후 복귀

Cart 유지.

### Timeout

정책에 따라 warning 후 reset.

### 가격 변경

Order 생성 시 최신 금액 안내.

---

## Figma QA

- [ ] 옵션 수정 visible
- [ ] 삭제 visible
- [ ] 제외/추가 분리
- [ ] 중복 아보카도 제거
- [ ] `__spec` 화면 밖
- [ ] 16,800원 유지
- [ ] Empty state
- [ ] Delete Confirm
- [ ] quantity min

## React QA

- [ ] cartItemId key
- [ ] no index mutation
- [ ] immutable update
- [ ] total derived correctly
- [ ] modal draft separated
- [ ] reset only on valid reason
