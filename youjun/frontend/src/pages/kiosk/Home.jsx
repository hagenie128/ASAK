import { useNavigate } from 'react-router-dom'; // 페이지 이동 기능 가져오기
import LogoButton from '../../components/common/LogoButton'; // 로고 컴포넌트 가져오기
import useOrderTypeStore, { ORDER_TYPE } from '../../store/useOrderTypeStore'; // 주문 타입 store 가져오기

function Home() {
  const navigate = useNavigate(); // 페이지 이동시켜줄 함수 준비

  const setOrderType = useOrderTypeStore((state) => state.setOrderType); // store에서 저장 함수만 꺼내오기

  // 버튼 클릭 시 주문 타입 저장하고 메뉴 화면으로 이동시키는 함수
  const handleSelectOrderType = (type) => {
    setOrderType(type); // store에 주문 타입 저장
    navigate('/menu'); // 메뉴 화면으로 이동
  };

  return (
    <div className="home-page">
      <LogoButton /> {/* 상단 로고 */}
      <p className="home-guide-text">신선한 샐러드, 지금 주문하세요</p>{' '}
      {/* 안내 문구 */}
      <div className="home-image-wrapper">
        <img src="/images/salad-main.png" alt="샐러드 이미지" />{' '}
        {/* 메인 이미지 */}
      </div>
      <div className="order-type-buttons">
        <button
          type="button"
          onClick={() => handleSelectOrderType(ORDER_TYPE.EAT_IN)} // 매장식사 선택
        >
          <span>매장에서 먹기</span>
          <span>Eat In</span>
        </button>

        <button
          type="button"
          onClick={() => handleSelectOrderType(ORDER_TYPE.TAKE_OUT)} // 포장 선택
        >
          <span>포장하기</span>
          <span>Take Out</span>
        </button>
      </div>
    </div>
  );
}

export default Home; // 다른 파일에서 가져다 쓸 수 있도록 내보내기
