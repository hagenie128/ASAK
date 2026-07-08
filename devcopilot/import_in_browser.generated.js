/**
 * DevCopilot 시나리오 일괄 입력 스크립트
 *
 * 사용법:
 * 1. https://devcopilot.ai.kr/workspace/2/scenarios 에 로그인(Admin)
 * 2. F12 → Console 탭
 * 3. 이 파일 전체를 복사해서 붙여넣고 Enter
 * 4. importAllScenarios() 실행 (또는 importMvpOnly() 로 MVP만)
 *
 * 주의: 진행 중 브라우저 탭을 닫지 마세요.
 */

const SCENARIOS = [
  {
    "scenarioId": "SC-001",
    "title": "신규 고객의 기본 주문 흐름",
    "preCondition": "ASAK 키오스크 화면 진입(처음 방문 고객)",
    "postCondition": "결제 완료 후 주문번호가 화면에 표시됨",
    "normalFlow": "홈 → 먹고가기/포장 → 카테고리·메뉴 선택 → 옵션 선택 → 장바구니(SCR-005) → 주문 확인(SCR-006) → 결제(SCR-007) → 주문 완료(SCR-008)",
    "alternativeFlow": "옵션이 헷갈려 이전 단계로 돌아가도 선택 내용이 유지됨 (사용자가 지적한 키오스크 취소 시 초기화 문제 개선)",
    "mermaid": "flowchart TD\n    A[홈 SCR-001] --> B[먹고가기/포장 SCR-002]\n    B --> C[메뉴 선택 SCR-003]\n    C --> D[옵션 선택 SCR-004]\n    D --> E[장바구니 SCR-005]\n    E --> F[주문 확인 SCR-006]\n    F --> G[결제 SCR-007]\n    G --> H[주문 완료 SCR-008]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-002",
    "title": "재방문 고객의 빠른 주문(속도 중심)",
    "preCondition": "재방문 고객이 키오스크 사용 시작",
    "postCondition": "결제 완료 및 주문번호 표시, 화면 전환 5회 이내 목표 (2026-07-05 수정: 4단계→5회, 주문확인 화면 반영)",
    "normalFlow": "메뉴 선택 → 추천조합 기본값 → 장바구니(SCR-005) → 주문 확인(SCR-006) → 결제(SCR-007) → 완료(SCR-008)",
    "alternativeFlow": "없음",
    "mermaid": "flowchart TD\n    A[메뉴 선택 SCR-003] --> B[추천조합 기본값 SCR-004]\n    B --> C[장바구니 SCR-005]\n    C --> D[주문 확인 SCR-006]\n    D --> E[결제 SCR-007]\n    E --> F[완료 SCR-008]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-003",
    "title": "품절 판매 항목이 포함된 상황에서의 주문",
    "preCondition": "관리자가 특정 재료 또는 옵션 항목을 품절 처리한 상태",
    "postCondition": "고객이 품절되지 않은 항목으로 주문 진행",
    "normalFlow": "품절된 판매 항목은 회색 처리된 채 SOLD OUT 표시됨 → 선택 불가 → 고객이 다른 항목으로 대체 선택",
    "alternativeFlow": "핵심 재료 또는 베이스 재료가 품절된 경우 해당 메뉴 또는 관련 카테고리 메뉴가 품절 표시됨",
    "mermaid": "flowchart TD\n    A[관리자 품절 처리 SCR-011] --> B[메뉴/옵션 SOLD OUT 표시 SCR-003, SCR-004]\n    B --> C[고객 선택 불가 SCR-003, SCR-004]\n    C --> D[다른 항목으로 대체 선택 SCR-003, SCR-004]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-004",
    "title": "결제 성공 흐름(수단 노출 포함)",
    "preCondition": "장바구니에 1개 이상 메뉴가 담겨있음",
    "postCondition": "결제 승인 완료 및 주문번호 표시",
    "normalFlow": "장바구니(SCR-005) → 주문 확인(SCR-006) → API-005 주문 생성 → 결제(SCR-007) → 승인 → 주문 완료(SCR-008)",
    "alternativeFlow": "없음(정상 흐름)",
    "mermaid": "flowchart TD\n    A[장바구니 SCR-005] --> B[주문 확인 SCR-006]\n    B --> C[API-005 주문 생성]\n    C --> D[결제 SCR-007]\n    D --> E{결제 승인?}\n    E -->|성공| F[주문 완료 SCR-008]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-005",
    "title": "결제 실패 흐름",
    "preCondition": "결제 진행 중",
    "postCondition": "재시도 성공 또는 직원 호출 안내",
    "normalFlow": "결제 진행 → 승인 실패 응답 수신(금액 불일치/주문 만료 등) → 실패 원인 화면 안내 → 결제 재시도 유도",
    "alternativeFlow": "장바구니 내용은 유지되며 사용자가 다시 결제를 시도할 수 있음",
    "mermaid": "flowchart TD\n    A[결제 SCR-007] --> B{결제 승인?}\n    B -->|실패| C[결제 실패 SCR-012]\n    C --> D[장바구니 유지 SCR-005]\n    D --> E[결제 재시도 SCR-007]\n    E --> A",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-006",
    "title": "멤버십 스탬프 1회 확인 후 자동 적립",
    "preCondition": "결제 단계 진입",
    "postCondition": "결제완료 화면에 적립 여부가 표시됨(결제 전/후 이중 확인 없음)",
    "normalFlow": "결제 진행 중 멤버십 적립 여부 1회 확인 → 결제 완료 시 자동 적립 처리 → 결제완료 화면에 적립 결과 표시",
    "alternativeFlow": "멤버십 미가입 고객은 적립 단계 생략하고 바로 결제 진행",
    "mermaid": "flowchart TD\n    A[결제 SCR-007] --> B[적립 확인 SCR-021 1회 노출]\n    B --> C[결제 완료 SCR-008]\n    C --> D[적립 결과 자동 표시]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-007",
    "title": "관리자의 판매 항목 품절 처리",
    "preCondition": "재료 또는 메뉴 구성 항목 소진으로 품절 발생",
    "postCondition": "키오스크 화면에 판매 항목 품절 상태가 반영됨",
    "normalFlow": "관리자 품절 관리 화면 진입(Week 5 MVP에서는 인증 없이 바로 접근) → 품절 처리할 메뉴/재료 선택 → 품절 토글 ON → 관련 메뉴 목록/메뉴 상세/옵션 선택 화면에 즉시 반영",
    "alternativeFlow": "같은 재료가 기본 구성과 추가 토핑에 모두 쓰이면 메뉴/상세/옵션 품절 상태에 함께 반영됨",
    "mermaid": "flowchart TD\n    A[품절 관리 SCR-011 토글 ON] --> B[메뉴/옵션 표시 갱신 SCR-003, SCR-004]\n    B --> C[고객 화면 즉시 반영]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-008",
    "title": "관리자의 주문 상태 관리",
    "preCondition": "고객이 결제를 완료함",
    "postCondition": "주문 상태가 완료로 변경되고 관리자 화면에 반영됨",
    "normalFlow": "주문 접수 → 관리자 주문 목록에 노출 → 주문 상세 확인 → 준비중으로 상태 변경 → 조리 완료 후 완료로 변경",
    "alternativeFlow": "없음",
    "mermaid": "flowchart TD\n    A[고객 결제 완료 SCR-008] --> B[관리자 주문 목록 SCR-009]\n    B --> C[주문 상세 SCR-010]\n    C --> D[준비중으로 변경 API-008]\n    D --> E[완료로 변경 API-008]\n    E --> F[매장/포장 구분 표시 SCR-010]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-009",
    "title": "장바구니 수정(수량변경/삭제)",
    "preCondition": "장바구니에 1개 이상 메뉴가 담겨있음",
    "postCondition": "수정된 내용이 즉시 반영됨",
    "normalFlow": "장바구니 진입 → 담은 항목 수량 -/+ 조정 → 특정 항목 삭제 → 총금액 자동 재계산",
    "alternativeFlow": "마지막 1개 삭제 시 장바구니 빈 상태로 메뉴선택 화면으로 유도",
    "mermaid": "flowchart TD\n    A[장바구니 진입 SCR-005] --> B[수량 -/+ 조정 SCR-005]\n    B --> C[개별 항목 삭제 SCR-005]\n    C --> D[총금액 자동 재계산 SCR-005]\n    C -->|마지막 1개 삭제| E[메뉴선택 유도 SCR-003]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-010",
    "title": "알레르기/비건 태그 확인 후 주문",
    "preCondition": "견과류 알레르기가 있는 고객이 메뉴 탐색 중",
    "postCondition": "고객이 안전하게 메뉴를 선택하거나 회피함",
    "normalFlow": "알레르기/비건 태그 확인 → 해당 재료 포함 여부 인지 → 태그 기준으로 메뉴 선택/회피",
    "alternativeFlow": "태그 미표시 재료가 있을 경우 고객이 직접 문의하도록 안내 문구 필요",
    "mermaid": "flowchart TD\n    A[메뉴/옵션 선택 SCR-003, SCR-004] --> B[알레르기/비건 태그 확인]\n    B --> C{해당 재료 포함?}\n    C -->|예| D[메뉴 회피 또는 옵션 조정]\n    C -->|아니오| E[정상 진행]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-011",
    "title": "재료 제외(-) 옵션으로 커스텀 주문",
    "preCondition": "특정 재료를 못 먹는 고객이 옵션선택 단계 진입",
    "postCondition": "장바구니/주문서에 제외 재료가 명시됨",
    "normalFlow": "기본 포함 재료 중 특정 항목 \"빼기\" 선택 → 가격 변동 없이 장바구니에 반영 → 주문서에 제외 항목 표시",
    "alternativeFlow": "없음(가격 차감 로직 없음을 명확히 확인, 선생님 피드백 6번 반영)",
    "mermaid": "flowchart TD\n    A[기본 포함 재료 확인 SCR-004] --> B[특정 재료 '빼기' 선택 SCR-004]\n    B --> C[가격 변동 없이 반영]\n    C --> D[장바구니/주문서 제외 항목 표시 SCR-005, SCR-006]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-012",
    "title": "일정시간 미입력 시 자동 초기화",
    "preCondition": "주문 진행 중 고객이 자리를 비움",
    "postCondition": "초기화면으로 전환되고 다음 고객이 깨끗한 상태로 이용 가능",
    "normalFlow": "고객이 주문 진행 중 자리를 뜨 → 일정시간(예 30초) 동안 입력 없음 → 경고 없이 초기화면으로 자동 복귀 → 장바구니 초기화",
    "alternativeFlow": "타임아웃 직전 다시 터치하면 타이머 리셋(앞팀 사례 참고)",
    "mermaid": "flowchart TD\n    A[주문 진행 중 입력 없음] --> B{일정시간 경과?}\n    B -->|예| C[초기화면 자동 복귀 SCR-001]\n    B -->|아니오| D[대기 지속]\n    C --> E[장바구니 초기화 SCR-005]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-013",
    "title": "접근성 옵션으로 저시력 고객 주문",
    "preCondition": "저시력 고객이 키오스크 이용 시작",
    "postCondition": "안내 없이 주문 완료(성공기준 첫방문고객 기준과 동일)",
    "normalFlow": "저시력 고객이 초기화면 진입 → 글자크기 확대 옵션 인지 → 큰 글자/높은 대비로 메뉴 탐색 → 주문 완료",
    "alternativeFlow": "없음",
    "mermaid": "flowchart TD\n    A[저시력 고객 진입 SCR-001] --> B[접근성 설정 SCR-014]\n    B --> C[큰 글자/고대비 메뉴 탐색 SCR-003~SCR-008]\n    C --> D[안내 없이 주문 완료 SCR-008]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-014",
    "title": "매장/포장 여부 선택",
    "preCondition": "홈 화면에서 주문시작 버튼 클릭",
    "postCondition": "주문에 orderType(EAT_IN/TAKE_OUT) 구분값이 저장되어 장바구니로 이동",
    "normalFlow": "홈 화면에서 주문시작 클릭 → 먹고가기/포장 선택 → 선택값(orderType)을 장바구니와 주문확인 단계까지 유지 → 주문 생성 시 orderType에 반영",
    "alternativeFlow": "선택 없이 다음 단계로 진행 불가(필수 선택)",
    "mermaid": "flowchart TD\n    A[홈 SCR-001] --> B[주문 시작 클릭]\n    B --> C[먹고가기/포장 SCR-002]\n    C --> D[orderType 유지 SCR-005, SCR-006]\n    D --> E[주문 생성 시 orderType 반영]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-015",
    "title": "영수증 출력 여부 선택",
    "preCondition": "결제 승인 완료 직후",
    "postCondition": "영수증 출력 완료 또는 화면 주문번호 표시",
    "normalFlow": "결제 완료 화면에서 영수증 출력 여부 선택 → 출력 선택 시 모의 프린터 요청 → 미선택 시 화면 주문번호로 대체",
    "alternativeFlow": "프린터 오류 시 화면 주문번호로 자동 대체",
    "mermaid": "flowchart TD\n    A[주문 완료 SCR-008] --> B{영수증 출력? SCR-020}\n    B -->|예| C[API-019 모의 프린터 요청]\n    B -->|아니오| D[화면 주문번호 표시]\n    C --> E[출력 결과 확인]\n    E --> D",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-016",
    "title": "QR/바코드로 쿠폰 인식 후 결제",
    "preCondition": "고객이 모바일 쿠폰을 보유하고 있음",
    "postCondition": "할인 적용된 금액으로 결제 완료",
    "normalFlow": "결제 단계 진입 → 모바일 쿠폰/멤버십 바코드 스캔 → 할인 자동 적용 → 잔액 결제 진행",
    "alternativeFlow": "스캔 실패/만료된 쿠폰 시 오류 메시지 안내 후 일반결제로 진행",
    "mermaid": "flowchart TD\n    A[결제 단계 SCR-007] --> B[모바일 쿠폰 QR/바코드 스캔 SCR-021]\n    B --> C{유효 코드?}\n    C -->|예| D[할인 자동 적용]\n    C -->|아니오| E[오류 안내 후 일반결제 진행]\n    D --> F[잔액 결제]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-017",
    "title": "관리자의 신규 메뉴 등록",
    "preCondition": "관리자가 신규 메뉴를 추가하려는 상황",
    "postCondition": "신규 메뉴가 키오스크 메뉴선택 화면에 즉시 노출",
    "normalFlow": "관리자 로그인 → 신규 메뉴 등록(이름/가격/이미지/카테고리) → 옵션그룹 연결 → 저장",
    "alternativeFlow": "필수값 누락 시 저장 불가 안내",
    "mermaid": "flowchart TD\n    A[관리자 로그인 SCR-015] --> B[메뉴 관리 SCR-016]\n    B --> C[신규 메뉴 등록 SCR-017: 이름/가격/이미지/카테고리]\n    C --> D[옵션그룹 연결]\n    D --> E[저장 → 키오스크 메뉴 SCR-003 즉시 노출]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-018",
    "title": "관리자의 일별 매출 조회",
    "preCondition": "관리자가 매출 현황을 확인하려는 상황",
    "postCondition": "기간별 매출/판매량이 화면에 표시됨",
    "normalFlow": "관리자 로그인 → 기간 선택 → 일별 매출/메뉴별 판매량 조회",
    "alternativeFlow": "해당 기간에 데이터가 없을 경우 공백 상태 안내",
    "mermaid": "flowchart TD\n    A[관리자 로그인 SCR-015] --> B[기간 선택 SCR-019]\n    B --> C[일별 매출/메뉴별 판매량 조회 SCR-019]\n    C --> D{데이터 존재?}\n    D -->|없음| E[공백 상태 안내 SCR-019]\n    D -->|있음| F[표/그래프 표시 SCR-019]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-019",
    "title": "피크타임 다중 주문 동시처리",
    "preCondition": "점심시간대 다수 고객 동시 접근 가정",
    "postCondition": "동시 요청이 목표 응답시간 내에 처리됨",
    "normalFlow": "동일 시간대에 여러 고객이 동시에 메뉴 조회/주문 진행 → 응답 지연 없이 처리",
    "alternativeFlow": "부하 증가 시 응답 지연이 발생하면 로딩 인디케이터로 안내",
    "mermaid": "flowchart TD\n    A[점심시간 다수 고객 동시 접속] --> B[메뉴조회/주문 동시 요청]\n    B --> C{응답 목표시간 이내?}\n    C -->|예| D[정상 처리]\n    C -->|아니오| E[로깅 및 지연 안내]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-020",
    "title": "드레싱 별도포장 추가 주문",
    "preCondition": "옵션선택 단계에서 드레싱을 하나 더 맛보고 싶은 고객",
    "postCondition": "장바구니에 기본 드레싱과 별도포장 드레싱이 각각 표시됨",
    "normalFlow": "기본 드레싱 선택 → 드레싱 별도포장 추가 선택(균일가) → 장바구니에 드레싱 2개(기본+추가) 반영 → 주문서에 별도포장 표시",
    "alternativeFlow": "없음",
    "mermaid": "flowchart TD\n    A[기본 드레싱 선택 SCR-004] --> B[별도포장 드레싱 추가 선택 SCR-004]\n    B --> C[장바구니에 드레싱 2개 표시 SCR-005]\n    C --> D[주문서에 별도포장 안내 SCR-006]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-021",
    "title": "토핑 개별 수량 조절 주문",
    "preCondition": "특정 토핑(예: 에그)을 더 많이 원하는 고객이 토핑선택 단계 진입",
    "postCondition": "선택한 수량만큼 장바구니에 가격이 반영됨",
    "normalFlow": "토핑 목록에서 특정 토핑 + 버튼으로 수량 증가 → 가격이 수량만큼 배수로 자동 재계산 → 같은 토핑을 최대 5개까지 중복 담을 수 있음",
    "alternativeFlow": "최대치 도달 시 + 버튼 비활성화 및 안내",
    "mermaid": "flowchart TD\n    A[토핑 선택 SCR-004] --> B[+ 버튼으로 수량 증가 SCR-004]\n    B --> C[가격 수량만큼 자동 재계산 SCR-005]\n    C --> D{최대 5개 도달?}\n    D -->|예| E[버튼 비활성화 안내 SCR-004]\n    D -->|아니오| F[계속 담기 가능 SCR-005]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-022",
    "title": "관리자의 주문서 추가/제외 재료 확인",
    "preCondition": "커스텀 옵션이 포함된 주문이 접수된 상황",
    "postCondition": "관리자가 선택 옵션과 제외 재료를 구분해 조리 준비할 수 있음",
    "normalFlow": "커스텀 옵션이 포함된 주문 생성 → 관리자 주문 목록에서 해당 주문 선택 → 주문 상세에서 선택 옵션과 제외 재료 확인 → 조리 준비",
    "alternativeFlow": "없음",
    "mermaid": "flowchart TD\n    A[커스텀 옵션 포함 주문 접수 SCR-008] --> B[관리자 주문목록 SCR-009]\n    B --> C[추가 재료 강조 SCR-010]\n    C --> D[제외 재료 강조 SCR-010]\n    D --> E[조리 준비]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-023",
    "title": "핵심 API 응답속도 검증",
    "preCondition": "개발 완료 후 부하테스트 진행 시점",
    "postCondition": "각 API가 명시된 목표 응답시간 내에 응답함",
    "normalFlow": "메뉴목록/옵션조회/결제 각 API 호출 → 목표 응답시간(2초/1초/3초) 내 응답 확인",
    "alternativeFlow": "목표시간 초과 시 병목 구간(DB 인덱스, 쿼리문) 점검",
    "mermaid": "flowchart TD\n    A[개발 완료 후 부하테스트] --> B[메뉴목록 API-001 - 목표 2초]\n    B --> C[옵션조회 API-004 - 목표 1초]\n    C --> D[결제 API-006 - 목표 3초]\n    D --> E{목표시간 내 응답?}\n    E -->|아니오| F[병목 구간 점검]",
    "status": "DRAFT"
  },
  {
    "scenarioId": "SC-024",
    "title": "최종 통합 리허설에서 주문-결제-관리자 확인",
    "preCondition": "1차 발표 또는 최종 발표 전 전체 데모 환경이 준비되어 있음",
    "postCondition": "고객 주문 완료와 관리자 주문 확인/상태 변경까지 한 번에 시연 가능",
    "normalFlow": "1. 홈(SCR-001) 주문 시작 → 2. 먹고가기/포장(SCR-002) → 3. 메뉴·옵션(SCR-003/004) → 4. 장바구니·주문확인(SCR-005/006) → 5. 결제(SCR-007) → 6. 완료(SCR-008) → 7. 관리자 주문 확인·상태변경(SCR-009/010)",
    "alternativeFlow": "결제 실패, 품절 항목 포함, 필수 옵션 미선택, 관리자 상태 변경 실패 시 해당 화면과 API 오류 응답을 기준으로 재시도 또는 오류 안내를 확인한다.",
    "mermaid": "flowchart TD\n    A[홈 SCR-001] --> B[먹고가기/포장 SCR-002]\n    B --> C[메뉴·옵션 SCR-003/004]\n    C --> D[장바구니·주문확인 SCR-005/006]\n    D --> E[결제 SCR-007]\n    E --> F[완료 SCR-008]\n    F --> G[관리자 확인 SCR-009/010]",
    "status": "DRAFT"
  }
];

