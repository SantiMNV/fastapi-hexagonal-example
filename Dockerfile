FROM python:3.11-slim-bookworm

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

# Override in docker-compose: main:app vs posts_main:app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
