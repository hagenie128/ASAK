# Figma 0718 × 프로젝트 Gap (2026-07-20) — 정정본

정본: [ASAK Design System & Product UI 0718](https://www.figma.com/design/yHhvn5RKjBd91U8BJUQz7F)  
fileKey: `yHhvn5RKjBd91U8BJUQz7F`  
❌ 0715 (`JSrjOy668zhfkiLplCkreh`) 링크 금지

> **정정:** 이전 버전에서 PARTIAL/MISSING을 「UI 미이식」처럼 읽히게 적었다.  
> 코드 실측 결과 **화면 시안·className·에셋·CSS는 이미 이식됨.**  
> 팀이 CSS를 손으로 새로 쓰지 않았고, 스타일은 `commonStyle.css` / `app-shell.css`에 Figma 이식분으로 들어 있다.  
> 아래 Gap은 **로직·API·상태 연결**만 가리킨다.

---

## 1. 결론 (코드 실측)

| 층 | 상태 | 근거 |
|----|------|------|
| **UI 이식** | **대부분 완료** | 페이지 JSX + `assets/figma` + 대형 CSS |
| **키오스크 주문 로직** | Home~Cart **동작** | store / `priceCalculation` / `quantityLimits` |
| **키오스크 결제 이후** | UI 있음 · **선택/API/훅 미연결** | `selectedMethodId = null` 등 상수 |
| **관리자** | UI 있음 · **adapter/API/세션 미연결** | `ui-implementation-map.md` 「정적 UI」 |
| **학습용 자리표시자** | 소수만 | `common/Button.jsx` 주석만, `PaymentMethodList` 81B 등 |

스타일 용량 (손으로 안 썼다는 말과 일치):

- `ASAK-Kiosk/src/styles/commonStyle.css` ≈ 59KB
- `ASAK-Admin/src/styles/app-shell.css` ≈ 89KB
- `tokens.css` ≈ 5.7KB (Variable 실측)

---

## 2. 상태 정의 (다시)

| 표기 | 의미 |
|------|------|
| UI ✅ | 레이아웃·class·에셋·CSS 이식됨 (시안 보임) |
| LOGIC 연결 | 클릭/선택/저장/API가 동작함 |
| LOGIC 대기 | UI는 있으나 disabled·상수·adapter TODO |

---

## 3. 키오스크 — UI ✅ / 로직만 구분

| 화면 | 파일 크기(대략) | UI | 로직 |
|------|-----------------|----|------|
| Home | 0.9KB | ✅ | ✅ 진입 |
| Menu List | 2.7KB | ✅ | ✅ 목록·담기 흐름 |
| Menu Detail | 6.0KB | ✅ | ✅ draft·가격·수량 · EditCartItem 등 일부 상태 대기 |
| Cart | 5.1KB | ✅ | ✅ store · Confirm/Toast 일부 대기 |
| Payment | 6.4KB | ✅ | 대기 — 선택·API (`selectedMethodId = null`) |
| Complete | 2.5KB | ✅ | 대기 — 주문번호 props, 자동복귀 |
| Payment Error | 2.6KB | ✅ | 대기 — 분기·재시도 연결 |
| Timeout | 2.5KB | ✅ | 대기 — idle 훅 |
| Accessibility | 2.6KB | ✅ | 대기 — 전역 적용 |
| Receipt | 2.5KB | ✅ | 대기 — print 분기 |

라우트는 전부 있음 (`KioskApp.jsx`). `/ui-preview`만 제거.

**실제 CTA는** `MenuListFooter` / `MenuDetailFooter` / 각 페이지 footer 버튼 + CSS.  
`components/common/Button.jsx`는 학습용 주석 자리표시자일 뿐, 「버튼 UI가 없다」가 아님.

---

## 4. 관리자 — UI ✅ / 데이터만 구분

`ASAK-Admin/docs/ui-implementation-map.md` 정본:

> 정적 UI 단계 · 이후 데이터 구현자가 adapter/query로 연결

| 화면 | UI | 데이터·동작 |
|------|----|-------------|
| Login | ✅ | 인증·세션 대기 |
| Live Order (`/`) | ✅ | 조회·상태전이·TTS 대기 |
| Dashboard | ✅ | KPI adapter 대기 (목업 상수) |
| Orders | ✅ Preview | 필터·상세 query 대기 (`OrderDetailPage` 파일은 있음) |
| Sold-out | ✅ | draft·저장 mutation 대기 |
| Menus / Edit | ✅ | 조회·폼·저장 대기 |
| Payment Methods | ✅ | 토글·저장 대기 (버튼 disabled) |
| Sales / Daily / Monthly | ✅ | 기간·adapter 대기 |

hooks/api/adapters/types 다수 = **자리표시자 주석** (UI와 별개).

---

## 5. 진짜로 얇은 파일 (UI 이식과 무관·학습용)

| 파일 | 크기 | 비고 |
|------|------|------|
| `PaymentMethodList.jsx` | ~81B | 자리표시자 — **PaymentPage가 카드 UI를 직접 그림** |
| `ReceiptActions.jsx` | ~93B | 자리표시자 — Receipt 페이지에 UI 있음 |
| `common/Button.jsx` 등 | 주석 | 화면 footer가 실제 CTA |
| `UiStatePreviewPage.jsx` | 힌트 | 라우트 제거됨 |

→ Gap Matrix에서 이들을 MISSING으로 적어 「화면이 없다」처럼 보이게 한 것은 **오해**.

---

## 6. 수요일에 할 일 (UI 다시 이식 ❌)

UI를 갈아엎지 않는다. **연결만** 한다.

**나연:** Payment 선택 상태 · 결제 mock · Complete 주문번호 · Error/Timeout 훅  
**하진:** 세션 · Live 상태변경 · 주문상세 query · 품절 저장 · 매출 날짜 · 메뉴편집 저장

Figma에서 추가로 볼 것: Variant 미세 차이·상태 프레임 대조 (이미 있는 CSS 위 조정).

---

## 7. 관련

- [figma-0718-page-map.md](./figma-0718-page-map.md)
- [ui-index.md](../../../ui-index.md) — 「미구현」열 = **데이터/동작**, UI 파일 없음이 아님
- [ui-implementation-map.md](../../../ASAK-Admin/docs/ui-implementation-map.md)
