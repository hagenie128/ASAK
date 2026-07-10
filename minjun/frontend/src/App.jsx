import { BrowserRouter, Routes, Route } from "react-router-dom";

// kiosk pages
import Home from "./pages/kiosk/Home";
import Menu from "./pages/kiosk/Menu";
import MenuDetail from "./pages/kiosk/MenuDetail";
import Cart from "./pages/kiosk/Cart";
import Payment from "./pages/kiosk/Payment";
import PaymentDeclined from "./pages/kiosk/PaymentDeclined";
import PaymentRetry from "./pages/kiosk/PaymentRetry";
import Receipt from "./pages/kiosk/Receipt";
import OrderComplete from "./pages/kiosk/OrderComplete";
import Time from "./pages/kiosk/Time";

// admin pages
import Login from "./pages/admin/Login";
import MenuManage from "./pages/admin/MenuManage";
import OrderManage from "./pages/admin/OrderManage";
import OrderStatus from "./pages/admin/OrderStatus";
import PaymentSetting from "./pages/admin/PaymentSetting";
import SalesSummary from "./pages/admin/SalesSummary";
import SoldOutManage from "./pages/admin/SoldOutManage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ---------- 고객용 키오스크 화면 ---------- */}
        <Route path="/" element={<Home />} />
        <Route path="/menu" element={<Menu />} />
        <Route path="/menu/:menuId" element={<MenuDetail />} />
        <Route path="/cart" element={<Cart />} />
        <Route path="/payment" element={<Payment />} />
        <Route path="/payment/declined" element={<PaymentDeclined />} />
        <Route path="/payment/retry" element={<PaymentRetry />} />
        <Route path="/receipt" element={<Receipt />} />
        <Route path="/order-complete" element={<OrderComplete />} />
        <Route path="/time" element={<Time />} />

        {/* ---------- 관리자 화면 ---------- */}
        <Route path="/admin/login" element={<Login />} />
        <Route path="/admin/menu" element={<MenuManage />} />
        <Route path="/admin/orders" element={<OrderManage />} />
        <Route path="/admin/order-status" element={<OrderStatus />} />
        <Route path="/admin/payment-setting" element={<PaymentSetting />} />
        <Route path="/admin/sales-summary" element={<SalesSummary />} />
        <Route path="/admin/sold-out" element={<SoldOutManage />} />
      </Routes>ㄴ
    </BrowserRouter>
  );
}

export default App;