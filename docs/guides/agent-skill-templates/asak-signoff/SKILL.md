---
name: asak-signoff
description: "Use for ASAK end-of-day worklogs, documentation, Notion records, and Figma evidence."
---

# 퇴근

오늘의 작업을 실제 Git·코드·문서·Figma 근거와 대조해 워크로그와 필요한 문서에 정확히 남긴다. 구현, 검증, 다음 할 일을 섞어 쓰지 않는다. 소스코드와 Git 원격 상태는 바꾸지 않는다.

1. 날짜·작성자·대상 저장소를 확인하고 `AGENTS.md`, Git 상태/최근 커밋, Product Bible, Screen Bible, 기존 워크로그를 먼저 읽는다.
2. ASAK, ASAK-back, ASAK-Admin, ASAK-Kiosk의 변경을 저장소별로 분리한다. 커밋 존재는 기능 검증·배포 완료의 근거가 아니다.
3. 변경 파일·데이터 흐름·커밋/브랜치/원격 상태·실행한 검증을 근거로 수집한다. SQL 정의 수정은 실제 DB 조회 전까지 DB 반영으로 적지 않는다.
4. UI 관련이면 최신 Figma의 Screen ID, Frame/Node, Default·Loading·Empty·Error·Disabled 상태를 확인한다. 예전 Node를 추정해 적지 않는다.
5. 일일 워크로그에는 요약·직접 수행·검증 범위·다음 작업을, 상세 워크로그에는 목적·변경 파일/커밋·데이터 흐름·AI 도움·이슈/판단·남은 위험을 기록한다.
6. WBS·상태 노트·API 계약·DB 문서는 해당 근거가 상태/계약/운영 판단에 영향을 줄 때만 갱신한다. 완료 상태는 DoD와 검증 증거가 있을 때만 바꾼다.
7. Notion 동기화가 요청되었으면 수정 직전에 페이지·속성을 다시 읽고 기존 본문을 보존해 추가한다. 미확인 원격/DB 반영·테스트 통과를 기록하지 않는다.
8. 수정한 문서만 `git diff --check`로 확인해 trailing whitespace를 제거하고, 기존 사용자 변경과 이번 문서 변경을 구분해 보고한다.

보고: 반영한 기록, 확인 근거, 미검증 항목, 다음 작업.
