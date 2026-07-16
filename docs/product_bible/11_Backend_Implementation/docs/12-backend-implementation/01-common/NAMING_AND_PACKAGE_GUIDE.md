# Naming and Package Guide

## 클래스

```text
MenuController
MenuService
MenuRepository
MenuCreateRequest
MenuDetailResponse
```

## 메서드

```text
getMenuList
getMenuDetail
createOrder
updateOrderStatus
calculateTotalAmount
```

## 패키지

현재 scaffold를 우선한다.

권장 예:

```text
com.asak
├─ common
├─ menu
├─ ingredient
├─ option
├─ order
├─ payment
├─ admin
└─ sales
```

전면 이동은 금지한다.
