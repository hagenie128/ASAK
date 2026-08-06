# ASAK Doc Sync + DevCopilot Sync 근거 보고서

- 기준 시점: **2026-08-06**
- 작업공간: DevCopilot workspace **2** (`ASAK 키오스크 프로젝트`)
- 방식: MCP `user-devcopilot` 전수 조회 + 로컬 코드/문서 대조
- Git 자동 commit/push/merge: **하지 않음**
- 원격 쓰기: **이 보고서 작성 시점까지 미수행** (승인 대기)

## 1. 대상 저장소·기준 커밋

| 저장소 | 브랜치 | 비고 |
|---|---|---|
| `ASAK-back` | `main...origin/main` | 주문 상태 관련 unstaged 3파일. Admin Controllers는 트리에 존재 |
| `ASAK-Admin` | `main...origin/main` | working tree clean |
| `ASAK` (docs) | `main...origin/main` | planning 문서(08-05/08-06) 정본 |

최근 back 커밋 예: `4cc7b50 feat: 관리자 주문 상태 전이 및 취소 가드 구현`

## 2. DevCopilot 조회 범위 (전수)

MCP get_* 도구는 pagination 파라미터가 없고, 각 1회 호출로 목록이 반환됨.

| 범위 | 개수 | 판정 요약 |
|---|---|---|
| Wiki | — | **MCP 미지원** (Wiki 도구 없음) |
| 요구사항 | 56 | 상태 그대로 유지 권고. DONE로 자동 승격하지 않음 |
| WBS | 170 | EXCLUDED 98 / IN_PROGRESS 35 / TODO 19 / DONE 11 / BLOCKED 7. ARCHIVED·SUPERSEDED 보존 |
| API | 24 | Admin 경로·바디 계약 불일치 다수 → 결정 필요 |
| 시나리오 | 25 | DRAFT/ARCHIVED 유지. 본문 추정 수정 안 함 |
| QA | 16 | 전부 TODO. 실행 증거 없어 PASS 변경 안 함 |
| 화면 | 24 | WIREFRAME/ARCHIVED. SCR-009 명칭 불일치 → 결정 필요 |
| DB | 39 테이블 | 원격 ERD 덮어쓰기 안 함 (실제 DB 재검증 없음) |
| 버그 | 0 | 변경 없음 |

워크스페이스 통계(원격): req_rate 0%, wbs_rate 6.5%, qa_rate 0%, bugs 0

## 3. 코드로 확인한 구현 사실 (Admin)

| 기능 | 코드 근거 | 상태 |
|---|---|---|
| 주문 목록/상세/live/상태변경/cancel | `AdminOrderController` — `GET/`, `GET/{id}`, `GET/live`, `PATCH/{id}/{status}`, `PATCH/{id}/cancel` | **구현됨** (통합 검증은 미검증) |
| 메뉴 GET 목록·상세 | `AdminMenuController` GET 구현. POST/PATCH/DELETE는 TODO 주석 | **부분 구현** |
| 품절 | `AdminSoldOutController` 빈 클래스 + TODO-040 | **미구현(스텁)** |
| 결제수단 | `AdminPaymentMethodController` 빈 클래스 + TODO-044. path=`/api/admin/paymentMethods` | **미구현(스텁)** |
| 매출·대시보드 | `AdminStatsController` TODO-048~056만 | **미구현(스텁)** |

경로 코드 정본(현재 트리):

- Live: `GET /api/admin/orders/live` (DevCopilot API-021은 `/orders/active` → **계약 불일치**)
- 결제수단: `/api/admin/paymentMethods` (DevCopilot API-015/016은 `/payment-methods` → **계약 불일치**)
- 품절: `/api/admin/soldOut` + 계획 DTO `{targetType,targetId,isSoldOut}` (DevCopilot API-009 body는 `{menuId,isSoldOut}` → **계약 불일치**)

## 4. 로컬 문서 현황

