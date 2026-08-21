# 2026-08-21 태블릿 LAN 실접속 문제 계층별 분석 — 이하진

> **템플릿:** [03-work-log-template.md](../../../docs/guides/03-work-log-template.md) · **일일:** [2026-08-21.md](../../daily/이하진/2026-08-21.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-08-21
- 담당자: 이하진
- 저장소: ASAK-Kiosk, ASAK-back
- 관련 커밋: 없음 — 분석·정책 검토 단계이며 daily 기준 실제 코드 반영 여부는 별도 확인 필요.
- 작업 유형: `debug`

## 2. 작업 목적

PC에서는 정상 동작하는 Kiosk↔Spring 연동이 같은 네트워크의 태블릿에서 접속하면 백엔드 응답을 받지 못하는 문제의 원인을 계층별로 좁힌다.

## 3. 직접 구현 영역 (원인 후보 분리)

- 태블릿의 `localhost:8080`은 개발 PC가 아니라 태블릿 자신을 가리키므로, 프론트 API base URL이 `localhost`로 고정돼 있으면 Spring에 접근할 수 없다.
- Spring이 외부 LAN 접속을 받으려면 `server.address=0.0.0.0`, `server.port=8080` 바인딩이 필요하다.
- Vite 개발 서버도 `host: 0.0.0.0` (또는 `npm run dev -- --host 0.0.0.0`)이 필요하다.
- PC/태블릿이 동일 네트워크인지, Windows Defender Firewall이 8080/5173 inbound를 막고 있는지 확인이 필요하다.
- CORS 설정도 별도 확인 대상이다.

## 4. 구현 로직 / 적용한 방식

- 문제를 "태블릿에서 안 됨"이라는 하나의 증상으로 보지 않고 `Browser secure context → 프론트 API URL → Vite host/proxy → CORS·Firewall → Spring binding` 순서로 계층을 나눠 각 계층을 독립적으로 확인하는 방식을 사용했다.
- 개발 시 `.env`에 PC IP를 매번 고정하는 방식 대신, 아래처럼 `VITE_API_BASE_URL=/api` + Vite proxy로 상대경로를 사용하는 방향을 검토했다.

```env
VITE_API_BASE_URL=/api
```

```js
server: {
  host: "0.0.0.0",
  proxy: {
    "/api": {
      target: "http://localhost:8080",
      changeOrigin: true
    }
  }
}
```

- 이렇게 하면 개발 PC의 IP가 바뀔 때마다 프론트 환경변수를 수정할 필요가 줄어든다.

## 5. 발생 이슈

- 증상: PC 브라우저(`http://localhost`)에서는 정상 동작하던 기능이 태블릿(`http://192.168.x.x:*`)에서는 일부 브라우저 API가 제한됐다.
- 원인: `http://localhost`는 브라우저가 secure context로 취급하지만, 일반 HTTP로 LAN IP에 접속하면 secure context가 아니게 되어 `crypto.randomUUID()` 같은 API가 브라우저에 따라 제한될 수 있다.
- 해결(검토): UUID 라이브러리 사용 또는 fallback UUID 생성 함수 도입을 검토했다. 이 시점 기준 실제 코드 반영 여부는 별도 확인이 필요하다.

## 6. 이번 작업에서 배운 점

"태블릿에서 안 됨"을 프론트 버그 하나로 뭉뚱그리지 않고, 브라우저 보안(secure context) → 네트워크(방화벽) → 개발 서버 바인딩(Vite/Spring) → API 주소 구성 → CORS의 순서로 원인을 분리하면, 실제로 막힌 지점을 좁혀서 확인할 수 있다는 점을 확인했다.

## 7. 개선사항 / TODO

- [ ] Spring `server.address=0.0.0.0` 적용 여부 확인.
- [ ] Vite `host: 0.0.0.0` 및 proxy 설정 적용 여부 확인.
- [ ] Windows Firewall 8080/5173 inbound 허용 확인.
- [ ] `crypto.randomUUID()` LAN HTTP 환경 대응(라이브러리/fallback) 적용 여부 결정.
- [ ] 태블릿에서 Kiosk → Spring API 실접속 재검증.

## 8. 검증 내용

- 이 작업은 원인 후보를 계층별로 분리해 정리한 분석 단계이며, 실제 태블릿 재접속 테스트로 원인을 확정하지는 않았다.
- 미검증: Spring/Vite 바인딩 변경, 방화벽 설정 변경, UUID 대응 코드의 실제 적용 여부.

## 9. 포트폴리오용 요약

"태블릿에서만 안 된다"는 증상을 브라우저 secure context, 네트워크 바인딩, 방화벽, API 주소 구성 등 서로 다른 계층의 문제로 분해해 분석했다. 이후 동일한 계층 분해 방식을 매출 지연, boolean 직렬화 문제 등 다른 디버깅에도 재사용했다.

## 10. 참고 자료

- [2026-08-21 daily](../../daily/이하진/2026-08-21.md) — "태블릿 로컬 실접속 시 Spring/Vite 네트워크 구조 점검" 카드
- [2026-08-21 RTOS 영수증 병행 구조·팀 조율](2026-08-21-rtos-receipt-dual-format-collaboration.md)
