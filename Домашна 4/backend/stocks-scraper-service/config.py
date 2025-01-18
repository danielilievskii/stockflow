import os

# DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = "postgresql://postgres:postgres@database:5432/stockflow_db"

BASE_URL = "https://www.mse.mk/en/stats/symbolhistory/ALK"
HEADERS = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.mse.mk',
}