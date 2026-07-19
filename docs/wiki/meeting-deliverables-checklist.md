# ASAK 회의록 및 최종 배포 검증

> **현재 감사 안내 (2026-07-16):** 산출물 존재만으로는 구현 evidence가 아닙니다. 현재 evidence와 남은 blocker는 [current status baseline](current-status-baseline.md), [WBS 2.0](wbs-v2.md), [DevCopilot sync report](devcopilot-sync-report.md)에서 관리합니다.

> Notion 10. 회의록 + 11. 최종 제출 체크리스트 (2026-07-06)

## 회의록 인덱스

| 회의 | Notion | 로컬 |
|------|--------|------|
| 2026-07-03 키오스크 컨셉 | (Notion 10) | 아래 § |
| 화면 설계 초기 회의 · 사전 의견 | [Notion 인덱스](https://app.notion.com/p/39551ef04f0b8190b76ae4b48b8497ac) | [Archive 회의 기록](../archive/project-history/design-meetings/README.md) |
| **2026-07-06 화면 설계 초기 회의** | [Notion 취합본](https://app.notion.com/p/39551ef04f0b815f8dc6e788176186d7) | [회의록](../archive/project-history/design-meetings/screen-design-meeting-minutes-2026-07-06.md) · [변경 이력](../archive/project-history/design-meetings/screen-design-changes-2026-07-06.md) |

## 회의록

### 2026-07-03 키오스크 컨셉 회의

| 항목 | 내용 |
|------|------|
| 참석 | 하진, 유진, 나연 |
| 결정 | 서비스명 **ASAK/아삭**, Week 5 MVP = 고객 주문 (SCR-001~008, 8/1) + Week 6 관리자 확인, KVS/매출/멤버십 보류 |
| 디자인 | Primary #16A34A, Crunch Yellow #FACC15, Cream #FFFDF3 |
| 다음 | Figma 팔레트, 화면 흐름도, MVP DB/API, 와이어프레임 |

**MVP 고객**: 홈~결제완료 8화면 · **관리자**: 주문목록/상세/상태/품절

### 2026-07-06 화면 설계 초기 회의

| 항목 | 내용 |
|------|------|
| 참석 | 이하진, 김나연, 박유진, 강민준 |
| 결정 | **DS-02 Modern Minimal**, SCR-001+002 병합, SCR-005+006 병합(컨펌 팝업), 고객 UI **6단계**, 결제 로딩·에러 팝업/토스트 |
| 보류 | DS-08 참고안, 추천 우선 모드, 멤버십·영수증, 고객/관리자 DS 분리 |
| 다음 | Figma DS-02·통합 와이어, Notion SCR DB 반영 |

**MVP 고객 UI**: 홈·매장/포장 → 메뉴 → 옵션 → 장바구니·주문확인(팝업) → 결제 → 완료 (**6 UI 단계**, SCR-001~008 ID 유지)

상세: [회의록](../archive/project-history/design-meetings/screen-design-meeting-minutes-2026-07-06.md) · [변경 이력](../archive/project-history/design-meetings/screen-design-changes-2026-07-06.md)

---

## 11. 최종 제출 체크리스트

### 필수 산출물

| 산출물 | 위치 | 상태 |
|--------|------|------|
| 요구사항 정의서 | Notion 02 / Wiki | 완료 |
| 사용자 시나리오 | Notion 03 SC-001~018 | 완료 |
| 화면 설계서 | Notion 04 SCR-001~021 | 진행중 (로컬·Hub 반영 완료, Notion 수동) |
| ERD·테이블 정의 | Notion 05 · 22테이블 | 완료 |
| API 명세 | Notion 06 API-001~020 | 완료 |
| React/Spring | GitHub ASAK-front/back | 예정 |
| MySQL seed | asak-data/seed | 진행중 |
| 테스트 결과 | Notion 09 TC-001~014 | 진행중 |
| README | ASAK/README.md | 완료 |

### 시연 체크리스트

- [ ] 관리자 데이터 등록
- [ ] 키오스크 목록 조회
- [ ] 손님 주문 (SC-001)
- [ ] 결제 (SC-004)
- [ ] 완료 화면·주문번호
- [ ] 관리자 주문 확인·상태 변경
- [ ] 품절 비활성화 (SC-003)
- [ ] 재방문 5단계 이내 주문 (SC-002)

### DevCopilot Wiki 검증

1. https://devcopilot.ai.kr/workspace/2/wiki 접속
2. 산출물 8개 Wiki 문서 제목·내용 확인
3. Requirements / APIs / WBS 탭과 ID 추적성 대조

### 화면 설계 회의 반영 (2026-07-06)

- [x] `screens.json`·Wiki·SCR_REQ_MAP 병합 반영 (001+002, 005+006)
- [x] DS-02 Modern Minimal 프로덕션 DS 문서화
- [ ] Notion 04 SCR DB 수동 반영
- [ ] Figma DS-02·통합 와이어 적용

### Notion 문서 완성 (2026-07-05)

- [x] API-001~020 정합
- [x] SC-001~018 Mermaid
- [x] DB ERD 22테이블
- [x] WBS·테스트 Relation 컬럼
- [ ] Figma 프로토타입 (Notion 밖) — **DS-02 Modern Minimal** 방향 확정, 적용 진행
- [ ] React/Spring 구현 (Notion 밖)
