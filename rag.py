import os
import hashlib
import yaml
import re
import chromadb
from chromadb.utils import embedding_functions
from rank_bm25 import BM25Okapi

def tokenize(text):
    return re.findall(r'\w+', text.lower())


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
    def __init__(self, auto_sync_blog=True, sync_all=True):
        self.persist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="terence_tao_rag_v4",
            embedding_function=self.embedding_function,
            metadata={"hnsw:space": "cosine"}
        )
        
        if auto_sync_blog:
            try:
                from scraper import sync_tao_blog
                print("[*] Automatically syncing all posts from Terence Tao's blog (terrytao.wordpress.com)...")
                sync_tao_blog(all_posts=sync_all, target_dir=DOCUMENTS_DIR, verbose=True)
            except Exception as e:
                print(f"[!] Notice: Startup blog auto-sync skipped: {e}")
                
        self._sync_database()

    def sync_from_web(self, count=None, all_posts=True, category=None, search=None, tag=None, force=False):
        """Scrapes Terence Tao's blog and immediately synchronizes the Chroma vector and BM25 index."""
        from scraper import sync_tao_blog
        summary = sync_tao_blog(
            count=count,
            all_posts=(all_posts if count is None else False),
            category=category,
            search=search,
            tag=tag,
            target_dir=DOCUMENTS_DIR,
            force=force,
            verbose=False
        )
        self._sync_database()
        return summary

    def sync_arxiv(self, max_papers=50, force=False):
        """Discovers and ingests cited arXiv research papers and re-indexes the RAG store."""
        from scraper import sync_arxiv_papers
        summary = sync_arxiv_papers(
            max_papers=max_papers,
            target_dir=DOCUMENTS_DIR,
            force=force,
            verbose=False
        )
        self._sync_database()
        return summary

    def get_stats(self):
        """Returns stats about indexed documents and chunks."""
        docs = load_markdown_documents(DOCUMENTS_DIR)
        chunks_count = self.collection.count()
        return {
            "documents_count": len(docs),
            "chunks_count": chunks_count
        }

    def _sync_database(self):
        all_docs = load_markdown_documents(DOCUMENTS_DIR)
        active_doc_ids = {doc["id"] for doc in all_docs}
        
        existing_items = self.collection.get(include=["metadatas"])
        indexed_hashes = {}
        if existing_items and existing_items["metadatas"]:
            existing_doc_ids = {meta["doc_id"] for meta in existing_items["metadatas"] if meta and "doc_id" in meta}
            orphaned_ids = existing_doc_ids - active_doc_ids
            for o_id in orphaned_ids:
                self.collection.delete(where={"doc_id": o_id})
                
            for meta in existing_items["metadatas"]:
                if meta and "doc_id" in meta:
                    indexed_hashes[meta["doc_id"]] = meta.get("content_hash")
        
        docs_to_index = []
        for doc in all_docs:
            doc_id, content = doc["id"], doc["content"]
            content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
            if indexed_hashes.get(doc_id) != content_hash:
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
                print(f"[*] Embedding {len(chunk_texts)} new chunks across {len(docs_to_index)} documents into ChromaDB...")
                batch_size = 500
                for i in range(0, len(chunk_texts), batch_size):
                    self.collection.add(
                        ids=chunk_ids[i:i+batch_size],
                        documents=chunk_texts[i:i+batch_size],
                        metadatas=chunk_metadatas[i:i+batch_size]
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

    def retrieve_hybrid(self, query, top_k=3, dense_weight=1.0, sparse_weight=1.0):
        dense_results = self.retrieve(query, top_k=20)
        
        all_items = self.collection.get(include=["documents", "metadatas"])
        documents = all_items.get("documents", [])
        metadatas = all_items.get("metadatas", [])
        
        if not documents:
            return dense_results[:top_k]
        tokenized_corpus = [tokenize(doc) for doc in documents]
        bm25 = BM25Okapi(tokenized_corpus)
        query_tokens = tokenize(query)
        doc_scores = bm25.get_scores(query_tokens)
        sparse_scores = [(idx, score) for idx, score in enumerate(doc_scores)]
        sparse_scores.sort(key=lambda x: x[1], reverse=True)
        
        dense_rank = {}
        for rank, (doc, sim) in enumerate(dense_results):
            dense_rank[doc["content"]] = rank
            
        sparse_rank = {}
        rank_idx = 0
        for idx, score in sparse_scores:
            if score <= 0.0:
                continue
            doc_text = documents[idx]
            sparse_rank[doc_text] = rank_idx
            rank_idx += 1
            
        rrf_scores = {}
        
        for doc, sim in dense_results:
            content = doc["content"]
            r_dense = dense_rank[content]
            rrf_scores[content] = {
                "doc": doc,
                "score": dense_weight / (60.0 + r_dense)
            }
            
        for idx, score in sparse_scores:
            if score <= 0.0:
                continue
            content = documents[idx]
            r_sparse = sparse_rank[content]
            
            if content in rrf_scores:
                rrf_scores[content]["score"] += sparse_weight / (60.0 + r_sparse)
            else:
                meta = metadatas[idx]
                categories_str = meta.get("categories", "")
                categories = categories_str.split(",") if categories_str else []
                doc_dict = {
                    "id": meta.get("doc_id"),
                    "title": meta.get("title", ""),
                    "source": meta.get("source", ""),
                    "url": meta.get("url", ""),
                    "date": meta.get("date", ""),
                    "categories": categories,
                    "content": content
                }
                rrf_scores[content] = {
                    "doc": doc_dict,
                    "score": sparse_weight / (60.0 + r_sparse)
                }
                
        sorted_rrf = sorted(rrf_scores.values(), key=lambda x: x["score"], reverse=True)
        return [(item["doc"], item["score"]) for item in sorted_rrf[:top_k]]

    def retrieve_hybrid_question_aware(self, query, hop_query, top_k=3, dense_weight=1.0, sparse_weight=1.0):
        hop_results = self.retrieve_hybrid(hop_query, top_k=15, dense_weight=dense_weight, sparse_weight=sparse_weight)
        orig_results = self.retrieve_hybrid(query, top_k=15, dense_weight=dense_weight, sparse_weight=sparse_weight)
        
        hop_rank = {}
        for rank, (doc, score) in enumerate(hop_results):
            hop_rank[doc["content"]] = rank
            
        orig_rank = {}
        for rank, (doc, score) in enumerate(orig_results):
            orig_rank[doc["content"]] = rank
            
        combined_scores = {}
        for doc, score in hop_results:
            content = doc["content"]
            r_hop = hop_rank[content]
            r_orig = orig_rank.get(content, 15)
            
            combined_scores[content] = {
                "doc": doc,
                "score": 0.7 / (60.0 + r_hop) + 0.3 / (60.0 + r_orig)
            }
            
        sorted_docs = sorted(combined_scores.values(), key=lambda x: x["score"], reverse=True)
        return [(item["doc"], item["score"]) for item in sorted_docs[:top_k]]

    def format_context_hybrid(self, query, top_k=3):
        results = self.retrieve_hybrid(query, top_k=top_k)
        if not results:
            return 'No highly relevant sources retrieved.'
        parts = []
        for (doc, score) in results:
            parts.append(f"[SOURCE: {doc['source']}]\nTopic: {doc['title']}\n{doc['content'].strip()}")
        return '\n\n---\n\n'.join(parts)

_retriever = None

def get_retriever():
    global _retriever
    if _retriever is None:
        _retriever = ChromaRetriever()
    return _retriever