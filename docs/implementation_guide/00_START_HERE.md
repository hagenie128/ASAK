# ASAK 구현 작업대

> **문서를 처음부터 읽지 않는다.** 지금 만들 기능을 골라서 해당 블록만 본다.  
> 이 폴더는 Product Bible을 다시 쓴 문서가 아니라, 구현 중 필요한 정보를 빠르게 찾는 **작업용 인덱스**다.  
> **노트북 이어서:** [핸드오프 2026-07-18](../handoff/LAPTOP_CONTINUE_2026-07-18.md) · 브랜치 `handoff/0718-to-kiosk-continue` · 다음 **SCR-005 장바구니**

## 지금 하는 일 선택

| 지금 만들거나 고칠 것 | 바로 열기 | 그 안에서 바로 확인하는 것 |
| --- | --- | --- |
| 키오스크 메뉴 목록·상세·옵션 | [Kiosk: 메뉴 목록](02_KIOSK_IMPLEMENTATION.md#scr-003--menu-list) | Figma, `GET` URL, 응답 필드, 품절/오류 |
| 키오스크 장바구니·주문 생성 | [Kiosk: 장바구니](02_KIOSK_IMPLEMENTATION.md#scr-005--cart) | request body, 주문 응답, 가격/품절 실패 |
| 키오스크 결제·완료 | [Kiosk: 결제](02_KIOSK_IMPLEMENTATION.md#scr-007--payment) | 결제 request, 성공/실패 응답, 재시도 |
| 키오스크 timeout·접근성 | [Kiosk: Timeout](02_KIOSK_IMPLEMENTATION.md#scr-013--timeout) | 경고/복귀/High Contrast |
| 관리자 실시간 주문·주문 관리 | [Admin: 실시간 주문](03_ADMIN_IMPLEMENTATION.md#scr-009--live-order-board) | 조회/상태 변경, TTS, 충돌 복구 |
| 관리자 품절·메뉴 | [Admin: 품절](03_ADMIN_IMPLEMENTATION.md#scr-011--sold-out-management) | 저장 필드, 품절 영향, 저장 실패 |
| 관리자 결제 수단·매출·대시보드 | [Admin: 대시보드](03_ADMIN_IMPLEMENTATION.md#scr-022--dashboard) | 기간 query, 집계 필드, Empty/Error |
| 영수증·멤버십·쿠폰 확장 | [Extension 화면](07_EXTENSION_IMPLEMENTATION.md) | 출력/스캔 상태, 미확정 API와 보류 기준 |
| API 공통 처리·기존 mock 연결 | [API 공통 규칙](04_API_DB_IMPLEMENTATION.md) | envelope, error, adapter, Backend 진행 상태 |
| UI 컴포넌트/토큰 | [UI 컴포넌트](05_UI_COMPONENT_GUIDE.md) | 기존 컴포넌트 재사용, Figma 상태 |
| Figma 화면 상태를 하나씩 대조 | [상태 체크리스트](09_FIGMA_STATE_CHECKLIST.md) | Default/Loading/Empty/Error/Saving/복구 |
| 코드·정책 상태가 다를 때 | [현재 구현 지도](../planning/CURRENT_IMPLEMENTATION_MAP.md) + [정본 계약](../governance/CANONICAL_CONTRACT_DECISIONS.md) | 실제 코드·route·API 계약 충돌 |
| 테스트·시연 직전 | [QA](06_QA_RELEASE_GUIDE.md) | 화면 상태, P0 시나리오 |

## 작업할 때 보는 순서

1. 위 표에서 **기능 한 개**를 연다.
2. 해당 블록의 Figma 링크에서 Default와 Loading·Empty·Error·Disabled를 본다.
3. 같은 블록의 API 표에서 URL·request·응답 필드만 가져온다.
4. 실제 Kiosk/Admin/Backend 코드에서 기존 route·store·컴포넌트를 찾는다.
5. 블록 하단의 `완료 체크`만 통과시키고 다음 기능으로 넘어간다.

## 공통으로 딱 세 가지만 기억

- 실제 Backend business API는 아직 구현 전이다. 문서의 API는 **목표 계약**이며 mock과 실제 호출을 구분한다.
- 가격·품절·주문 상태 전이는 화면이 확정하지 않는다. 서버 응답을 최종값으로 사용한다.
- `05-C Kiosk`, `06-C Admin`, `07-C QA`가 현재 화면 기준이다. 화면 링크가 연결되어 있다고 구현 완료를 뜻하지는 않는다.
- Screen Registry에는 Kiosk 9개·Admin 10개·Extension 2개가 있다. Figma에는 같은 화면의 세부 상태 프레임이 별도로 있으므로 Default만 구현하고 끝내지 않는다.

## 기준 화면 빠른 링크

> **정본 파일: 0718** (`yHhvn5RKjBd91U8BJUQz7F`). 0715는 Archive(읽기 전용).

| 용도 | Figma |
| --- | --- |
| 파일 구조 확인 | [00-C Cover](https://www.figma.com/design/yHhvn5RKjBd91U8BJUQz7F/ASAK-%E2%80%94-Design-System---Product-UI-0718?node-id=174-8727) |
| 고객 키오스크 | [05-C Screens / Kiosk](https://www.figma.com/design/yHhvn5RKjBd91U8BJUQz7F/?node-id=134-7720) |
| 관리자 | [06-C Screens / Admin](https://www.figma.com/design/yHhvn5RKjBd91U8BJUQz7F/?node-id=134-10606) |
| KEEP 키오스크 | [✅ KEEP — Code Core](https://www.figma.com/design/yHhvn5RKjBd91U8BJUQz7F/?node-id=3006-12340) |
| KEEP 관리자 | [✅ KEEP — Admin Code Core](https://www.figma.com/design/yHhvn5RKjBd91U8BJUQz7F/?node-id=3006-40067) |

<details>
<summary>원본 정책이 서로 다를 때만 열기</summary>

우선순위는 `Decision/ADR → Screen Registry → Feature/API 문서 → 최신 Figma → 실제 코드`다. 실제 코드와 정책이 다르면 임의로 덮어쓰지 말고 차이를 기록한다.

- [Canonical Source](../product_bible/01_Foundation/docs/00-product-bible/CANONICAL_SOURCE.md)
- [Screen Registry](../product_bible/07_Screen_Bible/docs/07-screens/SCREEN_REGISTRY.md)
- [Product Bible Index](../governance/PRODUCT_BIBLE_INDEX.md)
</details>
