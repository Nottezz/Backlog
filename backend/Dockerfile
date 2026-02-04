FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY ./pyproject.toml ./
COPY ./uv.lock ./
COPY ./backlog_app ./backlog_app

RUN uv sync

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "backlog_app/main.py", "--port", "8000"]
