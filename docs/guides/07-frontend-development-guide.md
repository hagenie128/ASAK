# 프론트엔드 개발 가이드 (ASAK-front)

> 이 문서는 ASAK 프론트엔드 구현을 시작할 때 참고할 공통 가이드입니다.  
> 기준 스택: React 19 + Vite 8 + React Router 7 + Zustand + Axios + 일반 CSS / CSS Modules

---

## 1. 프론트엔드 진행 순서

프론트엔드는 아래 순서로 진행하는 것을 권장합니다.

1. 환경 준비
   - Node.js 24 LTS, npm 11.x 설치
   - ASAK-front 저장소 클론
   - 의존성 설치: `npm install`

2. 데이터/환경 준비
   - 백엔드 API 주소 확인
   - `.env` 또는 Vite 환경 변수 설정
   - 메뉴/옵션 데이터가 있다면 프런트가 읽을 수 있는 형태로 연결

3. 공통 레이아웃 구성
   - 전체 페이지 레이아웃
   - 헤더/푸터/네비게이션/공통 버튼 영역
   - 화면 폭·폰트·색상 토큰 정리

4. 라우팅 구조 설계
   - 홈, 메뉴 선택, 옵션 선택, 장바구니, 주문 확인, 결제, 주문 완료 등 흐름 연결
   - SCR 기준 화면별 페이지 분리

5. 핵심 기능 구현
   - 메뉴 목록 조회
   - 옵션 선택 상태 관리
   - 장바구니 계산
   - 주문 요청/결제 흐름

6. 상태 관리 분리
   - 화면 UI 상태와 비즈니스 상태를 구분
   - 장바구니, 주문, 사용자 선택 상태는 Zustand 또는 전역 상태로 정리

7. 연동 및 QA
   - 백엔드 API와 실제 통신 확인
   - 에러/로딩/빈 상태 처리
   - 화면별 동작 검증

8. 리팩터링 및 정리
   - 중복 코드 제거
   - 기능별 모듈 분리
   - 파일명/폴더명/컴포넌트 구조 정리

---

## 2. 권장 프론트 영역 구조

프로젝트가 커질수록 기능 단위로 분리하는 것이 유지보수에 좋습니다.  
아래 구조를 기본 템플릿으로 추천합니다.

```text
src/
  app/
    router/
    providers/
    constants/
  pages/
    HomePage/
    OrderPage/
    CheckoutPage/
    AdminPage/
  features/
    menu-selection/
    cart/
    payment/
    admin-order/
  widgets/
    Header/
    BottomNav/
    Modal/
  entities/
    menu/
    order/
    user/
  shared/
    ui/
    hooks/
    lib/
    styles/
    types/
    utils/
  services/
    api/
    mock/
  stores/
  assets/
    images/
    icons/
```

### 영역별 역할

- `app/`: 앱 전역 설정, 라우팅, 프로바이더
- `pages/`: 라우트 단위 화면
- `features/`: 기능 단위 모듈
- `widgets/`: 여러 페이지에서 재사용되는 UI 블록
- `entities/`: 핵심 데이터 모델과 관련 로직
- `shared/`: 범용 컴포넌트, 훅, 유틸리티
- `services/`: API 호출, mock 데이터, 외부 연동
- `stores/`: Zustand 스토어
- `assets/`: 이미지, 아이콘, 폰트

---

## 3. 패키지명(모듈명) 규칙

실제 npm 패키지명이 아니라, 프론트엔드 내부의 “영역/모듈명” 기준으로 아래 규칙을 권장합니다.

### 3-1. 폴더명(모듈명)

- 기능 단위는 소문자 + 케밥케이스 사용
- 예: `menu-selection`, `order-summary`, `admin-menu`
- 화면 단위는 `HomePage`, `OrderPage`처럼 의미를 바로 알 수 있게 구성

### 3-2. import 경로 기준

