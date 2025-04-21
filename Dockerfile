FROM python:3.13.2-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set workdir
WORKDIR /app

# Copy pyproject and poetry.lock
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "atropos.main:app", "--host", "0.0.0.0", "--port", "8000"]
