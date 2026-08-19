# 스키마 문서 실측 동기화 — 테이블 26개 · 뷰 22개

> 작성일: 2026-08-19
> 대상: `ASAK-back/docs`, `ASAK/docs/wiki`
> 기준: 운영 DB `asak_db`(`nam3324.synology.me:33338`)의 `SHOW CREATE TABLE` / `SHOW CREATE VIEW` 실측
> 상태: **테이블 문서 갱신 완료 · 뷰 문서 검증 완료(수정 불필요) · 중앙 wiki 갱신 완료 · 결정 필요 2건**

## 1. 왜 했나

2026-08-19 주문 데이터 작업 중 `ASAK-back/docs/아삭_mysql.sql` 이 실제 DB와 어긋난 것이 드러났다.
문서만 보고 `payment` 에 INSERT 하면 다음으로 실패했다.

```text
Field 'idempotency_key' doesn't have a default value
```

문서에 없는 `NOT NULL` 컬럼이 실제로는 있었기 때문이다. 다른 항목도 믿을 수 없다고 판단해
전체를 실측과 대조했다.

## 2. 확인 방법

Python + pymysql 로 운영 DB에 **읽기 전용** 접속해 `SHOW CREATE TABLE`, `SHOW CREATE VIEW`,
`information_schema` 를 조회했다. 스키마는 변경하지 않았다. 이 PC에 mysql CLI 는 없다.

재현·재검증 도구를 `ASAK-back/docs/tools/schema_sync.py` 로 남겼다.

```bash
python docs/tools/schema_sync.py all
```

`SELECT` / `SHOW` / `DESCRIBE` / `EXPLAIN` 외의 SQL 은 실행 전에 막는다.

## 3. 확인한 사실

### 테이블 — 문서가 크게 어긋나 있었다

실제 운영 테이블은 **26개**다. 이와 별개로 `backup_*` / `*_backup_*` 일회성 백업 테이블이
22개 있으나 스키마 문서 대상이 아니다.

기존 `아삭_mysql.sql`(25개 기재) 과의 차이는 240여 건이었다.

| 유형 | 건수 | 대표 사례 |
|---|---|---|
| 테이블 통째 누락 | 1 | `media_asset` |
| 컬럼 누락 | 8 | `payment.idempotency_key`, `menu.image_asset_id`, `ing.kcal`/`protein_g`/`icon_asset_id`/`photo_asset_id`, `pay_method_cfg.image_asset_id`/`description` |
| AUTO_INCREMENT 누락 | 25 | `ing_nutr` 외 전 테이블 |
| DEFAULT 누락 | 40여 | `total_price` DEFAULT 0, `created_at` DEFAULT CURRENT_TIMESTAMP, `updated_at` ON UPDATE |
| UNIQUE 누락 | 20 | `orders.order_no`, `payment.order_id`, `payment.idempotency_key` |
| 일반 INDEX 누락 | 26 | `idx_orders_status_created_at`, `idx_menu_deleted_at` |
| FK 이름 불일치 | 46 (전부) | 문서 `fk_menu_cat_id` / 실제 `fk_menu_category` |
| 컬럼 순서 뒤섞임 | 21 테이블 | — |

FK 는 46개 **전부** 이름이 달랐다. 문서 이름으로 `ALTER TABLE ... DROP FOREIGN KEY` 를 하면
하나도 듣지 않는다.

전체 내역: `ASAK-back/docs/2026-08-19_schema_doc_drift.md`

### 뷰 — 문서가 맞았다

`ASAK-back/docs/view.sql` 은 어긋나지 않았다. 뷰 22개가 존재·정의 모두 실제와 일치했다.

- 20개는 정의가 토큰 단위까지 같았다.
- `vw_menu_list`, `vw_menu_opt_policy_json` 2개는 MySQL 이 조인 트리에 붙이는 중첩 괄호를
  `view.sql` 이 가독성 때문에 생략한 표기 차이뿐이었다. 추론에 맡기지 않고 실제 뷰와 문서 SQL 을
  각각 실행해 행 수(72 / 324), 전체 행 체크섬(`BIT_XOR(CRC32)` + `SUM(CRC32)`), 컬럼 이름·순서가
  모두 같음을 확인했다.
