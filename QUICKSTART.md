# 🚀 LegalX AI - Step-by-Step Setup Guide

## Phase 1: Before You Start

### ✅ Checklist
- [ ] Python 3.9+ installed
- [ ] Node.js installed
- [ ] Google API Key ready
- [ ] Ollama downloaded

---

## Phase 2: Initial Setup

### Step 1: Get Your Google API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikeys)
2. Click "Create API Key" 
3. Copy the key (keep it safe!)

### Step 2: Install Ollama
1. Download from [ollama.ai](https://ollama.ai/)
2. Install and open the app
3. In terminal, run:
   ```bash
   ollama pull qwen3-embedding:0.6b
   ```

### Step 3: Clone/Prepare Project
```bash
cd /path/to/Mini-LegalX-AI-Knowledge-Centre
```

---

## Phase 3: Backend Setup

### Step 1: Create Virtual Environment
```bash
cd backend

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

✅ You should see `(venv)` in your terminal

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

⏳ This takes 2-3 minutes. Wait for completion.

### Step 3: Setup Environment File
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Google API Key
nano .env   # or use your preferred editor
```

Add this to `.env`:
```
GOOGLE_API_KEY=<paste_your_key_here>
LLM_MODEL=gemini-1.5-flash
EMBEDDING_MODEL=qwen3-embedding:0.6b
```

### Step 4: Add Legal Documents
```bash
# Put your PDF files here
backend/legal_documents/
├── YourDocument1.pdf
└── YourDocument2.pdf
```

### Step 5: Test Backend
```bash
python information_agent.py
```

✅ Should display JSON output of extracted information

---

## Phase 4: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# This takes 2-5 minutes
```

✅ When complete, you'll see "added X packages"

---

## Phase 5: Running the Application

### 📟 You need 3 terminal windows:

#### Terminal Window 1: Ollama
```bash
ollama serve
```
Keep this running.

#### Terminal Window 2: Backend
```bash
cd backend
source venv/bin/activate  # macOS/Linux
python app.py
```

✅ Should show:
```
✅ RAG System initialized successfully
Running on http://127.0.0.1:5000
```

#### Terminal Window 3: Frontend
```bash
cd frontend
npm start
```

✅ Browser should open to `http://localhost:3000`

---

## Phase 6: Using the Application

### On Home Page
- See cards with legal topics
- Each card shows:
  - Topic name
  - Short description
  - "Read More" button

### Click "Read More"
You'll see:
- 📋 Full summary
- 🛡️ Key Rights
- 📜 Important Provisions
- ⚠️ Penalties
- 👥 Who Can Benefit
- 🌐 Real-World Context

### Click "Legal Assistant"
- Chat interface appears
- Ask questions about legal documents
- AI provides RAG-powered answers

---

## ⚡ Common Issues & Quick Fixes

### "ModuleNotFoundError"
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### "Port 5000 already in use"
```bash
# Kill the process or use different port in app.py
# Change: app.run(port=5000) to app.run(port=5001)
```

### "Frontend can't reach backend"
1. Make sure backend is running: `python app.py`
2. Check http://localhost:5000/api/health in browser
3. If error, restart backend

### "No documents showing"
1. Add PDFs to `backend/legal_documents/`
2. Restart backend server
3. Refresh browser

### "Ollama connection error"
```bash
# Make sure Ollama is running
ollama serve

# Or check if Ollama app is open (macOS)
```

---

## 📊 Verification Checklist

After setup, verify each component:

### ✅ Backend Check
```bash
curl http://localhost:5000/api/health
# Should return: {"status": "ok", ...}
```

### ✅ Topics API Check
```bash
curl http://localhost:5000/api/topics
# Should return: [{...topic data...}, ...]
```

### ✅ Chat API Check
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello"}'
# Should return: {"reply": "...", "success": true}
```

### ✅ Frontend Check
- Go to http://localhost:3000
- Should see topic cards
- Should see "Legal Assistant" button in header

---

## 🔧 Advanced: Customization

### Change LLM Model
Edit `backend/config.py`:
```python
LLM_MODEL='gemini-2.0-flash'  # Or another Google model
```

### Change Embedding Model
Edit `backend/config.py`:
```python
EMBEDDING_MODEL='mistral-embedding:latest'  # Different model
```

### Change Port Numbers
- Backend: Edit `backend/app.py` line ~150
- Frontend: Use `PORT=3001 npm start`

### Add More Documents
1. Drop PDFs in `backend/legal_documents/`
2. Delete `backend/topics_cache.json` (optional)
3. Restart backend
4. Refresh frontend

---

## 📚 File Reference

| File | Purpose |
|------|---------|
| `backend/app.py` | Flask API server |
| `backend/information_agent.py` | PDF processing |
| `backend/legal_assistant.py` | RAG chatbot |
| `backend/config.py` | Configuration |
| `backend/requirements.txt` | Python packages |
| `backend/.env` | Your API keys |
| `frontend/src/App.js` | Main React component |
| `frontend/package.json` | NPM packages |

---

## 🆘 Help Resources

1. **Setup Issues**: Check [SETUP.md](./SETUP.md)
2. **Architecture**: See README.md
3. **Errors in Terminal**: Google the error message
4. **Browser Issues**: Press F12, check Console tab
5. **API Problems**: Try curl commands above

---

## ✨ Next Steps After Setup

1. **Add More Documents**: Put PDFs in `legal_documents/` folder
2. **Customize UI**: Edit components in `frontend/src/components/`
3. **Change Colors**: Modify Tailwind classes in components
4. **Deploy**: Prepare for production deployment
5. **Scale**: Consider Docker/Kubernetes for scaling

---

## 🎉 You're All Set!

Your LegalX AI Knowledge Centre is now running!

**Access Points:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000/api
- Ollama: http://localhost:11434

Enjoy! 🚀
