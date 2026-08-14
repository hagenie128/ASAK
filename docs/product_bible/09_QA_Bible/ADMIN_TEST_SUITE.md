# Admin Test Suite

> Status: `Canonical`
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `ADMIN_SMOKE_TEST.md`
- `DASHBOARD_TESTS.md`
- `KITCHEN_TTS_TESTS.md`
- `MENU_MANAGEMENT_TESTS.md`
- `SALES_TESTS.md`
- `SOLD_OUT_TESTS.md`

---

## 원문: `ADMIN_SMOKE_TEST.md`

### Admin Smoke Test

- Login 표시
- Login 성공 후 Dashboard
- Dashboard KPI 표시
- Live Order Board 진입
- Order Management 진입
- Sold-out 진입
- Menu Management 진입
- Payment Settings 진입
- Sales 진입
- Console fatal error 없음

---

## 원문: `DASHBOARD_TESTS.md`

### Dashboard Tests

#### DASH-001 — KPI

- 순매출
- 주문 수
- 평균 객단가
- 진행 중 주문

Expected:
- 계산 기준 일치

#### DASH-002 — Empty

Expected:
- 0값
- 정상 Empty copy

#### DASH-003 — Partial Error

Expected:
- 실패 widget만 Error
- 전체 Dashboard 유지

#### DASH-004 — Refresh

Expected:
- duplicate fetch 없음
- lastUpdatedAt 갱신

#### DASH-005 — Navigation

Expected:
- Home active
- 주문관리와 역할 분리

---

## 원문: `KITCHEN_TTS_TESTS.md`

### Kitchen and TTS Tests

#### KIT-001 — 상태 전이

```text
RECEIVED → PREPARING → COMPLETED
```

#### KIT-002 — 잘못된 전이

Expected:
- 서버 차단
- 사용자 안내

#### KIT-003 — 완료 중복 클릭

Expected:
- 1회 처리
- TTS 1회

#### KIT-004 — Polling stale response

Expected:
- 최신 updatedAt 우선

#### KIT-005 — 네트워크 실패

Expected:
- 기존 card 유지
- Error Toast

#### TTS-001 — 완료 성공

Expected:
- orderNo 발화

#### TTS-002 — 같은 주문 10초 이내

Expected:
- 중복 차단

#### TTS-003 — 음소거

Expected:
- 주문 완료 정상
- 발화 없음

#### TTS-004 — 브라우저 미지원

Expected:
- crash 없음

#### TTS-005 — 연속 완료

Expected:
- queue 순서 유지

---

## 원문: `MENU_MANAGEMENT_TESTS.md`

### Menu Management Tests

#### MENU-ADM-001 — 신규 등록

- 필수값
- 관계 저장
- 성공 Toast

#### MENU-ADM-002 — 수정

- original/draft 분리
- dirty fields
- SaveBar

#### MENU-ADM-003 — 필수 옵션 그룹 오류

Expected:
- min/max validation

#### MENU-ADM-004 — 추천 옵션 비활성

Expected:
- 저장 차단 또는 추천 해제

#### MENU-ADM-005 — 재료 중복

Expected:
- 정책에 따라 차단

#### MENU-ADM-006 — 이미지 업로드 실패

Expected:
- draft 유지

#### MENU-ADM-007 — 삭제

Expected:
- ConfirmDialog
- soft delete (`menu.deleted_at` 설정, 행 물리 삭제 없음)
- 과거 주문 보존 (`order_item.menu_id` FK 유지)
- 삭제 후 관리/키오스크 목록·상세에서 미노출

상태: Backend soft delete **구현됨** (2026-08-11). Admin UI ConfirmDialog·E2E는 **미검증**.

#### MENU-ADM-008 — Modal

Expected:
- 검색
- preload
- cancel
- add

---

## 원문: `SALES_TESTS.md`

### Sales Tests

#### 공식 정의

```text
고객 수 = 결제 승인 건수
평균 객단가 = 총매출 / 고객 수
```

#### SALES-001 — KPI 정합성

- 총매출
- 고객 수
- 평균 객단가

#### SALES-002 — 차트 합계

Expected:
- 일별/월별 합계 = KPI

#### SALES-003 — 시간대별 고객 수

Expected:
- 합계 = 전체 고객 수

#### SALES-004 — 결제수단 비율

Expected:
- 합계 100%

#### SALES-005 — 주문유형 비율

Expected:
- 합계 100%

#### SALES-006 — 비교율

Expected:
- 표시값과 계산값 일치

#### SALES-007 — previous 0

Expected:
- 비교 데이터 없음

#### SALES-008 — Mock Data

Expected:
- 날짜 중복 없음
- KPI·표·차트 모두 일치

---

## 원문: `SOLD_OUT_TESTS.md`

### Sold-out Tests

#### SOLD-001 — Menu direct sold-out

Expected:
- Kiosk card disabled

#### SOLD-002 — CORE ingredient

Expected:
- 연결 메뉴 derived sold-out

#### SOLD-003 — BASE 일부 품절

Expected:
- 대체 base가 있으면 메뉴 유지

#### SOLD-004 — BASE 전체 품절

Expected:
- 메뉴 품절

#### SOLD-005 — STANDARD ingredient

Expected:
- 제거 가능 시 메뉴 유지 + 안내

#### SOLD-006 — OPTIONAL

Expected:
- 해당 옵션만 disabled

#### SOLD-007 — Required group 전체 품절

Expected:
- 메뉴 품절

#### SOLD-008 — 저장 취소

Expected:
- dirty draft 폐기

#### SOLD-009 — 일부 저장 실패

Expected:
- 전체 rollback

#### SOLD-010 — 해제

Expected:
- derived 원인 해소 시 복구
- direct sold-out이면 유지
