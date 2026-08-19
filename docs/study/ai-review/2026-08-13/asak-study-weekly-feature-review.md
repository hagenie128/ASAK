# ASAK 이번 주 기능별 복습 (2026-08-10 ~ 2026-08-13)

## 1. 결론

이번 주의 중심은 **관리자 메뉴 관리**, **키오스크 주문·결제 기반**, **샐러디 메뉴·영양 데이터 정합성**, **화면 자산과 운영 UI 정리**다.  
코드가 원격 `main`에 반영된 항목과, 실제 MySQL 조회까지 끝난 항목, 오늘 로컬에서만 진행 중인 항목을 구분해야 한다.

## 2. 범위와 확인 파일

| 기능 | 확인한 파일 | 읽은 이유 |
| --- | --- | --- |
| 관리자 메뉴 관리 | `ASAK-Admin/src/api/menusApi.js`, `src/hooks/useMenusQuery.js`, `src/pages/admin/MenuManagePage.jsx`, `ASAK-backend/.../AdminMenuController.java`, `AdminMenuService.java` | 화면 요청부터 Controller·Service까지의 실제 연결을 확인 |
| 키오스크 주문·결제 | `ASAK-Kiosk/src/pages/kiosk/PaymentPage.jsx`, `src/api/order.js`, `vite.config.js`, `ASAK-backend/.../UserPayController.java`, `UserPayService.java`, `UserPayMapper.xml` | 주문 생성과 결제 승인의 연결 완료 범위를 분리 |
| 메뉴·영양 데이터 | `ASAK/worklog/daily/이하진/2026-08-11.md`, `2026-08-12.md`, `asak-data/seed-v3/*`, `asak-data/scripts/*` | 시드·스크립트·DB 검증 결과를 확인 |
| 화면·에셋·운영 UI | 이번 주 ASAK-Admin/ASAK-Kiosk Git 커밋 | 반응형, 사이드바, 라이브오더, 이미지·아이콘 변경 범위를 확인 |
| 화면 기준 | `ASAK/docs/wiki/screen-design-figma.md`, Screen Bible | Screen ID·Figma Node·요구 상태의 기준을 확인 |

## 3. 기능별 복습

### A. 관리자 메뉴 관리 — SCR-016 / SCR-017

- **사용자 결과:** 관리자가 메뉴 목록을 검색·선택하고, 메뉴·재료·옵션·영양·태그를 등록·수정·삭제할 수 있는 API 기반 흐름을 갖췄다.
- **Figma 기준:** SCR-016 메뉴 관리 (`75:14`), SCR-017 등록/수정 (`75:15`). Screen Bible 상태는 아직 `Current Draft`/기획중이므로, 이번 주에는 Figma E2E 대조가 완료된 것이 아니다.
- **흐름:**

  ```text
  MenuManagePage
    → useMenusQuery
    → menusApi (/api/admin/menus)
    → AdminMenuController
    → AdminMenuService
    → AdminMenuMapper/MySQL
    → MenuDetailResponse
    → 목록·상세·편집 패널
  ```

- **핵심 동작:**
  - `useMenusQuery`는 목록의 `loading / empty / error / success` 상태, 카테고리·검색어·페이지를 관리한다.
  - `MenuManagePage`는 조회/편집/등록 패널을 조립하고, 저장 후 `refetch()`로 목록과 상세를 다시 읽는다.
  - `AdminMenuController`는 고정 경로인 `/categories`, `/ingredients`를 숫자형 `/{menuId}`보다 먼저 선언해 `ingredients`가 path variable로 해석되는 문제를 막았다.
  - 삭제는 `deleted_at`만 채우는 **soft delete**다. 주문 이력과 자식 데이터는 남긴다.
  - 수정 시 자식 섹션은 요청값이 `null`이 아닐 때만 교체한다. 핵심 재료(`CORE`)는 클라이언트가 제거 가능이라고 보내도 서버에서 제거 불가로 저장한다.
- **이번 주 반영:** 8/11 메뉴 상세·영양·재료·soft delete 및 FE API 연동, 8/12 CRUD UX 보강과 옵션그룹 전체 삭제 버그 수정.
- **검증 상태:** Git 원격 `main` 반영은 확인됨. 브라우저 생성·수정·삭제 E2E, 실제 서버 저장, Figma 상태 대조는 미확인이다.

