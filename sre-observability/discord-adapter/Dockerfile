FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev

COPY app.py .

RUN useradd --system --no-create-home --shell /usr/sbin/nologin appuser \
    && mkdir -p /app/.cache/uv \
    && chown -R appuser:appuser /app
    
ENV UV_CACHE_DIR=/app/.cache/uv

USER appuser

EXPOSE 5001

CMD ["uv", "run", "--no-dev", "python", "app.py"]
