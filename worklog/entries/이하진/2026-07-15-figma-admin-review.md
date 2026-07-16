# 2026-07-15 Figma 구조·Admin 컴포넌트 적용 검토 — 이하진

> **템플릿:** [03-work-log-template.md](../../../docs/guides/03-work-log-template.md) · **일일:** [2026-07-15.md](../../daily/이하진/2026-07-15.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-07-15
- 담당자: 이하진
- 저장소: ASAK / ASAK-front
- 브랜치: 확인하지 않음
- 관련 이슈/PR: -
- 작업 유형: `docs` / `frontend`

## 2. 작업 목적

- 계속 진행해 온 Figma 파일 구조·페이지·컴포넌트 계층·화면/React 매핑 검토를 이어간다.
- Admin 화면에 실제 연결된 공통 컴포넌트와 상태를 확인해 구현 핸드오프 기준을 확정한다.

## 3. 직접 구현 영역

- `06-B. Screens / Admin (컴포넌트 적용)` 페이지의 관리자 화면 구조와 컴포넌트 인스턴스를 검수했다.
- `SCR-009` 주문 현황, `SCR-010` 주문 상세, `SCR-019` 매출 요약, 메뉴 관리 화면의 상태·필터·테이블·모달 구성을 확인했다.
- `START HERE`·Source Inventory·Foundations·Shared/Kiosk/Admin Components·Screens·Flows·Handoff로 이어지는 전체 파일 구조에서 Admin 화면의 위치를 재확인했다.

## 4. 구현 로직 / 적용한 방식

- 주문 현황은 `Admin/Navbar`, `Admin/OrderCard`, 좌우 이동, 조리 완료 TTS 안내 구조로 확인했다.
- 주문 상세는 `Admin/OrderPageHeader`, `FilterDropdown`, `SearchInput`, `DataTableHeader`, `DataTableRow-Active`, 상세 패널, `Pagination` 조합으로 확인했다.
- 매출 요약은 기간 필터, 순매출·주문 수·고객 수·취소/환불 Summary Card, 일별 매출 테이블 구조로 확인했다.
- 메뉴 관리는 재료 추가 모달, 검색·유형 필터, Checkbox, 판매중·품절·이미 추가됨 상태와 품절 안내로 확인했다.
- React 구현 시 Figma 컴포넌트 인스턴스를 기준으로 화면·데이터·상태 계약을 분리하고, 품절·TTS 알림을 별도 인터랙션으로 정의한다.

## 5. AI 도움 영역

- 사용한 AI 도구: Figma MCP, Codex
- 어떤 질문/요청을 했는지: Figma 파일 구조와 Admin 화면의 컴포넌트·상태·React 구현 매핑을 계속 검토하고 오늘 워크로그에 반영
- AI가 도움 준 내용: 노드 구조, 화면 이름, 인스턴스 연결, 화면별 구성 확인 보조
- 그대로 사용한 부분: SCR 번호, 화면명, 컴포넌트명, 화면 규격 등 Figma에서 확인된 사실
- 수정해서 사용한 부분: 구현 우선순위, 데이터·상태 계약, 후속 TODO는 직접 검토해 정리

## 6. 발생 이슈

- 이슈 1:
  - 증상: Figma 화면 구조만으로 실제 React 데이터·상태 계약이 모두 드러나지 않음.
  - 원인: 디자인 컴포넌트와 애플리케이션 상태·API 연결 기준이 별도이기 때문.
  - 해결: 주문·메뉴·매출별 데이터/상태 계약과 품절·TTS 인터랙션을 후속 구현 항목으로 분리했다.

## 7. 디버깅 기록

- 확인한 로그/에러 메시지: Figma design context는 현재 선택 상태가 없어 사용할 수 없었으나, 노드 metadata로 구조 검토를 완료했다.
- 의심했던 지점: 지정 노드가 Icon이 아닌 Admin 화면 페이지인지, Admin 인스턴스가 실제 화면에 연결됐는지.
- 실제 원인: 최초 링크의 노드와 수정 링크의 노드 범위가 달랐고, 수정 링크 `39:7344`는 Admin 화면 캔버스를 가리켰다.
- 다시 같은 문제가 생기면 먼저 볼 파일/명령어: Figma URL의 `node-id`, `get_metadata`, `START HERE`의 Source Inventory, 화면 인스턴스와 Component Set 연결

## 8. 이번 작업에서 배운 점

- 개별 화면 검수보다 파일 전체 구조와 Source Inventory를 함께 봐야 컴포넌트의 역할과 구현 위치를 정확히 판단할 수 있다.
- Figma 인스턴스 연결 확인과 React 데이터·상태 계약 정의는 별도 검토 단계로 기록해야 한다.

## 9. 개선사항 / TODO

- 관리자 화면별 실제 데이터·상태 모델과 Figma Variant를 대응시킨다.
- 주문 목록/상세의 TTS 알림, 필터·검색·Pagination 인터랙션 계약을 React 구현 항목으로 구체화한다.
- 메뉴 관리의 품절·이미 추가됨 상태를 API 응답과 화면 노출 규칙에 연결한다.

## 10. 검증 내용

- 실행한 명령어: Figma MCP `get_metadata(fileKey, nodeId=39:7344)`
- 테스트한 시나리오:
  - `SCR-009` 주문 현황의 OrderCard·Navbar·TTS 구조 확인
  - `SCR-010` 주문 상세의 필터·검색·테이블·상세 패널 확인
  - `SCR-019` 매출 요약의 필터·Summary Card·일별 매출 테이블 확인
  - 메뉴 관리 모달의 재료 필터·Checkbox·판매 상태 확인
- 확인 결과: Admin 컴포넌트 인스턴스와 화면 구성이 연결되어 있으며, 후속 React 구현에 필요한 매핑 후보와 상태 계약 TODO를 정리했다.

## 11. 포트폴리오용 요약

ASAK Figma 디자인 시스템의 전체 구조를 지속적으로 검토하면서 관리자 주문·매출·메뉴 관리 화면에 적용된 공통 컴포넌트와 상태를 확인하고, React 구현을 위한 화면·데이터·상태 계약으로 연결했다.

## 12. 첨부하면 좋은 자료

- [Figma — ASAK Design System Product UI 0715](https://www.figma.com/design/JSrjOy668zhfkiLplCkreh/ASAK-%E2%80%94-Design-System---Product-UI-0715?node-id=39-7344)
- [Figma–React 검토 기록](../../../docs/archive/design-audits/ASAK_FIGMA_MCP_REVIEW_2026-07-14.md)
- [오늘 일일 워크로그](../../daily/이하진/2026-07-15.md)
