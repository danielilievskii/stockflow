import axiosInstance from "../axios/axiosInstance";

export const AnalysisActions = {
    fetchTechAnalysisResult: (companyName, timeframe) => {
        return axiosInstance
            .post(
                "/technical-analysis",
                { company_name: companyName, timeframe: timeframe },
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            )
            .then((response) => {
                return { success: true, data: response.data };
            })
            .catch((error) => {
                return {
                    success: false,
                    message: error.response
                        ? `Error: ${error.response.data.detail}`
                        : "Error communicating with server",
                };
            });
    },

    fetchFundamentalAnalysisResult: (companyName) => {
        return axiosInstance
            .post(
                "/fundamental-analysis",
                { company_name: companyName},
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            )
            .then((response) => {
                return { success: true, data: response.data };
            })
            .catch((error) => {
                return {
                    success: false,
                    message: error.response
                        ? `Error: ${error.response.data.detail}`
                        : "Error communicating with server",
                };
            });
    },

    fetchPriceAnalysisResult: (companyName) => {
        return axiosInstance
            .post(
                "/lstm-analysis",
                { company_name: companyName},
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            )
            .then((response) => {
                return { success: true, data: response.data };
            })
            .catch((error) => {
                return {
                    success: false,
                    message: error.response
                        ? `Error: ${error.response.data.detail}`
                        : "Error communicating with server",
                };
            });
    },

    getDecisionMessage: (decision) => {
        switch (decision) {
            case "Buy":
                return "Предлагаме да купите акции од оваа компанија бидејќи анализата покажува позитивен тренд.";
            case "Hold":
                return "Предлагаме да ги задржите вашите акции засега бидејќи анализата покажува неутрален тренд.";
            case "Sell":
                return "Предлагаме да ги продадете вашите акции бидејќи анализата покажува негативен тренд.";
            default:
                return "";
        }
    }
};
