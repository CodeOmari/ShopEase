import "../styles/NotFound.css";
import { Link } from "react-router-dom";

export default function NotFound() {

    return (
        <div className="d-flex flex-column justify-content-center align-items-center mt-5 not-found">
            <h1>404 - Not Found</h1>
            <p>The page you are looking for does not exist.</p>
            <Link to="/" className="btn btn-primary">Go Back</Link>
        </div>
    )
}