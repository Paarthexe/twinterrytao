# Terence Tao AI Agent - Advanced Hybrid RAG Digital Twin

An advanced conversational digital twin of mathematician Terence Tao. The agent mimics his reasoning patterns, collaborative and intellectually humble tone, uses persistent memory to construct a user profile, and retrieves mathematical context from Terence Tao's blogs and papers.

---

## Tech Stack & Infrastructure

- **GUI & Interface**: React + Tailwind + KaTeX.
- **Backend API**: Flask REST API (`server.py`).
- **Dense Retrieval**: ChromaDB vector database using cosine similarity.
- **Sparse Retrieval**: rank-bm25 scoring.
- **Rank Fusion**: Reciprocal Rank Fusion (RRF) combining dense and sparse search scores.
- **LLM Engine**: Ollama running locally (`gemma4:e4b`).
- **Memory Storage**: Local JSON-based persistent long-term storage (`long_term_memory.json`).

---

## File Structure

- `server.py`: Flask API backend.
- `frontend/`: React frontend web application.
- `model.py`: Core LLM orchestration engine. Implements RAG context retrieval, draft generation, skeptic verification, and revision.
- `rag.py`: ChromaDB synchronization and hybrid search (Vector Dense + BM25 Sparse) with Reciprocal Rank Fusion (RRF).
- `memory.py`: Synchronizes long-term memory metrics (discussed topics, notable questions, facts profile) and parses user message cues.
- `prompts.py`: Contains system prompts, persona definitions, and peer review guidelines.

---

## Key Features

- **KaTeX Formula Rendering**: Native inline and block LaTeX typesetting ($\int, \sum, \mathbb{R}^n$).
- **Hybrid Retrieval & RRF**: Combines dense vector search with sparse BM25 keyword matching using Reciprocal Rank Fusion (RRF) to pull the most relevant blog posts and papers.
- **Skeptic Peer Review & Sources**: Verification audit that flags unsupported claims and hallucinated assertions against retrieved paper sources.
- **Interactive Concept Explorer**: Generates concept network maps with contextual explanations.
- **Memory Matrix**: Real-time visualization of learned user facts profile, discussed topic cloud, and stored questions timeline.

---

## Setup & Execution

### 1. Install Dependencies
```bash
python3 -m pip install -r requirements.txt
cd frontend && npm install && cd ..
```

### 2. Set Up Local LLM (Ollama)
Ensure Ollama is installed and running on your system.
```bash
ollama pull gemma4:e4b
```

### 3. Launch Application
Start the backend server and frontend dev server:
```bash
# Terminal 1 - Backend Server
python3 server.py

# Terminal 2 - React Frontend
cd frontend && npm run dev
```
Open **http://localhost:3000** in your browser.



