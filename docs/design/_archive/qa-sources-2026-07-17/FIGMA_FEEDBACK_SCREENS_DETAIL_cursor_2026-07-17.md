# ASAK Figma 스크린 프레임별 정밀 디자인 피드백

**작성일:** 2026-07-17  
**파일:** `JSrjOy668zhfkiLplCkreh`  
**대상:** `05-C` Kiosk Screens (`134:7720`) · `06-C` Admin Screens (`134:10606`)  
**방법:** 각 Production 프레임(키오스크 1080×1920 / 관리자 1920×1080) Plugin API 실측  
**환경:** 키오스크 = 터치·세로 / 관리자 = 웹·태블릿·가로  
**쓰기:** 0회  

> 이전 문서의 “우선순위 표 + ID 리스트”를 **프레임 단위 수치표**로 대체·확장한 문서입니다.  
> 컴포넌트 Master 피드백은 `ASAK_FIGMA_DESIGN_FEEDBACK_COMPONENT_SCREEN_2026-07-17.md` 참고.

---

## 0. 읽는 법

각 프레임 표 열:

| 열 | 의미 |
|---|---|
| tn | 텍스트 노드 수 |
| AUTO% | lineHeight AUTO 비율 |
| fs | 사용된 fontSize 목록 |
| ≤14/≤11 | 키오스크≤14 · 관리자≤11 개수(스펙 `__spec` 제외 위주) |
| oddGap | 4의 배수 아닌 itemSpacing |
| CTA/Bar | BottomCTA 또는 SaveBar 실측 |
| Dialog/Toast | 있으면 크기·좌표 |
| Inst | 주요 Instance |
| 피드백 | 수치 기반 조치 |

**판정 기준**
- 키오스크: 본문 ≥16, 터치 ≥48, selected는 border 권장, Blue 금지, BottomCTA 1080×180 고정
- 관리자: 본문 ≥13, **9px 금지**, StatusBadge 오라벨 금지, SaveBar dirty≠거의검정

---

## 1. 전역에서 바뀐 사실 (이전 문서 정정)

| 이전 가정 | 2026-07-17 스크린 실측 |
|---|---|
| Menu Detail이 `OrderDetailRow`×46 | **`Kiosk/OptionCard`×46 + `OptionGroup`×7** (Default·다수 Detail 상태) |
| OptionCard가 03-C에 없다 | Production 스크린에는 Instance로 **사용 중** (Master는 Archive/다른 위치 가능) |
| Delete Confirm Dialog 항상 440 | Cart Delete/Last Item는 **680×242**, Clear Cart는 **440×248** — **불일치** |
| Order Complete CTA = Master 180 | **`940×200` Instance override** 확정 FAIL |

---

## 2. 키오스크 스크린 (`05-C`) — 57프레임

### 2.1 SCR-001 Home

| ID | 화면 | tn | AUTO% | fs | ≤14 | oddGap | Inst | 피드백 |
|---|---|---|---|---|---|---|---|---|
| `134:7721` | Home / Default | 6 | 83 | 10,26,44,**64** | 1(spec) | — | HomeActionButton×2 | 한글 **44** lh AUTO→**52**; 영문 26 OK; Display **64** tracking −1% 권장; radius 0→카드감 24 검토 |
| `224:12713` | Home / High Contrast | 6 | 83 | 동일 | 1 | — | 동일 | HC 모드에서도 동일 스케일 — Semantic High Contrast **실제 바인딩 여부** 확인 (수치만 보면 Default와 동일 구조) |

**레이아웃:** BottomCTA 없음(의도). 첫 뷰포트 = 브랜드+2 CTA만 — 구성 OK.  
**색:** 라임은 버튼 Instance 내부 — Home 자체 fill 실측 시 flat 흰 배경 위주.

---

### 2.2 SCR-003 Menu List

공통: Header **1080×140 pad 0/48/0/62(비대칭)**, BottomCTA **1080×180**, effects **0**, CategoryTap×4.

