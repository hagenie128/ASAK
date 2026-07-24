# ASAK AI 스킬 명령어 예시

> 상태: **Current** · 갱신: 2026-07-24
> 상세 원칙과 도구 설치 상태는 [12-ai-agent-tools-guide.md](12-ai-agent-tools-guide.md)를 먼저 확인한다.

## 사용 방법

아래 회색 상자 문장을 **그대로 AI 대화창에 붙여넣고**, 대괄호만 현재 작업에 맞게 바꾼다.

- ASAK 스킬은 보통 `/명령어`를 외우지 않아도, 요청의 한국어 주제어를 보고 자동 적용된다.
- `수정하지 마`를 붙이면 분석·설명·검토만 한다.
- 실제 수정은 팀원이 직접 하고, AI에는 수정 후 리뷰와 테스트 항목 확인을 요청한다.

## 구현 전에 공통으로 붙일 문장

```text
먼저 AGENTS.md, Product Bible, Screen Bible, 최신 Figma와 현재 Git 상태를 확인해.
Screen ID, Figma Frame/Node, Default·Loading·Empty·Error 상태, 화면 이동,
데이터 필드, 재사용 컴포넌트를 먼저 정리해. 코드·문서·Git 파일은 수정하지 마.
```

## 기존 ASAK 스킬별 예시

### API 연결 — `asak-api`

```text
API 연결 점검 - [SCR-009 / 주문 현황]
GET과 PATCH의 URL, 메서드, 요청·응답 필드, 상태값을 현재 mock과 비교해줘.
누락·이름 차이·Loading·Empty·Error 처리만 표로 정리하고 수정하지 마.
```

### React 화면 구조 — `asak-react-review`

```text
React 전체 점검 - [OrderListPage.jsx]
이 화면의 라우트 → 페이지 → 컴포넌트 → repository 데이터 흐름과 재사용 컴포넌트만 설명해줘.
직접 JSON import나 중복 상태가 있는지 확인하고 수정하지 마.
```

### Figma 화면 QA — `asak-figma-review`

```text
피그마 점검 - [SCR-009, Frame 39:7345]
Figma와 현재 코드의 문구, Default·Loading·Empty·Error 상태, 간격·색상·컴포넌트 재사용 차이만 알려줘.
Figma와 코드 모두 수정하지 마.
```

### 백엔드/Spring — `asak-backend-review`

```text
백엔드 점검 - [GET /api/admin/orders/active]
Controller → Service → Mapper → XML → DB 순서로 현재 구현 여부와 빠진 파일만 정리해줘.
DTO와 SQL의 필드 매핑도 설명하되 코드는 수정하지 마.
```

### DB — `asak-db`

```text
DB 점검 - [orders / order_item]
테이블, 조회 SQL, DTO 필드가 어떻게 연결되는지와 null·상태값 위험만 설명해줘.
스키마나 데이터를 수정하지 마.
```

### 버그 원인 — `asak-debug` 또는 `diagnosing-bugs`

```text
버그 원인 추적 - [증상]
재현 조건, 확인할 파일과 로그, 원인 후보를 우선순위대로 알려줘.
자동 수정·파일 생성·Git 명령은 하지 마.
```

### 코드 공부용 설명 — `asak-explain`

```text
설명 - [파일 경로]
이 파일을 입력 → 처리 → 출력 흐름으로 초보자용으로 설명해줘.
중요 함수와 상태, 오류가 나기 쉬운 부분, 3줄 요약과 작은 연습문제 1개를 줘.
수정하지 마.
```

### 주문 흐름 — `asak-order-review`

```text
주문 흐름 점검 - [SCR / 기능]
주문 생성부터 상태 변경·완료·취소까지 현재 코드와 정본의 차이만 점검해줘.
화면 상태와 API 상태를 분리해서 설명하고 수정하지 마.
```

### 가격·수량 — `asak-price-review`, `asak-quantity-review`

```text
가격 계산 점검 - [장바구니 / 옵션]
단가, 옵션 추가금, 수량, 합계 필드가 어디서 계산되는지 추적해줘.
서버 재검증이 필요한 값과 경계값 테스트만 제안하고 수정하지 마.
```

```text
수량 제한 점검 - [메뉴 / 옵션]
최소·최대 수량, 품절, 중복 선택, 버튼 Disabled 상태를 확인해줘.
누락된 테스트 항목만 정리하고 수정하지 마.
```

### 테스트/QA — `asak-test-plan`

```text
테스트 및 QA 작성 - [SCR-009]
Default·Loading·Empty·Error·Disabled 상태와 화면 이동을 기준으로 테스트 체크리스트를 작성해줘.
API 성공·실패와 권한 오류도 포함하고 코드 수정은 하지 마.
```

### 오늘 작업/이어서 — `asak-today`, `asak-continue`, `handoff`

```text
오늘 작업 정리 - [오늘 한 작업]
확인됨, 미확인, 팀원이 직접 구현한 범위, AI가 도운 범위, 다음 첫 파일만 짧게 정리해줘.
채팅에만 출력하고 파일을 만들지 마.
```

```text
이전 작업 이어서 - [화면 또는 이슈]
현재 Git 상태와 이전 결정 사항을 먼저 확인하고, 지금 해야 할 첫 확인 파일과 질문만 알려줘.
코드 수정은 하지 마.
```

### 발표 준비 — `asak-presentation`

```text
발표 준비 - [주제]
팀원이 직접 구현한 내용과 AI가 도운 분석·리뷰 범위를 구분해서 3분 발표 흐름을 작성해줘.
과장된 구현 완료 표현은 쓰지 마.
```

## 외부 공학 스킬과 코드 그래프

### 요구사항을 더 꼼꼼히 질문받기 — `grill-with-docs`

```text
grill-with-docs 방식으로 [SCR / 기능] 구현 전에 빠진 요구사항만 질문해줘.
Product Bible, Screen Bible, Figma, 기존 코드를 근거로 하고 코드·문서 파일은 만들거나 수정하지 마.
```

### 관련 파일부터 찾기 — `code-review-graph`

```text
[ASAK-Admin / ASAK-Kiosk / ASAK-back]에서 code-review-graph로 변경 영향 범위를 분석해줘.
먼저 읽어야 할 파일, 호출·의존 관계, 관련 테스트만 알려줘.
정본 문서와 Figma는 별도 근거로 구분하고 수정하지 마.
```

### 작업 넘기기 — `handoff`

```text
handoff 형식으로 이번 작업을 채팅에만 정리해줘.
확인됨, 미확인, 테스트 결과, 다음 담당자가 볼 첫 파일을 300자 안팎으로 작성해.
파일을 만들지 마.
```

## 가장 간단한 추천 흐름

```text
1. 구현 전: 구현 전 공통 문장 + 해당 ASAK 스킬 요청
2. 파일이 많음: code-review-graph 요청
3. 팀원이 직접 구현
4. 오류 발생: 버그 원인 추적 요청
5. 수정 후: 테스트 및 QA 작성 요청
6. 끝: 오늘 작업 정리 또는 handoff 요청
```
