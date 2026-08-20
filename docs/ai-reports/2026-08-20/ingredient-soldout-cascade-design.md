# 재료 품절 연쇄 처리 설계

- 기록 시작: 2026-08-20 (Asia/Seoul)
- 범위: 재료(`ing`) 품절이 메뉴(`menu`)·옵션(`opt_item`)으로 전파되는 규칙 설계
- 상태: 설계만 정리 · 구현은 사용자가 직접 진행 (코드/DB 변경 없음)
- 관련 테이블: `ing`, `menu`, `menu_ing`, `opt_item`, `opt_group`, `opt_policy`, `opt_policy_item`, `menu_opt_policy`, `menu_opt_override`

## 요청 요약

1. **단백질**(재료) 품절 → 그 단백질을 쓰는 메뉴도 품절 + 관련 옵션도 품절
2. **베이스**(재료) 품절 → 해당 메뉴 품절, 또는 추가금 없는 다른 베이스로 default를 잠시 바꾸고 + 옵션은 품절
3. **그 외 재료** 품절 → 그 재료에 연결된 옵션도 따라서 품절

## 확인된 현재 데이터 구조

실제 운영 DB(`asak_db`)를 조회해서 확인한 내용이다.

| 개념 | 실제 컬럼/코드 |
|---|---|
| 메뉴 품절 | `menu.sold_out` |
| 재료 품절 | `ing.sold_out` |
| 옵션 품절 | `opt_item.sold_out` |
| 옵션 ↔ 재료 연결 | `opt_item.ing_id` → `ing.id` (전체 opt_item 115행 중 ing_id가 채워진 행만 대상) |
| 메뉴가 쓰는 재료의 "역할" | `menu_ing.role_id` → `common_code`(그룹7): `CORE`(핵심=단백질), `BASE`(베이스), `DEFAULT`(일반 기본 재료) |
| 옵션 그룹 종류 | `opt_group.group_type_id` → `common_code`(그룹5): `TOPPING`, `DRESSING`, `BASE`, `SET_SIDE`, `SET_DRINK`, `REQUEST` |
| 메뉴별 노출 옵션 | `menu_opt_policy(menu_id, policy_id)` → `opt_policy(opt_group_id)` → `opt_policy_item(policy_id, opt_item_id, is_default)` |
| 메뉴별 default 재정의 | `menu_opt_override(menu_id, opt_item_id, is_default, active, note)` — 없으면 `opt_policy_item.is_default`가 정본 |

## 확인된 현재 상태 (이미 되는 것 vs 안 되는 것)

| 구분 | 현재 상태 | 이번 설계에서 다뤄야 하는 부분 |
|---|---|---|
| 메뉴 품절(단백질/필수 기본재료) | `vw_menu_availability`가 **이미** `ing.sold_out` + `menu_ing.role_id(CORE/DEFAULT)`로 실시간 계산해 `vw_menu_list.is_orderable`에 반영 중 (`has_core_sold_out`, `has_blocking_standard`) | 그대로 재사용 가능. 새로 만들 필요 없음 |
| 옵션 품절 연쇄 | **없음.** `opt_item.sold_out`은 `ing.sold_out`과 완전히 독립된 수동 플래그 | 이번에 새로 만들어야 할 부분 |
| 데이터 불일치 실사례 | 방금 전 턴에서 `ing.sold_out=1`로 바꾼 베이컨(143)·두부(151)·드라이토마토(175)·김자반(191)·바베큐소스(210)·에그(149)에 연결된 `opt_item`(282, 285, 315, 325, 2974 등)이 여전히 `sold_out=0`으로 남아 있음 | 연쇄 처리가 없으면 이런 불일치가 매번 수동 작업마다 생김 |
| "빼기" 옵션 | `REQUEST` 그룹(예: `opt_item` 1844 "김자반 빼기", 7641 "드라이토마토 빼기")은 재료가 품절돼도 항상 선택 가능해야 정상 (없는 재료를 "빼는" 요청이므로) | 캐스케이드 대상에서 **제외**해야 함 |
| "베이스 변경" 옵션의 실체 | `opt_group` 243(베이스 변경) 산하 옵션 3개(포케볼/메밀면볼/파스타볼, `opt_item` 334/335/336)는 전부 **+1,500원 유료 업그레이드**이고 재료(`ing_id`)가 아니라 다른 메뉴 스타일을 가리킴 | 현재 데이터에는 "추가금 없는 대체 베이스"가 하나도 없음 — 규칙 2를 그대로 구현해도 지금 당장은 거의 항상 "대체 없음 → 메뉴 품절" 분기로 빠질 것. 나중에 무료 대체 옵션이 추가되면 그때부터 자연히 동작함 |

