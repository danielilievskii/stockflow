import React, { useEffect, useState } from "react";
import { StockActions } from "../../../../actions/stockActions";
import { AnalysisActions } from "../../../../actions/analysisActions";
import Result from "./result/Result";
import useFetchCompanies from "../../../../hooks/useFetchCompanies";
import useResponseHandler from "../../../../hooks/useResponseHandler";
import AnalysisForm from "./form/Form";
import {useNavigate} from "react-router-dom";
import {formatClosingPrice, formatDate, sortStocksByDateAscending} from "../../../../utils/stockUtils";

const FundamentalAnalysis = () => {
    const navigate = useNavigate();
    const { companies } = useFetchCompanies();
    const { response, handleResponse, handleError } = useResponseHandler();

    const [selectedCompany, setSelectedCompany] = useState("");

    const [companyName, setCompanyName] = useState("");
    const [historicalData, setHistoricalData] = useState([]);
    const [decision, setDecision] = useState("");

    const [isLoading, setIsLoading] = useState(false);


    const handleFundamentalAnalysisSubmit = () => {
        setIsLoading(true)
        if (!selectedCompany) {
            handleError({ message: "Please select a company." });
            return;
        }

        if (decision) {
            setDecision("")
        }

        AnalysisActions.fetchFundamentalAnalysisResult(selectedCompany)
            .then((result) => {
                handleResponse(result, (data) => {
                    setCompanyName(data.company_name);
                    setDecision(data.decision);
                    setIsLoading(false)
                }, { message: "Script executed successfully!" });
            })
            .catch((error) => {
                handleError(error);
            });

        StockActions.fetchCompanyData(selectedCompany)
            .then((result) => {
                handleResponse(result, (data) => {
                    const historicalData = data.map(stock => ({
                        date: formatDate(stock.date),
                        closing_price: formatClosingPrice(stock.closing_price)
                    }));
                    setHistoricalData(sortStocksByDateAscending(historicalData));


                }, { message: "Script executed successfully!" });
            })
            .catch((error) => {
                handleError(error);
            });

    };

    const handleNavigateToResult = () => {
        navigate('/chart-data', {
            state: { historicalData }
        });
    };

    return (
        <main className="analysis-section">
            <h2 className="text-center">Фундаментална анализа</h2>

            <AnalysisForm
                selectedCompany={selectedCompany}
                setSelectedCompany={setSelectedCompany}
                companies={companies}
                handleSubmit={handleFundamentalAnalysisSubmit}
                showPeriodField={false}
                isLoading={isLoading}
            />

            {decision && (
                <>
                    <Result decision={decision} message={AnalysisActions.getDecisionMessage(decision)} companyName={companyName}/>

                    <div className="text-center mt-2">
                        <button onClick={handleNavigateToResult} className="btn btn-warning">
                            Погледни ценовен график
                        </button>
                    </div>
                </>
            )}

            {/*{response && <p className="text-center text-info">{response}</p>}*/}
        </main>
    );
};

export default FundamentalAnalysis;
