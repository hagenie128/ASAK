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

## 6. 결정 필요

**(1) 레거시 `menu_option` / `menu_option_group` 의 현재 대응 테이블**

시드 manifest 의 `menu_option`(9,166건)과 `menu_option_group`(467건)이 현재 어느 테이블로
갔는지 확정하지 못했다. 옵션 구조는 `menu_opt_policy → opt_policy → opt_policy_item → opt_item`
으로 재편됐고 `menu_opt_override` 가 추가됐으나, 두 레거시 테이블이 이 중 어디로 어떻게
나뉘었는지 마이그레이션 기록을 찾지 못했다. 시드를 다시 만들 계획이 있으면 먼저 정리해야 한다.
`db-table-definition.md` 에 `결정 필요` 로 남겼다.

**(2) 신규 5개 테이블의 연계 REQ**

`ing_nutr`, `opt_policy`, `opt_policy_item`, `menu_opt_override`, `media_asset` 은 요구사항 ID 를
확인하지 못해 `— (미확인)` 으로 뒀다. 요구사항 정의서와 대조해 채워야 한다.

**(3) 범위 밖이지만 낡은 문서 — 이번에 고치지 않음**

`ASAK-back/docs/implementation_guide/04-api-db-implementation.md` 의 "실제 연결 상태" 표는
기준일 2026-07-23 으로, `Controller/Service/Mapper` 를 "패키지와 빈 클래스 존재", "SQL은 아직 없음"
으로 적고 있다. 실제로는 `UserPayService` 등 결제·주문 로직이 구현돼 있어 사실과 다르다.
이번 요청 범위(스키마 동기화) 밖이라 손대지 않았다. 별도로 갱신할 것.

## 7. 주의

DB `nam3324.synology.me:33338/asak_db` 는 **팀 공용**이다. 로컬 사본이 아니다.
`schema_sync.py` 는 읽기 전용으로 막아뒀지만, 다른 작업으로 쓰기를 할 때는 백업과 승인이 필요하다.

`view.sql` 을 운영에 적용할 때 주의할 점이 하나 있다. 실제 뷰는 전부
``DEFINER=`asakasak`@`%` ``, `SQL SECURITY DEFINER` 인데 `view.sql` 의 `CREATE OR REPLACE VIEW`
에는 DEFINER 절이 없다. 그대로 적용하면 실행한 계정이 definer 가 된다.
