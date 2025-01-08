import { useState, useEffect } from 'react';
import './StocksTable.css'; // Assuming you have a separate CSS file for custom styles

const StocksTable = ({ data }) => {
    const [stocks, setStocks] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [stocksPerPage] = useState(10); // Adjust the number of stocks per page

    // Sort function for sorting by date in descending order (DD.MM.YYYY)
    const sortStocksByDate = (stocks) => {
        return stocks.sort((a, b) => {
            const dateA = a.date.split('.').reverse().join('-'); // Convert to YYYY-MM-DD format
            const dateB = b.date.split('.').reverse().join('-'); // Convert to YYYY-MM-DD format
            return new Date(dateB) - new Date(dateA); // Sort descending
        });
    };

    // Paginate stocks: Only show stocks for the current page
    const paginateStocks = () => {
        const sortedStocks = sortStocksByDate(stocks);
        const indexOfLastStock = currentPage * stocksPerPage;
        const indexOfFirstStock = indexOfLastStock - stocksPerPage;
        return sortedStocks.slice(indexOfFirstStock, indexOfLastStock);
    };

    // Change page handler
    const handlePageChange = (pageNumber) => {
        setCurrentPage(pageNumber);
    };

    useEffect(() => {
        if (data && data.length > 0) {
            setStocks(data);
        }
    }, [data]);

    const paginatedStocks = paginateStocks();

    // Calculate total pages
    const totalPages = Math.ceil(stocks.length / stocksPerPage);

    // Determine the page range to show (show fixed window around current page)
    const range = 1; // Always show 1 page before and after the current page
    const startPage = Math.max(1, currentPage - range);
    const endPage = Math.min(totalPages, currentPage + range + 1);

    return (
        <div>
            {paginatedStocks.length > 0 ? (
                <>
                    <table className="table table-striped table-bordered">
                        <thead>
                        <tr>
                            <th>Компанија</th>
                            <th>Датум</th>
                            <th>Цена на посл. трансакција</th>
                            <th>Макс. цена</th>
                            <th>Мин. цена</th>
                            <th>Просечна цена</th>
                            <th>Промена</th>
                            <th>Количина</th>
                            <th>Вкупен промет</th>
                        </tr>
                        </thead>
                        <tbody>
                        {paginatedStocks.map((stock, index) => (
                            <tr key={index}>
                                <td>{stock.company}</td>
                                <td>{stock.date}</td>
                                <td>{stock.closing_price}</td>
                                <td>{stock.max_price}</td>
                                <td>{stock.min_price}</td>
                                <td>{stock.avg_price}</td>
                                <td>{stock.percentage_change}%</td>
                                <td>{stock.volume}</td>
                                <td>{stock.total_turnover}</td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                    <div className="pagination-container">
                        {/* First Page Button */}
                        {currentPage > 1 && (
                            <button className="pagination-btn" onClick={() => handlePageChange(1)}>
                                First
                            </button>
                        )}

                        {/* Previous Page Button */}
                        {currentPage > 1 && (
                            <button className="pagination-btn" onClick={() => handlePageChange(currentPage - 1)}>
                                Prev
                            </button>
                        )}

                        {/* Page Numbers */}
                        {Array.from({ length: endPage - startPage }, (_, index) => startPage + index).map(pageNumber => (
                            <button
                                key={pageNumber}
                                onClick={() => handlePageChange(pageNumber)}
                                className={`pagination-btn ${currentPage === pageNumber ? 'active' : ''}`}
                            >
                                {pageNumber}
                            </button>
                        ))}

                        {/* Next Page Button */}
                        {currentPage < totalPages && (
                            <button className="pagination-btn" onClick={() => handlePageChange(currentPage + 1)}>
                                Next
                            </button>
                        )}

                        {/* Last Page Button */}
                        {currentPage < totalPages && (
                            <button className="pagination-btn" onClick={() => handlePageChange(totalPages)}>
                                Last
                            </button>
                        )}
                    </div>
                </>
            ) : (
                <p className="text-center">No stocks available</p>
            )}
        </div>
    );
};

export default StocksTable;
