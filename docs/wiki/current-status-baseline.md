# ASAK Current Status Baseline

> 기준일: 2026-07-16 · 소스 저장소와 DevCopilot workspace 2를 점검했습니다. 이 문서는 구현 baseline이며 완료 주장이 아닙니다.

## Evidence 기반 상태

| 영역 | 검증된 상태 | Status |
|---|---|---|
| Figma foundation/shared/component structure | 사용자 제공 Figma evidence; Figma MCP 미사용 | DESIGN_DONE only |
| Kiosk | React/Vite 빌드 통과; route는 home/menu/detail만; 데이터 I/O 작업 진행 중 | IN_PROGRESS |
| Admin | React/Vite 빌드 통과; 화면은 placeholder이며 route가 registry와 충돌 | TODO |
| Backend | Spring Boot 4.1.0 / Java 25 skeleton과 `GET /api/health`만 존재 | business API는 TODO |
| DB | DevCopilot model 26 tables·4 views; backend에 schema/entity/repository 구현 없음 | TODO |
| QA | 테스트 케이스 16건, 실행 evidence 없음 | TODO |

## 저장소 baseline

| Local folder | Current remote | Intended role | Decision |
|---|---|---|---|
| `ASAK` | `hagenie128/ASAK` | 정본 docs/data/Product Bible | 현재 정본 문서 소스 |
| `ASAK-Kiosk` | `hagenie128/ASAK-front` | 고객 React 앱 | BLOCKED — 로컬 remote와 목표 `ASAK-Kiosk` 불일치; 자동 변경 금지 |
| `ASAK-Admin` | `hagenie128/ASAK_Admin` | 관리자 React 앱 | 현재 정본 admin 구현 대상 |
| `ASAK-back` | `hagenie128/ASAK-back` | Spring Boot API | Skeleton only |

## 적용 규칙

- Design 완료는 코드·통합·QA evidence 없이 implementation DONE이 되지 않습니다.
- DevCopilot에 문서화된 API·DB model은 backend evidence가 있을 때까지 명세입니다.
- Kiosk 저장소 마이그레이션은 `NEEDS_CONFIRMATION`; pull, remote rewrite, reset, rebase, 소스 수정은 허용되지 않습니다.
