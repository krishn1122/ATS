# Vercel entry point for Flask app
from frontend.app import app

# Export the Flask app for Vercel
if __name__ == "__main__":
    app.run()