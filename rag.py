import os
import hashlib
import yaml
import chromadb
from chromadb.utils import embedding_functions

DOCUMENTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "documents")

def chunk_text(text, max_chars=1200, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        if end >= len(text):
            chunks.append(text[start:])
            break
        boundary = text.rfind('\n', start, end)
        if boundary == -1 or boundary <= start + max_chars // 2:
            boundary = text.rfind(' ', start, end)
        if boundary != -1 and boundary > start:
            end = boundary
        chunks.append(text[start:end].strip())
        start = max(start + 1, end - overlap)
    return chunks

def load_markdown_documents(directory):
    docs = []
    if not os.path.exists(directory):
        return docs
    for filename in os.listdir(directory):
        if not filename.endswith('.md'):
            continue
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        title = filename
        source = "terrytao.wordpress.com"
        url = ""
        date = ""
        categories = []
        content = text
        
        if text.startswith('---'):
            parts = text.split('---', 2)
            if len(parts) >= 3:
                front_matter_str = parts[1]
                content = parts[2].strip()
                try:
                    meta = yaml.safe_load(front_matter_str)
                    if meta:
                        title = meta.get('title', title)
                        source = meta.get('source', source)
                        url = meta.get('url', url)
                        date = str(meta.get('date', ''))
                        categories = meta.get('categories', [])
                except Exception as e:
                    print(f"Error parsing YAML in {filename}: {e}")
        
        docs.append({
            "id": f"file_{filename}",
            "title": title,
            "source": source,
            "url": url,
            "date": date,
            "categories": categories,
            "content": content
        })
    return docs

class ChromaRetriever:
    def __init__(self):
        self.persist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="terence_tao_rag_v4",
            embedding_function=self.embedding_function,
            metadata={"hnsw:space": "cosine"}
        )
        self._sync_database()

    def _sync_database(self):
        all_docs = load_markdown_documents(DOCUMENTS_DIR)
        active_doc_ids = {doc["id"] for doc in all_docs}
        
        existing_items = self.collection.get(include=["metadatas"])
        if existing_items and existing_items["metadatas"]:
            existing_doc_ids = {meta["doc_id"] for meta in existing_items["metadatas"] if meta and "doc_id" in meta}
            orphaned_ids = existing_doc_ids - active_doc_ids
            for o_id in orphaned_ids:
                self.collection.delete(where={"doc_id": o_id})
        
        docs_to_index = []
        for doc in all_docs:
            doc_id, content = doc["id"], doc["content"]
            content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
            
            existing = self.collection.get(
                where={"doc_id": doc_id},
                limit=1,
                include=["metadatas"]
            )
            
            needs_indexing = True
            if existing and existing["metadatas"]:
                if existing["metadatas"][0].get("content_hash") == content_hash:
                    needs_indexing = False
            if needs_indexing:
                docs_to_index.append(doc)
                
        if docs_to_index:
            for doc in docs_to_index:
                self.collection.delete(where={"doc_id": doc["id"]})
                
            chunk_ids = []
            chunk_texts = []
            chunk_metadatas = []
            
            for doc in docs_to_index:
                doc_id, content = doc["id"], doc["content"]
                content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
                chunks = chunk_text(content)
                for idx, chunk in enumerate(chunks):
                    chunk_ids.append(f"{doc_id}_chunk_{idx}")
                    chunk_texts.append(chunk)
                    chunk_metadatas.append({
                        "doc_id": doc_id,
                        "content_hash": content_hash,
                        "title": doc["title"],
                        "source": doc["source"],
                        "url": doc["url"],
                        "date": doc["date"],
                        "categories": ",".join(doc["categories"]) if isinstance(doc["categories"], list) else doc["categories"]
                    })
                    
            if chunk_texts:
                self.collection.add(
                    ids=chunk_ids,
                    documents=chunk_texts,
                    metadatas=chunk_metadatas
                )

    def retrieve(self, query, top_k=3):
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        
        retrieved_docs = []
        if not results or not results["documents"] or not results["documents"][0]:
            return retrieved_docs
            
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        
        for doc_text, meta, dist in zip(documents, metadatas, distances):
            similarity = 1.0 - dist
            categories_str = meta.get("categories", "")
            categories = categories_str.split(",") if categories_str else []
            
            doc_dict = {
                "id": meta.get("doc_id"),
                "title": meta.get("title", ""),
                "source": meta.get("source", ""),
                "url": meta.get("url", ""),
                "date": meta.get("date", ""),
                "categories": categories,
                "content": doc_text
            }
            retrieved_docs.append((doc_dict, similarity))
        return retrieved_docs

    def format_context(self, query, top_k=3, score_threshold=0.01):
        results = self.retrieve(query, top_k=top_k)
        if not results:
            return 'No specific retrieved sources for this query.'
        parts = []
        for (doc, score) in results:
            if score < score_threshold:
                continue
            parts.append(f"[SOURCE: {doc['source']}]\nTopic: {doc['title']}\n{doc['content'].strip()}")
        if not parts:
            return 'No highly relevant sources retrieved.'
        return '\n\n---\n\n'.join(parts)

_retriever = None

def get_retriever():
    global _retriever
    if _retriever is None:
        _retriever = ChromaRetriever()
    return _retriever