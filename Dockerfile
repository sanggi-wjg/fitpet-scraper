FROM python:3.12-slim AS base
EXPOSE 8000
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install --only=main --no-interaction --no-ansi --no-root

COPY . .

FROM base AS web
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM base AS worker
CMD ["celery", "-A", "app.task.celery", "worker", "--loglevel=info"]

FROM base AS beat
CMD ["celery", "-A", "app.task.celery", "beat", "--loglevel=info"]

