import React from "react";
import logo from "../../assets/logo/logo.png"

const Navbar = () => {

    return(
        <nav className="navbar navbar-expand-lg bg-body-tertiary">
            <div className="container-fluid">
                <a className="navbar-brand" href="#">
                <img src={logo} alt="Logo" width="30" height="25" class="d-inline-block align-text-top" />
                    E-commerce
                </a>
            </div>
        </nav>
    );
}; 

export default Navbar;