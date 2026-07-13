# 2026-07-09 ~ 2026-07-14 Figma 디자인 작업 정리 — 이하진

> 상세 일일 기록: [2026-07-09](../../daily/이하진/2026-07-09.md) · [2026-07-13](../../daily/이하진/2026-07-13.md) · [2026-07-14](../../daily/이하진/2026-07-14.md)

## 1. 작업 범위

ASAK Figma 파일의 고객 키오스크 주문 흐름, 관리자 화면, 공통 컴포넌트, 디자인 시스템, 레퍼런스·생성 에셋, 아카이브 및 백업을 정리·제작했다. 파일 인벤토리상 14개 페이지, Component 노드 832개, Component Set 119개가 확인된다.

날짜가 파일에 명시된 작업은 7/9의 생성 에셋 정리와 7/13의 컴포넌트 통합·아카이브 이동이다. 그 외 화면·컴포넌트 제작은 이 기간의 통합 작업으로 기록하며, 파일에 없는 날짜를 임의로 배정하지 않았다.

## 2. 고객 키오스크 화면 설계

- 기존 SCR 주문 흐름과 리디자인 `k001~k007` 시리즈를 함께 구성했다.
- 홈, 메뉴 리스트, 메뉴 상세, 장바구니, 결제 요약 접힘/펼침, 결제 처리 중, 결제 실패, 타임아웃, 주문 완료 화면을 설계했다.
- 1080px 폭의 세로형 키오스크 기준으로 Header, CategoryTab, 메뉴 카드/상세, 하단 CTA, 결제 수단, 주문 요약, 모달을 조합했다.
- 리디자인 화면에서는 주문 단계, 장바구니 요약, 결제 상태, 오류·타임아웃 같은 예외 상태까지 화면 흐름에 포함했다.

## 3. 공통 컴포넌트 제작

### 장바구니·메뉴 선택

- `CartItem`을 ProductHeader, SelectionRow, IngredientRow, RequestRow, QuantityRow, SummaryRow로 나누어 재사용 구조를 만들었다.
- `CartItem`은 `State=Default/Disabled` Variant를 두고, 옵션 추가/제거/기본 상태를 IngredientRow Variant로 관리했다.
- 레퍼런스 기반 개선안인 `CartItem_v2`를 별도 구성했다. 960px 기준 세로 Auto Layout, Default/Disabled 상태, 48×48px 수량 버튼 터치 영역, 32px 상품명·가격 등 키오스크 가독성 기준을 반영했다.
- MenuCard, CategoryTab, OptionChip, OptionCategory, OrderDetailList, OrderDetailRow, QuantityStepper를 제작해 메뉴 선택과 옵션 흐름을 구성했다.

### 결제·주문 흐름

- PaymentMethodCard의 카드/카카오 및 선택/기본 상태, OrderSummaryInfo의 접힘/펼침 상태, OrderInfoToggle, StepIndicator, ProgressDot, Modal을 구성했다.
- BottomCTA를 `twoCTA`, `singlePrimary`, `cartSummary` 3개 레이아웃 Variant로 제작해 화면별 하단 행동을 재사용할 수 있게 했다.
- 결제 실패·타임아웃 모달과 결제 처리 중 상태를 공통 컴포넌트로 구성했다.

## 4. 관리자 화면 및 컴포넌트

- 관리자 로그인, 주문 현황·주문 관리, 품절 관리·상세, 매출 요약·월별·일별 매출, 설정 화면을 1920×1080 기준으로 설계했다.
- Sidebar, Admin/Nav-Item, Summary-Card, Filter-Tab, Section-Card, Page-Header, Export-Button을 제작했다.
- 주문 관리 화면에 DataTable, 상태 Badge, 검색 입력, 필터 드롭다운, 페이지네이션, 주문 상세 항목·요청사항·합계·액션 버튼을 구성했다.
- 주문·결제·환불 상태를 포함하는 Badge Variant와 주문 상태별 DataTable/Row Variant를 정리했다.

## 5. 디자인 시스템·레퍼런스

- Text Style 31개, Effect Style 7개, Paint Style 2개와 컬러 컨테이너를 확인·정리했다.
- Charcoal + Electric Lime 기반 DS-02 Modern Minimal 방향을 바탕으로 홈 히어로, 카테고리 탭, 메뉴 카드, 옵션 칩의 표현 기준을 구성했다.
- ASAK LOGO 크기 Variant, 12개 조합의 공통 Button Variant, 메뉴 이미지 자산을 정리했다.
- 장바구니·카테고리·컬러 사용 레퍼런스 보드와 생성 비주얼 에셋 11종, 이미지 생성 프롬프트 보드를 관리했다.

## 6. 파일 정리·마이그레이션

- Badge 3세트와 DataTable 관련 중복 세트를 통합하고, 이전 세트는 Archive로 이동했다.
- 미사용 Shared 자산과 이전 PaymentMethodCard, 디자인 탐색용 보드를 분리 보관했다.
- 고객 키오스크 원본과 컴포넌트 교체 전 스냅샷을 백업해 리디자인 전후를 비교·복구할 수 있게 했다.

## 7. 검수 및 다음 작업

- `CartItem_v2`를 실제 `k004` 장바구니 화면의 menu-list에 반영할지 검수한다.
- CartFooterBar와 BottomCTA의 역할을 최종 결정하고, 중복 구조를 정리한다.
- 기존 `CartItem`과 `CartItem_v2` 중 실제 적용 컴포넌트를 확정한 뒤 라이브러리 명명과 인스턴스 사용처를 정리한다.
- Archive에 남긴 컴포넌트는 화면 인스턴스 의존성이 없는지 확인한 뒤 유지·삭제 범위를 결정한다.

## 8. 코드 연동 및 구현 준비

- 요구사항·화면·데이터 맵을 기준으로 Figma `k001~k007`과 React의 `HomePage`, `MenuListPage`, `MenuDetailPage`, `CartPage`, `PaymentPage`, `OrderCompletePage`를 대응시켰다.
- 관리자 `A-001~A-007`도 로그인, 주문 목록/상세, 품절 관리, 메뉴 관리, 결제수단, 매출 요약 화면으로 구분해 구현 후보를 정리했다.
- 장바구니에는 cart items, 옵션, 제외 재료, 수량, 합계가 필요하고 결제에는 orderId, 결제수단, 금액, 오류 코드가 필요함을 데이터 계약으로 확정했다.
- `cartStore.js`, `orderStore.js`, `tokens.css`는 현재 구현 전 자리표시자이므로, 디자인 작업과 별개로 실제 Zustand 상태와 CSS 변수 구현이 필요한 상태임을 기록했다.
- Button, MenuCard, CategoryTab, CartItem, OptionCategory, PaymentMethodCard, Badge, DataTable을 Code Connect/React 연동 우선 컴포넌트로 정했다. Figma의 텍스트·Boolean·Instance swap Property는 향후 React props에 대응시킨다.
- 화면별로 로딩, 빈 목록, 오류, 품절, 필수 옵션 오류, 결제 실패, 타임아웃 등 예외 상태를 구현 범위에 포함했다.

## 9. 포트폴리오 요약

고객 키오스크의 주문 전 과정을 화면·상태별로 설계하고, 장바구니·결제·관리자 UI를 Variant 기반 공통 컴포넌트로 구조화했다. 이후 화면·데이터·상태 계약과 React 컴포넌트 매핑을 정리하고, 중복 자산을 통합·백업해 디자인 시스템을 실제 구현과 유지보수로 이어질 수 있게 만들었다.
