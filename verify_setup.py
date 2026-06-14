#!/usr/bin/env python3

import subprocess
import sys
import time

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def check_python():
    """Check if Python is installed"""
    print_header("Checking Python")
    try:
        version = subprocess.check_output(['python3', '--version']).decode().strip()
        print_success(f"Python is installed: {version}")
        return True
    except:
        try:
            version = subprocess.check_output(['python', '--version']).decode().strip()
            print_success(f"Python is installed: {version}")
            return True
        except:
            print_error("Python is not installed!")
            return False

def check_node():
    """Check if Node.js is installed"""
    print_header("Checking Node.js")
    try:
        version = subprocess.check_output(['node', '--version']).decode().strip()
        print_success(f"Node.js is installed: {version}")
        return True
    except:
        print_error("Node.js is not installed!")
        return False

def check_npm():
    """Check if npm is installed"""
    print_header("Checking npm")
    try:
        version = subprocess.check_output(['npm', '--version']).decode().strip()
        print_success(f"npm is installed: {version}")
        return True
    except:
        print_error("npm is not installed!")
        return False

def check_backend_files():
    """Check if backend files exist"""
    print_header("Checking Backend Files")
    required_files = [
        'backend/app.py',
        'backend/information_agent.py',
        'backend/legal_assistant.py',
        'backend/config.py',
        'backend/requirements.txt'
    ]
    
    import os
    for file in required_files:
        if os.path.exists(file):
            print_success(f"Found: {file}")
        else:
            print_error(f"Missing: {file}")
            return False
    return True

def check_frontend_files():
    """Check if frontend files exist"""
    print_header("Checking Frontend Files")
    required_files = [
        'frontend/package.json',
        'frontend/src/App.js',
        'frontend/src/components/TopicCards.js',
        'frontend/src/components/LegalDetail.js',
        'frontend/src/components/AIAssistant.js'
    ]
    
    import os
    for file in required_files:
        if os.path.exists(file):
            print_success(f"Found: {file}")
        else:
            print_error(f"Missing: {file}")
            return False
    return True

def check_env_file():
    """Check if .env file exists"""
    print_header("Checking Environment Configuration")
    import os
    if os.path.exists('backend/.env'):
        print_success("Backend .env file exists")
        
        # Check if it has GOOGLE_API_KEY
        with open('backend/.env', 'r') as f:
            content = f.read()
            if 'GOOGLE_API_KEY' in content:
                if 'your_google_api_key_here' in content or content.count('=') == 0:
                    print_error(".env exists but GOOGLE_API_KEY is not configured!")
                    return False
                else:
                    print_success("GOOGLE_API_KEY is configured")
                    return True
            else:
                print_error(".env file doesn't have GOOGLE_API_KEY!")
                return False
    else:
        print_info(".env file not found - you'll need to create it")
        print_info("Copy backend/.env.example to backend/.env and fill in your API key")
        return False

def check_legal_documents():
    """Check if legal documents folder exists"""
    print_header("Checking Legal Documents")
    import os
    
    if os.path.exists('backend/legal_documents'):
        print_success("legal_documents folder exists")
        
        # Count PDFs
        pdfs = [f for f in os.listdir('backend/legal_documents') if f.endswith('.pdf')]
        if pdfs:
            print_success(f"Found {len(pdfs)} PDF(s): {', '.join(pdfs)}")
            return True
        else:
            print_info("No PDFs found in legal_documents/ - the system will have nothing to process")
            return True  # Not a hard error
    else:
        print_error("legal_documents folder doesn't exist!")
        return False

def main():
    print("\n")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   LegalX AI Knowledge Centre - Setup Verification       ║")
    print("╚══════════════════════════════════════════════════════════╝")
    
    checks = [
        ("Python", check_python),
        ("Node.js", check_node),
        ("npm", check_npm),
        ("Backend Files", check_backend_files),
        ("Frontend Files", check_frontend_files),
        ("Environment Configuration", check_env_file),
        ("Legal Documents", check_legal_documents),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print_error(f"Error checking {name}: {e}")
            results[name] = False
    
    # Summary
    print_header("Summary")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print_success("All checks passed! You're ready to run:")
        print("\n  Terminal 1: ollama serve")
        print("  Terminal 2: cd backend && source venv/bin/activate && python app.py")
        print("  Terminal 3: cd frontend && npm start")
        return 0
    else:
        print_error("Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
