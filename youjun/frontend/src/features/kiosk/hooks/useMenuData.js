import { useEffect } from 'react';
import { useMenuStore } from '../../../store/useMenuStore';

// Menu.jsx에서 store 내부 구조를 몰라도 되게 정리해서 꺼내주는 hook
export function useMenuData() {
  const categories = useMenuStore((state) => state.categories);
  const menus = useMenuStore((state) => state.menus);
  const selectedCategoryId = useMenuStore((state) => state.selectedCategoryId);
  const isLoading = useMenuStore((state) => state.isLoading);
  const error = useMenuStore((state) => state.error);
  const fetchCategories = useMenuStore((state) => state.fetchCategories);
  const fetchMenus = useMenuStore((state) => state.fetchMenus);

  // Menu.jsx 화면이 처음 켜질 때 자동으로 카테고리 + 전체 메뉴 불러오기
  useEffect(() => {
    fetchCategories();
    fetchMenus(null);
  }, [fetchCategories, fetchMenus]);

  // 카테고리 버튼 클릭 시 실행할 함수
  const selectCategory = (categoryId) => {
    fetchMenus(categoryId);
  };

  return {
    categories,
    menus,
    selectedCategoryId,
    isLoading,
    error,
    selectCategory,
  };
}