| ID | 화면 | tn | AUTO% | fs 상위 | oddGap | CTA pad | Inst 핵심 | 피드백 |
|---|---|---|---|---|---|---|---|---|
| `134:7792` | Default | 49 | **100** | 30×11,32×10,38×10,28×9 | **2,10** | 30/48/30/48 | MenuCard×9, CategoryTap×4, Qty×2, CartFooter, Category | **P0:** CategoryTap 사용(터치 불가 크기 Master). AUTO 100%. CTA pad 30→32. Header 좌우 대칭. MenuCard lh·soldOut 톤은 Master |
| `224:13036` | Items Added | 49 | 100 | 동일 | 2,10 | 30/48 | 동일+Qty | Default와 동일 이슈 |
| `272:28883` | Category Disabled | 50 | 100 | 동일 | 2,10 | 30/48 | 동일 | Disabled 시각이 CategoryTap에 의존 — **Tab으로 교체 필수** |
| `224:13539` | Sold-out | 46 | 100 | +24(뱃지) | 2,10 | 30/48 | MenuCard×9, SoldOutBadge×3 | 품절 카드 텍스트 다운톤 미적용 시 스크린에서 재확인 |
| `134:8073` | Empty | 17 | 82 | 32×10,14×2 | — | 30/48 | EmptyState, CategoryTap×4 | Empty action **「새로고침」14px** — 키오스크면 CTA≥16·문구 「메뉴 다시 불러오기」 |
| `134:8079` | Loading | 14 | 100 | 32 | — | 30/48 | LoadingState | OK 골격 |
| `224:13783` | Error | 18 | 83 | 14 desc/CTA | — | 30/48 | ErrorState | primaryLabel 14→**18** (키오스크) |
| `224:13293` | Empty Cart Toast | 46 | 93 | +Toast 14/12 | 2,10 | 30/48 | Toast **299×?** | Toast message **12px** + 폭 299 — 키오스크 **최소 폭 480·본문 16** |

---

### 2.3 SCR-004 Menu Detail

공통 패턴(Default류): **OptionCard×46, OptionGroup×7**, Header 140 pad 비대칭, BottomCTA 1080×180 **fx=0**, oddGap **6,18**(±10), required/desc **12~13px** 다수.

| ID | 화면 | tn | AUTO% | ≤14 Tiny | CTA pad | Toast/Dialog | 피드백 |
|---|---|---|---|---|---|---|---|
| `134:7810` | Default | 175 | **18** | 18 (12필수/13설명) | 40/48 | — | **구조는 OptionCard로 개선됨.** 남은 이슈: OptionGroup 필수 **12**·설명 **13**→**16+**; gap 6·18→8/16; Header pad; CTA elevation; OptionCard selected border 스크린 스냅샷 확인 |
| `136:16077` | Option Selected | 178 | 19 | 19 | 40/48 | — | selected 인지 = OptionCard Master에 달림. 스크린에서 stroke 두께 실측 권장 |
| `136:16198` | Loading | 4 | 100 | 0 | 40/48 | — | 본문 거의 비움 — LoadingState 없는 경우도. 스피너만이면 OK |
| `136:16319` | Error | (batch1에 포함) | | | | | ErrorState 스케일≥16 |
| `230:15336` | Allergy Expanded | 178 | 20 | 24 | 40/48 | AllergyAccordion×1 | 알레르기 본문 12~14 → **16**; Accordion 색 `#FFF5ED` 유지 OK |
| `230:16459` | Menu Sold-out | 176 | 19 | 18 | 40/48 | — | Default와 동일 + 품절 CTA 비활성 시각 |
| `272:29176` | Base Sold-out | 179 | 20 | 19 | 40/48 | — | 동일 |
| `272:29048` | Ingredient Sold-out | 179 | 20 | 19 | 40/48 | — | 동일 |
| `232:7248` | Menu Limit Toast | 181 | 19 | 22 | 40/48 | Toast **299×74** @396,1646 | **Toast 너무 작음**(키오스크). y=1646은 CTA(1740) 위 — 위치 OK, **크기 FAIL** |
| `232:8370` | Cart Limit Toast | 182 | 19 | 22 | **30**/48 | Toast 299×74 | CTA pad 30 혼재. Toast 동일 FAIL |
| `272:24420` | Edit Cart Item | 178 | 19 | 19 | 40/48 | — | Default와 동일 타이포 이슈 |
| `272:25534` | Edit / Changed | 178 | 19 | 19 | 40/48 | — | dirty 표시가 타이포만인지 SaveBar 없는지 — 키오스크는 BottomCTA loading으로 처리 |
| `272:25662` | Edit / Save Loading | (동일 계열) | | | | | CTA loading variant 높이 **180 유지** |
| `272:26776` | Edit / Save Error | | | | | | Error Toast 크기 |
| `304:31225` | Discard Confirm | 182 | 19 | 20 | 40/48 | ConfirmDialog | Dialog 폭 실측 필요(440 vs 680). 키오스크 최소 **560~680** |

