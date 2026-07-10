import { create } from 'zustand';
import { ENDPOINTS } from '../api/endpoints';

// 카테고리, 메뉴 데이터를 관리하는 store
export const useMenuStore = create((set) => ({
  categories: [], // 카테고리 목록
  menus: [], // 메뉴 목록
  selectedCategoryId: null, // 현재 선택된 카테고리 (null = 전체보기)
  isLoading: false, // 불러오는 중인지
  error: null, // 에러 메시지

  // 카테고리 목록 불러오기
  fetchCategories: async () => {
    set({ isLoading: true, error: null });

    try {
      const response = await fetch(ENDPOINTS.mockData);
      if (!response.ok) throw new Error('카테고리를 불러오지 못했습니다.');

      const result = await response.json();
      set({ categories: result.categories ?? [], isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },

  // 메뉴 목록 불러오기, categoryId 없으면 전체 조회
  fetchMenus: async (categoryId = null) => {
    set({ isLoading: true, error: null, selectedCategoryId: categoryId });

    try {
      const response = await fetch(ENDPOINTS.mockData);
      if (!response.ok) throw new Error('메뉴를 불러오지 못했습니다.');

      const result = await response.json();
      const allMenus = result.menus ?? [];

      // categoryId가 있으면 그 카테고리 메뉴만 걸러냄
      const filtered = categoryId
        ? allMenus.filter((menu) => menu.categoryId === categoryId)
        : allMenus;

      set({ menus: filtered, isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },
}));