## 규칙별 처리 방법

### 규칙 0 (공통 전제) — 재료 품절 → 연결된 옵션 품절

```
UPDATE opt_item oi
JOIN opt_group og ON og.id = oi.opt_group_id
JOIN common_code gt ON gt.id = og.group_type_id
SET oi.sold_out = :ing.sold_out 값
WHERE oi.ing_id = :품절된 ing.id
  AND gt.code <> 'REQUEST'   -- "빼기" 옵션은 제외
```

세 규칙(단백질/베이스/그 외) 모두 이 규칙 0을 공통으로 깔고, 그 위에 메뉴 단위 처리를 얹는 구조로 설계했다.

### 규칙 1 — 단백질(`menu_ing.role_id = CORE`) 품절

1. 규칙 0 실행 (연결 옵션 품절)
2. 그 재료를 `CORE` 역할로 쓰는 모든 메뉴 조회
   ```sql
   SELECT DISTINCT mi.menu_id
   FROM menu_ing mi
   JOIN common_code rc ON rc.id = mi.role_id
   WHERE mi.ing_id = :ing_id AND rc.code = 'CORE'
   ```
3. 해당 메뉴 전부 `menu.sold_out = 1`

> 참고: `vw_menu_availability.has_core_sold_out`이 읽기 시점엔 이미 이 조건을 계산해준다. `menu.sold_out`을 직접 쓰지 않고 이 뷰만 신뢰해도 되는지(2번을 생략 가능한지)는 "결정 필요 항목"에 남겨둔다.

### 규칙 2 — 베이스(`menu_ing.role_id = BASE`) 품절

1. 규칙 0 실행 (연결 옵션 품절)
2. 그 재료를 `BASE` 역할로 쓰는 메뉴마다 반복:
   a. 그 메뉴에 연결된 `BASE` 타입 옵션 그룹(`menu_opt_policy` → `opt_policy(opt_group.group_type='BASE')` → `opt_policy_item`)에서 **품절이 아니고 `add_price = 0`인 대체 옵션**을 찾는다. 후보가 여러 개면 `sort_no`가 가장 작은 것을 고른다(정렬 우선순위 = 진열 우선순위).
   b. 대체 옵션이 있으면:
      - `menu_opt_override`에 `(menu_id, 대체 opt_item_id, is_default=1, active=1)` upsert
      - 같은 메뉴에서 기존에 default였던 opt_item은 `is_default=0`으로 내림
      - **메뉴는 품절 처리하지 않는다**
   c. 대체 옵션이 없으면:
      - `menu.sold_out = 1`

### 규칙 3 — 그 외 재료(`DEFAULT` 등, 단백질/베이스가 아닌 나머지)

1. 규칙 0만 실행 (연결 옵션 품절)
2. 메뉴 품절 여부는 새로 만들 필요 없음 — `vw_menu_availability.has_blocking_standard`(role=`DEFAULT`이면서 `can_remove=0`인 필수 재료가 품절된 경우)가 읽기 시점에 이미 처리해준다.

## 되돌리기(재입고) 처리

재료가 다시 `sold_out=0`이 될 때:

- 규칙 0의 역방향: 그 `ing_id`를 쓰는 opt_item을 다시 `sold_out=0`으로 (단, 그 옵션이 **다른 이유로** 별도 품절 처리된 게 아니어야 함 — 이 구분을 어떻게 할지는 "결정 필요 항목" 참고)
- 규칙 1: 품절 때문에 내려간 메뉴는 다시 `sold_out=0` — 단 CORE 재료가 여러 개인 메뉴는 "이번에 복구한 재료 때문에 내려갔던 게 맞는지" 확인 필요(다른 CORE 재료가 여전히 품절 상태일 수 있음 → `vw_menu_availability.is_orderable` 재조회로 판단하는 게 안전)
- 규칙 2: `menu_opt_override`로 만든 임시 default를 원래 상태로 되돌려야 함. 이때 "원래 default가 무엇이었는지"를 알아야 하므로, override를 만들 때 `menu_opt_override.note` 컬럼(현재 미사용, `VARCHAR(255)`)에 마커를 남겨두는 방법을 제안한다.
  - 예: `note = 'AUTO_SOLDOUT_FALLBACK:origin_opt_item_id=123'`
  - 재입고 시 이 마커가 붙은 override만 찾아서: 원래 override가 없었으면 override 행 자체를 삭제(=정책 기본값으로 복귀), 원래 override가 있었으면 그 값으로 복원

