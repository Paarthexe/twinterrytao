import os
import json
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

from memory import (
    load_long_term_memory,
    save_long_term_memory,
    add_notable_question,
    extract_topics_from_exchange
)
from model import (
    generate_topic_graph,
    explain_graph_topic,
    send_message,
    send_message_detailed,
    get_current_model_name,
    should_check_for_facts,
    extract_and_save_user_fact,
    get_multi_hop_context
)
from rag import get_retriever
from scraper import list_local_documents

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        retriever = get_retriever()
        stats = retriever.get_stats()
        items = stats["chunks_count"]
        docs_count = stats["documents_count"]
    except Exception as e:
        items = 0
        docs_count = 0
    return jsonify({
        "status": "ok",
        "chroma_items": items,
        "documents_count": docs_count,
        "model": get_current_model_name()
    })

@app.route('/api/documents', methods=['GET'])
def get_documents():
    try:
        retriever = get_retriever()
        docs = list_local_documents()
        stats = retriever.get_stats()
        return jsonify({
            "status": "success",
            "documents": docs,
            "stats": stats
        })
    except Exception as e:
        return jsonify({"error": f"Failed to list documents: {str(e)}"}), 500

@app.route('/api/documents/sync', methods=['POST'])
def sync_documents():
    data = request.json or {}
    count = int(data['count']) if 'count' in data and data['count'] is not None else None
    all_posts = bool(data.get('all', count is None))
    category = data.get('category') or None
    search = data.get('search') or None
    tag = data.get('tag') or None
    force = bool(data.get('force', False))
    
    try:
        retriever = get_retriever()
        summary = retriever.sync_from_web(
            count=count,
            all_posts=all_posts,
            category=category,
            search=search,
            tag=tag,
            force=force
        )
        stats = retriever.get_stats()
        return jsonify({
            "status": "success",
            "message": f"Successfully processed {summary['total_fetched']} posts from Terence Tao's blog.",
            "summary": summary,
            "stats": stats
        })
    except Exception as e:
        return jsonify({"error": f"Failed to sync documents: {str(e)}"}), 500

@app.route('/api/arxiv/sync', methods=['POST'])
def sync_arxiv():
    data = request.json or {}
    max_papers = int(data.get('max_papers', 50))
    force = bool(data.get('force', False))
    
    try:
        retriever = get_retriever()
        summary = retriever.sync_arxiv(max_papers=max_papers, force=force)
        stats = retriever.get_stats()
        return jsonify({
            "status": "success",
            "message": f"Successfully ingested {summary['total_saved']} arXiv research papers.",
            "summary": summary,
            "stats": stats
        })
    except Exception as e:
        return jsonify({"error": f"Failed to sync arXiv papers: {str(e)}"}), 500


@app.route('/api/memory', methods=['GET'])
def get_memory():
    memory = load_long_term_memory()
    discussed_topics = memory.get('discussed_topics', [])
    user_questions = memory.get('user_questions', [])
    user_facts = memory.get('user_facts', [])
    last_updated = memory.get('last_updated')
    
    return jsonify({
        "discussed_topics": discussed_topics,
        "user_questions": user_questions,
        "user_facts": user_facts,
        "last_updated": last_updated,
        "stats": {
            "topics_count": len(discussed_topics),
            "questions_count": len(user_questions),
            "facts_count": len(user_facts)
        }
    })