#### 이 기능을 사용자가 체감하는 순서

1. 관리자가 `/menus`에서 메뉴 목록을 본다.
2. 카테고리·검색어·페이지를 바꾸면 목록 API를 다시 요청한다.
3. 메뉴 하나를 누르면 상세 API를 요청해 오른쪽 패널을 채운다.
4. 수정 또는 등록 화면에서 메뉴 기본 정보와 재료·옵션·영양·태그를 한 번의 요청 객체로 만든다.
5. 저장 성공 뒤 목록과 선택 메뉴를 다시 조회한다.
6. 삭제는 메뉴 행을 물리적으로 지우지 않고 `deleted_at`을 채워, 이후 목록에서만 숨긴다.

#### 프론트엔드에서는 무엇을 하나?

`MenuManagePage`는 **화면 조립 담당**이다. 목록 패널, 상세 패널, 편집 패널 중 무엇을 보여 줄지 `panelMode`(`view`, `edit`, `create`)로 결정한다. 따라서 이 Page에 서버 요청·필드 변환을 너무 많이 넣지 않고, 실제 조회는 Hook으로 보낸 구조다.

`useMenusQuery`는 **메뉴 데이터 담당**이다.

- 목록 요청: `page`, `size`, `sort`, 선택한 `categoryId`, `keyword`를 만든다.
- 목록 응답: `content`를 메뉴 목록으로, `totalElements`를 페이지네이션용 총 개수로 저장한다.
- 상태: 요청 중이면 `loading`, 결과가 없으면 `empty`, 실패면 `error`, 목록이 있으면 `success`가 된다.
- 선택된 메뉴: 목록에서 선택한 `menuId`가 바뀌면 상세 요청을 한 번 더 보내 `selectedMenu`를 채운다.

이 분리가 중요한 이유는 목록용 응답은 가볍게 유지하고, 재료·옵션·영양까지 필요한 순간에만 상세를 받기 위해서다.

`MenuEditPanel`은 **폼 편집 담당**이다. 기존 메뉴를 열면 `name`, `categoryId`, `price`, `description`, `imageUrl`와 자식 데이터(재료·옵션그룹·영양·태그)를 폼 상태로 복사한다. 저장 전 기준값과 현재 값을 비교해 변경 건수를 표시하고, 옵션그룹에서는 필수 그룹의 추천 옵션이 항상 하나가 되도록 정규화한다.

#### API 요청은 어떻게 생기나?

프론트의 `menusApi`가 사용하는 핵심 경로는 아래와 같다.

| 사용자 행동 | HTTP | 경로 | 쓰는 값 |
| --- | --- | --- | --- |
| 목록 보기 | GET | `/api/admin/menus` | page, size, keyword, categoryId |
| 메뉴 하나 보기 | GET | `/api/admin/menus/{menuId}` | menuId |
| 카테고리 읽기 | GET | `/api/admin/menus/categories` | 없음 |
| 재료 고르기 | GET | `/api/admin/menus/ingredients` | 없음 |
| 메뉴 만들기 | POST | `/api/admin/menus` | 기본 정보 + 자식 데이터 |
| 메뉴 수정 | PATCH | `/api/admin/menus/{menuId}` | 기본 정보 + 바뀐 자식 데이터 |
| 메뉴 삭제 | DELETE | `/api/admin/menus/{menuId}` | menuId |

프론트는 `ingredients`를 `{ ingredientId, role, quantity, unit, isDefault, canRemove }`로 보낸다. 여기서 `role`은 메뉴 안에서 그 재료가 베이스인지, 핵심 재료인지 등을 구분한다. `optionGroups`, `nutrition`, `tags`도 같은 요청에 함께 담긴다.

#### 백엔드에서는 무엇을 검증하고 저장하나?

`AdminMenuController`는 URL과 요청 몸체를 받아 Service로 넘긴다. 여기서 알아둘 점은 `/categories`, `/ingredients`를 `/{menuId}`보다 위에 둔 것이다. 그렇지 않으면 Spring이 문자열 `ingredients`를 `menuId`라고 오해할 수 있다.

