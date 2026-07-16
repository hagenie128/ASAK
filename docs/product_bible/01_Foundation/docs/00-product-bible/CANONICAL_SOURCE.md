# ASAK Canonical Source

> Status: Current  
> 이 문서는 정보 충돌 시 어떤 자료를 우선할지 정의한다.

## 1. Repository Responsibility

| Repository | Responsibility |
|---|---|
| ASAK | 공식 문서, 설정, 데이터, seed, 운영 기준, AI 기준 |
| ASAK-Kiosk | 고객용 React JavaScript |
| ASAK_Admin | 관리자용 React JavaScript |
| ASAK-back | Spring Boot API |

---

## 2. Source of Truth by Domain

| Domain | Canonical Source |
|---|---|
| Product policy | `ASAK/docs/00-product-bible` |
| Design token | `ASAK/docs/01-design` |
| Screen ID | `ASAK/docs/07-screens/SCREEN_REGISTRY.md` |
| Figma latest screen | 05-B, 06-B 또는 승인된 05-C, 06-C |
| Prototype flow | PrototypeMap v2 `107:7720` |
| React component | 각 앱 저장소 실제 source |
| API contract | `ASAK/docs/06-api` |
| DB schema | `ASAK/docs/05-database` + migration/seed |
| Feature policy | `ASAK/docs/09-features` |
| QA | `ASAK/docs/10-qa` |
| AI instruction | `ASAK/docs/11-ai` |

---

## 3. Figma Priority

현재 최신 기준:

- `05-B Screens/Kiosk`
- `06-B Screens/Admin`
- `07 User Flows & Prototype`

원본 보존:

- `05 Screens/Kiosk`
- `06 Screens/Admin`

Premium 제안:

- `05-C Screens/Kiosk Premium`
- `06-C Screens/Admin Premium`

원칙:

- 명백한 오타·금액 오류는 B 수정 가능
- 레이아웃·브랜드·정보구조 변경은 C에서 진행
- PrototypeMap v1은 보존용
- PrototypeMap v2가 최신

---

## 4. Screen ID Conflict Rule

같은 SCR ID가 여러 기능을 의미하면 구현을 중단하고 Registry를 먼저 수정한다.

현재 권장:

- SCR-020: Admin Monthly Sales
- SCR-021: Admin Daily Sales
- SCR-022: Admin Dashboard
- SCR-023: Receipt Output
- SCR-024: Membership/Coupon

---

## 5. Document Status

모든 공식 문서는 상단에 다음을 가진다.

```txt
Status: Current | Draft | Archived | Superseded
Version:
Last Updated:
Supersedes:
```

`Archived`와 `Superseded` 문서는 AI 작업 기준으로 사용하지 않는다.

---

## 6. Conflict Resolution Order

1. 승인된 Decision/ADR
2. Canonical Registry
3. Feature Policy
4. API/DB Contract
5. 최신 Figma
6. 실제 source code
7. 이전 문서
8. 채팅 기록

단, 실제 코드가 공식 계약과 다르면 자동으로 계약을 바꾸지 않고 차이로 보고한다.
