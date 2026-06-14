@echo off
REM LegalX AI Knowledge Centre - Quick Start Script for Windows

echo.
echo 🚀 Starting LegalX AI Knowledge Centre Setup...
echo.

REM Check Python
echo ✓ Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check Node.js
echo ✓ Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found. Please install it from https://nodejs.org/
    pause
    exit /b 1
)

REM Check npm
echo ✓ Checking npm...
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm not found. Please install Node.js.
    pause
    exit /b 1
)

echo.
echo 📦 Setting up Backend...

cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install backend dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Check for .env file
if not exist ".env" (
    echo.
    echo ⚠️  .env file not found!
    echo Please create backend\.env with the following:
    echo.
    echo GOOGLE_API_KEY=your_google_api_key_here
    echo LLM_MODEL=gemini-1.5-flash
    echo EMBEDDING_MODEL=qwen3-embedding:0.6b
    echo.
    echo Get your Google API Key from: https://aistudio.google.com/app/apikeys
    pause
    exit /b 1
)

cd ..

echo.
echo 📦 Setting up Frontend...

cd frontend

REM Install frontend dependencies
echo Installing Node.js dependencies...
call npm install

cd ..

echo.
echo ✅ Setup complete!
echo.
echo 🎯 Next steps:
echo.
echo 1. Make sure Ollama is running:
echo    Download from: https://ollama.ai/
echo.
echo 2. Start the backend (in Command Prompt 1):
echo    cd backend
echo    venv\Scripts\activate.bat
echo    python app.py
echo.
echo 3. Start the frontend (in Command Prompt 2):
echo    cd frontend
echo    npm start
echo.
echo 4. Open your browser to http://localhost:3000
echo.
pause
