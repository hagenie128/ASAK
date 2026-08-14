# ASAK Admin 공부 가이드 (개인용 · git 올림 금지)

> 위치: `ASAK-workspace/_local_study/admin/` · 루트 `.gitignore`에 `_local_study/` 등록됨
> 목적: **초보자도** Admin이 왜 이렇게 나뉘어 있는지, mock이 어떻게 흐르는지 복습하기
> 짧은 지도(어디 파일이 있는지): [`../../../../ASAK-Admin/src/STRUCTURE_GUIDE.md`](../../../../ASAK-Admin/src/STRUCTURE_GUIDE.md)
> Mock 필드 사전: [`../../../../ASAK-Admin/public/mocks/README.md`](../../../../ASAK-Admin/public/mocks/README.md)
> 화면별(SCR) 완료도 문서는 2026-07-23 과거 이력으로 제거했습니다. 현재 상태는 WBS와 실제 코드를 확인합니다.

---

## 0. 이 문서로 무엇을 배우나

| 순서 | 주제 | 한 줄 |
|------|------|--------|
| 1 | 전체 그림 | Page → Hook → Repository → JSON |
| 2 | Page = 조합 | OrderListPage처럼 얇게 |
| 3 | 메뉴 우측 패널 | 목록 + Detail/Edit |
| 4 | CSS 계층 | tokens → reset → global → commonStyle |
| 5 | 셸 높이 | 뷰포트 채움 · 안쪽만 스크롤 |
| 6 | 품절 좌중우 | 스크롤은 패널 안 |
| 7 | 페이지네이션 | 화면마다 pageSize |
| 8 | QA 치트 | sessionStorage fail flags |
| 9 | 왜 나눴는지 | 실무 의도 |

---

## 1. 한 줄 결론 (먼저 외우기)

관리자 화면은 **지금 서버 없이** 이렇게 움직인다.

```text
Page (화면 조립)
  → Hook (상태·조회·draft)
    → adminMockRepository.js (가짜 API 입구)
      → public/mocks/asak-admin-data.json (가짜 DB)
```

- Page에서 JSON을 **직접 import하면 안 된다.**
- 나중에 실서버가 붙으면 **repository(또는 api 모듈)만** 바꾸면 되고, Page/UI는 그대로 두는 것이 목표다.
- Envelope(포장) 형태는 보통 `{ success, status, code, message, data }` 이다. Hook은 보통 `data`만 Page에 넘긴다.

---

## 2. 왜 이렇게 나눴는가 (초보자용)

### 2-1. Page / Component / Hook / Mock 을 나눈 이유

| 계층 | 비유 | 하는 일 | 하지 않는 일 |
|------|------|---------|--------------|
| `pages/admin/*` | 무대 감독 | hook 호출, 조각 조립, 이벤트 연결 | JSX 수백 줄 UI, JSON 직접 읽기 |
| `components/admin/*` | 배우·소품 | 표시·입력 UI (props로 데이터) | repository 직접 호출 (합의된 예외 제외) |
| `hooks/*` | 대본·큐 | 조회, 필터, draft, 저장 시도 | 화면 마크업 |
| `mocks/adminMockRepository.js` | 가짜 창구 | JSON에서 꺼내 envelope로 돌려줌 | JSX |
| `public/mocks/*.json` | 가짜 DB | 데이터만 | 로직 없음 |

**실무 의도:** “화면 그리는 사람”과 “데이터 가져오는 곳”을 섞지 않으면, 나중에 API만 갈아끼우기 쉽다.

### 2-2. “미리 파일만 많이 만들기”를 피한 이유

안 쓰는 stub를 잔뜩 만들면 읽는 사람이 “이게 살아 있는 코드인지” 헷갈린다.
**실제로 연결하는 화면만** 분리하고, 안 만든 화면은 정적/placeholder를 유지하는 편이 안전하다.

### 2-3. Admin 저장소가 정본인 이유

관리자 UI·로직의 **정본은 `ASAK-Admin`만**이다.
키오스크(`ASAK-Kiosk`)에 Admin 화면을 복사해 두지 않는다. 역할이 다르기 때문이다.

---

## 3. Page = 조합 (모범: OrderListPage)

가장 얇은 예시부터 보면 이해가 빠르다.

