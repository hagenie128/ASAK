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

- Cursor가 mock README 필드 계약과 Figma SCR 주석을 대조하며 hook·페이지 연결 초안을 보조했다.

## 6. 발생 이슈

- dev 서버에서 `SoldOutManagePage` onClick 핸들러 누락으로 JSX parse error가 발생 → 핸들러 연결로 수정.
- 필터·실패 fixture·결제수단/매출 화면 연결은 후속 작업으로 남김.

## 7. 디버깅 기록

- Vite HMR 오류: `onClick={}` 빈 expression → `handleToggleAll` 등 핸들러 연결 후 해소.

## 8. 이번 작업에서 배운 점

- draft baseline을 state로 두어야 저장 후 dirtyCount가 즉시 0으로 재계산된다 (useRef만 쓰면 리렌더가 없음).

## 9. 개선사항 / TODO

- WBS2-040 결제수단, WBS2-034~043 대시보드/매출 getter 연결.
- Admin #1 TC-A01~A06 체크리스트 실행.
- 저장 실패·롤백 fixture 추가.

## 10. 검증 내용

- 실행: `npm run dev` (ASAK-Admin)
- 확인: 주문 목록 pagination, 상세 패널, 환불 confirm/toast; 품절 이동·저장·dirtyCount (수동 진행 중)

## 11. 포트폴리오용 요약

- Admin 운영 화면을 mock repository + hook 패턴으로 연결해 정적 UI 다음 단계인 상태·데이터 바인딩을 시작했다.

## 12. 첨부하면 좋은 자료

- [Admin #1](https://github.com/hagenie128/ASAK_Admin/issues/1)
- `ASAK-Admin/IMPLEMENTATION_PLAN.md` §1 스프린트 P0
- `ASAK-Admin/public/mocks/README.md`
