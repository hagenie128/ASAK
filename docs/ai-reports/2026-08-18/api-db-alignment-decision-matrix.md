# ASAK API · DB 정렬 의사결정 매트릭스

> 기준일: 2026-08-18  
> 목적: 관리자/키오스크/공용에서 API 명세, 실DB, 현재 구현이 갈리는 항목을 한눈에 보고 최종 정본을 결정한다.  
> 기준 자료: `ASAK/docs/wiki/rest-api-spec.md`, `ASAK/docs/governance/contract-decisions-2026-07-16.md`, `ASAK-back/src/main/resources/mappers/*.xml`, 실DB `asak_db`

## 판정 기준

- `일치`: API 명세, DB/뷰, 구현이 같은 방향으로 정렬됨
- `매핑 OK`: DB 컬럼명은 다르지만 정본 원칙대로 API에서 별칭 매핑함
- `구현 불일치`: DB 또는 뷰는 맞지만 API 응답/요청 이름이 명세와 다름
- `결정 필요`: 문서, 구현, 소비 코드가 갈려 있어 최종 선택이 필요함

## 공용

| 항목 | 현재 API 명세 | 현재 DB / 뷰 | 현재 구현 | 판정 | 최종 권장안 | 메모 |
|---|---|---|---|---|---|---|
| 공통 네이밍 원칙 | API는 `camelCase` | DB는 `snake_case` | 대부분 mapper alias 적용 | 일치 | 유지 | 정본 원칙 자체는 맞다. 문제는 일부 endpoint별 예외다. |
| 총액 | `totalAmount` | `orders.total_price` | `AS totalAmount` | 매핑 OK | 유지 | DB rename 불필요 |
| 결제 승인 금액 | `approvedAmount` | `payment.amount` | `AS approvedAmount` | 매핑 OK | 유지 | DB rename 불필요 |
| 결제 승인 시각 | `approvedAt` | `payment.paid_at` | `AS approvedAt` | 매핑 OK | 유지 | DB rename 불필요 |
| 대기 주문 수 | `waitingOrderCount` | 계산 컬럼 없음, COUNT 서브쿼리 | `AS waitingOrderCount` | 매핑 OK | 유지 | 저장 컬럼으로 만들 필요 없음 |
| 주문 상태 | `orderStatus` 또는 생성 응답 `status` 혼재 | `orders.status_id` + `common_code.code` | 목록/상세=`orderStatus`, 생성=`status` | 결정 필요 | `orderStatus`로 통일 권장 | 생성 응답만 예외라 프런트 혼선이 큼 |
| 결제 상태 | `paymentStatus` | `payment.status_id` + `common_code.code` | 상세/목록/결제 승인에 사용 | 매핑 OK | 유지 | 생성 응답에는 아직 없음 |
| 주문 유형 | `orderType` | `orders.order_type_id` + `common_code.code` | `EAT_IN`/`TAKE_OUT` | 매핑 OK | 유지 | 정본과 동일 |
| 결제수단 코드 | `methodCode` / `paymentMethodCode` | `pay_method_cfg.method_id` + `common_code.code` | API-014/006에서 코드 문자열 노출 | 매핑 OK | 유지 | FK → 코드 노출 정상 |
| 추가금 | `extraPrice` | `opt_item.add_price`, `order_item_option.price` | `AS extraPrice`, insert `#{extraPrice}` | 매핑 OK | 유지 | 정본 원칙에 부합 |
| 옵션 원가 | `originalPrice` | `opt_item.list_price` | `AS originalPrice` | 매핑 OK | 유지 | 문제 없음 |
| 제공량 | `servingAmount` | `opt_item.amount` | `AS servingAmount` | 매핑 OK | 유지 | 문제 없음 |
| 테이블 짧은 이름 | 문서 일부에 long name 잔존 | `ing`, `menu_ing`, `opt_group`, `pay_method_cfg` 등 | 코드/실DB는 short name 기준 | 결정 필요 | 문서를 short name 기준으로 정리 | DB rename 아님, 문서 정리 이슈 |

## 키오스크