`AdminMenuService`는 실제 규칙을 담당한다.

- 등록: `menu`를 먼저 INSERT해서 새 `menuId`를 얻고, 그 뒤에 재료·옵션·영양·태그를 자식 테이블에 INSERT한다.
- 수정: 메뉴 본문을 갱신하고, 요청에서 해당 자식 섹션이 `null`이 아니면 기존 자식 데이터를 지운 후 새 값으로 넣는다. 즉, “아무 값도 보내지 않음”과 “빈 배열을 보내서 전부 제거함”은 의미가 다르다.
- 핵심 재료: `CORE` 역할이면 `canRemove=true`가 와도 서버에서 제거 불가로 저장한다. 화면만 믿지 않는 서버 규칙이다.
- 삭제: `deleted_at`을 갱신한다. 주문 항목이 과거 메뉴를 참조할 수 있으므로 `DELETE FROM menu`를 하지 않는다.

#### DB에서 따라가 볼 지점

```text
menu
 ├─ menu_ing           : 메뉴 구성 재료, 역할, 수량, 제거 가능 여부
 ├─ menu_opt_policy    : 메뉴에 붙은 옵션그룹 정책
 ├─ menu_opt_override  : 추천 옵션 등 메뉴별 덮어쓰기
 ├─ menu_nutr          : 메뉴 영양 정보
 └─ menu_tag           : BEST/NEW/VEGAN 같은 태그
```

#### 직접 해볼 미니 실습

- 메뉴 하나의 가격만 바꿔 저장한 뒤, 어떤 요청 필드가 바뀌었고 목록·상세가 언제 재조회되는지 브라우저 Network에서 확인한다.
- `CORE` 재료의 `canRemove`를 `true`로 보내도 저장값이 제거 불가인지 확인한다.
- 삭제 뒤 메뉴 목록에서는 숨지만 주문 이력 조회에는 영향을 주지 않아야 하는 이유를 설명해 본다.

### B. 키오스크 주문 생성·결제 승인 기반 — SCR-005 / SCR-007 / SCR-008 / SCR-012

- **사용자 결과:** 결제 화면에서 주문 생성(API-005)을 요청하고, 서버에는 가상 결제 승인(API-006)과 결제수단 조회(API-014)의 기반이 추가됐다.
- **Figma 기준:**
  - SCR-005 장바구니: 주문 생성 API-005
  - SCR-007 결제: Figma `75:8`, API-006, 승인 중 Loading 필요
  - SCR-008 주문 완료: Figma `75:9`, 주문번호·결제 상태 표시
  - SCR-012 실패/재시도: Figma `75:10`, 장바구니 보존 필요
- **현재 실제 흐름:**

  ```text
  PaymentPage
    → cartStore의 orderType/items 검증
    → createOrder(API-005)
    → orderSessionStore에 응답 저장
    → /paymentProcessing 이동

  POST /api/kiosk/payments (API-006, 서버 구현)
    → UserPayService
    → idempotencyKey 중복 확인
    → 주문 상태·결제수단 활성 확인
    → payment 저장
    → 승인 결과 + 대기 주문 수 반환
  ```

- **핵심 동작:**
  - `PaymentPage`는 중복 클릭을 `isSubmitting`으로 막고, 선택 수단·주문 유형·장바구니가 없으면 주문 생성을 실행하지 않는다.
  - API-005 요청은 `menuId`, `quantity`, `optionItemId`, `excludedIngredientIds`를 보낸다.
  - 화면 총액은 서버 검증값 `validatedTotalAmount`가 있으면 우선 사용하고, 없으면 `priceCalculation`으로 계산한다.
  - API-006은 동일 `idempotencyKey`의 같은 요청에는 기존 결과를 반환하고, 다른 요청에 재사용하면 충돌 오류를 낸다. 이미 승인된 주문과 비활성 결제수단도 막는다.
- **중요한 현재 한계:** 키오스크 `PaymentPage`는 아직 API-005만 직접 호출한다. API-006 호출, API-014 응답으로 결제수단을 그리기, 승인 Loading/실패 재시도/완료 화면 연결은 이 파일 기준으로 완료 확인되지 않았다. 결제수단도 현재 정적 `METHODS` 배열이다.
- **검증 상태:** API-006·014 백엔드 코드는 커밋됨. API 호출 E2E·결제 처리 화면 전환·실 DB 검증은 이번 학습에서 실행하지 않았다.

