# ASAK Figma 디자인 피드백 — 컴포넌트·스크린 전수 (수치 기준)

**작성일:** 2026-07-17  
**파일:** `JSrjOy668zhfkiLplCkreh` (ASAK — Design System · Product UI)  
**측정 기준 페이지:** `02-C` Shared / `03-C` Kiosk / `04-C` Admin / `05-C` Kiosk Screens / `06-C` Admin Screens  
**방법:** Figma Plugin API 읽기 전용 실측 (쓰기 0회)  
**전제 (F-ARCH-1 이후):** Production 페이지에서 완료 Sandbox는 `92-Archive`로 이동된 상태

> **스크린 프레임별 정밀 실측표:** [`ASAK_FIGMA_DESIGN_FEEDBACK_SCREENS_DETAIL_2026-07-17.md`](./ASAK_FIGMA_DESIGN_FEEDBACK_SCREENS_DETAIL_2026-07-17.md)  
> (이 문서 4~5장의 ID·우선순위만으로는 부족했던 부분을, 05-C 57프레임 + 06-C 전수 수치표로 보완)

---

## 0. 읽는 방법 · 환경 전제

### 0.1 두 제품의 물리 환경이 다름

| | 키오스크 | 관리자 |
|---|---|---|
| 대표 프레임 | **1080×1920** (세로) | **1920×1080** (가로) |
| 입력 | 손가락 터치 | 마우스·트랙패드·(태블릿 터치 보조) |
| 시청 거리 | 팔 길이 ~ 서서 조작 | 책상 앞 40~70cm |
| 최소 터치 | **48×48** (필수), 핵심 조작 **56~64** 권장 | 클릭 타깃 32~40도 가능, 터치 보조면 44+ |
| 본문 최소 글자 | **16px 이상** 권장 | **13~14px** 본문 가능, **12px**는 caption/badge만 |
| 밀도 | 여유 있게 (허전함보다 터치 여유 우선) | 정보 밀도 높여도 됨 |
| 브랜드 표현 | CTA·선택에 라임 크게 | 내비·포인트에만, 본문은 뉴트럴 |

### 0.2 피드백 → 스크린 반영 원칙

1. **Master를 고치면** `05-C` / `06-C` Production Instance에 전파된다.  
2. 스크린만 고치면 Master와 어긋나 **재발**한다.  
3. 아래 각 항목에 **「스크린 반영」**을 붙였다.  
4. “~한 느낌” 대신 **실측값 → 권장값 → 적용 위치**만 적는다.

### 0.3 공통 토큰 목표 (제안 — 아직 미적용)

| 토큰 | 키오스크 | 관리자(웹/태블릿) |
|---|---|---|
| Type scale | 16 / 20 / 24 / 32 / 40 (+Display 44) | 12 / 14 / 16 / 20 / 24 |
| Line height | 본문 150%, 제목 120~130% (px 고정 가능) | 본문 140~150%, 표 행 20px |
| Letter spacing | 본문 0%, Display만 −1~−2% | 전부 0% 유지 가능 |
| Spacing | 8 / 16 / 24 / 32 / 48 | 4 / 8 / 12 / 16 / 24 |
| Radius | 버튼 12 / 카드 16~24 / 칩 999 | 버튼 8 / 카드 12~16 / 뱃지 100 |
| Brand CTA fill | `#9CC600`(Green/400) 또는 `#B5E30F`+텍스트 `#0D0D0D` | 동일, 단 면적은 작게 |
| Selected | tint `#F5FBE0` + border `#6C9700` 3~4px | tint + border 2~3px |

**금지 (AI 템플릿 느낌):** 퍼플 액센트 남발, Blue `#3B82F6`/`#0088FF` 선택색, 다층 글로우, 화면마다 새 hex, lineHeight AUTO 방치.

---

## 1. Shared 컴포넌트 (`145:2`)

Shared는 키오스크·관리자 **둘 다** 쓴다. 수치를 키오스크 기준으로 키우면 Admin이 과해지고, Admin 기준으로 줄이면 키오스크가 작아진다.  
→ **Variant 또는 size property로 분기**하거나, 키오스크는 별도 Kiosk wrapper를 쓰는 편이 안전하다.

---

### 1.1 `Shared/ConfirmDialog` `158:23975` (12 variants)

| 항목 | 실측 | 판정 |
|---|---|---|
| 크기 | 전 variant **440×248** | Admin 웹에 적절. 키오스크(1080폭)에서는 **너무 작음** |
| pad | **32/32/32/32** | OK (8그리드) |
| gap | **20** | 8그리드 밖 → **16 또는 24** |
| radius | **16** | OK |
| fill | `#FFFFFF` | OK |
| shadow | DROP_SHADOW r6/y2 + r28/y10 | OK |
| title | 16 Medium `#1A1A1A` lh **20px** | Admin OK. 키오스크면 **22~24 / lh 28** |
| desc | 14 Regular `#737373` lh 20px | Admin OK. 키오스크면 **16~18** |
| 버튼 pad | **14/28/14/28**, radius 8 | Admin OK. 키오스크 터치면 높이 **≥56** 권장 |
| primary danger | fill `#EF4444` | OK |
| primary warning | fill `#B5E30F`, 라벨 `#FFFFFF` | **대비 문제**: 라임 위 흰색은 더 위험. 라임 CTA는 텍스트 `#292D30` 또는 `#0D0D0D` |
| letterSpacing | **0%** | OK |
| lineHeight | **전부 명시(20px)** | Shared 중 모범 |

