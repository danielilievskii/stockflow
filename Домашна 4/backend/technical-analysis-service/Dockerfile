FROM python:3.12-slim

WORKDIR /app

COPY ./backend/technical-analysis-service/requirements.txt .

COPY ./backend/util/dist/preprocess-0.1.0.tar.gz .

RUN pip install -r requirements.txt

RUN pip install preprocess-0.1.0.tar.gz

COPY ./backend/technical-analysis-service .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]