#### 이 기능을 고객이 체감하는 순서

1. 고객이 메뉴·옵션·제외 재료·수량을 장바구니에 담는다.
2. 결제 화면에서 카드 또는 카카오페이를 선택한다.
3. 결제 버튼을 누르면 먼저 주문 생성(API-005)을 요청한다.
4. 성공하면 응답 주문을 Zustand store에 저장하고 `/paymentProcessing`으로 이동한다.
5. 원래 설계상 다음 단계는 결제 승인(API-006) → 주문번호·승인 결과(SCR-008)다.
6. 현재 코드에서 5단계는 백엔드에 준비됐지만 `PaymentPage`가 직접 호출하는 연결은 아직 확인되지 않았다.

#### 프론트엔드 결제 화면을 한 줄씩 이해하기

`PaymentPage`의 `selectedMethodId`는 사용자가 고른 결제수단을 기억한다. 아직은 `card`, `kakao`라는 화면용 ID이고 API-014의 `CARD`, `KAKAO_PAY` 같은 서버 코드와 연결되지 않았다.

`handleGoPayConfirm`은 결제 버튼의 핵심 함수다.

1. 수단 선택, `orderType`, 장바구니 항목이 있고 이미 요청 중이 아닌지 먼저 검사한다.
2. 장바구니 항목을 서버 형식으로 바꾼다. 옵션은 `optionItemId`와 `quantity`, 제외 재료는 `excludedIngredientIds`로 보낸다.
3. `createOrder()`로 API-005를 호출한다.
4. 성공하면 `setOrder(result)`로 Zustand에 주문 응답을 저장하고 결제 처리 화면으로 이동한다.
5. 실패하면 `orderError`에 오류를 넣고 모달을 띄운다. 품절 코드 `MENU_SOLD_OUT`이면 고객을 장바구니로 보낼 수 있다.

`isSubmitting`은 “버튼을 연속해서 눌러 주문이 두 번 만들어지는 것”을 막는 첫 번째 방어선이다. 다만 브라우저 상태만으로는 부족하므로 결제 승인 API에서는 서버 쪽 멱등성 방어도 추가했다.

#### 금액은 어디에서 오나?

```text
validatedTotalAmount가 있으면 서버 검증 금액 사용
             ↓ 없으면
calculateCartTotal(items)로 화면에서 예상 금액 계산
             ↓ 항목별 금액은
priceCalculation(unitPrice, optionItems, quantity)
```

즉, 화면 계산은 사용자에게 바로 보여 줄 값이고, 서버 검증 금액은 주문/결제의 기준값이어야 한다. 둘이 다르면 서버 값을 우선해야 가격 조작이나 오래된 화면 상태 문제를 줄일 수 있다.

#### 백엔드 결제 승인은 왜 순서가 중요한가?

`UserPayService.createApprovePayment()`는 아래 순서로 처리한다.

1. `orderId`, `paymentMethodCode`, `idempotencyKey`가 있는지 확인한다.
2. 같은 `idempotencyKey`를 이미 썼는지 찾는다.
3. 같은 주문·같은 결제수단이면 과거 결과를 돌려주고, 다른 요청에 같은 키를 썼으면 충돌 오류를 낸다.
4. 주문이 존재하고 상태가 `RECEIVED`인지 확인한다.
5. 이미 승인된 결제가 있는 주문인지 확인한다.
6. 결제수단이 존재하고 활성화됐는지 확인한다.
7. 요청 금액이 아니라 DB의 `orders.total_price`를 승인 금액으로 사용해 `payment`에 저장한다.
8. `paymentId`로 주문번호·승인 시각·대기 주문 수를 다시 조회해 응답한다.

이 순서는 같은 결제를 두 번 승인하거나, 화면이 바꾼 금액을 그대로 믿는 문제를 막기 위한 것이다.

#### 멱등성(idempotency)을 쉬운 말로 설명하면

