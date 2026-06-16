# Terence Tao AI Agent - Advanced Hybrid RAG Digital Twin

An advanced conversational digital twin of mathematician Terence Tao. The agent mimics his reasoning patterns, collaborative and intellectually humble tone, uses persistent memory to construct a user profile, and retrieves mathematical context from Terence Tao's blogs and papers.

---

## Tech Stack & Infrastructure

- **GUI & Interface**: Streamlit + Streamlit Agraph for interactive network graphs.
- **Dense Retrieval**: ChromaDB vector database using cosine similarity.
- **Sparse Retrieval**: rank-bm25 scoring.
- **Rank Fusion**: Reciprocal Rank Fusion (RRF) combining dense and sparse search scores.
- **LLM Engine**: Ollama running locally.
- **LLM Model**: gemma4:e4b (Edge 4B parameter model).
- **Memory Storage**: Local JSON-based persistent long-term storage (long_term_memory.json).

---

## File Structure

- app.py: Entry point for the Streamlit web application. Handles GUI layout, tabs, state rendering, and event handlers.
- model.py: Core LLM orchestration engine. Implements RAG context retrieval, draft generation, skeptic verification, and revision.
- rag.py: ChromaDB synchronization and hybrid search (Vector Dense + BM25 Sparse) with Reciprocal Rank Fusion (RRF).
- memory.py: Synchronizes long-term memory metrics (discussed topics, notable questions, facts profile) and parses user message cues.
- prompts.py: Contains system prompts, persona definitions, and peer review guidelines.

---

## Key Features

- **Hybrid Retrieval & RRF**: Combines dense vector search with sparse BM25 keyword matching using Reciprocal Rank Fusion (RRF) to pull the most relevant blog posts and papers.
- **Skeptic Peer Review**: A verification audit that flags unsupported claims, hallucinations, or logical errors in the draft answer against the retrieved context and may initiate more relevant retreival by returning a query if it deems necessary
- **Targeted Verification Retrieval**: If issues are found, the skeptic generates targeted search queries to fetch additional context directly from RAG.
- **Defensive Revision**: The revision model incorporates style advice and the expanded context to rewrite the draft answer safely and accurately.
- **Concept Explorer**: Generates and visualizes an interactive network of related mathematical topics that users can click to get contextual explanations.
---

## Setup & Execution

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Local LLM (Ollama)
Ensure Ollama is installed and running on your system.
```bash
ollama pull gemma4:e4b
```

### 3. Run Web App
```bash
streamlit run app.py
```
