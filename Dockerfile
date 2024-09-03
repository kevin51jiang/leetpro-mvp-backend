# Use an official Python runtime as the base image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y wget curl && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files into the container
COPY pyproject.toml poetry.lock ./

# Install the project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

# Create directories for audio files
RUN mkdir -p public/vo public/speech_in

# Expose the port the app runs on
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV QUART_APP=api
ENV QUART_ENV=production

# Run the application
CMD ["poetry", "run", "hypercorn", "api", "--bind", "0.0.0.0:5000"]