**스크린 반영**
- Admin `SCR-016 Delete Confirm` `241:16747`, Live Order Confirm, Payment Save Confirm 등 → Master만 고쳐도 전파.
- Kiosk Cart Delete Confirm `137:22303`, Clear Cart `272:19493` → **440폭 Dialog를 그대로 쓰면 터치 UX 부족**. 키오스크용 최소 **560~640폭 / 버튼 높이 64** 별도 size 필요.
- type에 `deleteMenu` 있음(12 variants). Production이 `discardChanges+warning`만 쓰면 **type mismatch** — 스크린 Annotation과 Master type 정렬 필요.

---

### 1.2 `Shared/Toast` `158:24049` (10 variants)

| 항목 | 실측 | 판정 |
|---|---|---|
| 크기 | **299×76** (전 size 동일) | Admin OK. 키오스크면 폭 **≥400**, 글자 **≥16** |
| pad | **14/16/14/16** | 14는 4의 배수이나 8그리드 핵심은 아님 → **16/16/16/16** |
| gap | **10** | → **8 또는 12** |
| radius | **12** | OK |
| title | 14 Regular `#292D30` lh 20px | Admin OK |
| success icon fill | `#B5E30F` | OK |
| oddGaps | 2, 10 | 정리 대상 |

**스크린 반영**
- Admin Save Success `241:17521` Toast ≈300×76 — Master와 일치.
- Kiosk quantity limit Toast 프레임 `136:19700` **920×115** — Shared Toast와 **스케일이 다름**. 키오스크는 별도 큰 Toast 또는 size=`kiosk` 필요. 스크린에 작은 299 Toast를 올리면 대비·가독 실패.

---

### 1.3 `Shared/EmptyState` `158:24093` (7 types)

| 항목 | 실측 |
|---|---|
| 크기 | general/cart 등 **400×280**, orders/sales/search **400×216** |
| pad | **40/32/40/32**, gap **16** |
| title 16 / desc 14 / action 14 | lh 20px 명시 |
| action 기본 문구 | **「새로고침」** (전 type 동일 기본값 의심) |

**피드백**
- type별 문구 Property가 화면에서 덮어쓰이는지 확인. Menu Empty는 CTA가 「새 메뉴 추가」여야 하는데 Master 기본이 「새로고침」이면 **스크린 Content QA 재발**.
- radius 0 + 회색 아이콘 `#E5E7EB` — 기능은 OK, 개성은 약함. 아이콘만 브랜드 연한 라임 링 정도는 가능 (과한 일러스트 금지).

**스크린 반영:** Admin Empty `241:21716`, Kiosk Cart Empty `134:8085`, Menu List Empty `134:8073`.

---

### 1.4 `Shared/ErrorState` `158:24161` (7)

| 항목 | 실측 |
|---|---|
| page | 480×248 pad 32, title 16, desc 14, CTA 라임 `#B5E30F` |
| section | 360×248 |
| inline | 280×172 pad 16, title **14**, desc **12** |

**피드백:** inline 12px는 Admin section용으로만. 키오스크 Error 화면(`136:16319` 등)에 inline을 쓰면 실패.

---

### 1.5 `Shared/LoadingState` `158:24192` (4: card/table/page/button)

| 항목 | 실측 |
|---|---|
| card | 300×184 radius 12 pad 16 gap 12 fill `#FFFFFF`, skeleton `#F5F5F5` |
| 텍스트 | **0개** (순수 스켈레톤) |

**피드백:** OK. Admin Loading `241:22038`에 card/table이 맞게 쓰이는지 스크린에서 Instance 확인.

---

### 1.6 `Shared/Modal` `158:23908` (paymentError/timeout/information)

| 항목 | 실측 |
|---|---|
| 크기 | 480×196 pad 32 radius 16 |
| title | **22 Bold** lh 28px `#0D0D0D` |
| desc | 16 Regular lh 24px |
| primary | 라임 `#B5E30F` 위 텍스트 `#0D0D0D` | ← ConfirmDialog warning보다 **올바른 CTA 대비** |

**피드백:** ConfirmDialog warning primary를 Modal과 같이 **라임+다크텍스트**로 통일.

**스크린:** Kiosk Timeout `134:7913`, Payment Error `134:7900`.

---

### 1.7 `AllergenNotice` `158:24225` / `AllergenTag` `158:24215`

| 항목 | 실측 |
|---|---|
| Notice | 480×76 pad 16 radius 8 fill `#F5F5F5`, title 14, desc **12** |
| Tag | 61×32 pad 6/12 radius 4, label 14 |

**피드백 (키오스크):** desc 12px → **최소 16**. Tag 높이 32는 터치 비대상(표시용)이면 OK.  
**스크린:** Menu Detail Allergy `230:15336`, Accordion.

---

### 1.8 Icons `CaretLeft/Right` `158:24226/7`, `Placeholder` `171:4843`

| 항목 | 실측 |
|---|---|
| Caret | 32×32 fill `#E6E6E6` radius 4 |
| Placeholder | 32×32 fill `#E0E0E0` radius 16 |

**피드백:** 아이콘 배경이 연회색이라 “비활성 버튼”처럼 보임. 키오스크 헤더 뒤로가기는 **최소 48 hit area** + 아이콘 24~28.

---

## 2. Kiosk 컴포넌트 (`150:2`) — 터치·세로 1080 기준

---

### 2.1 `Kiosk/MenuCard` `150:678` (default / soldOut)

