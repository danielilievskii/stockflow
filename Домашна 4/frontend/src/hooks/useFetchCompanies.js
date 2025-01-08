import { useState, useEffect } from 'react';
import {StockActions} from '../actions/stockActions';
import useResponseHandler from "./useResponseHandler";  // Adjust path as needed

function useFetchCompanies() {
    const [companies, setCompanies] = useState([]);
    const { response, handleResponse, handleError } = useResponseHandler();

    useEffect(() => {
        StockActions.fetchCompanies()
            .then((result) => {
                handleResponse(result, (data) => {
                    setCompanies(data);
                }, {message: "Companies loaded successfully!"});
            })
            .catch(() => {
                handleError({ message: "Please select both a company and a time period." });
            });
    }, []);

    return { companies };
}

export default useFetchCompanies;