#!/usr/bin/env python3
"""
Unified Server for Railway Deployment
Combines FastAPI backend and Flask frontend into a single service
"""

import os
import sys
import logging
from pathlib import Path

# Add project to path
sys.path.append(str(Path(__file__).parent))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import Flask app and configure for integration
from frontend.app import app as flask_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

# Import FastAPI backend
try:
    from backend.app.main import app as fastapi_app
    
    # Convert FastAPI to WSGI
    from fastapi.middleware.wsgi import WSGIMiddleware
    
    # Create a simple WSGI app that wraps FastAPI
    class FastAPIWrapper:
        def __init__(self, fastapi_app):
            self.fastapi_app = fastapi_app
            
        def __call__(self, environ, start_response):
            # Simple wrapper - in production, use proper ASGI->WSGI adapter
            from fastapi.testclient import TestClient
            client = TestClient(self.fastapi_app)
            
            path = environ.get('PATH_INFO', '/')
            method = environ.get('REQUEST_METHOD', 'GET')
            query_string = environ.get('QUERY_STRING', '')
            
            try:
                if method == 'GET':
                    response = client.get(path + ('?' + query_string if query_string else ''))
                elif method == 'POST':
                    # Handle POST data
                    response = client.post(path, json={})
                else:
                    response = client.request(method, path)
                
                status = f"{response.status_code} {response.reason_phrase if hasattr(response, 'reason_phrase') else 'OK'}"
                headers = [(k, v) for k, v in response.headers.items()]
                start_response(status, headers)
                return [response.content]
                
            except Exception as e:
                logger.error(f"FastAPI wrapper error: {e}")
                start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
                return [b'Internal Server Error']
    
    # Create the unified WSGI application
    app = DispatcherMiddleware(flask_app, {
        '/api': FastAPIWrapper(fastapi_app)
    })
    
except Exception as e:
    logger.error(f"Error setting up unified server: {e}")
    # Fallback to Flask only
    app = flask_app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting unified Smart ATS service on port {port}")
    
    # For Railway deployment
    if os.environ.get('RAILWAY_ENVIRONMENT'):
        # Use gunicorn for production
        import gunicorn.app.wsgiapp
        gunicorn.app.wsgiapp.run()
    else:
        # Local development
        run_simple('0.0.0.0', port, app, use_debugger=False, use_reloader=False)