| 항목 | 실측 | 권장 |
|---|---|---|
| 크기 | 305×369 | 스크린 그리드에 맞게 유지 가능 |
| radius | **0** | 카드로 쓸 거면 **16**, 아니면 “카드가 아님”을 문서화 |
| pad/gap root | 0 | 내부 gap **4**만 |
| 이름 | 30 Medium `#292D30` lh **AUTO** | lh **36~40**, tracking 0 |
| 가격 | **38 Bold `#6C9700`** lh AUTO | OK (브랜드 가격색). lh **44** |
| kcal | 28 Regular `#888888` | 키오스크에서 28은 큼 — 위계상 **20~24**로 내려 가격을 더 돋보이게 |
| soldOut | 이미지만 흑백, **텍스트 색 동일** | 이름·가격·kcal를 `#9CA3AF`로 다운, 또는 opacity 0.5 |
| 품절 뱃지 | 24 Bold 흰글자 | OK |

**색:** 이미지 placeholder `#F5FBE0` flat — soft radial 1단 또는 shadow r8/y4 수준만.  
**스크린:** Menu List `134:7792`, Sold-out `224:13539` — Master 수정이 그리드 전체에 전파.

---

### 2.2 `Kiosk/BottomCTA` `150:385` (9 variants)

| 항목 | 실측 | 권장 |
|---|---|---|
| 바 크기 | **1080×180** | 스크린 하단 고정. Order Complete 등에서 940×200 보고 이력 있음 → **Instance override 금지**, Master 180 유지 |
| pad | **40/48/40/48** (cartSummary는 T/B **30**) | 30 → **32**. 48 OK |
| gap | 32 | OK |
| 바 fill | `#FFFFFF` | OK |
| stroke | `#E6E6E6` **1px**, **effects 없음** | border-top **2px `#E5E7EB`** 또는 shadow r8/y−4 |
| 라벨 | **34 Bold** `#292D30` lh AUTO | lh **40**. 34는 키오스크에 적절 |
| primary 버튼 | lime Frame **476×100** radius **15**, 텍스트 `#292D30` | radius **12 또는 16**으로 통일. 15는 비체계 |
| secondary | 비라임(추정 stroke 버튼) | 높이 primary와 **동일 100** 유지 |

**트렌드:** 하단 전체를 라임 블록으로 칠하지 말고(현재는 흰 바+라임 버튼 — 이미 나은 편), **버튼을 inset round**로 유지.  
**스크린:** 거의 모든 SCR-003~008. Master 1회 수정 = 전 화면.

---

### 2.3 `Kiosk/CartItemCard` `150:404` (Default/Disabled/SoldOut)

| 항목 | 실측 | 권장 |
|---|---|---|
| Default | 960×515 radius **24** stroke `#F5F5F5` **2px** | radius OK |
| Disabled | 960×**627** | 상태마다 높이 다름 — 레이아웃 점프. 최소 높이 고정 검토 |
| 텍스트 | Default **38개 전부 lh AUTO** | 전면 명시화 |
| fontSizes | 13,20,24,26,28,32,36 | → **16/20/24/32**로 축소. **13px 옵션수정/삭제 금지**(키오스크) |
| gaps | 0,8,10,12,14,16,20,22,24,40 | **10·14·22 제거** |
| Blue | Vector stroke `#3B82F6`, fill `#0088FF`, Admin/MenuButton stroke | **P0 제거** → 브랜드 그린/뉴트럴 |
| Disabled 타이포 | 19/21 등 중간값 | 20/24로 스냅 |

**스크린:** Cart `134:7835`, Item Sold-out `303:17658` 등. Blue는 Production에서 즉시 보임.

---

### 2.4 `Kiosk/Category` `150:700` / `CategoryTab` `150:695` / `CategoryTap` `150:737`

| 컴포넌트 | 실측 | 문제 |
|---|---|---|
| Category page=K | 1080×117 pad 32/48, 탭 텍스트 **32**, lh AUTO | OK 스케일 |
| Category page=A | 1080×58 pad 8/12, 텍스트 **14** | Admin용? 키오스크 페이지에 혼재 — **이름·용도 분리** |
| CategoryTab | 128×52, 텍스트 30 | 높이 52 ≥48 OK |
| CategoryTap | Size=s **25×11**, 14px / active **15px** | **이름 오타 Tap/Tab**. 25×11은 터치 불가 — Deprecated 또는 Admin 전용으로 격리 |
| 레이어명 버그 | 여러 텍스트 노드 name이 「포케볼」인데 characters는 랩&롤/음료 | **Property 바인딩/이름 정리** |

**스크린:** Menu List 카테고리 바. CategoryTap이 Production에 쓰이면 **터치 실패**.

---

### 2.5 `Kiosk/Header` `425:54752`

| 항목 | 실측 |
|---|---|
| 크기 | **1080×140** |
| pad | **0/48/0/62** (좌우 비대칭 48 vs 62) |
| 텍스트 | 0 (아이콘·로고만) |

**피드백:** 좌우 패딩 **48/48 또는 60/60**으로 대칭.  
**스크린:** Detail/Cart/Payment 공통 헤더.

---

### 2.6 `Kiosk/HomeActionButton` `150:718`

| 항목 | 실측 | 권장 |
|---|---|---|
| 크기 | 444×450 | OK (홈 2분할) |
| 한글 | **44 Bold** `#292D30` lh AUTO | lh **52**, tracking **−1%** |
| 영문 | 26 Regular `#888888` | OK 보조 |
| radius | 0 | 카드감 필요 시 **24** |