```text
OrderListPage.jsx
  └── 하는 일: LiveOrderPreview 한 줄만 렌더
LiveOrderPreview.jsx
  └── 실제 UI · 상태 · 액션 · (내부에서 mock 조회)
```

파일: `src/pages/admin/OrderListPage.jsx`

```jsx
export default function OrderListPage() {
  return <LiveOrderPreview />;
}
```

**왜?**
URL(`/`)에 붙는 “페이지 이름”과, 실제 보드 UI를 분리하면:

1. 라우트 표가 단순해지고
2. Live 보드를 다른 경로에서도 재사용하기 쉽고
3. Page가 두꺼워져 “모든 로직의 쓰레기통”이 되는 것을 막는다.

### 다른 화면의 같은 패턴

| Page | 조합하는 조각 |
|------|----------------|
| `MenuManagePage` | `MenuListPanel` + (`MenuDetailPanel` \| `MenuEditPanel`) |
| `DashboardPage` | `DashboardPanels` 안의 KPI·최근주문 등 섹션 |
| `OrderManagementPreview` | 필터 + `OrderTable` + `OrderDetailPanel` |
| `SalesSummaryPage` 등 | 기간 UI + KPI/차트 + `SalesShareCard` 등 |

좋은 예:

```text
MenuManagePage
  → useMenusQuery({ initialMenuId })
  → usePagination(...)
  → <MenuListPanel /> + <MenuDetailPanel /> 또는 <MenuEditPanel />
```

나쁜 예:

```text
MenuManagePage 안에
  카드 그리드 · 상세 카드 · 편집 폼 · 페이지네이션 마크업을 전부 인라인
```

---

## 4. Hook → mock repository → JSON (데이터 흐름)

### 4-1. 읽는 순서 (공부할 때)

1. `public/mocks/asak-admin-data.json` — “가짜 DB에 뭐가 있나”
2. `src/mocks/adminMockRepository.js` — “어떤 getter가 있나”
3. `src/hooks/useOrdersQuery.js` (또는 해당 화면 hook) — “Page에 뭐를 넘기나”
4. `src/pages/admin/...` — “어떻게 조립하나”

### 4-2. Repository의 역할

- Page/Component가 JSON 경로(`sales.daily.data.rows`)를 직접 알지 않게 **함수 이름**으로 감싼다.
  예: `getAdminOrders()`, `getSalesSummary("today")`, `getSoldOutCatalog()`
- 실패/빈 목록도 envelope로 통일한다.
  예: `{ empty: true }` 옵션, `asak_mock_fail_save`로 저장 실패 시뮬레이션

### 4-3. Hook의 역할

| Hook | 화면 | 대략 하는 일 |
|------|------|----------------|
| `useOrdersQuery` | 주문 관리 | 필터·조회·목록·페이지네이션 |
| `useSalesQuery` | 매출 3화면 | 기간/일/월 데이터 |
| `useSoldOutDraft` | 품절 | 탭·검색·이동·저장·롤백 |
| `usePaymentMethodDraft` | 결제수단 | 토글·정렬·저장·롤백 |
| `useMenusQuery` | 메뉴 | 카테고리·검색·선택 |
| `useDashboard` | 대시보드 | KPI 등 |
| `usePagination` | 여러 화면 | **화면별 pageSize**로 잘라 주기 |

Hook이 `envelope.data`를 풀어 Page에는 “쓰기 쉬운 값”만 넘기는 패턴을 기억하자.

### 4-4. 화면별 “데이터가 바뀌는 조건”

| 화면 | 경로 | 핵심 파일 | 데이터가 바뀌는 조건 |
|------|------|-----------|---------------------|
| Live 주문 | `/` | `LiveOrderPreview.jsx` | 완료/취소 → mock 상태 변경 · 페이지 |
| 주문 관리 | `/orders` | `OrderManagementPreview.jsx` | 필터·달력·조회 · 상태 변경 |
| 품절 | `/sold-out` | `SoldOutManagePage.jsx` | 탭·검색·←→ · 저장(실패 시 롤백) |
| 메뉴 | `/menus` | `MenuManagePage.jsx` | 카테고리·검색·카드 선택 · 우측 패널 모드 |
| 메뉴 편집 URL | `/menus/edit?menuId=` | `MenuEditPage` → Manage | `initialMode`만 넘김 |
| 결제수단 | `/payment-methods` | `PaymentMethodPage.jsx` | 토글·저장 · 점검중 뱃지 |
| 매출 요약 | `/sales` | `SalesSummaryPage.jsx` | 기간 탭 + 달력 기간 |
| 월별 / 일별 | `/sales/monthly` · `/daily` | 각 Page | ‹ › + 달력 점프 |
| 대시보드 | `/dashboard` | `DashboardPage.jsx` | KPI mock (전주 대비는 mock에 없으면 `—`) |

