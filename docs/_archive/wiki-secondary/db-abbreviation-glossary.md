# DB Abbreviation Glossary

> Draft — the real backend schema has not been implemented. No table or column rename is authorized by this document.

| Abbreviation | Full Name | Korean Meaning | Used In | Table/Column | Related Requirement | Notes | Confirmation Status |
|---|---|---|---|---|---|---|---|
| `vw` | View | 데이터베이스 뷰 | Modeler | `vw_sales_*`, `vw_top_menu_*` | LMIS-ORDER-005 | Read-model candidate, not a proven backend object | NEEDS_CONFIRMATION |
| `id` | Identifier | 식별자 | Modeler | PK/FK columns | all entity requirements | Keep existing naming | CONFIRMED_CONVENTION |
| `fk` | Foreign Key | 외래 키 | Modeler metadata | relation columns | data requirements | Do not infer missing backend FK from Modeler alone | NEEDS_CONFIRMATION |
| `pk` | Primary Key | 기본 키 | Modeler metadata | `id` columns | data requirements | Do not rename | CONFIRMED_CONVENTION |
| `qty` | Quantity | 수량 | API/UI contract candidate | order/menu payloads | FWD-CART-002 | Actual current fields use `quantity` | NEEDS_CONFIRMATION |
