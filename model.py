import os
import json
import requests
from datetime import datetime

from prompts import (
    SYSTEM_PROMPT,
    GRAPH_PROMPT,
    EXPLAIN_PROMPT,
    FACT_EXTRACTION_PROMPT,
    SKEPTIC_PROMPT,
    REVISION_PROMPT
)
from memory import (
    format_long_term_context,
    save_long_term_memory
)
from rag import get_retriever

OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434')

def ollama_chat(messages, stream=False, json_format=False):
    url = f"{OLLAMA_URL}/api/chat"
    payload = {
        "model": "gemma4:e4b",
        "messages": messages,
        "stream": stream
    }
    if json_format:
        payload["format"] = "json"
        payload["options"] = {"temperature": 0.2}
    else:
        payload["options"] = {"temperature": 0.85, "top_p": 0.95}
        
    try:
        response = requests.post(url, json=payload, stream=stream)
        response.raise_for_status()
        
        if stream:
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    content = chunk.get('message', {}).get('content', '')
                    if content:
                        yield content
        else:
            result = response.json()
            yield result.get('message', {}).get('content', '')
    except Exception as e:
        raise RuntimeError(f"Error communicating with Ollama: {e}")

def ollama_chat_sync(messages, json_format=False):
    generator = ollama_chat(messages, stream=False, json_format=json_format)
    return next(generator)


def get_multi_hop_context(query, top_k=3):
    retriever = get_retriever()
    
    results = retriever.retrieve_hybrid(query, top_k=top_k)
    docs = []
    for doc, score in results:
        docs.append(doc)
                
    final_parts = []
    sources = []
    for doc in docs:
        final_parts.append(f"[SOURCE: {doc['source']}]\nTopic: {doc['title']}\n{doc['content'].strip()}")
        if doc['title'] not in sources:
            sources.append(doc['title'])
            
    final_context = '\n\n---\n\n'.join(final_parts) if final_parts else 'No highly relevant sources retrieved.'
    return final_context, sources

def generate_topic_graph(topic):
    prompt = GRAPH_PROMPT.format(topic=topic)
    messages = [{'role': 'user', 'content': prompt}]
    text = ollama_chat_sync(messages, json_format=True).strip()
    try:
        return json.loads(text)
    except Exception:
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())

def explain_graph_topic(topic_label, core_topic):
    retriever = get_retriever()
    rag_context = retriever.format_context_hybrid(topic_label, top_k=2)
    
    prompt = EXPLAIN_PROMPT.format(
        topic_label=topic_label,
        core_topic=core_topic,
        rag_context=rag_context
    )
    messages = [{'role': 'user', 'content': prompt}]
    return ollama_chat_sync(messages)

def run_skeptic(user_query, retrieved_context, draft_answer):
    prompt = SKEPTIC_PROMPT.format(
        user_query=user_query,
        retrieved_context=retrieved_context,
        draft_answer=draft_answer
    )
    messages = [{'role': 'user', 'content': prompt}]
    try:
        text = ollama_chat_sync(messages, json_format=True).strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        return json.loads(text)
    except Exception as e:
        print(f"[Skeptic] Error running skeptic audit: {e}")
        return {"status": "pass", "issues": []}

def run_revision(user_query, retrieved_context, draft_answer, issues, advice=None):
    critique_str = json.dumps(issues, indent=2)
    if advice:
        critique_str += f"\n\nStyle & Tone Advice:\n{advice}"
    prompt = REVISION_PROMPT.format(
        user_query=user_query,
        retrieved_context=retrieved_context,
        draft_answer=draft_answer,
        critique=critique_str
    )
    messages = [{'role': 'user', 'content': prompt}]
    try:
        return ollama_chat_sync(messages).strip()
    except Exception as e:
        print(f"[Revision] Error running revision: {e}")
        return draft_answer


