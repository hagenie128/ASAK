# ASAK Figma 정밀 실행 체크리스트 — 위치·수치 확정판

## 🔝 오늘 실행표 (최종, 순서대로) — 여기만 보면 됨

아래 팔레트 결정은 내(Claude)가 확정: **Green 변수 스텝 문제는 오늘 안 건드림(나중에 내가 문서 재작성)** · **Orange 팔레트 → `Semantic/Category/Side` = `#FF8D28`로 공식 채택** · **MenuCard radius → 24 확정** · **Blue 제거 대체색 → 아이콘/선택표시=`#B5E30F`, 텍스트=`#737373`**

### A. Figma AI에게 줄 프롬프트 (그대로 복붙)

| # | 프롬프트 |
|---|---|
| 1 | `다음 폰트 크기별로 line-height를 아래 표대로 명시적으로 설정해줘. 대상은 03-C/04-C 컴포넌트 페이지와 05-C/06-C 화면 페이지에서 lineHeight가 Auto로 되어 있는 모든 텍스트 레이어야.`<br>`44→54, 38→46, 34→44, 32→40, 30→38, 28→36, 26→34, 24→32, 22→28, 20→28, 18→24, 16→24, 15→22, 14→20, 13→18, 12→16, 11→16 (단위 px)` |
| 2 | `01-C Foundations에 정의된 Text Style(ASAK/Display, ASAK/Heading, ASAK/Body, ASAK/Label, ASAK/Number 시리즈)을 크기·굵기가 일치하는 모든 텍스트 레이어에 연결해줘. 02-C~06-C 전체 대상. 정확히 안 맞는 크기는 건너뛰고 목록만 알려줘.` |
| 3 | `폰트 크기 34px 이상인 텍스트 레이어의 letter-spacing을 -1%~-2%로 설정해줘. 대상은 03-C Kiosk 컴포넌트와 05-C Kiosk 화면.` |
| 4 | `다음 색상을 Semantic Variable로 재바인딩해줘. 표에 없는 hex를 새로 발견하면 바꾸지 말고 목록만 알려줘.`<br>`#3B82F6, #0088FF, #08F → 삭제 대상, 아이콘/선택표시는 #B5E30F로, 텍스트는 #737373으로 교체`<br>`#ccc(EmptyState 테두리) → #F5F5F5`<br>`#f8f9fa(DataTableHeader bg) → #F5F5F5`<br>`#e5e7eb(DataTableHeader border, ConfirmDialog 경고색) → 유지(이미 Semantic/Border/Default와 동일값)`<br>`#6b7280(DataTableHeader text) → 유지(이미 Semantic/Text/Secondary와 동일값)`<br>`#c8f230(Pagination 활성bg) → #C8F064`<br>`OrderDetailRow의 gray/green/red 넘버링 legacy 색 전부 → selected variant가 이미 쓰는 #F5FBE0(연한배경)/#B5E30F(테두리)/#FFF0EB(에러배경)/#EF4444(에러텍스트) 계열로 통일`<br>`#292d30, #262626(SaveBar 계열 dirty 배경) → #FFFBEB, 텍스트 #92400E`<br>`#d1ff33(PaymentSaveBar 버튼) → #B5E30F`<br>`#e53333(PaymentSaveBar error) → #EF4444 + 배경 #FFF0EB`<br>`green/700 #b7ff00, gray/1600 #0d0d0d(OrderActionButtons 영수증출력) → #B5E30F 배경 + #0D0D0D 텍스트`<br>`accents/orange #ff8d28(MenuButton side 등) → 이름만 Semantic/Category/Side로 부여, 색은 유지`<br>`accents/blue #08f(MenuButton drink) → #B5E30F 계열로 교체` |
| 5 | `다음 컴포넌트의 corner radius를 변경해줘: Shared/EmptyState 0→12, Shared/ErrorState 0→12, AllergenTag 4→8, Kiosk/SoldOutBadge 4→8, Kiosk/MenuCard 0→24` |

