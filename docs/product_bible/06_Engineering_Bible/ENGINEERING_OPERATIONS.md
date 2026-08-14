# Engineering Operations

> Status: `Canonical`
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `ENGINEERING_CHECKLIST.md`
- `ENVIRONMENT_RULES.md`
- `GIT_AND_REVIEW_RULES.md`
- `NAMING_BIBLE.md`
- `REPOSITORY_BOUNDARY.md`

---

## 원문: `ENGINEERING_CHECKLIST.md`

### Engineering Checklist

#### Frontend

- [ ] JavaScript
- [ ] 실제 폴더 구조 준수
- [ ] Component PascalCase
- [ ] variable/function camelCase
- [ ] constant UpperCamelCase
- [ ] API module 분리
- [ ] Store 범위 적절
- [ ] loading/empty/error
- [ ] no index key
- [ ] accessibility
- [ ] build
- [ ] lint

#### Backend

- [ ] Controller → Service → Repository
- [ ] DTO 분리
- [ ] Entity 직접 반환 금지
- [ ] Bean Validation
- [ ] Business Validation
- [ ] Transaction
- [ ] GlobalExceptionHandler
- [ ] status transition
- [ ] price recalculation
- [ ] logging

#### Database

- [ ] snake_case
- [ ] FK
- [ ] index
- [ ] money integer
- [ ] historical snapshot
- [ ] delete policy
- [ ] migration/seed

#### API

- [ ] URL camelCase
- [ ] JSON camelCase
- [ ] status UPPER_SNAKE_CASE
- [ ] response envelope
- [ ] error code
- [ ] pagination/filter
- [ ] date/timezone
- [ ] idempotency

#### Integration

- [ ] Figma field
- [ ] React props/state
- [ ] API DTO
- [ ] Entity/DB
- [ ] QA case
- [ ] Product Bible update

---

## 원문: `ENVIRONMENT_RULES.md`

### Environment Rules

#### 1. Fixed Versions

- Spring Boot 4.1.0
- Java 25
- React JavaScript
- Zustand
- Axios
- Vite

AI가 변경하지 않는다.

---

#### 2. Frontend Environment

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

#### 3. Backend Profile

```text
application.yml
application-local.yml
application-prod.yml
```

민감 정보는 environment variable.

---

#### 4. Git 금지

- 실제 비밀번호
- DB credential
- token
- private key
- `.env` 실값

`.env.example`만 커밋한다.

---

#### 5. Local Setup

README에 반드시:

- Java version
- Node version
- install
- run
- port
- env
- DB setup

을 기록한다.

---

## 원문: `GIT_AND_REVIEW_RULES.md`

### Git and Code Review Rules

#### 1. Branch

```text
feature/
fix/

refactor/
hotfix/
```

한 branch는 하나의 목적.

---

#### 2. Commit

권장:

```text
feat:
fix:
docs:
refactor:
style:
test:
chore:
```

예:

```text
feat: 관리자 대시보드 KPI 카드 추가
fix: 결제 오류 화면 금액 정합성 수정
docs: TTS 중복 호출 정책 문서화
```

---

#### 3. Commit Scope

너무 큰 commit 금지.

좋은 분리:

1. scaffold
2. component
3. state
4. API
5. QA/docs

---

#### 4. PR Description

```md
#### 목적
#### 변경 내용
#### 변경 이유
#### 영향 화면
#### API/DB 영향
#### 테스트
#### 스크린샷
#### 남은 작업
```

---

#### 5. Review Checklist

- naming
- duplication
- state
- error recovery
- API contract
- DB impact
- Figma consistency
- accessibility
- build/lint
- secrets

---

#### 6. Merge

팀원 작업과 충돌 가능한 파일:

- App/Router
- store
- constants
- shared component
- API client

수정 전에 담당자와 범위를 확인한다.

---

#### 7. 일상 워크플로 (원격 main까지 반영하기)

`main`에 직접 커밋하지 않는다. 독립 저장소마다 아래 1→10 순서를 지킨다. 변경 파일은 `git add .`로 일괄 stage하지 않고, 승인된 경로만 명시한다. 작업 트리가 더럽거나 `main`을 안전하게 최신화할 수 없으면 stash·reset·rebase를 하지 말고 중단한다.

