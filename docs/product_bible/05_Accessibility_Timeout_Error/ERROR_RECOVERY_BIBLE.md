# Error Recovery Bible

> Status: `Canonical`
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `ERROR_CODE_AND_COPY_MAP.md`
- `ERROR_EDGE_CASE_AND_QA.md`
- `ERROR_RECOVERY_ARCHITECTURE.md`

---

## 원문: `ERROR_CODE_AND_COPY_MAP.md`

### Error Code and Copy Map

| Error Code | User Copy | Primary Action |
|---|---|---|
| MENU_NOT_FOUND | 메뉴 정보를 찾을 수 없어요. | 메뉴로 |
| MENU_SOLD_OUT | 선택한 메뉴가 품절되었어요. | 다른 메뉴 보기 |
| OPTION_ITEM_SOLD_OUT | 선택한 옵션이 품절되었어요. | 옵션 수정 |
| INVALID_OPTION_SELECTION | 필수 옵션을 확인해주세요. | 옵션 확인 |
| ORDER_PRICE_CHANGED | 메뉴 가격이 변경되었어요. | 변경 금액 확인 |
| ORDER_CREATE_FAILED | 주문을 생성하지 못했어요. | 다시 시도 |
| PAYMENT_FAILED | 결제가 완료되지 않았어요. | 다시 결제 |
| PAYMENT_METHOD_DISABLED | 현재 이용할 수 없는 결제수단이에요. | 다른 수단 선택 |
| NETWORK_ERROR | 네트워크 연결을 확인해주세요. | 다시 시도 |
| SESSION_EXPIRED | 이용 시간이 지나 처음 화면으로 돌아갑니다. | 처음으로 |

#### Admin
| Error Code | Admin Copy |
|---|---|
| ORDER_STATUS_CONFLICT | 다른 화면에서 주문 상태가 변경되었습니다. |
| SAVE_FAILED | 변경사항을 저장하지 못했습니다. 다시 시도해주세요. |
| PARTIAL_LOAD_FAILED | 일부 데이터를 불러오지 못했습니다. |
| TTS_NOT_SUPPORTED | 이 브라우저에서는 음성 호출을 지원하지 않습니다. |

---

## 원문: `ERROR_EDGE_CASE_AND_QA.md`

### Error Edge Cases and QA

#### Edge Cases
- 네트워크 재연결: 기존 입력 유지 후 retry
- 저장 중 중복 클릭: disabled + loading
- 일부 API 성공: widget별 partial error
- 오래된 응답: request sequence/updatedAt 기준 최신만 적용
- 서버 오류 후 자동 이동 금지

#### QA
- [ ] error code mapping
- [ ] raw server message 미노출
- [ ] retry 동작
- [ ] draft 유지
- [ ] duplicate submit 차단
- [ ] error focus
- [ ] Toast duration
- [ ] Modal action 명확

---

## 원문: `ERROR_RECOVERY_ARCHITECTURE.md`

### Error Recovery Architecture

> Status: Current

#### 원칙
오류는 기술 메시지가 아니라 다음 행동을 선택할 수 있는 제품 상태다.

#### 오류 분류
```text
VALIDATION
NETWORK
SERVER
BUSINESS
PAYMENT
SESSION
UNSUPPORTED
```

#### Kiosk
- Menu Load Error: 다시 시도 / 처음으로
- Menu Detail Validation: 선택 유지 + 해당 옵션 안내
- Cart Validation: 품절 항목 강조 + 수정/삭제
- Order Create Error: Cart 유지 + 다시 시도
- Payment Error: 다시 결제 / 다른 수단 / Cart
- Timeout: 계속 주문 / 처음으로

#### Admin
- page retry
- widget partial error
- save rollback
- Toast
- unsaved draft 유지

#### Error Response Draft
```json
{
  "success": false,
  "message": "OPTION_ITEM_SOLD_OUT",
  "data": {
    "field": "selectedOptionItemIds",
    "targetId": 101,
    "canRetry": true
  }
}
```

#### 공통 React 구조
```text
ErrorState
InlineError
Toast
ConfirmDialog
useApiError
errorMessageMap
```

#### 금지
- alert() 남용
- 서버 원문 노출
- 오류 후 무조건 Home 이동
- 사용자 입력 즉시 초기화
