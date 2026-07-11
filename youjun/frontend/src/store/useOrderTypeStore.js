import { create } from 'zustand'; // zustand의 store 생성 함수 가져오기

// 주문 타입 값을 문자열 오타 없이 관리하기 위한 상수
export const ORDER_TYPE = {
  EAT_IN: 'EAT_IN', // 매장에서 먹기
  TAKE_OUT: 'TAKE_OUT', // 포장하기
};

// 주문 타입만 관리하는 전역 상태 보관함 생성
export const useOrderTypeStore = create((set) => ({
  orderType: null, // 현재 선택된 주문 타입 (초기값 없음)

  setOrderType: (type) => set({ orderType: type }), // 주문 타입 저장하는 함수

  resetOrderType: () => set({ orderType: null }), // 주문 타입 초기화하는 함수
}));
