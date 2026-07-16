# ASAK Product Bible Pack 6 — Engineering Bible

> Status: Current  
> Scope: ASAK-Kiosk · ASAK_Admin · ASAK-back · ASAK Root

## 목적

이 Pack은 ASAK의 구현 규칙을 정의한다.

지금까지의 Feature Bible이 **무엇을 만들지** 정했다면,
Engineering Bible은 **어떤 구조와 기준으로 만들지** 정한다.

## 고정 기술 환경

### Frontend

- React
- JavaScript
- React Router
- Zustand
- Axios
- Vite
- CSS

### Backend

- Spring Boot 4.1.0
- Java 25
- Gradle
- Spring Web
- Bean Validation
- JPA/MySQL은 구현 단계에서 추가

## 고정 저장소 역할

| Repository | Responsibility |
|---|---|
| ASAK | 문서·설정·데이터·seed·AI 기준 |
| ASAK-Kiosk | 고객용 React |
| ASAK_Admin | 관리자용 React |
| ASAK-back | Spring API |

## 금지

- TypeScript 전환
- Tailwind 신규 설치
- Spring Boot/Java 버전 변경
- Zustand 제거
- scaffold를 미구현이라는 이유로 삭제
- 저장소 책임을 무시한 중복 구현
