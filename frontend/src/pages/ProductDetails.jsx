import { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import api from "../api";
import Swal from "sweetalert2";
import { ArrowLeft, Heart } from "lucide-react";

import "../styles/ProductDetails.css";
import defaultImg from "../assets/default-image.jpg";

export default function ProductDetails(){
    const {slug} = useParams();
    const [product, setProduct] = useState(null);
    const [quantity, setQuantity] = useState(1);

    const navigate = useNavigate();

    useEffect(() => {
        const showError = async (title, text) => {
            await Swal.fire({
                icon: "error",
                title,
                text,
                confirmButtonText: "Back to shop",
                allowOutsideClick: false,
            });
            navigate("/shop");
        };

        const fetchProduct = async () => {
            try {
                const res = await api.get(`/api/shop-ease/products/${slug}/`);

                setProduct(res.data);
            } catch (err) {
                console.error(err);

                if (!err.response) {
                    await showError(
                        "Connection problem",
                        "We couldn't reach the server. Check your internet connection and try again."
                    );
                    return;
                }

                switch (err.response.status) {
                    case 404:
                        await showError(
                            "Product not found",
                            "This product doesn't exist or may have been removed."
                        );
                        break;
                    case 401:
                    case 403:
                        await showError(
                            "Access denied",
                            "You don't have permission to view this product."
                        );
                        break;
                    case 500:
                    default:
                        await showError(
                            "Something went wrong",
                            "We couldn't load this product. Please try again later."
                        );
                }
            }
        };

        fetchProduct();
    }, [slug, navigate]);

    if (!product) return null;

    return(
        <div className="container-fluid">
            <div className="container-fluid border-bottom">
                <div className="container d-flex align-items-center justify-content-between p-4">
                    <Link to="/shop" className="back-shop d-flex align-items-center">
                        <ArrowLeft size={20}  className="pe-1"/>
                        Back to shop
                    </Link>

                    <Link to="" className="border border-1 rounded p-2 favorite-btn" data-bs-toggle="tooltip" title="Add to favorite">
                        <Heart size={20} color="#6C757D" />
                    </Link>
                </div>
            </div>

            <div className="container mt-4">
                <div className="row">
                    <div className="col-12 col-sm-6">
                        <img 
                            src={
                            product.images?.[0]?.image ||
                            defaultImg
                            }
                            className="img-fluid rounded"
                            alt={product.name}
                        />
                    </div>

                    <div className="col-12 col-sm-6 mt-3">
                        <p className="category-name p-1 rounded-pill text-center">
                            { product.category?.category }
                        </p>

                        <h4 className="item-name">{ product.name }</h4>

                        <h5 className="item-price">Ksh.{ product.price }</h5>

                        <p className="item-description">
                            {product.description}
                        </p>

                        <p className="item-stock">
                            <small className="stock">In stock</small> - {product.stock} available
                        </p>

                        <p className="item-seller">
                            <small className="seller">Seller</small> - {product.seller?.business_name}
                        </p>

                        <div className="add-to-cart d-flex">
                            <div className="d-flex align-items-center">
                                <button
                                    type="button"
                                    className="add-btn pe-2 ps-2 pt-2 pb-2 border-0"
                                    onClick={() => setQuantity(prev => Math.max(1, prev - 1))}
                                    disabled={quantity <= 1}
                                >
                                    -
                                </button>

                                <span className="fw-semibold px-1">
                                    {quantity}
                                </span>

                                <button
                                    type="button"
                                    className="add-btn me-2 pe-2 ps-2 pt-2 pb-2 border-0"
                                    onClick={() => setQuantity(prev => Math.min(product.stock, prev + 1))}
                                    disabled={quantity >= product.stock}
                                >
                                    +
                                </button>

                            </div>

                            <button
                                type="button"
                                className="cart-button border-0 rounded w-75"
                                disabled={!product.is_available || product.stock <= 0}
                                onClick={() => {
                                    console.log("Adding to cart:", {
                                        product: product.id,
                                        quantity: quantity
                                    });
                                }}
                            >
                                Add to Cart
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            
        </div>
    )
}