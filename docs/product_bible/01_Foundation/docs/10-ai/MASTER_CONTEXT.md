# ASAK AI Master Context

> Status: Current  
> AI는 작업 전에 이 문서를 읽는다.

## Project

ASAK는 샐러드 키오스크와 관리자 운영 시스템이다.

## Repositories

- ASAK: docs/config/data/seed/AI rules
- ASAK-Kiosk: React JavaScript customer app
- ASAK_Admin: React JavaScript admin app
- ASAK-back: Spring Boot 4.1.0 / Java 25

## Fixed Technology

- React JavaScript
- Zustand
- Axios
- Vite
- Spring Boot 4.1.0
- Java 25
- DB snake_case
- JSON camelCase

변경 금지:

- TypeScript 변환
- Tailwind 신규 설치
- Spring/Java 다운그레이드
- 저장소 전면 통합
- 기존 scaffold를 미구현이라는 이유로 삭제

## Figma

- File: JSrjOy668zhfkiLplCkreh
- Latest Kiosk: 05-B `39:6828`
- Latest Admin: 06-B `39:7344`
- PrototypeMap v2: `107:7720`
- Audit Board: `103:2`

## Current Important Decisions

- Pretendard Variable
- Apple + Salady
- SCR-022 Dashboard
- waitingOrderCount
- Cart option edit/delete
- timeout warning flow
- Admin TTS
- Figma B original preservation
- Premium work in C pages

## Naming

- variables/methods/props/state/url: camelCase
- React/Java classes: PascalCase
- DB: snake_case
- JS constant object: UpperCamelCase
- status value: UPPER_SNAKE_CASE

## Work Rule

1. Read canonical docs.
2. Inspect actual files.
3. Report differences.
4. Do not force code to match old assumptions.
5. Preserve scaffold.
6. Explain why every structural change is needed.
7. Update docs after work.

## Completion Report

```md
## Target
## Changed
## Why
## Figma Impact
## React Impact
## API/DB Impact
## QA
## Remaining P0/P1/P2
```
