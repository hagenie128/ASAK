# 2026-08-11 관리자 메뉴 상세·영양·재료·soft delete·FE 연동

> **일일 기록:** [2026-08-11 daily](../../daily/이하진/2026-08-11.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-08-11
- 담당자: 이하진
- 저장소: `ASAK-back`, `ASAK-Admin`
- 브랜치: `feat/admin-menu-nutrition` → `main` (`2afa10b`) · `feat/admin-menu-manage-api` → `main` (`b6e93a7`)
- 관련 이슈/PR: Issue 번호 미기재 · WBS-045·058·059 관련 코드 진전(상태 문서 DONE 변경 없음)
- 작업 유형: `feature`
- 구현 근거: back `73ab0f7` / `a6391b5` / merge `2afa10b` · Admin `0fd00f5` / merge `b6e93a7`
- Figma 기준: UI 관련이나 이번 퇴근에서 Frame/Node 대조 안 함 → `Figma 미확인`
- 완료 판정: **원격 main 코드·Bruno 문서 반영**까지. 실DB soft delete 적용·HTTP E2E·화면 QA는 미검증.

## 2. 작업 목적

- 관리자 메뉴를 목록/상세뿐 아니라 수정·삭제·재료 조회까지 서버에서 다루게 한다.
- 주문 이력 FK를 위해 삭제는 soft delete(`menu.deleted_at`)로 한다.
- Admin 화면의 편집·재료 선택이 해당 API를 호출하도록 붙인다.

## 3. 직접 구현 영역

### ASAK-back (`73ab0f7`)

- `AdminMenuService`: `getIngredients`, `updateMenu`(본문 갱신 + null이 아닌 자식 컬렉션 delete+insert), `deleteMenu`(soft delete), `insertChildren` 공통화.
- `AdminMenuController`: `GET /categories`, `GET /ingredients`를 `/{menuId}`보다 앞에 배치, `/{menuId:\\d+}`, `PATCH`/`DELETE`, 생성 시 categoryId 검증.
- Mapper/XML·DTO(`IngredientResponse` 등), `ErrorCode` 보강.
- Bruno admin 요청 번호 재정렬·`12-ingredient-list` 등 추가.
- `docs/migrations/2026-08-11_menu_soft_delete.sql`, `docs/아삭_mysql.sql`·`view.sql` soft delete/뷰 조건 정리.

### ASAK-Admin (`0fd00f5`)

- `menusApi`: `getIngredients`, `createMenu`, `updateMenu`, `deleteMenu`.
- `useMenusQuery`: 재료 로드, create/update/delete 후 목록·선택 상태 갱신.
- `MenuEditPanel` / `IngredientSelectModal` / `MenuManagePage` 연동 보완.

## 4. 구현 로직 / 적용한 방식

- **경로 충돌 방지:** Spring이 `ingredients`를 `menuId`로 오해하지 않게 고정 경로를 앞에 두고 menuId는 숫자 패턴만 허용.
- **수정 전략:** 요청에 자식 배열이 있으면 해당 관계만 교체. DTO equals 비교는 타입 차이로 위험해 제거.
- **삭제 전략:** hard delete 대신 `deleted_at`. 자식 행은 감사/복구용으로 유지하는 주석·마이그레이션 의도.
- **FE:** API 모듈 → 훅 → 패널/모달. 응답 실패 시 재료는 빈 배열로 떨어뜨려 UI 붕괴를 줄임.

데이터 흐름(수정):

1. Admin `MenuEditPanel` 저장 → `menusApi.updateMenu`
2. `PATCH /api/admin/menus/{id}` → `AdminMenuService.updateMenu`
3. menu 본문 update → (옵션) ingredients/options/nutrition/tags 교체 → detail 재조회 응답

## 5. AI 도움 영역

- 사용한 AI 도구: Cursor (co-authored-by)
- 요청: 관리자 메뉴 update/delete/ingredients, Bruno 정리, Admin FE API 연동, 깃반영
- AI 도움: 서비스·컨트롤러·FE 훅/패널 초안, Bruno 번호 재정렬 초안
- 사람이 남긴 부분: soft delete vs hard, 경로 순서, 완료를 E2E/DB와 분리해 기록, WBS DONE 미변경

## 6. 발생 이슈

### 이슈 1 — `ingredients` path 충돌

- 증상: `GET .../ingredients`가 menuId로 파싱될 수 있음.
- 해결: categories/ingredients를 `/{menuId}`보다 위, menuId에 `\\d+` 패턴.

### 이슈 2 — SQL 파일 ≠ DB 반영

- 증상: soft delete 컬럼 SQL이 저장소에만 있음.
- 해결: 워크로그에 미적용 명시. information_schema 확인 전 DONE 금지.

### 이슈 3 — FE 연동 ≠ 화면 검증

- 증상: API 함수·훅이 있어도 브라우저 저장 성공을 이 세션에서 보지 않음.
- 해결: 상태 = 코드·원격 반영. E2E는 내일 계획.

## 7. 디버깅 기록

| 확인 항목 | 이번에 확인한 사실 | 다음에 먼저 볼 곳 |
|---|---|---|
| back 커밋 | `73ab0f7` · merge `2afa10b` · origin 일치 | `AdminMenuService` · Bruno |
| Admin 커밋 | `0fd00f5` · merge `b6e93a7` · origin 일치 | `menusApi` · `useMenusQuery` |
| soft delete SQL | 파일 존재 | 실DB `menu.deleted_at` |
| Figma | 미확인 | Screen Bible / 승인 Frame |
| 테스트 | 퇴근 세션에서 `gradlew test`/브라우저 미실행 | 로컬 서버 + Admin 메뉴 관리 |

## 8. 이번 작업에서 배운 점

1. 관리자 REST에서 고정 세그먼트와 path variable 순서는 계약의 일부다.
2. 주문 FK가 있으면 soft delete를 먼저 문서·SQL·목록 필터(`deleted_at IS NULL`)까지 같이 적어야 한다.
3. FE API 연결 커밋만으로 “메뉴 관리 완료”를 쓰면 안 된다.

## 9. 개선사항 / TODO

- [ ] MySQL에 `2026-08-11_menu_soft_delete.sql` 적용 후 컬럼·인덱스 확인
- [ ] Bruno 또는 HTTP로 PATCH/DELETE/GET ingredients 응답 확인
- [ ] Admin 브라우저에서 생성·수정·삭제·재료 선택 E2E
- [ ] Figma SCR-016 등과 문구·상태 대조
- [ ] WBS-045 등은 DoD·검증 후에만 상태 갱신

## 10. 검증 내용

- 실행한 확인:
  - `git show --stat` / `HEAD == origin/main` (back·Admin)
  - 변경 파일·핵심 메서드 diff 대조
- 미실행:
  - `gradlew test`, 실서버 HTTP, 브라우저 E2E, 실DB ALTER, Figma

## 11. 포트폴리오 요약

관리자 메뉴를 soft delete와 자식 교체 수정 전략으로 백엔드에 올리고, Admin FE를 동일 계약의 create/update/delete/ingredients 호출로 연결했다. 원격 main 반영은 확인했으나 DB 적용과 화면 E2E는 명시적으로 남겼다.

## 12. 연결된 기록

- [일일 2026-08-11](../../daily/이하진/2026-08-11.md)
- [영양 시드 분리](2026-08-11-nutrition-seed-split.md)
