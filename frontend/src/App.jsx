import react from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import NotFound from "./pages/NotFound";
import LandingPage from "./pages/LandingPage";

function Logout() {
  localStorage.clear()
  return <Navigate to="/login" />
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

        <Route path="*" element={<NotFound />} />

      </Routes>
    </BrowserRouter>
  )
}