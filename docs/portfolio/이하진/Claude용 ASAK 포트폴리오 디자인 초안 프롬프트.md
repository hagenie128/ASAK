너는 Senior Product Designer이자 Frontend Designer다.

아래 내용을 기반으로 **한국어 개발자 포트폴리오 웹사이트의 디자인 초안**을 만들어라.

목표는 흔한 AI 생성 포트폴리오처럼 보이는 것이 아니라, 실제 디자이너가 편집한 듯한 **절제된 Editorial + Product Case Study 스타일**을 만드는 것이다.

포트폴리오의 주인공은 **이하진**, 프로젝트는 **ASAK(A Salad A Kiosk)​**이다.

---

# 1. 가장 중요한 디자인 방향

이 포트폴리오는 단순히

- React 사용
- Spring Boot 사용
- API 몇 개 구현
- DB 연결

같은 기술 목록을 보여주는 사이트가 아니다.

핵심은 다음 인상을 주는 것이다.

> “이 사람은 요구사항을 그대로 받아 코딩만 하는 사람이 아니라,  
> 사용자의 실제 업무 흐름을 보고 문제를 정의하고,  
> 기획 → 디자인 → 프론트 → API → DB → 검증까지 연결해서 일할 줄 안다.”

면접관이 사이트를 1~2분 정도 훑었을 때

**“주니어인데 일하는 방식이 꽤 실무적이다.”**

라는 인상을 받을 수 있도록 구성한다.

---

# 2. 반드시 피해야 할 AI스러운 디자인

아래 스타일은 사용하지 않는다.

- 보라색 / 파란색 네온 그라데이션
- 과도한 Glassmorphism
- 흐릿한 원형 blob 배경
- 의미 없는 그라데이션 텍스트
- 모든 요소를 둥근 카드 안에 넣는 구성
- 카드 6~8개를 동일한 크기로 반복하는 Bento Grid 남발
- 개발자 포트폴리오에서 흔한 가짜 Terminal UI
- `<Hello World />` 같은 클리셰
- 지나치게 큰 이모지
- GitHub contribution 스타일을 장식으로 사용하는 것
- 스킬을 pill badge 수십 개로 나열하는 것
- Tailwind 기본 예제처럼 보이는 UI
- 모든 섹션에 shadow / border / radius를 동시에 적용하는 것
- 20~32px 수준의 과도한 border-radius
- 의미 없는 아이콘 남발
- 텍스트보다 장식 요소가 더 눈에 띄는 구성
- 모든 텍스트를 중앙 정렬하는 레이아웃
- 지나치게 완벽하게 대칭적인 AI식 레이아웃
- “Passionate Developer”, “Creative Developer” 같은 추상적인 자기소개
- 과도한 스크롤 애니메이션
- 마우스 따라 움직이는 장식
- 숫자가 날아다니는 장식
- 불필요한 3D 오브젝트

전체적으로 **AI가 만든 포트폴리오 템플릿 느낌을 최대한 제거한다.**

---

# 3. 전체 무드

키워드:

- Editorial
- Product Case Study
- Documentation
- Minimal
- Professional
- Calm
- Structured
- Slightly technical
- Korean typography
- Magazine-like layout
- 실제 프로젝트 리포트 같은 밀도

느낌은

**개발자 개인 홈페이지 40% + 제품 디자인 케이스 스터디 40% + 잘 편집된 프로젝트 리포트 20%**

정도로 구성한다.

너무 차갑거나 기업 홈페이지처럼 만들지는 않는다.

개인의 취향과 감각은 느껴지되, 디자인이 콘텐츠보다 앞서지 않아야 한다.

---

# 4. 폰트

한글 및 전체 UI의 메인 폰트는 반드시 **Paperlogy(페이퍼로지)​**를 사용한다.

가능하다면 다음과 같이 weight를 구분한다.

- Paperlogy 3 / 4: 본문
- Paperlogy 5 / 6: 소제목, UI
- Paperlogy 7 / 8: Hero 및 주요 숫자

영문 코드, API Path, 기술적인 짧은 문자열만 monospace를 제한적으로 사용할 수 있다.

Monospace는 장식이 아니라 다음과 같은 부분에만 사용한다.

- `/api/admin/sales/daily`
- `React → API → Service → Mapper → DB`
- `8.0s → 0.43s`
- 파일명 및 코드 경로

본문까지 monospace로 만들지 않는다.

---

# 5. 컬러 시스템

전체 배경은 순백색보다 살짝 부드러운 Off-white 계열로 한다.

예시:

- Background: `#F5F4F0` 또는 비슷한 warm off-white
- Main text: 거의 black에 가까운 charcoal
- Secondary text: neutral gray
- Divider: 연한 warm gray

