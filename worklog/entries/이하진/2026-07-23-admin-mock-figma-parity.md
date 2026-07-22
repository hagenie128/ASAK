# 2026-07-23 Admin mock·Figma 정합

> **일일:** [2026-07-23](../../daily/이하진/2026-07-23.md)  
> **이전 흐름:** [2026-07-21 mock 바인딩](../../daily/이하진/2026-07-21.md) → [2026-07-22 문서 동기화](../../daily/이하진/2026-07-22.md) → **오늘 코드·Figma 정합**

---

## 1. 기본 정보

- 작업 날짜: 2026-07-23
- 담당자: 이하진
- 저장소: `ASAK-Admin` (+ `ASAK` worklog/docs)
- 브랜치: `feature/admin-mock-figma-parity`  
  - ASAK_Admin 원격에 push 완료  
  - **main에는 머지하지 않음** (피처 브랜치로만 보관)
- 관련 WBS / 화면: WBS2-039~043, SCR-016·018~022 (보조로 SCR-010·011·009)
- 관련 이슈: [Admin #1](https://github.com/hagenie128/ASAK_Admin/issues/1)
- Figma 정본 파일: `yHhvn5RKjBd91U8BJUQz7F` (0718 Admin)
- 작업 유형: `feature` / `refactor` / `fix` / `docs`

---

## 2. 작업 목적

### 해결하려던 문제

1. **7/21~22 기준** Admin은 주문·품절·결제수단 mock 1차 연결까지였고, **매출 3화면·메뉴**는 정적/문서 상태였다.
2. Page가 UI를 한 파일에 다 그리는 화면이 남아 있어, 주문 목록처럼 **Page=조합(assembly)** 규칙을 메뉴·대시보드에도 맞출 필요가 있었다.
3. Figma 0718의 DatePicker·Detail·재료 모달·Shared·결제수단과 코드/mock이 어긋나 있었다.  
   특히 결제수단 mock이 **8종**인데 SCR-018 Default는 **4종**이었다.
4. KEEP QA(`3006:40067`)에서 loading/empty/confirm이 화면마다 제각각이었다.
5. 뷰포트만 키우면 UI가 커 보여, 태블릿 **1920×1080** 시안과 맞지 않았다.

### 기대 결과

- 매출 요약·월별·일별이 mock + 기간/일자 필터로 동작한다.
- 메뉴는 목록 + 우측 Detail/Edit 패널 + 재료 모달로 조합된다.
- 대시보드 최근 주문이 주문 관리와 **같은 소스**(`getAdminOrders`)를 쓴다.
- Shared `AdminAsyncState` / `AdminConfirmDialog`가 주요 화면에 붙는다.
- 결제수단이 Figma 4종·순서로 맞는다.
- 작업 결과는 `feature/admin-mock-figma-parity` 브랜치에 올린다.

---

## 3. 직접 구현 영역

### 3-1. 매출 3화면 + AdminDatePicker (SCR-019~021 · WBS2-041~043)

- **목적:** 정적 매출 화면을 mock repository에 연결하고, Figma 기간/일자 네비를 동작시킨다.
- **직접 한 일:**
  - `useSalesQuery`로 repository 조회·로딩·에러 상태를 모은다.
  - `salesDisplay` 유틸로 금액·기간 라벨 표시를 page에서 분리한다.
  - `SalesSummaryPage` / `MonthlySalesPage` / `DailySalesPage`에 mock 바인딩.
  - `AdminDatePicker`
    - **single:** 한달 달력 (일별·단일 일자)
    - **range:** 두달 + 프리셋 (요약 기간)
  - 일별 헤더 라벨: `YYYY.MM.DD (요일)`
  - 일별 연간 달력에서 월/일 선택 흐름 정리
- **CSS 버그 (핵심):**
  - 증상: 한달 달력을 열면 **모든 날짜가 라임색 원**처럼 보임.
  - 원인: `sales-period.css`의 `.sales-daily__date span` 같은 **자손 span 선택자**가 DatePicker 팝오버 안 `span`까지 스타일을 덮침 (특이도 누수).
  - 조치: sales-period 쪽 과도한 자손 규칙 정리 + date-picker 쪽 span 리셋.
- **포트폴리오 요약:** mock 기간 필터 + Figma DatePicker(한달/두달) 연결, CSS 누수 원인 추적.

### 3-2. 메뉴 Page=조립 + Detail/Edit + 재료 모달 (SCR-016 · WBS2-039)

- **목적:** Page가 그리기만 하던 구조를 `OrderListPage`처럼 **조합만** 하게 바꾼다. Figma상 별도 빈 “편집 페이지”가 아니라 **우측 패널**로 신규/수정을 연다.
- **직접 한 일:**
  - `useMenusQuery`
  - `MenuListPanel` / `MenuDetailPanel` / `MenuEditPanel`
  - `MenuManagePage` = thin assembly (어떤 패널을 켤지만 결정)
  - `MenuEditPage` = 모드 wrapper (라우트 호환용)
  - `IngredientSelectModal` — Figma `150:5525` 기준으로 Edit에 연결
  - 저장은 **stub toast**로 유지 (실 API 대기)
- **포트폴리오 요약:** Admin 메뉴 워크스페이스를 목록+우측 상세/편집 조합 패턴으로 재구성.

### 3-3. 대시보드·주문·품절·셸 스케일 (SCR-022 · SCR-010 · SCR-011)

- **목적:** 운영 홈·목록 화면의 데이터 경계와 태블릿 레이아웃을 맞춘다.
- **직접 한 일:**
  - `DashboardPanels` · `SalesShareCard`로 대시보드 섹션 조합
  - 최근 주문 3건 ← `getAdminOrders` (주문 관리와 동일 소스)
  - 품절: `@media` 브레이크 1500→1100, 가로 배치·스크롤
  - 화면별 `ADMIN_PAGINATION` 상수
  - 주문 목록에서 **상태 변경 UI 제거** (표시·필터만 — 시안/범위에 맞춤)
  - Admin 셸: **1920×1080 캔버스 + viewport `scale`**  
    → “창만 키우면 컴포넌트가 커짐”을 막고 시안 비율 유지
- **포트폴리오 요약:** mock 기준 데이터 단일화 + 태블릿 셸 스케일 전략.

### 3-4. Figma 0718 컴포넌트·Shared·KEEP QA

| 노드 | 내용 | 코드 반영 |
|---|---|---|
| DatePicker 한달 `162:15939` | 단일 월 구조·선택 원 | `AdminDatePicker` single |
| DatePicker 두달 `3218:16401` | 두 달 + 프리셋·연녹 바 | `AdminDatePicker` range |
| DetailPanel `150:5418` | default / empty / 취소 | `MenuDetailPanel` 등 |
| IngredientModal `150:5525` | 재료 선택 | `IngredientSelectModal` |
| Admin Components `150:2860` | StatusBadge · SearchInput · Checkbox | 컴포넌트 + CSS 분리 |
| Shared `145:2` | Toast · Confirm · AsyncState | `AdminAsyncState`, `AdminConfirmDialog` |
| Foundations `148:12745` | `--admin-bg-inverse` | tokens |
| State Matrix `191:3` | 상태 표 (문서용) | **UI로 가져오지 않음** |
| KEEP QA `3006:40067` | 전 페이지 갭 | AsyncState 등 Shared 적용 |

### 3-5. P1 — AsyncState · ConfirmDialog · 주문 달력 연도

- **목적:** KEEP QA에 남은 loading/empty/confirm을 Shared로 통일한다.
- **직접 한 일:**
  - `AdminAsyncState` → 주문·품절·메뉴·결제수단 (매출·대시보드는 선반영)
  - `AdminConfirmDialog` → 저장/위험 액션 confirm
  - 주문 화면 달력 **연도 범위** 정리
- **원칙:** 화면마다 스피너 JSX를 새로 만들지 않고 Shared만 재사용.

### 3-6. 결제수단 SCR-018 정합 (WBS2-040 후속)

- **목적:** mock **8종**을 Figma SCR-018 Default(`134:11493`) **4종**에 맞춘다.
- **직접 한 일:**
  - 순서·이름: `card` → `kakao` → `naver` → `zero`
  - 미리보기 토글 UX
  - `AdminAsyncState` + `AdminConfirmDialog` 연결
  - `paymentMethodGlyphs.js`, `payment-methods.css`
  - mocks README에 4종 계약 명시
- **포트폴리오 요약:** 운영 설정 화면을 Figma 계약(개수·순서)과 Shared UX에 맞춤.

### 3-7. CSS 레이어·문서·Git

- CSS 레이어를 Kiosk와 동일하게: `tokens` → `reset` → `global` → `commonStyle`  
  (+ date-picker, status-badge, filters-inputs, ingredient-select, payment-methods)
- `STRUCTURE_GUIDE.md`에 Page=조합 규칙 보강
- 임시 투두/체크리스트 정리 (로컬 개인 메모)
- Git: 브랜치 `feature/admin-mock-figma-parity`를 ASAK_Admin에 push (**main 아님**)

---

## 4. 구현 로직 / 적용한 방식

### 데이터·화면 경계

```text
Page (assembly만)
  → Hook (useSalesQuery / useMenusQuery / useXxxDraft …)
    → adminMockRepository
      → public/mocks/asak-admin-data.json
```

- Page는 “무엇을 보여줄지”만 조합한다. JSON을 직접 import하지 않는다.
- 표시 포맷(금액·날짜·라벨)은 유틸/상수로 밀어낸다.

### Figma → 코드

```text
정본 노드 URL 확정
  → 디자인 컨텍스트 조회
    → 최소 반영 (색·구조·상태)
      → 시안에 없으면 발명하지 않음 (MISSING / State Matrix)
```

### DatePicker

- single = 한달 그리드, 선택일은 `#6c9700` 원
- range = 두 달 + 프리셋, 구간은 연녹 바
- 팝오버는 sales 화면 레이아웃 **밖에** 떠 있으므로, 부모 페이지의 `span` 규칙이 침범하면 안 됨 → CSS 스코프 중요

### 셸 스케일

- 고정 캔버스 1920×1080을 기준으로 두고, 실제 창 크기에 `scale`로 맞춤
- “viewport에 width 100%로 늘리기”와 “시안 픽셀을 유지하기”를 분리

### 결제수단 계약

- **단일 기준:** SCR-018 Default 4종·순서  
- mock JSON·UI 행·README가 같은 계약을 따른다 (8종 잔존 금지)

---

## 5. AI 도움 영역

- **사용한 AI 도구:** AI 코딩 어시스턴트 (대화형 편집·리뷰)
- **어떤 요청을 했는지:**
  - Figma 노드별 DatePicker / Detail / 재료 모달 / Shared 대조 초안
  - 메뉴 Page=조립 리팩터 초안
  - “한달 전부 라임” CSS 원인 후보 정리
  - P1 AsyncState·Confirm을 Shared로만 연결
  - 결제수단 8→4 정렬
- **AI가 도움 준 내용:**
  - 패널 파일 분리 초안, DatePicker 마크업/스타일 초안
  - CSS 선택자 누수 후보 목록
  - KEEP QA 갭을 컴포넌트 단위로 묶는 제안
- **그대로 사용한 부분:**
  - build가 통과하고 시안과 맞다고 확인된 DatePicker 색·구조, Shared 연결부
- **수정·거절한 부분:**
  - Admin 전체 프레임을 DatePicker로 착각한 대조 → 노드 URL 재지정 후 폐기
  - State Matrix를 UI 컴포넌트로 가져오기 → 문서용만
  - 결제수단 장식 아이콘/8종 유지 → Figma 4종만
  - 화면별 스피너 복붙·과도한 새 추상화 → Shared만
  - 메뉴 실 CRUD API 한 번에 생성 → stub toast로 범위 제한
- **배운 점 (AI 활용):**  
  “만들어 줘”보다 **노드 ID·금지 사항(발명 금지)·DONE 금지 원칙**을 먼저 주면 재작업이 줄어든다.

---

## 6. 발생 이슈

### 이슈 1 — 한달 달력 전부 라임 원

- 증상: DatePicker single을 열면 날짜 숫자가 전부 선택 원처럼 보임.
- 원인: `.sales-daily__date span` 등 **페이지 CSS 자손 선택자 누수**.
- 해결: sales-period 규칙 축소 + date-picker span 리셋.
- 공부 포인트: 팝오버/포털 UI는 부모 페이지의 넓은 `span`/`div` 규칙을 특히 조심.

### 이슈 2 — 뷰포트만 키우면 UI가 커 보임

- 증상: 브라우저 창을 키우면 카드·타이포가 시안보다 커짐.
- 원인: 레이아웃이 viewport에 직접 늘어남.
- 해결: 1920×1080 캔버스 + `scale`.
- 공부 포인트: 키오스크/태블릿 Admin은 “반응형 늘리기”와 “시안 스케일”을 구분.

### 이슈 3 — 결제수단 mock ≠ Figma

- 증상: 화면/데이터가 8행, 시안은 4행.
- 원인: mock을 먼저 넓게 넣었고 SCR-018 Default 계약을 나중에 맞춤.
- 해결: `card`→`kakao`→`naver`→`zero`로 JSON·UI·README 정렬.
- 공부 포인트: mock 개수는 화면 SCR Default가 **계약**.

### 이슈 4 — Backend / 저장 stub

- 증상: 저장·환불 등이 실제 서버에 반영되지 않음.
- 원인: business API 미구현 (블로커).
- 대응: repository stub + toast/confirm UX만 완성. 실 adapter는 BLOCKED.

### 이슈 5 — 품절·메뉴 카드 UI (후속 수정 완료)

- 증상: 품절 카드 truncation·배지, 메뉴 카드 이름/가격 wrap이 Figma와 어긋날 수 있음.
- 후속 수정(당일):
  - 품절: 메뉴명 2줄 clamp, mock 재생성·menus sync로 카테고리 배지 다양화
  - 메뉴 목록 카드: 이름 2줄 높이, 가격 `nowrap` + `flex-shrink: 0`
  - `npm run build` 통과
  - 진척 코멘트: [ASAK_Admin #4](https://github.com/hagenie128/ASAK_Admin/issues/4#issuecomment-5050010242)
- 상태: **완료** (더 이상 잔여 UI TODO 아님)

---

## 7. 디버깅 기록

| 증상 | 의심 | 실제 원인 | 다시 보면 볼 곳 |
|---|---|---|---|
| 한달 전부 라임 | DatePicker 선택 state 버그 | `sales-period.css` span 누수 | `sales-period.css`, date-picker CSS, DevTools Computed |
| UI가 창에 비례해 커짐 | rem/폰트 문제 | 셸이 viewport에 직접 flex grow | app-shell / scale 관련 CSS |
| 결제 행 수 불일치 | 컴포넌트 필터 버그 | mock 8종 데이터 | `asak-admin-data.json`, mocks README, SCR-018 |
| 잘못된 Figma 대조 | — | 노드 URL 오지정 | 작업 전 노드 표 고정 |

**다시 같은 CSS 누수가 의심되면:**

1. 팝오버 안 요소를 DevTools로 선택
2. Computed에서 어떤 규칙이 색/원형을 주는지 확인
3. 선택자에 페이지 접두(`sales-daily` 등) + 자손 `span`이 있는지 검사

---

## 8. 이번 작업에서 배운 점 (공부 포인트)

1. **Page=조립:** Page는 hook 결과와 패널을 붙이는 자리. UI 세부·JSON 직접 참조는 금지에 가깝다.
2. **Figma 노드 단위 작업:** 파일 전체가 아니라 DatePicker/Detail 같은 **노드 ID**를 계약으로 삼는다.
3. **발명 금지:** State Matrix·MISSING empty는 문서/QA용이지, 마음대로 UI를 만들지 않는다.
4. **CSS 스코프:** 팝오버는 DOM상 부모 밖일 수 있어도, **선택자 문자열**이 자손을 넓게 잡으면 같이 깨진다.
5. **1차 mock ≠ DONE:** 목록이 보여도 필터·실패 fixture·Figma 개수 계약·Shared 상태가 남으면 IN_PROGRESS.
6. **Shared 재사용:** loading/confirm을 화면마다 새로 짜지 말고 `145:2` 계열을 붙인다.
7. **브랜치 전략:** 큰 Admin 정합 작업은 `feature/admin-mock-figma-parity`처럼 피처 브랜치에 모으고, main과 분리해 둔다.

---

## 9. 개선사항 / TODO

### 아직 임시·stub

- 메뉴/품절/결제수단 **저장 실API**
- 매출 일별 mock 상세(7월 중심) 확장
- 주문 필터 고도화(WBS2-036 후속) — 7/21부터 잔여

### 후속 수정 완료 (당일)

- [x] 품절 카드 truncation(2줄 clamp) / 카테고리 배지 다양화 (mock 재생성 + menus sync)
- [x] 메뉴 카드 이름 2줄 높이 · 가격 nowrap + flex-shrink 0
- 진척: [ASAK_Admin #4 comment](https://github.com/hagenie128/ASAK_Admin/issues/4#issuecomment-5050010242)

### 아직 열림

- Backend business API stub (실 adapter BLOCKED)
- Admin↔Kiosk 결제수단 개수 불일치 (Admin 4종 vs Kiosk 8종 잔존 가능) — 계약 재확인
- 품절 저장 stub가 `menus.isSoldOut`을 갱신하지 않음
- Evidence 원격 반영 (DevCopilot / WBS)

### 다음 스프린트 후보 (P2)

- 결제 정책 수정 화면
- Login Unauthorized 상태
- 메뉴 이미지 폴백
- (선택) `feature/admin-mock-figma-parity` PR 초안

### 구조적으로 아쉬운 점

- range DatePicker 폭(~625px)이 좁은 창에서 잘릴 수 있음 → 위치/스케일 추가 검토
- CSS 레이어는 맞췄지만, 화면별 CSS에 남은 넓은 자손 선택자가 더 있을 수 있음 → 점진적 정리

---

## 10. 검증 내용

### 명령

- `npm run build` — 다수 회차 성공

### 수동 시나리오

| 화면 | 확인 |
|---|---|
| 매출 요약 | 기간 탭 · range DatePicker · 로딩 AsyncState |
| 매출 일별 | single DatePicker · 라벨 `YYYY.MM.DD (요일)` · 라임 원 버그 재발 없음 |
| 메뉴 | 목록 → 보기/수정/신규 패널 전환 · 재료 모달 오픈 |
| 대시보드 | 최근 주문 3건이 주문 목록과 동일 소스인지 |
| 품절 | 가로 배치·페이지네이션·Confirm |
| 주문 | 상태 변경 UI 없음 · AsyncState · 달력 연도 |
| 결제수단 | **4행** · 순서 card/kakao/naver/zero · 토글 · Confirm/toast |
| 셸 | 1920×1080 비율 유지(창 크기 변경 시 scale) |

### Git

- 원격 브랜치 `feature/admin-mock-figma-parity` 존재 확인
- main에 직접 push하지 않음

---

## 11. 포트폴리오용 요약

ASAK Admin 태블릿(1920×1080)에서 매출·메뉴·대시보드까지 mock을 연결하고, Figma 0718 DatePicker/Detail/재료 모달/Shared와 결제수단 SCR-018(4종)을 맞추며, Page=조립 구조와 CSS 선택자 누수·셸 스케일 문제를 직접 정리했다. 작업은 `feature/admin-mock-figma-parity` 브랜치에 모았다.

**한 줄:** Admin mock 전 화면 연결 + Figma 컴포넌트 정합 + Page 조합 + Shared Async/Confirm.

---

## 12. 첨부 / 관련 링크

- **일일 정본:** [2026-07-23 daily](../../daily/이하진/2026-07-23.md)
- GitHub daily: https://github.com/hagenie128/ASAK/blob/main/worklog/daily/이하진/2026-07-23.md
- GitHub entry: https://github.com/hagenie128/ASAK/blob/main/worklog/entries/이하진/2026-07-23-admin-mock-figma-parity.md
- 이전 daily: [07-21](../../daily/이하진/2026-07-21.md) · [07-22](../../daily/이하진/2026-07-22.md)
- Admin 이슈: https://github.com/hagenie128/ASAK_Admin/issues/1
- 브랜치: `feature/admin-mock-figma-parity` (ASAK_Admin, main 아님)
- Figma file: `yHhvn5RKjBd91U8BJUQz7F`
- KEEP QA: `3006:40067` · SCR-018 Default: `134:11493`
- Shared: `145:2` · Admin Components: `150:2860`