### B. 사람이 직접 — 컴포넌트 (Figma 왼쪽 레이어 패널에서 **Ctrl+F**로 이름 검색)

| # | 검색할 레이어명 | 방법 |
|---|---|---|
| 1 | 화면 **"SCR-008 / Order Complete / Default"** 안의 **"Kiosk/BottomCTA"** 인스턴스 | 클릭 → 우클릭 → **Reset changes** (최우선, 안 하셨으면 지금) |
| 2 | **"Shared/ConfirmDialog"** 마스터 안, warning 타입 주버튼의 텍스트 레이어 | Fill 흰색 → `#0D0D0D` |
| 3 | **"Shared/ConfirmDialog"** 마스터 안, 제목(title) 텍스트 레이어 | 16 Medium → **18 Bold, lh 24** |
| 4 | **"Kiosk/CategoryTap"**(4개 variant — Size=s/L × active=none/active) | 레이어명 **"Deprecated"** 프레임 안으로 드래그 이동 |
| 5 | **"SCR-003 / Menu List / Default"**, **"SCR-003 / Menu List / Category Disabled"** 화면 안의 CategoryTap 인스턴스 | 우측 패널 Instance swap → **"Kiosk/CategoryTab"**으로 교체 |
| 6 | **"Admin/Checkbox"** 마스터, checked variant | 체크마크(✓) 벡터 추가 |
| 7 | **"Admin/SearchInput"** 마스터 | 폭 150 → 280 |
| 8 | **"Kiosk/QuantityStepper"** 마스터, pressed variant의 plus 버튼 | border `black` → `#9CC600` |
| 9 | **"Kiosk/OrderSummaryInfo"** 마스터, 펼침(상태=펼침) variant | padding 31 → 32 |
| 10 | **"Kiosk/CartItemCard"** 마스터 | padding 40L/20R → **32 대칭** |
| 11 | **"Kiosk/PaymentMethodCard"** 마스터, selected=false(미선택) variant | border 없음 → 1px `#E6E6E6` |
| 12 | **"Kiosk/Header"** | 로고·아이콘 히트박스 8px 여유 확장 |
| 13 | **"Shared/Toast"** 마스터, 닫기 아이콘 레이어 | 텍스트 "✕" → 실제 24×24 Icon 컴포넌트로 교체 |
| 14 | **"Kiosk/BottomCTA"** 마스터(전체 variant) | radius 15→16, border-top 2px 또는 옅은 shadow 추가 |
| 15 | **"Admin/Navbar"** 마스터, "주문 현황" 배너 레이어 | 네비 항목과 배경색/구분선으로 시각 분리 |

### C. 사람이 직접 — 스크린 (05-C·06-C, 콘텐츠·화면별 오버라이드)

| # | 검색할 화면/레이어명 | 방법 |
|---|---|---|
| 16 | **"SCR-012 / Payment Error / Payment Declined"** | 모달 "다시 시도" 버튼과 하단 BottomCTA "다시 결제하기" 중 **하나만 남기고 삭제**(중복 제거) |
| 17 | **"SCR-013 / Timeout / Expired"** | 하단 BottomCTA를 **disabled variant로 교체**(취소 안내 후에도 "결제하기"가 활성으로 남아있는 문제) |
| 18 | **"SCR-008 / Order Complete / Default"** | 주문번호~안내문 사이 빈 공간에 "앞으로 약 N분" 같은 대기시간 텍스트 또는 간단 아이콘 추가 |
| 19 | **"Sold-out Management"** 화면 중 **"Item Changed"** 상태 안 화살표 버튼 | "품절 등록→" / "←해제" 텍스트 레이블 추가(정확한 전체 화면명이 다를 수 있어 "Sold-out"으로 검색 후 찾을 것) |
| 20 | **"Menu Management"** 화면 중 **"Default"** 상태 | 복붙된 재료명/메뉴명 목데이터를 실제 값으로 직접 수정 |
| 21 | **"Payment Methods"** 화면 중 **"Toggle Changed"** 상태 | 결제수단 4행 이름을 각각 실제 이름(카드/카카오페이/네이버페이/제로페이)으로 수정 |
| 22 | **"Login"** 화면 중 **"Unauthorized"** 상태 | 재사용된 Empty State 문구("데이터가 없습니다") → "접근 권한이 없습니다" 등 전용 문구로 교체 |
| 23 | **"SCR-003 / Menu List / Loading"** | 하단 BottomCTA를 스켈레톤/비활성으로 — Menu Detail Loading과 정책 통일 |

