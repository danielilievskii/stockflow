import React from "react";
import "../technical/techincalAnalysis.css";

const ModelAnalysis = () => {
    return (

        <main className="analysis-section">
            <h2>Ценовна анализа</h2>
            <section className="analysis-container">
                <form className="analysis-form d-flex flex-column gap-4">
                    <div className="form-group">
                        <label className="form-label">Одберете издавач:</label>
                        <select id="issuer" className="form-select" name="issuer">
                            <option value="">-- Одберете издавач --</option>
                            <option value="alkaloid">Алкалоид</option>
                            <option value="komercijalna">Комерцијална банка</option>
                        </select>
                    </div>
                    <div className="form-group">
                        <label className="form-label">Одберете временски период:</label>
                        <select id="time-period" className="form-select" name="time-period">
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

    );
};

export default ModelAnalysis;