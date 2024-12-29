export const sortStocksByDateAscending = (stocks) => {
    return stocks.sort((a, b) => {
        return new Date(a.date) - new Date(b.date);
    });
};

export const formatClosingPrice = (price) => {
    return price.replace('.', '').split(',')[0];
};

export const formatDate = (dateString) => {
    return dateString.split('.').reverse().join('-');
};