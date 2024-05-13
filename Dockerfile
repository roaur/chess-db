# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Poetry
ENV POETRY_VERSION=1.1.11 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VENV="/opt/poetry-venv" \
    POETRY_NO_INTERACTION=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PATH="$POETRY_HOME/bin:$POETRY_VENV/bin:$PATH" \
    PYTHON_VERSION=3.11

RUN apt-get update && \
    apt-get install -y curl libpq-dev libpq5 && \
    curl -sSL https://install.python-poetry.org | python - && \
    apt-get remove -y curl && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install pipx
RUN pip install pipx

# Install Poetry using pipx
RUN pipx install poetry

# Disable virtualenv creation by poetry as the Docker container itself provides isolation
RUN /root/.local/bin/poetry config virtualenvs.create false

# Copy pyproject.toml and optionally poetry.lock if present
COPY pyproject.toml .
COPY poetry.lock* .

# Install dependencies using Poetry
RUN /root/.local/bin/poetry install

# Copy the rest of your application's code
COPY src/ .

# Make the main.py executable
RUN chmod +x main.py

# Command to run the application on container startup
CMD ["/root/.local/bin/poetry", "run", "python", "/usr/src/app/main.py"]