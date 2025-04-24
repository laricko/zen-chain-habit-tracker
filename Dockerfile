# Base image with Python
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/root/.local/bin:$PATH"

# Install system dependencies
RUN apt update && apt-get install -y --no-install-recommends \
    curl \
    cron \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set working directory
WORKDIR /app

# Copy only dependency files
COPY pyproject.toml poetry.lock ./

# Install Python dependencies
RUN poetry install --no-root

# Copy project source code
COPY src/ .

# Set up cron to use environment variables from the container
RUN echo "0 * * * * . /etc/container_env.sh && cd /app && /usr/local/bin/python -c 'from app.services.progress import create_progress_for_all_users; create_progress_for_all_users()' >> /cron_logs.log 2>&1" > /etc/cron.d/create_progress \
    && chmod 0644 /etc/cron.d/create_progress \
    && crontab /etc/cron.d/create_progress

# Generate /etc/container_env.sh at runtime and start cron + app
CMD bash -c 'printenv | sed "s/^/export /" > /etc/container_env.sh && cron && python3 main.py'