- 22개 모두 정상 조회되고 `backup_*` 테이블을 참조하는 뷰는 없다.

### 레거시 테이블 이름 대응

중앙 wiki 가 short-name 마이그레이션 이전 이름을 쓰고 있었다. 대응은 추정이 아니라
**실제 FK 제약 이름이 옛 테이블명을 보존하고 있는 것**을 근거로 확정했다.

| 이전 이름 | 실제 | 근거 FK |
|---|---|---|
| `ingredient` | `ing` | `fk_ingredient_type` |
| `ingredient_allergen` | `ing_allergen` | `fk_ingredient_allergen_ingredient` |
| `menu_ingredient` | `menu_ing` | `fk_menu_ingredient_menu` |
| `menu_nutrition` | `menu_nutr` | `fk_menu_nutrition_menu` |
| `option_group` | `opt_group` | `fk_option_group_type` |
| `option_item` | `opt_item` | `fk_option_item_group` |
| `option_item_component` | `opt_item_comp` | `fk_option_item_component_item` |
| `payment_method_config` | `pay_method_cfg` | `fk_payment_method_config_method` |
| `menu_option_policy` | `menu_opt_policy` | `fk_menu_option_policy_menu` |

`ing_nutr`, `media_asset` 은 FK 이름도 short-name 이라 마이그레이션 이후 신규 생성으로 보인다.

### 결제 멱등성 키

`payment.idempotency_key` 는 `VARCHAR(64) NOT NULL UNIQUE`, DB 기본값 없음.

- `ApprovePaymentRequest.idempotencyKey` 로 요청마다 클라이언트가 UUID 를 보낸다.
- `UserPayService` 가 null·blank 면 `INVALID_ORDER_REQUEST`,
  같은 키인데 `order_id` 나 결제수단이 다르면 `IDEMPOTENCY_KEY_CONFLICT`(409) 로 거절한다
  (`validateSameRequest`).
- 네트워크 단절 후 재시도가 와도 UNIQUE 제약이 중복 결제 행을 막는다.

## 4. 갱신한 문서

| 저장소 | 문서 | 변경 | 상태 |
|---|---|---|---|
| ASAK-back | `docs/아삭_mysql.sql` | 실측 DDL 로 전면 재생성 (테이블 26개, FK 46개) | 구현됨 |
| ASAK-back | `docs/view.sql` | 내용 변경 없음. 헤더에 검증 방법·결과·DEFINER 주의 기록 | 검증됨 |
| ASAK-back | `docs/2026-08-19_schema_doc_drift.md` | 테이블·뷰 대조 내역 신규 | 신규 |
| ASAK-back | `docs/tools/schema_sync.py`, `README.md` | 재동기화 도구 신규 | 신규 |
| ASAK-back | `docs/implementation_guide/04-api-db-implementation.md` | 필드 매핑에 `idempotency_key`·`image_asset_id` 추가, DB 정책 4항목 추가, 정본 링크 추가 | 구현됨 |
| ASAK | `docs/wiki/db-table-definition.md` | 22테이블·레거시 이름 → 26테이블 실측 기준. ERD 재작성, 이전 이름 열 추가 | 구현됨 |
| ASAK | `docs/wiki/db-view-definition.md` | 헤더에 2026-08-19 실측 검증 결과 추가 | 검증됨 |
| ASAK | `docs/wiki/requirements-definition.md` | FWD-MENU-015 의 `menu_option.is_recommended` 에 현재 위치 주석 병기 (원문 보존) | 구현됨 |
| ASAK | `docs/wiki/screen-design-figma.md` | 274행 "추천 드레싱은 menu_option 기준" 에 주석 병기 (원문 보존) | 구현됨 |

`ASAK-back/docs/MENU_IMAGE_ASSET_FLOW.md` 는 확인 결과 `media_asset` 구조와 FK 이름이
실측과 정확히 일치해 수정하지 않았다.

