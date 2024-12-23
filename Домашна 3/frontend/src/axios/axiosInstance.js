import axios from "axios";
export const AUTH_TOKEN = 'AUTH_TOKEN';

const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:8000'+'/api',
    headers: {
        'Access-Control-Allow-Origin': '*'
    }
})

export default axiosInstance;