import { Link } from "react-router-dom";

import '../styles/LandingPage.css';
import Logo from '../assets/shopease-logo.webp';
import { ShoppingCart, Sparkles, ArrowRight, Truck, ShieldCheck, Shield } from "lucide-react";
import productsData from '../products';
import FeaturedProducts from "../components/FeaturedProducts";
import Footer from "../components/Footer";

export default function LandingPage(){
    
    return(
        <div className="container-fluid">
            <div className="container-fluid top-section d-flex align-items-center justify-content-between border-bottom sticky-top">
                <div>
                    <img src={Logo} alt="ShopEase logo" className="img-fluid logo" />
                </div>

                <nav className="navigation-section">
                    <Link to="/" className="pe-3 navigation-link">Home</Link>
                    <Link to='/shop' className="pe-3 navigation-link">Shop</Link>
                    <Link to="/dashboard" className="navigation-link">Dashboard</Link>
                </nav>

                <div>
                    <Link to="/cart" className="border border-1 rounded p-2 cart-btn">
                        <ShoppingCart size={18} color="#6C757D"/>
                    </Link>
                </div>
            </div>

            <div className="container mt-5 mb-5">
                <div className="row">
                    <div className="col-12 col-sm-5 col-lg-5 mt-5">
                        <span className="arrivals d-flex align-items-center border p-1 rounded-pill w-50 mb-3">
                            <Sparkles size={22} color="#3061EF" className="pe-1 ps-1" />
                            New arrivals every week
                        </span>

                        <h1 className="shop-smart mb-3">
                            Shop smarter with <b className="name">ShopEase</b>.
                        </h1>

                        <p className="about pb-4">
                            A modern marketplace built for buyers who want quality and sellers who want insight. 
                            One clean experience for both.
                        </p>

                        <div className="navigation-btn border-bottom d-flex pb-5">
                            <div className="shop-link me-2">
                                <Link to='' className="border shop-btn rounded p-3">
                                    Browse to shop
                                    <ArrowRight size={20} color="#fff" className="ps-1" />
                                </Link>
                            </div>

                            <div className="dashboard-link">
                                <Link to='' className="border dashboard-btn rounded p-3">Open Dashboard</Link>
                            </div>
                        </div>

                        <div className="stats d-flex align-items-center justify-content-between mt-4">
                            <div className="stat-details d-flex flex-column align-items-center">
                                <h5>Products</h5>
                                <p>8</p>
                            </div>

                            <div className="stat-details d-flex flex-column align-items-center">
                                <h5>Categories</h5>
                                <p>6</p>
                            </div>

                            <div className="stat-details d-flex flex-column align-items-center">
                                <h5>Live Offers</h5>
                                <p>2</p>
                            </div>
                        </div>
                    </div>

                    <div className="col-12 col-sm-7 col-lg-7 product-section">
                        <div className="container">
                            <div className="row">
                                {productsData.map((product) => (
                                    <div className="col-12 col-sm-6 col-lg-6 d-flex" key={product.id}>
                                        <div className=" product-container p-4">
                                            <img src={product.img.src} alt={product.img.alt} className="img-fluid rounded" />   
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="container mt-5">
                <FeaturedProducts />
            </div>

            <div className="container mb-5">
                <div className="row g-4">
                    <div className="col-12 col-sm-4 col-sm-4">
                        <div className="border p-3 rounded details-container">
                            <Truck  color="#3061EF" size={20}/>

                            <div className="details mt-3">
                                <h5>Fast Shipping</h5>
                                <p className="text-secondary">Free on orders over $150.</p>
                            </div>  
                        </div>
                    </div>
                    <div className="col-12 col-sm-4 col-sm-4">
                        <div className="border p-3 rounded details-container">
                            <ShieldCheck color="#3061EF" size={20} />

                            <div className="details mt-3">
                                <h5>Buyer Protection</h5>
                                <p className="text-secondary">30-day easy returns</p>
                            </div>
                        </div>
                    </div>
                    <div className="col-12 col-sm-4 col-sm-4">
                       <div className="border p-3 rounded details-container">
                             <Sparkles color="#3061EF" size={20} />

                            <div className="details mt-3">
                                <h5>Seller-friendly</h5>
                                <p className="text-secondary">Track sales and offers in one dashboard.</p>
                            </div>
                       </div>
                    </div>
                </div>
            </div>

            <div className="container-fluid mt-5">
                <Footer />
            </div>
        </div>
    )
}