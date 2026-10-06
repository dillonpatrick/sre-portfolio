FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY app.py .

EXPOSE 8000

CMD [ "uv","run","--no-dev", "python", "app.py" ]

