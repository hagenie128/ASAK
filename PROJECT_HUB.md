# ASAK 프로젝트 작업 허브

> 팀원이 작업을 시작할 때 **이 문서 하나만 먼저 연다.** 상세 문서는 필요한 순간에만 연다.

## 1. 지금 할 일

1. [구현 작업대](docs/implementation_guide/00_START_HERE.md)에서 기능 한 개를 고른다.
2. 해당 저장소의 실제 코드를 확인한다.
3. 완료 기준·검증 결과를 [팀 워크로그](worklog/TEAM_WORKLOG.md)에 남긴다.
4. 남은 작업·버그·팀 결정이 있으면 GitHub 이슈 **초안**을 만든다.

## 2. 저장소 역할

| 저장소 | 여기서 하는 일 | 새 기능을 만들 때 |
|---|---|---|
| `ASAK` | 제품 기준, API·화면 계약, 문서, 워크로그 | 정책·계약 확인과 기록만 |
| `ASAK-Kiosk` | 고객 키오스크 React | 메뉴·장바구니·결제·완료 구현 |
| `ASAK-Admin` | 관리자 React | 주문·품절·메뉴·매출 화면 구현 |
| `ASAK-back` | Spring Boot API·DB | 메뉴·주문·결제·관리자 API 구현 |

## 3. 현재 상태를 짧게 보면

| 영역 | 현재 상태 | 다음 우선순위 |
|---|---|---|
| Kiosk | 메뉴 목록은 mock 기반, 상세는 일부만 연결 | 메뉴 상세 → 장바구니 → 주문 |
| Admin | 라우트·페이지 대부분 placeholder | Live Order 상태 변경 |
| Backend | Health endpoint만 있음 | 메뉴 목록 API와 DB 연결 |
| Figma | 작업 중지, 코드 구현 우선 | 필요할 때만 디자인 참고 |

정확한 화면별 상태는 [현재 구현 지도](docs/planning/CURRENT_IMPLEMENTATION_MAP.md)를 확인한다.

## 4. 기준이 충돌할 때

1. 실제 코드와 현재 구현 지도
2. [정본 계약](docs/governance/CANONICAL_CONTRACT_DECISIONS.md)
3. 구현 가이드의 해당 기능 블록
4. Product Bible의 해당 기능 문서
5. Figma·회의록·과거 QA·AI 대화

5번은 참고 자료다. 현재 코드나 계약을 임의로 덮어쓰지 않는다.

## 5. 포트폴리오로 남길 정보

아래는 보관한다.

- 기능별 문제, 본인의 판단과 구현, AI 제안을 검토·수정한 이유
- 테스트 결과, 해결한 오류의 원인과 해결 방법
- PR, 화면 캡처, 시연 영상, 완료 기준

기록 위치: [팀 워크로그](worklog/TEAM_WORKLOG.md) → 필요하면 `worklog/entries/{이름}/` 상세 기록.

## 6. 굳이 먼저 읽지 않을 자료

- `docs/_archive/`, `docs/design/_archive/`, `docs/notion/`
- 날짜가 붙은 회의·감사·Figma AI 프롬프트
- Kiosk 안의 Admin scaffold

필요한 근거를 찾는 경우에만 열고, 새 작업 기준으로 복사하지 않는다.
