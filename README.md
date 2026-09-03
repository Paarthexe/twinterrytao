# Terence Tao AI — Hybrid RAG Digital Twin

A specialized conversational AI modeled on mathematician Terence Tao's expository writing, research preprints, and pedagogical style. It combines multi-hop hybrid retrieval (ChromaDB dense vectors + BM25 sparse keyword matching via Reciprocal Rank Fusion) with a two-phase Skeptic Peer Review pipeline to verify mathematical assertions against retrieved literature before replying.

---

## Architecture Overview

```
User Query
   │
   ├─► 1. Hybrid Retrieval (Dense Vector + BM25 Sparse Search + RRF)
   │      └── Source: 1,080+ blog posts (terrytao.wordpress.com) + arXiv preprints
   │
   ├─► 2. Context Aggregation (RAG Chunks + Persistent User Profile)
   │
   ├─► 3. Initial Formulation (Draft Generation via Local Ollama LLM)
   │
   ├─► 4. Skeptic Peer Review Audit
   │      ├── Grounding Check: Claims, bounds, and theorem assumptions verified
   │      └── Supplementary Hop: Targeted retrieval if citations or corrections needed
   │
   └─► 5. Final Synthesis (KaTeX-typeset response + Collapsible Peer Review Drawer)
```

---

## Core Components

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend UI** | React 19, TypeScript, Tailwind CSS, KaTeX | Chat interface with live KaTeX rendering, collapsible Peer Review Drawer, Memory Matrix, and Concept Explorer. |
| **Alternate UI** | Streamlit (`app.py`) | Interactive dashboard for quick prototyping, knowledge base metrics, and manual ingestion triggers. |
| **Backend API** | Python, Flask, Flask-CORS (`server.py`) | REST & SSE endpoints for streaming responses, memory syncing, graph generation, and data ingestion. |
| **LLM Inference** | Ollama (`gemma4:e2b` / `gemma4:e4b`) | Local inference engine configured via `OLLAMA_MODEL` and `OLLAMA_URL`. |
| **Dense Search** | ChromaDB | Chunked embeddings stored in local SQLite vector index with MD5-based incremental hashing. |
| **Sparse Search** | `rank-bm25` (BM25Okapi) | Tokenized keyword inverted index with reciprocal rank fusion (RRF, $k=60$). |
| **Data Ingestion** | `scraper.py` | WordPress REST API crawler for Terence Tao's blog + arXiv API batch fetcher for cited preprints. |
| **Memory Engine** | `memory.py` | Local JSON store tracking user facts profile, notable questions, and topic clusters across sessions. |

---

## Key Features

1. **Automated Knowledge Ingestion & Sync**:
   - Downloads all 1,080+ posts from `terrytao.wordpress.com` via the WordPress REST API, converting HTML into clean Markdown while preserving inline and block LaTeX formulas.
   - Automatically parses blog posts for cited `arxiv.org/abs/...` links (discovering 640+ research papers) and fetches abstracts, authors, and metadata via the official arXiv API.
   - Syncs incrementally: existing documents with unchanged MD5 hashes are skipped in milliseconds.

2. **Multi-Stage Skeptic Peer Review (Skeptic Mode)**:
   - Draft responses are passed through an internal peer-review critique step before being delivered.
   - The skeptic evaluates whether bounds, conjectures, and theorem conditions are grounded in the retrieved sources.
   - The UI provides a collapsible **"Peer Review Audit"** drawer showing the audit verdict (`Passed` or `Revised`), flagged issues, skeptic commentary, and the original pre-audit draft.

3. **Hybrid RRF Retrieval**:
   - Combines cosine-similarity dense search with BM25 sparse search using Reciprocal Rank Fusion:
     $$\text{RRF Score}(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
   - Ensures exact mathematical terms (e.g., *Navier-Stokes blowup*, *Kakeya maximal function*, *Gowers norm*) match precisely even when semantic embeddings are diffuse.

4. **Memory Matrix & Concept Explorer**:
   - Automatically extracts user background facts and discussed topics across conversation turns.
   - Visualizes knowledge graphs and mathematical concept dependencies with on-demand AI explanations.

---

## Getting Started

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+** & `npm`
- **Ollama** running locally

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/your-username/twinterrytao.git
cd twinterrytao

# Install Python dependencies
pip install -r requirements.txt

# Install Frontend dependencies
cd frontend && npm install && cd ..
```

### 3. Start Ollama Model
```bash
# Pull and start your preferred model (e.g. gemma4:e2b or gemma4:e4b)
ollama pull gemma4:e2b
```

### 4. Running the Application

**Option A: Full Stack (React + Flask Backend)**
```bash
# Terminal 1 — Backend API
python3 server.py

# Terminal 2 — React Frontend Dev Server
cd frontend
npm run dev
```
Open **http://localhost:3000** in your browser.

**Option B: Streamlit Dashboard**
```bash
streamlit run app.py
```

---

## Data Management & Scraper CLI

The repository includes a dedicated CLI for managing the knowledge base:

```bash
# Sync latest 20 posts from Terence Tao's blog
python3 scraper.py --count 20

# Sync all posts across the entire blog history (~1,087 posts)
python3 scraper.py --all

# Filter posts by WordPress category (e.g. expository, combinatorics, math.CA)
python3 scraper.py --category expository --count 30

# Discover and ingest cited arXiv research papers
python3 scraper.py --arxiv --arxiv-count 50

# List currently downloaded markdown documents
python3 scraper.py --list
```

You can also trigger blog or arXiv syncing directly from the React UI Navbar or the Streamlit *Knowledge Base & Sync* tab.

---

## REST API Reference

| Endpoint | Method | Payload / Params | Description |
| :--- | :--- | :--- | :--- |
| `/api/health` | `GET` | — | Returns server status, active model name, and ChromaDB/document stats. |
| `/api/chat` | `POST` | `{"message": str, "history": list}` | Executes RAG + Skeptic pipeline, returning final response and audit data. |
| `/api/chat/stream` | `POST` | `{"message": str, "history": list}` | Server-Sent Events (SSE) streaming live phase updates, tokens, and audit payload. |
| `/api/documents` | `GET` | — | Lists indexed documents and vector count. |
| `/api/documents/sync` | `POST` | `{"count": int, "all": bool, "force": bool}` | Triggers blog scraping and vector re-indexing. |
| `/api/arxiv/sync` | `POST` | `{"max_papers": int, "force": bool}` | Discovers and fetches cited arXiv papers. |
| `/api/memory` | `GET` | — | Returns user facts profile, discussed topics, and question history. |
| `/api/memory/clear` | `POST` | — | Clears persistent long-term user memory. |
| `/api/explore/graph` | `POST` | `{"topic": str}` | Generates concept relationship nodes and edges for the Concept Explorer. |
| `/api/explore/explain` | `POST` | `{"topic_label": str, "core_topic": str}` | Provides in-depth expository explanation for a specific concept node. |

---

## Configuration & Environment Variables

| Variable | Default | Description |
| :--- | :--- | :--- |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama service endpoint. |
| `OLLAMA_MODEL` | `gemma4:e2b` | Ollama model identifier to use for generation. |
| `PORT` | `5001` | Flask server listening port. |

