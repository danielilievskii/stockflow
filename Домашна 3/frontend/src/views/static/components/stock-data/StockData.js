import React, {useEffect, useState} from "react";
import StocksTable from "./StocksTable";
import { StockActions } from "../../../../actions/stockActions";
import useFetchCompanies from "../../../../hooks/useFetchCompanies";
import useResponseHandler from "../../../../hooks/useResponseHandler";

export const StockData = () => {
    const [stocks, setStocks] = useState([]);
    const [selectedCompany, setSelectedCompany] = useState("");

    const { companies } = useFetchCompanies();
    const { response, handleResponse, handleError } = useResponseHandler();

    const handleFetchCompanyData = () => {
        StockActions.fetchCompanyData(selectedCompany)
            .then((result) => {
                handleResponse(result, (data) => {
                    setStocks(data);
                }, { message: "Data fetched successfully" });
            })
            .catch((error) => {
                handleError(error);
            });
    };

    return (
        <div className="container mt-5">
            <h2 className="text-center mb-4">Македонска Берза</h2>
            <form className="mb-4">
                <div className="row align-items-center">
                    <div className="col-md-6">
                        <label htmlFor="companySelect" className="form-label">
                            Изберете компанија:
                        </label>
                        <select
                            id="companySelect"
                            className="form-select"
                            value={selectedCompany}
                            onChange={(e) => setSelectedCompany(e.target.value)}
                        >
                            <option value="">-- Изберете компанија --</option>
                            {companies.map((company, index) => (
                                <option key={index} value={company}>
                                    {company}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div className="col-md-6 text-md-end mt-3 mt-md-0">
                        <button
                            type="button"
                            className="btn btn-warning me-2"
                            onClick={handleFetchCompanyData}
                        >
                            Превземи податоци
                        </button>
                    </div>
                </div>
            </form>

            {response && <p className="text-center text-info">{response}</p>}

            <StocksTable data={stocks}/>
        </div>
    );
};
