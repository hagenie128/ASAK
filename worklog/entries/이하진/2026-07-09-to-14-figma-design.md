# 2026-07-09 ~ 2026-07-14 Figma 디자인 작업 정리 — 이하진

> 상세 일일 기록: [2026-07-09](../../daily/이하진/2026-07-09.md) · [2026-07-13](../../daily/이하진/2026-07-13.md) · [2026-07-14](../../daily/이하진/2026-07-14.md)

## 1. 작업 범위

ASAK Figma 파일의 고객 키오스크 주문 흐름, 관리자 화면, 공통 컴포넌트, 디자인 시스템, 레퍼런스·생성 에셋, 아카이브 및 백업을 정리·제작했다. 파일 인벤토리상 14개 페이지, Component 노드 832개, Component Set 119개가 확인된다.

날짜가 파일에 명시된 작업은 7/9의 생성 에셋 정리와 7/13의 컴포넌트 통합·아카이브 이동이다. 그 외 화면·컴포넌트 제작은 이 기간의 통합 작업으로 기록하며, 파일에 없는 날짜를 임의로 배정하지 않았다.

### 기본 정보

- 작업 날짜: 2026-07-09 ~ 2026-07-14
- 담당자: 이하진
- 저장소: ASAK / ASAK-front
- 브랜치: 확인하지 않음
- 관련 이슈/PR: -
- 작업 유형: `design` / `docs` / `frontend`

## 2. 작업 목적

- 고객 키오스크와 관리자 서비스의 화면·공통 컴포넌트를 Figma에서 일관된 디자인 시스템으로 정리한다.
- Figma 화면을 React 페이지, 상태, 데이터 계약, 디자인 토큰으로 연결해 구현과 유지보수에 사용할 수 있는 기준을 만든다.

## 3. 직접 구현 영역

### 고객 키오스크 화면 설계

- 기존 SCR 주문 흐름과 리디자인 `k001~k007` 시리즈를 함께 구성했다.
- 홈, 메뉴 리스트, 메뉴 상세, 장바구니, 결제 요약 접힘/펼침, 결제 처리 중, 결제 실패, 타임아웃, 주문 완료 화면을 설계했다.
- 1080px 폭의 세로형 키오스크 기준으로 Header, CategoryTab, 메뉴 카드/상세, 하단 CTA, 결제 수단, 주문 요약, 모달을 조합했다.
- 리디자인 화면에서는 주문 단계, 장바구니 요약, 결제 상태, 오류·타임아웃 같은 예외 상태까지 화면 흐름에 포함했다.

### 공통 컴포넌트 제작

### 장바구니·메뉴 선택

- `CartItem`을 ProductHeader, SelectionRow, IngredientRow, RequestRow, QuantityRow, SummaryRow로 나누어 재사용 구조를 만들었다.
- `CartItem`은 `State=Default/Disabled` Variant를 두고, 옵션 추가/제거/기본 상태를 IngredientRow Variant로 관리했다.
- 레퍼런스 기반 개선안인 `CartItem_v2`를 별도 구성했다. 960px 기준 세로 Auto Layout, Default/Disabled 상태, 48×48px 수량 버튼 터치 영역, 32px 상품명·가격 등 키오스크 가독성 기준을 반영했다.
- MenuCard, CategoryTab, OptionChip, OptionCategory, OrderDetailList, OrderDetailRow, QuantityStepper를 제작해 메뉴 선택과 옵션 흐름을 구성했다.

### 결제·주문 흐름

- PaymentMethodCard의 카드/카카오 및 선택/기본 상태, OrderSummaryInfo의 접힘/펼침 상태, OrderInfoToggle, StepIndicator, ProgressDot, Modal을 구성했다.
- BottomCTA를 `twoCTA`, `singlePrimary`, `cartSummary` 3개 레이아웃 Variant로 제작해 화면별 하단 행동을 재사용할 수 있게 했다.
- 결제 실패·타임아웃 모달과 결제 처리 중 상태를 공통 컴포넌트로 구성했다.

### 관리자 화면 및 컴포넌트

