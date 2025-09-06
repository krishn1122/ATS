# Vercel serverless function for Flask app
from flask import Flask
import sys
import os

# Add the root directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from frontend.app import app
except ImportError:
    # Fallback if import fails
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return "Smart ATS Frontend - Import Error. Please check deployment."

# Export the Flask app for Vercel
# This is required for @vercel/python
if __name__ == "__main__":
    app.run()