# 2026-07-21 Admin mock 페이지 바인딩

> **일일:** [2026-07-21](../../daily/이하진/2026-07-21.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-07-21
- 담당자: 이하진
- 저장소: ASAK-Admin
- 브랜치: `main` (로컬 작업 중, 미커밋)
- 관련 이슈/PR: [Admin #1](https://github.com/hagenie128/ASAK_Admin/issues/1)
- 작업 유형: `feature` / `refactor`

## 2. 작업 목적

- 7/20에 고정한 mock 상태 연결 스프린트의 P0 항목(주문 목록·품절 draft 저장)을 Admin 페이지에 실제로 연결한다.

## 3. 직접 구현 영역

- `useOrdersQuery` + `OrderManagementPreview`: mock 주문 목록·상세·환불/영수증 stub.
- `useSoldOutDraft` + `SoldOutManagePage`: catalog 로드·양방향 이동·저장·dirtyCount.
- `usePaymentMethodDraft` + `PaymentMethodPage`: 결제수단 토글·저장·loading/save bar.
- `usePagination` / `AdminPagination`: 주문·품절 목록 공통 페이징.
- `adminMockRepository`: `refundAdminOrder`, `printAdminOrderReceipt`, `saveSoldOutCatalog` stub.
- `orderLabels`, `currency`, `date`, `confirm`, `toast` 유틸 정리.

## 4. 구현 로직 / 적용한 방식

```text
Page → hooks (useOrdersQuery / useSoldOutDraft / usePagination)
     → api/* 또는 mocks/adminMockRepository
```

- Page에서 JSON을 직접 import하지 않고 repository 경계를 유지한다.
- 품절은 mock에서 읽은 뒤 화면 draft로 복사하고, 저장 시에만 `saveSoldOutCatalog`로 반영한다.
- 주문 환불은 `paymentStatus === PAID`일 때만 허용하고 envelope success/failure를 toast로 표시한다.

## 5. AI 도움 영역

- 이번 기록에서는 "AI가 해줬다" 수준이 아니라, **내가 무엇을 요청했고 무엇을 다시 고치게 했는지**까지 남긴다.
- 주문 관리:
  - 첫 요청: `OrderManagementPreview`를 mock repository 경계 안으로 옮기고 JSON 직접 import를 없애는 연결 초안을 보라고 시켰다.
  - 1차 초안 문제: 목록은 보였지만 page 전환 시 상세 패널 초기화, 표시용 라벨/포맷 분리, 액션 성공/실패 흐름 설명이 약했다.
  - 수정 지시: `getAdminOrders`는 전체 목록만 주고, `useOrdersQuery`는 상태만 들고, slice는 `usePagination`에 맡기도록 역할을 다시 쪼개라고 했다.
  - 추가 피드백: 환불/영수증 버튼은 "보이기만 하는 UI"가 아니라 `adminOrderApi` stub의 조건 분기와 toast 메시지까지 이어지게 하라고 요구했다.
- 품절 관리:
  - 첫 요청: 좌우 이동형 품절 화면을 mock catalog 기준 draft 패턴으로 재구성해 보라고 시켰다.
  - 1차 초안 문제: selected 상태와 saved 상태가 섞여 dirtyCount 설명이 불명확했고, 저장 후 기준선이 바로 갱신되지 않는 구조였다.
  - 수정 지시: `available`, `soldOut`, `selectedAvailable`, `selectedSoldOut`, `baselineSoldOutKeys`를 분리해서 "지금 선택", "현재 draft", "저장된 기준"이 코드에서 읽히게 다시 작성하라고 했다.
  - 디버깅 피드백: dev 서버에서 `onClick={}` JSX parse error가 나왔을 때, 단순 문법 수정이 아니라 어떤 핸들러가 빠졌는지까지 추적해서 다시 설명 가능한 형태로 고치게 했다.
- 결제수단:
  - 첫 요청: 품절 draft 패턴을 그대로 복사하지 말고, 토글 중심 설정 화면에 맞게 더 가볍게 적용하라고 했다.
  - 1차 초안 문제: 로딩과 저장은 있었지만 어떤 변경이 저장 대상인지 즉시 읽기 어렵고, save bar 조건이 흐릿했다.
  - 수정 지시: `getPaymentMethods` 조회, draft 변경 감지, `AdminSaveBar` 노출 기준을 분리하고 "사용자 기준에서 변경 사항이 보이는가"를 중심으로 다시 정리하라고 했다.
- 공통화 판단:
  - Cursor가 반복 코드를 광범위하게 후보로 제안했지만 그대로 받지 않았다.
  - `usePagination`, `currency`, `date`, `confirm`, `toast`처럼 **여러 화면에서 재사용 가치가 분명한 것만** 남기고, 페이지 문맥에 강하게 묶인 로직은 각 화면 안에 두도록 정리했다.
- 정리 기준:
  - AI 초안은 빠른 탐색용으로 쓰고, 최종 반영은 "역할이 분리되어 설명 가능한가", "mock 계약을 어기지 않는가", "화면에서 검증 가능한가" 기준으로 직접 걸렀다.

## 6. 발생 이슈

- dev 서버에서 `SoldOutManagePage` onClick 핸들러 누락으로 JSX parse error가 발생 → 핸들러 연결로 수정.
- 필터·실패 fixture·결제수단/매출 화면 연결은 후속 작업으로 남김.

## 7. 디버깅 기록

- Vite HMR 오류: `onClick={}` 빈 expression → `handleToggleAll` 등 핸들러 연결 후 해소.
- AI가 준 초안에서 상태 책임이 섞여 있던 부분은 바로 반영하지 않고, dev 서버에서 실제로 깨지는 지점과 화면 동작을 먼저 본 뒤 구조를 다시 나눴다.

## 8. 이번 작업에서 배운 점

- draft baseline을 state로 두어야 저장 후 dirtyCount가 즉시 0으로 재계산된다 (useRef만 쓰면 리렌더가 없음).
- AI를 많이 쓸수록 "무엇을 시켰는지"보다 "무엇이 마음에 안 들어서 어떻게 다시 시켰는지"를 남겨야 다음 작업에서 같은 시행착오를 줄일 수 있다.

## 9. 개선사항 / TODO

- WBS2-040 결제수단, WBS2-034~043 대시보드/매출 getter 연결.
- Admin #1 TC-A01~A06 체크리스트 실행.
- 저장 실패·롤백 fixture 추가.

## 9-1. 집에서 이어서 할 때 메모

- 오늘 기준 Admin 쪽 1차 바인딩은 주문 목록/상세, 품절 draft 저장, 결제수단 토글·저장, 공통 pagination 유틸까지 정리했다.
- 다음 세션에서는 이 entry만 보지 말고 **프로젝트 전체 기준**으로 상태를 다시 잡아야 한다.
  - Kiosk: Home → Cart mock 동작, Payment / Complete / Error / Timeout 미연결
  - Admin: 7/21 진척이 공용 문서에 아직 충분히 반영되지 않았을 수 있음
  - Backend: `GET /api/health` 외 business API evidence 없음
- 이번 세션에서 의도적으로 미룬 범위:
  - 매출 3화면 getter 연결(WBS2-041~043)
  - Admin #1 TC-A01~A06 전체 회귀 점검
- 집에서 먼저 확인할 문서:
  - `ASAK/docs/planning/current-implementation-map-2026-07-16.md`
  - `ASAK/docs/wiki/current-status-baseline.md`
  - `ASAK/docs/wiki/wbs-status-notes.md`
  - `ASAK/docs/wiki/wbs-v2-2026-07-16.md`
- DevCopilot은 7/20 기준 동기화 기록은 남아 있지만, 7/21 진척 반영 여부는 이번 세션에서 원격 확인을 끝내지 못했다. 토큰 URL 직접 호출은 차단/타임아웃 이슈가 있었다.

## 10. 검증 내용

- 실행: `npm run dev` (ASAK-Admin)
- 확인: 주문 목록 pagination, 상세 패널, 환불 confirm/toast; 품절 이동·저장·dirtyCount (수동 진행 중)

## 11. 포트폴리오용 요약

- Admin 운영 화면을 mock repository + hook 패턴으로 연결해 정적 UI 다음 단계인 상태·데이터 바인딩을 시작했다.

## 12. 첨부하면 좋은 자료

- [Admin #1](https://github.com/hagenie128/ASAK_Admin/issues/1)
- `ASAK-Admin/IMPLEMENTATION_PLAN.md` §1 스프린트 P0
- `ASAK-Admin/public/mocks/README.md`
