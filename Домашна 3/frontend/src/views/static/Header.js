import "./Header.css";
import { Link, NavLink } from "react-router-dom";
import React from "react";

export const Header = () => {
    return (
        <nav className="navbar navbar-expand-lg">
            <div className="container-fluid">
                <Link to="/" className="navbar-brand">
                    <img src="./logo-stockflow-main.png" alt="Logo" className="logo-main" height={80} />
                    <img src="./logo-stockflow-secondary.png" alt="Secondary Logo" className="logo-secondary" height={45} />
                </Link>

                <button
                    className="navbar-toggler navbar-toggler-custom"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarScroll"
                    aria-controls="navbarScroll"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="collapse navbar-collapse" id="navbarScroll">
                    <ul className="navbar-nav ms-auto my-2 my-lg-0 navbar-nav-scroll">
                        <li className="nav-item">
                            <NavLink to="/technical" className="nav-link text-white small">Техничка анализа</NavLink>
                        </li>
                        <li className="nav-item">
                            <NavLink to="/fundamental" className="nav-link text-white small">Фундаментална анализа</NavLink>
                        </li>
                        <li className="nav-item">
                            <NavLink to="/model" className="nav-link text-white small">Ценовна анализа</NavLink>
                        </li>
                        <li className="nav-item">
                            <NavLink to="/stock-data" className="nav-link text-white small">Историја</NavLink>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    );
};