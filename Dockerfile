FROM python:3.9-buster as base
FROM base as dev

ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=5000

WORKDIR /app

RUN apt update && \
    apt install -y postgresql-client

COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

CMD uvicorn application:pypi_app --host ${HOST} --port ${PORT} --reload
