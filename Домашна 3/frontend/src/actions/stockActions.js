import axiosInstance from "../axios/axiosInstance";

export const StockActions = {
    fetchCompanies: () => {
        return axiosInstance
            .get('/companies')
            .then((res) => {
                const companyNames = res.data.map((item) => item.company_name);
                return { success: true, data: companyNames };
            })
            .catch((error) => {
                return {
                    success: false,
                    message: error.response
                        ? `Error: ${error.response.data.message}`
                        : "Error communicating with server",
                };
            });
    },

    fetchCompanyData: (selectedCompany) => {
        if (!selectedCompany) {
            return Promise.resolve({ success: false, message: "Please select a company." });
        }

        return axiosInstance
            .get(`/stocks/${selectedCompany}`)
            .then((res) => {
                return { success: true, data: res.data || [] };
            })
            .catch((error) => {
                return {
                    success: false,
                    message: error.response
                        ? `Error: ${error.response.data.message}`
                        : "Error communicating with server",
                };
            });
    },
}