---

## 5. 메뉴: 우측 Detail / Edit 패널

### 5-1. URL과 패널 모드

| URL | 실제 | `panelMode` |
|-----|------|-------------|
| `/menus` | `MenuManagePage` | 기본 `view` (우측 상세) |
| `/menus/new` | 얇은 `MenuEditPage` → Manage에 `create` | `create` |
| `/menus/edit?menuId=` | 얇은 `MenuEditPage` → Manage에 `edit` | `edit` + 해당 메뉴 선택 |

**별도 “빈 편집 전용 페이지”가 아니다.**
등록/수정 라우트는 Manage 화면을 열고, 우측만 편집 폼(`MenuEditPanel`)으로 바꾸는 방식이다.

### 5-2. 왜 우측 패널인가

- 목록을 보면서 상세/편집을 하므로 문맥이 유지된다.
- Figma 시안(목록 + Detail)과 맞춘다.
- 스크롤은 **우측 패널 안쪽**(`.menu-detail-panel__scroll` 등)만 하고, 셸 전체는 안 흔들리게 한다.

### 5-3. 흐름 그림

```text
카테고리/검색 → filteredMenus → usePagination → MenuListPanel
카드 클릭 → selectMenu → MenuDetailPanel (view)
수정 버튼 → panelMode=edit → MenuEditPanel
신규 메뉴 → panelMode=create → MenuEditPanel
취소/저장 stub → toast 후 view 복귀 (저장은 아직 stub)
```

---

## 6. CSS 체계 (키오스크와 같은 순서)

`AdminApp.jsx`에서 **이 순서로** 로드한다.

```text
tokens.css      → 색·폰트·간격 변수 (--admin-*)
reset.css       → 브라우저 기본 스타일 정리
global.css      → html/body/#root, 뷰포트 높이, overflow
commonStyle.css → @import 로 admin/*.css 묶음
```

`commonStyle.css` 안에서는 대략:

```text
admin/base.css      (셸·사이드바·메인)
admin/shared.css
admin/orders.css, sold-out.css, menu.css, …
```

### 왜 순서가 중요한가

1. **tokens 먼저** — 뒤에서 `var(--admin-bg)`를 쓸 수 있다.
2. **reset 다음** — 브라우저마다 다른 margin을 맞춘다.
3. **global** — `body` 높이·`overflow: hidden` 같은 “앱 뼈대”
4. **commonStyle** — 화면별 디테일

키오스크도 같은 레이어 이름을 쓴다. Admin/Kiosk를 오가며 공부할 때 “어디를 고치면 되는지”가 같다.

`app-shell.css`에도 같은 `@import` 순서가 적혀 있을 수 있다. **실행 정본은 `AdminApp.jsx`의 import**를 본다.

---

## 7. 셸 높이: 뷰포트 기준 (의도)

> 코드가 진행 중일 수 있다. 아래는 **의도(설계 방향)** 설명이다.

### 의도

- Figma는 1920×1080 캔버스를 기준으로 그렸지만,
  실제 브라우저는 모니터마다 높이가 다르다.
- 그래서 셸은 **뷰포트를 꽉 채우는 방향**으로 맞춘다.
  - `body`: `height: 100vh` / `100dvh`, `overflow: hidden`
  - `.admin-app`: `height: 100%`, `max-height: 100dvh`, `overflow: hidden`
- **바깥(body)은 스크롤하지 않고**, 사이드바는 고정, **메인·내부 패널만** 세로 스크롤.

### 왜 body 스크롤을 막나

운영 화면(키오스크형 관리자)은 “페이지 전체가 위아래로 흔들리는” UX보다,
**표·카드 영역만 스크롤**하는 편이 익숙하고 실수(더블 스크롤)가 적다.

### 예전에 문서에 있던 “1080px 고정”

시안 맞춤용으로 `1080px` 고정을 쓰던 시기가 있었다.
지금은 **뷰포트 채움**이 의도에 가깝다. 화면이 잘리면 `global.css` / `admin/base.css`의 height·overflow를 먼저 본다.