```powershell
### 1. main 최신화
git switch main
git pull --ff-only origin main

### 2. 기능별·레포별 작업 브랜치 생성
git switch -c feat/admin-order-list   # 또는 ..., fix/..., chore/...

### 3. 승인된 파일 검토·stage·검증
git diff
git diff --check
git add -- src/api/ordersApi.js src/pages/admin/OrderListPage.jsx
### 프로젝트에 맞는 build/test 실행

### 4. 한글 커밋: 에이전트 이름을 제목에 넣지 않는다
git commit -m "feat: admin 주문목록 조회 구현"

### 5. 작업 브랜치를 GitHub에 푸시
git push -u origin feat/admin-order-list

### 6. main으로 이동 후 다시 최신화
git switch main
git pull --ff-only origin main

### 7. 작업 브랜치를 main에 병합
git merge feat/admin-order-list

### 8. 병합된 main을 GitHub에 푸시
git push origin main

### 9. 병합된 로컬 작업 브랜치 삭제
git branch -d feat/admin-order-list

### 10. GitHub 원격 작업 브랜치 삭제
git push origin --delete feat/admin-order-list
```

8단계 뒤에는 대상 커밋이 `main`에 포함되고 `HEAD == origin/main`인지 확인한다. 7단계에서 충돌이 발생하면 자동 해결하지 말고 중단한다. PR이 필수인 저장소는 5단계에서 PR을 만든 뒤, 승인·병합 후 6·8·9·10단계를 수행한다.

##### 7.4 자주 막히는 경우

| 메시지 | 의미 | 할 일 |
|--------|------|--------|
| `non-fast-forward` / behind | 원격이 더 앞섬 | `main`에서 `git pull --ff-only origin main` 후 병합 가능 여부를 다시 확인 |
| `Everything up-to-date` | 올릴 새 커밋 없음 | 보통 정상 (이미 같음) |
| merge 충돌 | 같은 파일 양쪽 수정 | 자동 해결하지 말고 충돌 범위와 다음 조치를 팀에 확인 |

**요약:** main 최신화 → 기능/레포별 브랜치 → 명시 stage·검증 → 한글 커밋 → 원격 브랜치 푸시 → main 최신화 → 병합 → 원격 main 푸시 → 로컬 브랜치 삭제 → 원격 브랜치 삭제

`git push --force`는 원격 커밋을 덮어쓰므로, 단순 behind 상황에서는 쓰지 않는다.

---

## 원문: `NAMING_BIBLE.md`

### ASAK Naming Bible

> Status: Current

#### 1. Frontend Variable / Function / State / Props

```text
camelCase
```

좋은 예:

```js
selectedCategory
totalAmount
waitingOrderCount
handlePayment
fetchOrderList
```

---

#### 2. Backend Field / Method / Package Variable

```text
camelCase
```

```java
orderService
totalAmount
findOrderById()
updateOrderStatus()
```

---

#### 3. Class / React Component

```text
PascalCase
```

```text
OrderController
OrderService
OrderDetailResponse
MenuCard
CartItemCard
```

---

#### 4. Database

```text
snake_case
```

```text
order_item
payment_method
created_at
order_status
```

---

#### 5. URL

```text
camelCase
```

```text
/admin/paymentMethods
/kiosk/menuDetail
```

---

#### 6. Constants

사용자 결정:

```text
UpperCamelCase
```

```js
export const OrderStatus = {
  Received: "RECEIVED",
  Preparing: "PREPARING",
  Completed: "COMPLETED",
};
```

상수 객체명과 key는 UpperCamelCase.

실제 code value는 UPPER_SNAKE_CASE.

---

#### 7. Figma Component

```text
Domain/PascalCase
```

```text
Admin/StatusBadge
Kiosk/BottomCTA
Shared/ConfirmDialog
```

---

#### 8. Figma Layer / Variant Property

```text
camelCase
```

```text
mainContent
totalAmount
state=loading
status=success
```

---

#### 9. Git Branch

```text
feature/
fix/

refactor/
hotfix/
```

예:

```text
feature/admin-dashboard
fix/payment-amount
tts-architecture
```

---

## 원문: `REPOSITORY_BOUNDARY.md`

### Repository Boundary

#### ASAK

담당:

- Product Bible
- Design/API/DB 문서
- seed
- 설정
- AI rules
- 운영 기준

금지:

- Kiosk/Admin 실제 UI 구현 복제
- Spring source 복제

---

#### ASAK-Kiosk

담당:

- 고객용 React
- Cart/Order session
- Kiosk API client
- 접근성/Timeout

금지:

- Admin 실제 화면 신규 구현
- Backend 비즈니스 규칙 복제

---

#### ASAK_Admin

담당:

- Dashboard
- Live Order
- Order Management
- Sold-out
- Menu Management
- Payment Settings
- Sales
- TTS

금지:

- 고객 Cart 구현
- Kiosk route

---

#### ASAK-back

담당:

- API
- 비즈니스 검증
- Entity/DTO
- DB
- 상태 전이
- 가격 권한

금지:

- UI 문구 결정
- 브라우저 TTS 실행
- React state 책임
