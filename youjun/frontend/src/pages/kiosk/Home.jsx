import { useNavigate } from 'react-router-dom'; // 페이지 이동 기능 가져오기
import useOrderTypeStore, { ORDER_TYPE } from '../../store/useOrderTypeStore'; // 주문 타입 store 가져오기

function Home() {
  const navigate = useNavigate(); // 페이지 이동시켜줄 함수 준비

  const setOrderType = useOrderTypeStore((state) => state.setOrderType); // store에서 저장 함수만 꺼내오기

  // 버튼 클릭 시 주문 타입 저장하고 메뉴 화면으로 이동시키는 함수
  const handleSelectOrderType = (type) => {
    setOrderType(type); // store에 주문 타입 저장 (EAT_IN 또는 TAKE_OUT)
    navigate('/menu'); // 메뉴 화면으로 이동
  };

  return (
    <div>
      <p>신선한 샐러드, 지금 주문하세요</p>

      {/* 주문 방식(매장/포장) 선택 영역 */}
      <div>
        <button
          type="button"
          onClick={() => handleSelectOrderType(ORDER_TYPE.EAT_IN)}
        >
          매장에서 먹기 (Eat In)
        </button>

        <button
          type="button"
          onClick={() => handleSelectOrderType(ORDER_TYPE.TAKE_OUT)}
        >
          포장하기 (Take Out)
        </button>
      </div>
    </div>
  );
}

export default Home;
