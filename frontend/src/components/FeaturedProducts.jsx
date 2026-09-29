import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import '../styles/FeaturedProducts.css';
export default function FeaturedProducts(){
    const [products, setProducts] = useState([]);

    useEffect(() => {
        const fetchFeaturedProducts = async () => {
            try {
                const response = await api.get(
                    "/api/products/featured/"
                );

                setProducts(response.data);
            } catch (err) {
                console.error(err)
            }
        };
        fetchFeaturedProducts();
    }, []);

    return (
        <div className="container mt-5">
            <div className="featured-products d-flex justify-content-between">
                <div className="right-section">
                    <h4>Featured Products</h4>
                    <p className="text-secondary">Handpicked for the week</p>
                </div>

                <div className="left-section d-flex align-items-center">
                    <Link to="" className="link-shop">View all</Link>
                </div>
            </div>

            {products.length === 0 ? (
                <p className="text-secondary text-center py-4">
                    No featured products available.
                </p>
            ) : (
                <div className="row g-4">
                    {products.map((product) => (
                        <div
                            className="col-12 col-sm-6 col-lg-4 col-xl-2"
                            key={product.id}
                        >
                            <div className="card h-100 shadow-sm">
                                <img
                                    src={product.image}
                                    className="card-img-top"
                                    alt={product.name}
                                    style={{
                                        height: "180px",
                                        objectFit: "cover",
                                    }}
                                />

                                <div className="card-body d-flex flex-column">
                                    <h6 className="card-title">
                                        {product.name}
                                    </h6>

                                    <p className="fw-bold text-primary">
                                        KSh {product.price}
                                    </p>

                                    <Link
                                        to={`/products/${product.id}`}
                                        className="btn btn-primary mt-auto"
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