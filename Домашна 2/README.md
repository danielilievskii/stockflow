# **Домашна 2: Архитектура, mockups и tech prototype**

# Tech prototype
На следниот линк се наоѓа кратко видео каде се покажува како работи техничкиот прототип.
> https://www.youtube.com/watch?v=hyn2v7SX9zc


# Упатство за користење

Зависностите потребни за користење на оваа демо апликација се наоѓаат во **requirements.txt**.

## Инсталација

```bash
git clone https://github.com/danielilievskii/stockflow.git
cd "stockflow/Домашна 2"
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