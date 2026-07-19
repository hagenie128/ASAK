# 먹고가기/포장 선택 및 orderType 유지 검증

↔ API: 주문 생성 (../../06%20API%20%EB%AA%85%EC%84%B8/API%20%EB%AA%85%EC%84%B8%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4/%EC%A3%BC%EB%AC%B8%20%EC%83%9D%EC%84%B1.md)
↔ 시나리오: 매장/포장 여부 선택 (../../03%20%EC%82%AC%EC%9A%A9%EC%9E%90%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4/%EC%82%AC%EC%9A%A9%EC%9E%90%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4/%EB%A7%A4%EC%9E%A5%20%ED%8F%AC%EC%9E%A5%20%EC%97%AC%EB%B6%80%20%EC%84%A0%ED%83%9D.md)
관련 API: API-005 POST /api/orders (orderType 필드)
관련 화면: SCR-001 홈 (매장·포장)
구분: 화면
기대 결과: 홈(SCR-001)에서 매장(먹고가기)/포장 선택 후 장바구니·주문확인(SCR-005) 컨펌 팝업·주문 생성까지 orderType(EAT_IN/TAKE_OUT)이 유지되고 API-005 요청에 반영된다.
단계: FWD
비고: 2026-07-06: SCR-002→001 병합. 주문확인은 SCR-005 컨펌 팝업.
상태: 예정
수행 절차: 1) 홈(SCR-001)에서 매장(먹고가기) 선택 2) 메뉴 1건 장바구니 담기 3) 장바구니·주문확인(SCR-005)에서 orderType 확인 4) 컨펌 팝업 확인 후 API-005 body의 orderType 확인
오류 발생: N
우선순위: 상
전제조건: 키오스크 홈 화면 접근 가능
테스트 ID: TC-001
테스트 데이터: orderType=EAT_IN, menuId=364