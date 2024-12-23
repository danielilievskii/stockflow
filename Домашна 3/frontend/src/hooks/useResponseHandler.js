import { useState } from 'react';

function useResponseHandler() {
    const [response, setResponse] = useState("");

    const handleResponse = (result, onSuccess, success) => {
        if (result.success) {
            onSuccess(result.data);
            setResponse(success.message);
        } else {
            setResponse(result.message);
        }
    };

    const handleError = (error) => {
        setResponse(error.message || "An error occurred.");
    };

    return { response, setResponse, handleResponse, handleError };
}

export default useResponseHandler;