| 문서 | 상태 |
|---|---|
| `docs/planning/admin-todo-checklist-2026-08-05.md` | 우선순위·TODO 번호 정합. 메뉴/품절/결제 미착수 표기와 코드 스텁 일치 |
| `docs/planning/admin-feature-verify-todos-2026-08-06.md` | 검증 투두. 경로·필드가 코드/Screen Bible 쪽과 대체로 일치 |
| `docs/wiki/project-flow.md` | 기준일 **2026-07-23**. Admin Live/주문 구현 이후 내용 미반영 → 갱신 후보 |
| `docs/wiki/rest-api-spec.md` | Admin 결제경로 kebab 등 혼재 → 결정 필요 |
| Product/Screen Bible Admin 구현 가이드 | UX·의도 정본. 코드와 다르면 조용히 덮지 않음 |

## 5. 갱신 후보 (승인 대기)

### A. 로컬 문서 (asak-doc-sync)

| # | 문서 | 제안 | 근거 | 권고 |
|---|---|---|---|---|
| A1 | `docs/wiki/project-flow.md` | 기준일을 2026-08-06으로 올리고 Admin 주문(Live·상태·취소) **구현됨·미검증**, 메뉴 GET **부분**, 품절/결제/매출 **스텁**으로 표시 | Controller 실측 | 승인 시 수정 |
| A2 | `docs/planning/admin-todo-checklist-2026-08-05.md` | 진행 로그에 「2026-08-06 문서·DevCopilot 점검」한 줄 추가. TODO 상태를 임의 완료 처리하지 않음 | 점검 사실만 | 승인 시 최소 수정 |
| A3 | `docs/planning/admin-feature-verify-todos-2026-08-06.md` | 진행 로그에 점검일·미검증 유지 기록 | 동일 | 승인 시 최소 수정 |
| A4 | `docs/wiki/rest-api-spec.md` | Admin path/body를 코드에 맞출지 명세에 맞출지 | **결정 필요** | 자동 수정 금지 |
| A5 | Product/Screen Bible | 경로·필드 의도 변경 | 코드와 충돌 시 **결정 필요** | 자동 수정 금지 |

### B. DevCopilot 원격 (asak-devcopilot-sync)

| # | 원격 ID | 현재 | 제안 | 판정 |
|---|---|---|---|---|
| B1 | API-021 `id=71` | `GET /api/admin/orders/active` | `.../orders/live`로 맞출지 | **계약 불일치 · 결정 필요** |
| B2 | API-015 `id=68`, API-016 `id=81` | `/payment-methods` | `/paymentMethods`로 맞출지 | **계약 불일치 · 결정 필요** |
| B3 | API-009 `id=212` | body `{menuId,isSoldOut}` | `{targetType,targetId,isSoldOut}`로 맞출지 | **계약 불일치 · 결정 필요** |
| B4 | SCR-009 | 이름「관리자 주문 관리」 | Screen Bible Live Board와 정렬할지 | **결정 필요** |
| B5 | WBS/요구사항/QA 상태 | IN_PROGRESS·TODO | DONE/PASS로 올리기 | **보류** (실행 검증 증거 없음) |
| B6 | Wiki | — | REST fallback 갱신 | **MCP 미지원** · 별도 승인+토큰/REST 필요 |
| B7 | DB 39테이블 | 원격 유지 | 덮어쓰기 | **보류** (실DB 미검증) |

## 6. 실행·검증 결과

- MCP `list_workspaces` / `get_workspace_details` / 8종 get_* : 성공
- Admin API 통합 테스트(HTTP)·DB 조회·Admin UI E2E: **미실행 → 미검증**
- 원격 update_*: **미실행**

## 7. 남은 불일치·결정 필요

1. Admin 결제수단 path: camelCase(`paymentMethods`) vs kebab(`payment-methods`)
2. Live 주문 path: `orders/live` vs `orders/active`
3. 품절 PATCH body: `targetType/targetId` vs `menuId`
4. SCR-009 역할/명칭 (Live vs 주문관리)
5. Wiki 최신화 수단 (MCP 없음)

