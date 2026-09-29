import "../styles/Footer.css";

export default function Footer(){
    const date = new Date();
    const currentYear = date.getFullYear();
    return(
        <div className="container-fluid border-top pt-2 text-secondary">
            <div>
                <p className="footer">
                    &copy; {currentYear} ShopEase. All Rights Reserved.
                </p>
            </div>
        </div>
    )
}