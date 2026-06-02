import math
import re
from collections import Counter
from typing import List, Dict, Tuple
from persona import KNOWLEDGE_BASE

def tokenize(text):
    text = text.lower()
    tokens = re.findall('[a-z0-9]+', text)
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'this', 'that', 'is', 'it', 'are', 'was', 'we', 'be', 'as', 'have', 'has', 'i', 'can', 'which', 'also', 'not', 'if', 'so', 'do', 'its', 'into', 'more', 'than', 'some', 'such', 'any', 'all', 'one', 'two', 'three', 'each', 'very', 'will', 'then', 'they', 'their', 'our', 'these', 'those', 'been', 'both', 'what', 'when', 'how'}
    return [t for t in tokens if t not in stopwords and len(t) > 1]

class TFIDFRetriever:

    def __init__(self, corpus):
        self.corpus = corpus
        self.doc_tokens: List[List[str]] = []
        self.df: Counter = Counter()
        self.idf: Dict[str, float] = {}
        self.tfidf_vectors: List[Dict[str, float]] = []
        self._build_index()

    def _build_index(self):
        for doc in self.corpus:
            text = doc['title'] + ' ' + doc['content'] + ' ' + doc.get('source', '')
            tokens = tokenize(text)
            self.doc_tokens.append(tokens)
            for t in set(tokens):
                self.df[t] += 1
        N = len(self.corpus)
        for (term, freq) in self.df.items():
            self.idf[term] = math.log((N + 1) / (freq + 1)) + 1.0
        for tokens in self.doc_tokens:
            tf = Counter(tokens)
            vec = {}
            for (term, count) in tf.items():
                vec[term] = count / len(tokens) * self.idf.get(term, 1.0)
            norm = math.sqrt(sum((v * v for v in vec.values())))
            if norm > 0:
                vec = {k: v / norm for (k, v) in vec.items()}
            self.tfidf_vectors.append(vec)

    def _query_vector(self, query):
        tokens = tokenize(query)
        if not tokens:
            return {}
        tf = Counter(tokens)
        vec = {}
        for (term, count) in tf.items():
            vec[term] = count / len(tokens) * self.idf.get(term, 1.0)
        norm = math.sqrt(sum((v * v for v in vec.values())))
        if norm > 0:
            vec = {k: v / norm for (k, v) in vec.items()}
        return vec

    def _cosine_similarity(self, vec1, vec2):
        if not vec1 or not vec2:
            return 0.0
        common = set(vec1.keys()) & set(vec2.keys())
        return sum((vec1[t] * vec2[t] for t in common))

    def retrieve(self, query, top_k=3):
        qvec = self._query_vector(query)
        scores = []
        for (i, dvec) in enumerate(self.tfidf_vectors):
            score = self._cosine_similarity(qvec, dvec)
            scores.append((i, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for (idx, score) in scores[:top_k]:
            if score > 0.0:
                results.append((self.corpus[idx], score))
        return results

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
_retriever: TFIDFRetriever = None

def get_retriever():
    global _retriever
    if _retriever is None:
        _retriever = TFIDFRetriever(KNOWLEDGE_BASE)
    return _retriever