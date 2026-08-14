# Accessibility Rules and QA

## 터치
- 최소 80×80px
- 주요 CTA 100~120px
- 작은 아이콘만으로 핵심 행동 제공 금지

## 대비
- 오류·성공·선택은 색상 외 아이콘·문구 병행
- disabled도 상태를 식별 가능하게 유지

## 포커스
- Admin은 keyboard focus 제공
- Kiosk도 focus outline을 제거하지 않음

## 오류
- 관련 입력 위치와 연결
- 해결 방법 포함
- 사용자를 탓하지 않음

## QA
- [ ] 고대비에서 모든 텍스트 식별
- [ ] 글자 확대 시 overflow 없음
- [ ] Bottom CTA 가림 없음
- [ ] Modal clipping 없음
- [ ] 색상 없이 상태 구분
- [ ] 확대 후 뒤로가기 가능
