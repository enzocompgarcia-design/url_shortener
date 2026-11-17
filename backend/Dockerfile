
FROM python:3.14-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project

COPY . .

ENV PYTHONPATH="/app/src:/app"

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "uvicorn", "src.app.main:app", "--app-dir", ".", "--host", "0.0.0.0", "--port", "8000"]
