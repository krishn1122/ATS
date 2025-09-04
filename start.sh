#!/bin/bash

# Smart ATS Startup Script for Linux/Mac

echo "Starting Smart ATS Application..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file with your API keys and configuration"
    exit 1
fi

# Create necessary directories
mkdir -p logs uploads

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is required but not installed. Please install pip3."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Load environment variables
source .env

# Check if Google API key is set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "GOOGLE_API_KEY is not set in .env file. Please add your Google Gemini API key."
    exit 1
fi

# Start backend server in background
echo "Starting backend server..."
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 5

# Start frontend server
echo "Starting frontend server..."
cd frontend
python3 app.py &
FRONTEND_PID=$!
cd ..

echo "Smart ATS is now running!"
echo "Frontend: http://localhost:5000"
echo "Backend API: http://localhost:8000"
echo "API Documentation: http://localhost:8000/api/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo "Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Wait for processes
wait