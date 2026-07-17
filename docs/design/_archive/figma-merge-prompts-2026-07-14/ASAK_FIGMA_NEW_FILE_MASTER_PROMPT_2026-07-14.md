# ASAK Figma 새 파일 재구성 마스터 프롬프트

> 작성일: 2026-07-14  
> 대상 원본: [ASAK Figma](https://www.figma.com/design/o9mxSeovLQPdWNwM4mNySk/ASAK)  
> 사용법: 아래 **복사해서 Figma에 전달할 프롬프트** 전체를 Figma AI 또는 내일 실행할 Figma MCP 작업 지시로 사용한다.

## 작업 원칙

- 원본 파일은 수정·삭제·이동하지 않는다. 백업은 원본 안에 복제하지 말고, 별도의 새 Figma Design 파일로 만든다.
- 새 파일은 `ASAK — Design System & Product UI — 2026-07-14`로 생성한다. 원본은 `ASAK — Legacy (Read only) — 2026-07-14`라는 이름으로 남겨 둔다. 파일명을 바꿀 권한이 없으면 새 파일명만 위 이름으로 하고 원본은 그대로 보존한다.
- 새 파일은 원본의 색, 타이포그래피, 브랜드 톤과 실제 화면 내용을 기준으로 재구성한다. 보이는 화면을 단순 스크린샷처럼 복제하지 말고, 재사용 가능한 컴포넌트·변수·오토레이아웃 구조로 만든다.
- 이 문서에서 확정하지 않은 API 데이터는 그럴듯한 수치로 꾸며내지 않는다. 빈 상태 또는 `데이터 연결 예정` 상태를 만든다.
- 완료 기준은 “예쁜 화면”이 아니라, 명명 규칙과 구조가 정리되어 내일 MCP/Code Connect에서 안전하게 읽고 수정할 수 있는 파일이다.

## 복사해서 Figma에 전달할 프롬프트

```text
당신은 ASAK 제품의 수석 Figma 디자이너이자 디자인 시스템 정리 담당자다.

목표는 기존 ASAK Figma 파일을 절대로 훼손하지 않고 백업으로 보존한 뒤, 별도의 새 Figma Design 파일에 디자인 시스템, 키오스크, 관리자 화면, 프로토타입을 실제 개발 연동이 가능한 수준으로 재구성하는 것이다. 기존 원본을 수정하거나 기존 노드를 삭제/이동/이름 변경하지 마라.

────────────────────────────────
0. 안전한 백업과 새 파일 생성
────────────────────────────────
1) 현재 원본 파일을 읽기 전용 기준점으로 남긴다. 원본 안에 작업하지 않는다.
2) 새 Figma Design 파일을 생성하고 이름을 아래처럼 지정한다.
   `ASAK — Design System & Product UI — 2026-07-14`
3) 새 파일의 첫 페이지 `00. START HERE`에 아래 내용을 포함한 메모 프레임을 만든다.
   - Source: ASAK Legacy file
   - Created: 2026-07-14
   - Purpose: MCP / Code Connect ready design source
   - Rule: legacy file must not be edited
   - Handoff: frontend implementation uses Figma components, not screen screenshots
4) 원본에서 필요한 화면과 스타일을 새 파일로 복제해 시작하되, 복제 후에는 아래 구조와 이름으로 정리한다.
5) 새 파일의 모든 편집 대상은 Auto Layout 기반으로 만들고, 절대 위치 배치만으로 화면을 구성하지 않는다.

────────────────────────────────
0-A. 원본 자산 재사용 우선 원칙 (필수)
────────────────────────────────
이 작업은 원본을 참고해 새 디자인을 만드는 작업이 아니다. **원본에서 실제 사용 중인 컴포넌트, 컴포넌트 인스턴스, 아이콘, 이미지, 색상 스타일, effect style, 변수, 텍스트 스타일을 새 파일로 가져와 정리·재사용하는 마이그레이션 작업**이다.

1) 화면을 새로 그리기 전에 원본에서 다음 목록을 먼저 조사하고 `00. START HERE > Asset migration inventory`에 기록한다.
   - 원본 component set과 variant
   - 화면 안의 주요 component instance
   - 아이콘 component/instance와 이미지 asset
   - color/text/effect/grid styles와 variables
   - 이미 사용된 Auto Layout 구조
2) 원본 component set이 있으면 새 파일로 가져와 이름, property, variant, Auto Layout만 정리한다. 동일 기능을 가진 새 component set을 따로 만들지 않는다.
3) 원본 화면 안의 component instance는 가능한 한 인스턴스 관계를 유지한 채 새 파일로 가져온다. detached copy를 기본 작업 방식으로 쓰지 않는다.
4) 아이콘·로고·메뉴 이미지·일러스트는 원본 asset을 재사용한다. 유사한 새 아이콘, placeholder 이미지, 다른 icon pack을 만들거나 섞지 않는다.
5) 원본의 color/text/effect style 또는 variable이 있으면 새 Foundations에서 이름을 정리하고 alias를 연결한다. 똑같은 값의 새 스타일을 중복 생성하지 않는다.
6) 원본에 없는 UI 또는 상태만 새 컴포넌트로 추가한다. 새로 만든 항목은 반드시 `Asset migration inventory`에 `New — reason: <원본에 없음>`으로 남긴다.
7) 중복 또는 잘못된 원본 컴포넌트를 통합해야 하는 경우, 기존 사용처를 정식 component set 인스턴스로 교체한 뒤에만 archive 처리한다. 사용처를 detached layer로 바꾸지 않는다.

재사용 판단 순서:
```text
원본 component/style/asset 존재?
├─ 예 → 복제/가져오기 → 이름·속성·레이아웃 정리 → 기존 instance 유지 → 새 파일에서 사용
└─ 아니오 → 기존 공통 컴포넌트로 조합 가능한가?
          ├─ 예 → 기존 instance 조합
          └─ 아니오 → 새 component 생성 + inventory에 생성 사유 기록
```

────────────────────────────────
1. 페이지 구조 (페이지 이름은 정확히 사용)
────────────────────────────────
새 파일에 아래 페이지를 이 순서대로 만든다.

`00. START HERE`
`01. Foundations`
`02. Components / Shared`
`03. Components / Kiosk`
`04. Components / Admin`
`05. Screens / Kiosk`
`06. Screens / Admin`
`07. User Flows & Prototype`
`08. Handoff / Specs`
`99. Archive / Imported Legacy`

- 기존 화면을 원형 보관해야 하면 `99. Archive / Imported Legacy`에만 둔다.
- 개발에 사용할 정리된 화면은 반드시 `05`, `06`에 둔다.
- 페이지 이름, 섹션 이름, 프레임 이름, 컴포넌트 이름에 이모지, 임시 이름, 한글/영문 혼용의 모호한 약어를 쓰지 않는다.

────────────────────────────────
2. 명명 및 레이어 규칙 (엄격 적용)
────────────────────────────────
금지 이름: `Frame 123`, `Group 4`, `Component 2`, `Variant2`, `Property 1`, `bg`, `copy`, `final final`, 숫자만 있는 이름.

모든 화면 루트 프레임 이름:
`SCR-XXX / Area / Screen / State=...`

예시:
- `SCR-001 / Kiosk / Home / State=Default`
- `SCR-004 / Kiosk / Menu Detail / State=Default`
- `SCR-007 / Kiosk / Payment / Summary=Collapsed`
- `SCR-009 / Admin / Order List / State=Default`
- `SCR-019 / Admin / Sales Summary / State=Default`

모든 레이어는 사용자에게 보이는 문구가 아니라 역할과 데이터 의미로 이름을 짓는다.

권장 레이어 구조:
```text
screen-root
├─ app-shell
│  ├─ global-header
│  ├─ side-navigation
│  └─ page-content
├─ page-header
│  ├─ title-area
│  └─ page-actions
├─ primary-content
├─ secondary-content
├─ overlay-layer
└─ __spec
```

- 반복 요소는 `menu-card/`, `order-row/`, `metric-card/`처럼 역할별 접두어를 사용한다.
- 아이콘 레이어는 `icon/Name`, 이미지 레이어는 `image/MenuName`, 텍스트는 `text/Role` 형식으로 명확하게 이름을 붙인다.
- 숨겨진 프로토타입용 레이어도 `prototype/...` 이름을 사용한다.
- 모든 화면의 루트 프레임 마지막 자식에 `__spec` 메모를 둔다. 메모에는 Route, Data, States, Actions를 적는다.

`__spec` 예시:
```text
Route: /admin/sales
Data: from, to, dailySales[], orderList[]
States: default | loading | empty | error
Actions: selectPeriod, openMonthlySales, openDailySales
```

────────────────────────────────
3. Foundations 및 디자인 토큰
────────────────────────────────
**중요 — 첨부 레퍼런스 이미지는 색상·크기·아이콘·UI 디자인의 출처가 아니라, 디자인 시스템을 전시하는 “정리 형식”의 레퍼런스다.** 이미지의 파랑, 숫자, 폰트 스케일, 컴포넌트 모양을 ASAK에 그대로 적용하거나 추측하지 않는다. ASAK 원본 파일에서 실제 사용 중인 시각 언어를 추출하여 그 값을 정리하고, 글꼴만 아래 지시에 따라 `Noto Sans KR`로 통일한다. 아래의 토큰명·카탈로그 예시는 **분류용 이름 예시일 뿐 수치/hex/효과값을 확정하지 않는다**. Figma 작업 시에는 원본에서 추출한 실제 값으로 교체하고, 원본에 없는 값은 `TBD — design decision required`로 표시해 임의로 결정하지 않는다.

`01. Foundations`는 첨부 레퍼런스처럼 큰 흰색 보드 위에 `Color`, `Typography / PC`, `Typography / MO`, `Iconography`, `Effects & Borders` 섹션을 **열(column) 단위로 병렬 배치**해 한눈에 검수 가능하게 구성한다. 각 섹션에는 토큰 샘플, 이름, 실제 값, 사용 상태를 표 또는 스와치로 보여 준다. 기존 원본의 실제 값을 우선 확인하되, 아래 토큰 명칭과 사용 규칙은 반드시 지킨다.

### 3-1. Typeface 및 Typography

- **유일한 제품 글꼴은 `Noto Sans KR`**로 지정한다. 영문, 숫자, 한글, 통화, 날짜, 버튼, 표, 차트 라벨 모두 `Noto Sans KR`을 사용한다. 별도 영문 Display 글꼴이나 Paperlogy를 사용하지 않는다.
- Figma에 `Noto Sans KR`이 제공되지 않을 경우에만 `Noto Sans`를 임시 대체로 쓰고, `00. START HERE`의 QA checklist에 `FONT FALLBACK USED`를 남긴다. 임의의 다른 글꼴로 대체하지 않는다.
- Font collection 또는 텍스트 스타일의 명칭은 `Type/...`로 통일하고, weight는 실제 값(`Regular 400`, `Medium 500`, `Bold 700`, `ExtraBold 800`)을 쓴다. `SemiBold`는 원본에 확정된 경우만 사용한다.
- 텍스트 색상은 스타일 내부에 하드코딩하지 않고 `Color/Text/*` variable로 연결한다.

PC/MO text style의 **행 구성과 표기 방식은 첨부 레퍼런스의 Typography 보드처럼** `스타일명 | Weight | Size | Line height | 예시(가나다 Aa 123)` 열로 만든다. 아래 항목은 필요한 스타일 카탈로그이며, 수치와 weight는 원본 ASAK 화면을 분석해 확정한다. 임의의 Paperlogy 스타일을 복사하지 않는다.

PC text styles (font family: Noto Sans KR, values to be extracted from ASAK source):
```text
Type/PC/Display/52: 52 / 68, Medium 500
Type/PC/Display/40: 40 / 56, Regular 400
Type/PC/Display/32: 32 / 44, Medium 500
Type/PC/Display/28: 28 / 40, Medium 500
Type/PC/Display/24: 24 / 34, Medium 500
Type/PC/Display/20: 20 / 30, Medium 500
Type/PC/Display/18: 18 / 28, Medium 500
Type/PC/Display/16: 16 / 24, Medium 500
Type/PC/Body/40: 40 / 56, ExtraBold 800
Type/PC/Body/28: 28 / 40, Bold 700; Medium 500
Type/PC/Body/24: 24 / 34, Bold 700; Medium 500
Type/PC/Body/20: 20 / 30, ExtraBold 800; Bold 700; Medium 500
Type/PC/Body/18: 18 / 28, Bold 700; Medium 500
Type/PC/Body/16: 16 / 24, Bold 700; Medium 500; Light 300
Type/PC/Body/14: 14 / 22, Bold 700; Medium 500; Light 300
Type/PC/Body/13: 13 / 20, Medium 500
Type/PC/Body/12: 12 / 18, Bold 700; Medium 500
```

MO text styles (font family: Noto Sans KR, values to be extracted from ASAK source):
```text
Type/MO/Display/52: 52 / 68, Medium 500; Regular 400
Type/MO/Display/32: 32 / 44, Medium 500
Type/MO/Display/28: 28 / 40, Medium 500
Type/MO/Display/24: 24 / 34, Medium 500
Type/MO/Display/20: 20 / 30, Medium 500
Type/MO/Display/18: 18 / 28, Medium 500
Type/MO/Display/16: 16 / 24, Medium 500
Type/MO/Body/28: 28 / 40, Bold 700
Type/MO/Body/24: 24 / 34, ExtraBold 800; Bold 700
Type/MO/Body/20: 20 / 30, Bold 700; Medium 500
Type/MO/Body/18: 18 / 28, Bold 700; Medium 500
Type/MO/Body/16: 16 / 24, Bold 700; Medium 500; Light 300
Type/MO/Body/14: 14 / 22, Bold 700; Medium 500; Light 300
Type/MO/Body/13: 13 / 20, Medium 500
Type/MO/Body/12: 12 / 18, Bold 700; Medium 500
```

- 본문 기본값은 PC `Type/PC/Body/16 / Medium`, 모바일 `Type/MO/Body/16 / Medium`이다.
- 버튼은 최소 14px Medium, 표/보조 정보는 최소 12px Medium으로 한다. 12px 미만 본문 텍스트는 만들지 않는다.
- 숫자 금액은 proportional numeral을 유지하되, 표의 비교 열은 필요할 때만 tabular figures를 적용한다.

### 3-2. Color variables

Collection은 `Color` 하나로 만들고 모드는 `Light`만 사용한다. `Mode 1`이라는 이름은 금지한다. primitive token과 semantic token을 분리하며, 컴포넌트와 화면은 반드시 semantic token만 사용한다. Color 보드는 첨부 레퍼런스처럼 좌측에 그룹명(Primary, Secondary, Surface, Text, Grayscale, Icon)을 두고, 우측에 스와치 + 토큰명 + hex 값을 행별로 전시한다.

```text
Color/Brand/Primary/Enabled   #00B0E1
Color/Brand/Primary/Pressed   #0091C2
Color/Brand/Primary/Disabled  #A1C7D6
Color/Brand/Secondary/Enabled #007DC5
Color/Brand/Secondary/Pressed #186995
Color/Brand/Secondary/Disabled #8FBAD2

Color/Surface/01              #D8F2FA
Color/Surface/02              #E8F6FB
Color/Surface/03              #F2FAFD
Color/Surface/04              #FFFFFF
Color/Surface/05              #2B2B2B
Color/Surface/06              #F3F6F6

Color/Text/Primary            #222222
Color/Text/Secondary          #51585E
Color/Text/Tertiary           #758185
Color/Text/Inverse            #FFFFFF
Color/Text/Link               {Color/Brand/Secondary/Enabled}

Color/Neutral/900             #222222
Color/Neutral/800             #344143
Color/Neutral/700             #51585E
Color/Neutral/600             #758185
Color/Neutral/500             #99A3A7
Color/Neutral/400             #C6D0D2
Color/Neutral/300             #E0E5E6
Color/Neutral/200             #EBEEEE
Color/Neutral/100             #EEF2F3
Color/Neutral/50              #F7F7F7

Color/Border/Default          {Color/Neutral/300}
Color/Border/Subtle           {Color/Neutral/200}
Color/Border/Strong           {Color/Neutral/600}
Color/Border/Focus            {Color/Brand/Primary/Enabled}
Color/Icon/Default            {Color/Text/Primary}
Color/Icon/Secondary          {Color/Text/Secondary}
Color/Icon/Brand              {Color/Brand/Primary/Enabled}

Color/Status/Success           #2E9B62
Color/Status/Success-Subtle    #E8F6EE
Color/Status/Warning           #E39A18
Color/Status/Warning-Subtle    #FFF6E3
Color/Status/Error             #D94343
Color/Status/Error-Subtle      #FDEDED
Color/Status/Info              {Color/Brand/Secondary/Enabled}
Color/Status/Info-Subtle       {Color/Surface/01}
```

- 위 hex 값은 확정 디자인 지시가 아니다. 새 파일을 만들 때 **ASAK 원본에 존재하는 실제 색상·그라디언트·상태색을 추출해 교체**한다. 첨부 이미지를 근거로 새 블루/그레이 팔레트를 만들지 않는다. 각 색상 보드에는 원본에서 가져온 최종 hex만 표시한다.
- disabled 상태는 opacity로 색을 흐리게 만들지 말고 해당 disabled token을 사용한다. 투명도가 필요한 overlay만 opacity를 사용한다.
- 위험/성공/경고 색상을 일반 본문·브랜드 장식에 재사용하지 않는다.

### 3-3. Gradients

Gradient는 별도 `Gradient` 보드에 linear/radial 미리보기 스와치, style name, stop color, angle, 사용처를 함께 표시한다. 원본에 없는 새 gradient를 임의로 추가하지 않는다. 장식적 강조와 hero/summary 영역에만 쓰고, 버튼·본문·표의 정보 전달에는 solid semantic token을 우선 사용한다.

```text
Gradient/Brand/Soft: linear 135deg, #00B0E1 0% → #007DC5 100%
Gradient/Brand/Pale: linear 135deg, #E8F6FB 0% → #D8F2FA 100%
Gradient/Surface/Blue-Wash: linear 180deg, #FFFFFF 0% → #F2FAFD 100%
Gradient/Overlay/Scrim: linear 180deg, rgba(34,34,34,0.00) 0% → rgba(34,34,34,0.56) 100%
```

- gradient는 `Gradient/...` paint style로만 사용한다. 노드마다 독립 Gradient fill을 만들지 않는다.
- 텍스트 위 gradient를 사용할 경우 WCAG AA 대비를 확인하고, 충족하지 않으면 단색 텍스트로 전환한다.

### 3-4. Stroke, Radius, Spacing

`Layout` collection에는 Spacing, Radius, Stroke 보드를 별도로 만들고, 첨부 레퍼런스처럼 각 값의 시각적 예시와 token name, 숫자 값을 함께 전시한다. 실제 scale은 ASAK 원본에서 추출해 확정하고 오토레이아웃 gap/padding, radius, stroke에 직접 바인딩한다.

```text
Space/0=0, Space/2=2, Space/4=4, Space/6=6, Space/8=8,
Space/12=12, Space/16=16, Space/20=20, Space/24=24,
Space/32=32, Space/40=40, Space/48=48, Space/64=64

Radius/None=0, Radius/XS=4, Radius/SM=8, Radius/MD=12,
Radius/LG=16, Radius/XL=24, Radius/Full=999

Stroke/Hairline=1, Stroke/Default=1, Stroke/Strong=2,
Stroke/Focus=2
```

- 기본 카드·입력창은 `Radius/MD`와 `Stroke/Default`를 사용한다.
- 작은 태그/칩은 `Radius/Full` 또는 `Radius/SM`, 모달은 `Radius/LG`, 이미지 썸네일은 용도에 맞는 `Radius/SM` 또는 `Radius/MD`를 사용한다.
- Focus 상태는 `Color/Border/Focus` 2px stroke로 표현하고, 색상만으로 상태를 구분하지 않는다.
- 카드 테두리는 `Color/Border/Subtle`, 입력/테이블 구분선은 `Color/Border/Default`, 선택된 항목은 `Color/Border/Focus`를 사용한다.

### 3-5. Shadows and effects

Effect 보드는 elevation별 카드 미리보기, style name, X/Y/blur/spread/색상/opacity를 한 행씩 보여 주는 형식으로 만든다. 실제 shadow 수치는 ASAK 원본의 사용값을 추출해 확정한다. 불투명한 검정 대신 neutral 기반의 낮은 농도를 사용하며, 컴포넌트별로 임의 shadow 값을 만들지 않는다.

```text
Elevation/None: none
Elevation/XS: 0 1 2 0 rgba(34,34,34,0.08)
Elevation/SM: 0 2 6 0 rgba(34,34,34,0.10)
Elevation/MD: 0 8 20 0 rgba(34,34,34,0.12)
Elevation/LG: 0 16 40 0 rgba(34,34,34,0.16)
Elevation/Focus: 0 0 0 3 rgba(0,176,225,0.24)
```

- 일반 카드: `Elevation/XS` 또는 border만 사용한다.
- hover 가능 요소: 기본 `Elevation/XS` → hover `Elevation/SM`.
- drawer, modal, floating save bar: `Elevation/MD`; 중요한 full dialog만 `Elevation/LG`.
- 그림자는 레이어 효과로만 적용한다. shadow 색을 fill로 만들어 겹치지 않는다.
- background blur는 modal/drawer overlay 외에 쓰지 않으며, overlay fill은 `rgba(34,34,34,0.48)`을 기본으로 한다.

### 3-6. Icons, grid, documentation

- Iconography 보드는 첨부 레퍼런스처럼 `12 / 16 / 20 / 24 / 32 / 40 / 48` 사이즈별 섹션으로 나누고, 각 줄에 실제 아이콘 인스턴스를 배치한다. 아이콘은 인스턴스 교체가 가능하도록 `Icon/...` 컴포넌트로 정리한다.
- 기본 icon 색상은 `Color/Icon/Default`, 비활성은 `Color/Neutral/500`, 브랜드 강조는 `Color/Icon/Brand`만 사용한다.
- PC와 kiosk는 8pt spacing grid, 모바일은 4pt의 배수로 정렬한다. grid style도 `Grid/Desktop`, `Grid/Tablet`, `Grid/Mobile`로 명시한다.
- Foundations의 각 샘플에는 이름, 실제 값, 연결된 variable/style, 권장 사용처를 표시한다. Do/Don't 메모도 짧게 남긴다.

────────────────────────────────
4. 공통 컴포넌트와 속성
────────────────────────────────
컴포넌트는 반드시 최상위 Component Set으로 만들고, 인스턴스 복제본을 컴포넌트처럼 방치하지 않는다. 단, 아래 목록을 별도로 새로 그리라는 뜻으로 해석하지 말고 **원본의 같은 컴포넌트를 먼저 찾아 가져와 정식 이름·속성으로 정리하는 목표 목록**으로 사용한다. 상태 변화는 필요한 경우에만 Variant로 만들고, 텍스트·아이콘·단순 표시 여부는 Component Property를 우선 사용한다.

공통 컴포넌트:
- `Shared/Button`
  - properties: `variant=primary|secondary|tertiary|danger`, `size=sm|md|lg`, `state=default|hover|pressed|disabled|loading`, `label` Text, `leadingIcon` Instance swap, `trailingIcon` Instance swap
- `Shared/Modal`
  - properties: `type=confirm|paymentError|timeout|info`, `title` Text, `description` Text, `primaryLabel` Text, `secondaryLabel` Text
- `Shared/Badge`
  - properties: `status=received|preparing|completed|cancelled|paymentPending|paymentFailed|refunded`, `label` Text
- `Shared/EmptyState`
  - properties: `type=general|sales|paymentMethods|orders`, `title` Text, `description` Text, `showAction` Boolean
- `Shared/ErrorState`
  - properties: `type=load|save|payment`, `title` Text, `description` Text, `retryLabel` Text
- `Shared/LoadingState`
  - properties: `type=page|card|table|button`
- `Shared/ConfirmDialog`
  - properties: `type=delete|discardChanges|disableAllPaymentMethods`, `title` Text, `description` Text

키오스크 컴포넌트:
- `Kiosk/OrderTypeButton`: `type=eatIn|takeOut`, `state=default|selected|disabled`, `label` Text
- `Kiosk/MenuCard`: `menuName`, `price`, `calories` Text; `image` Instance swap; `soldOut`, `recommended`, `ingredientSoldOut` Boolean
- `Kiosk/CategoryTab`: `label` Text, `selected` Boolean, `disabled` Boolean
- `Kiosk/OptionCategory`: `title` Text, `required` Boolean, `maxSelectable` Text, `status=default|error|soldOut`
- `Kiosk/CartItem`: `menuName`, `optionSummary`, `quantity`, `unitPrice` Text; `soldOut`, `expanded` Boolean
- `Kiosk/PaymentMethodCard`: `methodName` Text, `selected`, `disabled` Boolean, `icon` Instance swap
- `Kiosk/AllergenTag`: `type=nut|milk|egg|shellfish|soy|wheat|etc`, `state=default|warning`, `label` Text
- `Kiosk/DietaryTag`: `type=vegan|vegetarian|etc`, `label` Text
- `Kiosk/AllergenNotice`: `state=default|hasAllergen|optionChanged`, `title` Text, `description` Text
- `Kiosk/AllergenDetailModal`: 성분명 및 포함 출처(기본 구성/추가 옵션) 표시

관리자 컴포넌트:
- `Admin/OrderStatusBadge`
- `Admin/DataTableRow`: `orderNo`, `orderType`, `paymentStatus`, `orderStatus`, `amount`, `orderedAt` Text
- `Admin/PaymentMethodSettingRow`: `state=enabled|disabled|maintenance`, `name`, `description` Text, `icon` Instance swap, `enabled` Boolean
- `Admin/PaymentMethodOrderControl`: `state=default|first|last`, `direction=up|down`
- `Admin/PaymentPolicyCard`: `policyType=resetOnFailure|notice|receipt`, `state=default|changed`
- `Admin/SaveBar`: `state=idle|dirty|saving|success|error`
- `Admin/SalesPeriodFilter`: `state=default|open|customRange|loading`
- `Admin/SalesMetricCard`: `metric=totalSales|orderCount|averageOrderValue`, `state=default|loading|empty`
- `Admin/SalesChart`: `granularity=daily|monthly`, `state=default|loading|empty|error`
- `Admin/SalesBreakdownTable`: `type=daily|monthly|menu|order`, `state=default|empty|loading|error`

동일한 기능의 `MenuCard`와 `Menu Card`처럼 이름만 다른 중복 컴포넌트는 새 파일에서 하나의 정식 컴포넌트로 통합한다.

────────────────────────────────
5. 키오스크 화면 (05. Screens / Kiosk)
────────────────────────────────
아래 화면을 만들거나 원본 화면을 재구성하고, 각 화면의 default와 필요한 예외 상태를 준비한다.

- `SCR-001 / Kiosk / Home / State=Default`
  - 매장/포장 선택, 선택 상태, 비활성 상태
- `SCR-003 / Kiosk / Menu List / State=Default`
  - 카테고리 탭, 추천/품절/이미지 없음 메뉴 카드, 가격·칼로리 표시
- `SCR-004 / Kiosk / Menu Detail / State=Default`
  - 필수 옵션 미선택 오류, 최대 선택 초과, 옵션 품절, 추가 금액 갱신 상태
  - `product-info`와 첫 `OptionCategory` 사이에 `allergen-section`을 삽입한다.
  - 레이어: `allergen-section > allergen-section-header, allergen-tag-list, allergen-notice`
  - 알레르기 위험 성분은 태그로 표시하고 옵션 선택으로 새 성분이 포함되면 warning notice로 바뀐다.
  - 의학적 안전 보장 문구는 쓰지 말고, 성분 정보 안내 문구만 사용한다.
- `SCR-005 / Kiosk / Cart / State=Default`
  - 빈 장바구니, 재고/품절 경고, 수량 최소·최대, 주문 확인 모달
- `SCR-007 / Kiosk / Payment / Summary=Collapsed`
- `SCR-007 / Kiosk / Payment / Summary=Expanded`
  - 결제수단 선택/비활성, 결제 버튼 로딩을 명확히 분리한다.
- `SCR-007 / Kiosk / Payment Processing / State=Default`
  - 카드 삽입/태깅 대기, 취소 가능 여부, 진행 상태
- `SCR-012 / Kiosk / Payment Error / State=Default`
  - 오류 코드, 재시도, 장바구니 복귀, 금액 불일치 안내
- `SCR-013 / Kiosk / Timeout Modal / State=Default`
  - 남은 시간, 주문 계속, 처음으로 버튼, 자동 초기화 결과
- `SCR-008 / Kiosk / Order Complete / State=Default`
  - `orderNo`, `paidAt`, `paymentStatus`, 영수증 선택 및 출력 실패 상태
- `SCR-014 / Kiosk / Accessibility / State=Default`
  - 글자 크기, 고대비 적용/되돌리기 상태

키오스크 화면은 실제 키오스크 기준으로 넉넉한 터치 영역과 버튼 간 간격을 유지한다. 각 화면은 app shell, 콘텐츠, 하단 CTA가 구조적으로 분리되어야 한다.

────────────────────────────────
6. 관리자 화면 (06. Screens / Admin)
────────────────────────────────
아래 모든 화면은 기본, loading, empty, error 상태를 필요한 수준으로 준비한다.

- `SCR-015 / Admin / Login / State=Default`: 기본, 입력 오류, 로그인 진행, 권한 없음
- `SCR-009 / Admin / Order List / State=Default`: 전체/상태 필터, 검색, loading, empty, error, pagination
- `SCR-010 / Admin / Order Detail / State=Default`: 상태별 섹션, 변경 확인, 변경 실패, 옵션/제외 재료
- `SCR-011 / Admin / Sold-out Management / State=Default`: 메뉴/재료 구분, 토글 진행/성공/실패, 품절 사유
- `SCR-016 / Admin / Menu Management / State=Default`: 검색, 필터, 정렬, 빈 목록, 메뉴 등록 진입
- `SCR-017 / Admin / Menu Edit / State=Create`: 등록/수정, 필수값 오류, 이미지 없음/업로드/취소/실패
- `SCR-018 / Admin / Payment Methods / State=Default`
  - 수단 목록, 아이콘, 이름, 설명, 활성 여부, 노출 순서, 정책 카드
  - 변경되면 `Admin/SaveBar`가 dirty로 표시된다.
  - 저장 중/성공/오류 상태와 “모든 결제수단 비활성화”, “변경사항 버리기” 확인 다이얼로그를 만든다.
  - 실제 설정 저장 API가 확정되지 않았으므로 화면에 `Mock settings` 또는 `연동 예정`임을 __spec에 명시한다.
- `SCR-019 / Admin / Sales Summary / State=Default`
  - 기간 필터: 오늘, 최근 7일, 이번 달, 직접 선택
  - 총매출, 총 주문 수, 평균 객단가
  - 일별 매출 추이, 메뉴별 판매량 상위 목록, 최근 주문 목록
  - 별도 화면: `SCR-020 / Admin / Monthly Sales / State=Default`, `SCR-021 / Admin / Daily Sales / State=Default`

매출 화면의 실제 사용 가능 데이터는 아래로 제한한다.
- 일별 매출 API: `date`, `orderCount`, `totalAmount`
- 관리자 주문 목록: `orderNo`, `orderType`, `totalPrice`, `orderStatus`, `paymentStatus`, `createdAt`, `items[].menuName`, `items[].quantity`

따라서 시간대별 매출, 결제수단별 매출, 전년/전월 비교, 목표 달성률, 환불/취소 분석은 수치를 가공해 만들지 않는다. 해당 영역이 필요하면 `데이터 연결 예정` 카드와 필요한 필드를 명시한다.

────────────────────────────────
7. 프로토타입 (07. User Flows & Prototype)
────────────────────────────────
`07. User Flows & Prototype`에 흐름도와 실제 클릭 가능한 프로토타입 시작 프레임을 만든다. 흐름도는 화살표와 조건 레이블을 사용해 다음 분기를 모두 표현한다.

키오스크 대표 흐름:
1) Home → 매장/포장 선택 → Menu List → Menu Detail
2) 옵션을 정상 선택 → 장바구니 추가 → Cart → Payment Summary Collapsed → 결제수단 선택 → Payment Processing → Order Complete
3) 필수 옵션 미선택 → Menu Detail의 오류 상태
4) 품절 메뉴 또는 옵션 → 선택 불가/경고 상태
5) 결제 실패 → Payment Error → 재시도 또는 장바구니 복귀
6) 시간 초과 → Timeout Modal → 주문 계속 또는 처음으로
7) 접근성 버튼 → Accessibility → 적용 → 이전 화면 복귀

관리자 대표 흐름:
1) Login → Order List → Order Detail → 주문 상태 변경 확인 → 성공 또는 실패
2) Sold-out Management → 토글 변경 → 진행 → 성공 또는 실패
3) Payment Methods → 활성화/순서 변경 → SaveBar dirty → 저장 → success/error
4) Sales Summary → 기간 선택 → Monthly Sales 또는 Daily Sales

프로토타입 연결 규칙:
- 각 화면의 실제 CTA와 메뉴/탭만 연결한다. 장식 레이어 전체에 연결하지 않는다.
- 기본 전환은 `Navigate to` + `Smart animate`(200~300ms, Ease out)를 사용한다.
- 모달은 `Open overlay`, 닫기는 `Close overlay`를 사용하고, 배경 클릭 닫힘이 적절한 모달에만 적용한다.
- 토글, 탭, 요약 확장/축소는 가능하면 component interactive variant로 연결한다.
- 로딩은 실제 기다림을 흉내 내는 긴 지연보다 명확한 별도 상태 프레임으로 연결한다.
- 시작점 이름: `Prototype Start / Kiosk Order`, `Prototype Start / Admin Operations`
- 모든 연결 대상은 정식 화면 프레임이어야 하며 archive 프레임에 연결하지 않는다.

────────────────────────────────
8. Handoff 및 MCP 준비 (08. Handoff / Specs)
────────────────────────────────
1) `Screen Inventory` 테이블을 만든다: Screen ID, Figma frame name, route, code page/component, states, prototype entry.
2) `Component Inventory` 테이블을 만든다: Figma component, properties, intended frontend component.
3) 아래 코드 매핑을 기록한다.
   - `Shared/Button` → `frontend/src/components/common/Button.jsx`
   - `Shared/Modal` → `frontend/src/components/common/Modal.jsx`, `ConfirmDialog.jsx`
   - `Kiosk/MenuCard` → `frontend/src/components/kiosk/MenuCard.jsx`
   - `Kiosk/CategoryTab` → `frontend/src/components/kiosk/CategoryTabs.jsx`
   - `Kiosk/CartItem` → `frontend/src/components/kiosk/CartItem.jsx`
   - `Kiosk/OptionCategory` → `frontend/src/components/kiosk/OptionGroup.jsx`
   - `Kiosk/PaymentMethodCard` → `frontend/src/components/kiosk/PaymentMethodList.jsx`
   - `Kiosk/OrderTypeButton` → `frontend/src/components/kiosk/OrderTypeSelector.jsx`
   - `Admin/OrderStatusBadge` → `frontend/src/components/admin/OrderStatusBadge.jsx`
   - `Admin/DataTableRow` → `frontend/src/components/admin/OrderTable.jsx`
   - `Admin/SoldOutToggle` → `frontend/src/components/admin/SoldOutToggle.jsx`
4) Code Connect의 대상은 화면 프레임이 아니라 최상위 Component Set임을 명시한다.
5) MCP가 읽기 쉽도록 모든 디자인 요소의 이름, variant property, text property가 의미 있는 영어 식별자인지 최종 점검한다.

────────────────────────────────
9. 완료 전 강제 검수
────────────────────────────────
다음 항목을 모두 확인하고, `00. START HERE`에 `QA checklist`로 체크 상태를 남긴다.

- [ ] 원본 파일은 변경하지 않았고 새 파일에서만 작업했다.
- [ ] 새 파일의 9개 페이지가 지정된 순서와 이름으로 존재한다.
- [ ] `Frame`, `Group`, `Component`, `Variant`, `Property`의 자동 생성 이름이 남아 있지 않다.
- [ ] 모든 화면 루트 프레임이 `SCR-XXX / Area / Screen / State=...` 규칙을 따른다.
- [ ] 모든 화면에 `__spec`이 있고 route/data/states/actions가 적혀 있다.
- [ ] 모든 반복 UI가 Auto Layout과 정식 컴포넌트 인스턴스를 사용한다.
- [ ] Button, MenuCard, OptionCategory, CartItem, PaymentMethodCard, Badge가 속성과 상태를 갖춘 Component Set이다.
- [ ] 키오스크의 빈/로딩/오류/필수 옵션 오류/결제 실패/시간 초과 상태가 있다.
- [ ] 관리자의 빈/로딩/오류/저장 실패/권한 없음 상태가 있다.
- [ ] 알레르기 섹션과 옵션 변경 경고가 Menu Detail에 있다.
- [ ] 미확정 매출 데이터에 가짜 수치가 없고 `데이터 연결 예정`으로 처리했다.
- [ ] 키오스크와 관리자 프로토타입 시작점 및 핵심 분기 연결이 작동한다.
- [ ] `08. Handoff / Specs`에 Screen/Component inventory와 코드 매핑이 있다.

완료 보고는 아래 형식으로 간단히 작성한다.
1. 새 파일 링크와 이름
2. 원본 보존 여부
3. 생성한 페이지 및 화면 수
4. 생성/정리한 Component Set 목록
5. 연결한 프로토타입 플로우 목록
6. 데이터 연결 예정으로 남긴 항목
7. 남은 수동 확인 항목
```

## 내일 MCP 실행 시 권장 순서

1. 새 Figma 파일을 만든 뒤 위 프롬프트의 0~2단계만 먼저 실행하고, 페이지·이름·원본 보존을 확인한다.
2. Foundations → Components → Screens 순서로 작성한다. 화면부터 만들면 중복 컴포넌트와 레이어명이 다시 생긴다.
3. 화면과 상태가 모두 마련된 뒤에만 Prototype과 Handoff 페이지를 연결한다.
4. 마지막으로 `00. START HERE`의 QA checklist를 MCP로 다시 읽어, 미체크 항목을 보완한다.

## 원본 대비 핵심 변경점

- 기존 원본을 고치지 않고 별도 파일에서 재구성한다.
- 화면 명칭을 `k001`, `A-006` 같은 내부 임시명에서 `SCR-XXX / Area / Screen` 규칙으로 정규화한다.
- 화면뿐 아니라 컴포넌트 속성, 상태, `__spec`, 프로토타입, Code Connect 매핑까지 인계 범위에 넣는다.
- 현재 API로 만들 수 없는 분석은 가짜 데이터 대신 명확한 연결 예정 상태로 남긴다.