**스크린:** Home `134:7721` — 첫인상. flat보다 이미지·약한 elevation 1단이 “매장 키오스크”다움.

---

### 2.7 `Kiosk/MenuDetailSummary` `160:1734` (5 states)

| 항목 | 실측 | 권장 (키오스크) |
|---|---|---|
| default | 480×403 pad 20/24 | |
| badgeText | **11 SemiBold `#EF4444`** | **≥16**, 색은 레드 남발 대신 `#243300` on `#E2FF99` 검토 |
| menuName | 20 Bold | **28~32** |
| description | 14 | **16~18** |
| calories | **13** `#888888` | **16** |
| price | 18 SemiBold | **24~28** |
| optionSummary | **13 `#3B82F6`** | **Blue 금지** → `#6C9700` 또는 `#737373` |
| 다른 variant | 1080×320, 이름 36, 가격 **48**, BEST `#FF0004` | variant 간 스케일 폭주 — **하나의 type scale로 통합** |

**스크린:** Menu Detail `134:7810` (P0 구조 이슈와 별개로 타이포 최소 크기 적용).

---

### 2.8 `Kiosk/OptionGroup` `160:1764`

| 항목 | 실측 | 권장 |
|---|---|---|
| 크기 | 960×139 pad 16/24 gap 12 | OK |
| title | 16 Bold | 키오스크 **22~24** |
| required | **12 SemiBold `#EF4444`** | **16** |
| description | **13** `#888888` | **16** |
| lh | AUTO 100% | 명시화 |

---

### 2.9 `Kiosk/OptionSelectionRow` `160:1831` (15 variants)

| 항목 | 실측 | 권장 |
|---|---|---|
| 크기 | **432×80** (구 피드백의 112와 다름 — 현재 80) | 터치 **≥80 유지**, 여유면 88~96 |
| pad | **30/16/30/16** | 상하 30 vs 글자 15 → 허전. **20/20/20/20** + 글자 **18~20** |
| default fill | `#F5F5F5` | OK |
| selected fill | `#F5FBE0`, **stroke 없음** | **border 3px `#6C9700`** 또는 `#B5E30F` 추가 |
| label | **15** Regular | **18 Medium** |
| price | **14** | **16** |
| lh | AUTO | 명시 |

**참고:** `Kiosk/OptionCard`는 현재 `03-C`에서 **missing** (D1-B Sandbox로 Archive 이동). Production Detail이 OrderDetailRow/일반 Frame을 쓰면 스크린 정본화 Batch와 연동.

**스크린:** Detail 옵션 영역 전반. selected 인지 강화는 **스크린 QA에서 가장 체감 큼**.

---

### 2.10 `Kiosk/OrderDetailRow` `150:247` (7) — Legacy 성격 강함

| 항목 | 실측 | 권장 |
|---|---|---|
| 크기 | 298×92 radius 12 pad 12/16 gap **14** | gap **12 또는 16** |
| 추천 뱃지 | **10 Bold** | **≥14** (키오스크) |
| kcal/protein | **12** | **≥16** 또는 정보 과다하면 키오스크 카드에서 숨김 |
| lh | 55% AUTO / 일부 28px·24px | 통일 |
| selected/pressed | fill `#F9FFE6` stroke `#80B200` | PaymentMethodCard와 토큰 통일 (`#F5FBE0` + `#B5E30F`) |

**스크린:** Menu Detail Default `134:7810`에 46개 오용(P0). **디자인 polish 전에 구조 교체가 우선**.

---

### 2.11 `Kiosk/OrderSummaryInfo` `150:182`

| 항목 | 실측 |
|---|---|
| 접힘 | 920×114 radius 16 stroke `#F5F5F5` 1.5, 텍스트 28~30 흰글자 lh AUTO |
| 펼침 | 920×329 pad **0/31/24/31** (31 비체계) → **32** |
| gap | **5** 포함 → **4 또는 8** |

**스크린:** Payment Summary `134:7861` / `134:7875`.

---

### 2.12 `Kiosk/PaymentMethodCard` `150:3` (24)

| 항목 | 실측 | 권장 |
|---|---|---|
| selected L | 920×240 pad 40 radius **24** fill `#F5FBE0` stroke `#B5E30F` **4px** shadow r20/y10 | **선택 패턴의 모범** — OptionSelectionRow·OrderDetailRow가 이걸 따를 것 |
| title | 36 Bold lh AUTO | lh 44 |
| subtitle | 24 Regular `#737373` | OK |

---

### 2.13 `Kiosk/QuantityStepper` `150:166`

| 항목 | 실측 | 권장 |
|---|---|---|
| 전체 | 176×80 | OK |
| ± 버튼 | **64×64** radius 8 | **터치 기준 PASS** |
| plus fill | `#B5E30F` | OK |
| minus fill | `#33383D` | OK |
| 숫자 | 18 Bold | **20~22** 가능 |

**스크린:** Detail·Cart 수량. 52px 이슈는 과거 오판 — **현재 64 PASS**.

---

### 2.14 `Kiosk/SoldOutBadge` `311:1789` / `StepIndicator` `150:359` / `AllergyAccordion` `160:1852`

- SoldOutBadge: MenuCard와 조합 — 텍스트 다운톤과 세트 mid.
- StepIndicator: 결제 스텝 — 실측 시 작은 라벨 있으면 16+.
- AllergyAccordion: Notice 12px 문제와 동일하게 **스크린 Expanded `136:19707`**에 반영.

