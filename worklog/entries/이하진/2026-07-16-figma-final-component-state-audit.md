# 2026-07-16 Figma Final 컴포넌트·상태 정책 감사 — 이하진

> **템플릿:** [03-work-log-template.md](../../../docs/guides/03-work-log-template.md) · **일일:** [2026-07-16.md](../../daily/이하진/2026-07-16.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-07-16
- 담당자: 이하진
- 저장소: ASAK / Figma
- 브랜치: `docs/notion-web-audit-v1` (워크로그 작성 시점 확인)
- 관련 이슈/PR: PR #5 병합 완료, PR #6 Cleanup Draft, PR #7 Notion Audit Draft, PR #8 Frontend 80% Plan Draft
- 작업 유형: `design` / `docs`

## 2. 작업 목적

- Figma C 버전을 구현 정본으로 유지하면서 Kiosk/Admin 컴포넌트·Variant·인스턴스·상태가 실제 React 구현 정책과 맞는지 확인한다.
- 장바구니 수량, 품절, 결제 차단, 결제수단 브랜드 색상처럼 구현 오류로 이어질 수 있는 정책 충돌을 화면·컴포넌트 수준에서 닫는다.

## 3. 직접 구현 영역

- `03-C. Components / Kiosk`, `04-C. Components / Admin`의 Implementation Final 복제·감사 범위를 정하고, 원본 페이지를 수정하지 않는 기준을 유지했다.
- `PaymentMethodCard`, `QuantityStepper`, `BottomCTA`, `MenuCard`, `CartItemCard`, `OrderSummaryInfo`, `OrderDetailRow` 및 Admin 컴포넌트의 Variant·중복·정본 후보를 검토했다.
- Cart 정책을 다음처럼 확정했다: 수량 1은 minus disabled, 수량 0 금지, 동일 `menuId` 최대 9개, Cart 전체 최대 30개, 30개 초과 시도 때만 직원 문의 안내, 수정은 `cartItemId` 기준 `updateCartItem`, 품절 항목은 자동 삭제하지 않고 수정/삭제를 제공하며 해결 전 결제를 차단한다.
- 품절 원인을 메뉴/핵심 재료, 일반 옵션, Base 일부 품절로 나누고 Cart의 `Item Sold-out`, `Edit Required`, `Checkout Blocked` 상태별 Action 정책을 정리했다.

## 4. 구현 로직 / 적용한 방식

- C 버전은 B 버전의 시각 정본을 되돌리는 대상이 아니라, Component·Variant·상태·Prototype을 구현 가능하게 확장한 정본으로 정의했다.
- 공통 UI는 Shared로 올릴 수 있는지, 화면 전용 UI는 역할이 충분히 다른지를 먼저 비교했다. 예: `StatusBadge`와 `Badge`는 구조·색상·크기·Variant가 같은 중복 후보이고, `Toast`와 `AddResultToast`는 맥락은 다르지만 통합 가능성을 남겼다.
- 결제수단 로고의 브랜드 색상은 선택/성공/오류 상태색과 분리했다. 카드 선택은 Border·Background로, 로고 식별은 공식 브랜드 색상으로 유지하도록 규칙을 세웠다.
- Figma Agent에는 전체 화면을 한 번에 수정시키지 않고, 대상 Page/Frame/Node, 유지·변경·금지 항목, 정량 기준, 완료 보고 형식을 포함한 배치형 지시를 사용했다.

## 5. AI 도움 영역

- 사용한 AI 도구: ChatGPT, Codex, Figma MCP/Figma Agent
- 어떤 질문/요청을 했는지: 기존 원본을 보존한 Final 페이지 복제, Component Set/Variant/Property/인스턴스 감사, Cart 품절·수량 정책 보정, 결제 브랜드 토큰 분리, 화면별 수정 지시와 PASS/FAIL 검수표 작성을 요청했다.
- AI가 도움 준 내용: Figma 노드·Variant·속성·인스턴스 수를 구조화하고, 중복·오타·Legacy 혼용 후보와 수정 후 보고 항목을 표로 정리했다. Cart 3개 Frame의 CTA 정책, 수동 opacity 제거, `minusDisabled` Boolean 적용 등 검수 기준도 제안했다.
- 그대로 사용한 부분: Figma Agent가 반환한 Component Set/Variant ID, 속성명, 인스턴스 수, 수동 Frame·Detach 유무처럼 도구로 확인한 사실과 화면 구조.
- 수정해서 사용한 부분: 어떤 컴포넌트를 정본으로 삼을지, 품절 원인별 수정/삭제 Action, 30개 제한의 안내 문구 노출 시점, 브랜드 색상과 상태 색상 분리, 배치 우선순위는 이하진이 프로젝트 정책과 사용성을 기준으로 판단했다.
- AI 사용 경계: AI가 소스코드를 구현하거나 임의로 전체 Figma를 수정하게 하지 않았다. Figma Agent 변경은 대상 노드·금지 범위·완료 보고를 지정한 뒤 결과를 검수하는 방식으로 제한했다.

## 6. 발생 이슈

- 이슈 1: Kiosk 컴포넌트의 Variant·정본 구조가 불완전하거나 중복됨.
  - 증상: `PaymentMethodCard`의 카카오 선택 Variant 중복, `QuantityStepper`의 의미 없는 `border_bottom` 속성, `OrderDetailRow`의 `Property 1=Error` 불일치가 확인됨.
  - 원인: 초기 컴포넌트와 Implementation Final 컴포넌트가 공존하고, Variant 명명·상태 설계가 단계적으로 확장됐기 때문.
  - 해결: 즉시 대규모 정리하지 않고 Final Master 우선·Legacy→Final Instance Swap·누락 Master 승격·교차 컴포넌트 분리를 배치 작업으로 나눴다.
- 이슈 2: 품절 Cart에서 수정/삭제 Action과 결제 차단이 일관되지 않음.
  - 증상: 일부 품절 Frame의 BottomCTA가 default여서 결제 가능처럼 보일 수 있었고, 메뉴·핵심 재료 품절에도 수정 유도 문구가 보일 위험이 있었다.
  - 원인: 품절 원인별 화면 상태는 존재했지만 결제 CTA와 Action 정책이 같은 규칙으로 연결되지 않았다.
  - 해결: 모든 unavailable Cart 상태의 checkout CTA는 disabled로 통일하고, 일반 옵션/Base 품절에는 수정·삭제, 메뉴/핵심 재료 품절에는 삭제 중심 Action을 적용하도록 규칙을 고정했다.

## 7. 디버깅 기록

- 확인한 로그/에러 메시지: Component Property를 읽을 수 없게 하는 중복 Variant와 속성명 불일치, Clone 시 단독 Component가 Instance로 복제되는 현상을 확인했다.
- 의심했던 지점: `StatusBadge`와 `Badge`가 역할이 다른지, `Toast`와 `AddResultToast`가 중복인지, Cart 품절 상태가 CTA·버튼 속성과 실제로 일치하는지 점검했다.
- 실제 원인: 디자인 페이지의 단독 Component/Instance 혼재와 Legacy/Final 병행, 그리고 정책 문서와 화면 Variant의 연결 부족이었다.
- 다시 같은 문제가 생기면 먼저 볼 파일/명령어: Figma의 Component Set/Variant Property, 05-C·06-C 인스턴스 사용 위치, `docs/implementation_guide/09-figma-state-checklist.md`, Cart·Sold-out Product Bible, 해당 Frame의 BottomCTA Set/Variant.

## 8. 이번 작업에서 배운 점

- Figma의 보기 좋은 기본 화면만으로는 구현 준비가 끝나지 않는다. Loading·Empty·Error·Disabled·품절·Processing 같은 상태를 Component Property와 Action 정책까지 연결해야 한다.
- AI를 디자인 실행 도구로 쓸 때는 한 번에 전체 수정시키기보다, Frame/Node ID와 변경 금지 범위를 주고 결과를 수치로 보고받아야 원본·정본 혼선을 줄일 수 있다.
- 브랜드 색상, 제품의 상태색, 선택 상태색은 모두 역할이 달라 한 토큰으로 합치면 의미와 접근성이 동시에 무너질 수 있다.

## 9. 개선사항 / TODO

- `PaymentMethodCard` 중복 Variant, `OrderDetailRow` 속성명, `Admin/MenuCard`의 `seleted` 오타를 Final Master 정리 배치에서 수정한다.
- `StatusBadge`/`Badge`, `ConfirmDialog`, `ErrorState`, Toast 계열의 Shared 통합 여부를 확정한다.
- `DatePicker`/`DateRangePicker`를 Frame 상태에서 컴포넌트화할지 결정한다.
- `SoldOutBadge`의 Default/High Contrast 대비 문제는 `Semantic/Status/Error` 값 또는 전용 On-Status 토큰 설계와 함께 재검토한다.
- 05-C/06-C의 실제 Prototype 연결과 각 C Frame 상태는 화면별로 재확인한다.

## 10. 검증 내용

- 실행한 명령어: Figma MCP/Figma Agent 기반 Component·Variant·인스턴스 감사 및 ChatGPT 공유 대화의 작업 보고 재검토.
- 테스트한 시나리오:
  - `CartItemCard`의 quantity=1에서 minus disabled, quantity>1에서 감소 가능 여부.
  - 일반 옵션/Base 품절과 메뉴/핵심 재료 품절에서 수정·삭제·결제 차단 Action 차이.
  - `PaymentMethodCard`의 selected/disabled 상태와 로고 브랜드 색상 분리.
  - Kiosk/Admin Implementation Final 복제 시 원본 페이지 무변경, Instance Detach 금지, 다른 페이지 무변경 보고 여부.
- 확인 결과: Figma 구조와 정책 충돌 후보를 기록했고, 후속 수정은 범위가 정해진 배치로 진행할 수 있는 상태가 됐다. 본 워크로그 작성 시점에는 전체 Figma 파일을 다시 변경하거나 전수 재감사하지 않았다.

## 11. 포트폴리오용 요약

ASAK Figma C 버전을 실제 구현 정본으로 관리하기 위해 Kiosk/Admin 컴포넌트의 Variant·중복·상태를 감사하고, 장바구니 수량 제한·품절 복구·결제 차단·결제 브랜드 색상 정책을 화면과 컴포넌트 기준으로 정리했다. AI는 노드 구조 확인과 작업지시서 초안에 활용했고, 정책 판단과 최종 검수는 직접 수행했다.

## 12. 첨부하면 좋은 자료

- [2026-07-15 Figma Admin 검토 기록](2026-07-15-figma-admin-review.md)
- [Figma 상태 체크리스트](../../../docs/implementation_guide/09-figma-state-checklist.md)
- [기능 구현 매트릭스](../../../docs/implementation_guide/08-feature-implementation-matrix.md)
- ChatGPT 공유 대화: `피그마 MCP 활용법`, `ASAK 프로젝트 검토` (워크로그 작성 근거)
