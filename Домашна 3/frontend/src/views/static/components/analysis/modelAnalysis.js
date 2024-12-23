import React, {useEffect, useState} from "react";
import {StockActions} from "../../../../actions/stockActions";
import {AnalysisActions} from "../../../../actions/analysisActions";
import Result from "./result/Result";
import useFetchCompanies from "../../../../hooks/useFetchCompanies";
import useResponseHandler from "../../../../hooks/useResponseHandler";
import "./analysis.css"
import AnalysisForm from "./form/Form";

const LstmAnalysis = () => {

    const [selectedCompany, setSelectedCompany] = useState("");

    const [companyName, setCompanyName] = useState("");
    const [decision, setDecision] = useState("");

    const {companies} = useFetchCompanies();
    const {response, handleResponse, handleError} = useResponseHandler();

    const handlePriceAnalysisSubmit = () => {
        if (!selectedCompany) {
            handleError({message: "Please select a company."});
            return;
        }
    };

    return (
        <main className="analysis-section">
            <h2 className="text-center">Ценовна анализа</h2>

            <AnalysisForm
                selectedCompany={selectedCompany}
                setSelectedCompany={setSelectedCompany}
                companies={companies}
                handleSubmit={handlePriceAnalysisSubmit}
                showPeriodField={false}
            />

            {decision && (
                <Result decision={decision} companyName={companyName}/>
            )}

            {response && <p className="text-center text-info">{response}</p>}
        </main>
    );
};
export default LstmAnalysis;
