# Inventory and Sold-out Policy

> Status: Current

## 1. Policy Matrix

| Target | Result |
|---|---|
| Menu direct sold-out | 해당 메뉴 주문 불가 |
| CORE ingredient sold-out | 연결 메뉴 품절 |
| BASE ingredient sold-out | 해당 베이스를 필수로 쓰는 메뉴 품절 |
| STANDARD ingredient sold-out | 제거 가능하면 메뉴 유지 + 안내 |
| OPTIONAL ingredient sold-out | 해당 옵션만 disabled |
| Option Item sold-out | 해당 옵션만 disabled |
| Required Option Group 전체 품절 | 메뉴 품절 |

---

## 2. CORE Ingredient

예:

- 닭가슴살이 메뉴 정체성의 핵심
- 연어가 핵심 재료

품절 시 메뉴 자체를 판매할 수 없으므로 derived sold-out.

---

## 3. BASE Ingredient

베이스 품절 정책은 메뉴 구조에 따라 달라진다.

### 메뉴가 단일 베이스에 의존

메뉴 품절.

### 여러 베이스 중 선택

해당 베이스만 disabled.

모든 베이스가 품절이면 메뉴 품절.

---

## 4. STANDARD Ingredient

기본 포함 재료가 품절이어도:

- 제거 가능
- 메뉴 정체성에 영향 없음

이면 메뉴 판매 유지 가능.

Kiosk에서는:

```text
현재 양파는 제공되지 않습니다.
```

같은 안내 가능.

---

## 5. OPTIONAL Ingredient

옵션만 disabled.

메뉴 전체 품절로 전파하지 않는다.

---

## 6. Required Option Group

필수 그룹의 활성 option 수가 minimumSelection보다 적으면 메뉴 품절.

예:

```text
minimumSelection = 1
activeOptions = 0
```

→ 메뉴 품절.

---

## 7. Recovery Policy

품절 해제 시:

### direct sold-out

관리자가 직접 해제해야 한다.

### derived sold-out

원인이 모두 해제되면 자동 복구 가능.

단, direct sold-out이 true면 계속 품절.

---

## 8. Display Policy

### Kiosk

- 메뉴 품절: badge + card disabled
- 옵션 품절: option disabled
- 일부 재료 미제공: 안내
- 숨김 메뉴: 노출하지 않음

### Admin

- 직접 품절
- 영향 품절
- 원인
- 영향 메뉴 수

를 구분한다.

---

## 9. Implementation Checklist

- [ ] ingredient role
- [ ] direct/derived distinction
- [ ] required option group rule
- [ ] recovery rule
- [ ] affected menus
- [ ] Kiosk badge
- [ ] Admin explanation