## 5. 검증 결과

실제로 실행한 것만 적는다.

```text
python docs/tools/schema_sync.py verify
[테이블] 문서를 SHOW CREATE 형태로 되돌려 실제와 비교
  결과: 완전 일치 (테이블 26개)
[뷰] 정의 토큰 비교
  결과: 일치 20개 / 표기 차이 2개
[뷰] 표기가 다른 뷰는 실제로 실행해 결과가 같은지 확인
  OK  vw_menu_list — 행 72/72, 체크섬 동일
  OK  vw_menu_opt_policy_json — 행 324/324, 체크섬 동일
최종: 문서가 실제와 일치한다
```

`git diff --check` 공백 오류 없음. 04 문서에서 추가·수정한 상대 링크 8개 대상 존재 확인.

API 실행 검증, 화면 검증은 하지 않았다. 이번 범위는 문서와 DB 스키마 대조다.

## 6. 2차 작업 — 결정 필요 3건 후속 처리

1차에서 남긴 3건을 이어서 처리했다.

### (1) 레거시 `menu_option` / `menu_option_group` — 해결

요구사항 정의서와 뷰 SQL 에 근거가 있었다.

`FWD-MENU-015` 가 레거시 컬럼을 직접 지목한다 — "메뉴별로 다른 추천 드레싱을
`menu_option.is_recommended` 기준으로 표시한다." 그리고 `vw_menu_opt_resolved` 가 현재 구조를
보여준다.

```sql
COALESCE(mo.recommended, opi.recommended) AS recommended
COALESCE(mo.is_default,  opi.is_default)  AS is_default
COALESCE(mo.sort_no,     opi.sort_no)     AS sort_no
COALESCE(mo.active,      opi.active)      AS active
LEFT JOIN menu_opt_override mo ON mo.menu_id = mop.menu_id AND mo.opt_item_id = opi.opt_item_id
```

`menu_option` 이 담던 4개 값이 **공통 정책 기본값 `opt_policy_item` + 메뉴별 예외
`menu_opt_override`** 로 분해됐다. 9,166건 → 1,469건 + 76건. `menu_option_group`(467건) →
`menu_opt_policy`(1,454건), 근거는 FK 이름 `fk_menu_option_policy_menu` / `_policy`.

남은 것은 구조 대응이 아니라 데이터 이관 기록뿐이다. `asak-data` 저장소가 이 워크스페이스에 없어
`seed/manifest.json` 과 마이그레이션 스크립트는 확인하지 못했다. 시드를 처음부터 다시 만들 계획이
있을 때만 문제가 된다.

### (2) 연계 REQ — 재매핑함. 기존 매핑에 오류가 있었다

신규 5개만 비어 있는 게 아니라 **기존 매핑 자체가 여럿 틀려 있었다.**

| 테이블 | 이전 판의 REQ | 그 REQ 의 실제 내용 |
|---|---|---|
| `ing`, `menu_ing`, `opt_group`, `opt_item`, `menu_opt_policy` | FWD-MENU-003 | "메뉴 대표 이미지 제공" — 재료·옵션과 무관 |
| `menu_option` | FWD-MENU-004 | "알레르기/비건 태그 확인" — 옵션과 무관 |
| `code_group`, `common_code` | KSD-ARCH-001 | "데이터는 Spring Boot를 통해서만 접근" — 비기능 요구 |

`tag`=FWD-MENU-013, `allergen`/`ing_allergen`=FWD-MENU-008, `menu_nutr`=FWD-MENU-009,
`item_exclusion`=FWD-MENU-007, `opt_item_comp`=LMIS-MENU-006 은 정확했다.

`requirements-definition.md` 의 요구사항 내용과 대조해 26개를 다시 매핑했다. 근거가 강한 것만
확정하고 나머지는 `후보:` 로 표시했다. 확정한 것 중 근거가 뚜렷한 예:

