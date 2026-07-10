import { useNavigate } from 'react-router-dom';
import { useMenuData } from '../../features/kiosk/hooks/useMenuData';

function Menu() {
  const navigate = useNavigate();

  const {
    categories,
    menus,
    selectedCategoryId,
    isLoading,
    error,
    selectCategory,
  } = useMenuData();

  // 메뉴 클릭 시 상세 화면으로 이동
  const handleMenuClick = (menuId) => {
    navigate(`/menu/${menuId}`);
  };

  if (isLoading) return <div>메뉴 불러오는 중</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      {/* 카테고리 버튼 목록 */}
      <div>
        <button type="button" onClick={() => selectCategory(null)}>
          전체
        </button>

        {categories.map((category) => (
          <button
            key={category.id}
            type="button"
            onClick={() => selectCategory(category.id)}
          >
            {category.name}
          </button>
        ))}
      </div>

      {/* 메뉴 목록 테이블 */}
      <table>
        <thead>
          <tr>
            <th>메뉴명</th>
            <th>가격</th>
            <th>품절여부</th>
          </tr>
        </thead>
        <tbody>
          {menus.map((menu) => (
            <tr key={menu.id} onClick={() => handleMenuClick(menu.id)}>
              <td>{menu.name}</td>
              <td>{menu.price}원</td>
              <td>{menu.isSoldOut ? '품절' : '판매중'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Menu;
