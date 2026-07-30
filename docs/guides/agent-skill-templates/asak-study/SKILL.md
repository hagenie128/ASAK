---
name: asak-study
description: "Use to study implemented ASAK code by date, feature, file, screen, or API flow without editing source files, and leave a canonical-depth study report in the target repository."
---

# ASAK 공부

구현된 ASAK 코드를 날짜·기능·파일·Screen ID·API 흐름 기준으로 복습할 수 있게 설명한다. 코드를 대신 구현하지 않으며, 초보자도 실제 데이터 흐름을 따라 읽고 직접 확인할 수 있는 학습 경로와 결과 레포트를 남긴다.

## 정본과 결과 파일

기본 설명 정본은 팀 공용 ASAK 문서 저장소의 `docs/ai-reports/ASAK_STUDY_EXAMPLE_CANONICAL.md`이다. 작업 시작 전 실제 위치를 찾아 읽고, 개인 PC 절대경로를 기준으로 고정하지 않는다.

1. 공부를 시작하기 전에 정본을 읽는다.
2. 정본의 **설명 깊이와 구성 방식**을 따른다. 정본 속 예시의 기능 완료 여부·API 경로·Figma Node·데이터는 현재 작업의 사실로 복사하지 않는다.
3. 사용자가 다른 정본 파일을 지정하면 그 파일을 이번 작업의 우선 기준으로 사용한다.
4. 대상 저장소에 `docs/ai-reports/YYYY-MM-DD/asak-study-<짧은-주제>.md`를 만든다. 폴더가 없으면 만든다.
5. 같은 공부 요청을 이어서 처리하면 같은 레포트를 갱신한다. 별도 주제면 새 파일을 만든다.
6. 채팅에는 레포트 전체를 붙여 넣지 않는다. 완료 결과와 파일 링크만 짧게 알린다.

정본 파일을 읽을 수 없으면 그 사실을 밝히고, 아래 필수 목차를 기준으로 레포트를 남긴다. 정본이 없다는 이유로 코드나 문서의 내용을 추정하지 않는다.

## 시작 전 확인

1. 학습 기준(날짜/기능/파일/화면/API), 대상 저장소, 이해 수준을 확인한다. 지정이 없으면 최근 커밋이나 사용자가 말한 기능을 기준으로 범위를 제안한다.
2. `AGENTS.md`, 현재 Git 상태, 관련 Product Bible·Screen Bible·Figma, 실제 변경 파일과 최근 커밋을 읽는다.
3. 구현 완료, Mock 기반, 실제 API 연결, DB 반영, 미검증 상태를 분리한다.
4. 소스코드, DB, 원격 Git 이력은 수정하지 않는다. 이 스킬이 만드는 파일은 공부 레포트뿐이다.

## 읽는 순서

기능을 아래 흐름으로 역추적한다. 없는 계층은 억지로 만들지 말고 실제 구조를 표시한다.

```text
화면/Page → Component → Hook/상태 → API 또는 Repository → DTO/응답 → Service/Mapper/DB 또는 Mock JSON
```

- Frontend Mock은 Page → Hook → Repository → JSON 흐름으로 설명한다.
- 실제 API는 화면 요청 → Controller → Service → Mapper/Repository → DB → 응답 DTO → 화면 표시 흐름으로 설명한다.
- UI는 Screen ID, Figma Frame/Node, 상태별(Default·Loading·Empty·Error·Disabled) 차이를 함께 확인한다.
- 공통 계약은 `totalAmount`, `approvedAmount`, `approvedAt`, `waitingOrderCount`, `CANCELED`, `APPROVED`를 기준으로 설명한다. 레거시 Mock 필드는 호환 경계로 분리한다.

## 레포트 필수 목차

정본의 형식을 바탕으로, 현재 작업의 실제 증거로 아래 항목을 작성한다.

1. 문서 기본 정보와 한 줄 결론
2. 화면 목적과 사용자 관점의 동작
3. 범위·확인 파일·각 파일을 읽은 이유
4. 전체 호출·데이터 흐름 그림
5. 파일별 복습: 핵심 함수/props/상태, 입력 → 처리 → 출력, 초보자 주의점
6. 화면 상태: Default·Loading·Empty·Error·Disabled와 Figma/Screen Bible 확인 결과
7. 데이터 필드와 Mock·API·DB·명세의 검증 상태
8. 확인한 사실 / 코드 근거에 따른 해석 / 미확인 또는 TODO의 분리
9. 검증 기록: lint·build·브라우저·API·DB 등 실제로 실행하거나 확인한 항목과 결과
10. 직접 해 볼 확인 항목, 연습문제 3~5개, 다음에 읽을 파일 최대 3개

다음 원칙을 지킨다.

- 파일을 열지 않고 함수명·필드명·동작을 추정하지 않는다.
- 스크린샷이나 기획 문서를 현재 코드의 증거처럼 쓰지 않는다.
- Mock으로 화면이 보이는 사실, 실제 API 연결, DB 반영, 결제 환불 처리를 서로 다른 검증 항목으로 쓴다.
- 취소와 환불을 같은 의미로 단정하지 않는다. 결제 환불은 서비스 호출·DB 기록·실패 처리 근거가 있을 때만 확인됨으로 쓴다.
- 명세와 코드가 다르면 어느 한쪽을 임의로 정답 처리하지 말고 불일치와 확인할 담당 범위를 기록한다.
- 실패한 검증은 실패 위치·현재 레포트에서 확정 가능한 범위·다음 확인을 함께 적는다.
- 비밀값, 토큰, 개인정보, 원본 오류 로그 전체는 기록하지 않는다.

## 마무리

1. 생성 또는 갱신한 레포트의 경로와 Git 상태를 확인한다.
2. 자동 commit·push·branch 작업은 하지 않는다. Git 반영은 사용자의 별도 승인 범위만 따른다.
3. 사용자에게는 레포트 파일 링크와 핵심 완료 사실만 짧게 전달한다.
