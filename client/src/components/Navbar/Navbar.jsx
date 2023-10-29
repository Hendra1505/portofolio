import React from "react";
import logo from "../../assets/logo/logo.png"

const Navbar = () => {

    return(
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container-fluid">
            <a className="navbar-brand" href="#">
                <img src={logo} width="45" height="40"/>
            </a>
            <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarTogglerDemo01">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                <li className="nav-item">
                    <a className="nav-link" aria-current="home" href="#">Home</a>
                </li>
                <li className="nav-item">
                    <a className="nav-link" aria-current="services" href="#">Services</a>
                </li>
                <li className="nav-item">
                    <a className="nav-link" aria-current="order" href="#">Order</a>
                </li>
            </ul>
            </div>
        </div>
        </nav>
    );
}; 

export default Navbar;