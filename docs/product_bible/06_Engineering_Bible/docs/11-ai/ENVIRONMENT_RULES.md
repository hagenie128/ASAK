# Environment Rules

## 1. Fixed Versions

- Spring Boot 4.1.0
- Java 25
- React JavaScript
- Zustand
- Axios
- Vite

AI가 변경하지 않는다.

---

## 2. Frontend Environment

`.env` 예:

```text
VITE_API_BASE_URL=http://localhost:8080
```

코드:

```js
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
```

secret을 `VITE_`에 넣지 않는다.
Frontend env는 사용자에게 노출된다.

---

## 3. Backend Profile

```text
application.yml
application-local.yml
application-prod.yml
```

민감 정보는 environment variable.

---

## 4. Git 금지

- 실제 비밀번호
- DB credential
- token
- private key
- `.env` 실값

`.env.example`만 커밋한다.

---

## 5. Local Setup

README에 반드시:

- Java version
- Node version
- install
- run
- port
- env
- DB setup

을 기록한다.
