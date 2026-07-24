# ASAK DB 뷰(View) 정의서

> 기준일: 2026-07-24 · 실DB `asak_db` · DDL/주석 원본: [`ASAK-back/docs/view.sql`](https://github.com/nayeon0828/ASAK-backend/blob/main/docs/view.sql)  
> DevCopilot ERD(워크스페이스 2)와 동기화. 매출 4종은 `asak-data/scripts/create_sales_views_mysql.py` 원본.
>
> 2026-07-24 확인: 저장소 안 로컬 스냅샷(`devcopilot-db-live-2026-07-22.json`)은 short-name 마이그레이션 이전 기록이라 오래됐지만, 실제 DevCopilot 허브(workspace 2)는 이미 short-name·`canceled_at`/`refunded_at` 전부 최신 상태로 확인됨. 로컬 스냅샷 파일만 오래된 것이고 허브 자체는 문제없음.

뷰는 **읽기 전용 읽기 모델(read model)** 이다. 앱/API는 조인·집계·품절 판정을 뷰에 맡기고, 쓰기(INSERT/UPDATE)는 베이스 테이블만 사용한다.

## 용도별 요약

| 그룹 | 뷰 | 주요 소비자 |
|------|-----|-------------|
| 메뉴 옵션/재료 | `vw_menu_opt_resolved`, `vw_menu_opt_policy_json`, `vw_menu_ing_detail`, `vw_menu_ing_json` | 메뉴 상세 API |
| 메뉴 목록/품절 | `vw_menu_availability`, `vw_menu_list`, `vw_soldout_catalog` | 메뉴 목록·품절 관리 |
| 주문 상세 | `vw_order_item_*`, `vw_order_summary`, `vw_order_list_summary`, `vw_order_live` | 관리자 주문·주방 보드 |
| 주문 집계 | `vw_order_status_summary` | 대시보드 |
| 결제 | `vw_payment_result` | 결제 승인 API |
| 매출 | `vw_sales_daily`, `vw_sales_hourly`, `vw_top_menu_daily`, `vw_top_menu_hourly` | 관리자 매출 API |

품절관리 "영향 메뉴 개수" 미리보기와 결제수단 목록은 뷰가 아니라 파라미터 있는 매퍼 인라인 쿼리 —
`view.sql` [17]·[18]번 참고.

## JSON 묶음 (`JSON_ARRAYAGG`)

부모 1행에 자식 N행을 붙일 때 JOIN만 하면 행이 폭발(fan-out)한다.  
`JSON_OBJECT`로 한 행을 객체로 만들고 `JSON_ARRAYAGG`로 배열 컬럼 1개에 합친다.  
자식 0건이면 `NULL` → 필요 시 `COALESCE(..., JSON_ARRAY())`로 `[]` 처리.

---

## 1. 메뉴·옵션

### `vw_menu_opt_resolved`
메뉴–옵션정책–옵션항목을 **행 단위로 펼친** 뷰. `menu_opt_override`가 있으면 정책 기본값보다 메뉴 오버라이드 우선(`COALESCE`).

| 컬럼 | 타입 | 설명 |
|------|------|------|
| menu_id | BIGINT | 메뉴 ID |
| policy_id | BIGINT | 옵션 정책 ID |
| policy_name | VARCHAR | 정책명 |
| min_select / max_select | INT | 최소·최대 선택 수 |
| policy_required | TINYINT | 정책 필수 여부 |
| opt_item_id / opt_item_name | — | 옵션 항목 |
| add_price | INT | 추가 금액 |
| opt_item_sold_out | TINYINT | 옵션 품절 |
| recommended / is_default / sort_no / active | — | 오버라이드 병합 결과 |

### `vw_menu_opt_policy_json`
정책당 1행(`option_group_id`, `name`). 옵션 항목을 `items` JSON 배열로 묶음. `group_type`, `select_type`(SINGLE/MULTI), 영양·아이콘 필드 포함.
2026-07-24: 필드명을 `rest-api-spec.md` API-004 계약에 맞춤 (`optId→optionItemId`, `addPrice→extraPrice`, `listPrice→originalPrice`, `amount→servingAmount`, `unitId→servingUnit`).

| 컬럼 | 설명 |
|------|------|
| items | JSON 배열. optionItemId, ingredientId, name, extraPrice, originalPrice, servingAmount, servingUnit, iconUrl, colorHex, isSoldOut, extraKcal, proteinG, isRecommended, isDefault 등 |

### `vw_menu_ing_detail`
메뉴 재료 + 알레르기. 알레르기 N개면 재료 행이 N줄로 늘어날 수 있음.

### `vw_menu_ing_json`
재료당 1행(`ingredient_id`). 알레르기를 `allergens` JSON 배열로 묶어 fan-out 방지. `role`은 코드 소문자(core/base/default), `unit`은 표시 코드(g/ml/개)로 노출.
2026-07-24: 프론트 실제 필드명에 맞춤 (`ing_id→ingredient_id`, `role_id→role`, `unit_id→unit`).

메뉴 상세 헤더의 `allergens`(메뉴 레벨, 재료+옵션 통합 중복제거)와 `allergyText`(합쳐진 문자열, API-003 계약)는 이 뷰가 아니라 헤더 조회 SQL에 서브쿼리로 붙는다 — `view.sql` [15]번 참고.

---

## 2. 메뉴 목록·품절

### `vw_menu_availability`
메뉴별 품절 판정 플래그.

| 컬럼 | 의미 |
|------|------|
| direct_sold_out | 메뉴 자체 품절 |
| has_core_sold_out | CORE 재료 품절 → 무조건 품절 |
| base_ing_exhausted | BASE 재료(고정형) 전부 품절 |
| base_opt_exhausted | BASE 옵션그룹 선택 가능 옵션 0 |
| has_blocking_standard | DEFAULT 재료 품절 + 제거 불가 |
| has_exhausted_required_group | 필수 옵션그룹이 min_select 미충족 |

### `vw_menu_list`
목록용(`category_id`). `vw_menu_availability`를 합쳐 `is_orderable`, `has_sold_out_ingredient` 산출.
2026-07-24: `cat_id→category_id` (`MENU_API_CONTRACT.md`: "Use categoryId").

### `vw_soldout_catalog`
메뉴/재료/옵션아이템 UNION. 품절 관리 화면용 (`target_type`: MENU | INGREDIENT | OPTION_ITEM).

---

## 3. 주문

### `vw_order_item_detail`
주문번호 + 메뉴명 + 수량·가격.

### `vw_order_item_option` / `vw_order_item_exclusion`
정규화 행 단위 옵션·제외재료.

### `vw_order_item_full`
주문라인 1행(`unit_price`) + `option_items`/`excluded_ingredients` JSON 배열. 품목 id 컬럼 없음(계약에 없어서 제거).
2026-07-24: Admin `OrderDetailPanel.jsx` / `rest-api-spec.md` API-007 실제 필드명에 맞춤 (`options→optionItems`, `exclusions→excludedIngredients`, `optItemId→optionItemId`, `ingId→ingredientId`, `price→unitPrice`, `order_item_id` 컬럼 삭제).

### `vw_order_item_base_dressing`
BASE/DRESSING을 컬럼으로 pivot (`base_name`, `dressing_name`).

### `vw_order_item_tag`
나머지 옵션·제외재료. `tone`: side / drink / plus / exclude (UI 태그용).

### `vw_order_summary`
주문 + 유형/상태/결제 코드명 + 결제수단.

### `vw_order_list_summary`
목록 한 줄. `menu_summary` = `"메뉴명"` 또는 `"메뉴명 외 N"`.

### `vw_order_live`
실시간 보드. `elapsed_sec` = 생성 후 경과 초.

### `vw_order_status_summary`
일자 × 주문유형 × 상태별 건수.

---

## 3-1. 결제

### `vw_payment_result`
결제 승인 응답용 (`PAYMENT_API_CONTRACT.md`: paymentId, orderId, orderNo, paymentStatus, approvedAmount, waitingOrderCount, approvedAt).
`waiting_order_count`는 상관 서브쿼리로 조회 시점마다 재계산 — 결제 시점이 아니라 "지금" 대기 건수.

---

## 4. 매출 (별도 DDL)

원본: `asak-data/scripts/create_sales_views_mysql.py`

| 뷰 | 설명 |
|----|------|
| `vw_sales_daily` | 일자별 승인/취소/순매출 |
| `vw_sales_hourly` | 일자·시간대별 매출 |
| `vw_top_menu_daily` | 일자별 인기 메뉴 |
| `vw_top_menu_hourly` | 시간대별 인기 메뉴 |

---

## 관련 문서

- 테이블 정의: [db-table-definition.md](./db-table-definition.md)
- 백엔드 뷰 SQL: `ASAK-back/docs/view.sql`
- DevCopilot 동기화: `asak-data/scripts/sync_devcopilot_views.py`