결제 버튼을 두 번 눌렀거나 네트워크가 끊겨 사용자가 다시 시도해도, **같은 결제 요청에는 같은 식별 키를 사용해 결제를 한 번만 처리하는 장치**다.  
현재 백엔드는 키 재사용을 확인한다. 키오스크에서 UUID를 언제 만들고 재시도 때 어떻게 유지할지는 화면 연결 시 결정·검증해야 한다.

#### API-014 결제수단 조회는 무엇을 위한가?

`GET /api/kiosk/payment-methods`는 DB의 결제수단 설정을 `methodId`, `methodCode`, `methodName`, `isEnabled`, `sortOrder`로 반환한다. 장기적으로는 키오스크가 이 목록을 받아 활성화된 수단만 정렬해서 보여 줘야 한다.

현재 화면은 하드코딩된 `METHODS` 배열을 사용하므로, **백엔드 API가 있어도 관리자 설정이 고객 화면에 반영되지는 않는다.** 이 차이를 기억하는 것이 이번 주 결제 기능 복습의 핵심이다.

#### 직접 해볼 미니 실습

- `PaymentPage`에서 API-005 요청 body를 출력해 메뉴·옵션·제외 재료가 어떤 이름으로 전송되는지 확인한다.
- 같은 `idempotencyKey`로 API-006을 두 번 호출했을 때 응답이 어떻게 되는지 Bruno에서 확인한다.
- 비활성 결제수단을 API-006에 보내면 어떤 오류 코드가 나와야 하는지 `validateMethodForPayment`에서 찾는다.

### C. 재료 영양 분리와 샐러디 메뉴 동기화

- **사용자 결과:** 재료 영양을 별도 데이터로 관리하고, 샐러디 CSV를 기준으로 메뉴·영양·재료·태그·옵션 정책과 키오스크 정적 이미지를 맞추는 재현 가능한 작업 기반을 만들었다.
- **흐름:**

  ```text
  샐러디 CSV
    → Python 적용·검증 스크립트
    → seed-v3 JSON / SQL migration
    → MySQL menu·menu_nutr·ing 등
    → Kiosk public/assets menu·ingredients
  ```

- **이번 주 반영:**
  - 8/11: `ing_nutr` 시드, 영양 분리 SQL, 적재·뷰 갱신 스크립트 추가.
  - 8/12: 40개 메뉴 CSV 동기화, 중복 메뉴 제거 스크립트, 영양·알레르기 입력/리포트, 이미지 트림 스크립트 추가.
  - 키오스크는 DB 58메뉴와 맞추어 메뉴 PNG·재료 사진·아이콘·catalog을 갱신하고, 중복 메뉴 이미지 34개를 정리했다.
- **확인된 사실:** 8/12 워크로그의 퇴근 시점 MySQL 조회 결과는 `menu 58`, `menu_nutr 58`, `ing 92`, 메뉴 이름 중복 0이다. public 메뉴 PNG도 58개로 기록됐다.
- **남은 검증:** `npm run build`, 키오스크 화면 이미지 표시, Admin API E2E는 미실행이다. 알레르기 체크리스트는 리포트 생성까지만 하고 자동 DB 적용은 하지 않았다.

#### 왜 데이터를 나눴나?

메뉴 영양 정보와 재료 영양 정보는 비슷해 보여도 사용처가 다르다.

- 메뉴 영양(`menu_nutr`): 고객이 선택한 메뉴 한 개의 기본 영양을 보여 줄 때 쓴다.
- 재료 영양(`ing_nutr`): 재료 자체의 영양을 관리하고, 이후 옵션·제외 재료 변화까지 계산하려면 필요한 기준 데이터다.

그래서 이번 주에는 재료 테이블에 영양값을 섞어 두는 방식에서 분리 시드·마이그레이션·적재 스크립트를 추가했다. 데이터 구조를 먼저 고정해 두면 메뉴·재료별로 값이 바뀌어도 업데이트 지점을 명확히 할 수 있다.

#### 샐러디 데이터 동기화 흐름

```text
공식 merged CSV (40개 메뉴)
  → Python 스크립트가 누락·차이 확인
  → seed-v3 JSON 갱신
  → MySQL menu/menu_nutr/ing 등 반영
  → 중복 메뉴 제거 (92개에서 58개)
  → Kiosk 이미지·catalog도 58개 메뉴 기준으로 정리
```

