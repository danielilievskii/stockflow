const AnalysisForm = ({
                          selectedCompany,
                          setSelectedCompany,
                          selectedPeriod,
                          setPeriod,
                          companies,
                          showPeriodField,
                          handleSubmit,
                            isLoading
                      }) => {
    return (
        <section className="analysis-container p-4 mb-5 bg-white rounded-3 shadow-sm">
            <form className="analysis-form">
                <div className="form-group mb-4">
                    <label htmlFor="companySelect" className="form-label fw-bold">
                        Изберете компанија:
                    </label>
                    <select
                        id="companySelect"
                        className="form-select"
                        value={selectedCompany}
                        onChange={(e) => setSelectedCompany(e.target.value)}
                    >
                        <option value="">Сите</option>
                        {companies.map((company, index) => (
                            <option key={index} value={company}>
                                {company}
                            </option>
                        ))}
                    </select>
                </div>

                {showPeriodField && (
                    <div className="form-group mb-4">
                        <label className="form-label fw-bold">Одберете временски период:</label>
                        <select
                            id="time-period"
                            className="form-select"
                            name="time-period"
                            value={selectedPeriod}
                            onChange={(e) => setPeriod(e.target.value)}
                        >
                            <option value="">-- Одберете период --</option>
                            <option value="1">1 ден</option>
                            <option value="7">1 недела</option>
                            <option value="30">1 месец</option>
                        </select>
                    </div>
                )}

                <div className="d-flex justify-content-center">
                    <button
                        disabled={isLoading}
                        type="button"
                        className="btn submit-btn"
                        onClick={handleSubmit}
                    >
                        ИЗВРШИ
                    </button>
                </div>
            </form>
        </section>
    );
};

export default AnalysisForm;