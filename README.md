# LegalX AI Knowledge Centre

An AI-powered legal knowledge system that extracts information from legal documents using RAG (Retrieval-Augmented Generation) and provides an interactive chat interface for legal queries.

## 🎯 Features

- **📄 Smart Document Processing**: Automatically extracts legal information from PDF documents
- **🤖 AI-Powered Chat**: RAG-based legal assistant for answering questions about documents
- **🎨 Modern UI**: Beautiful React frontend with Tailwind CSS
- **🔍 Structured Information**: Displays:
  - Topic summaries
  - Key rights
  - Important provisions
  - Penalties
  - Who can benefit
  - Real-world context from web search

---

## 🚀 Quick Start (5 Minutes)

### 1️⃣ One-Command Setup (macOS/Linux)
```bash
bash setup.sh
```

### 2️⃣ Windows Setup
```cmd
setup.bat
```

### 3️⃣ Manual Setup

**Terminal 1 - Start Backend:**
```bash
cd backend
source venv/bin/activate  # macOS/Linux: or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm install  # First time only
npm start
```

**Terminal 3 - Start Ollama (keep running):**
```bash
ollama serve
```

---

## 📋 Prerequisites

- ✅ Python 3.9+
- ✅ Node.js 14+
- ✅ Ollama ([Download](https://ollama.ai/))
- ✅ Google API Key ([Get Free](https://aistudio.google.com/app/apikeys))

---

## 📖 Detailed Setup Guide

See [SETUP.md](SETUP.md) for comprehensive step-by-step instructions.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│            Frontend (React)                 │
│   • Topic Cards Display                     │
│   • Legal Details Page                      │
│   • AI Chat Interface                       │
└────────────────┬────────────────────────────┘
                 │ (HTTP REST API)
┌─────────────────┴────────────────────────────┐
│         Backend (Flask Python)              │
│   ✓ /api/topics - Get all topics            │
│   ✓ /api/topic/{id} - Get topic details     │
│   ✓ /api/chat - Send chat messages          │
└─────────────────┬────────────────────────────┘
                 │
        ┌────────┴─────────┐
        │                  │
   ┌────▼──────┐    ┌─────▼──────┐
   │ Ollama    │    │  Google    │
   │Embeddings │    │   Gemini   │
   │           │    │    LLM     │
   └────┬──────┘    └─────┬──────┘
        │                 │
   ┌────▼─────────────────▼──────┐
   │  PDF Documents              │
   │  • legal_documents/*.pdf    │
   │  • Vector Database (Chroma) │
   └─────────────────────────────┘
```

---

## 🔧 Configuration

### Environment Variables (.env)
Create `backend/.env` (use `.env.example` as template):
```env
GOOGLE_API_KEY=your_key_here
LLM_MODEL=gemini-1.5-flash
EMBEDDING_MODEL=qwen3-embedding:0.6b
```

### Add Your Legal Documents
1. Place PDF files in `backend/legal_documents/`
2. Restart the backend
3. Documents are automatically processed

---

## 📁 Project Structure

```
├── backend/
│   ├── app.py                 # Flask API server
│   ├── information_agent.py   # PDF processing & extraction
│   ├── legal_assistant.py     # RAG chatbot engine
│   ├── config.py              # Configuration
│   ├── requirements.txt        # Python dependencies
│   ├── .env                   # Your API keys (create this)
│   ├── legal_documents/       # Place PDFs here
│   ├── chroma_db/             # Vector database
│   └── venv/                  # Virtual environment
│
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── App.js             # Main component
│   │   ├── components/
│   │   │   ├── TopicCards.js
│   │   │   ├── LegalDetail.js
│   │   │   └── AIAssistant.js
│   │   └── services/
│   │       └── api.js
│   └── node_modules/
│
├── SETUP.md                   # Detailed setup instructions
├── setup.sh                   # Auto setup script (macOS/Linux)
└── setup.bat                  # Auto setup script (Windows)
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/topics` | Get all legal topics |
| GET | `/api/topic/<id>` | Get specific topic details |
| POST | `/api/chat` | Chat with legal assistant |
| GET | `/api/health` | Health check |

---

## ⚡ Usage

### Step 1: Add Documents
Place your PDF files in `backend/legal_documents/`:
```
legal_documents/
├── Indian_Penal_Code.pdf
├── Constitution.pdf
└── Labor_Laws.pdf
```

### Step 2: Process Documents
The backend automatically:
- Loads PDFs
- Extracts text
- Creates embeddings with Ollama
- Stores in vector database (Chroma)
- Generates summaries using Gemini LLM

### Step 3: Query the System
Use the frontend to:
- Browse topic cards
- View detailed information
- Ask questions via AI Assistant
- Get RAG-powered responses

---

## 🐛 Troubleshooting

### Backend Issues
| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError" | Run: `pip install -r requirements.txt` |
| "Connection refused" | Make sure Flask is running on port 5000 |
| "Ollama connection error" | Start Ollama: `ollama serve` |
| "GOOGLE_API_KEY not found" | Create `backend/.env` with your API key |
| "No documents found" | Add PDFs to `backend/legal_documents/` |

### Frontend Issues
| Problem | Solution |
|---------|----------|
| "Failed to load topics" | Backend must be running on `http://localhost:5000` |
| "npm ERR" | Delete `node_modules/` and `package-lock.json`, then `npm install` |
| "Port 3000 already in use" | Use different port: `PORT=3001 npm start` |

---

## 📊 Data Flow

```
PDF Upload
    ↓
Information Agent extracts:
├─ Topic Name
├─ Short Description
├─ Summary
├─ Key Rights
├─ Important Provisions
├─ Penalties
├─ Who Can Benefit
└─ Web Context
    ↓
Stored as JSON in memory / cache
    ↓
Frontend API receives data
    ↓
User sees beautiful cards and details
    ↓
User asks question via chat
    ↓
RAG System retrieves relevant context
    ↓
Gemini LLM generates answer
    ↓
Response shown in chat
```

---

## 💾 Caching

The system caches processed topics in `topics_cache.json` for faster subsequent loads. To refresh:
```bash
rm backend/topics_cache.json
# Restart backend - it will regenerate the cache
```

---

## 🚀 Deployment

Ready to deploy? Consider:
- **Docker**: Containerize both services
- **Heroku**: Deploy Python backend + React frontend
- **AWS**: Use Lambda + S3 + RDS
- **Vercel + Railway**: Frontend + Backend separately

---

## 📝 License

[Add your license here]

---

## 💡 Support

- **Documentation**: See [SETUP.md](SETUP.md)
- **Troubleshooting**: Check section above
- **Browser Console**: Press F12 for frontend errors
- **Terminal Logs**: Check backend terminal for API errors

---

## 🎓 Technologies Used

- **Backend**: Python, Flask, LangChain, Chroma
- **Frontend**: React 18, Tailwind CSS, Axios
- **AI/ML**: Google Gemini, Ollama Embeddings, RAG
- **Database**: ChromaDB (Vector Store)
- **Search**: DuckDuckGo for real-world context

---

## 📞 Quick Command Reference

```bash
# Backend setup (first time)
cd backend
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# Run backend
python app.py

# Frontend setup (first time)
cd frontend
npm install

# Run frontend
npm start

# Start Ollama (separate terminal)
ollama serve
```

---

Happy exploring! 🎉