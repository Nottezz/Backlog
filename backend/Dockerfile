FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY --from=ghcr.io/astral-sh/uv:0.9.29 /uv /uvx /bin/

WORKDIR /app

COPY ./pyproject.toml ./
COPY ./uv.lock ./
COPY ./backlog_app ./backlog_app

RUN uv sync

EXPOSE 8000
CMD ["sh", "-c", "cd backlog_app && uv run alembic upgrade head && cd .. && uv run fastapi run backlog_app/main.py --port 8000"]
