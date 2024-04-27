FROM python:3.10-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends curl

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN pip3 install --no-cache-dir --upgrade pip

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin" \
POETRY_VIRTUALENVS_CREATE=false

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-cache --no-root --only=main

FROM python:3.10-slim AS base

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY . /app/

FROM base AS dev

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN pip3 install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir aiohttp-devtools

ENTRYPOINT ["adev", "runserver", ".", "--port", "3000"]

FROM base AS prod

ENTRYPOINT ["python", "app.py"]