- `media_asset` → FWD-MENU-003 "메뉴 대표 이미지 제공"
- `menu_opt_override`, `opt_policy_item` → FWD-MENU-015 (`recommended` 보유)
- `pay_method_cfg` → LMIS-PAY-001 "결제 수단 설정 관리"
- `payment` → FWD-PAY-002 · KSD-PAY-001 "결제 데이터 무결성 보장"

`code_group`, `common_code` 는 대응하는 요구사항이 없어 비워뒀다.

### (3) 04 문서 "실제 연결 상태" 표 — 코드 확인 후 갱신함

2026-08-19 기준 코드로 확인한 실제 상태로 표를 다시 썼다. 파일 존재와 내용 기준이며 실행 검증은
하지 않았다.

| 항목 | 이전 판 | 실제 |
|---|---|---|
| `ApiResponse<T>` | "필드 구조만 존재, factory·Controller 적용 필요" | 5필드 envelope + `success()` factory 구현. Controller 13개 중 10개 사용 |
| Controller/Service/Mapper | "빈 클래스 존재, SQL은 아직 없음" | Controller 13(9개 매핑 보유), Service 10(`UserOrderService` 471줄 등), Mapper XML 10개 중 6개에 SQL 66문 |
| Bruno `api/` | 24개 | 37개 |
| 예외 처리 | (항목 없음) | `ErrorCode`, `GlobalExceptionHandler` 구현됨 |

`AdminPaymentMethodMapper`, `AdminSoldOutMapper`, `AdminStatsMapper`, `DeviceEventMapper`
4개 XML 은 여전히 비어 있어 표에 명시했다.

## 7. 업무 코드 규칙 — 문자열로 확정

04 문서를 고치다 발견했다. "업무 코드 규칙" 절은 API 의 `code` 를 `"0000"`, `"1001"` 같은
**숫자 코드**로 반환한다고 적고 있으나, 실제 코드는 문자열 상수를 쓴다.

```java
// ErrorCode.java
INVALID_OPTION_SELECTION("INVALID_OPTION_SELECTION", HttpStatus.BAD_REQUEST, ...)
IDEMPOTENCY_KEY_CONFLICT("IDEMPOTENCY_KEY_CONFLICT", HttpStatus.CONFLICT, ...)

// ApiResponse.java 주석
// code는 API별 의미 있는 문자열을 쓴다. (레거시 "0000" 숫자 코드 사용 안 함)
```

근거가 될 `devcopilot-api-alignment-2026-07-23.md` 는 저장소에 없고, 숫자 코드 규칙을 담은 문서도
04 문서 하나뿐이었다(`ASAK/docs/wiki`, `docs/governance` 전체 검색). 반면 구현은 51개 코드가
모두 문자열로 일관돼 있고 프론트도 그 값으로 분기한다.

**2026-08-19 확정: 업무 코드는 문자열이다.** 04 문서의 숫자 코드 규칙을 폐기 처리하고, 문자열
규칙과 응답 예시, `ErrorCode.java` 정본 링크, 새 오류 추가 절차로 다시 썼다. 폐기된 숫자 매핑은
이력으로 남겨 뒀다.

## 8. `vw_order_live` 에 READY 포함 — 적용 완료

2차 작업 마무리 검증에서 문서와 실제의 차이로 잡혔다가, 확인 결과 **의도한 변경**이었고
운영 DB 적용까지 끝났다. 1차 보고의 "뷰 22개 일치"는 적용 전 시점 기준이라 이 건에 한해 틀렸다.

주방 보드가 결제 대기(`READY`) 주문도 보여주도록 `vw_order_live` 의 상태 필터를 4곳 모두 넓혔다.

```sql
WHERE st.code IN ('RECEIVED','PREPARING','READY')
```

`ASAK-back/docs/view.sql` 은 커밋 `3fc21b5` 에서 먼저 바뀌었고, 이후 운영 DB에도 적용됐다.
2026-08-19 재덤프 후 `verify` 결과 정의 차이 0개. 보드에 READY 3건이 함께 잡히는 것도 확인했다
(PREPARING 9 · RECEIVED 1 · READY 3 = 13행).

