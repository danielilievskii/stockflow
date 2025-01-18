import React, {useEffect, useState} from "react";
import {StockActions} from "../../../../actions/stockActions";
import {AnalysisActions} from "../../../../actions/analysisActions";
import Result from "./result/Result";
import useFetchCompanies from "../../../../hooks/useFetchCompanies";
import useResponseHandler from "../../../../hooks/useResponseHandler";
import "./analysis.css"
import AnalysisForm from "./form/Form";
import { formatClosingPrice, sortStocksByDateAscending, formatDate  } from '../../../../utils/stockUtils';
import ResultChart from "./result/ResultChart";
import { useNavigate } from "react-router-dom";
import {type} from "@testing-library/user-event/dist/type";
const LstmAnalysis = () => {
    const navigate = useNavigate();
    const {companies} = useFetchCompanies();
    const {response, handleResponse, handleError} = useResponseHandler();

    const [selectedCompany, setSelectedCompany] = useState("");

    const [company, setCompany] = useState("");
    const [historicalData, setHistoricalData] = useState([]);
    const [predictedData, setPredictedData] = useState([]);
    const [decision, setDecision] = useState("");

    const [isLoading, setIsLoading] = useState(false);

    const [lastPrice, setLastPrice] = useState("");
    const [predictedPrice, setPredictedPrice] = useState("");

    const formatPrice = (price) => {
        const priceString = price.toString();
        return priceString.split('.')[0];
    };

    const handlePriceAnalysisSubmit = () => {
        setIsLoading(true)

        if (!selectedCompany) {
            handleError({message: "Please select a company."});
            return;
        }

        if (decision) {
            setDecision("")
            setLastPrice("")
            setPredictedPrice("")
            setPredictedData([])
            setHistoricalData([])
        }

        setCompany(selectedCompany)


        AnalysisActions.fetchPriceAnalysisResult(selectedCompany)
            .then((result) => {
                handleResponse(result, (data) => {
                    // setCompanyName(data.company_name);
                    setPredictedData(data.predictions);
                }, { message: "Script executed successfully!" });
            })
            .catch((error) => {
                handleError(error);
            });

        StockActions.fetchCompanyData(selectedCompany)
            .then((result) => {
                handleResponse(result, (data) => {
                    // setCompanyName(data.company_name);
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

    useEffect(() => {
        if (historicalData.length > 0 && predictedData.length > 0) {
            const lastHistoricalPrice = Number(historicalData[historicalData.length - 1].closing_price);
            const firstPredictedPrice = Number(formatPrice(predictedData[0].price));

            setLastPrice(lastHistoricalPrice)
            setPredictedPrice(firstPredictedPrice)

            if (firstPredictedPrice > lastHistoricalPrice) {
                setDecision('Buy');
            } else if (firstPredictedPrice == lastHistoricalPrice) {
                setDecision('Hold');
            } else {
                setDecision('Sell');
            }

            setIsLoading(false)
        }
        // console.log("Historical Data:", historicalData);
        // console.log("Predicted Data:", predictedData);
    }, [historicalData, predictedData]);

    const handleNavigateToResult = () => {
        navigate('/chart-data', {
            state: { historicalData, predictedData }
        });
    };

    const getDecisionMessageCustom = (decision) => {
        switch (decision) {
            case "Buy":
                return `Предлагаме да купите акции од оваа компанија бидејќи анализата покажува позитивен тренд. Последната продадена акција беше ${lastPrice} денари, а предвидената цена за утрешниот ден се очекува да достигне ${predictedPrice} денари.`;
            case "Hold":
                return `Предлагаме да ги задржите вашите акции засега бидејќи анализата покажува неутрален тренд. Последната продадена акција беше ${lastPrice} денари, а цената се очекува да остане иста за утрешниот ден.`;
            case "Sell":
                return `Предлагаме да ги продадете вашите акции бидејќи анализата покажува негативен тренд. Последната продадена акција беше ${lastPrice} денари, а предвидената цена за утрешниот ден се очекува да падне на ${predictedPrice} денари.`;
            default:
                return "";
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
                isLoading={isLoading}

            />

            {decision && (
                <>
                    <Result decision={decision} message={getDecisionMessageCustom(decision)} companyName={company}/>

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
export default LstmAnalysis;
