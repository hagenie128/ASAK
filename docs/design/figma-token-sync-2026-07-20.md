# Figma → Code 핸드오프 (내일 구현용)

기준 파일: [ASAK — Design System & Product UI 0718](https://www.figma.com/design/yHhvn5RKjBd91U8BJUQz7F/ASAK-%E2%80%94-Design-System---Product-UI-0718?node-id=134-7720)  
fileKey: `yHhvn5RKjBd91U8BJUQz7F`

## 이미 맞춰 둔 것 (오늘)

| 대상 | 파일 | 내용 |
| --- | --- | --- |
| 1. 토큰 | [`ASAK-Kiosk/src/styles/tokens.css`](../../../ASAK-Kiosk/src/styles/tokens.css) | Figma Variable 실측값으로 교체 (근사값 주석 제거) |
| 1. 토큰 | [`ASAK-Admin/src/styles/app-shell.css`](../../../ASAK-Admin/src/styles/app-shell.css) `:root` | Kiosk와 동일 Semantic 규칙 (`#b5e30f`, Pretendard, Admin text 스케일) |
| 연결 | `commonStyle.css` MenuCard·BottomCTA disabled | 새 토큰 변수 참조 |

**건드리지 않음:** Zustand, 가격/수량 로직, Axios, mock JSON, 나연이 담기 흐름(OrderList 등).

---

## 내일 가져올 것 (체크리스트)

### 2. Button / Bottom CTA / Header — Variant·Disabled·아이콘

| Figma | 코드 연결 | 할 일 |
| --- | --- | --- |
| `Kiosk/Header` `425:54752` | `components/kiosk/Header.jsx` | back/home 60px, 로고 200×68, py 36 수치 재확인 |
| `Kiosk/BottomCTA` `150:385` | `MenuListFooter`, `MenuDetailFooter` | Variant: `twoCTA` / `singlePrimary` / `cartSummary` + `default`/`disabled`/`loading` |
| Shared Button | `components/common/Button.jsx` | Disabled = 정식 Variant (`#d9dee0`/`#99a1a6`), opacity 50% 아님 |

### 3. MenuCard / CartItem / OptionGroup / QuantityStepper

| Figma | 코드 | 할 일 |
| --- | --- | --- |
| `Kiosk/MenuCard` `150:678` | `MenuCard.jsx` | `state=default\|soldOut`만. 표시값은 props 유지 |
| CartItem `150:404` | `CartItem.jsx` | 선택/수량/삭제 UI 상태 — **store 로직은 이미 있음** |
| OptionGroup | `OptionGroup.jsx` + `OptionItem.jsx` | Selected = lime border + subtle fill |
| QuantityStepper | `QuantityStepper.jsx` | `+` = Brand/Primary, `-` disabled = BG/Subtle |

### 4. Toast / Confirm / Loading / Empty / Error

| Figma | 코드 | 토큰 |
| --- | --- | --- |
| Toast | `KioskToast.jsx` | success `#5da45d`, warning `#fbbf24`, overlay elevated |
| Confirm | `KioskConfirmDialog.jsx` | scrim `rgba(0,0,0,0.45)`, danger/warning CTA |
| Loading/Empty/Error | `LoadingSpinner` / `EmptyState` / `ErrorMessage` | MenuList `viewState` + common 컴포넌트 |

### 5. 결제·영수증·접근성

| 화면 | 파일 | 할 일 |
| --- | --- | --- |
| 결제수단 카드 | `PaymentPage.jsx` | selected / disabled 테두리·배경만 |
| 영수증 버튼 | `ReceiptPage.jsx` / `ReceiptActions.jsx` | 선택 상태 |
| 접근성 토글 | `AccessibilityPage.jsx` | on/off (`#6c9700` knob 패턴은 Admin Toggle과 동일) |

### 6. 없는 에셋

`src/assets/figma/`에 없는 아이콘만 Figma MCP asset → 로컬 저장.  
**이미 있는 홈 로고·히어로는 사용자 교체 예정이면 덮어쓰지 말 것.**

후보: qty +/- SVG(이전에 삭제된 적 있음), Confirm/Toast 마크, 결제 브랜드 로고 정본 SVG.

---

## 절대 가져오지 말 것

- 메뉴명·가격·주문번호 하드코딩
- 메뉴/주문 JSON 전체 재생성
- Axios / Zustand / `priceCalculation` / `quantityLimits` 재작성
- 화면 전체 자동생성 React 붙여넣기

---

## 구현 순서 추천 (내일)

1. Header + BottomCTA Variant (눈에 잘 띔)
2. MenuCard soldOut / QuantityStepper
3. Toast·Confirm 상태 색
4. 결제·접근성 선택 상태
5. 빠진 아이콘만 assets에 추가

끝나면 `npm run build` (Kiosk) + Admin 한 번.