---

### 2.15 `Shared/CartFooterBar` `150:655` (Kiosk 페이지에 위치)

키오스크 풋터 변형. BottomCTA와 **역할 중복** 여부 확인 — 스크린에서 둘 다 쓰이면 높이·라임 CTA 토큰을 BottomCTA와 **동일 숫자**로.

---

## 3. Admin 컴포넌트 (`150:2860`) — 웹·태블릿 1920 기준

Admin은 **12~14px·48행 높이**가 허용된다. 다만 **9~11px 본문급**, **StatusBadge 오라벨**, **Blue/Purple**, **SaveBar 다크**는 웹이어도 결함.

---

### 3.1 `Admin/MenuCard` `150:5194`

| 항목 | 실측 | 권장 (웹) |
|---|---|---|
| selected | 210×296 radius **16** stroke `#B5E30F` **3px** shadow | OK — 키오스크 MenuCard(radius 0)와 **의도적 계층 다름** 문서화 |
| 이름 | **15** Bold "MENU" | 실제 메뉴명 Property, **14~16** |
| 가격 | 14 Bold `#6C9700` | OK |
| 뱃지 | **10px** BEST/NEW/EDITING | 웹 caption **11~12**로. 9 이하는 금지 |
| lh | AUTO 100% | 20px |

**스크린:** Menu Management 그리드 `134:12137` — 현재 placeholder "MENU" 다수.

---

### 3.2 `Admin/MenuIngredientSummaryRow` `784:57899` (core/base)

| 항목 | 실측 | 판정 |
|---|---|---|
| 크기 | 588×88 pad 12 radius 8 | 웹 OK |
| core fill | `#FFE6E7` | Tone 구분 OK |
| 이름 | 14 SemiBold lh **20px** | **모범 (명시 lh)** |
| secondary | 13 Bold | 웹 OK |
| status | 12 | 웹 badge OK |

**스크린:** SCR-016 Save Success `241:17521` 등. Master 품질 양호 — **스크린 Content만** 이슈.

---

### 3.3 `Admin/MenuOptionSummaryCard` `764:1490`

| 항목 | 실측 |
|---|---|
| 288×124 pad 12 radius 8 stroke `#E5E7EB` |
| groupName 16 Medium lh 20 |
| required 13 `#FF1A1D` |
| desc/추천 12 `#8C8C8C` lh 16 |

**피드백:** 추천 문자열 Property — Git `isRecommended`와 매핑은 계약 이슈. 색 `#8C8C8C` vs `#6B7280` 뉴트럴 통일.  
**스크린:** 옵션 그리드 6카드 — 베이스에 드레싱명 복붙은 **스크린 데이터** 문제.

---

### 3.4 `Admin/SaveBar` `150:5115` (4)

| state | fill | 텍스트 |
|---|---|---|
| dirty | **`#292D30`** | 14 `#FFFFFF` + 저장 버튼 `#111827` |
| saving | **`#292D30`** | 14 `#FFFFFF` |
| success | `#F5FBE0` | 14 `#5DA45D` |
| error | `#FFF0EB` | 14 `#EF4444` |

**피드백 (웹):** dirty/saving이 거의 검정 바라 **야간 터미널 톤**. success만 라이트 → 상태 체계 단절.  
권장: dirty = `#FFFBEB` + `#92400E` 텍스트, saving = `#F5F5F5`, success 유지, error 유지.  
radius 12 pad 0/24 높이 56 — 웹 OK. lh AUTO → 20px.

**스크린:** 메뉴/품절/결제수단 저장 플로우 전부.

---

### 3.5 `Admin/Navbar` `150:4739` / `NavItem` `150:5187`

| 항목 | 실측 |
|---|---|
| Desktop | 240×1080 pad 0/20/28/20 gap **28** |
| 활성 | 라임 pill (스크린에서 Home 오활성 보고 있음) |
| 라벨 | 14 Medium, 일부 `#666666` / `#737373` / `#0D0D0D` 혼재 |
| effects | shadow **4개** 중첩 | → **1개**로 |
| gap 10 | odd | → 8/12 |
| NavItem | 100×41 pad 0/24, 14 `#6B7280` | 웹 OK |

**스크린:** 전 Admin SCR. **활성 라우트와 라임 하이라이트 불일치**는 스크린 데이터 이슈로 재스냅샷.

---

### 3.6 `Admin/DataTableRow` `150:2906` / `DataTableRow-Active` `150:4932` / `DataTableHeader` `425:54822`

| 항목 | 실측 | 웹 판정 |
|---|---|---|
| Row 높이 | **48** | OK |
| 셀 텍스트 | **13** lh AUTO | OK (웹). lh **20** 권장 |
| Header | 41h, 라벨 **12 Bold `#6B7280`** | OK |
| Active status | **11 Bold** | OK caption |
| 뉴트럴 | `#111827` vs `#6B7280` | CoolGray 토큰으로 통일 |

**스크린:** Order Management `235:14618` 등.

---

### 3.7 `Admin/StatusBadge` `150:5064` (12) — **P0 결함**