- 관리자 로그인, 주문 현황·주문 관리, 품절 관리·상세, 매출 요약·월별·일별 매출, 설정 화면을 1920×1080 기준으로 설계했다.
- Sidebar, Admin/Nav-Item, Summary-Card, Filter-Tab, Section-Card, Page-Header, Export-Button을 제작했다.
- 주문 관리 화면에 DataTable, 상태 Badge, 검색 입력, 필터 드롭다운, 페이지네이션, 주문 상세 항목·요청사항·합계·액션 버튼을 구성했다.
- 주문·결제·환불 상태를 포함하는 Badge Variant와 주문 상태별 DataTable/Row Variant를 정리했다.

### 디자인 시스템·레퍼런스

- Text Style 31개, Effect Style 7개, Paint Style 2개와 컬러 컨테이너를 확인·정리했다.
- Charcoal + Electric Lime 기반 DS-02 Modern Minimal 방향을 바탕으로 홈 히어로, 카테고리 탭, 메뉴 카드, 옵션 칩의 표현 기준을 구성했다.
- ASAK LOGO 크기 Variant, 12개 조합의 공통 Button Variant, 메뉴 이미지 자산을 정리했다.
- 장바구니·카테고리·컬러 사용 레퍼런스 보드와 생성 비주얼 에셋 11종, 이미지 생성 프롬프트 보드를 관리했다.

### 파일 정리·마이그레이션

- Badge 3세트와 DataTable 관련 중복 세트를 통합하고, 이전 세트는 Archive로 이동했다.
- 미사용 Shared 자산과 이전 PaymentMethodCard, 디자인 탐색용 보드를 분리 보관했다.
- 고객 키오스크 원본과 컴포넌트 교체 전 스냅샷을 백업해 리디자인 전후를 비교·복구할 수 있게 했다.

## 4. 구현 로직 / 적용한 방식

- 키오스크 화면은 1080px 폭의 세로형 기준으로 Header, CategoryTab, 메뉴 카드/상세, 하단 CTA, 결제 수단, 주문 요약, 모달을 조합하는 구조로 구성했다.
- 반복 UI는 Variant와 Property로 상태를 관리했다. 예를 들어 CartItem은 Default/Disabled, BottomCTA는 `twoCTA`·`singlePrimary`·`cartSummary`, PaymentMethodCard는 선택/기본 상태로 분리했다.
- 관리자 화면은 Sidebar, Page Header, Filter, DataTable, Badge 등 공통 단위를 먼저 두고 화면별 조합이 가능하도록 구성했다.
- 디자인 시스템은 Charcoal + Electric Lime 방향의 컬러·텍스트·효과 스타일과 Button·Logo·메뉴 이미지 자산을 공통 기준으로 관리했다.
- 코드 연동 시에는 Figma의 텍스트·Boolean·Instance swap Property를 React props에 대응시키고, 화면별 로딩·빈 목록·오류·품절·타임아웃을 별도 상태로 구현하는 기준을 적용했다.

## 5. AI 도움 영역

- 사용한 AI 도구: Figma MCP
- 어떤 질문/요청을 했는지: Figma 파일의 화면·컴포넌트 구조와 React 구현 후보의 대응 관계 점검
- AI가 도움 준 내용: 화면 및 컴포넌트 매핑 초안, 디자인 시스템·상태 점검 보조
- 그대로 사용한 부분: 파일 구조와 화면·컴포넌트 후보를 확인하는 참고 자료
- 수정해서 사용한 부분: 구현 우선순위, React props·상태·데이터 계약, 예외 상태 정의는 직접 검토·정리

## 6. 발생 이슈

- 이슈 1:
  - 증상: 같은 역할의 Badge, DataTable, MenuCard, PaymentMethodCard 등이 중복되거나 이전 구조로 남아 있었다.
  - 원인: 화면 리디자인과 컴포넌트 확장이 병행되면서 이전 자산과 신규 자산이 함께 존재했다.
  - 해결: 컴포넌트 세트를 통합하고 이전 세트는 Archive로 이동했으며, 고객 키오스크 원본과 교체 전 스냅샷을 백업했다.
- 이슈 2:
  - 증상: Figma 화면만으로는 React 구현에 필요한 데이터, 상태, 예외 처리 범위가 명확하지 않았다.
  - 원인: 디자인 산출물과 실제 페이지·스토어·API의 연결 기준이 분리되어 있었다.
  - 해결: 화면·데이터·상태 요구사항 맵과 React 페이지 후보 매핑을 기록하고, 구현 전 체크리스트를 작성했다.

