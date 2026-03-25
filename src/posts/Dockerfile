FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 8001

CMD ["uv", "run", "uvicorn", "src.posts.main:app", "--host", "0.0.0.0", "--port", "8001"]
