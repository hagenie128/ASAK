# 2026-08-06 관리자 메뉴 검색 흐름 및 상세 응답 정리

> 일일 기록: [2026-08-06.md](../../daily/이하진/2026-08-06.md)
> 기준 화면: [SCR-016](../../../docs/product_bible/07_Screen_Bible/SCR-016-ADMIN-MENU-MANAGEMENT.md)

---

## 1. 기본 정보

- 작업 일자: 2026-08-06
- 담당자: 이하진 (`hagenie128` Git 사용자 매핑 기준)
- 저장소: ASAK / ASAK-Admin / ASAK-back
- 반영 이력: `bf72b3c`(Admin 검색 입력 흐름과 TODO 순서 정리), `a09faa6`(backend 메뉴 상세 응답과 TODO 순서 정리), 참고 `69d2b89`·`8ac8b39`(같은 브랜치의 이전 메뉴 관리 기반 작업)
- 관련 화면/계약: SCR-016 관리자 메뉴 관리, `GET /api/admin/menus`, `GET /api/admin/menus/{menuId}`, `GET /api/admin/menus/categories`
- 작업 유형: `fix`
- 완료 판정: Admin/Backend 커밋과 현재 코드, backend `bootRun` 성공 로그는 확인했다. Admin dev server는 HMR 로그만 확인했으며, 실제 메뉴 조회 HTTP 응답, 브라우저 회귀, 등록/수정/삭제 저장 동작은 확인하지 않았다.

## 2. 작업 목적

- 메뉴 관리 화면에서 검색 입력 중간값과 실제 조회 keyword를 분리해 페이지 리셋과 검색 적용 시점을 명확히 한다.
- 메뉴 선택 상태와 상세 패널 전환이 create/edit/view 모드에서 덜 흔들리도록 정리한다.
- backend 메뉴 상세 응답이 옵션 그룹 추천 라벨, 태그, 카테고리 정보까지 화면이 그대로 읽을 수 있는 형태를 안정적으로 제공하도록 맞춘다.

## 3. 대상 저장소와 변경 범위

### ASAK-Admin

- `src/pages/admin/MenuManagePage.jsx`
- `src/components/admin/MenuDetailPanel.jsx`
- `src/components/admin/MenuEditPanel.jsx`
- `src/components/admin/MenuListPanel.jsx`
- `src/api/menusApi.js`
- `src/api/paymentMethodsApi.js`
- `src/api/soldOutApi.js`
- `src/hooks/usePaymentMethodDraft.js`
- `src/hooks/useSoldOutDraft.js`

### ASAK-back

- `src/main/java/com/asak/admin/controller/AdminMenuController.java`
- `src/main/java/com/asak/admin/service/AdminMenuService.java`
- `src/main/java/com/asak/admin/mapper/AdminMenuMapper.java`
- `src/main/java/com/asak/admin/dto/response/MenuOptionGroupSummaryResponse.java`
- `src/main/resources/mappers/AdminMenuMapper.xml`
- `src/main/java/com/asak/admin/controller/AdminSoldOutController.java`
- `src/main/java/com/asak/admin/controller/AdminPaymentMethodController.java`
- `src/main/resources/mappers/AdminSoldOutMapper.xml`
- `src/main/resources/mappers/AdminPaymentMethodMapper.xml`

## 4. 직접 구현 영역

### Admin 검색·선택 흐름

- 검색 input의 draft 상태와 실제 조회 keyword를 분리하고, submit 또는 clear 시점에만 `onKeywordChange()`와 `onPageChange(0)`가 호출되도록 정리했다.
- 메뉴 생성 진입 시 목록 페이지를 0으로 되돌리고, 메뉴 선택 시 상세 보기 모드로 복귀하도록 흐름을 정리했다.
- 상세 패널에서 재료 수량/단위 문자열을 별도 함수로 정리하고, 옵션 그룹 필수 여부와 추천 라벨 표기를 읽기 쉬운 형태로 맞췄다.

### Backend 메뉴 상세 응답 정리

