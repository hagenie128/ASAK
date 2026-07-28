---
name: asak-study
description: "Use to study implemented ASAK code by date, feature, file, screen, or API flow without editing source files."
---

# 공부

구현된 ASAK 코드를 날짜·기능·파일·Screen ID·API 흐름 중 사용자가 정한 기준으로 복습할 수 있게 설명한다. 목표는 코드를 대신 구현하는 것이 아니라, 초보자도 실제 데이터 흐름을 따라 읽고 직접 확인할 수 있는 학습 경로를 만드는 것이다.

## 시작 전 확인

1. 학습 기준(날짜/기능/파일/화면/API), 대상 저장소, 이해 수준을 확인한다. 지정이 없으면 최근 커밋이나 사용자가 말한 기능을 기준으로 범위를 제안한다.
2. `AGENTS.md`, 현재 Git 상태, 관련 Product Bible·Screen Bible·Figma, 실제 변경 파일과 최근 커밋을 읽는다.
3. 구현 완료, mock 기반, 실제 API 연결, DB 반영, 미검증 상태를 분리한다. 소스코드·문서·Git 이력은 수정하지 않는다.

## 읽는 순서

기능을 아래 흐름으로 역추적한다. 없는 계층은 억지로 만들지 말고 실제 구조를 표시한다.

```text
화면/Page → Component → Hook/상태 → API 또는 Repository → DTO/응답 → Service/Mapper/DB 또는 Mock JSON
```

- Frontend mock은 Page → Hook → Repository → JSON 흐름으로 설명한다.
- 실제 API는 화면 요청 → Controller → Service → Mapper/Repository → DB → 응답 DTO → 화면 표시 흐름으로 설명한다.
- UI는 Screen ID, Figma Frame/Node, 상태별(Default·Loading·Empty·Error·Disabled) 차이를 함께 확인한다.
- 공통 계약은 `totalAmount`, `CANCELED`를 기준으로 설명하고 legacy mock 필드는 호환 경계로 분리한다.

## 학습 가이드 출력

1. 한 문장 결론: 이 기능이 사용자에게 제공하는 결과
2. 범위와 확인 파일: 파일마다 “왜 읽는지” 한 줄
3. 전체 흐름 그림: 실제 호출/데이터 경로
4. 파일별 복습: 핵심 함수/props/상태, 입력→처리→출력, 초보자 주의점
5. mock·API·DB·검증 상태: 확인된 사실과 아직 확인하지 않은 사실을 분리
6. 직접 해볼 확인 항목: 화면 조작, API/JSON 관찰, 상태 변화, 디버깅 포인트
7. 짧은 연습문제 3~5개와 정답 확인 위치

## 품질 기준

- Page가 조립만 하는지, 데이터 계층이 어디인지 실제 파일을 근거로 설명한다.
- 스크린샷/문서 설명을 현재 코드의 증거처럼 쓰지 않는다.
- 파일을 열지 않고 함수명·필드명·동작을 추정하지 않는다.
- 답변 끝에는 다음에 읽을 파일 3개 이내와 스스로 설명해 볼 질문을 남긴다.
