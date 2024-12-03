import React, { useState } from 'react';
import {Link} from "react-router-dom";


export const LandingPage = () => {

    return (
        <div className={"mt-5"}>
            <Link to={`/stock-data`} className={'btn btn-warning'}> ЗАПОЧНИ СО АНАЛИЗА </Link>
        </div>
    )
}

