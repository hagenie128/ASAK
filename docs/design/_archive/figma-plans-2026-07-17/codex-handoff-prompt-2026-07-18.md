> Status: **Historical** (2026-07-20) · 1회성 핸드오프  
> → **정본:** [figma-change-register-2026-07-18.md](../figma-change-register-2026-07-18.md)

# 코덱스 인수인계 프롬프트 (복붙용)

ASAK 키오스크·관리자 주문 시스템의 Figma 디자인을 React 프론트엔드 코드로 반영하는 작업이야.

## 먼저 읽어야 할 문서 (프로젝트 안에 있음)
1. `ASAK/docs/design/ASAK_FIGMA_DESIGN_FEEDBACK_COMPONENT_SCREEN_2026-07-17.md` — 컴포넌트·화면 전수 실측 QA. 정확한 px/hex/line-height 값, 색상 토큰, 키오스크(터치·세로1080)/관리자(웹·태블릿·가로1920) 기준 차이가 다 정리돼 있음.
2. `ASAK/docs/design/figma-precise-fix-checklist-2026-07-18.md` — 실제로 Figma에서 뭘 고쳤고 뭘 안 고쳤는지 최종 상태. 특히 맨 아래 "D. 나(Claude)에게 남긴 것" 섹션에 뭐가 완료됐고 뭐가 보류됐는지 정확히 적혀 있음.
3. `ASAK/docs/design/kiosk-design-system.md` 등 기존 프로젝트 컨벤션 문서 — **작업 시작 전에 반드시 먼저 읽고 기존 패턴을 따를 것.** 새로 임의로 컨벤션 만들지 말 것.
4. `CLAUDE.md` — 프로젝트 공통 지침(React+JavaScript, Spring Boot+JPA, 네이밍 규칙, `priceCalculation.js`/`quantityLimits.js`가 가격·수량의 단일 기준이라는 것 등).

## 반드시 지킬 원칙
1. **실데이터·API 연동은 하지 마.** JSON 로딩과 실제 연동은 내가 직접 할 거야. 화면 구현에는 **최소한의 플레이스홀더 데이터**만 써.
2. **Figma 텍스트를 그대로 코드에 복붙하지 마.** 특히 `Admin/StatusBadge`처럼 "Figma 안에서는 12개 Role 라벨이 하드코딩돼 있지만, 실제로는 role→label 매핑 테이블을 프론트엔드 코드에서 따로 만들어야 하는" 함정이 있어 — 위 QA 문서에 이런 함정들이 상세히 적혀 있으니 그대로 옮기기 전에 꼭 확인해.
3. **가격 계산은 `priceCalculation.js`, 수량 제한은 `quantityLimits.js`가 단일 기준**이야. 새로 계산 로직 만들지 말고 이거 기준으로 붙여.
4. **Figma에는 아무것도 다시 쓰지 마.** 이건 순수 코드 작업이야.

## 작업 시작 전에 나한테 먼저 물어봐야 하는 것
- Props/필드명 계약 (`isRecommended`, `categoryId`, `extraPrice`, `totalPrice` 등 실제 JSON 필드명이 뭔지)
- 어느 화면부터 작업할지 순서 (예: 홈 → 메뉴 → 장바구니 → 결제 순으로 갈지)

## 참고
디자인 QA·수정은 Claude(Figma MCP)로 진행했고, 코드 컨벤션은 그동안 코덱스/GPT로 작업해온 것과 이어가는 게 맞아서 이 작업도 너한테 넘기는 거야. Figma 관련 추가 확인이 필요하면 Claude 세션으로 돌아갈 거니까, 코드 작업 중 "디자인이 이상한데?" 싶은 부분이 있으면 임의로 판단하지 말고 나한테 먼저 물어봐줘.