## 8. 수정하지 않은 범위

- 소스코드, DB, Figma
- DevCopilot 원격 모든 항목 (쓰기 없음)
- Product Bible / Screen Bible 본문
- ARCHIVED DUPLICATE / SUPERSEDED WBS
- QA PASS 처리, 요구사항 DONE 처리

## 10. 승인 반영 결과 (2026-08-06 · A+B 코드기준)

사용자 승인: **A+B 코드기준**

### 로컬 문서 갱신

| ID | 파일 | 결과 |
|---|---|---|
| A1 | `docs/wiki/project-flow.md` | 기준일 2026-08-06, Admin 주문 API 연동·나머지 mock/스텁 반영 |
| A2 | `docs/planning/admin-todo-checklist-2026-08-05.md` | 진행 로그 1행 추가 (TODO 상태값 변경 없음) |
| A3 | `docs/planning/admin-feature-verify-todos-2026-08-06.md` | 진행 로그 점검일 기록 (검증칸 ⬜ 유지) |

### DevCopilot 원격 갱신 + 재조회

| ID | 원격 | 변경 전 | 변경 후 | 재조회 |
|---|---|---|---|---|
| B1 | API-021 `id=71` | `/api/admin/orders/active` | `/api/admin/orders/live` | 반영 확인 |
| B2 | API-015 `id=68` | `/api/admin/payment-methods` | `/api/admin/paymentMethods` | 반영 확인 |
| B3 | API-016 `id=81` | `/api/admin/payment-methods/{methodId}` | `/api/admin/paymentMethods/{methodId}` | 반영 확인 |
| B3b | API-009 `id=212` | body `{menuId,isSoldOut}` | `{targetType,targetId,isSoldOut}` | 반영 확인 |

### 여전히 미수정 / 잔여

- Wiki 원격 REST: `DEVCOPILOT_TOKEN` 미설정 → **미업로드**. 로컬 `rest-api-spec.md`·`project-flow.md`만 갱신됨. 토큰 설정 후 `asak-data/scripts/upload_wiki.py`로 wiki/12 등 upsert 가능.
- WBS/QA 상태 승격: 실행 검증 증거 없음 → **보류 유지**
- Product Bible 본문(업무 규칙) 대량 수정: 하지 않음. Screen Bible은 SCR-009·Registry 라우트만 코드 정렬.
- 소스코드 / Git commit·push: 미수행

자동 Git 작업은 수행하지 않음.

## 11. 잔여 항목 추가 반영 (2026-08-06 이어짐)

| 항목 | 결과 |
|---|---|
| `rest-api-spec.md` | Admin soldOut·paymentMethods·Live/cancel 주석 코드 기준 반영 |
| SCR-009 Screen Bible | Route `/`+alias, 컴포넌트 `LiveOrderPreview`, cancel API 명시 |
| SCREEN_REGISTRY | SCR-009=`/`, SCR-022=`/dashboard`, sold-out/payment-methods 코드 경로 |
| DevCopilot SCR-009 | 명칭 → `관리자 Live 주문 보드 (LMIS-ORDER-001)` (재조회 확인) |
| Wiki 원격 | MCP 미지원 + `DEVCOPILOT_TOKEN` 없음 → 미업로드 |
| WBS/QA 승격 | 하지 않음 |

## 12. Wiki REST 업로드 (2026-08-06)

- 방식: `MCP 아닌 REST fallback` (PUT `/api/workspaces/2/wikis/12`)
- 대상: **wiki/12** `ASAK REST API 명세서` ← 로컬 `docs/wiki/rest-api-spec.md`
- 재조회(목록 API): `soldOut`·`paymentMethods`·`orders/live` 포함 확인, 구 `sold-out-items` 없음
- URL: https://devcopilot.ai.kr/workspace/2/wiki/12
- 토큰·자격 증명은 보고서·파일에 기록하지 않음
- `project-flow.md` 원격 Wiki 페이지는 기존 ID 매핑 없음 → 별도 승인 시 생성/업로드