- 메뉴 상세 조회에서 옵션 그룹 응답에 `recommendedLabel`을 포함하도록 DTO와 MyBatis 질의를 맞췄다.
- 카테고리 목록 응답과 운영 API TODO 주석의 이름/순서를 정리해 프론트와 백엔드에서 다음 저장 슬라이스를 이어가기 쉽게 맞췄다.
- 같은 날짜의 이전 커밋 범위와 연결해 메뉴 목록, 카테고리, 상세 응답 계약을 한 브랜치 안에서 정리했다.

## 5. 구현 로직 / 데이터 흐름

### 메뉴 검색 적용 흐름

1. `MenuManagePage`가 `draftKeyword`를 별도 상태로 가진다.
2. 사용자가 입력 중일 때는 `draftKeyword`만 바뀌고, 기존 조회 keyword는 유지된다.
3. submit 시점에만 `onKeywordChange(draftKeyword)`와 `onPageChange(0)`가 호출된다.
4. 입력을 모두 지운 경우에는 즉시 keyword를 빈 문자열로 되돌리고 첫 페이지로 복귀한다.

### 메뉴 상세 읽기 흐름

1. 메뉴 목록에서 선택된 `selectedMenuId`가 `useMenusQuery()`를 통해 상세 데이터와 연결된다.
2. `MenuDetailPanel`은 `ingredients`, `optionGroups`, `nutrition`, `allergens`, `tags`를 화면 섹션별로 분리해 렌더링한다.
3. backend `AdminMenuMapper.xml`은 `vw_menu_opt_policy_json`, `menu_tag`, 알레르기 조합 조회로 상세 응답을 구성한다.
4. 옵션 그룹의 추천 항목은 `policy.items` JSON에서 `is_recommended = 1`인 항목 이름을 추출해 `recommendedLabel`로 내려준다.

## 6. 커밋과 브랜치

### ASAK-Admin

- 브랜치: `fix/admin-search-and-todo-flow`
- 확인한 커밋
  - `bf72b3c` `fix: 관리자 검색 입력 흐름과 TODO 순서 정리`
  - `69d2b89` `fix: 관리자 메뉴 관리 선택과 페이지네이션 정리`
  - `15d2092` `chore: 관리자 인라인 TODO를 교사 우선순위로 재번호`

### ASAK-back

- 브랜치: `fix/admin-search-and-todo-flow`
- 확인한 커밋
  - `a09faa6` `fix: 관리자 메뉴 상세 응답과 TODO 순서 정리`
  - `8ac8b39` `fix: 관리자 메뉴 조회와 운영 API 정리`
  - `7bfa0f0` `chore: 관리자 인라인 TODO를 교사 우선순위로 재번호`

상위 워크스페이스 `ASAK-workspace`는 여러 하위 저장소 포인터와 보조 파일이 함께 바뀌어 있어, 오늘 기능 기록의 정본 근거로 쓰지 않았다.

## 7. 실행한 검증

| 구분 | 실행/확인 | 결과 | 검증하지 못한 범위 |
|---|---|---|---|
| Git 이력 | `ASAK-Admin`, `ASAK-back`의 2026-08-06 커밋 로그와 변경 파일 통계 확인 | 위 커밋들이 같은 브랜치에서 메뉴 관리 흐름과 응답 정리를 수행한 근거 확인 | 원격 PR/CI, 코드리뷰 상태 |
| Backend 실행 | `ASAK-back` 터미널에서 `.\gradlew bootRun` 로그 확인 | 18:19에 Tomcat 8080 기동 성공, Spring context 시작 완료 | 메뉴 API 실호출, DB 결과 정합 |
| Admin 실행 | `ASAK-Admin` 터미널에서 `npm run dev` HMR 로그 확인 | dev server는 동작 중이며 수정 파일 HMR 기록 확인 | 브라우저 실제 렌더링, 저장/삭제 버튼 동작 |
| Admin 오류 로그 | 같은 dev server 로그에서 `MenuDetailPanel` parse error 이력과 이후 `public` 자산 import 경고 확인 | 문법 오류는 수정된 것으로 보이나 `public` 자산 import 경고가 남아 있음 | 현재 최신 화면에서 경고가 사용자 흐름에 미치는 영향 |

