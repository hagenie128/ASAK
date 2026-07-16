# Kitchen and Live Order Architecture

> Status: Current  
> Figma: SCR-009, SCR-010

## 1. 화면 역할

### SCR-009 Live Order Board
- 현재 진행 주문
- 빠른 상태 변경
- 조리 우선순위
- 완료 TTS

### SCR-010 Order Management
- 검색
- 상태·기간 필터
- 주문 이력
- 상세 조회

실시간 처리 화면과 관리 조회 화면을 분리한다.

## 2. 상태

```text
RECEIVED
→ PREPARING
→ COMPLETED
```

## 3. 정렬

기본은 `createdAt ascending`, 오래된 주문 우선.

## 4. 실시간 갱신

MVP:
```text
5초 polling
```

확장:
- WebSocket
- SSE

## 5. 상태 변경 원칙

1. 버튼 loading
2. API 요청
3. 성공 후 UI 변경
4. 실패 시 기존 상태 유지 + Toast

운영 상태는 성공 응답 전에 바꾸지 않는 편이 안전하다.

## 6. TTS Trigger

```text
PREPARING
→ PATCH COMPLETED
→ success
→ Toast
→ TTS
```

Polling이나 새로고침으로 완료 주문을 발견했다고 TTS를 실행하지 않는다.

## 7. Order Card 정보

- orderNo
- orderType
- createdAt
- elapsed time
- item summary
- quantity
- option/request summary
- current status
- next action

## 8. 경과시간

```text
now - createdAt
```

예시 정책:
- 10분 이상 warning
- 20분 이상 critical

색상만으로 표현하지 않고 텍스트·아이콘을 병행한다.

## 9. React Mapping

```text
LiveOrderBoardPage
LiveOrderColumn
OrderCard
OrderStatusAction
ElapsedTimeBadge
TtsControl
OrderManagementPage
OrderTable
OrderDetailPanel
FilterBar
```

## 10. API

```http
GET /api/admin/orders/active
GET /api/admin/orders
GET /api/admin/orders/{orderId}
PATCH /api/admin/orders/{orderId}/status
```
