# 문서 네이밍 규칙 (신규)

> 적용: **앞으로 새로 만드는** 문서만.  
> 기존 파일은 **대량 이름 변경하지 않는다** (링크 깨짐 위험).

## 한 가지 규칙

**신규 문서는 `kebab-case.md`**

| 좋은 예 | 나쁜 예 |
|---|---|
| `payment-flow-notes.md` | `PaymentFlowNotes.md` |
| `sprint-checklist-2026-07-22.md` | `SPRINT_CHECKLIST.md` (신규라면) |
| `admin-mock-binding.md` | `Admin Mock Binding.md` (공백) |

## 예외 (유지)

| 패턴 | 이유 |
|---|---|
| `README.md` | 폴더 기본 진입 |
| `START_HERE.md` | 전역 진입 허브 (의도적 고정명) |
| 이미 있는 `UPPER_SNAKE.md` | `CURRENT_IMPLEMENTATION_MAP.md` 등 — **이동안 함** |

날짜가 필요하면 접미사: `frontend-wednesday-wbs-2026-07-20.md` 형태.

## 폴더별 안내

| 위치 | 신규 문서 |
|---|---|
| `docs/wiki/` | kebab-case |
| `docs/planning/` · `governance/` · `architecture/` | kebab-case 권장 (기존 UPPER는 유지) |
| `docs/product_bible/` | Pack 안 규칙은 각 Pack README 따름 · 루트에 산발 파일 추가 금지 |
| `docs/archive/` | 이동만 · 신규 작성 지양 |

## 제목(H1) vs 파일명

- 파일명: 영문 kebab-case  
- 본문 제목: 한국어 가능  
- 상태 배너: 문서 맨 위 인용구로 `Current` / `Historical` / `→ 대신 X`

## 하지 말 것

- 수백 개 일괄 rename  
- 승인 없이 archive로 이동·삭제  
- Product Bible 본문 대량 재작성
