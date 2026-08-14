# 프론트 미사용 Mock 보관

> Status: **HISTORY**

프론트 런타임이 더 이상 읽지 않는 대용량 JSON을 여기로 옮겼습니다.

| 파일 | 출처 | 비고 |
|---|---|---|
| `kiosk.json` | `ASAK-Kiosk/public/mocks/` | 메뉴·옵션·결제 시나리오 전체 |
| `student-project-data.json` | `ASAK-Kiosk/public/mocks/` | 발표용 확장 목업 |
| `asak-admin-data.legacy.json` | `ASAK-Kiosk/public/mocks/` | 구스키마 Admin mock |

현재 프론트 기준:

- Kiosk 실행: 실 API + `public/mocks/payment-scenarios.sample.json`(예시만)
- Admin 실행: `ASAK-Admin/src/mocks/asak-admin-data.json` + `adminMockRepository.js`
