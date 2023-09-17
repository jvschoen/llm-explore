FROM python:3.9.17-slim
RUN apt-get update \
    && apt-get install sqlite3

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "db_service.py"]