import os

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#DB_DIR = os.path.join(BASE_DIR, "database")
#os.makedirs(DB_DIR, exist_ok=True)
#DATABASE_URL = f"sqlite:///{os.path.join(DB_DIR, 'stock_data.db')}"

DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/stockflow_db"