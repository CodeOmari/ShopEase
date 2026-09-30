import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import { ACCESS_TOKEN } from "../constants";

export default function DashboardRedirect(){
    const token = localStorage.getItem(ACCESS_TOKEN);

    if (!token) {
        return <Navigate to="/login" replace />;
    }

    try {
        const decoded = jwtDecode(token);

        console.log("Decoded JWT:", decoded);
        console.log("User role:", decoded.role);

        if (decoded.role === "SELLER") {
            return <Navigate to="/seller-dashboard" replace />;
        }

        if (decoded.role === "BUYER") {
            return <Navigate to="/customer-dashboard" replace />;
        }

        return <Navigate to="/" replace />;
    } catch (error) {
        localStorage.removeItem(ACCESS_TOKEN);
        return <Navigate to="/login" replace />;
    }
};