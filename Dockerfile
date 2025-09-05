# Railway Deployment Dockerfile - Updated
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (excluding .env files for security)
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY config.py .
COPY main.py .

# Create necessary directories
RUN mkdir -p logs uploads

# Railway provides PORT environment variable
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]