- 도메인 중심으로 폴더를 나누고, 내부에서 다시 하위 폴더를 구성
- 예:
  - `features/menu-selection`
  - `features/cart`
  - `shared/ui`

### 3-3. 기능별 예시

- 메뉴 관련: `features/menu-selection`
- 장바구니: `features/cart`
- 결제: `features/payment`
- 관리자 기능: `features/admin-order`

---

## 4. 파일명 규칙

파일명은 역할에 따라 구분하면 혼란이 줄어듭니다.

| 역할       | 권장 규칙                         | 예시                  |
| ---------- | --------------------------------- | --------------------- |
| 컴포넌트   | PascalCase                        | `MenuCard.tsx`        |
| 페이지     | PascalCase + Page                 | `HomePage.tsx`        |
| 훅         | `use` + camelCase                 | `useCart.ts`          |
| 스토어     | `xxxStore.ts`                     | `cartStore.ts`        |
| API 서비스 | `xxxApi.ts` 또는 `xxx.service.ts` | `menuApi.ts`          |
| 타입       | `xxx.types.ts`                    | `menu.types.ts`       |
| 상수       | `xxx.constants.ts`                | `routes.constants.ts` |
| 유틸       | `xxx.util.ts` 또는 `xxx.ts`       | `price.util.ts`       |
| 스타일     | `.module.css` 또는 `.css`         | `MenuCard.module.css` |

### 예시 구조

```text
features/
  menu-selection/
    components/
      MenuCard.tsx
      CategoryTabs.tsx
    hooks/
      useMenuList.ts
    api/
      menuApi.ts
    types/
      menu.types.ts
    index.ts
```

---

## 5. 화면 구현 기준

SCR 기반으로 화면을 나누면 개발 순서가 더 명확해집니다.

### 고객 키오스크 흐름

- 홈 화면
- 먹고가기 / 포장 선택
- 메뉴 선택
- 메뉴 상세 / 옵션 선택
- 장바구니
- 주문 확인
- 결제
- 주문 완료

### 관리자 흐름

- 주문 관리
- 주문 상세
- 품절 관리
- 메뉴 관리
- 결제수단 설정
- 매출 요약

각 화면은 아래처럼 분리하면 좋습니다.

```text
pages/
  HomePage/
  OrderTypePage/
  MenuListPage/
  MenuDetailPage/
  CartPage/
  CheckoutPage/
  PaymentPage/
  CompletePage/
```

---

## 6. 팀 공통 규칙

- 컴포넌트는 한 파일에 너무 많은 책임을 담지 않기
- 페이지는 화면 조립용으로만 사용하고, 로직은 기능 모듈로 분리하기
- 공통 UI는 `shared/ui`로 이동하기
- API 호출은 `services/api` 또는 `features/*/api` 쪽에 모으기
- 상태는 화면 단위보다 기능 단위로 관리하기
- 이름은 “무슨 역할인지 바로 보이게” 짓기

---

## 7. 추천 작업 템플릿

새 기능을 시작할 때는 아래 흐름으로 진행하면 좋습니다.

1. `features/기능명` 폴더 생성
2. `components`, `hooks`, `api`, `types` 하위 폴더 구성
3. 페이지에서 해당 기능 모듈을 조립
4. 공통 UI는 `shared`로 분리
5. 상태와 API 연동 완료 후 리팩터링

예시:

```text
features/cart/
  components/
    CartItem.tsx
    CartSummary.tsx
  hooks/
    useCartStore.ts
  api/
    cartApi.ts
  types/
    cart.types.ts
```

---

## 8. 정리

프론트엔드는 “화면 단위 구현”과 “기능 단위 모듈화”를 함께 쓰는 방식이 가장 깔끔합니다.  
즉, 페이지는 흐름 중심, 기능 폴더는 비즈니스 로직 중심, 공통 컴포넌트는 재사용 중심으로 나누면 팀 협업이 수월해집니다.