| 항목 | 현재 API 명세 | 현재 DB / 뷰 | 현재 구현 | 판정 | 최종 권장안 | 메모 |
|---|---|---|---|---|---|---|
| 카테고리 활성 | `isActive` | `category.active` | `active AS isActive` | 매핑 OK | 유지 | 정상 |
| 메뉴 목록 카테고리 | `categoryId` | `menu.cat_id` | `m.cat_id AS categoryId` | 매핑 OK | 유지 | 정상 |
| 메뉴 목록 품절 | `isSoldOut` | `menu.sold_out` | `m.sold_out AS isSoldOut` | 매핑 OK | 유지 | 정상 |
| 메뉴 목록 주문가능 | 명세 요약엔 암시됨 | 뷰 `vw_menu_list.is_orderable` 존재 | 현재 mapper는 뷰 미사용, 응답 없음 | 구현 불일치 | `isOrderable` 추가 권장 | 목록을 `vw_menu_list` 기준으로 바꾸는 편이 자연스러움 |
| 메뉴 목록 품절 재료 | 명세/화면에서 필요 | 뷰 `vw_menu_list.has_sold_out_ingredient` 존재 | 현재 응답 없음 | 구현 불일치 | `hasSoldOutIngredient` 추가 여부 결정 | 카드 비주얼과 주문 가능 판정에 영향 |
| 목록 칼로리 | 화면/구문서 `calories`/`baseKcal` 흔적 | `menu_nutr.kcal`, 뷰는 `base_kcal` | 현재 응답은 `kcal` | 결정 필요 | `kcal` 유지 권장 | 현재 화면도 `kcal ?? baseKcal`로 우회 중 |
| 메뉴 상세 품절 | `isSoldOut` | `menu.sold_out` | `m.sold_out AS isSoldOut` | 매핑 OK | 유지 | 정상 |
| 메뉴 상세 재료 이름 | 문서에 `ingredientName` 흔적 | `ing.name` | `i.name AS ingName` | 구현 불일치 | `name` 또는 `ingredientName`로 통일 권장 | `ingName`은 DB short-name이 새어 나온 형태 |
| 메뉴 상세 재료 기본 여부 | `isDefault` | `menu_ing.is_default` | `AS isDefault` | 매핑 OK | 유지 | 정상 |
| 메뉴 상세 재료 제거 가능 | `canRemove` | `menu_ing.can_remove` | `AS canRemove` | 매핑 OK | 유지 | 정상 |
| 메뉴 상세 재료 품절 | 화면은 필요 | `ing.sold_out` 또는 뷰 `ing_sold_out` | 현재 응답 없음 | 구현 불일치 | `isSoldOut` 추가 권장 | 상세 재료 품절 표시와 제외 가능성 판단에 영향 |
| 메뉴 상세 옵션 그룹 id | `optionGroupId`처럼 보임 | 실제는 `opt_policy.id` | `op.id AS optionGroupId` | 결정 필요 | 이름 유지하되 문서에 “policy id” 명시 | 지금 이름과 의미가 다름 |
| 옵션 그룹 선택 타입 | `selectType` | 계산 컬럼 없음 (`max_select` 기반) | CASE로 `SINGLE/MULTIPLE` | 매핑 OK | 유지 | 정상 |
| 옵션 아이템 재료 id | `ingredientId` | `opt_item.ing_id` | `AS ingredientId` | 매핑 OK | 유지 | 정상 |
| 옵션 아이템 추가금 | `extraPrice` | `opt_item.add_price` | `AS extraPrice` | 매핑 OK | 유지 | 정상 |
| 옵션 아이템 제공량 단위 | `servingUnit` | `common_code.name` | `unit.name AS servingUnit` | 결정 필요 | 표시용이면 유지, 코드 필요하면 재설계 | 현재는 코드가 아니라 표시명 |
| 장바구니 항목 단가 | 과거 문서에 `unitAmount`/`lineAmount` 흔적 | `order_item.price` / 뷰 `unit_price` | 응답은 `unitPrice` | 결정 필요 | `unitPrice`로 통일 권장 | 키오스크 코드가 이미 `unitPrice` 사용 |
| 주문 생성 상태 필드 | 위키 `orderStatus`, 일부 문서 `status` | `orders.status_id` | 응답은 `status` | 결정 필요 | `orderStatus` 권장 | 목록/상세와 맞추기 쉬움 |
| 주문 생성 결제 상태 | 위키엔 `paymentStatus` | `payment` row는 생성 시 아직 없음 | 응답 없음 | 구현 불일치 | 문서에서 제거 또는 후속 구현 | 실제 생성 직후 결제 전 상태임 |
| 결제수단 활성 | `active` | `pay_method_cfg.active` | `active AS active` | 일치 | 유지 | 방금 문서 정리 완료 |
| 결제수단 설명/이미지 | 명세 최신 반영 | `pay_method_cfg.description`, `image_asset_id` + `media_asset.url` | 노출 중 | 매핑 OK | 유지 | 정상 |
| 결제수단 enum | 정본 3종 `CARD/KAKAO_PAY/NAVER_PAY` | `common_code`에 추가 코드 가능 | 코드엔 `TOSS_PAY` enum 존재 | 결정 필요 | 3종 유지 또는 정본 확장 결정 | API/화면/데이터 전부 영향 |

## 관리자

