# 2026-08-25 관리자 로그인·결제수단 프론트 연결 — 이하진

> **템플릿:** [03-work-log-template.md](../../../docs/guides/03-work-log-template.md) · **일일:** [2026-08-25.md](../../daily/이하진/2026-08-25.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-08-25
- 담당자: 이하진
- 저장소: ASAK-Admin
- 커밋: `6da1c2d` feat: 관리자 결제수단 및 로그인 API 연결 · merge `5e0ab5b`
- 작업 유형: `feature`

## 2. 작업 목적

- Login·Payment Method 화면을 mock 대신 백엔드 API에 연결한다.
- 세션은 JWT 없이 기존 `loggedIn` 플래그 경계를 유지한다.

## 3. 직접 구현 영역

- `adminApi.js`, `LoginPage.jsx`, `AdminStartGate.jsx`, `adminSession.js` / store
- `paymentMethodsApi.js`, `usePaymentMethodDraft.js`, `AdminPaymentMethodRow.jsx`, `PaymentMethodPage.jsx`
- `apiClient.js`·상수·glyph·types 정리 (15 files)

## 4. 구현 로직 / 적용한 방식

```text
LoginPage → adminApi.login(storeNumber)
  → POST /api/admin/login
  → approved면 loginAdmin()/loggedIn

PaymentMethodPage → usePaymentMethodDraft
  → listPaymentMethods / patchPaymentMethod
  → active·sortNo를 행 단위 반영
```

## 5. AI 도움 영역

- 원 구현 시점 AI 범위 미특정. entry는 Cursor 퇴근 backfill.

## 6. 발생 이슈

- 익일 진단 문서(`admin-login-error-diagnosis.md`, `payment-methods-frontend-*`)에 정리: 서버 미기동, body 계약 불일치 이력, `apiClient` data-only 반환과 success 판정 차이, mock 필드명(`isActive`/`sortOrder`) vs DTO(`active`/`sortNo`).

## 7. 개선사항 / TODO

- 백엔드 기동 상태에서 로그인·토글·정렬 저장 E2E.
- Figma Frame ID(`39:8203` vs `134:11493`) 정합 확인.

## 8. 이번 작업에서 배운 점

- mock 필드명을 화면 전체에 퍼뜨리면 API DTO 연결 비용이 adapter 한 곳이 아니라 행·훅·페이지로 번진다.

## 9. 포트폴리오용 요약

관리자 로그인·결제수단 화면을 실제 Admin API에 연결하고, JWT 없는 승인 플래그 세션 경계를 유지했다.

## 10. 참고 자료

- `6da1c2d`, `5e0ab5b`
- `ASAK-Admin/docs/ai-reports/2026-08-25/*` (익일 커밋 `bc852c3`)
- [2026-08-25 daily](../../daily/이하진/2026-08-25.md)
