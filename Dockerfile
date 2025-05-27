FROM python:3.13-slim

WORKDIR /app
COPY pyproject.toml .

RUN pip install uv && \
    uv pip install --system -e .

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
