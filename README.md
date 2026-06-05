# Terence Tao AI Agent

## Features

1. **Conversational Digital Twin**: Chat with a RAG-enhanced replica of mathematician Terence Tao.
2. **Context-Aware Memory**: Remembers user facts, notable questions, and topics discussed across sessions.
3. **Concept Explorer**: Generates an interactive graph of related mathematical subtopics, allowing users to click nodes for custom RAG explanations.

## File Structure

- `app.py`: Main Streamlit application entry point containing layout, tabs, and graph display logic.
- `rag.py`: Handles vector database storage, text chunking, document loading, and ChromaDB retrieval.
- `prompts.py`: Prompt templates.
- `memory.py`: Manages short-term and long-term memory.
- `documents/`: Knowledge base folder.
