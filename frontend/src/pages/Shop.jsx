import "../styles/Shop.css";
import {useState, useEffect} from "react";
import api from "../api";

import '../styles/LandingPage.css';
import Logo from '../assets/shopease-logo.webp';
import { Link } from "react-router-dom";
import { ShoppingCart, Search } from "lucide-react";

import defaultImage from "../assets/default-image.jpg";
import Footer from "../components/Footer";

const truncateDescription = (description, maxLength = 100) => {
    if (description.length <= maxLength) {
        return description;
    }

    return description.slice(0, maxLength) + "...";
};


export default function Shop(){
    const [products, setProducts] = useState([]);
    const [search, setSearch] = useState("");
    const [categories, setCategories] = useState([]);
    const [activeCategory, setActiveCategory] = useState("All");

    useEffect(() => {
        const fetchProducts = async () => {
        try {
            const response = await api.get("/api/shop-ease/products/");
            setProducts(response.data);
        } catch (error) {
            console.error("Failed to fetch products:", error);
        }
        };

        fetchProducts();
    }, []);

    useEffect(() => {
        const fetchCategories = async () => {
        try {
            const response = await api.get("/api/shop-ease/categories/");
            setCategories(response.data);
        } catch (error) {
            console.error("Failed to fetch categories:", error);
        }
        };

        fetchCategories();
    }, []);

    const filteredProducts = products.filter((product) => {
        const matchesCategory =
            activeCategory === "All" ||
            product.category.id === activeCategory;

        const searchTerm = search.toLowerCase();

        const matchesSearch =
            product.name.toLowerCase().includes(searchTerm) ||
            product.brand?.toLowerCase().includes(searchTerm) ||
            product.seller?.business_name?.toLowerCase().includes(searchTerm) ||
            product.description?.toLowerCase().includes(searchTerm);

        return matchesCategory && matchesSearch;
    });

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
                <h4 className="mt-2 shop-title">Shop</h4>
                
                <p className="available-products">
                    {products.length}{" "}
                    {products.length === 1
                        ? "Product"
                        : "Products"}{" "}
                    Available
                </p>
            </div>

            <div className="container mb-4">
                <div className="row align-items-center justify-content-between">
                    <div className="col-12 col-sm-5 search-bar d-flex align-items-center">
                        <input 
                            type="text" 
                            placeholder="Search products..." 
                            className="search rounded-pill ps-2 p-1"
                            value={search}
                            onChange={(e) =>
                                setSearch(e.target.value)
                            }
                        />

                        <span className="search-icon">
                            <Search size={18} />
                        </span>
                    </div>

                    <div className="col-12 col-sm-7  d-flex justify-content-end gap-2">
                        <button
                            className={`border-0 rounded-pill pt-1 pb-1 ps-2 pe-2 active-btn {activeCategory === "All" ? "active" : ""}`}
                            onClick={() => setActiveCategory("All")}
                        >
                            All
                        </button>

                        {categories.map((category) => (
                            <button
                                key={category.id}
                                className={`rounded-pill p-1 category-btn {activeCategory === category.id ? "active" : ""}`}
                                onClick={() => setActiveCategory(category.id)}
                            >
                                {category.category_display}
                            </button>
                        ))}
                    </div>
                </div>
            </div>

            <div className="container">
                <div className="row">
                    {filteredProducts.length === 0 ? (
                        <div className="text-center py-5">
                            <p className="no-products">
                                No products available. 
                                We are working hard to bring you more products.
                            </p>
                        </div>
                    ) : (
                        filteredProducts.map((product) => (
                            <div
                                className="col-12 col-sm-3 col-lg-3"
                                key={product.id}
                            >
                                <div className="product-container mb-4">
                                    <img
                                        src={product.images?.[0]?.image || defaultImage }
                                        className="img-fluid rounded-top"
                                        alt={product.name}
                                    />
                        
                                    <div className="d-flex flex-column p-4 product-info border rounded-bottom">
                                        <div className="d-flex align-items-center justify-content-between start-section">
                                            <p className="category-info p-1 rounded-pill">
                                                { product.category?.category }
                                            </p> 
                        
                                            <p className="price-info">
                                                Ksh.{product.price}
                                            </p>
                                        </div>
                        
                                        <h6 className="product-name">
                                            {product.name}
                                        </h6>
                        
                                        <p className="description-info">
                                            {truncateDescription(product.description, 100)}
                                        </p>
                        
                                        <Link
                                            to={`/products/${product.slug}`}
                                            className="text-center p-2 mt-auto view-btn rounded"
                                        >
                                            View Product
                                        </Link>
                                    </div>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>

            <div className="container-fluid mt-2">
                <Footer />
            </div>
        </div>
    )
}