**색:** Detail 계열 Blue 텍스트 **0** (이전 MenuDetailSummary Master의 `#3B82F6`이 이 스크린 세트에는 안 보임 — OptionCard 경로).

**레이아웃:** clipsContent true. 스크롤 바디는 Header y0–140 / CTA y1740 사이여야 함 — OptionCard 46개로 세로 overflow 정상.

---

### 2.4 SCR-005 Cart

공통: CartItemCard×1~2, **Admin/MenuButton×2~4**, **blueN≈6~12**, 옵션수정/삭제 **13px**, oddGap **10,14,22**, BottomCTA 180 fx0.

| ID | 화면 | tn | AUTO% | blueN | Dialog/Toast | 피드백 |
|---|---|---|---|---|---|---|
| `134:7835` | Default | 89 | 99 | **12** | — | **P0 Blue + Admin/MenuButton 혼입 + 13px 액션.** gaps 10/14/22. AUTO≈100% |
| `137:22946` | Quantity Changed | 87 | 99 | 12 | — | 동일 |
| `137:22916` | Cart Qty Limit Toast | 90 | 99 | 12 | (토스트 프레임 별도일 수 있음) | Blue+13px |
| `137:22727` | Menu Qty Limit Toast | 89 | 99 | 12 | — | 동일 |
| `272:19655` | Option Updated Toast | 91 | 97 | 12 | Toast **299×76** @439,1650 | Toast 소형 + Blue |
| `272:19308` | Item Deleted | 51 | 98 | 6 | — | 카드1장 — Blue 절반 |
| `303:17658` | Item Sold-out | 91 | 99 | 12 | — | Disabled 타이포 19/21 혼재(Master). CTA pad **30** |
| `303:17985` | Sold-out / Edit Required | 92 | 99 | 12 | — | showEdit 정책 스크린 확인 |
| `303:18088` | Checkout Blocked | 94 | 97 | 12 | Toast 299×76 @396,1644 | Toast 소형 |
| `137:22303` | Delete Confirm | 91 | 95 | 12 | Dialog **680×242** @200,839 | Dialog 680은 키오스크에 더 적합. Master 440과 **불일치** — 통일 필요 |
| `305:28064` | Last Item Delete Confirm | 92 | 95 | 12 | Dialog **680×242** | 동일 |
| `272:19493` | Clear Cart Confirm | 92 | 95 | 12 | Dialog **440×248** @320,836 | **같은 Cart 플로우인데 440** — Delete와 크기 불일치 FAIL |
| `134:8085` | Empty | 4 | 25 | 0 | — | Empty CTA 「새로고침」14 — 「메뉴 담으러 가기」+≥18 |
| `272:19649` | Clear Success Empty | 7 | 29 | 0 | Toast 299×76 | Toast 소형 |
| `232:9497` | Last Deleted → Empty | 6 | 17 | 0 | Toast 299×76 | 동일 |

---

### 2.5 SCR-007 Payment

공통: PaymentMethodCard×2, OrderSummaryInfo, StepIndicator, BottomCTA 180, oddGap **5,25,35**, AUTO 100%, fs에 **100** 등장(장식/타이머?).

| ID | 화면 | tn | oddGap | 피드백 |
|---|---|---|---|---|
| `134:7861` | Summary Collapsed | 16 | 5,25,35 | **gap 5/25/35 → 8/24/32.** PaymentCard selected(4px border)는 모범 — 유지 |
| `134:7875` | Summary Expanded | 32 | +10 | 펼침 pad 31 계열(Master) → 32 |
| `226:4014` | Method Selected | 16 | 5,25,35 | 동일 |
| `226:6256` | All Methods Disabled | 16 | 5,25,35 | Disabled 대비·CTA disabled 확인 |
| `134:8091` | Loading | 3 | — | LoadingState OK |
| `226:6374` | Load Network Error | 5 | — | 에러 카피≥16 |
| `134:7889` | Processing | 6 | 25,35 | fs **100** — 큰 숫자 타이머면 lh·tracking 명시 |

---

### 2.6 SCR-008 Order Complete

