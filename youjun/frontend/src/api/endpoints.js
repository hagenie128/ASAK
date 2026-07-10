// api/endpoints.js
// 서버 API 주소들을 한곳에 모아 관리하는 파일
// 나중에 백엔드 주소가 바뀌어도 이 파일만 수정하면 됨

export const ENDPOINTS = {
  // ---------- 키오스크 (손님용) ----------
  categories: '/api/categories', // API-001 카테고리 목록 조회
  menus: '/api/menus', // API-002 메뉴 목록 조회

  mockData: '/mocks/asak-admin-data.json', // 백엔드 완성 전까지 사용할 임시 목업 데이터 경로

  // ---------- 관리자 ----------
  ADMIN_LOGIN: '/admin/login', // 관리자 로그인
};