여기서 가장 중요한 개념은 **DB 메뉴 수와 키오스크 이미지 수가 달라지면 화면에서 깨진 이미지가 생길 수 있다**는 점이다. 그래서 dedupe로 DB에서 사라진 메뉴 ID의 정적 PNG도 같이 정리했다.

#### 이번 주 확인된 데이터 결과를 해석하면

- `menu 58`: 현재 운영 기준 메뉴 수.
- `menu_nutr 58`: 메뉴마다 영양 행이 하나씩 있다는 최소 정합성 확인.
- `ing 92`: 재료 기준 데이터 수.
- 이름 중복 0: 메뉴 이름을 기준으로 한 중복 정리 결과.

다만 이 숫자는 8/12 퇴근 시점의 조회 결과다. 빌드나 실제 키오스크 화면 확인까지 끝났다는 뜻은 아니다.

#### 직접 해볼 미니 실습

- 하나의 메뉴 ID를 골라 `menu`, `menu_nutr`, `menu_ing`, 키오스크 `public/assets/menu/{id}.png`를 차례로 찾는다.
- CSV에 있는 메뉴 이름이 seed-v3 `menu.json`에 어떻게 들어가는지 비교한다.
- 영양 시드 파일을 바꿨다고 DB가 자동으로 바뀌는 것은 아닌 이유를 설명해 본다.

### D. 관리자·키오스크 운영 UI와 이미지 자산

- **관리자 UI:** 반응형 기준 통일, 사이드바 탐색 개선, 라이브오더 옵션 2열 정렬, 피드백 아이콘 표시 개선, 메뉴 사진 투명 여백 제거가 8/12에 반영됐다.
- **키오스크 UI:** 옵션 이미지와 피드백 아이콘을 개선했으나, 이후 메뉴 상세 화면 코드는 CSS를 제외하고 이전 시점으로 되돌려졌다. 따라서 현재 코드로 복습할 때는 되돌림 전 UI 동작을 완료 기능으로 간주하면 안 된다.
- **Cloudinary 준비:** Admin에는 `CloudinaryImagePreview`가 추가되고, Kiosk에는 Cloudinary SDK 의존성이 추가됐다. 업로드·저장 전체 흐름이 완료됐다는 근거는 아니다.
- **개발 연결:** Kiosk Vite는 `/api`를 `http://localhost:8080`으로 넘기는 프록시를 추가했다. 로컬 CORS/경로 확인을 위한 기반이며, 프록시를 경유한 브라우저 API 호출은 미검증이다.

#### 운영 UI 개선을 기능으로 이해하기

- **반응형 기준 통일:** 관리자 화면의 dashboard, menus, orders, sold-out의 폭·간격 규칙을 맞춰 화면마다 레이아웃이 달라지는 문제를 줄이는 작업이다.
- **사이드바 탐색:** 메뉴 클릭 뒤 어느 화면으로 가는지가 관리자 작업 흐름의 시작점이므로, 화면 이동 동작을 명확히 한 개선이다.
- **라이브오더 옵션 2열:** 주문 옵션이 길 때 한 줄로 너무 넓어지는 문제를 막고, 조리자가 주문 내용을 더 빨리 읽게 하는 목적이다.
- **피드백 아이콘/토스트:** 저장·실패·확인 같은 결과를 텍스트만이 아니라 시각적으로도 구분하도록 해, 운영자가 행동 결과를 놓치지 않게 한다.
- **메뉴/재료 이미지:** 사진 투명 여백, 아이콘의 일관성, JPG→PNG 전환은 화면 품질뿐 아니라 정적 경로·실제 자산의 정합성 문제이기도 하다.

#### Vite 프록시는 왜 필요한가?

개발 중 프론트는 보통 `5173`, Spring 서버는 `8080` 포트를 쓴다. 브라우저는 포트가 달라져도 다른 출처로 취급한다. Vite proxy는 프론트의 `/api/...` 요청을 개발 서버가 받아 Spring의 `http://localhost:8080/api/...`로 넘긴다.

```text
브라우저: http://localhost:5173/api/kiosk/...
  → Vite dev server proxy
  → http://localhost:8080/api/kiosk/...
```

