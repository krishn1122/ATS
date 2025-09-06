# Vercel entry point for Flask app
import sys
import os

# Add the root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.app import app

# Export the Flask app for Vercel
# This is the main WSGI application that Vercel will use
app = app

if __name__ == "__main__":
    app.run(debug=False)