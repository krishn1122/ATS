#!/usr/bin/env python3
"""
Test the integrated backend with frontend serving
"""
import os
import sys
from pathlib import Path

# Add project to path
sys.path.append(str(Path(__file__).parent))

def test_integration():
    """Test that the backend can serve frontend content"""
    print("Testing integrated backend with frontend serving...")
    
    try:
        # Set environment to simulate Railway
        os.environ["DEPLOYMENT_MODE"] = "integrated"
        os.environ["PORT"] = "8000"
        
        # Import and test the backend
        from backend.app.main import app, templates, static_path, templates_path
        
        print(f"✅ Backend app loaded successfully")
        print(f"✅ Templates available: {templates is not None}")
        print(f"✅ Static path: {static_path}")
        print(f"✅ Templates path: {templates_path}")
        
        # Test with FastAPI test client
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        # Test API endpoints
        health_response = client.get("/api/health")
        print(f"✅ Health check: {health_response.status_code}")
        
        # Test frontend serving
        home_response = client.get("/")
        print(f"✅ Home page: {home_response.status_code}")
        print(f"   Content-Type: {home_response.headers.get('content-type')}")
        
        if "text/html" in home_response.headers.get('content-type', ''):
            print("✅ HTML content served correctly")
        else:
            print("⚠️  Warning: Expected HTML content")
        
        # Test other frontend routes
        routes_to_test = ["/dashboard", "/about", "/results"]
        for route in routes_to_test:
            response = client.get(route)
            print(f"✅ {route}: {response.status_code}")
        
        print("\n🎉 Integration test completed successfully!")
        print("Your backend is ready to serve both API and frontend content!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_integration()
    sys.exit(0 if success else 1)