async function loadScenariosFromJson() {
  // scenarios_import.json 내용을 아래 배열에 붙여넣거나,
  // 로컬에서 fetch로 불러올 수 없으므로 generate_browser_script.py 로 재생성하세요.
  throw new Error(
    "SCENARIOS 데이터가 비어 있습니다. python devcopilot/generate_browser_script.py 를 실행한 뒤\n" +
      "생성된 import_in_browser.generated.js 를 사용하세요."
  );
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function setReactInputValue(el, value) {
  if (!el) return false;
  const proto =
    el.tagName === "TEXTAREA"
      ? window.HTMLTextAreaElement.prototype
      : window.HTMLInputElement.prototype;
  const setter = Object.getOwnPropertyDescriptor(proto, "value")?.set;
  if (setter) setter.call(el, value);
  else el.value = value;
  el.dispatchEvent(new Event("input", { bubbles: true }));
  el.dispatchEvent(new Event("change", { bubbles: true }));
  el.dispatchEvent(new Event("blur", { bubbles: true }));
  return true;
}

function findFieldByLabel(partialLabel) {
  const labels = [...document.querySelectorAll("label")];
  const label = labels.find((l) =>
    l.textContent.replace(/\s+/g, " ").trim().includes(partialLabel)
  );
  if (!label) return null;

  if (label.htmlFor) {
    const byId = document.getElementById(label.htmlFor);
    if (byId) return byId;
  }

  const container = label.closest("div")?.parentElement || label.parentElement;
  const input = container?.querySelector("input, textarea, select");
  if (input) return input;

  return label.parentElement?.querySelector("input, textarea, select") || null;
}

function clickButtonByText(...texts) {
  const buttons = [...document.querySelectorAll("button, a, [role='button']")];
  const btn = buttons.find((b) => {
    const t = b.textContent.replace(/\s+/g, " ").trim();
    return texts.some((x) => t === x || t.includes(x));
  });
  if (btn) {
    btn.click();
    return true;
  }
  return false;
}

async function fillScenarioForm(scenario) {
  const fields = [
    ["시나리오 ID", scenario.scenarioId],
    ["시나리오 제목", scenario.title],
    ["시작 조건", scenario.preCondition],
    ["종료 조건", scenario.postCondition],
    ["기본 흐름", scenario.normalFlow],
    ["예외 흐름", scenario.alternativeFlow],
    ["Mermaid", scenario.mermaid],
  ];

  for (const [label, value] of fields) {
    const el = findFieldByLabel(label);
    if (!el) {
      console.warn(`[경고] 필드를 찾지 못함: ${label}`);
      continue;
    }
    setReactInputValue(el, value ?? "");
    await sleep(80);
  }

  // 상태 선택 (DRAFT / APPROVED)
  const status = (scenario.status || "DRAFT").toUpperCase();
  const statusButtons = [...document.querySelectorAll("button, label, span")];
  const statusEl = statusButtons.find((el) => {
    const t = el.textContent.replace(/\s+/g, " ").trim();
    return t.includes(status) || t.includes(status === "DRAFT" ? "임시" : "검토완료");
  });
  if (statusEl) statusEl.click();

  await sleep(200);
}

async function saveCurrentScenario() {
  const saved =
    clickButtonByText("저장", "등록", "추가 완료", "Save") ||
    clickButtonByText("확인");
  if (!saved) console.warn("[경고] 저장 버튼을 찾지 못했습니다. 수동으로 저장해 주세요.");
  await sleep(1200);
}

async function importScenarios(scenarios, { startIndex = 0 } = {}) {
  if (!scenarios?.length) {
    console.error("시나리오 데이터가 없습니다.");
    return;
  }

  console.log(`총 ${scenarios.length}개 시나리오 입력 시작 (index ${startIndex})`);

  for (let i = startIndex; i < scenarios.length; i++) {
    const s = scenarios[i];
    console.log(`[${i + 1}/${scenarios.length}] ${s.scenarioId} - ${s.title}`);

    // 새 시나리오 추가
    const added = clickButtonByText("추가", "새 시나리오", "New");
    if (!added) {
      console.error("추가 버튼을 찾지 못했습니다. 시나리오 목록 탭이 열려 있는지 확인하세요.");
      break;
    }
    await sleep(800);

    await fillScenarioForm(s);
    await saveCurrentScenario();
    await sleep(500);
  }

  console.log("완료!");
}

// MVP 우선 시나리오 ID (10일 MVP 기준)
const MVP_IDS = new Set([
  "SC-001", "SC-002", "SC-003", "SC-004", "SC-005",
  "SC-007", "SC-008", "SC-009", "SC-012", "SC-014",
]);

async function importAllScenarios(data) {
  const list = data || (typeof SCENARIOS !== "undefined" && SCENARIOS) || null;
  if (!list) await loadScenariosFromJson();
  return importScenarios(list);
}

async function importMvpOnly(data) {
  const list = (data || SCENARIOS || []).filter((s) => MVP_IDS.has(s.scenarioId));
  return importScenarios(list);
}

console.log(
  "DevCopilot import 준비됨.\n" +
    "- 전체: importAllScenarios(SCENARIOS)\n" +
    "- MVP만: importMvpOnly(SCENARIOS)\n" +
    "※ SCENARIOS 변수에 JSON 배열을 먼저 붙여넣거나 generated 파일을 사용하세요."
);


// 자동 생성됨 — 바로 실행:
// importAllScenarios()
// importMvpOnly()
