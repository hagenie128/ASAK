# 앱 구현 문서 허브

> Status: **CURRENT**
> Product Bible(정책) · implementation-guide(작업 카드) · 저장소 PLAN(진행) 역할을 한 표로 정리합니다.

## 어디를 보나

| 질문 | 정본 | 보조 |
|---|---|---|
| **지금 코드가 어디까지?** | [구현 맵](impl-map-2026-07-16.md) · [baseline](../wiki/current-status-baseline.md) | [WBS 상태 메모](../wiki/wbs-status-notes.md) |
| **무엇을 할 일로 잡나?** | [작업 분해표](../wiki/wbs.md) | [프론트 3일 WBS](frontend-sprint-wbs-2026-07-20.md) *(Historical)* |
| **제품 규칙·API·SCR ID?** | [Product Bible 허브](../product_bible/product-bible-hub.md) → Pack README | [Canonical](../governance/contract-decisions-2026-07-16.md) |
| **지금 고치는 화면 작업 카드?** | [implementation-guide/00_START_HERE](../implementation-guide/00-start-here.md) | Pack 07·12 |
| **저장소별 이번 스프린트?** | Kiosk·back `IMPLEMENTATION_PLAN.md` · Admin `STRUCTURE_GUIDE` + Mock 사전 | `src/STRUCTURE_GUIDE.md` |
| **Figma↔코드 한 표?** | 워크스페이스 [ui-index.md](../../UI-INDEX.md) | [design/README.md](../design/README.md) |

## Pack 11/12 vs IMPLEMENTATION_PLAN (merge 안 함)

| 문서 | 역할 |
|---|---|
| `product_bible/11_Backend_Implementation/` | 백엔드 **수직 슬라이스·엔티티** 정책 |
| `product_bible/12_Frontend_Implementation/` | 프론트 **라우트·상태·통합** 정책 |
| `ASAK-Kiosk/IMPLEMENTATION_PLAN.md` | 키오스크 **이번 스프린트** 진행 |
| `ASAK-Admin/src/STRUCTURE_GUIDE.md` · `public/mocks/README.md` | 관리자 **이번 스프린트** (루트 `IMPLEMENTATION_PLAN.md` 삭제됨) |
| `ASAK-back/IMPLEMENTATION_PLAN.md` | 백엔드 **이번 스프린트** — 조회/장바구니 검증 경로 존재, 저장·결제·변경 API는 미완성 |

본문을 합치지 않습니다. Pack은 목표, PLAN은 저장소 실행 맥락입니다.

## 읽는 순서 (기능 하나 고칠 때)

1. [구현 맵](impl-map-2026-07-16.md)에서 SCR 상태 확인
2. [implementation-guide](../implementation-guide/00-start-here.md)에서 해당 SCR 블록
3. 관련 Pack **README** 또는 [Product Bible 허브](../product_bible/product-bible-hub.md) §2 MVP 15링크
4. 담당 저장소 실행 문서 확인 (Kiosk/back `IMPLEMENTATION_PLAN.md`, Admin `STRUCTURE_GUIDE` + Mock 사전)
