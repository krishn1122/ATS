#!/usr/bin/env python3
"""
Smart ATS - Railway Deployment Launcher
Supports both local development and Railway production deployment
"""

import sys
import subprocess
import os
import threading
import time
from pathlib import Path

# Add current directory to Python path
sys.path.append(str(Path(__file__).parent))

def check_setup():
    """Run setup validation"""
    print("Validating Smart ATS setup...")
    try:
        result = subprocess.run([sys.executable, "test_setup.py"], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Setup validation failed: {e}")
        return False

def start_backend():
    """Start the FastAPI backend server"""
    try:
        import uvicorn
        port = int(os.environ.get("BACKEND_PORT", 8001))
        uvicorn.run(
            "backend.app.main:app",
            host="0.0.0.0",
            port=port,
            log_level="info",
            reload=False
        )
    except Exception as e:
        print(f"Backend startup error: {e}")

def start_frontend():
    """Start the Flask frontend server"""
    try:
        # Import Flask app
        from frontend.app import app
        
        # Configure for production
        app.config['ENV'] = 'production'
        app.config['DEBUG'] = False
        
        port = int(os.environ.get("PORT", 5000))
        app.run(
            host="0.0.0.0",
            port=port,
            debug=False
        )
    except Exception as e:
        print(f"Frontend startup error: {e}")
        sys.exit(1)

def railway_deployment():
    """Handle Railway deployment"""
    print("🚀 Starting Smart ATS on Railway...")
    
    # Validate environment variables
    required_vars = ["GOOGLE_API_KEY", "SECRET_KEY"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your Railway dashboard.")
        sys.exit(1)
    
    print("✅ Environment variables validated")
    
    # For Railway deployment - single service mode
    deployment_mode = os.environ.get("DEPLOYMENT_MODE", "frontend")
    
    if deployment_mode == "backend":
        print("Starting backend service...")
        start_backend()
    else:
        print("Starting frontend service...")
        # Start backend in background thread for integrated deployment
        if not os.environ.get("BACKEND_URL") or os.environ.get("BACKEND_URL") == "http://localhost:8000":
            print("Starting integrated backend...")
            backend_thread = threading.Thread(target=start_backend, daemon=True)
            backend_thread.start()
            time.sleep(3)  # Give backend time to start
        
        start_frontend()

def start_services():
    """Start backend and frontend services"""
    print("\\nStarting Smart ATS services...")
    
    # Check if .env exists
    if not Path(".env").exists():
        print("Creating .env from template...")
        if Path(".env.example").exists():
            subprocess.run(["copy" if os.name == "nt" else "cp", 
                          ".env.example", ".env"], shell=True)
            print("Please edit .env file with your API keys before continuing.")
            return False
        else:
            print("No .env.example found!")
            return False
    
    try:
        if os.name == "nt":  # Windows
            subprocess.run(["start.bat"], shell=True)
        else:  # Unix/Linux/Mac
            subprocess.run(["chmod", "+x", "start.sh"])
            subprocess.run(["./start.sh"])
        return True
    except Exception as e:
        print(f"Failed to start services: {e}")
        return False

def main():
    """Main function - detects environment and runs accordingly"""
    print("=" * 60)
    print("🚀 Smart ATS - Professional Resume Analysis System")
    print("=" * 60)
    
    # Check if running on Railway
    if os.environ.get("RAILWAY_ENVIRONMENT") or os.environ.get("PORT"):
        railway_deployment()
        return True
    
    # Local development mode
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            return check_setup()
        elif sys.argv[1] == "--start":
            if check_setup():
                return start_services()
            else:
                print("Setup validation failed. Please fix issues before starting.")
                return False
        elif sys.argv[1] == "--help":
            print("Usage:")
            print("  python main.py           - Interactive mode")
            print("  python main.py --test    - Run setup validation only")
            print("  python main.py --start   - Validate and start services")
            print("  python main.py --help    - Show this help")
            return True
    
    # Interactive mode for local development
    print("\\nOptions:")
    print("1. Validate setup")
    print("2. Start services")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\\nSelect option (1-3): ").strip()
            
            if choice == "1":
                check_setup()
                break
            elif choice == "2":
                if check_setup():
                    start_services()
                else:
                    print("\\nSetup validation failed. Please fix issues before starting.")
                break
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please select 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\\nGoodbye!")
            break
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\\nOperation cancelled.")
        sys.exit(1)