이 작업에서는 lint, build, Bruno 호출, DB 조회, Figma 대조를 실행한 근거를 찾지 못했으므로 성공으로 기록하지 않았다.

## 8. AI 또는 도구 도움 범위

- 사용한 도구: Codex, 로컬 shell, 파일 읽기 도구
- 요청 범위: Git 이력, 현재 코드, 실행 중 터미널 로그를 대조해 퇴근용 일일/상세 워크로그 작성
- AI가 제공한 내용: 커밋과 코드 근거 정리, 검증/미검증 구분, 기록 문안 정리
- 사람이 결정·확인한 부분: 실제 소스 구현, 브랜치 운용, 오늘 커밋 범위
- AI가 직접 구현하거나 변경한 범위: 소스코드·DB·원격 Git 변경 없음. 워크로그 문서만 작성

## 9. 이슈와 판단

### 이슈 1 — Admin 현재 워킹트리와 오늘 커밋 범위가 분리되어 있음

- `ASAK-Admin` 현재 상태에는 9개 미커밋 파일이 남아 있다.
- 오늘 18:28 커밋 이후의 추가 수정이 섞여 있어, 다음 commit/push 전에 오늘 기록 범위와 새 변경 범위를 다시 분리할 필요가 있다.
- 이 문서에는 확인 가능한 커밋과 현재 파일 상태만 기록하고, 미커밋 변경을 완료 작업으로 과장하지 않았다.

### 이슈 2 — 메뉴 상세 패널 관련 dev server 경고가 남아 있음

- dev server 로그에는 `MenuDetailPanel.jsx` parse error 이력이 있고, 이후 `public` 디렉터리 자산 import 경고가 남아 있다.
- 현재 파일은 문법상 읽히지만, 실제 브라우저에서 경고가 해결됐는지는 확인하지 않았다.
- 따라서 메뉴 상세 패널의 시각 회귀나 asset 로딩 정상 여부는 미검증으로 남긴다.

### 이슈 3 — 저장 동작은 TODO 정리 단계

- `menusApi.js`와 `MenuManagePage.jsx`에는 등록/수정/삭제 저장 연결 TODO가 남아 있다.
- 이번 작업의 핵심은 검색-선택-상세 읽기 흐름과 응답 shape 정리이며, 저장 성공/실패 시나리오는 구현 완료로 기록하지 않는다.

## 10. 남은 위험

- 프론트 검색 흐름이 정리됐더라도 실제 `GET /api/admin/menus` 응답 shape가 다르면 pagination·selection이 깨질 수 있다.
- 메뉴 상세 응답의 `recommendedLabel`, 태그, 알레르기 구조가 화면 mock과 일치해도 실데이터에서 null/빈 배열 케이스를 아직 검증하지 않았다.
- `ASAK-Kiosk`의 대량 이미지 변경과 `ASAK-Admin`의 현재 미커밋 변경이 이후 상위 워크스페이스 상태와 섞이면 퇴근 후 추적성이 떨어질 수 있다.

## 11. 다음 작업

- `ASAK-Admin` 현재 워킹트리에서 `MenuDetailPanel` 관련 자산 import 경고를 정리한다.
- 브라우저에서 메뉴 검색, 페이지 이동, 메뉴 선택, 상세 패널 렌더링을 실제로 확인한다.
- `GET /api/admin/menus`, `GET /api/admin/menus/{menuId}`, `GET /api/admin/menus/categories`를 HTTP로 호출해 프론트 기대 shape와 일치하는지 검증한다.
- 저장 TODO 슬라이스는 create/update/delete API 계약 확정 후 별도 작업으로 이어간다.

## 12. 포트폴리오용 요약

- 관리자 메뉴 관리 화면에서 검색 입력 상태와 실제 조회 시점을 분리해 UX 흔들림을 줄이고, 선택-상세 읽기 흐름을 더 안정적으로 정리했다.
- 같은 날 backend 메뉴 상세 응답의 옵션 그룹 추천 라벨과 운영 API 정리를 함께 반영해, 프론트 화면 요구와 서버 응답 shape를 한 브랜치에서 정렬했다.
