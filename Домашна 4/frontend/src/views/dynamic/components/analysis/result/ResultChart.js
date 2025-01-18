import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import { useLocation, useNavigate } from "react-router-dom";
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const ResultChart = () => {
    const location = useLocation();
    const { historicalData, predictedData } = location.state || {};

    const [filteredData, setFilteredData] = useState(historicalData);

    const navigate = useNavigate();

    const handleBackClick = () => {
        navigate(-1);
    };

    const handleFilterChange = (filter) => {
        const now = new Date();
        let filtered;

        switch (filter) {
            case 'lastWeek':
                const lastWeek = new Date(now);
                lastWeek.setDate(now.getDate() - 7);
                filtered = historicalData.filter(item => {
                    const date = new Date(item.date);
                    return date >= lastWeek && date <= now;
                });
                break;
            case 'lastMonth':
                const lastMonth = new Date(now);
                lastMonth.setMonth(now.getMonth() - 1);
                filtered = historicalData.filter(item => {
                    const date = new Date(item.date);
                    return date >= lastMonth && date <= now;
                });
                break;
            case 'lastYear':
                const lastYear = new Date(now);
                lastYear.setFullYear(now.getFullYear() - 1);
                filtered = historicalData.filter(item => {
                    const date = new Date(item.date);
                    return date >= lastYear && date <= now;
                });
                break;
            case 'lifetime':
            default:
                filtered = historicalData;
        }

        setFilteredData(filtered);
    };

    const chartData = {
        labels: [
            ...filteredData.map(item => item.date),
            ...(predictedData?.map(item => item.date) || [])
        ],
        datasets: [
            {
                label: 'Historical Prices',
                data: filteredData.map(item => item.closing_price),
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
            },
            ...(predictedData ? [
                {
                    label: 'Predicted Prices',
                    data: [
                        ...Array(Math.max(0, filteredData.length - 1)).fill(null),
                        filteredData.length > 0 ? filteredData[filteredData.length - 1].price : null,
                        ...predictedData.map(item => item.price)
                    ],
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    fill: true,
                }
            ] : []),
        ]
    };

    const options = {
        scales: {
            y: {
                suggestedMin: 80,
                suggestedMax: 110
            }
        }
    };

    return (
        <div className="analysis-section">
            <h2 className="text-center mb-4">Ценовен график</h2>

            {/* Filter Buttons */}
            <div className="text-center mb-4">
                <div className="btn-group" style={{ gap: '10px' }} role="group">
                    <button className="btn btn-danger" onClick={() => handleFilterChange('lastWeek')}>Последни 7 дена</button>
                    <button className="btn btn-danger" onClick={() => handleFilterChange('lastMonth')}>Последни 30 дена</button>
                    <button className="btn btn-danger" onClick={() => handleFilterChange('lastYear')}>Последна година</button>
                    <button className="btn btn-danger" onClick={() => handleFilterChange('lifetime')}>Последни 10 години</button>
                </div>
            </div>

            {/* Chart Container */}
            <div className="d-flex justify-content-center align-content-center align-items-center flex-column mb-4">
                <div style={{ width: '60vw',  }}>
                    <Line data={chartData} options={options} />
                </div>

                {/* Back Button */}
                <div className="mb-3">
                    <button className="btn btn-secondary" onClick={handleBackClick}>
                        Назад
                    </button>
                </div>
            </div>


        </div>
    );
};

export default ResultChart;
