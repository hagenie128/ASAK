# Product Bible — 읽는 법 (얇은 안내)

> **MVP 스프린트에서는 Pack README만** 먼저 보세요.  
> 세부 계약·ADR·장문 문서는 **필요할 때만** 엽니다.  
> 문서 진입점: [START_HERE](../START_HERE.md) · Index: [PRODUCT_BIBLE_INDEX](../governance/PRODUCT_BIBLE_INDEX.md)

## 구현 vs 정책

| 구분 | 역할 |
|---|---|
| Product Bible | **목표 정책·계약** (이렇게 만들자) |
| baseline / 구현 맵 / 앱 PLAN | **코드 현실** (지금 이렇게 되어 있다) |
| `_archive/` | **구버전** — 구현 기준에서 제외 |

충돌 시: 코드·baseline을 현실로 보고, Bible은 Canonical/갭 문서로 추적합니다.

## 지금 MVP에 중요한 Pack

| Pack | README | 언제 |
|---|---|---|
| **01** Foundation | [README](01_Foundation/README.md) | 결정·정본 충돌 시 |
| **02** Order / Cart / Payment | [README](02_Order_Cart_Payment/README.md) | 키오스크 주문·결제 |
| **03** Menu / Inventory / Sold-out | [README](03_Menu_Inventory_SoldOut/README.md) | 메뉴·품절 |
| **05** Accessibility / Timeout / Error | [README](05_Accessibility_Timeout_Error/README.md) | 타임아웃·오류 (WBS2-027~030) |
| **07** Screen | [README](07_Screen_Bible/README.md) | SCR·라우트 |
| **11** Backend | [README](11_Backend_Implementation/README.md) | P5 슬라이스 시작 시 |
| **12** Frontend | [README](12_Frontend_Implementation/README.md) | Kiosk/Admin 확장 |

참고(필요할 때): **04** 매출·주방·TTS · **06** 엔지니어링 규칙 · **08** 컴포넌트 · **09** QA · **10** AI 거버넌스

## 스프린트에서 건너뛰기 (FUTURE_SCOPE / 후순위)

아래는 **이번 주 MVP 완료 주장에 넣지 마세요.**  
상세: [future-scope.md](../wiki/future-scope.md)

- SCR-023 영수증 실출력 · SCR-024 멤버십/쿠폰  
- 외부 TTS · WebSocket · 고급 차트·예측  
- RTOS/장치 API · CMS 원격 모니터링 · 배달 주문  
- Pack 세부 문서 중 Future로 표시된 항목  
- `product_bible/_archive/**` 전체

## 읽는 짧은 순서

1. [START_HERE](../START_HERE.md) → baseline · WBS  
2. 담당 앱 `IMPLEMENTATION_PLAN` / `STRUCTURE_GUIDE`  
3. 관련 Pack **README만**  
4. Canonical 충돌 시에만 해당 계약 파일 + [CANONICAL_CONTRACT_DECISIONS](../governance/CANONICAL_CONTRACT_DECISIONS.md)

## Pack 1~12 빠른 링크

| # | Pack |
|---|---|
| 01 | [Foundation](01_Foundation/README.md) |
| 02 | [Order / Cart / Payment](02_Order_Cart_Payment/README.md) |
| 03 | [Menu / Inventory / Sold-out](03_Menu_Inventory_SoldOut/README.md) |
| 04 | [Dashboard / Sales / Kitchen / TTS](04_Dashboard_Sales_Kitchen_TTS/README.md) |
| 05 | [Accessibility / Timeout / Error](05_Accessibility_Timeout_Error/README.md) |
| 06 | [Engineering](06_Engineering_Bible/README.md) |
| 07 | [Screen](07_Screen_Bible/README.md) |
| 08 | [Component](08_Component_Bible/README.md) |
| 09 | [QA](09_QA_Bible/README.md) |
| 10 | [AI Master](10_AI_Master_Bible/README.md) |
| 11 | [Backend Implementation](11_Backend_Implementation/README.md) |
| 12 | [Frontend Implementation](12_Frontend_Implementation/README.md) |
