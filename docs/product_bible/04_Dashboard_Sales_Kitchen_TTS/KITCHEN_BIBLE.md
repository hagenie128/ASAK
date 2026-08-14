# Kitchen Bible

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `KITCHEN_ARCHITECTURE.md`
- `KITCHEN_FLOW_AND_EDGE_CASE.md`

---

## 원문: `KITCHEN_ARCHITECTURE.md`

### Kitchen and Live Order Architecture

> Status: Current
> Figma: SCR-009, SCR-010

#### 1. 화면 역할

##### SCR-009 Live Order Board
- 현재 진행 주문
- 빠른 상태 변경
- 조리 우선순위
- 완료 TTS

##### SCR-010 Order Management
- 검색
- 상태·기간 필터
- 주문 이력
- 상세 조회

실시간 처리 화면과 관리 조회 화면을 분리한다.

#### 2. 상태

```text
RECEIVED
→ PREPARING
→ COMPLETED
```

#### 3. 정렬

기본은 `createdAt ascending`, 오래된 주문 우선.

#### 4. 실시간 갱신

MVP:
```text
5초 polling
```

확장:
- WebSocket
- SSE

#### 5. 상태 변경 원칙

1. 버튼 loading
2. API 요청
3. 성공 후 UI 변경
4. 실패 시 기존 상태 유지 + Toast

운영 상태는 성공 응답 전에 바꾸지 않는 편이 안전하다.

#### 6. TTS Trigger

```text
PREPARING
→ PATCH COMPLETED
→ success
→ Toast
→ TTS
```

Polling이나 새로고침으로 완료 주문을 발견했다고 TTS를 실행하지 않는다.

#### 7. Order Card 정보

- orderNo
- orderType
- createdAt
- elapsed time
- item summary
- quantity
- option/request summary
- current status
- next action

#### 8. 경과시간

```text
now - createdAt
```

예시 정책:
- 10분 이상 warning
- 20분 이상 critical

색상만으로 표현하지 않고 텍스트·아이콘을 병행한다.

#### 9. React Mapping

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

#### 10. API

```http
GET /api/admin/orders/live
GET /api/admin/orders
GET /api/admin/orders/{orderId}
PATCH /api/admin/orders/{orderId}/{status}
```

---

## 원문: `KITCHEN_FLOW_AND_EDGE_CASE.md`

### Kitchen Flow and Edge Cases

#### Main Flow

```text
Payment APPROVED
→ Order RECEIVED
→ Live Order Board
→ PREPARING
→ COMPLETED
→ TTS
→ Dashboard active count 감소
```

매출은 Payment APPROVED 기준으로 집계하고 Order COMPLETED와 혼동하지 않는다.

#### Polling

- 이전 요청이 끝나지 않았으면 새 요청 금지
- unmount 시 interval clear
- 오류 시 기존 카드 제거 금지

#### Edge Cases

##### 상태 변경 중 Polling 충돌
- updatedAt 또는 request timestamp 비교
- 최신 응답 우선

##### 완료 버튼 중복
- loading disabled
- backend idempotent
- TTS duplicate block

##### 다른 관리자가 먼저 완료
- 현재 상태 반환 후 UI 동기화

##### 네트워크 실패
- 기존 카드 유지
- Error Toast

##### 주문 취소
- MVP 포함 전 Live Board action에 넣지 않는다

#### QA

- [ ] oldest first
- [ ] status transition
- [ ] duplicate click
- [ ] polling clear
- [ ] stale response
- [ ] error preserves data
- [ ] completed removed
- [ ] TTS once
