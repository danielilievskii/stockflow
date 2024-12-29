# **Домашна 3: Technical, fundamental (NLP model) и price (LSTM model) analysis**

# Функциски и нефункциски барања
На следниот линк се наоѓа видео каде се покажуваат сите функциски и нефункциски барања од Домашна 1.
> https://www.youtube.com/watch?v=aTgbCe7ekMc

# Упатство за користење

## Инсталација

```bash
git clone https://github.com/danielilievskii/stockflow.git
cd "stockflow/Домашна 3"
```

## База на податоци - PostgreSQL
```bash
docker-compose up -d
```

## Frontend дел - React
```bash
cd frontend

# Симнување зависности
npm install

# Стартување на апликација
npm start
```

## Backend дел - FastAPI
```bash
cd backend

# Стартување на апликацијата
uvicorn app.main:app --reload
```

## Опционално: Креирање виртуелна околина

```bash
# Креирање на виртуелна околина
python3 -m venv venv

# Активирање на виртуелна околина
# На Windows
venv\Scripts\activate
# На macOS/Linux
source venv/bin/activate
```

## Инсталирање на потребните зависности

```bash
pip install -r requirements.txt
```