---

## 8. 품절 화면: 좌 · 중 · 우

레이아웃 의도 (`sold-out.css` 주석과 코드):

```text
┌─────────────┬────┬─────────────┐
│ 판매중(좌)   │ ←→ │ 품절(우)     │
│ 탭·검색·카드 │중 │ 카드 그리드  │
│ + 페이지네이션│이 │ + 페이지네이션│
└─────────────┴────┴─────────────┘
```

- `.sold-out-management__workspace` = 가로 flex (좌 패널 · transfer · 우 패널)
- **페이지(셸) 전체가 스크롤되지 않게** `overflow: hidden`
- 긴 카드 목록은 **각 패널 안쪽**에서 스크롤
- 가운데는 이동 버튼(선택 항목을 반대편으로)

저장 시 `useSoldOutDraft`가 repository에 맡기고,
실패하면 draft를 **이전 스냅샷으로 롤백**한다 (아래 QA 치트).

---

## 9. 화면별 페이지네이션 (의도)

공통:

- UI: `AdminPagination.jsx`
- 로직: `usePagination(items, { pageSize })`
- 설정: `src/constants/pagination.js` 의 `ADMIN_PAGINATION`

```text
orders     → pageSize 15  (주문 테이블)
liveOrders → pageSize 3   (Live 카드, 좌우 넘김)
soldOut    → pageSize 12  (품절 좌/우 그리드)
menus      → pageSize 12  (메뉴 4열×3행 느낌)
```

### 왜 “전역 기본 10개”로 안 묶나

화면마다 카드/행 밀도가 다르다.
Live는 카드가 커서 3장, 주문 표는 15행처럼 **시안에 맞게 화면 키로만** 맞춘다.
`usePagination`에 pageSize를 안 넘기면 에러를 내서, “깜빡하고 전역 기본에 의존”하는 실수를 막는다.

> 구현이 화면마다 조금씩 진행 중일 수 있다. **의도**는 “공통 훅 + 화면별 설정”이다.

---

## 10. 달력 (`AdminDatePicker`)

파일: `src/components/admin/AdminDatePicker.jsx`

| mode | 용도 |
|------|------|
| `single` | 하루/한 달 점프 (일별·월별) |
| `range` | 시작~끝 (매출 요약·주문 필터) |

- `open` + `onClose` + `onChange`
- **적용** 누르기 전까지는 draft만 바뀜

### 매출 요약에서

1. 기간 탭(오늘/주/달) → KPI·차트는 `getSalesSummary(period)`
2. 달력 기간 → **하단 일자별 표**만 `daily.rows` 필터
3. 탭을 다시 누르면 커스텀 기간 해제

### 주문 관리에서

날짜를 고른 뒤 **조회**를 눌러야 `appliedFilters`에 반영된다.
**draft(작성 중)** 와 **applied(실제 조회)** 를 나눈 이유를 기억하자.

---

## 11. QA 치트 (sessionStorage)

브라우저 개발자 도구 콘솔에서:

```js
// 저장 실패 → 품절·결제·주문상태 저장이 실패하고 draft 롤백되어야 함
sessionStorage.setItem("asak_mock_fail_save", "1");

// Live 빈 목록 / 에러 UI
sessionStorage.setItem("asak_live_fixture", "empty");
sessionStorage.setItem("asak_live_fixture", "error");

// 해제
sessionStorage.removeItem("asak_mock_fail_save");
sessionStorage.removeItem("asak_live_fixture");
```

코드 위치:

- 저장 실패 플래그: `adminMockRepository.js` (`asak_mock_fail_save`)
- Live fixture: `LiveOrderPreview.jsx` (`asak_live_fixture`)

**공부 포인트:** “실패 UI”와 “빈 목록 UI”는 다르다. empty는 에러가 아니다.

---

## 12. 자주 헷갈리는 포인트

1. **`getMonth()`는 0부터** → 화면에 보여줄 때 `+1`. `getFullYear()`는 +1 하지 않음.
2. **`onClick={handleMonth("prev")}`** → 렌더 시 즉시 실행.
   올바른 예: `onClick={() => handleMonth("prev")}`
