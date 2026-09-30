import { Navigate } from 'react-router-dom';
import { jwtDecode} from "jwt-decode";
import { ACCESS_TOKEN } from '../constants';

export default function RoleProtectedRoute({ children, allowedRole }){
    const token = localStorage.getItem(ACCESS_TOKEN);

    if (!token) {
        return <Navigate to="/login" replace />;
    }

    try {
        const decoded = jwtDecode(token);

        if (decoded.role !== allowedRole) {
            return <Navigate to="/dashboard" replace />;
        }

        return children;
    } catch (error) {
        console.error("Invalid token:", error);

        localStorage.removeItem("access_token");

        return <Navigate to="/login" replace />;
    }
};