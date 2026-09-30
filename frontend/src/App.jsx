import react from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import NotFound from "./pages/NotFound";
import LandingPage from "./pages/LandingPage";
import ProtectedRoute from "./components/ProtectedRoute";
import Shop from "./pages/Shop";
import Cart from "./pages/Cart";

import SellerDashboard from "./pages/SellerDashboard";
import CustomerDashboard from "./pages/CustomerDashboard";
import RoleProtectedRoute from "./components/RoleProtectedRoute";
import DashboardRedirect from "./routes/DashboardRedirect";

function Logout() {
  localStorage.clear()
  return <Navigate to="/" />
}

function RegisterAndLogout() {
  localStorage.clear()
  return <Register />
}


export default function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/register" element={<RegisterAndLogout />} />

        <Route path="/" element={<LandingPage />} />
        <Route 
          path="/shop"
          element = {
            <ProtectedRoute>
              <Shop />
            </ProtectedRoute>
          }
        />
        <Route 
          path="/seller-dashboard"
          element = {
            <ProtectedRoute>
              <RoleProtectedRoute allowedRole="SELLER">
                <SellerDashboard />
              </RoleProtectedRoute>
            </ProtectedRoute>
          }
        />
        <Route
          path="/customer-dashboard"
          element = {
            <ProtectedRoute>
              <RoleProtectedRoute allowedRole="BUYER">
                <CustomerDashboard />
              </RoleProtectedRoute>
            </ProtectedRoute>
          }
        />

        <Route path="/dashboard" element={ 
          <ProtectedRoute>
              <DashboardRedirect />
          </ProtectedRoute>
        } />

        <Route path="/cart" element={
          <ProtectedRoute>
            <Cart />
          </ProtectedRoute>
        } />
        <Route path="*" element={<NotFound />} />

      </Routes>
    </BrowserRouter>
  )
}