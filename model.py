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
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'gemma4:e2b')

def get_current_model_name():
    return OLLAMA_MODEL

def ollama_chat(messages, stream=False, json_format=False, model=None):
    url = f"{OLLAMA_URL}/api/chat"
    target_model = model or OLLAMA_MODEL
    payload = {
        "model": target_model,
        "messages": messages,
        "stream": stream
    }
    if json_format:
        payload["format"] = "json"
        payload["options"] = {"temperature": 0.2}
    else:
        payload["options"] = {"temperature": 0.85, "top_p": 0.95}
        
    try:
        response = requests.post(url, json=payload, stream=stream, timeout=60)
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
        raise RuntimeError(f"Error communicating with Ollama ({target_model}): {e}")

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

def send_message_detailed(user_message, conversation_history, long_term_memory):
    """
    Orchestrates draft generation, skeptic peer review audit, and final revision,
    yielding structured event dictionaries:
      - {'type': 'phase', 'phase': 'retrieving', 'sources': sources}
      - {'type': 'phase', 'phase': 'drafting'}
      - {'type': 'draft', 'content': draft_answer}
      - {'type': 'phase', 'phase': 'auditing'}
      - {'type': 'audit', 'data': audit_data}
      - {'type': 'phase', 'phase': 'revising'} (if revision occurred)
      - {'type': 'chunk', 'content': token}
      - {'type': 'done', 'response': final_answer, 'audit': audit_data, 'sources': sources}
    """
    rag_context, sources = get_multi_hop_context(user_message, top_k=3)
    memory_context = format_long_term_context(long_term_memory)
    
    yield {"type": "phase", "phase": "retrieving", "sources": sources}
    
    retrieved_context = f"RAG Context:\n{rag_context}\n\nMemory Context:\n{memory_context}"
    system_prompt = SYSTEM_PROMPT.format(rag_context=rag_context, memory_context=memory_context)
    
    messages = [{'role': 'system', 'content': system_prompt}]
    for msg in conversation_history[:-1]:
        role = 'user' if msg.get('role') == 'user' else 'assistant'
        messages.append({'role': role, 'content': msg.get('content', '')})
    messages.append({'role': 'user', 'content': user_message})
    
    yield {"type": "phase", "phase": "drafting"}
    draft_answer = ollama_chat_sync(messages)
    yield {"type": "draft", "content": draft_answer}
    
    yield {"type": "phase", "phase": "auditing"}
    skeptic_result = run_skeptic(user_message, retrieved_context, draft_answer)
    status = skeptic_result.get("status", "pass")
    issues = skeptic_result.get("issues", [])
    advice = skeptic_result.get("advice", "")
    
    extra_sources = []
    if status == "revise" and len(issues) > 0:
        yield {"type": "phase", "phase": "revising"}
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
                            extra_sources.append(doc['title'])
            extra_context = "\n\n---\n\n".join(extra_parts) if extra_parts else ""
            combined_context = f"{rag_context}\n\n---\n\n{extra_context}" if extra_context else rag_context
        else:
            combined_context = rag_context
            
        final_answer = run_revision(user_message, combined_context, draft_answer, issues, advice)
    else:
        print("[Skeptic] Status: PASS.")
        final_answer = draft_answer
        
    audit_data = {
        "status": status,
        "issues": issues,
        "advice": advice,
        "draft": draft_answer,
        "extra_sources": extra_sources,
        "checked_sources": sources
    }
    
    yield {"type": "audit", "data": audit_data}
    
    chunk_size = 8
    for i in range(0, len(final_answer), chunk_size):
        yield {"type": "chunk", "content": final_answer[i:i+chunk_size]}
        
    yield {
        "type": "done",
        "response": final_answer,
        "audit": audit_data,
        "sources": sources
    }

def send_message(user_message, conversation_history, long_term_memory, stream=True):
    """Backwards-compatible helper that yields response text chunks and saves audit to streamlit session if available."""
    final_answer = ""
    audit_data = None
    sources = []
    
    for event in send_message_detailed(user_message, conversation_history, long_term_memory):
        if event["type"] == "chunk":
            yield event["content"]
        elif event["type"] == "done":
            final_answer = event["response"]
            audit_data = event.get("audit")
            sources = event.get("sources", [])
            try:
                import streamlit as st
                st.session_state['current_sources'] = sources
                st.session_state['last_audit'] = audit_data
            except Exception:
                pass