참고로 `common_code` 에 `READY` 코드가 두 개 있다(id 14, id 51 — 둘 다 이름이 "결제 대기").
코드 그룹이 달라 `(code_grp_id, code)` UNIQUE 는 지켜지지만, 상태 필터를 코드 문자열로 거는
뷰에서는 어느 그룹을 뜻하는지 모호해질 수 있다. **확인 필요.**

### 도구도 함께 고쳤다

이 건을 `schema_sync.py verify` 초기 버전이 **"표기 차이"로 잘못 통과시켰다.** 두 SQL 의 실행
결과(행 수·체크섬)가 현재 데이터에서 우연히 같았기 때문이다. 실행 비교는 "지금 데이터에서 결과가
같다"만 보일 뿐 "정의가 같다"를 보이지 못한다.

차이를 두 종류로 나누도록 고쳤다.

- **괄호 표기 차이** — 차이나는 토큰이 전부 `(` `)` 인 경우만. 이때만 실행 비교로 확인한다.
- **정의 차이** — 리터럴·식별자가 다르면 실행 결과와 무관하게 불일치로 판정하고 종료코드 1.

수정 후 결과:

```text
[뷰] 정의 토큰 비교
  결과: 일치 19개 / 괄호 표기 차이 2개 / 정의 차이 1개
  !! 정의가 다르다: vw_order_live (괄호 외 토큰이 다름)
최종: 차이가 있다. diff 를 실행할 것
```

## 9. 덤으로 발견 — 04 문서의 정본 링크 6개가 깨져 있다

링크 검사에서 나왔다. 대상 파일이 존재하지 않는다.

```text
ASAK/docs/governance/devcopilot-api-alignment-2026-07-23.md
ASAK/docs/product_bible/02_Order_Cart_Payment/order/ORDER_API_CONTRACT.md
ASAK/docs/product_bible/02_Order_Cart_Payment/payment/PAYMENT_API_CONTRACT.md
ASAK/docs/product_bible/03_Menu_Inventory_SoldOut/menu/MENU_API_CONTRACT.md
ASAK/docs/product_bible/06_Engineering_Bible/03-backend/VALIDATION_AND_EXCEPTION_RULES.md
ASAK/docs/product_bible/11_Backend_Implementation/01-common/EXCEPTION_IMPLEMENTATION.md
```

`product_bible` 이 평탄화 재구성되면서 `order/`, `payment/`, `menu/`, `01-common/`, `03-backend/`
하위 폴더가 사라진 것으로 보인다. 지금 `02_Order_Cart_Payment/` 아래에는 `ORDER_BIBLE.md`,
`PAYMENT_BIBLE.md`, `CART_BIBLE.md` 가 있고 `11_Backend_Implementation/` 아래에는
`BACKEND_COMMON_IMPLEMENTATION.md` 가 있다.

어느 문서가 옛 계약 문서를 이어받았는지 내용 확인 없이는 알 수 없어 링크를 임의로 바꾸지 않았다.
04 문서 "정본 링크" 절에 경고만 달았다. 별도 정리가 필요하다.

앞의 (7) 업무 코드 규칙 충돌도 이 문제와 얽혀 있다. 근거가 될 정렬 문서 자체가 없어 판단이 막혔다.

## 7. 주의

DB `nam3324.synology.me:33338/asak_db` 는 **팀 공용**이다. 로컬 사본이 아니다.
`schema_sync.py` 는 읽기 전용으로 막아뒀지만, 다른 작업으로 쓰기를 할 때는 백업과 승인이 필요하다.

`view.sql` 을 운영에 적용할 때 주의할 점이 하나 있다. 실제 뷰는 전부
``DEFINER=`asakasak`@`%` ``, `SQL SECURITY DEFINER` 인데 `view.sql` 의 `CREATE OR REPLACE VIEW`
에는 DEFINER 절이 없다. 그대로 적용하면 실행한 계정이 definer 가 된다.
