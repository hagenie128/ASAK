# Error Edge Cases and QA

## Edge Cases
- 네트워크 재연결: 기존 입력 유지 후 retry
- 저장 중 중복 클릭: disabled + loading
- 일부 API 성공: widget별 partial error
- 오래된 응답: request sequence/updatedAt 기준 최신만 적용
- 서버 오류 후 자동 이동 금지

## QA
- [ ] error code mapping
- [ ] raw server message 미노출
- [ ] retry 동작
- [ ] draft 유지
- [ ] duplicate submit 차단
- [ ] error focus
- [ ] Toast duration
- [ ] Modal action 명확
