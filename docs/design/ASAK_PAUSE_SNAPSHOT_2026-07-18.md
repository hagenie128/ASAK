# ASAK 휴식 전 스냅샷 (2026-07-18)

> **디자인 작업 일시 중지.** 이 문서는 “지금 어디쯤인지”만 적어 둔다. 급하게 고치지 않는다.

## 저장소 역할

| 폴더 | 하는 일 | 지금 상태 (한 줄) |
|------|---------|-------------------|
| `ASAK/` | 중앙 문서·Product Bible | 정본 문서 허브 |
| `ASAK-Kiosk/` | 키오스크 React | 홈·메뉴 목록 위주, 카트/결제/완료는 뼈대 |
| `ASAK-Admin/` | 관리자 React | placeholder 위주, 정본 구현 위치 |
| `ASAK-back/` | Spring Boot | health만 있음, 업무 API 미구현 |

## 볼 문서 (우선순위)

1. [`implementation_guide/00_START_HERE.md`](../implementation_guide/00_START_HERE.md) — 기능 고르고 블록만
2. [`planning/CURRENT_IMPLEMENTATION_MAP.md`](../planning/CURRENT_IMPLEMENTATION_MAP.md) — 코드 실제 상태
3. [`planning/IMPLEMENTATION_PRIORITY.md`](../planning/IMPLEMENTATION_PRIORITY.md) — Vertical Slice 1~5
4. [Figma 작업 보관 묶음](./_archive/2026-07-18-figma-handoff/README.md) — 색·화면·QA 근거가 필요할 때만 확인
5. Product Bible Screen Registry — 화면 ID

## Figma (참고만 · 2주간 안 건드림)

| 파일 | fileKey | 역할 |
|------|---------|------|
| **0718** | `yHhvn5RKjBd91U8BJUQz7F` | 쓰기 타깃이었음 |
| 0715 | `JSrjOy668zhfkiLplCkreh` | Archive·창고 |
| 0714 | `VXKyzoNdsgM4oN57mrECxb` | 키오스크 레이아웃 참고 |
| ASAK-1 | `k67gDKvnB29ILSzIpFYSaT` | 라임·SCR-008 참고 |
| kiosk_design | `iqaoVwFjFE6Zq1WpOVgjeG` | 로고 원본 |

0718에서 이미 손댄 것(중단 시점): 색 복구 일부, Core/QA 섹션, 로고 쑥색→Primary 일부, `Kiosk/ReceiptCard` 생성, SCR-008에 영수증 카드 배치 시작. SCR-023·Modal/DatePicker는 미완.

## 코드 핵심 (이미 있음)

- 가격: `ASAK-Kiosk/src/utils/priceCalculation.js`
- 수량: `ASAK-Kiosk/src/utils/quantityLimits.js`
- 토큰 CSS: `ASAK-Kiosk/src/styles/tokens.css`
- 세션: `orderSessionStore.js`

## 재개 시 추천 (디자인 말고 구현)

1. Slice 1 메뉴 목록 (mock/API 정합)
2. Slice 2 메뉴 상세·옵션
3. Slice 3 장바구니·주문
4. Slice 4 결제·완료
5. Slice 5 Admin Live Order  

영수증(SCR-023)은 MVP 후순위(FUTURE_SCOPE).

## 피그마 졸업 → 코드 (2026-07-18 밤)

- 검수 모음: [Figma 작업 보관 묶음](./_archive/2026-07-18-figma-handoff/README.md)
- **다음:** `implementation_guide/00_START_HERE.md` → Slice 1 메뉴 목록 (`ASAK-Kiosk`)
- 피그마 AI bulk / 전면 재작업은 하지 않음. Master 수치 FAIL만 필요할 때 최소 수정.

## 금지 (재개 전)

- Figma AI bulk rebinding
- 디자인 전면 재작업
- “일단 예쁘게” 대규모 리팩터
