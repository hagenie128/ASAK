# ASAK 문서 동기화 — API·위키 최신화 (2026-08-18)

- 범위: 로컬 API/운영 위키를 현재 코드 기준으로 맞춘 뒤 Hub workspace 2에 반영
- Git commit/push: **미수행**
- 토큰·자격 증명은 본 문서에 기록하지 않음

## 대상 저장소와 기준 커밋

| 저장소 | HEAD (short) |
|---|---|
| ASAK | `1a6426d` |
| ASAK-back | `467a9c9` |
| ASAK-Admin | `e6286db` |
| ASAK-Kiosk | `90e3f15` |

작업 트리의 미커밋 문서 변경은 이 동기화에서 추가로 수정했다. HEAD만으로 문서가 이미 반영된 상태는 아니다.

## 확인한 코드·문서

- Controller: `HealthController`, `UserMenuController`, `UserOrderController`, `UserPayController`, `AdminOrderController`, `AdminMenuController`, `AdminOptionController`, 스텁 `AdminSoldOutController`/`AdminPaymentMethodController`/`AdminStatsController`/`AdminAuthController`
- DTO: `CreateMenuRequest`, `MenuDetailResponse`, `MenuListRequest`/`MenuListResponse`, `OptionGroupSummaryResponse`, `AdminCategoryResponse`, `IngredientResponse`, `PaymentMethodResponse`, `PageResult`
- Kiosk: `API_ENDPOINTS.payments = "/payments"`, `PaymentPage`→API-014, `PaymentProcessingPage`→`createOrder`만 (approvePayment 미호출)
- Admin: `menusApi` 목록/상세/등록/수정/삭제/카테고리/재료 호출
- Bruno: `ASAK-back/api/README.md`

## 갱신한 로컬 문서

| 파일 | 변경 |
|---|---|
| `docs/wiki/rest-api-spec.md` | CURRENT. `/api/kiosk/**`·`/api/admin/**` 정본. 구현/스텁/미구현 분리. Hub 신규 ID 430~435 |
| `docs/wiki/index.md` | REST 명세를 CURRENT로 표기 |
| `docs/wiki/meeting-minutes-weekly.md` | 기간~08-18, 8/18 스냅샷 추가 |
| `docs/wiki/worklog-index.md` | 기간 W33~W34 |
| `docs/wiki/meeting-deliverables-checklist.md` | W33/W34 행, Hub 링크 |
| `docs/wiki/project-flow.md` | 8/18 헤더, 결제·메뉴 코드 연결 반영 |
| `docs/wiki/current-status-baseline.md` | HISTORY 위에 8/18 overlay |
| `docs/operations/meeting-minutes/README.md` | 8/18 일정 표는 유지, 8/07 스냅샷 안내 |
| `ASAK-back/api/README.md` | 옵션 그룹 Controller 존재, 레거시 path 폐기 |
| `asak-data/scripts/upload_wiki.py` | `--list` 추가 |

## 변경 근거

- 구현 사실: Controller 메서드 존재 여부
- 클라이언트 연결: 실제 import/호출. 연결 ≠ HTTP E2E
- 스텁: `@RequestMapping`만 있는 클래스

## 실행 또는 검증 결과

- `git diff --check` on 수정 문서: 문제 없음
- Bruno/브라우저 E2E: **미실행**. health 외 성공 assert 없음

## 남은 불일치 · 결정 필요

1. **계약 불일치:** Kiosk `POST /payments` vs 서버 `POST /api/kiosk/payments`
2. **미연결:** 결제 승인 API는 서버에 있으나 `PaymentProcessingPage`는 타이머 mock
3. **결정 필요:** 결제수단 정본 3종 vs DTO `TOSS_PAY`. Admin PATCH `isActive` vs 예전 Hub `isEnabled`. RTOS `device_event`는 코드 없음. API-019은 월별 매출이지 영수증 출력이 아님
4. **미검증:** Admin 메뉴 CRUD·주문 API HTTP/브라우저 E2E

## 수정하지 않은 범위

- 소스코드, DB, Figma
- Product Bible 본문, HISTORY Notion export (`requirements-definition.md` 등)
- Hub 요구사항·WBS 카드·QA·화면·DB ERD 상태값
- Git commit/push
