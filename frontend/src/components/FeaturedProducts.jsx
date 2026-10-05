import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import '../styles/FeaturedProducts.css';
import defaultImage from "../assets/default-image.jpg";


const truncateDescription = (description, maxLength = 100) => {
    if (description.length <= maxLength) {
        return description;
    }

    return description.slice(0, maxLength) + "...";
};


export default function FeaturedProducts(){
    const [products, setProducts] = useState([]);

    useEffect(() => {
        const fetchFeaturedProducts = async () => {
            try {
                const response = await api.get(
                    "/api/shop-ease/products/featured/"
                );

                setProducts(response.data);
            } catch (err) {
                console.error(err)
            }
        };
        fetchFeaturedProducts();
    }, []);

    console.log("PRODUCTS:", products);

    return (
        <div className="container mt-5">
            <div className="featured-products d-flex justify-content-between">
                <div className="right-section">
                    <h4>Featured Products</h4>
                    <p className="text-secondary">Handpicked for the week</p>
                </div>

                <div className="left-section d-flex align-items-center">
                    <Link to="/shop" className="link-shop">View all</Link>
                </div>
            </div>

            {products.length === 0 ? (
                <p className="text-secondary text-center py-4">
                    No featured products available.
                </p>
            ) : (
                <div className="row g-4 mb-5">                    
                    {products.map((product) => (
                        <div
                            className="col-12 col-sm-3 col-lg-3"
                            key={product.id}
                        >
                            <div className="product-container">
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
                    ))}
                </div>
            )}
        </div>
    )
}