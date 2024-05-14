FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends curl

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN pip3 install --no-cache-dir --upgrade pip

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin" \
POETRY_VIRTUALENVS_CREATE=false

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-cache --no-root --only=main

FROM python:3.12-slim AS base

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


FROM base AS dev

ENTRYPOINT ["python", "-m", "app"]

FROM base AS prod

RUN addgroup --gid 1001 --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app
USER app

COPY . /app/

ENTRYPOINT ["python", "-OO", "-m", "app"]