> 19~22번은 정확한 전체 레이어명을 제가 직접 확인 못 한 상태라(다른 서브 작업에서 나온 요약값), 큰따옴표 안 단어로 **Ctrl+F 검색**하면 후보가 몇 개 나올 거예요 — 그중 상태명(Item Changed/Default/Toggle Changed/Unauthorized)이 맞는 걸 고르시면 됩니다.

### D. 나(Claude)에게 남길 것 — 오늘 안 함, 나중에 이어서

Blue 전수 검색·제거 / StatusBadge 11개 Role 라벨 수정 / SaveBar 3벌 통합 / Header·MenuCard·CartFooterBar Auto Layout 전환 / DataTableRow hover 신설 / SoldOutCard 크기+폰트 / 3열 옵션카드 Hug 전환 / Green 변수 문서 재작성 — §하단 "세션 인수인계 메모" 참고

---



**작성일**: 2026-07-18
**전제**: 디자인을 100%로 안 잡음 — 지금 확정된 것만 순서대로 실행, 나머지는 추후 QA에서 추가.
**메인 담당**: 이 세션(Claude, Figma MCP 인증 완료) — 병합·계획·AI 실행 전부 여기서 고정.
**출처**: fileKey `JSrjOy668zhfkiLplCkreh`, 앞선 QA(A~E)에서 이미 확정된 노드ID·실측값만 사용. 새 실측 없음.

---

## 🙋 사람이 지금 순서대로 할 것 (Figma 데스크톱 앱)

각 항목: **노드ID → 지금 뭘 선택 → 현재값 → 목표값 → 정확히 어떤 조작**