@app.route('/api/memory/clear', methods=['POST'])
def clear_memory():
    empty_mem = {
        'sessions': [],
        'user_facts': [],
        'discussed_topics': [],
        'user_questions': [],
        'last_updated': None
    }
    save_long_term_memory(empty_mem)
    return jsonify({"status": "success", "message": "Memory cleared"})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json or {}
    message = data.get('message', '').strip()
    history = data.get('history', [])
    
    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400
        
    long_term_memory = load_long_term_memory()
    
    add_notable_question(long_term_memory, message)
    if should_check_for_facts(message):
        extract_and_save_user_fact(message, long_term_memory)
        
    full_response = ""
    audit_data = None
    sources = []
    
    for event in send_message_detailed(
        user_message=message,
        conversation_history=history,
        long_term_memory=long_term_memory
    ):
        if event["type"] == "done":
            full_response = event["response"]
            audit_data = event.get("audit")
            sources = event.get("sources", [])
            
    topics = extract_topics_from_exchange(message, full_response)
    updated_topics = False
    for topic in topics:
        if topic not in long_term_memory.get('discussed_topics', []):
            if 'discussed_topics' not in long_term_memory:
                long_term_memory['discussed_topics'] = []
            long_term_memory['discussed_topics'].append(topic)
            updated_topics = True
            
    if updated_topics:
        save_long_term_memory(long_term_memory)
        
    return jsonify({
        "response": full_response,
        "sources": sources,
        "audit": audit_data,
        "topics": topics
    })

@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    data = request.json or {}
    message = data.get('message', '').strip()
    history = data.get('history', [])
    
    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400
        
    long_term_memory = load_long_term_memory()
    
    add_notable_question(long_term_memory, message)
    if should_check_for_facts(message):
        extract_and_save_user_fact(message, long_term_memory)
        
    def generate():
        full_response = ""
        audit_data = None
        sources = []
        
        for event in send_message_detailed(
            user_message=message,
            conversation_history=history,
            long_term_memory=long_term_memory
        ):
            if event["type"] == "phase":
                yield f"data: {json.dumps({'type': 'phase', 'phase': event['phase'], 'sources': event.get('sources', [])})}\n\n"
            elif event["type"] == "draft":
                yield f"data: {json.dumps({'type': 'draft', 'content': event['content']})}\n\n"
            elif event["type"] == "audit":
                audit_data = event.get("data")
                yield f"data: {json.dumps({'type': 'audit', 'data': audit_data})}\n\n"
            elif event["type"] == "chunk":
                yield f"data: {json.dumps({'type': 'chunk', 'content': event['content']})}\n\n"
            elif event["type"] == "done":
                full_response = event["response"]
                audit_data = event.get("audit")
                sources = event.get("sources", [])
                
        topics = extract_topics_from_exchange(message, full_response)
        updated_topics = False
        for topic in topics:
            if topic not in long_term_memory.get('discussed_topics', []):
                if 'discussed_topics' not in long_term_memory:
                    long_term_memory['discussed_topics'] = []
                long_term_memory['discussed_topics'].append(topic)
                updated_topics = True
                
        if updated_topics:
            save_long_term_memory(long_term_memory)
            
        yield f"data: {json.dumps({'type': 'done', 'response': full_response, 'audit': audit_data, 'sources': sources, 'topics': topics})}\n\n"

    return Response(generate(), mimetype='text/event-stream')

@app.route('/api/explore/graph', methods=['POST'])
def explore_graph():
    data = request.json or {}
    topic = data.get('topic', '').strip()
    
    if not topic:
        return jsonify({"error": "Topic cannot be empty"}), 400
        
    try:
        graph = generate_topic_graph(topic)
        return jsonify({"graph": graph})
    except Exception as e:
        return jsonify({"error": f"Failed to generate graph: {str(e)}"}), 500

@app.route('/api/explore/explain', methods=['POST'])
def explore_explain():
    data = request.json or {}
    topic_label = data.get('topic_label', '').strip()
    core_topic = data.get('core_topic', '').strip()
    
    if not topic_label or not core_topic:
        return jsonify({"error": "Missing topic_label or core_topic"}), 400
        
    try:
        explanation = explain_graph_topic(topic_label=topic_label, core_topic=core_topic)
        return jsonify({"explanation": explanation})
    except Exception as e:
        return jsonify({"error": f"Failed to generate explanation: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"Starting Terence Tao AI Flask Backend on port {port}...")
    # Initialize retriever and perform automatic blog sync
    get_retriever()
    app.run(host='0.0.0.0', port=port, debug=True)
