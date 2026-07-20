# 2026-07-16 Notion P0·API·DTO·DB 감사 — 이하진

> **템플릿:** [03-work-log-template.md](../../../docs/guides/03-work-log-template.md) · **일일:** [2026-07-16.md](../../daily/이하진/2026-07-16.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-07-16
- 담당자: 이하진
- 저장소: ASAK
- 브랜치: `docs/notion-web-audit-v1`
- 관련 이슈/PR: PR #7 Notion Audit Draft
- 작업 유형: `docs` / `api` / `database`

## 2. 작업 목적

- Notion의 P0 화면·시나리오·API·DB 기록을 실제 코드와 Product Bible에 대조해, 설계/계획과 구현 사실을 분리한다.

## 3. 직접 구현 영역

- P0 Screen record와 Cart/Sold-out 흐름을 검토해 legacy Figma 참조, 화면명, 상태 누락, 정책 불일치를 기록했다.
- API-002 메뉴 목록, API-003 메뉴 상세, API-004 메뉴 옵션, API-005 주문 생성, API-006 결제, API-009 품절, API-010 관리자 판매 항목 등 API 레코드를 재열람·수정·검증했다.
- `menu`, `ingredient`, `base`, `category`, `option`, `allergen`, `soldOut`, `order`, `payment`, `cartItemId`의 설계·구현 상태와 DTO/View Model 경계를 정리했다.

## 4. 구현 로직 / 적용한 방식

- endpoint는 문서의 예전 경로를 그대로 믿지 않고 Product Bible의 canonical 후보와 실제 Controller 존재 여부를 각각 확인했다.
- Notion 페이지마다 `MODIFIED / VERIFIED`, `SPEC_ONLY`, `NEEDS_CONFIRMATION`, `LEGACY`, `PENDING_FIGMA_CONFIRMATION`을 구분해 “문서에 있음”과 “코드에 구현됨”을 분리했다.
- Cart는 Client-only 정책, `cartItemId`, 수량 1/0/9/30 기준, 화면 문구의 View Model 책임을 API/DB 설계와 분리해 기록했다.

## 5. AI 도움 영역

- 사용한 AI 도구: ChatGPT, Codex, Notion/Figma 조회 보조
- 어떤 질문/요청을 했는지: P0 감사 대상을 빠짐없이 묶고, 각 항목의 근거·상태·후속 확인을 같은 표 형식으로 정리하도록 요청했다.
- AI가 도움 준 내용: API 경로, DTO field, DB entity/seed 여부, Figma 링크 상태를 비교할 체크리스트와 기록 형식을 제공했다.
- 그대로 사용한 부분: 화면/레코드 ID, Product Bible 계약, 실제 Backend Controller/Entity 검색 결과처럼 근거가 명확한 정보.
- 수정해서 사용한 부분: 구현 상태 라벨, legacy 처리, 후속 우선순위와 팀에 전달할 주의사항은 직접 재검토했다.

## 6. 발생 이슈

- 이슈 1:
  - 증상: Notion에는 API와 DB 설계가 있으나 실제 Backend 구현으로 오해할 수 있음.
  - 원인: 설계 문서, ERD, seed 데이터, API 명세와 Controller/Service/Repository/Entity 구현이 별도 단계임.
  - 해결: 실제 확인된 Backend는 `GET /api/health`와 공통 `ApiResponse`의 일부라는 점을 명시하고, 나머지 business endpoint·도메인 계층·JPA/Flyway 연결을 미구현/확인 필요로 구분했다.

## 7. 디버깅 기록

- 확인한 로그/에러 메시지: Cart endpoint와 Client-only Cart 정책, legacy Figma 링크, DB 키워드 검색 결과와 실제 구현 근거의 차이를 확인했다.
- 의심했던 지점: API 문서의 경로와 현재 canonical 후보가 일치하는지, `cartItemId`가 영속 DB 필드인지 화면 편집 식별자인지, 메뉴/품절 API 역할이 중복되는지.
- 실제 원인: 문서 버전 간 endpoint 명칭과 화면 참조가 변했으며, Backend 구현 증거가 아직 부족했다.
- 다시 같은 문제가 생기면 먼저 볼 파일/명령어: `notion-web-audit-ledger-2026-07-16.md`, Product Bible API Contract, `current-implementation-map-2026-07-16.md`, ASAK-back의 Controller·Entity·Migration 검색.

## 8. 이번 작업에서 배운 점

- 문서 감사의 핵심은 더 많은 내용을 채우는 일이 아니라, 증거가 있는 사실·설계·추정·보류를 구분해 다음 구현자가 잘못된 가정에서 시작하지 않게 하는 일이다.
- 화면 문구·옵션 요약은 DB DTO를 그대로 쓰기보다 View Model/Selector에서 만드는 경계를 먼저 정해야 한다.

## 9. 개선사항 / TODO

- 메뉴·주문·결제·품절의 canonical API 경로, request/response DTO, 오류 코드, owner를 프론트·백엔드 담당자가 확정한다.
- Entity·Repository·Service·Controller·Migration·테스트가 추가되면 `SPEC_ONLY` 항목을 실제 구현 근거와 함께 갱신한다.
- P1 Figma 링크 정합성, 테스트/오류 관리, 최종 제출 체크리스트 감사 배치를 진행한다.

## 10. 검증 내용

- 실행한 명령어: Notion Web 레코드 재열람, Product Bible 계약 및 Backend Controller/DB 관련 파일 검색.
- 테스트한 시나리오: API 8건과 DB 설계 1건을 실제로 열람·수정·재열람했는지, Cart/Sold-out 정책이 화면/API 기록과 충돌하지 않는지 확인.
- 확인 결과: 감사 ledger 기준 API 8건과 DB 설계 1건이 `MODIFIED / VERIFIED`로 기록됐고, 실제 구현 근거가 없는 항목은 별도 상태로 유지됐다.

## 11. 포트폴리오용 요약

Notion·Product Bible·코드를 교차 검증해 API·DTO·DB 문서의 과장된 완료 인식을 제거하고, 프론트엔드와 백엔드가 같은 데이터 계약을 확정할 수 있는 감사 기준을 만들었다.

## 12. 첨부하면 좋은 자료

- [Notion Web Audit Ledger](../../../docs/governance/notion-web-audit-ledger-2026-07-16.md)
- [API·DB 구현 가이드](../../../docs/implementation_guide/04-api-db-implementation.md)
- [현재 구현 맵](../../../docs/planning/current-implementation-map-2026-07-16.md)
