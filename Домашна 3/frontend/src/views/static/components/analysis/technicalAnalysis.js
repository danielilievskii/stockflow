import React, {useEffect, useState} from "react";
import {StockActions} from "../../../../actions/stockActions";
import {AnalysisActions} from "../../../../actions/analysisActions";
import Result from "./result/Result";
import useFetchCompanies from "../../../../hooks/useFetchCompanies";
import useResponseHandler from "../../../../hooks/useResponseHandler";
import AnalysisForm from "./form/Form";

const TechnicalAnalysis = () => {

    const [selectedCompany, setSelectedCompany] = useState("");
    const [selectedPeriod, setPeriod] = useState("");

    const [companyName, setCompanyName] = useState("");
    const [decision, setDecision] = useState("");

    const { companies } = useFetchCompanies();
    const { response, handleResponse, handleError } = useResponseHandler();

    const handleTechAnalysisSubmit = () => {
        if (!selectedCompany || !selectedPeriod) {
            handleError({ message: "Please select both a company and a time period." });
            return;
        }

        AnalysisActions.fetchTechAnalysisResult(selectedCompany, selectedPeriod)
            .then((result) => {
                handleResponse(result, (data) => {
                    setCompanyName(data.company_name);
                    setDecision(data.decision);
                }, { message: "Script executed successfully!" });
            })
            .catch((error) => {
                handleError(error);
            });
    };

    return (
        <main className="analysis-section">
            <h2 className="text-center">Техничка анализа</h2>

            <AnalysisForm
                selectedCompany={selectedCompany}
                setSelectedCompany={setSelectedCompany}
                selectedPeriod={selectedPeriod}
                setPeriod={setPeriod}
                companies={companies}
                handleSubmit={handleTechAnalysisSubmit}
                showPeriodField={true}
            />

            {decision && (
                <Result decision={decision} companyName={companyName}/>
            )}

            {response && <p className="text-center text-info">{response}</p>}
        </main>
    );
};

export default TechnicalAnalysis;
