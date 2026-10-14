FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev

COPY app.py .

EXPOSE 5001

CMD ["uv", "run", "--no-dev", "python", "app.py"]
