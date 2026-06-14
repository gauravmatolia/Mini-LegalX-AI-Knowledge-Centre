#!/bin/bash

# LegalX AI Knowledge Centre - Quick Start Script
# This script sets up and runs both backend and frontend

echo "🚀 Starting LegalX AI Knowledge Centre Setup..."
echo ""

# Check Python
echo "✓ Checking Python..."
python3 --version || { echo "❌ Python 3 not found. Please install it."; exit 1; }

# Check Node.js
echo "✓ Checking Node.js..."
node --version || { echo "❌ Node.js not found. Please install it."; exit 1; }

# Check npm
echo "✓ Checking npm..."
npm --version || { echo "❌ npm not found. Please install Node.js."; exit 1; }

echo ""
echo "📦 Setting up Backend..."

# Setup backend
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install backend dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  .env file not found!"
    echo "Please create backend/.env with the following:"
    echo ""
    echo "GOOGLE_API_KEY=your_google_api_key_here"
    echo "LLM_MODEL=gemini-1.5-flash"
    echo "EMBEDDING_MODEL=qwen3-embedding:0.6b"
    echo ""
    echo "Get your Google API Key from: https://aistudio.google.com/app/apikeys"
    exit 1
fi

cd ..

echo ""
echo "📦 Setting up Frontend..."

cd frontend

# Install frontend dependencies
echo "Installing Node.js dependencies..."
npm install

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo ""
echo "1. Make sure Ollama is running:"
echo "   ollama serve"
echo ""
echo "2. Start the backend (in Terminal 1):"
echo "   cd backend && source venv/bin/activate && python app.py"
echo ""
echo "3. Start the frontend (in Terminal 2):"
echo "   cd frontend && npm start"
echo ""
echo "4. Open your browser to http://localhost:3000"
echo ""
