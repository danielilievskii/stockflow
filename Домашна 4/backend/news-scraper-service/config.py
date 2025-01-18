# DATABASE_URL = os.getenv("DATABASE_URL")
#DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/stockflow_db"
DATABASE_URL = "postgresql://postgres:postgres@database:5432/stockflow_db"

BASE_URL = 'https://www.mse.mk/en/symbol/'
COMPANIES_URL = "https://www.mse.mk/en/stats/symbolhistory/ALK"

CONTENT_URL = "https://api.seinet.com.mk/public/documents/single"
ATTACHMENT_URL = "https://api.seinet.com.mk/public/documents/attachment"

HEADERS = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.mse.mk',
}