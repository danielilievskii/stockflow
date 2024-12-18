import {Link} from "react-scroll";
import React from "react";
import "./AnalysisButton.css"

export const AnalysisButton =() => {
    return (
        <div className="mt-5">
            <Link to="targetSection" smooth={true} duration={100} className="btn btn-warning"> ЗАПОЧНИ СО АНАЛИЗА </Link>
        </div>
    )
}