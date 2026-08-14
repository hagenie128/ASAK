# Inventory Edge Cases and QA

## Edge Cases

### 품절 저장 중 일부 실패

전체 transaction rollback 권장.

### 여러 재료가 동시에 한 메뉴에 영향

원인 목록 유지.

### 옵션 품절 해제

추천 option badge 복구 여부 확인.

### 베이스 일부 품절

다른 베이스가 있으면 메뉴 유지.

### 모든 베이스 품절

메뉴 품절.

### 관리자 두 명 동시 수정

MVP에서는 updatedAt 기반 optimistic lock 검토.

---

## QA

- [ ] direct sold-out
- [ ] core propagation
- [ ] base partial
- [ ] base all unavailable
- [ ] standard ingredient notice
- [ ] option disabled
- [ ] required group all sold-out
- [ ] recovery
- [ ] transaction rollback
