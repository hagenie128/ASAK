//로그인 (기존교제 응용)

import { useRef, useState } from "react";
import { useAuthStore } from "../../store/useAuthStore";
import { useNavigate } from "react-router-dom";

export default () => {
  const username = useRef(null);
  const password = useRef(null);
  const [loading, setLoding] = useState(false);
  const { login } = useAuthStore();
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState('');

  const handleLogin = async () => {
    setLoding(true);
    try{
      await login(username.current.value,password.current.value);
      navigate('/admin');
    }catch(error){
      console.log(error);
      setErrorMessage(error.response?.data?.message || '로그인 실패했습니다.');
    }finally{
      setLoding(false);
    }
  };

  // 로그인 폼
  return <div className="login-container">
    <div className="login-card">
      <div className="login-header">
        <h2 className="login-title">로그인</h2>
        <p className="login-subtitle">ASAK 관리자 로그인</p>
      </div>
      <div className="frm-login">
        <input className="login-input" type="text" placeholder="아이디를 입력하세요" ref={username}/>
        <input className="login-input" type="password" placeholder="암호를 입력하세요" ref={password}/>
        {errorMessage && <div className="error-message-box">{errorMessage}</div>}
        {loading ? <p className="login-loading">현재 로그인 중입니다.</p> : <button className="btn btn-primary login-submit-btn" onClick={handleLogin}>로그인</button>}

</div>
    </div>
  </div>
}