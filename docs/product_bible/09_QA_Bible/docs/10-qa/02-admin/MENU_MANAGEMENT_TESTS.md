# Menu Management Tests

## MENU-ADM-001 — 신규 등록

- 필수값
- 관계 저장
- 성공 Toast

## MENU-ADM-002 — 수정

- original/draft 분리
- dirty fields
- SaveBar

## MENU-ADM-003 — 필수 옵션 그룹 오류

Expected:
- min/max validation

## MENU-ADM-004 — 추천 옵션 비활성

Expected:
- 저장 차단 또는 추천 해제

## MENU-ADM-005 — 재료 중복

Expected:
- 정책에 따라 차단

## MENU-ADM-006 — 이미지 업로드 실패

Expected:
- draft 유지

## MENU-ADM-007 — 삭제

Expected:
- ConfirmDialog
- soft delete
- 과거 주문 보존

## MENU-ADM-008 — Modal

Expected:
- 검색
- preload
- cancel
- add
