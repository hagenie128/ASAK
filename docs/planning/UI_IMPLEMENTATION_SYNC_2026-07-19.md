# UI 구현 최신 동기화 (2026-07-19)

## 범위

이 문서는 2026-07-18~19에 각 구현 저장소의 `main`에 반영된 Figma 기반 UI 결과를 중앙 문서에 동기화한다.

이번 반영은 화면 구조, 레이아웃, 로컬 이미지, 반응형 레일까지만 포함한다. API 호출, JSON 로딩/확장, 실제 주문·결제·로그인·저장은 의도적으로 연결하지 않았다. 기존 팀원의 store, 메뉴 상세 옵션, mock JSON과 API 모듈은 유지했다.

## 반영 저장소

| 저장소 | 화면 상태 | 확인 |
| --- | --- | --- |
| `ASAK-Kiosk` | 홈, 메뉴 목록/상세, 장바구니, 결제, 완료, 접근성 UI | `npm run build` 통과 |
| `ASAK-Admin` | 로그인, 주문 현황/관리, 대시보드, 메뉴, 품절, 결제수단, 매출 UI | `npm run build` 통과 |
| `ASAK-back` | Bruno `GET /api/health` 컬렉션 | UI 범위 아님 |

## Kiosk 경로

| 화면 | 경로 | 동작 범위 |
| --- | --- | --- |
| 홈 | `/` | 제공받은 ASAK 로고와 메뉴 진입 UI |
| 메뉴 목록 | `/menu` | 기존 `kiosk.json` 메뉴 표시 |
| 메뉴 상세 | `/menu/:menuId` | 기존 옵션/store 구조를 보존한 UI |
| 장바구니 | `/cart` | 빈 상태 UI |
| 결제 | `/payment` | 결제 수단 UI, 기능 없음 |
| 완료 | `/complete` | 영수증 UI, 기능 없음 |
| 접근성 | `/accessibility` | 컨트롤 표시 전용 |

## Admin 경로

| 화면 | 경로 | 동작 범위 |
| --- | --- | --- |
| 주문 현황 | `/` | 표시 전용 주문 현황; 1024px에서 아이콘 레일 |
| 대시보드 | `/dashboard` | 임시 지표/차트 UI |
| 주문 관리 | `/orders` | 목록·상세 레이아웃 |
| 품절 관리 | `/sold-out` | 토글 표시 전용 |
| 메뉴 관리 | `/menus` | 목록 UI |
| 메뉴 등록/수정 | `/menus/new`, `/menus/edit` | 폼 UI, 저장 없음 |
| 결제 수단 | `/payment-methods` | 설정 UI, 저장 없음 |
| 매출 | `/sales` | 기간/차트 UI |
| 로그인 | `/login` | 브랜드 UI, 인증 없음 |

## 디자인 및 CSS

- Kiosk 홈은 제공된 원본 로고를 투명 배경의 로컬 에셋으로 정리해 사용한다.
- 원형 플레이스홀더는 일관된 아이콘/SVG로 교체했고, 기능 없는 버튼은 비활성 또는 표시 전용이다.
- Admin은 1920×1080을 우선하고, 태블릿 주문 현황에서는 아이콘 전용 사이드바로 축소한다.
- CSS는 기존 구조를 유지한 채 Prettier로 정리했다. 동일 의미의 선택자 중복은 추가하지 않았고 반응형 재정의는 미디어 쿼리 안에 한정한다.

## 화면 캡처

- `ASAK-Kiosk/docs/screenshots/2026-07-18-kiosk-*.png`
- `ASAK-Kiosk/docs/screenshots/2026-07-19-kiosk-*.png`
- `ASAK-Admin/docs/screenshots/2026-07-18-admin-*.png`
- `ASAK-Admin/docs/screenshots/2026-07-19-admin-*.png`

## 다음 단계

1. 라우트/응답 계약 확정 후 API adapter를 연결한다.
2. UI의 임시 값을 실제 조회 데이터로 교체한다.
3. 주문·결제·로그인·메뉴 저장은 성공/실패/로딩 상태를 정의한 뒤 연결한다.
