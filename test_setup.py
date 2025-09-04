"""
Test script to validate Smart ATS setup and basic functionality
"""

import sys
import os
import importlib.util
from pathlib import Path

def test_python_version():
    """Test if Python version is compatible"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print("✓ Python version is compatible:", sys.version)
        return True
    else:
        print("✗ Python version too old. Requires Python 3.8+")
        return False

def test_dependencies():
    """Test if required dependencies are available"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'flask',
        'PyPDF2',
        'docx',
        'google.generativeai',
        'pydantic',
        'requests'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'docx':
                import docx
            else:
                __import__(package)
            print(f"✓ {package} is available")
        except ImportError:
            missing.append(package)
            print(f"✗ {package} is missing")
    
    if missing:
        print(f"\\nMissing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def test_environment():
    """Test environment configuration"""
    env_file = Path('.env')
    if env_file.exists():
        print("✓ .env file exists")
        
        # Try to load environment
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('GOOGLE_API_KEY')
        secret_key = os.getenv('SECRET_KEY')
        
        if api_key:
            print("✓ GOOGLE_API_KEY is set")
        else:
            print("✗ GOOGLE_API_KEY not found in .env")
            return False
            
        if secret_key:
            print("✓ SECRET_KEY is set")
        else:
            print("⚠ SECRET_KEY not set (will use default)")
        
        return True
    else:
        print("✗ .env file not found")
        print("Copy .env.example to .env and configure it")
        return False

def test_directories():
    """Test if required directories exist"""
    required_dirs = ['backend', 'frontend', 'logs', 'uploads']
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✓ {dir_name}/ directory exists")
        else:
            print(f"✗ {dir_name}/ directory missing")
            return False
    
    return True

def test_file_structure():
    """Test if critical files exist"""
    critical_files = [
        'backend/app/main.py',
        'backend/services/ai_service.py',
        'backend/utils/document_parser.py',
        'frontend/app.py',
        'frontend/templates/base.html',
        'frontend/static/css/style.css',
        'frontend/static/js/main.js',
        'requirements.txt',
        'config.py'
    ]
    
    for file_path in critical_files:
        if Path(file_path).exists():
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            return False
    
    return True

def run_basic_import_test():
    """Test basic imports from our modules"""
    try:
        # Test backend imports
        sys.path.append('backend')
        from models.ats_models import AnalysisResult
        from utils.document_parser import DocumentParser
        print("✓ Backend modules can be imported")
        
        return True
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Smart ATS Setup Validation")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Environment", test_environment),
        ("Directories", test_directories),
        ("File Structure", test_file_structure),
        ("Import Test", run_basic_import_test)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\\n{test_name}:")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"✗ {test_name} failed with error: {e}")
    
    print("\\n" + "=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\\n🎉 All tests passed! Your Smart ATS setup is ready.")
        print("\\nNext steps:")
        print("1. Configure your .env file with API keys")
        print("2. Run: ./start.bat (Windows) or ./start.sh (Linux/Mac)")
        print("3. Open http://localhost:5000 in your browser")
    else:
        print(f"\\n❌ {total - passed} test(s) failed. Please fix the issues above.")
        
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)