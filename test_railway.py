#!/usr/bin/env python3
"""
Railway Deployment Test Script
Tests if the application is ready for Railway deployment
"""

import os
import sys
import importlib.util
from pathlib import Path

def test_environment_variables():
    """Test if required environment variables are available"""
    print("Testing environment variables...")
    
    # Required for Railway
    required_vars = ["GOOGLE_API_KEY", "SECRET_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Set these in Railway dashboard before deployment")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    required_modules = [
        "fastapi",
        "uvicorn", 
        "flask",
        "google.generativeai",
        "requests",
        "pydantic"
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
        except ImportError:
            failed_imports.append(module)
    
    if failed_imports:
        print(f"❌ Failed to import: {', '.join(failed_imports)}")
        return False
    else:
        print("✅ All required modules can be imported")
        return True

def test_file_structure():
    """Test if required files exist"""
    print("Testing file structure...")
    
    required_files = [
        "Dockerfile",
        "railway.json", 
        "main.py",
        "requirements.txt",
        "backend/app/main.py",
        "frontend/app.py"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files exist")
        return True

def test_app_initialization():
    """Test if apps can be initialized"""
    print("Testing app initialization...")
    
    try:
        # Test backend import
        sys.path.append('.')
        from backend.app.main import app as backend_app
        print("✅ Backend app can be imported")
        
        # Test frontend import  
        from frontend.app import create_app
        frontend_app = create_app()
        print("✅ Frontend app can be created")
        
        return True
        
    except Exception as e:
        print(f"❌ App initialization failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 Railway Deployment Readiness Test")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_imports,
        test_environment_variables,
        test_app_initialization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 Ready for Railway deployment!")
        print("\nNext steps:")
        print("1. Push code to GitHub")
        print("2. Create Railway project")
        print("3. Set environment variables")
        print("4. Deploy!")
        return True
    else:
        print("❌ Fix the issues above before deploying")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)