Accent color는 하나만 사용한다.

추천 방향:

- muted olive
- dark green
- deep burgundy
- muted navy

중 하나.

샐러드 프로젝트라고 해서 밝은 초록색을 과하게 사용하지 않는다.

Accent는

- 숫자
- 링크
- 작은 라벨
- 핵심 Diagram
- 중요한 결과값

정도에서만 제한적으로 사용한다.

---

# 6. 레이아웃

Desktop 기준 최대 콘텐츠 폭은 약 **1240~1360px**.

본문 텍스트가 화면 전체 폭으로 길어지지 않게 한다.

긴 설명 구간에서는 약 680~760px 정도의 읽기 좋은 폭을 유지한다.

전체 레이아웃은 강한 12-column grid를 기반으로 하되, 카드형 UI보다 **텍스트와 이미지의 비대칭 배치**를 적극 사용한다.

예:

```text
01 / PROJECT

큰 제목                     작은 프로젝트 정보
큰 제목                     작은 프로젝트 정보

────────────────────────────────────────────

설명 본문 7 columns          프로젝트 메타 3 columns
```

또는

```text
문제 설명 5 columns          실제 화면 이미지 7 columns
```

처럼 구성한다.

모든 섹션을 같은 레이아웃으로 반복하지 않는다.

---

# 7. 첫 화면 Hero

Hero는 지나치게 거대한 이름 중심이 아니라 프로젝트와 개발자의 사고방식이 먼저 보이도록 한다.

예시 구조:

작은 상단 라벨:

`PRODUCT / FRONTEND / BACKEND`

메인:

# ASAK
### 매장 운영 흐름까지 설계한  
### 샐러드 키오스크 관리자 시스템

보조 설명:

“화면을 만드는 데서 멈추지 않고, 매장 직원이 믿고 사용할 수 있는 운영 흐름인지 끝까지 확인했습니다.”

아래에는 짧은 Meta 정보를 배치한다.

```text
2026.07 — 2026.08
2-person Team
Admin Domain Owner
Figma · React · Spring Boot · MySQL
```

Hero에서 기술 스택을 badge 10개로 나열하지 않는다.

텍스트 기반으로 담백하게 보여준다.

Hero 오른쪽 또는 아래에는 프로젝트 전체 흐름을 보여주는 실제 관리자 화면 캡처 또는 Figma 이미지가 들어갈 공간을 만든다.

Mockup 기기 프레임 속에 억지로 넣지 말고 원본 UI 캡처가 잘 보이게 한다.

---

# 8. Intro / Project Overview

프로젝트 개요는 단순 소개문보다

**문제 → 관점 → 역할**

순서로 보여준다.

예:

### 무엇을 만들었나

샐러드 주문 키오스크와 매장 운영 관리자 시스템.

### 내가 본 핵심 문제

주문·메뉴·품절·결제·매출이 화면에서는 서로 다른 기능이지만, 실제 매장에서는 하나의 데이터 흐름이라는 점.

### 내가 맡은 범위

Figma → React → Admin API → DB 계약 → 검증/운영 문서

이를 시각적으로 다음처럼 표현한다.

```text
Figma
 ↓
React
 ↓
API Contract
 ↓
Spring Boot
 ↓
MyBatis
 ↓
MySQL
 ↓
Real DB Verification
```

단, 흔한 아이콘 플로우차트처럼 만들지 말고, 편집 디자인처럼 선과 텍스트만 사용한다.

---

# 9. “How I Work” 섹션

이 섹션은 매우 중요하다.

제목 예시:

## How I Work

또는

## 기능보다 먼저 운영을 봅니다

내용은 3개의 큰 원칙으로 구성한다.

### 01. 사용자의 다음 행동을 먼저 생각합니다

- 관리자 화면은 직원의 업무 도구
- 버튼이 있는지보다 올바른 상태에서 올바른 행동이 가능한지 확인

### 02. “보인다”와 “운영된다”를 구분합니다

다음 단계를 작은 vertical progression으로 표현한다.

```text
Static UI
Mock
API Contract
Backend
Database
Real DB
Browser
Device
```

완료 여부를 하나의 checkbox로 표현하지 않고, 여러 단계의 validation 과정처럼 보여준다.

### 03. 문제가 생기면 책임 계층까지 따라갑니다

```text
React
↓
API
↓
Controller
↓
Service
↓
Mapper
↓
DB View
```

이 구조는 개발자의 사고방식을 보여주는 핵심 Visual로 사용한다.

---

# 10. Project Timeline

