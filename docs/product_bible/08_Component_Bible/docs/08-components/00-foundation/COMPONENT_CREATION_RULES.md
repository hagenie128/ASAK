# Component Creation Rules

새 컴포넌트를 만들기 전 아래를 확인한다.

1. 기존 동일 역할 컴포넌트가 있는가?
2. props 확장으로 해결 가능한가?
3. variant 추가로 해결 가능한가?
4. Figma component set에 이미 존재하는가?
5. Kiosk/Admin 중 한쪽에 동일 역할이 있는가?
6. 단일 화면에서만 사용하는 markup인가?

## 만들지 말아야 할 중복 예

```text
BottomCTA ↔ FooterButton ↔ PaymentFooter
MenuCard ↔ FoodCard ↔ ProductCard
StatusBadge ↔ StatusChip ↔ StateBadge
ConfirmDialog ↔ DeleteModal ↔ WarningPopup
SalesMetricCard ↔ KpiCard ↔ DashboardMetricCard
```

## 기존 코드 보호

기존 팀원이 만든 컴포넌트가 있으면:

- 이름만 다르다고 새로 만들지 않는다.
- 먼저 props와 책임을 확인한다.
- 필요한 기능만 추가한다.
- 대규모 rename은 별도 승인 후 진행한다.