## 7. 디버깅 기록

- 확인한 로그/에러 메시지: -
- 의심했던 지점: 중복 컴포넌트의 실제 사용처, CartItem/CartItem_v2의 적용 대상, 화면별 예외 상태 누락 여부
- 실제 원인: 리디자인·레거시 구조·아카이브 자산이 혼재했고, 코드 연동 기준이 문서화되기 전이었다.
- 다시 같은 문제가 생기면 먼저 볼 파일/명령어: Figma Component Set과 화면 인스턴스, `requirements-screen-map.md`, `cartStore.js`, `orderStore.js`, `tokens.css`, `docs/design/ASAK_FIGMA_MCP_REVIEW_2026-07-14.md`

## 8. 이번 작업에서 배운 점

- Variant와 Property를 화면 상태·React props의 후보로 미리 나누면 디자인과 구현 사이의 해석 차이를 줄일 수 있다.
- 화면 설계에는 정상 흐름뿐 아니라 로딩, 빈 목록, 오류, 품절, 필수 옵션 오류, 결제 실패, 타임아웃을 함께 정의해야 한다.
- 공통 컴포넌트의 중복을 정리하고 아카이브·백업 기준을 남기면 리디자인 이후에도 변경 이력과 복구 가능성을 유지할 수 있다.

## 9. 개선사항 / TODO

- `CartItem_v2`를 실제 `k004` 장바구니 화면의 menu-list에 반영할지 검수한다.
- CartFooterBar와 BottomCTA의 역할을 최종 결정하고, 중복 구조를 정리한다.
- 기존 `CartItem`과 `CartItem_v2` 중 실제 적용 컴포넌트를 확정한 뒤 라이브러리 명명과 인스턴스 사용처를 정리한다.
- Archive에 남긴 컴포넌트는 화면 인스턴스 의존성이 없는지 확인한 뒤 유지·삭제 범위를 결정한다.

## 10. 검증 내용

- 실행한 명령어: -
- 테스트한 시나리오:
  - 고객 키오스크 주문 흐름과 관리자 주요 화면의 Figma 프레임·컴포넌트 구성 확인
  - CartItem, MenuCard, CategoryTab, OptionCategory, PaymentMethodCard, Badge, DataTable의 Variant/Property 확인
  - ASAK-1·ASAK-2의 중복 자산과 Archive·백업 상태 확인
  - React 페이지·스토어·토큰 파일 후보와 화면·데이터·상태 매핑 확인
- 확인 결과:
  - 키오스크·관리자 화면 및 공통 컴포넌트의 디자인 구조와 코드 연동 우선순위를 정리했다.
  - 실제 Zustand 상태, CSS 토큰, API 연결 및 화면별 예외 상태 구현은 후속 개발 작업으로 남아 있다.

## 11. 포트폴리오용 요약

고객 키오스크의 주문 전 과정을 화면·상태별로 설계하고, 장바구니·결제·관리자 UI를 Variant 기반 공통 컴포넌트로 구조화했다. 이후 화면·데이터·상태 계약과 React 컴포넌트 매핑을 정리하고, 중복 자산을 통합·백업해 디자인 시스템을 실제 구현과 유지보수로 이어질 수 있게 만들었다.

## 12. 첨부하면 좋은 자료

- Figma: [ASAK — Design System & Product UI](https://www.figma.com/design/VXKyzoNdsgM4oN57mrECxb/ASAK-%E2%80%94-Design-System---Product-UI-%E2%80%94-2026-07-14?node-id=2-6)
- Figma: [ASAK](https://www.figma.com/design/o9mxSeovLQPdWNwM4mNySk/ASAK?node-id=395-12975)
- [Figma–React 검토 기록](../../../docs/design/_archive/audits/ASAK_FIGMA_MCP_REVIEW_2026-07-14.md)
- 화면·데이터 요구사항 맵: `ASAK-Kiosk/src/contracts/requirements-screen-map.md`, `ASAK-Admin/src/contracts/requirements-screen-map.md`