7월 초부터 8월 21일까지의 흐름을 시각화한다.

단순 연대표보다는 프로젝트가 어떻게 성숙해졌는지 보여준다.

예:

```text
01
Foundation
협업 구조 / React / Mock

02
Design System
Figma / Components / UI States

03
Admin Domain
Orders / Menu / Sold-out

04
Data Contract
API / DB / MyBatis

05
Operations
Sales / Dashboard / Performance

06
Device Extension
RTOS / Receipt
```

각 단계마다 모든 상세 내용을 적지 말고,

**“무엇을 만들었는지 + 그때 어떤 판단을 했는지”**

를 1~2문장으로 보여준다.

---

# 11. 핵심 Case Study 구성

전체 기능을 전부 같은 깊이로 보여주지 않는다.

다음 **4개 사례를 핵심 케이스 스터디**로 크게 구성한다.

---

## CASE 01 — 품절 정책

제목 예:

### 품절 기능을 토글이 아니라 운영 정책으로 다시 정의했습니다

구조:

**Problem**

“품절 관리”라는 한 줄 요구만 있었으며 메뉴·재료·옵션 범위가 정의되지 않음.

**Decision**

데이터 모델과 관리자 화면 정책을 분리.

**Implementation**

`vw_soldout_catalog`

Menu / Ingredient / Option Item을 통합 구조로 제공.

관리자 화면에는 메뉴와 재료만 노출.

**Why**

현재 사용성은 단순하게 유지하면서 향후 옵션 품절 확장을 막지 않기 위해.

Visual:

왼쪽 문제 설명 + 오른쪽 실제 Admin Sold-out 화면.

그 아래 작게 데이터 구조 Diagram.

---

## CASE 02 — 매출 데이터

제목 예:

### 차트를 만들기 전에 “관리자가 무엇을 판단해야 하는가”를 먼저 정했습니다

다음 질문을 크게 Typography로 보여준다.

- 오늘 장사가 어떤가?
- 이번 주는 지난주보다 나은가?
- 어느 시간대에 주문이 몰렸는가?
- 취소가 매출에 얼마나 영향을 줬는가?

그 다음 API 분리를 보여준다.

```text
Summary
Monthly
Daily
Time Slots
```

API path는 작게 표현한다.

여기서 API 이름보다 **왜 책임을 분리했는지**가 더 크게 보여야 한다.

---

## CASE 03 — 빈 시간대 처리

제목:

### “데이터 없음”과 “매출 0원”을 구분했습니다

시각적으로 매우 단순하게:

```text
10:00    ₩35,000
10:30    —
11:00    ₩72,000
```

↓

Service 보정

↓

```text
10:00    ₩35,000
10:30    ₩0
11:00    ₩72,000
```

그리고 아래 한 문장:

> DB에는 실제 발생한 데이터만 저장하고,  
> 화면에 필요한 연속된 시간축은 Service에서 구성했습니다.

이 부분은 기술 설명이지만 매우 직관적으로 디자인한다.

---

## CASE 04 — Dashboard Performance

이 케이스는 시각적으로 강하게 보여준다.

제목:

### 약 8초 걸리던 대시보드를 0.5초 안쪽으로 줄였습니다

큰 숫자:

**8.0s → 3.8s → 0.43~0.50s**

숫자는 사이트 전체에서 가장 강한 Visual hierarchy를 사용한다.

단순히 최종 성과만 보여주지 않고 과정도 표현한다.

```text
01
DB Query 10 → 6
3.7~3.9s

02
View 변경 시도
Performance ↓

03
측정 후 원복

04
최근 주문 조회 병목 확인
Base Table 직접 조회

05
0.43~0.50s
```

특히 “실패 → 측정 → 원복”을 숨기지 않는다.

이를 통해

**감이 아니라 측정으로 최적화했다**

는 메시지를 전달한다.

---

# 12. Team / Project Operation 섹션

제목 예:

## 코드 외에도 프로젝트가 굴러가는 방식을 만들었습니다

내용:

- Daily Worklog
- Detailed Entry
- WBS
- Meeting Minutes
- Bruno
- Git History

이것을 Tool Logo Grid로 만들지 않는다.

실제 문서 캡처와 작은 설명을 사용한다.

예:

왼쪽:

Daily screenshot

오른쪽:

> 오늘 작업 / Blocker / 다음 작업을 공유

다음:

Entry screenshot

> 변경 이유 / 계약 / 검증 결과 / 미검증 항목 기록

이 섹션의 핵심 메시지:

> 문서를 결과 보고서가 아니라 다음 사람이 안전하게 이어서 일하기 위한 도구로 사용했다.

---