| Role variant | fill | 텍스트 색 | **표시 문자 (실측)** |
|---|---|---|---|
| 핵심 재료 | `#FFF0EB` | `#EF4444` | 핵심 재료 |
| 베이스 재료 | `#EBF5EB` | `#5DA45D` | **「핵심 재료」** ← 버그 |
| 일반/선택 | `#F5F5F5` | `#6B7280` | **「핵심 재료」** |
| 품절 | `#FFF0EB` | `#EF4444` | **「핵심 재료」** |
| 판매중/기본/필수/자동 | `#EBF5EB` | `#5DA45D` | **「핵심 재료」** |
| 추천/토핑 | `#FFFBEB` | `#FBBF24` | **「핵심 재료」** |
| 드레싱 선택 | `#EEE8FC` | **`#6D3FC4`** | **「핵심 재료」** + **퍼플 AI톤** |

공통: **11px**, pad 4/10, radius 100, lh 16px.

**조치:** (1) 각 Role 라벨 문자열 수정 또는 text Property 바인딩 (2) 퍼플 Role 제거→브랜드/성공/경고만 (3) 웹이어도 11은 한계 — **12** 권장.

**스크린:** 메뉴·재료·뱃지 붙은 모든 Admin 화면이 **잘못된 라벨**을 보여줄 위험.

---

### 3.8 `Admin/SoldOutCard` `150:5089`

| 항목 | 실측 | 권장 |
|---|---|---|
| 130×134 pad 0/0/8 gap **6** | gap → **8** |
| 이름 **11** / category **9** / status **9** | **9px 금지**. 최소 이름 13, meta 11~12 |

**스크린:** Sold-out Management `134:11863`.

---

### 3.9 `Admin/DetailPanel` `150:5418`

| 항목 | 실측 |
|---|---|
| 460×540 pad 24/28 radius 12 | 웹 패널 OK |
| 텍스트 | 12~22, **AUTO 100%**, gap에 **10** |
| 제목 | 18 Bold |

**피드백:** lh 명시, gap 10→8/12. 메뉴 Detail 오른쪽 패널(스크린)과 크기 체계 맞출 것 (Save Success 패널 700×1052는 화면 전용 Frame).

---

### 3.10 `Admin/TopHeaderItem` `150:5128`

| 항목 | 실측 | 문제 |
|---|---|---|
| inactive 기본 | fill **`#B5E30F`**, 텍스트 20 `#333`, pad 12/24, radius **30**, gap **10** | 이름 inactive인데 라임 채움 — **state 색 반전 의심** |
| 높이 | 48 | 웹 OK |

**스크린:** 브레드크럼/탭류 — 활성·비활성 색 검증 필수.

---

### 3.11 `Admin/FilterDropdown` `150:5007` / `SearchInput` `425:54820`

| 항목 | 실측 | 웹 |
|---|---|---|
| Dropdown | 90×36 pad 10/14 radius 8, 13/12 | OK |
| Search | 150×39 — **폭 150 너무 좁음** | 스크린에서 **240~320** override 또는 Master 기본폭 상향 |

---

### 3.12 `Admin/SalesMetricCard` `150:2928`

240×120 pad 20 radius 12, 라벨 13, 값 **24** "데이터 연결 예정" — 웹 OK. lh AUTO→명시.

---

### 3.13 `Admin/OrderCard` `150:2956` (주방/라이브)

| 항목 | 실측 | 권장 |
|---|---|---|
| 1열 | 380×822 pad 20 radius 16 | 태블릿 주방 OK |
| 텍스트 | **120개**, AUTO **98%**, sizes 12~32 | 12 남발(65) — 본문 **14**, 메타 **12** |
| gaps | **6, 10, 218** | 218은 버그/스페이서 → 구조 재검토 |
| shadow | **4중** | 1~2중 |

**스크린:** Live Order `134:10607`. 주방 **거리**를 고려하면 12px는 약함 → **14 본문** 권장 (웹 데스크와 달리 태블릿 걸이형일 수 있음).

---

### 3.14 기타 Admin (요약 표)

| 컴포넌트 | 핵심 실측 | 액션 |
|---|---|---|
| OrderActionButtons | 높이 36, 14 Medium | 웹 OK. 환불 `#EF4444` OK |
| Checkbox | 18h+라벨 14 | 체크박스 히트영역 **≥16px 박스**, 행 높이 32+ |
| Pagination | 13px | OK |
| IngredientCard / OptionItemCard | (패턴상 12~14) | SoldOutCard처럼 9px 있는지 확인 |
| PaymentMethodSettingRow / PaymentSaveBar | SaveBar와 톤 통일 | dirty 다크 동일 이슈면 함께 수정 |
| MenuButton | 아이콘형, Blue stroke 이력 | CartItemCard와 함께 Blue 제거 |
| Toggle on/off | 48×28 | 웹 OK, 태블릿 터치면 높이 32+ |

---

## 4. 키오스크 스크린 페이지 (`05-C`) — 프레임별

공통: 대부분 **1080×1920**. Annotation·spec·Toast 조각은 별도.

### 4.1 반영 우선순위 (스크린 × 컴포넌트)

| 우선 | 스크린 | 의존 Master | 수치로 고칠 것 |
|---|---|---|---|
| P0 | `134:7810` Menu Detail Default | OrderDetailRow 오용 | 구조 Batch 먼저, 그다음 type scale |
| P0 | Cart `134:7835` + Sold-out 계열 | CartItemCard | Blue 제거, 13px→16, gaps 정리 |
| P0 | 전 화면 BottomCTA | BottomCTA | elevation, radius 15→12/16, lh |
| P1 | Home `134:7721` | HomeActionButton | lh, tracking, radius |
| P1 | Menu List `134:7792` | MenuCard, Category | soldOut 텍스트 톤, CategoryTap 제거 확인 |
| P1 | Payment `134:7861+` | PaymentMethodCard, OrderSummaryInfo | pad 31→32, 모범 selected 유지 |
| P1 | Timeout/Error Modals | Shared/Modal | 이미 대비 양호 — Confirm과 통일 |
| P2 | Accessibility `134:7972+` | High Contrast 변수 | Semantic 모드 실제 바인딩 여부 |
| P2 | Annotation 프레임들 | — | Archive 후보 (디자인 polish 대상 아님) |