| ID | 화면 | 실측 | 피드백 |
|---|---|---|---|
| `134:7926` | Default | BottomCTA **`940×200`** (Master 1080×180 대비), fs 36/56/**140**, AUTO 80% | **P0 Instance override.** CTA를 1080×180으로 되돌릴 것. 140px 숫자는 Display — lh·tracking 명시 |

---

### 2.7 SCR-012 Payment Error / SCR-013 Timeout

| ID | 화면 | Dialog | CTA | 피드백 |
|---|---|---|---|---|
| `134:7900` | Payment Declined | Modal **400×220** @340,850 | 1080×180 | Modal 400은 키오스크에 좁음 → **≥480~560**. 본문 16 유지(Shared/Modal 모범) |
| `226:6496` | Network Failure | 400×220 | 180 | 동일 |
| `226:7227` | Retry Loading | — | 180 | OK |
| `134:7913` | Timeout Expired | 400×220 | 180 | 동일 |
| `226:7323` | Warning Countdown | 400×220 + fs64 | 180 | 카운트다운 64 OK, Modal 폭 상향 |
| `226:7420` | Continue Order | — | 180 | OK |

oddGap 25/35 결제 플로우 공통.

---

### 2.8 SCR-014 Accessibility

| ID | tn | Inst | 피드백 |
|---|---|---|---|
| `134:7972` Default | 15 | **Instance 0** | 컴포넌트 미연결 수동 화면 가능 — HC 토큰 검증용으로 재구성 여부 결정 |
| `134:8005` High Contrast | 15 | 0 | Default와 fs 동일 패턴 — **실제로 고대비 hex가 달라지는지** 페인트 스냅샷 필요 |
| `134:8038` Reverted | 16 | 0 | 동일 |

---

## 3. 관리자 스크린 (`06-C`) — 72프레임 실측

### 3.1 SCR-009 Live Order (주방/태블릿 성격 강함)

| ID | 화면 | tn | AUTO% | fs 특징 | oddGap | Dialog/Toast | 피드백 |
|---|---|---|---|---|---|---|---|
| `134:10607` | Default | **487** | 98 | **12×260**, 14×130 | **6,10,218** | — | **gap 218 P0.** 본문 12 과다 — 태블릿 거리면 **14**. OrderCard×4, MenuButton×128, OptionItem×192 |
| `235:6361` | Detail Open | 513 | 98 | +13 | 6,10,218 | DetailPanel | 동일 + 패널 |
| `242:16397` | New Order Noti | 488 | 97 | +11 NEW | 6,10,218 | StatusBadge×1 **badgeWrong** | NEW 11 OK. Badge 「핵심 재료」오라벨 |
| `235:9009` | Status Confirm | 491 | 97 | | 6,10,218 | Dialog **440×248** @660,390 | 웹 440 OK. gap 218 여전 |
| `235:10132` | Saving | 489 | 97 | | +2 | Toast 300×76 @1596,24 | Toast 위치(우상단) 웹 OK |
| `235:11264` | Success Toast | 489 | 97 | | | Toast 300×76 | OK |
| `235:11294` | Save Error | 489 | 97 | | | Toast | OK |
| `235:11324` | TTS Failure | 489 | 97 | | | Toast | OK |
| `134:11447` | Loading | 1 | 100 | 18 | — | Navbar 1920×72? | 로딩 골격 |
| `134:11452` | Empty | 6 | 50 | 14/16 | 10 | EmptyState | OK |
| `134:11468` | Error | 6 | 50 | | 10 | ErrorState | OK |

**Navbar:** Live Order에서 `90×72`로 잡히는 경우 — **축소/아이콘 모드**. Desktop 240과 혼재 → 브레이크포인트 문서화.

---

### 3.2 SCR-010 Order Management / Detail

| ID | 화면 | tn | AUTO% | ≤11 | badgeWrong | 피드백 |
|---|---|---|---|---|---|---|
| `134:10630` | Order Detail Default | 146 | 99 | 12 | **1** (「핵심 재료」) | 표 13px 웹 OK. StatusBadge 오라벨 **P0**. SearchInput 폭 Master 150 — 스크린에서 실제 폭 확인 |
| `235:14618` | Detail Open | 144 | 99 | 12 | 1 | 동일 |
| `235:15030` | Filter Applied | 146 | 99 | 12 | 1 | 동일 |
| `235:15447` | Loading | 57 | 96 | 2 | 1 | Badge 오라벨만 남아도 FAIL |
| `235:15866` | Empty | 59 | 93 | 2 | 1 | EmptyState |
| `235:16269` | Error | 60 | 92 | 2 | 1 | ErrorState |

Navbar **240×1080** (정식 사이드바).

---

### 3.3 SCR-011 Sold-out Management

공통: SoldOutCard×13, **fs 9가 26회**, tinyN≈42, purpleN≈2, badgeWrong=1, oddGap 6/10.

| ID | 화면 | SaveBar fill | Dialog/Toast | 피드백 |
|---|---|---|---|---|
| `134:11863` | Default | — | — | **9px 카테고리/품절 P0.** 이름 11. Purple 2. Badge 오라벨 |
| `241:14211` | Item Changed | **`#292D30`** 800×56 | — | dirty 다크 SaveBar |
| `241:14507` | Disable-all Confirm | `#292D30` | Dialog 440 @740,416 | Confirm OK 크기(웹). SaveBar 다크 |
| `241:14927` | Saving | `#292D30` | — | saving 다크 |
| `241:15269` | Success Toast | — | Toast 300 @1596,24 | OK |
| `241:15352` | Save Error | `#FFF0EB` | Toast | error 톤 OK |
| `134:11939` | Save | — | — | 9px 잔존 |
| Empty/Error/Loading | | | | Badge 「핵심 재료」잔존 |

---

### 3.4 SCR-015 Login

| ID | tn | AUTO% | Inst | 피드백 |
|---|---|---|---|---|
| `134:12033` Default | 16 | 69 | 0 (수동?) | 필드 높이·라벨 14/15 — 웹 OK. Instance화 여부 검토 |
| `250:19761` Validation | 18 | 72 | 0 | 에러 12px 등장 — **≥13** |
| `250:19867` Auth Error | 17 | 71 | 0 | 동일 |
| `250:19972` Submitting | 16 | 69 | 0 | 버튼 disabled 높이≥40 |
| `134:11489` Unauthorized | 4 | 25 | EmptyState | OK |

---

### 3.5 SCR-016 Menu Management (핵심)

| ID | 화면 | tn | AUTO% | tinyN | badgeWrong | SaveBar | Toast/Dialog | Inst | 피드백 |
|---|---|---|---|---|---|---|---|---|---|
| `134:12137` | Default | 135 | 73 | 25 | 1 | — | — | MenuCard×8, OptionSummary×6, IngredientRow×2 | MenuCard **10px** BEST/NEW/category. Badge 오라벨. Option 12px 추천 문구 — 웹 caption 허용이나 **복붙 데이터** Content QA |
| `241:17521` | Save Success | 135 | 72 | 25 | 1 | — | Toast **300×76** @1596,24 | 동일+Toast | Toast 웹 OK. 구조 PASS(기존 Pilot). Content QA 유지 |
| `241:16747` | Delete Confirm | 140 | 71 | 27 | 1 | — | Dialog **440×248** @740,416 | Confirm×1 | 웹 Dialog OK. **메뉴명 미표시** Content. type variant 확인 |
| `241:21716` | Empty | 88 | 90 | 1 | 1 | — | EmptyState | CTA 「새로고침」vs 「새 메뉴 추가」 |
| `241:22038` | Loading | 85 | 93 | 1 | 1 | — | LoadingState | OK |
| `134:12328` | Detail Add | 222 | 83 | **53** | 1 | — | — | MenuCard×12, Toggle×7, Ingredient rows… | **9~10px 다수.** 편집 밀도↑ — 최소 이름 13 |
| `134:12668` | Detail Edit | 222 | 83 | 53 | 1 | — | — | 동일 | 동일 |
| `241:17178` | Save Loading | 175 | 97 | 38 | 1 | **`#292D30`** | — | | dirty/saving 다크 |
| `241:15965` | Validation Error | 182 | 97 | 39 | 1 | `#292D30` | — | | 동일 |
| `241:17719` | Save Error | 178 | 96 | 38 | 1 | `#FFF0EB` | Toast 300 | | error 톤 OK |

---

### 3.6 SCR-018 Payment Methods

공통: badgeWrong=1, PaymentSaveBar **560×69 fill `#262626`**(거의 검정), oddGap 2/10.

| ID | SaveBar fill | Dialog/Toast | 피드백 |
|---|---|---|---|
| Default `134:11493` | `#262626` | — | **PaymentSaveBar 다크** — SaveBar와 동일 P0 계열 |
| Toggle Changed | `#262626` | — | |
| Save Confirm | `#262626` | Dialog 440 | |
| Saving | `#262626` | — | |
| Save Success | `#262626` | Toast 300 | success인데 바가 다크면 위계 혼란 |
| Save Error | **`#E53333`** | Toast | 에러 바 빨강 — 토큰 `#EF4444`/`#FFF0EB`와 불일치 가능 |
| All Disabled Warning | `#262626` | Dialog 440 | |
| Loading / Load Error | `#262626` | | |

---

### 3.7 SCR-019~022 Sales / Dashboard

공통: StatusBadge **항상 badgeWrong=1**(「핵심 재료」가 매출 화면에도), AUTO≈98%, 본문 13~14 웹 OK.

| 그룹 | 대표 ID | 피드백 |
|---|---|---|
| Sales Summary Default/Filter/Partial | `134:10661` 등 | Metric 24 OK. Badge 오라벨만 Master 수정으로 일괄 해결 |
| Sales Empty/Error/Loading | | Empty/Error 14 OK |
| Monthly/Daily | `134:10957`, `134:11150` | DateSelector·차트 — gap 6/10 정리 |
| Dashboard `227:5008`+ | (동일 패턴) | Badge + AUTO |

---

## 4. 스크린에서만 보이는 결함 (Master와 별개)

| 결함 | 수치/증거 | 영향 화면 |
|---|---|---|
| BottomCTA **940×200** override | Order Complete | `134:7926` |
| ConfirmDialog **440 vs 680** 혼용 | Cart Clear 440 / Delete 680 | SCR-005 |
| Toast **299×74~76** on 1080 키오스크 | 본문 12~14 | Detail Limit, Cart Toasts |
| CategoryTap×4 | Menu List 전 상태 | SCR-003 |
| Empty CTA 「새로고침」 | 14px | Cart Empty, Menu Empty 등 |
| Navbar 90×72 vs 240×1080 | Live vs 기타 Admin | SCR-009 vs 010+ |
| PaymentSaveBar `#262626` / error `#E53333` | 560×69 | SCR-018 |
| gap **218** | OrderCard 레이아웃 | SCR-009 |
| StatusBadge 문자 「핵심 재료」 | 11px | Admin SCR 거의 전부 |
| MenuCard placeholder 10px | category/BEST/NEW | SCR-016 |

---

## 5. 색 · 타이포 · 여백 · 레이아웃 · 트렌드 (스크린 관점)

### 색
- 키오스크 Cart **Blue stroke/fill 다량** — 화면에서 즉시 보임.  
- 관리자 Sold-out **Purple** text 2건/화면.  
- SaveBar/PaymentSaveBar **차콜~검정** dirty — 웹에서 “시스템 콘솔” 느낌.  
- 라임 CTA는 BottomCTA/버튼에 국한 — Home·Complete는 OK 방향.

### 글자·행간
- 키오스크 Menu List **AUTO 100%**. Detail은 OptionCard 덕에 AUTO%↓(≈18%) but **12~13 필수/설명** 잔존.  
- 관리자 Live **12px×260**. Sold-out **9px×26**.  
- letterSpacing 스크린 단위 추가 샘플은 0% 가정(컴포넌트와 동일).

### 여백·레이아웃
- Header pad **62 vs 48**. CTA pad **30 vs 40** 혼재.  
- Payment gap **5/25/35**. Cart gap **14/22**. Live gap **218**.  
- Order Complete CTA 폭 **940 ≠ 1080**.

### 트렌드 / 비-AI
- Detail의 OptionCard×46은 “정리된 그리드” — 좋음. 남는 건 **selected border·타입 스케일**.  
- Admin 전 화면 StatusBadge 오라벨은 템플릿 실수처럼 보임 → **데이터/바인딩 수정이 개성보다 우선**.  
- 퍼플·블루·다크 SaveBar 제거가 “사람 손”에 더 가까움.

---

## 6. 스크린 반영 작업 순서 (재정의)

1. **Master:** CartItemCard Blue·MenuButton / StatusBadge 라벨 / SaveBar·PaymentSaveBar 톤 / OptionGroup 12→16 / CategoryTap→Tab  
2. **스크린 override 제거:** Order Complete CTA 940×200 → 1080×180  
3. **스크린 통일:** Cart ConfirmDialog 440 vs 680  
4. **키오스크 Toast size** 또는 전용 큰 Toast  
5. **Content:** Empty CTA 문구, SCR-016 추천 복붙, Delete 메뉴명  

---

## 7. 커버리지

| 범위 | 개수 | 상태 |
|---|---|---|
| Kiosk SCR 1080×1920 | **57** | 전수 실측·표 반영 |
| Admin SCR 1920×1080 | **72** | 전수 중 핵심·반복 패턴 실측, Sales/Dashboard는 그룹 요약 |
| Annotation/__spec only | 제외 | polish 비대상 |
| `190:2` QA Matrix | 미포함 | 요청 시 별도 |

---

*끝.*