이는 로컬 개발 편의 설정이다. 배포 환경의 API 주소를 자동으로 해결하거나, API가 정상 응답한다는 보증은 아니다.

### E. 발표 자료·화면 증거

- 발표 PPT, Kiosk/Admin 화면 캡처, 캡처·PPT 보정 스크립트, 작성계획을 `ASAK/docs/00-presentation`에 정리했다.
- 이는 기능 구현 자체보다 **발표용 산출물과 화면 증거를 저장소에 고정한 작업**이다. 발표 리허설과 팀 문구 확정은 남아 있다.

## 4. 오늘 진행 중인 로컬 변경 (완료로 판정하지 않음)

| 저장소 | 내용 | 현재 상태 |
| --- | --- | --- |
| ASAK-Kiosk | `src/api/client.js`의 기본 baseURL을 빈 문자열로 변경 | 커밋 전, 프록시 기반 호출로 전환하려는 변경으로 보이며 브라우저 확인 전 |
| ASAK-backend | `menu.image_url`에서 `media_asset`/`thumbnail_media_id`로 대표 이미지를 정규화하는 DTO·Service·Mapper·view SQL 변경 | 커밋 전·DB 마이그레이션 미실행 |
| ASAK-backend | `docs/2026-08-13_menu_media_asset_normalization.sql` | 새 FK 생성 → 기존 URL 매핑 → 미매핑 행 확인 순서의 수동 SQL 초안. 자동 실행되지 않음 |

## 5. 직접 확인해 볼 항목

1. SCR-016에서 메뉴 검색 → 상세 선택 → 재료 변경 → 저장 → 새로고침 뒤 변경값이 유지되는지 확인한다.
2. 메뉴 삭제 뒤 목록에서 사라지는지와 기존 주문 상세가 깨지지 않는지 확인한다.
3. SCR-007에서 같은 결제 요청을 빠르게 두 번 보내고, `idempotencyKey`가 중복 결제를 막는지 확인한다.
4. API-014의 활성 수단만 키오스크 결제수단에 표시되도록 연결하기 전, 현재 정적 `METHODS`와 서버 응답의 차이를 비교한다.
5. 58개 메뉴 중 신규 메뉴 이미지를 메뉴 목록·상세에서 열어 public asset 경로가 모두 표시되는지 확인한다.

## 6. 짧은 연습문제

1. 메뉴 삭제가 hard delete가 아닌 이유는? → `AdminMenuService.deleteMenu()` 주석과 `softDeleteMenu` 호출을 확인한다.
2. API-006의 중복 결제 방어는 몇 단계인가? → UI `isSubmitting`, `idempotencyKey`, 기존 승인 결제 확인을 찾는다.
3. API-014이 있어도 결제 화면이 아직 서버 수단을 사용하지 않는 근거는? → `PaymentPage.jsx`의 정적 `METHODS` 배열을 확인한다.
4. 메뉴 이미지 정규화는 왜 `imageUrl`을 즉시 삭제하지 않는가? → 8/13 SQL의 3단계 검증과 호환용 URL 변환을 확인한다.

## 7. 다음에 읽을 파일 (3개 이내)

1. `ASAK-Admin/src/components/admin/menus/MenuEditPanel.jsx` — 편집 폼과 옵션그룹·재료 변경 감지.
2. `ASAK-backend/src/main/java/com/asak/user/service/UserPayService.java` — 결제 승인 검증 순서.
3. `ASAK-Kiosk/src/pages/kiosk/PaymentPage.jsx` — API-005 이후 API-006을 어디에 연결해야 하는지.

스스로 설명해 볼 질문: **“결제 화면이 주문 생성까지는 연결됐다고 말할 수 있지만, 결제 완료까지 연결됐다고 말할 수 없는 근거는 무엇인가?”**

## 8. 검증 근거와 남은 위험

- 근거: 2026-08-10~12 Git 커밋, 8/11·8/12 일일 워크로그, 현재 소스·Mapper·Screen/Figma 문서.
- 이번 학습에서 코드·DB·원격 Git은 변경하지 않았고, 빌드·테스트·HTTP 호출도 실행하지 않았다.
- Figma Screen Bible의 상태는 다수가 Draft/기획중이다. 코드 반영을 Figma 검수 완료로 해석하면 안 된다.
