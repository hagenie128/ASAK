# WBS / ?�구?�항 / QA ??DONE·PASS ?��? (2026-08-07)

- 기�?: 코드 ?�측 + Hub ?�격 ?�태 + ?�행 증거 ?�무  
- ?�칙: **코드 ?�음 ??DONE** · **TC 미실????PASS**  
- ?�격 ?�기: ??문서 ?�성 ?�점 **미수??* (?�래 권고�?

## 1. Hub ?�황 ?�약

| 범위 | ?�격 집계 | 비고 |
|---|---|---|
| WBS ?�체 | EXCLUDED 98 / IN_PROGRESS 35 / TODO 19 / DONE 11 / BLOCKED 7 | `wbs_rate` 6.5%??EXCLUDED ?�함 ??지??무시 |
| WBS2 계열 | DONE **6** · IN_PROGRESS 35 · TODO 18 · BLOCKED 7 (+ EXCLUDED 보존) | 로컬 `wbs-v2`?� DONE 집합 ?�치 |
| ?�구?�항 | DONE **0** · IN_PROGRESS ?�수 · TODO · EXCLUDED | `req_rate` 0% |
| QA | 16�?**?��? TODO** · PASS **0** | `qa_rate` 0% |

## 2. ?��? DONE??WBS ???��??�도 ?�는가?

| task | ?�목 ?�약 | ?�정 | 근거 |
|---|---|---|---|
| WBS2-001 | MCP baseline | **DONE ?��?** | 기획/문서 ?�출 |
| WBS2-002 | ?�?�소 ??��/목표 | **DONE ?��?** | ?�출 ?�료 |
| WBS2-009 | Foundation ?�출 | **DONE ?��?** | ?�출 ?�료 |
| WBS2-017 | ?�오?�크 ?�우?�·흐�?| **DONE ?��?** | ?�우???�결 evidence |
| WBS2-022 | 메뉴 ?�량 max 9 | **DONE ?��?** | quantityLimits |
| WBS2-023 | ?�바구니 max 30 | **DONE ?��?** | quantityLimits |
| ?�거??WBS-001~024 ?��? DONE | ERD/?�키�???| **보존** | SUPERSEDED/?�반 DONE ?�재 ???�괄 변�?금�? |

??**?�못 ?�라�?DONE?� ?�음.** 추�?�?DONE ?�릴 ??��??**?�음** (?�합 ?�스????.

## 3. DONE?�로 ?�리�????�는 ?�보 (코드???�으??미�?�?

| ID | Hub ?�태 | 코드 | ??DONE 불�? |
|---|---|---|---|
| WBS2-035 Live | IN_PROGRESS | `GET .../orders/live` 구현 | 브라?��?·?�DB ?�합 미�?�?|
| WBS2-036 주문 목록/?�세 | IN_PROGRESS | Admin GET 구현 · FE ?�동 | ?�일 |
| WBS2-053 주문 조회/?�태 | IN_PROGRESS | PATCH status/cancel 구현 | Bruno/HTTP E2E 미기�?|
| WBS2-048/049 메뉴 GET | IN_PROGRESS | AdminMenu GET(+POST create) | CRUD·FE E2E 미완 |
| LMIS-ORDER-001~003 | IN_PROGRESS | ?��? ?�일 | ?�구?�항 DONE = ?�무 ?�료 주장 ??금�? |
| LMIS-MENU-004 | IN_PROGRESS | GET·POST ?�음, PATCH/DELETE TODO | ?�록/?�정/??�� ?�체 미완 |
| DEV-ORDER-001 | IN_PROGRESS | `POST /orders` 매핑 ?�음 | ?�DB ?�?�·응??검�???|
| DEV-PAY-001 | IN_PROGRESS | `UserPayController` **�?껍데�?* | ?�히??**TODO ?�향** 검??|

## 4. ?�태�?조정 권고 (DONE/PASS ?�님)

| ?�??| ?�재 | 권고 | 근거 |
|---|---|---|---|
| DEV-CART-001 | TODO | ??**IN_PROGRESS** | `POST /api/kiosk/cart/validate` 구현??|
| DEV-ORDER-002 | TODO | ??**IN_PROGRESS** | `PATCH .../cancel` 구현??· ?�합 미�?�?|
| WBS2-037 (?�태 UI·TTS) | TODO | ??**IN_PROGRESS** (?�택) | Live ?�태변�?취소 코드 ?�음 · TTS???�전??stub |
| DEV-PAY-001 | IN_PROGRESS | ??**TODO** (?�택) | Pay Controller 미구??|
| LMIS-MENU-001 ?�절 | IN_PROGRESS | ?��? ?�는 TODO | `AdminSoldOutController` �??�래??|
| LMIS-PAY-001 | IN_PROGRESS | ?��? ?�는 TODO | PaymentMethod Controller ?�텁 |
| LMIS-DASH-001 | TODO | **TODO ?��?** | Stats ?�텁 |
| QA TC-001~016 | TODO | **?��? TODO ?��?** | ?�행 로그/증거 ?�음 ??**PASS 0�?* |
| TC-005/015/016 FUTURE | TODO | PASS 금�? · EXCLUDED/보류 ?��? | 범위 �?|

## 5. QA PASS 가???��?

| TC | PASS? | 조건 |
|---|---|---|
| TC-001 orderType | **불�?(지�?** | Kiosk?�API-005 ?�요�?�DB ?�인 ??|
| TC-014 주문목록·?�태 | **불�?(지�?** | Admin Live/목록/PATCH ?�동+로그 ??|
| TC-010/011 메뉴 | **불�?** | CRUD·?�절 ?�동 ??|
| TC-012/013 결제·매출 | **불�?** | BE ?�텁 |
| ?�머지 | **불�?** | 미실??|

## 6. 권고 ?�션

1. **즉시 ?��? ?�음:** ?�떤 WBS/?�구??DONE, ?�떤 QA??PASS  
2. **?�인 ???�전 갱신�?** DEV-CART-001·DEV-ORDER-002�?TODO?�IN_PROGRESS (�??�택??WBS2-037 / DEV-PAY-001 조정)  
3. **PASS/DONE ?�격:** ?�모???�행 체크리스?�에 ?�짜·?�당·결과 URL/로그�??�긴 ?�에�?개별 ID�?처리  

## 7. 결론

- Hub??**기존 DONE 6�?WBS2)?� ?�??*?�다.  
- **?�로 DONE·PASS ????��?� 0�?*?�다.  
- 진행 중으�?보이??주문/메뉴 조회??**IN_PROGRESS가 ?�답**?�며, 강사 ?�청???�합 ?�스?�·실DB 검증이 ?�나�???DONE ?�격?� ?�위 ?�료가 ?�다.

## 8. Hub �ݿ� (���� ��)

| ��� | ���� | ��� |
|---|---|---|
| DEV-CART-001 | TODO �� IN_PROGRESS | �ݿ� |
| DEV-ORDER-002 | TODO �� IN_PROGRESS | �ݿ� |
| DONE / QA PASS | ���� ���� | ? |
