FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install torch==2.2.0+cpu --index-url https://download.pytorch.org/whl/cpu

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]