def should_check_for_facts(message):
    message_lower = message.lower()
    first_person_words = {'i', "i'm", "i've", "i'd", "i'll", 'my', 'me', 'myself', 'mine', 'we', 'our', 'us'}
    words = set(message_lower.split())
    if not words.intersection(first_person_words):
        return False
    personal_keywords = {
        'study', 'studies', 'student', 'research', 'work', 'working', 'interest', 'interested',
        'background', 'learn', 'learning', 'phd', 'degree', 'major', 'math', 'mathematician',
        'familiar', 'read', 'reading', 'solve', 'solving', 'class', 'course', 'university',
        'college', 'professor', 'school'
    }
    return any((kw in message_lower for kw in personal_keywords))

def extract_and_save_user_fact(user_message, long_term_memory):
    prompt = FACT_EXTRACTION_PROMPT.format(user_message=user_message[:300])
    messages = [{'role': 'user', 'content': prompt}]
    try:
        fact = ollama_chat_sync(messages).strip()
        if fact and fact != 'NONE':
            if 'user_facts' not in long_term_memory:
                long_term_memory['user_facts'] = []
            if fact not in long_term_memory['user_facts']:
                long_term_memory['user_facts'].append(fact)
                if len(long_term_memory['user_facts']) > 30:
                    long_term_memory['user_facts'] = long_term_memory['user_facts'][-30:]
                save_long_term_memory(long_term_memory)
    except Exception:
        pass

def send_message(user_message, conversation_history, long_term_memory, stream=True):
    rag_context, sources = get_multi_hop_context(user_message, top_k=3)
    memory_context = format_long_term_context(long_term_memory)
    
    try:
        import streamlit as st
        st.session_state['current_sources'] = sources
    except Exception:
        pass
        
    retrieved_context = f"RAG Context:\n{rag_context}\n\nMemory Context:\n{memory_context}"
    system_prompt = SYSTEM_PROMPT.format(rag_context=rag_context, memory_context=memory_context)
    
    messages = [{'role': 'system', 'content': system_prompt}]
    for msg in conversation_history[:-1]:
        role = 'user' if msg['role'] == 'user' else 'assistant'
        messages.append({'role': role, 'content': msg['content']})
    messages.append({'role': 'user', 'content': user_message})
    
    draft_answer = ollama_chat_sync(messages)
    
    skeptic_result = run_skeptic(user_message, retrieved_context, draft_answer)
    status = skeptic_result.get("status", "pass")
    issues = skeptic_result.get("issues", [])
    advice = skeptic_result.get("advice", "")

    if status == "revise" and len(issues) > 0:
        print(f"[Skeptic] Status: REVISE. Issues: {issues}")
        extra_queries = skeptic_result.get("queries", [])
        if extra_queries:
            retriever = get_retriever()
            extra_parts = []
            seen_extra = set()
            for eq in extra_queries:
                extra_results = retriever.retrieve_hybrid(eq, top_k=3)
                for doc, score in extra_results:
                    content_stripped = doc['content'].strip()
                    if content_stripped not in seen_extra:
                        seen_extra.add(content_stripped)
                        extra_parts.append(f"[SOURCE: {doc['source']}]\nTopic: {doc['title']}\n{content_stripped}")
                        if doc['title'] not in sources:
                            sources.append(doc['title'])
            try:
                import streamlit as st
                st.session_state['current_sources'] = sources
            except Exception:
                pass
            extra_context = "\n\n---\n\n".join(extra_parts) if extra_parts else ""
            combined_context = rag_context
            if extra_context:
                combined_context = f"{rag_context}\n\n---\n\n{extra_context}"
        else:
            combined_context = rag_context
        final_answer = run_revision(user_message, combined_context, draft_answer, issues, advice)
    else:
        print("[Skeptic] Status: PASS.")
        final_answer = draft_answer

    chunk_size = 8
    for i in range(0, len(final_answer), chunk_size):
        yield final_answer[i:i+chunk_size]