### 4.2 스크린별 체크 (프레임 ID)

**홈·목록**
- `134:7721` SCR-001 Home Default — CTA 44px lh, 버튼 터치면
- `224:12713` Home High Contrast — 대비율 ≥4.5:1 실측
- `134:7792` Menu List Default — MenuCard 305 그리드 간격이 8배수인지
- `134:8073` Empty / `134:8079` Loading / `224:13539` Sold-out / `224:13783` Error
- `272:28883` Category Disabled — CategoryTap 25px 사용 여부 **Fail if yes**

**메뉴 상세 (다수)**
- `134:7810` Default — P0 구조
- `136:16077` Option Selected — selected row border 존재 여부
- `136:16198` Loading / `136:16319` Error
- `230:15336` Allergy — 12px 텍스트
- `230:16459` Menu Sold-out / `272:29048` Ingredient SO / `272:29176` Base SO
- `232:7248`/`232:8370` Limit Toast — Toast 스케일(920 vs 299)
- Edit Cart 계열 `272:24420`~`304:31225` — BottomCTA loading 높이 180 유지

**카트**
- `134:7835` Default — CartItemCard
- `137:22303` Delete Confirm — Dialog **키오스크 크기**
- `272:19493` Clear Cart Confirm — 동일
- `303:17658`/`17985`/`18088` Sold-out — Blue·showEditButton 바인딩

**결제·완료·타임아웃**
- `134:7861`/`7875`/`7889`/`226:4014`/`226:6256` …
- `134:7926` Order Complete — BottomCTA 크기 override 여부 (940×200 금지)
- `134:7900`/`226:6496`/`226:7227` Payment Error
- `134:7913`/`226:7323`/`226:7420` Timeout

**기타**
- `224:10766` ARCHIVED_SCR-001 — Archive 이동 후보
- Annotation `136:19719`, `155:4014`, `__spec` 들 — polish 비대상

---

## 5. 관리자 스크린 페이지 (`06-C`) — 프레임별

공통: **1920×1080**.

### 5.1 반영 우선순위

| 우선 | 스크린 | 의존 Master | 수치로 고칠 것 |
|---|---|---|---|
| P0 | 전 SCR StatusBadge 사용처 | StatusBadge | 라벨 12종 문자열 + 퍼플 제거 |
| P0 | Save 플로우 | SaveBar | dirty/saving 라이트 톤 |
| P1 | `134:12137` Menu Default + `241:17521` Save Success | MenuCard, IngredientRow, OptionCard, Toast | 카드 15/10px, Toast 14 OK |
| P1 | `241:16747` Delete Confirm | ConfirmDialog | type=deleteMenu, 메뉴명 Content |
| P1 | `241:21716` Empty | EmptyState | CTA 「새 메뉴 추가」 vs 「새로고침」 |
| P1 | Live Order `134:10607` | OrderCard | 12→14 본문, gap 218 제거 |
| P2 | Sales/Dashboard | MetricCard, charts | lh AUTO 정리 |
| P2 | Login `134:12033`+ | — | 폼 필드 높이 40+, 14px |

### 5.2 스크린 그룹

**라이브·주문**
- `134:10607` Live Default, `134:11447` Loading, `134:11452` Empty, `134:11468` Error
- `235:6361` Detail Open, `235:9009` Confirm, `235:10132` Saving, `235:11264` Success Toast, `235:11294` Save Error, `235:11324` TTS Toast, `242:16397` New Order
- `134:10630` Order Detail Default
- `235:14618`~`235:16269` Order Management 계열

**품절**
- `134:11863` Default, Empty/Error/Loading, `134:11939` Save
- `241:14211` Changed, `241:14507` Disable-all Confirm, Saving/Toast/Error

**메뉴 관리 (SCR-016)**
- `134:12137` Default — Navbar 활성, MenuCard placeholder
- `134:12328` Detail Add / `134:12668` Detail Edit
- `241:15965` Validation Error
- `241:16747` Delete Confirm
- `241:17178` Save Loading / `241:17521` Save Success / `241:17719` Save Error
- `241:21716` Empty / `241:22038` Loading

**결제수단 SCR-018**
- `134:11493` Default + Toggle/Confirm/Saving/Success/Error/Warning/Loading/Load Error (`243:17279`~`243:17979`)
- PaymentSaveBar ↔ SaveBar 톤 통일

**매출·대시보드**
- SCR-019/020/021/022 전부 1920×1080 — Metric 24px, 표 12~13 OK. lh AUTO만 정리.

**로그인**
- `134:12033` Default, `134:11489` Unauthorized, `250:19761` Validation, `250:19867` Auth Error, `250:19972` Submitting

---

## 6. 색 활용도 — 종합

