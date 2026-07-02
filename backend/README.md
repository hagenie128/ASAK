# ASAK Backend

이 폴더는 `ASAK (A Salad A Kiosk)`의 실제 백엔드 앱 영역입니다.

현재는 기본 골격만 먼저 만들고, 1차 크롤링 파이프라인과는 분리해서 관리합니다.

## 목적

- API 서버 구현
- 인증/권한
- 메뉴/키오스크용 서비스 로직
- 프론트가 사용할 데이터 제공

## 현재 구조

```text
src/
  main/
    java/
    resources/
  test/
    java/
```

## 참고

- 1차 크롤링은 `../data-pipeline/phase1/`
- 프론트는 `../frontend/`
