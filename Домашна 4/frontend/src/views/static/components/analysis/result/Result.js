import {AnalysisActions} from "../../../../../actions/analysisActions";
import React from "react";

const Result = (props) => {
    const { decision, message, companyName } = props;

    return (
        <section className="result-container p-4 mb-3 bg-white rounded shadow-sm">
            <div className="text-center mb-4">
                <h3 className="fw-bold" style={{color: '#2B3051'}}>Резултати од анализата</h3>
            </div>
            <div className="result-box p-4 border rounded bg-light shadow-sm">
                <div className="d-flex justify-content-between align-items-center mb-4">
                    <div className="d-flex align-items-center">
                        <div>
                            <h5 className="mb-1" style={{color: '#2B3051'}}><strong>Компанија:</strong> {companyName}</h5>

                        </div>
                    </div>
                    <span
                        className={`badge fs-5 px-4 py-2 ${decision === "Buy" ? "bg-success" : decision === "Hold" ? "bg-warning text-dark" : "bg-danger"}`}>
                                {decision.toUpperCase()}
                            </span>
                </div>
                <hr />
                <div className="mt-2 text-center" style={{color: '#2B3051'}}>
                    <h5 className="fw-bold">{message}</h5>
                </div>
            </div>
        </section>
    )
}

export default Result