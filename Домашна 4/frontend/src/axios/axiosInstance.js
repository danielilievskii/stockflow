import axios from "axios";
const axiosInstance = axios.create({
    baseURL: process.env.REACT_APP_BACKEND_HOST +'/api',
    headers: {
        'Access-Control-Allow-Origin': '*'
    }
})

export default axiosInstance;