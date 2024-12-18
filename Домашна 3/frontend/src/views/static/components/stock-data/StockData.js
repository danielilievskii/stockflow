import React, {useEffect, useState} from "react";
import StocksTable from "./StocksTable";

export const StockData = () => {
    const [response, setResponse] = useState("");
    const [stocks, setStocks] = useState([]);
    const [companies, setCompanies] = useState([]);
    const [selectedCompany, setSelectedCompany] = useState("");
    // const companies = ["Apple", "Microsoft", "Google", "Amazon"]; // In-memory list of companies

    const fetchCompanyData = async () => {
        if (!selectedCompany) {
            setResponse("Please select a company.");
            return;
        }

        try {
            const res = await fetch(
                `http://127.0.0.1:8000/api/stocks/` + selectedCompany,
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );

            const data = await res.json();

            if (res.ok) {
                setStocks(data || []);
                setResponse("Script ran successfully");
            } else {
                setResponse(`Error: ${data.message}`);
            }
        } catch (error) {
            setResponse("Error communicating with server");
        }
    }
    const fetchCompanies = async () => {
        try {
            const res = await fetch(
                `http://127.0.0.1:8000/api/companies`,
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );

            const data = await res.json();

            if (res.ok) {
                const companyNames = data.map((item) => item.company_name);
                setCompanies(companyNames);
                setResponse("Script ran successfully");
            } else {
                setResponse(`Error: ${data.message}`);
            }
        } catch (error) {
            setResponse("Error communicating with server");
        }
    };

    useEffect(() => {
        fetchCompanies()
    }, [])

    const updateStockData = () => {
        console.log("Update stock data function called");
        setResponse("Update stock data not implemented yet");
    };

    return (
        <div className="container mt-5">
            <h1 className="text-center mb-4">Македонска Берза</h1>
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
                            onClick={fetchCompanyData}
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