| 항목 | 현재 API 명세 | 현재 DB / 뷰 | 현재 구현 | 판정 | 최종 권장안 | 메모 |
|---|---|---|---|---|---|---|
| 주문 목록 총액 | `totalAmount` | `orders.total_price` / `vw_order_list_summary.total_price` | `AS totalAmount` | 매핑 OK | 유지 | 정상 |
| 주문 상세 항목 단가 | `unitPrice` | `vw_order_item_full.unit_price` (`order_item.price` 기반) | `AS unitPrice` | 매핑 OK | 유지 | 정상 |
| Live 주문 유형 라벨 | `orderTypeLabel` | `vw_order_live.order_type_label` | `AS orderTypeLabel` | 매핑 OK | 유지 | 목록의 `orderType`과 용도 분리 정상 |
| 메뉴 목록 품절 | 명세는 `isSoldOut` 맥락 | 뷰 `vw_menu_list.is_sold_out` | DTO `boolean isSoldOut` → JSON `soldOut` | 구현 불일치 | JSON `isSoldOut`로 고정 권장 | `@JsonProperty`로 정리 가능 |
| 메뉴 목록 주문가능 | 명세는 `isOrderable` 맥락 | 뷰 `vw_menu_list.is_orderable` | DTO `boolean isOrderable` → JSON `orderable` | 구현 불일치 | JSON `isOrderable`로 고정 권장 | 화면 타입과도 맞춰야 함 |
| 메뉴 목록 품절 재료 | `hasSoldOutIngredient` | 뷰 `has_sold_out_ingredient` | JSON `hasSoldOutIngredient` | 매핑 OK | 유지 | 정상 |
| 카테고리 활성 | `isActive` | `category.active` | `active AS active` + `@JsonProperty(\"isActive\")` | 매핑 OK | 유지 | 이미 잘 정리됨 |
| 메뉴 상세 품절 | `isSoldOut` 맥락 | `menu.sold_out` | DTO `boolean isSoldOut` → JSON `soldOut` | 구현 불일치 | JSON `isSoldOut`로 고정 권장 | 현재 상세 뱃지 오동작 위험 |
| 메뉴 상세 재료 품절 | `isSoldOut` | 뷰 `ing_sold_out` | DTO `boolean isSoldOut` → JSON `soldOut` 가능성 | 구현 불일치 | JSON `isSoldOut`로 고정 권장 | 목록/상세 일관성 필요 |
| 메뉴 상세 재료 기본 여부 | `isDefault` | `menu_ing.is_default` | DTO `boolean isDefault` → JSON `default` 가능성 | 구현 불일치 | JSON `isDefault`로 고정 권장 | 키 이름이 언어 예약어처럼 보여 혼란 |
| 재료 목록 행 식별자 | 화면은 `ingredientId` 기대 | `ing.id` | API는 `id` | 결정 필요 | `ingredientId` 권장 | 등록/수정 body와 같은 이름이 더 자연스러움 |
| 재료 목록 품절 | `isSoldOut` 맥락 | `ing.sold_out` | DTO `boolean isSoldOut` → JSON `soldOut` | 구현 불일치 | `isSoldOut`로 고정 권장 | 현재 화면이 `item.isSoldOut ?? item.soldOut`로 우회 |
| 재료 목록 역할/단위 | `roleName`, `unitName` | `common_code.name` 분기 | 그대로 노출 | 매핑 OK | 유지 | 표시용이면 충분 |
| 결제수단 PATCH 활성 필드 | 이제 `active`로 정리 | `pay_method_cfg.active` | DTO도 `active` | 일치 | 유지 | Admin 스텁 구현 시 프런트 mock `isActive` 정리 필요 |
| 옵션 그룹 목록/상세 id | `optionGroupId` | 현재 구현은 `opt_group.id`, 메뉴 연결 검증은 `opt_policy.id`도 허용 | 조회와 검증 의미가 다름 | 결정 필요 | 조회는 `optionGroupId`, 검증 허용 id 범위 별도 명시 | 같은 이름에 두 의미가 섞임 |

## 최종 결정 우선순위

1. **관리자 boolean JSON 키**  
   `soldOut/orderable/default`를 `isSoldOut/isOrderable/isDefault`로 고정할지 결정
2. **주문 생성 응답 상태명**  
   `status` vs `orderStatus`
3. **키오스크 재료·옵션 명명**  
   `ingName`, policy id 기반 `optionGroupId`, `kcal/baseKcal`
4. **장바구니·주문 금액 항목명**  
   `unitPrice` vs `lineAmount`/`unitAmount`
5. **키오스크 목록 read model**  
   `menu` 직접 조회 유지 vs `vw_menu_list` 기반으로 `isOrderable`, `hasSoldOutIngredient`, `base_kcal` 반영
6. **결제수단 enum 범위**  
   정본 3종 유지 vs `TOSS_PAY` 포함
7. **실DB short-name 문서화**  
   `ing`, `menu_ing`, `opt_group`, `pay_method_cfg`를 문서 정본에 반영

## 권장 결정안

- **공용**
  - DB 컬럼 rename은 하지 않는다.
  - 금액/시각/상태는 지금처럼 mapper alias로 정규화한다.

- **키오스크**
  - `active`, `unitPrice`, `kcal`를 정본으로 삼는다.
  - 재료 이름은 `ingName` 대신 `name` 또는 `ingredientName`으로 바꾼다.
  - 목록은 `vw_menu_list`를 쓰는 쪽으로 정리한다.
  - 생성 응답 상태는 `orderStatus`로 통일하는 편이 전체 일관성이 높다.

- **관리자**
  - `is*` boolean JSON 키를 전부 명시적으로 고정한다.
  - 재료 목록 `id`는 `ingredientId`로 바꾼다.
  - 결제수단 PATCH는 `active`로 유지하고 프런트 mock도 후속 정리한다.