| 이슈 | 실측 | 키오스크 | 관리자 웹 |
|---|---|---|---|
| CTA 라임 `#B5E30F` + 텍스트 | Modal/BottomCTA는 다크텍스트, Confirm warning은 **흰텍스트** | 다크텍스트로 통일 | 동일 |
| Selected tint `#F5FBE0` | PaymentCard만 stroke 4px | OptionRow에도 stroke | 표 selected는 2px면 충분 |
| Blue `#3B82F6`/`#0088FF` | CartItemCard, MenuDetailSummary optionSummary | **삭제** | **삭제** |
| Purple `#6D3FC4` | StatusBadge 드레싱 | 해당 없음 | **삭제** |
| 뉴트럴 이중 | `#737373` vs `#6B7280` vs `#888888` vs `#8C8C8C` | Semantic/Text/* 3단만 | 동일 |
| SaveBar 다크 | `#292D30` dirty/saving | — | 라이트 계열로 |
| 추천 레드 | `#EF4444` / `#FF0004` / `#FF1A1D` 혼재 | 토큰 1개 | 토큰 1개 |

---

## 7. 글자 크기 · 행간 · 자간 — 종합

| 영역 | AUTO 비율 | 대표 문제 크기 | 조치 |
|---|---|---|---|
| Kiosk 컴포넌트 | MenuCard/BottomCTA/Cart **100% AUTO** | 10~13px 다수 | 최소 16, lh 명시 |
| Admin 컴포넌트 | 대체로 AUTO, IngredientRow/OptionCard/Toast/Confirm은 명시 | **9~11** | 본문 13~14, caption≥11, **9 금지** |
| Shared | Confirm/Toast/Empty **명시 lh** 모범 | Toast 14 | 키오스크 size 분기 |
| letterSpacing | 측정 범위 **거의 전부 0%** | Display 44 | 홈 44만 −1% |

---

## 8. 여백 · 레이아웃 — 종합

| 비체계 값 | 출현 | 치환 |
|---|---|---|
| gap 5,6,10,14,18,22,31 | Kiosk·Admin | 4/8/12/16/24/32 |
| gap 218 | OrderCard | 구조 버그 |
| pad 30 (OptionRow, BottomCTA cart) | Kiosk | 24/32 |
| Header 48 vs 62 | Kiosk Header | 대칭 |
| radius 15 | BottomCTA 버튼 | 12 또는 16 |
| radius 0 vs 16 vs 24 | MenuCard 계열 | 제품별 문서화 후 통일 |

---

## 9. 트렌드 · AI스럽지 않게 (실행 가능한 것만)

| Do | Don't |
|---|---|
| PaymentMethodCard식 **tint+두꺼운 브랜드 border**를 선택 패턴으로 확산 | 퍼플·블루 포인트 |
| SemiBold를 섹션 타이틀에 (Admin IngredientRow가 이미 SemiBold) | Regular/Bold만으로 위계 |
| BottomCTA는 흰 바+inset 라임 버튼 유지 | 하단 전체 네온 라임 도배 |
| 품절은 이미지+텍스트 동시 다운톤 | 이미지만 흑백 |
| 변수 Semantic에 바인딩 | 화면마다 새 hex |
| Admin은 밀도↑, Kiosk는 타깃↑ | 한쪽 스케일을 다른 쪽에 복사 |

---

## 10. 스크린에 바로 쓰기 — 작업 배치 제안

### Batch D-Visual-Kiosk (Master → 05-C 자동 전파)
1. CartItemCard Blue 제거 + font/gap  
2. BottomCTA elevation + radius 15→16 + lh  
3. OptionSelectionRow selected border + pad/type  
4. MenuCard soldOut 텍스트 톤 + lh  
5. MenuDetailSummary 11~13→16+, Blue 제거  

### Batch D-Visual-Admin (Master → 06-C 자동 전파)
1. StatusBadge 라벨 12종 + 퍼플 제거  
2. SaveBar dirty/saving 라이트 톤  
3. SoldOutCard 9px 제거  
4. OrderCard gap 218·본문 14  
5. Navbar shadow 1개·뉴트럴 통일  

### Batch D-Visual-Shared
1. ConfirmDialog warning primary = 라임+다크텍스트  
2. Toast/Confirm **size=kiosk** (선택)  
3. EmptyState type별 기본 CTA 문구  

### 스크린만 손댈 것 (Master 밖)
- SCR-016 추천 복붙 데이터, Delete 메뉴명, Navbar 활성 상태  
- ARCHIVED_ 프레임 Archive  
- Annotation은 polish 비대상  

---

## 11. 메타

| 항목 | 값 |
|---|---|
| 측정 | 2026-07-17, F-ARCH-1 이후 Production 페이지 |
| 쓰기 | 0 |
| Kiosk SCR 프레임(이름 SCR-/Toast 등) | 60+ |
| Admin SCR 프레임 | 70+ |
| OptionCard on 03-C | **missing** (Archive Sandbox 쪽) |

---

## 12. 결론

- **키오스크**는 “작음·AUTO·selected 약함·Blue”가 스크린에서 바로 실패한다. PaymentMethodCard(4px border)를 선택 표준으로 삼을 것.  
- **관리자**는 웹 밀도는 OK이나 **StatusBadge 전 variant 오라벨**, **SaveBar 다크**, **9px**, **퍼플**이 P0.  
- **Shared**는 수치가 가장 깔끔(Confirm/Toast lh 명시) — 키오스크에 넣을 때만 **size 분기**.  
- 모든 시각 수정은 **Master 우선**, 스크린은 전파 결과 스냅샷으로 QA.

---

*끝. 수정 적용은 별도 승인 후 Batch로.*
