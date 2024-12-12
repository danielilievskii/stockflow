import React from "react";
import "../technical/techincalAnalysis.css";

const FundamentalAnalysis = () => {
    return (
        <div className="technical-analysis-container" id={"technicalID"}>
            <main className="main-content">
                <h2>Фундаментална анализа</h2>
                <section className="analysis-section">
                    <form className="analysis-form">
                        <div className="form-group">
                            <label>Одберете издавач:</label>
                            <select id="issuer" name="issuer">
                                <option value="">-- Одберете издавач --</option>
                                <option value="alkaloid">Алкалоид</option>
                                <option value="komercijalna">Комерцијална банка</option>
                            </select>
                        </div>
                        <div className="form-group">
                            <label>Одберете временски период:</label>
                            <select id="time-period" name="time-period">
                                <option value="">-- Одберете период --</option>
                                <option value="1day">1 ден</option>
                                <option value="1week">1 недела</option>
                                <option value="1month">1 месец</option>
                            </select>
                        </div>
                        <button type="submit" className="submit-btn">ПРЕДВИДИ</button>
                    </form>
                </section>
            </main>
        </div>
    );
};

export default FundamentalAnalysis;