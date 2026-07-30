---
name: asak-doc-sync
description: "Use when updating ASAK Product Bible, Screen Bible, API specs, implementation guides, test documents, or README files from current code. Compare evidence first, update only approved documentation, and record unresolved code-to-spec conflicts."
---

# ASAK 현재 코드 기준 문서 동기화

현재 Git 코드와 검증 결과를 근거로 ASAK 문서를 갱신한다. 이 스킬은 문서를 갱신하는 도구이며 소스코드·DB·원격 Git은 수정하지 않는다.

## 시작 전 범위 확정

1. 대상 코드 저장소와 갱신 후보 문서를 확인한다. 문서 경로가 없으면 Product Bible, Screen Bible, API 명세, 구현 가이드, 테스트 문서, README 중 관련 후보를 먼저 제시한다.
2. `AGENTS.md`, 각 저장소의 Git 상태·최근 커밋·실제 변경 파일을 읽는다.
3. 관련 Product Bible·Screen Bible·Figma와 현재 코드를 모두 읽는다. 화면이면 Screen ID와 Figma Frame/Node, API면 method·path·request/response, DB면 테이블·필드·상태값을 확인한다.
4. 사용자가 문서 갱신을 요청한 범위만 수정한다. 범위가 넓거나 모호하면 변경 후보와 영향 문서를 먼저 제시하고 승인받는다.

## 증거와 불일치 처리

증거는 다음 순서로 정리한다.

1. 현재 코드, Git 이력, 실제 실행·테스트·브라우저 관찰
2. 기존 문서와 API 계약
3. Product Bible·Screen Bible
4. Figma

- 코드로 직접 확인한 구현 사실은 문서에 반영한다. 파일 경로, 화면 상태, API method/path, DTO 필드, 상태값, 검증 결과를 추정하지 않는다.
- 코드가 Product/Screen Bible의 사용자 경험·업무 규칙·계약과 충돌하면 정본을 코드에 맞춰 조용히 덮어쓰지 않는다. `결정 필요`로 기록하고, 코드/문서/Figma의 차이와 선택이 필요한 담당 범위를 남긴다.
- Mock 화면, 실제 API 연결, DB 반영, 결제/환불 처리는 서로 다른 상태로 표기한다.
- `totalAmount`, `approvedAmount`, `approvedAt`, `waitingOrderCount`, `CANCELED`, `APPROVED`를 공통 계약 용어로 쓰고, 레거시 이름은 adapter 또는 Mock 경계로 분리한다.

## 보조 스킬 선택

범위에 맞는 기존 ASAK 스킬을 함께 사용한다.

| 범위 | 보조 스킬 | 확인할 내용 |
| --- | --- | --- |
| API 명세 | `asak-api` | 요청·응답·오류·클라이언트 계약 |
| React 화면 | `asak-react-review` | Screen ID, 상태, 컴포넌트·Hook 흐름 |
| Spring/Mapper | `asak-backend-review` | Controller·Service·Mapper·DTO |
| DB 문서 | `asak-db` | 테이블·필드·상태 전이·DTO 매핑 |
| Figma/Screen Bible | `asak-figma-review` | Frame/Node, 문구, 화면 상태 |
| 테스트 문서 | `asak-test-plan` | Default·Loading·Empty·Error·Disabled 검증 |

보조 스킬의 분석 결과도 반드시 실제 파일과 실행 근거로 다시 확인한 뒤 문서에 반영한다.

## 문서 갱신 절차

1. 문서별로 현재 문장, 코드 근거, 변경 제안, 영향 화면/API를 표로 정리한다.
2. 코드 구현 사실과 명세 의도를 분리해 `구현됨`, `Mock`, `미연결`, `미검증`, `결정 필요` 중 알맞은 상태를 붙인다.
3. 승인된 문서만 최소 범위로 수정한다. 관련 없는 기존 문구·링크·팀원 변경은 보존한다.
4. API 문서에는 method/path, 인증, 요청/응답 필드, 상태·오류를 명시한다. 화면 문서에는 Screen ID, 상태, 이동, 문구, 데이터 필드, 재사용 컴포넌트를 명시한다.
5. 대상 저장소에 `docs/ai-reports/YYYY-MM-DD/asak-doc-sync-<짧은-주제>.md`를 남긴다. 이 기록에는 확인 코드, 갱신 문서, 변경 근거, 검증 결과, 결정 필요 사항을 적는다.

## 검증과 마무리

1. 갱신 문서를 다시 읽어 코드 근거와 method/path/필드/상태값이 일치하는지 확인한다.
2. `git diff --check`로 문서 공백 오류를 확인하고, 수정한 상대 링크의 대상 존재 여부를 확인한다.
3. 실행 검증을 했으면 실제 명령과 결과만 기록한다. 실행하지 않은 항목을 통과로 쓰지 않는다.
4. 자동 commit·push·branch 작업은 하지 않는다.
5. 사용자에게는 갱신 문서, 결과 기록, 남은 결정 필요 사항 링크만 짧게 전달한다.
