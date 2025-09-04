#!/usr/bin/env python3
"""
Smart ATS - Main Launcher Script
Validates setup and provides startup options
"""

import sys
import subprocess
import os
from pathlib import Path

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
    """Main function"""
    print("=" * 60)
    print("🚀 Smart ATS - Professional Resume Analysis System")
    print("=" * 60)
    
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
    
    # Interactive mode
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