3. **envelope vs data** — repository는 `{ success, data }`, Page는 보통 `data`만.
4. **매출 `chartBars`** — mock 값이 **막대 높이(px)** 인 경우가 있다. 금액이 아닐 수 있음.
5. **주문 상태 CSS** — mock은 `RECEIVED`, CSS는 `received` → `OrderStatusBadge`가 맞춤.
6. **금액 필드** — 목표 이름은 `totalAmount`일 수 있으나, **현재 mock은 `totalPrice`** 인 곳이 많다. `public/mocks/README.md` 표를 본다.
7. Canonical 문서 경로(`/orders/live` 등)와 코드 kebab-case(`/`)가 다를 수 있다. **실행 정본은 코드 라우트** (`AdminApp.jsx`).

---

## 13. 매출 JSON 키 (외우기용)

```text
sales.summary.data.periods.today|week|month|empty|partial
  → kpis, chartBars, paymentShare, orderShare, ranking, dateRange

sales.daily.data
  → rows[]            날짜별 합계
  → hourly[date][]    시간대
  → breakdown[date]   결제/주문유형 비중
  → ranking[date][]   메뉴 순위

sales.monthly.data
  → year, rows[] (month: "2026-07")
  → ranking["2026-07"][]
```

헬퍼: `src/utils/salesDisplay.js` (날짜 포맷, 막대 높이, 전일 대비 % 등)

필드 상세는 `public/mocks/README.md`가 정본에 가깝다.

---

## 14. 앱 진입 흐름 (큰 그림)

```text
main.jsx
  → AdminApp.jsx          URL ↔ 페이지, CSS 로드, 로그인 가드
  → layouts/AdminLayout   사이드바 + .admin-main
  → pages/admin/*.jsx     조합만
  → components/admin/*    UI
  → hooks/*               조회·draft
  → mocks/adminMockRepository.js
  → public/mocks/asak-admin-data.json
```

세션: `src/auth/adminSession.js` (localStorage mock).
보호 경로는 비로그인 시 로그인 화면으로 보낸다.

---

## 15. 아직 실서버가 아닌 것 (기대치)

- 메뉴 저장/삭제 → toast stub
- 결제 POLICIES 본문 수정 → 정적일 수 있음
- 대시보드 전주 대비 → mock에 값 없으면 `—`
- Live WebSocket → 폴링/수동 refresh 수준
- Backend business API → 아직 붙이지 않는 전제(BLOCKED일 수 있음)

“버그”가 아니라 **목업 범위**인 경우가 많다.

---

## 16. 작은 연습문제

1. 매출 요약에서 달력으로 `2026-07-05 ~ 2026-07-08`을 고르면 하단 표에 며칠이 보이는지 세어 보라.
2. 주문 관리에서 상태를 `PREPARING`만 고르고 조회한 뒤, 상세에서 상태 변경이 보이는지 확인하라.
3. `asak_mock_fail_save=1` 켠 채로 품절 저장 → 목록이 되돌아가는지 확인하라.
4. `OrderListPage`와 `MenuManagePage`를 나란히 열고, “Page가 조합만 하는지” 줄을 세어 보라.
5. (코드) `ADMIN_PAGINATION`에서 Live와 주문의 `pageSize`가 다른 이유를 한 문장으로 설명해 보라.

---

## 17. 다시 볼 파일 (복습 체크)

- [ ] `src/pages/admin/OrderListPage.jsx` — 가장 얇은 Page
- [ ] `src/pages/admin/MenuManagePage.jsx` — 목록 + 우측 패널
- [ ] `src/mocks/adminMockRepository.js`
- [ ] `src/hooks/useSalesQuery.js` / `useOrdersQuery.js` / `usePagination.js`
- [ ] `src/constants/pagination.js`
- [ ] `src/components/admin/AdminDatePicker.jsx`
- [ ] `src/apps/AdminApp.jsx` — 라우트 + CSS import 순서
- [ ] `src/styles/global.css` · `admin/base.css` · `commonStyle.css`
- [ ] `src/styles/admin/sold-out.css` — 좌중우
- [ ] `public/mocks/README.md` — 필드 사전
- [ ] `src/STRUCTURE_GUIDE.md` — 짧은 지도

---

## 18. 3줄 요약

1. **Page는 조립**, 데이터는 **Hook → Repository → JSON**.
2. CSS는 **tokens → reset → global → commonStyle**, 셸은 **뷰포트 · 안쪽만 스크롤**.
3. QA는 **sessionStorage 플래그**로 실패/빈 목록을 연습한다.