# 13. 2인 팀 전환 / 우선순위 재설계

이 내용도 꼭 보여준다.

제목:

## 팀이 줄었을 때, 기능 수보다 흐름 완성을 선택했습니다

초기 여러 기능을 모두 완성하려고 하는 대신 다음 핵심 운영 흐름을 우선했다.

```text
Menu
↓
Sold-out
↓
Order
↓
Payment
↓
Admin Processing
↓
Cancel
↓
Sales
↓
Dashboard
```

RTOS / Receipt는 그 이후 Extension으로 배치.

이 섹션은 **프로젝트 관리와 우선순위 판단 능력**을 보여주는 데 사용한다.

---

# 14. Validation 섹션

제목:

## Done의 기준을 나눴습니다

일반적인 checkbox 형태가 아니라 Progress / Stage 형태로 만든다.

예:

```text
01  UI
02  Mock
03  API Contract
04  Backend
05  DB
06  Real DB
07  Browser
08  Device
```

일부 프로젝트 화면을 예로 들어 각 단계가 어디까지 되었는지 표시할 수 있는 UI를 디자인한다.

목적은 완성도가 낮아 보이는 것이 아니라

**검증 기준을 엄격하게 관리했다는 인상**

을 주는 것이다.

---

# 15. Tech Stack

기술 스택은 매우 간결하게.

카드나 아이콘 20개 사용 금지.

텍스트 리스트로 다음처럼 정리한다.

```text
Frontend
React / Vite / Zustand / Axios

Backend
Java / Spring Boot / MyBatis

Data
MySQL / SQL View / Bruno

Design & Ops
Figma / Cloudinary / GitHub / PWA
```

가능하면 2-column 또는 4-column typography layout.

---

# 16. 마지막 섹션

일반적인

“Thanks for watching”
“Let's work together”

같은 문구는 쓰지 않는다.

대신 프로젝트를 통해 형성된 개발자의 태도로 끝낸다.

예:

## 내가 만들고 싶은 것은  
## “동작하는 화면”보다 “믿고 쓸 수 있는 시스템”입니다.

본문:

요구사항을 그대로 구현하기보다 실제 사용 흐름을 이해하고,  
문제가 생기면 어느 계층의 책임인지 확인하고,  
내가 보장하지 못하는 기능은 완료라고 말하지 않는 개발자가 되고 싶습니다.

아래에는

**이하진 / Full-stack Developer**

정도의 작은 서명만 배치한다.

---

# 17. 이미지 사용 방식

페이지에는 다음 이미지가 들어갈 수 있도록 placeholder를 만든다.

1. ASAK 관리자 Dashboard
2. 주문 Live 화면
3. Sold-out 관리 화면
4. 매출 Daily / Time Slot 화면
5. Figma Design System
6. Worklog Daily
7. Detailed Entry / WBS
8. Bruno API Response
9. Performance 측정 자료

이미지가 들어가는 자리는 의미 없는 mockup device 안에 넣지 않는다.

실제 UI가 잘 보이도록 큰 이미지 또는 crop 형태로 사용한다.

이미지마다 작은 caption을 붙인다.

예:

`Admin / Sales / 30min Time Slot`

---

# 18. 디테일

- border는 1px neutral gray 위주
- shadow는 정말 필요한 경우만 사용
- radius는 0~8px 중심
- 16px 이상의 둥근 카드 남발 금지
- section 사이 여백은 넉넉하게
- 본문 line-height는 읽기 편하게
- 숫자는 크게 사용 가능
- 섹션 번호 `01`, `02`, `03`을 편집 디자인 요소로 사용
- dividers 적극 활용
- 작은 uppercase 영문 label 사용 가능
- 아이콘보다 Typography 중심
- hover animation은 150~250ms 정도로 매우 절제
- scroll animation은 fade/translate 정도만 약하게
- 모바일에서도 내용 순서와 계층이 유지되도록 responsive 설계

---

# 19. 결과물 요청

먼저 코드부터 작성하지 말고 다음 순서로 결과를 제시한다.

1. 전체 Visual Direction
2. Color / Typography System
3. Grid / Spacing System
4. 전체 페이지 정보 구조
5. 각 Section의 Wireframe
6. Hero 시안
7. Case Study 시안
8. Mobile 대응 방식
9. 마지막에 실제 구현 가능한 HTML/CSS/React 구조 제안

디자인 판단에는 각각 이유를 짧게 적는다.

무엇보다 중요한 것은 **AI가 만든 화려한 포트폴리오가 아니라, 실제 개발자 한 명의 사고 과정과 프로젝트 운영 경험을 잘 편집한 포트폴리오​**처럼 보여야 한다.