import { BrowserRouter, Routes, Route } from 'react-router-dom'; // 라우팅 기능 가져오기
import Home from './pages/kiosk/Home'; // 홈 화면 컴포넌트만 가져오기

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />{' '}
        {/* "/" 경로로 오면 Home 화면 보여주기 */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
