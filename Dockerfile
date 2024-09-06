# Use an official Python runtime as the base image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y wget curl && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# # Copy the pyproject.toml and poetry.lock files into the container
# COPY pyproject.toml poetry.lock ./

# Copy the rest of the application code
COPY . .

# Install the project dependencies
RUN poetry install --no-interaction --no-ansi


# Create directories for persisting files
RUN mkdir -p public/vo public/speech_in public/analyze

# Make these directories writable by the application
RUN chmod -R 777 public/vo public/speech_in public/analyze

# Expose the port the app runs on
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV QUART_APP=api
ENV QUART_ENV=production

# Expose port 8000
EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.api:app"]
