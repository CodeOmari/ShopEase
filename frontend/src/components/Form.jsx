import { useState } from "react";
import api from "../api";
import { useNavigate, Link } from "react-router-dom"
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import LoadingIndicator from './LoadingIndicator';

import '../styles/Form.css';
import Logo from '../assets/shopease-logo.webp';
import Swal from 'sweetalert2';

export default function Form({route, method}){
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [role, setRole] = useState("");
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [phoneNumber, setPhoneNumber] = useState("");
    const [password1, setPassword1] = useState("");
    const [password2, setPassword2] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const [loading, setLoading] = useState(false);
 
    const navigate = useNavigate();

    const isLogin = method === "login";
    const action = method === "login" ? "Login" : "Register";

    const handleSubmit = async (e) => {
        e.preventDefault();

        const passwordRegex = /^(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$/;

        if (method === 'register') {
           if (password1 !== password2) {
                Swal.fire({ 
                    icon: "error", 
                    title: "Passwords do not match", 
                    text: "Please make sure both passwords are the same.", 
                });
            return;
           }

           if (!passwordRegex.test(password1)) {
             Swal.fire({ 
                icon: "warning", 
                title: "Weak Password", 
                text: "Password must be at least 8 characters long and include at least one special character.", 
            });
             return;
           }
    }

        setLoading(true);

        try {
        let payload;

        if (method === 'login') {
            payload = { 
            email, 
            password: password1,
            };
        } else {
            payload = { 
            username, 
            email,
            password1, 
            password2, 
            };
        }

        console.log("Payload:", payload);

        const res = await api.post(route, payload);

        if (method === "login") {
            localStorage.setItem(ACCESS_TOKEN, res.data.access);
            localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
            navigate("/");
        } else {
             await Swal.fire({ 
                    icon: "success", 
                    title: "Account Created!", 
                    text: "Your account was created successfully. Please log in.", 
                    confirmButtonText: "Go to Login", 
            });
            navigate("/login");
        }
        } catch (error) {
            if (method === "login") {
                Swal.fire({ 
                    icon: "error", 
                    title: "Login Failed", 
                    text: "Incorrect username or password.", 
                });
            } else {
                if (error.response && error.response.data) {
                const data = error.response.data;

                const messages = Object.values(data).flat().join("\n");
                    Swal.fire({ 
                        icon: "error", 
                        title: "Registration Failed", 
                        text: messages, 
                    });
                } else {
                    Swal.fire({ 
                        icon: "error", 
                        title: "Registration Failed", 
                        text: "Something went wrong. Please try again.", 
                    });
                }
            }
        } finally {
            setLoading(false);
        }
    };

    return(
        <div className="auth-page">
            <div className="auth-card">

                <div className="brand-icon">
                    <img src={Logo} alt="ShopEase icon" />
                </div>

                 <h1 className="brand-title">
                    Sign in to continue
                 </h1>

                <div className="tab-toggle">
                    <Link to="/login" className={isLogin ? "active" : ""}>Sign in</Link>
                    <Link to="/register" className={!isLogin ? "active" : ""}>Create account</Link>
                </div>

                <form onSubmit={handleSubmit} className="form-container">

                {method === 'register' && (
                    <div>
                        <div className="form-group">
                            <label className="form-label">First Name</label>
                            <input
                                className="form-input"
                                type="text"
                                value={firstName}
                                onChange={(e) => setFirstName(e.target.value)}
                                placeholder="First name"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label className="form-label">Last Name</label>
                            <input
                                className="form-input"
                                type="text"
                                value={lastName}
                                onChange={(e) => setLastName(e.target.value)}
                                placeholder="Last name"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label className="form-label">Username</label>
                            <input
                                className="form-input"
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                placeholder="username"
                                required
                            />
                            <p className="form-hint">3–24 characters. Letters, numbers, underscores.</p>
                        </div>

                        <div className="form-group">
                            <label className="form-label">Phone Number</label>

                            <input
                                className="form-input"
                                type="tel"
                                value={phoneNumber}
                                onChange={(e) => setPhoneNumber(e.target.value)}
                                placeholder="0712345678"
                                maxLength="10"
                                required
                            />

                            <p className="form-hint">
                                Enter a valid 10-digit phone number, e.g. 0712345678.
                            </p>
                        </div>

                        <div className="form-group">
                            <label className="form-label">Role</label>
                            <select
                                className="form-input"
                                value={role}
                                onChange={(e) => setRole(e.target.value)}
                                required
                            >
                                <option value="">Select your role</option>
                                <option value="BUYER">Buyer</option>
                                <option value="SELLER">Seller</option>
                            </select>
                            <p className="form-hint">
                                Choose Buyer if you want to purchase products, or Seller if you want to sell products.
                            </p>
                        </div>
                    </div>
                )}

                <div className="form-group">
                    <label className="form-label">Email</label>
                    <input
                    className="form-input"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="you@example.com"
                    required
                    />
                </div>

                <div className="form-group password-wrapper">
                    <label className="form-label">Password</label>
                    <input
                    className="form-input"
                    type={showPassword ? "text" : "password"}
                    value={password1}
                    onChange={(e) => setPassword1(e.target.value)}
                    placeholder="Password"
                    required
                    />
                    <button
                        type="button"
                            className="password-toggle"
                            onClick={() => setShowPassword(!showPassword)}
                        >
                        {showPassword ? "Hide" : "Show"}
                    </button>
                </div>

                {method === 'register' && (
                    <div className="form-group password-wrapper">
                        <label className="form-label">Confirm Password</label>
                        <input
                            className="form-input"
                            type={showConfirmPassword ? "text" : "password"}
                            value={password2}
                            onChange={(e) => setPassword2(e.target.value)}
                            placeholder=""
                            required
                        />
                        <button
                            type="button"
                            className="password-toggle"
                            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        >
                            {showConfirmPassword ? "Hide" : "Show"}
                        </button>
                    </div>
                )}

                {loading && <LoadingIndicator />}

                <button className="form-button" type="submit">
                    {action}
                </button>

                </form>
            </div>
        </div>
    );
}