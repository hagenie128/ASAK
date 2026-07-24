# DB Abbreviation Glossary

> 초안 — 실제 backend schema는 아직 구현되지 않았습니다. 이 문서만으로 table·column 이름 변경은 승인되지 않습니다.

| Abbreviation | Full Name | Korean Meaning | Used In | Table/Column | Related Requirement | Notes | Confirmation Status |
|---|---|---|---|---|---|---|---|
| `vw` | View | 데이터베이스 뷰 | Modeler | `vw_menu_*`, `vw_order_*`, `vw_sales_*`, `vw_top_menu_*` | LMIS-ORDER-005 외 | 읽기 모델(read model). 정의: `docs/wiki/db-view-definition.md`, DDL: `ASAK-back/docs/view.sql` | CONFIRMED |
| `id` | Identifier | 식별자 | Modeler | PK/FK columns | all entity requirements | 기존 명명 유지 | CONFIRMED_CONVENTION |
| `fk` | Foreign Key | 외래 키 | Modeler metadata | relation columns | data requirements | Modeler만으로 backend FK 누락 추론 금지 | NEEDS_CONFIRMATION |
| `pk` | Primary Key | 기본 키 | Modeler metadata | `id` columns | data requirements | 이름 변경 금지 | CONFIRMED_CONVENTION |
| `qty` | Quantity | 수량 | API/UI contract candidate | order/menu payloads | FWD-CART-002 | 현재 실제 필드는 `quantity` 사용 | NEEDS_CONFIRMATION |