## 구현 위치 후보

`AdminSoldOutController` / `AdminSoldOutMapper` / `SoldOutPatchRequest`가 이미 TODO 스텁으로 존재한다(TODO-007/008, 관리자 품절 일괄 변경 PATCH). 재료 품절 토글이 결국 이 PATCH를 거쳐 들어오므로, 캐스케이드 로직은 이 Service 계층에 붙이는 게 자연스러워 보인다. 이미 남겨진 TODO 주석에 "부분 실패/전체 롤백 정책을 정한다"는 언급이 있는데, 이번 캐스케이드 때문에 한 번의 PATCH가 여러 테이블(`ing`/`menu`/`opt_item`/`menu_opt_override`)을 건드리게 되므로 그 결정이 더 중요해진다.

## 결정 필요 항목

1. **write-time vs read-time**: 지금 설계는 PATCH 시점에 관련 테이블을 직접 `UPDATE`하는 방식(write-time)이다. 대안으로 `opt_item`/`menu` 품절 여부를 매번 뷰에서 계산하는 read-time 방식도 있다(`vw_menu_availability`가 이미 그 패턴). write-time은 기존 화면 코드를 안 건드려도 되는 대신 되돌리기가 복잡해지고, read-time은 항상 정합성이 보장되는 대신 opt_item을 읽는 모든 곳(주문 화면, 관리자 카탈로그 등)을 다 고쳐야 한다.
2. **재입고 시 opt_item 복구 조건**: 옵션이 "재료 품절 때문에" 내려간 건지 "그 옵션 자체가 원래 수동으로 품절"이었는지 구분할 방법이 지금 스키마엔 없다. `opt_item`에 원인 컬럼(`sold_out_reason` 등)을 추가하거나, 규칙 0을 "재료 품절 OR 수동 품절"을 합친 계산값으로 다루는 별도 뷰를 만드는 방법 중 선택이 필요하다.
3. **규칙 2 대체 후보 선정 기준**: `add_price=0`인 후보가 여러 개면 `sort_no`로 정할지, 아니면 다른 기준(예: 재료 재고 우선순위)이 있는지.
4. **CORE 재료가 여러 개인 메뉴**: 한 메뉴가 CORE 역할 재료를 2개 이상 쓰는 경우(현재 데이터 확인 필요), 그중 하나만 재입고됐을 때 메뉴를 바로 살릴지 다른 CORE 재료 상태까지 다 확인할지.
5. **성능/트랜잭션 범위**: 재료 하나 품절 시 영향받는 메뉴·옵션 수가 실제로 몇 개까지 나오는지(오늘 예시로는 재료당 최대 수십 개 메뉴 수준) 확인하고, 한 번의 PATCH·트랜잭션으로 처리할 범위를 정해야 한다.

## 권장 구현 순서

1. 위 "결정 필요 항목"부터 확정 (특히 1, 2번은 스키마에 영향을 줄 수 있어서 먼저 정해야 함)
2. `AdminSoldOutMapper`에 규칙 0(옵션 캐스케이드) UPDATE 추가
3. 규칙 1(단백질 → 메뉴 품절) 추가, `vw_menu_availability`와 결과가 어긋나지 않는지 대조
4. 규칙 2(베이스 대체/품절 분기) 추가 — 지금 데이터엔 무료 대체가 없으므로, 테스트용으로 `add_price=0`짜리 베이스 옵션을 하나 만들어서 분기 양쪽을 다 확인
5. 재입고(되돌리기) 경로 구현
6. 회귀 테스트: 재료 1개 품절 → 관련 메뉴·옵션 상태, 재입고 → 원상 복구까지 확인

## 작업 경계

- 이 문서는 설계 정리이며 코드·DB·Git 이력은 이번 턴에서 변경하지 않았다.
- 위에 인용한 실제 데이터(재료 ID, 옵션 ID, 메뉴 ID 등)는 2026-08-20 조회 시점 기준이며, 운영 DB는 팀 공용이므로 구현 시 다시 확인이 필요하다.