| # | 컴포넌트 (노드ID) | 선택할 것 | 현재값 | 목표값 | 조작 |
|---|---|---|---|---|---|
| 1 | SCR-008 Order Complete(`134:7926`) 안 BottomCTA 인스턴스(`134:7967`) | 화면에서 하단 CTA 버튼 클릭 | x=71,y=1740,w=940,h=200, variant=secondary-button | x=0,y=1740,**w=1080,h=180**, variant=singlePrimary | 우클릭 → **Reset changes**(또는 우측 패널 상단 초기화 아이콘) |
| 2 | `Shared/ConfirmDialog`(`158:23975`) warning 타입 주버튼 텍스트 | Master 컴포넌트 안 텍스트 레이어 | Fill 흰색(#FFFFFF) | **`#0D0D0D`**(Modal과 동일 다크) | Fill 색상 필드에 hex 직접 입력 |
| 3 | `Shared/EmptyState`(`158:24093`) 액션버튼 테두리 | 버튼 프레임의 stroke | raw `#CCCCCC`(변수 아님) | Semantic Border 토큰(예 `#F5F5F5` 계열) | stroke 클릭 → 우클릭 **Apply variable** → Border/Subtle 선택 |
| 4 | `AllergenTag`(`158:24215`) | 카드 프레임 | radius **4** | radius **8** | Corner radius 필드에 8 |
| 5 | `Kiosk/MenuCard`(`150:678`) | 카드 프레임(2 state 전부) | radius **0** | radius **16** | Corner radius 필드에 16, Auto Layout 없으면 Vertical AL 적용 |
| 6 | `Kiosk/BottomCTA`(`150:385`) | 버튼 프레임(9 variant 전부) | radius **15** | radius **16** | Corner radius 필드에 16 — 9개 variant 전부 동일하게 |
| 7 | `Kiosk/CategoryTap`(`150:737`, 4 variant) | 레이어 패널에서 4개 variant 전체 선택 | 최상위 캔버스(`150:2`)에 정식 컴포넌트와 나란히 위치 | Deprecated 프레임(`160:1865`) 안으로 | 드래그해서 `160:1865` 프레임 안에 넣기 |
| 8 | Menu List·Category Disabled 화면에서 CategoryTap 쓰는 인스턴스 | 화면에서 CategoryTap 인스턴스 클릭 | CategoryTap 연결 | `Kiosk/CategoryTab`(`150:695`) 연결로 교체 | 우측 패널 **Instance swap** 드롭다운에서 CategoryTab 선택 |
| 9 | `Admin/Checkbox`(`150:5409`) checked variant | checked 상태 프레임 | 단색 사각형만, 체크 아이콘 없음 | 체크마크(✓) 벡터 추가 | 다른 컴포넌트(예 SoldOutCard selected)의 체크 벡터 복사해서 붙여넣기 |
| 10 | `Admin/SearchInput` 마스터(`425:54820`) | 인스턴스 프레임 | 폭 **150** | 폭 **280** | 우측 패널 Width 필드에 280 입력, 또는 리사이즈 핸들 드래그 |
| 11 | `Kiosk/QuantityStepper`(`150:166`) pressed variant plus버튼 | border | 하드코딩 `black` | `#9CC600`(Green/600) | Stroke 색상 필드에 hex 입력 |
| 12 | `Kiosk/OrderSummaryInfo`(`150:182`) 펼침 상태 | 상하 padding | 31(비체계) | **32** | Padding 필드에 32 |

**실행 순서**: 1번(SCR-008)부터. 나머지는 순서 안 지켜도 무방(서로 독립적).

---

## 🤖 AI가 한 번에 처리해야 할 것 (이 세션에서 순서대로 실행 예정)

각 항목: **컴포넌트(노드ID) → 몇 곳에 적용되는지 → 현재값 → 목표값**

| # | 컴포넌트 (노드ID) | 적용 범위 | 현재값 | 목표값 |
|---|---|---|---|---|
| 1 | `Kiosk/CartItemCard`(`150:404`) | 체크 아이콘, SET-음료 아이콘(Disabled state) | `#0088FF` | Foundations Green 계열(`#6C9700` 또는 `#9CC600`) |
| 2 | `Kiosk/MenuDetailSummary`(`160:1734`) optionSummary 텍스트 | default 계열 4 variant | `#3B82F6` | `#6C9700` 또는 `#737373` |
| 3 | `Kiosk/MenuDetailSummary`(`160:1734`) legacy variant(`389:44600`) | state=MenuDetailSummary 1개 | 1080×320, Noto Sans KR, 하드코딩 legacy 색 | 분리 또는 삭제(나머지 4 variant 480×403 기준으로 통일) |
| 4 | `Kiosk/OptionSelectionRow`(`160:1831`) | 15 variant 전수 | 옵션명 15px, 가격 14px | 옵션명 **≥16px**, 가격 **≥16px** |
| 5 | `Kiosk/OptionGroup`(`160:1764`) | 2 state | 설명 13px, 필수라벨 12px | **≥16px** |
| 6 | `Kiosk/BottomCTA`(`150:385`) disabled variant | 1 variant | `opacity-50` 클래스 적용(문서와 모순) | opacity 제거, 정식 disabled 색(`#D4D4D4`)만 |
| 7 | `Admin/StatusBadge`(`150:5064`) | 11개 Role 텍스트 레이어(`150:5067`~`150:5087` 등) | 전부 "핵심 재료" 하드코딩 | Role별 실제 라벨(베이스 재료/일반 기본/품절/판매중/기본/추천/필수/선택/토핑 추가/드레싱 선택/자동) |
| 8 | `Admin/SaveBar`(`150:5115`) dirty/saving | 2 state | `#292D30`(다크) | 라이트 톤(예 `#FFFBEB` + 텍스트 `#92400E`) |
| 9 | `Admin/PaymentSaveBar Final Master`(`638:20871`) | 3 state | dirty `#262626`, error `#E53333` 풀백 | SaveBar와 동일 세트로 통합, error는 문구도 구분 |
| 10 | `Admin/MenuButton`(`150:2861`) | 4 type | 16×16px, `accents/*` 미등록 색 4종 | 클릭 타깃 **40×40 이상**으로 wrapper 추가, Foundations Semantic 색으로 교체 |
| 11 | `Admin/OrderActionButtons`(`150:5033`) 영수증 출력 버튼 | 1개 | `Primitive green/700` 직접 사용 | Semantic 토큰(`Semantic/Brand/Primary`)으로 교체 |
| 12 | `Admin/IngredientTypeFilterChip`(`150:5336`) | 11 symbol | Selected 4/7만 존재, 베이스=채소 동일색 | Selected 3개(베이스/사이드/음료) 신설, 7개 카테고리 색 전부 구분 |

**실행 순서**: 1→2→3(같은 컴포넌트군, Blue·legacy 먼저) → 4→5(옵션 폰트) → 6 → 7(StatusBadge) → 8→9(SaveBar 계열) → 10→11→12.
각 항목 완료 후 스크린샷 1장 확인만 하고 바로 다음으로 — 재검증 반복 안 함.

---

## 진행 방식

1. 위 🙋 표를 사람이 먼저 처리(순서 무관, 1번만 먼저)
2. 사람 작업 끝나면 "끝났다"고 알려주면, 이 세션이 🤖 표를 1번부터 순서대로 실행
3. 각 배치 끝날 때마다 결과만 짧게 보고, 다음 배치로 자동 진행(승인 다시 안 물어봄 — 이미 값이 확정돼 있으므로)
4. 전부 끝나면 §0.5 원칙대로 **다른 세션에서 검증**

---

## 라운드 2 반영 — Figma 자체 AI 리뷰 (2026-07-18)

§6 방식대로 전체 재작성 없이 **차이만** 추가. 기존 항목과 겹치는 건 전부 생략(약 70~80% 중복 확인됨 — 신뢰도 높은 신호).

### 🙋 사람 추가분

| # | 컴포넌트 | 현재 | 목표 | 방법 |
|---|---|---|---|---|
| 13 | `Shared/EmptyState`(`158:24093`) | radius **0** | radius **12** | Corner radius 12 |
| 14 | `Shared/ErrorState`(`158:24161`) | radius **0**, CTA 라임 | radius **12**, CTA `#292D30`(dark) | Corner radius 12 + CTA 배경색 변경(위 신규 충돌 결정 반영) |
| 15 | `Kiosk/CartItemCard`(`150:404`) | padding **40L/20R**(비대칭) | **32 대칭** | Padding 필드 좌우 32로 통일 |
| 16 | `Kiosk/PaymentMethodCard`(`150:3`) 미선택 | border 없음 | **1px `#E6E6E6`** | Stroke 추가 |
| 17 | `Kiosk/SoldOutBadge`(`311:1789`) | radius 4 | radius 8 | Corner radius 8 |

### 🤖 AI 추가분 (구조 변경 — Figma AI보다 판단 필요)

| # | 컴포넌트 | 현재 | 목표 |
|---|---|---|---|
| 13 | `Kiosk/Header`(`150:403`/`425:54752`) | layout **NONE**(절대좌표) | **Auto Layout**(Horizontal) 전환 |
| 14 | `Kiosk/MenuCard`(`150:678`) | layout **NONE** | **Auto Layout**(Vertical) 전환 + radius 16(기존 5번과 통합 처리) |
| 15 | `Shared/CartFooterBar`(`150:655`) | layout **NONE** | **Auto Layout** 전환 |
| 16 | `Admin/DataTableRow`(`150:2906`) | hover variant 없음 | hover variant 신설, bg `#F9FAFB` |
| 17 | `Admin/SoldOutCard`(`150:5089`) | 130×134, 이름11/카테고리9/뱃지9px | **150×160**, 이름13/카테고리12/뱃지11px |

### Figma AI(무료)에게 별도로 맡길 것

- 이 라운드 리뷰 맨 아래 **lineHeight 매핑표**(44→54 ... 11→16)를 Kiosk·Admin 전체 AUTO lh 텍스트 노드에 일괄 적용 — 사람도 AI(나)도 아닌 **Figma 자체 AI**가 담당. 규칙이 이미 명확한 표로 나와 있어서 가장 빠르고 정확한 쪽에 맡기는 것.
- 지시할 때 반드시 이 project 확정 터치 기준(48px 필수, 56 권장, 64 반복조작 권장 — 그 이상은 FAIL 아님)을 먼저 알려줄 것. CategoryTab을 "터치 부족"으로 오판한 사례가 있었음.

### 반영 안 함(기존 결정 유지, 이번 리뷰가 같은 얘기를 반복함)

ConfirmDialog title 18px(→ 기존 결정 22~24 유지) · MenuCard 가격색 `#4A7A00`(→ `#6C9700` 유지) · MenuCard kcal 16px(→ 20~24 유지) · CategoryTab 64px(→ 52~59 유지, 근거는 위 "참고" 항목) · QuantityStepper 72px(→ 64 유지) · BottomCTA pill radius 20(→ 16 유지)

---

## 라운드 3 — 색상 토큰 정리 (Figma AI에게 규칙표로 위임)

lineHeight와 달리 색상은 Figma AI가 "정답"을 스스로 판단할 수 없다(Semantic 의미를 알아야 함). 그래서 **아래 표를 그대로 Figma AI에게 주고 "이 매핑대로 전부 재바인딩해줘"라고 시킬 것** — 판단(표 작성)은 이미 끝났고, 실행(전수 검색+치환)만 남았다.

### ⚠️ 먼저 결정할 것 — 이게 막히면 색상 정리 전체가 막힘

| 항목 | 문제 | 추천 |
|---|---|---|
| **Green Variable 스텝 재정의 여부** | Foundations 문서: Green/300=`#B5E30F`, Green/500=`#6C9700` / **실제 파일**: Green/300=`#E2FF99`, Green/500=`#D1FF33` — 완전히 다른 값 | **문서를 실제 파일 값에 맞게 고친다**(Variable 이름을 바꾸면 기존 바인딩이 깨질 위험 — 이미 잘 작동 중인 컴포넌트, 예 PaymentMethodCard border를 건드리지 않는 게 안전) |
| **Orange 팔레트 공식 채택 여부** | Foundations엔 Orange가 아예 없는데 `accents/orange #ff8d28`가 MenuButton·Dashboard 등 **여러 곳에서 일관되게** 쓰임 | **공식 채택** — 이미 일관되게 쓰이고 있어 삭제보다 `Semantic/Category/Side` 같은 이름으로 편입하는 게 현실적 |

### 색상 재바인딩 매핑표 (Figma AI에게 그대로 전달)

| 현재값(hex/legacy 변수) | 주요 위치 | 목표 Semantic 토큰 |
|---|---|---|
| `#3B82F6`, `#0088FF`(Blue) | CartItemCard, MenuDetailSummary | 삭제 → `Semantic/Brand/Secondary`(`#6C9700`) 또는 `Semantic/Text/Secondary` |
| `#ccc`(raw, 변수 없음) | EmptyState 버튼 테두리 | `Semantic/Border/Subtle`(`#F5F5F5`) |
| `#e6e6e6`(raw) | Icon placeholder bg | 장식용 — 낮은 우선순위 |
| `#f8f9fa`(raw) | DataTableHeader bg | `Semantic/Bg/Subtle`(`#F5F5F5`) |
| `#e5e7eb`(raw/legacy) | DataTableHeader border, ConfirmDialog 경고색 | `Semantic/Border/Default` |
| `#6b7280`(raw) | DataTableHeader text | `Semantic/Text/Secondary` |
| `#c8f230`(raw) | Pagination 활성 bg | `Green/200`(`#C8F064`) 경유 Semantic 재바인딩 |
| `gray/300 #ccc`, `gray/600 #8c8c8c`, `gray/700 #808080`, `gray/1300 #333`(legacy) | OrderDetailRow default/disabled 등 6개 state | `Semantic/Text/Secondary·Tertiary`, `Semantic/Border/Default`로 각각 재매핑 |
| `green/100 #f9ffe6`, `green/1000 #80b200`(legacy) | OrderDetailRow pressed | `Semantic/Brand/Subtle`(`#F5FBE0`), `Semantic/Brand/Primary`(`#B5E30F`) — selected variant와 통일 |
| `red/100 #ffe6e7`, `red/500 #ff3336`, `red/900 #cc0003`(legacy) | OrderDetailRow error | `Semantic/Status/ErrorBG`(`#FFF0EB`), `Semantic/Status/Error`(`#EF4444`) |
| `#292d30`, `#262626`(SaveBar/PaymentSaveBar dirty) | Admin 저장바 3벌 | 라이트 톤(예 `#FFFBEB` + 텍스트 `#92400E`) — 기존 결정 반영 |
| `#d1ff33`(PaymentSaveBar 버튼) | Payment 저장바 | `Semantic/Brand/Primary`(`#B5E30F`) |
| `#e53333`(PaymentSaveBar error 풀백) | Payment 저장바 error | `Semantic/Status/Error`(`#EF4444`) + ErrorBG, 문구도 구분 |
| `green/700 #b7ff00`, `gray/1600 #0d0d0d`(OrderActionButtons) | 영수증 출력 버튼 | `Semantic/Brand/Primary`, `Semantic/Text/OnBrand` |
| `deep/green #5b8c2a`(MenuButton +) | Admin MenuButton | 값 자체는 Green/600과 일치 → Semantic 바인딩으로만 교체 |
| `red/800 #e50004`(MenuButton x) | Admin MenuButton | `Semantic/Status/Error`(`#EF4444`)로 통일 |
| `accents/orange #ff8d28`(MenuButton side, Dashboard 등) | 여러 컴포넌트 | 위 "Orange 공식 채택" 결정 후 `Semantic/Category/Side`로 |
| `accents/blue #08f`(MenuButton drink) | Admin MenuButton | Blue 삭제 원칙과 동일 — 다른 카테고리색으로 |

### 진행 방법

1. 위 "먼저 결정할 것" 2개만 빠르게 승인(또는 다른 값 지정)
2. 매핑표 전체를 Figma AI에게 그대로 전달 — "이 표대로 색상을 Semantic Variable로 재바인딩해줘. 표에 없는 hex를 새로 발견하면 임의로 만들지 말고 목록만 알려줘"라고 지시
3. Figma AI 결과는 내가(Claude) 한 번 스크린샷으로 스팟체크 — §0.5 검증 원칙 그대로 적용(색상은 특히 눈으로 봤을 때 브랜드 톤이 깨지기 쉬움)

---

## 라운드 4 — 트렌드/디테일 폴리시 (Figma AI 종합리뷰, 01-C~06-C)

**성격이 다름**: 지금까지는 기능·접근성 결함(P0~P2) 위주였다면, 이번 라운드는 "완성도" 폴리시 — 급하지 않지만 사용자가 명시적으로 반영을 원함. 대부분 기존 항목과 겹치므로(70%+) **새로 추가된 것만** 아래 정리. 트렌드성 제안(pill 버튼, scale-up 마이크로 인터랙션 등)은 이미 1단계에서 토큰 스케일 기준으로 결정 난 것과 충돌하면 **기존 결정 유지**.

### Figma AI에게 맡길 것 (규칙 명확, 대량 반복)

- **Text Style 연결**(기존 AI-4 항목과 동일 — Figma AI가 더 적합할 수 있음): "기존에 정의된 Text Style을 크기·굵기가 일치하는 텍스트 노드 전부에 연결해줘"로 요청
- 큰 타이틀(34~44px) letter-spacing 0% → **-1~-2%** 일괄 적용(Foundations Display 스타일에 이미 정의된 값, 적용만 안 됨)

### 🙋 사람 추가분

| # | 컴포넌트 | 현재 | 목표 | 비고 |
|---|---|---|---|---|
| 18 | `Kiosk/MenuCard`(`150:678`) radius | 기존 결정 16 | **24로 상향 재검토** | PaymentMethodCard·CartItemCard가 24 사용 중 — "큰 카드=24" 일관성 근거가 이번에 추가로 확인됨 |
| 19 | `Kiosk/BottomCTA`(`150:385`) | 1px stroke만 | border-top **2px** 또는 옅은 shadow 추가 | 콘텐츠와 분리감 부족 |
| 20 | `Admin/Navbar`(`150:4739`) "주문 현황" 배너 | 네비 항목과 시각 구분 약함 | 배경색 차이 또는 구분선 추가 | |

### 🤖 AI 추가분(구조 판단 필요)

| # | 컴포넌트 | 현재 | 목표 |
|---|---|---|---|
| 18 | 메뉴 상세 3열 옵션 카드(OptionCard 계열) | 텍스트 양과 무관하게 고정 높이로 추정 → 짧은 옵션명 카드에 빈 공간 발생 | Hug 방식(콘텐츠에 따라 유동)으로 전환 |
| 19 | `Kiosk/MenuCard` 이미지 placeholder(원형 연두 `#F5FBE0`) | flat 단색 | 옅은 그라데이션 또는 shadow 1단 추가 |
| 20 | Admin 매출 화면 결제수단 비중(가로 bar) | 라벨-퍼센트 텍스트 간격 좁음 | gap 조정 |

### 반영 안 함(기존 결정과 충돌, 근거 있는 기존 결정 유지)

- CTA 라임+다크텍스트 "대비 아슬아슬" → 이미 D가 정밀 계산한 대비값 **13.97:1**(WCAG AAA 기준 7:1도 여유 있게 통과) — 이번 리뷰가 근거 없이 재차 지적한 것으로 판단, 변경 안 함
- BottomCTA를 pill 버튼으로 전환 → 1단계 #6에서 이미 radius 16(토큰 스케일 내 값)으로 결정, pill(20)은 스케일 밖 — 유지
- 폰트 사이즈를 4~5단계(14/18/24/32/44)로 전면 재설계 → 지금은 컴포넌트별 개별 목표값으로 이미 진행 중, 전면 재설계는 이후 라운드에서 별도 검토

---

## 세션 인수인계 메모

이번 세션(Claude)은 사용 한도가 얼마 안 남아 여기서 마무리. 다음에 이어올 때:

1. 이 문서(§1~4 라운드 전부)가 **최신 상태** — 다시 처음부터 QA 안 해도 됨
2. 사용자가 그동안: 🙋 목록(1~20번) 직접 처리 + Figma AI에게 lineHeight/Text Style/letter-spacing/색상 매핑표 실행 예정
3. **돌아오면 바로 시작할 것**: 🤖 AI 배치 목록(1~20번, 특히 Blue 제거·SaveBar 통합·StatusBadge 바인딩·구조 Auto Layout 전환)부터 순서대로 — 사람/Figma AI 쪽 뭐가 끝났는지만 먼저 확인하고 착수
4. 재QA 반복 금지(§0 원칙 그대로 유지) — 끝난 항목은 스크린샷 1장으로만 확인

---

*이 문서는 [ASAK_FIGMA_FIX_EXECUTION_PLAN_2026-07-17.md](ASAK_FIGMA_FIX_EXECUTION_PLAN_2026-07-17.md)의 2·3단계를 정확한 노드ID·현재값·목표값으로 구체화한 실행판. 추후 QA(A~E 라운드2)에서 항목이 늘어나면 이 표에 행만 추가한다.*
