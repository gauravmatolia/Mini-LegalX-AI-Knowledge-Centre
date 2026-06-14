# LegalX AI Knowledge Centre - Setup & Installation Guide

## Prerequisites

Before starting, ensure you have the following installed on your system:

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js & npm** - [Download](https://nodejs.org/)
- **Git** (optional but recommended)

Verify installations:
```bash
python --version
node --version
npm --version
```

---

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create a Python Virtual Environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt, indicating the virtual environment is active.

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file in the `backend/` directory:
```bash
touch .env
```

Add the following to `.env`:
```
GOOGLE_API_KEY=your_google_api_key_here
LLM_MODEL=gemini-1.5-flash
EMBEDDING_MODEL=qwen3-embedding:0.6b
```

**Note:** You'll need:
- **Google API Key** for Gemini LLM: [Get it here](https://aistudio.google.com/app/apikeys)
- **Ollama** running for embeddings: [Install Ollama](https://ollama.ai/)

### 5. Setup Ollama (For Embeddings)

Ollama is required for document embeddings. Install and run it:

```bash
# Install Ollama from https://ollama.ai/
# Then run this command to pull the embedding model:
ollama pull qwen3-embedding:0.6b

# Keep Ollama running in the background (it runs on http://localhost:11434)
```

### 6. Add Legal Documents

Place your PDF files in the `backend/legal_documents/` directory:
```
backend/
├── legal_documents/
│   ├── YourDocument1.pdf
│   ├── YourDocument2.pdf
│   └── ...
```

### 7. Test Backend

Run a quick test to see if everything works:
```bash
cd backend
python information_agent.py
```

This will process all PDFs and display the extracted information in JSON format.

---

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install npm Dependencies
```bash
npm install
```

This may take 2-5 minutes. Wait for it to complete.

### 3. Verify Installation
```bash
npm list react react-dom react-scripts
```

---

## Running the Application

### Step 1: Start Ollama (if not already running)
```bash
# On macOS with Homebrew
ollama serve

# Or open the Ollama app from Applications
```

Keep this terminal window open.

### Step 2: Start the Backend Server

Open a **new terminal** and run:
```bash
cd backend
source venv/bin/activate  # (or venv\Scripts\activate on Windows)
python app.py
```

You should see output like:
```
Initializing RAG System...
✅ RAG System initialized successfully
🔄 Generating topics from legal documents...
Running on http://127.0.0.1:5000
```

**Keep this terminal window open** - the Flask server must stay running.

### Step 3: Start the Frontend Development Server

Open a **new terminal** and run:
```bash
cd frontend
npm start
```

This will automatically open your browser to `http://localhost:3000`

**You should now see your LegalX application with:**
- Home page with legal topic cards
- Legal Assistant chat page
- Topic detail pages with all information

---

## Troubleshooting

### ❌ "ModuleNotFoundError: No module named 'langchain'"
**Solution:** Make sure you've activated the virtual environment and installed requirements:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### ❌ "Connection refused" or Backend not responding
**Solution:** Ensure the Flask backend is running:
```bash
cd backend
python app.py
```

### ❌ "Ollama connection error"
**Solution:** Make sure Ollama is running:
```bash
ollama serve
```

Or keep the Ollama app open (macOS/Linux).

### ❌ Frontend shows "Failed to load legal topics"
**Solution:** 
1. Check that Flask backend is running on `http://localhost:5000`
2. Check browser console (F12) for error details
3. Make sure `legal_documents/` folder has PDF files
4. Restart both frontend and backend

### ❌ "GOOGLE_API_KEY not found"
**Solution:** Make sure your `.env` file in `backend/` has:
```
GOOGLE_API_KEY=your_actual_key_here
```

And restart the backend server.

---

## Project Structure

```
Mini-LegalX-AI-Knowledge-Centre/
├── backend/
│   ├── app.py                    # Flask API server
│   ├── information_agent.py      # Extract legal info from PDFs
│   ├── legal_assistant.py        # RAG chatbot
│   ├── config.py                 # Configuration
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # Environment variables (create this)
│   ├── legal_documents/           # Place PDFs here
│   ├── chroma_db/                # Vector database
│   └── venv/                     # Virtual environment (created)
│
├── frontend/
│   ├── package.json              # Node dependencies
│   ├── src/
│   │   ├── App.js               # Main app component
│   │   ├── components/
│   │   │   ├── TopicCards.js    # Display legal topics
│   │   │   ├── LegalDetail.js   # Show topic details
│   │   │   └── AIAssistant.js   # Chat interface
│   │   └── services/
│   │       └── api.js            # API calls to backend
│   └── node_modules/             # NPM packages (created)
│
└── README.md
```

---

## API Endpoints

Once the backend is running, you can test these endpoints:

### Get All Topics
```bash
curl http://localhost:5000/api/topics
```

### Get Specific Topic
```bash
curl http://localhost:5000/api/topic/0
```

### Chat with Legal Assistant
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are my rights under this act?"}'
```

### Health Check
```bash
curl http://localhost:5000/api/health
```

---

## Next Steps

1. **Customize** your legal documents - place your PDFs in `backend/legal_documents/`
2. **Update** the `config.py` for different LLM models or embedding models
3. **Deploy** to production (consider using Docker or cloud platforms like Heroku, AWS, etc.)

---

## Support & Debugging

- **Check logs** in the terminal windows for error messages
- **Browser console** (F12) shows frontend errors
- **Backend terminal** shows API errors and processing logs
- **Network tab** (F12) shows API requests/responses

Happy coding! 🎉
