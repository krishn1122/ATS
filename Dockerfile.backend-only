# Railway Backend Deployment Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements (ensure this file exists)
COPY backend-requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code only
COPY backend/ ./backend/
COPY config.py .

# Create necessary directories
RUN mkdir -p logs uploads

# Railway provides PORT environment variable
EXPOSE $PORT

# Run the backend only - Railway sets PORT automatically
CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]