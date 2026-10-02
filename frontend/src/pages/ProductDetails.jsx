import { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import api from "../api";
import Swal from "sweetalert2";

export default function ProductDetails(){
    const {slug} = useParams();
    const [product, setProduct] = useState(null);
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
        <div>
            <h2>Details</h2>
        </div>
    )
}