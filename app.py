import os
import json
import streamlit as st
from datetime import datetime

from memory import (
    load_long_term_memory,
    save_long_term_memory,
    add_notable_question,
    init_session_memory,
    add_message,
    get_api_messages,
    get_display_messages,
    extract_topics_from_exchange
)
from model import (
    generate_topic_graph,
    explain_graph_topic,
    send_message,
    should_check_for_facts,
    extract_and_save_user_fact
)

from streamlit_agraph import agraph, Node, Edge, Config

from rag import get_retriever
from scraper import list_local_documents

st.set_page_config(page_title='Terence Tao AI', layout='wide')

if 'session_memory' not in st.session_state:
    st.session_state.session_memory = init_session_memory()
if 'long_term_memory' not in st.session_state:
    st.session_state.long_term_memory = load_long_term_memory()
if 'session_saved' not in st.session_state:
    st.session_state.session_saved = False
if 'suggested_q' not in st.session_state:
    st.session_state.suggested_q = None
if 'explore_topic' not in st.session_state:
    st.session_state.explore_topic = ""
if 'explore_graph' not in st.session_state:
    st.session_state.explore_graph = None
if 'selected_node_id' not in st.session_state:
    st.session_state.selected_node_id = None
if 'node_explanation' not in st.session_state:
    st.session_state.node_explanation = None

title_col, new_chat_col, clear_mem_col = st.columns([4, 1, 1])
with title_col:
    st.title('Terence Tao AI')
with new_chat_col:
    if st.button('New Chat', use_container_width=True):
        st.session_state.session_memory = init_session_memory()
        st.session_state.session_saved = False
        st.session_state.explore_topic = ""
        st.session_state.explore_graph = None
        st.session_state.selected_node_id = None
        st.session_state.node_explanation = None
        st.rerun()
with clear_mem_col:
    if st.button('Clear Memory', use_container_width=True):
        st.session_state.long_term_memory = {'sessions': [], 'user_facts': [], 'discussed_topics': [], 'user_questions': [], 'last_updated': None}
        save_long_term_memory(st.session_state.long_term_memory)
        st.session_state.explore_topic = ""
        st.session_state.explore_graph = None
        st.session_state.selected_node_id = None
        st.session_state.node_explanation = None
        st.rerun()


chat_tab, visualize_tab, explore_tab, sync_tab = st.tabs(['Chat', 'Memory Visualization', 'Explore Mode', 'Knowledge Base & Sync'])

with chat_tab:
    msgs = get_display_messages(st.session_state.session_memory)
    chat_container = st.container()
    with chat_container:
        for msg in get_display_messages(st.session_state.session_memory):
            if msg['role'] == 'user':
                with st.chat_message('user'):
                    st.markdown(msg['content'])
            else:
                with st.chat_message('assistant'):
                    # Display Skeptic Peer Review Audit Expander if available
                    audit = msg.get('audit')
                    if audit:
                        status = audit.get('status', 'pass')
                        badge = "⚠️ Peer Review Audit: Revised" if status == 'revise' else "🛡️ Peer Review Audit: Passed"
                        with st.expander(badge, expanded=False):
                            if audit.get('issues'):
                                st.markdown("**Issues Identified & Corrected:**")
                                for iss in audit['issues']:
                                    st.markdown(f"- {iss}")
                            else:
                                st.markdown("✅ *All mathematical reasoning and bounds verified against literature.*")
                            if audit.get('advice'):
                                st.markdown(f"**Skeptic Notes:** *\"{audit['advice']}\"*")
                            if audit.get('draft'):
                                with st.expander("View Pre-Audit Draft"):
                                    st.code(audit['draft'], language="markdown")
                                    
                    st.markdown(msg['content'])
                    if 'sources' in msg and msg['sources']:
                        st.caption("Retrieved sources: " + ", ".join(msg['sources']))
                
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        user_input = st.text_area('Ask Terence Tao anything...', value='', height=90, placeholder='e.g. What is the key difficulty in the Kakeya conjecture?', label_visibility='collapsed', key='user_input_field')
    with col_btn:
        send_button = st.button('Send', use_container_width=True, type='primary')
        
    if send_button and user_input.strip():
        query = user_input.strip()
        add_message(st.session_state.session_memory, 'user', query)
        add_notable_question(st.session_state.long_term_memory, query)
        if should_check_for_facts(query):
            extract_and_save_user_fact(query, st.session_state.long_term_memory)
            
        with st.chat_message('assistant'):
            try:
                full_response = st.write_stream(send_message(user_message=query, conversation_history=get_api_messages(st.session_state.session_memory), long_term_memory=st.session_state.long_term_memory, stream=True))
            except Exception as e:
                error_msg = str(e)
                st.error(f'Error calling Ollama API: {error_msg}')
                st.session_state.session_memory['messages'].pop()
                st.session_state.session_memory['display_messages'].pop()
                st.stop()
                
        sources = st.session_state.get('current_sources', [])
        last_audit = st.session_state.get('last_audit', None)
        add_message(st.session_state.session_memory, 'assistant', full_response)
        if sources:
            st.session_state.session_memory['messages'][-1]['sources'] = sources
            st.session_state.session_memory['display_messages'][-1]['sources'] = sources
        if last_audit:
            st.session_state.session_memory['messages'][-1]['audit'] = last_audit
            st.session_state.session_memory['display_messages'][-1]['audit'] = last_audit
            
        topics = extract_topics_from_exchange(query, full_response)
        for topic in topics:
            if topic not in st.session_state.session_memory['topics_this_session']:
                st.session_state.session_memory['topics_this_session'].append(topic)
                if topic not in st.session_state.long_term_memory['discussed_topics']:
                    st.session_state.long_term_memory['discussed_topics'].append(topic)
        save_long_term_memory(st.session_state.long_term_memory)
        st.session_state['current_sources'] = None
        st.rerun()
        
    msg_count = len([m for m in get_display_messages(st.session_state.session_memory) if m['role'] == 'user'])
    if msg_count > 0:
        topics_this = st.session_state.session_memory.get('topics_this_session', [])
        info_parts = [f'{msg_count} exchanges this session']
        if topics_this:
            info_parts.append(f"Topics: {', '.join(topics_this[:4])}")
        st.caption(' · '.join(info_parts))

with visualize_tab:
    st.subheader('What the Agent Remembers')
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    discussed_topics = st.session_state.long_term_memory.get('discussed_topics', [])
    user_questions = st.session_state.long_term_memory.get('user_questions', [])
    user_facts = st.session_state.long_term_memory.get('user_facts', [])
    
    with col_stat1:
        st.metric('Mathematical Topics', len(discussed_topics))
    with col_stat2:
        st.metric('Notable Questions Asked', len(user_questions))
    with col_stat3:
        st.metric('Learned Profile Facts', len(user_facts))
        
    col_mem_left, col_mem_right = st.columns(2)
    with col_mem_left:
        st.markdown('### Explored Math Topics')
        if discussed_topics:
            for topic in discussed_topics:
                st.markdown(f"- {topic}")
        else:
            st.info('No mathematical topics registered yet.')
            
        st.markdown('### User Facts Profile')
        if user_facts:
            for fact in user_facts:
                st.markdown(f'{fact}')
        else:
            st.info('No personal facts learned from context yet.')
            
    with col_mem_right:
        st.markdown('### Stored Questions Timeline')
        if user_questions:
            for item in reversed(user_questions):
                try:
                    date_parsed = datetime.fromisoformat(item['date']).strftime('%b %d, %Y at %I:%M %p')
                except ValueError:
                    date_parsed = item['date']
                st.caption(date_parsed)
                st.write(item['question'])
                st.markdown("---")
        else:
            st.info('No questions logged in timeline history yet.')
            
    last_updated = st.session_state.long_term_memory.get('last_updated')
    if last_updated:
        try:
            formatted_updated = datetime.fromisoformat(last_updated).strftime('%b %d, %Y at %I:%M %p')
        except ValueError:
            formatted_updated = last_updated
        st.caption(f'Memory last synchronized: {formatted_updated}')

with explore_tab:
    st.subheader('Concept Explorer')
    st.markdown('Enter a mathematical topic below to generate a conceptual map of related topics.')

    col_exp_input, col_exp_btn = st.columns([5, 1])
    with col_exp_input:
        explore_query = st.text_input(
            'Topic to explore...',
            value=st.session_state.explore_topic if st.session_state.explore_topic else '',
            placeholder='e.g., Kakeya Conjecture',
            label_visibility='collapsed',
            key='explore_input_field'
        )
    with col_exp_btn:
        generate_btn = st.button('Explore', use_container_width=True, key='explore_submit_btn')

    if generate_btn and explore_query.strip():
        st.session_state.explore_topic = explore_query.strip()
        st.session_state.selected_node_id = None
        st.session_state.node_explanation = None
        
        with st.spinner(f"Mapping knowledge for '{st.session_state.explore_topic}'..."):
            try:
                st.session_state.explore_graph = generate_topic_graph(st.session_state.explore_topic)
            except Exception as e:
                st.error(f"Failed to generate knowledge map: {e}")
                st.session_state.explore_graph = None
        st.rerun()

    if st.session_state.explore_graph:
        nodes = st.session_state.explore_graph.get('nodes', [])
        edges = st.session_state.explore_graph.get('edges', [])
        
        st.markdown(f"### {st.session_state.explore_topic}")
        col_graph, col_info = st.columns([4, 2])
        
        with col_graph:
            
            agraph_nodes = []
            for n in nodes:
                agraph_nodes.append(Node(
                    id=n['id'], 
                    label=n['label'], 
                    title=n.get('description', ''),
                    size=20, 
                    shape="box"
                ))
            
            agraph_edges = []
            for e in edges:
                agraph_edges.append(Edge(
                    source=e.get('from') or e.get('source'),
                    target=e.get('to') or e.get('target'),
                    label=e.get('label', '')
                ))
            
            config = Config(
                width="100%",
                height=700,
                directed=True,
                interaction={
                    "dragNodes": False,
                    "dragView": False,
                    "zoomView": False
                }
            )
            config.physics = {
                "enabled": True,
                "solver": "forceAtlas2Based",
                "forceAtlas2Based": {
                    "gravitationalConstant": -150,
                    "centralGravity": 0.01,
                    "springLength": 220,
                    "springConstant": 0.08,
                    "damping": 0.4,
                    "avoidOverlap": 1.0
                },
                "stabilization": {
                    "enabled": True,
                    "iterations": 200,
                    "fit": True
                }
            }
            
            selected_node = agraph(nodes=agraph_nodes, edges=agraph_edges, config=config)
            
            if selected_node and selected_node != st.session_state.selected_node_id:
                st.session_state.selected_node_id = selected_node
                node_item = next((n for n in nodes if n['id'] == selected_node), None)
                if node_item:
                    with st.spinner(f"Formulating explanation for '{node_item['label']}'..."):
                        try:
                            st.session_state.node_explanation = explain_graph_topic(
                                topic_label=node_item['label'],
                                core_topic=st.session_state.explore_topic
                            )
                        except Exception as e:
                            st.session_state.node_explanation = f"Error generating explanation: {e}"
                st.rerun()
                
        with col_info:
            if st.session_state.selected_node_id:
                node_item = next((n for n in nodes if n['id'] == st.session_state.selected_node_id), None)
                if node_item:
                    st.markdown(f"#### {node_item['label']}")
                    
                    if st.session_state.node_explanation:
                        st.markdown(st.session_state.node_explanation)

with sync_tab:
    st.subheader("Terence Tao Blog Ingestion & Vector Knowledge Base")
    st.markdown("Automatically scrape mathematical expository posts and research updates from `terrytao.wordpress.com` into the RAG pipeline.")
    
    retriever = get_retriever()
    stats = retriever.get_stats()
    
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.metric(label="Total Markdown Documents", value=stats["documents_count"])
    with m_col2:
        st.metric(label="Indexed ChromaDB Chunks", value=stats["chunks_count"])
        
    st.markdown("---")
    st.markdown("#### Sync New Posts from terrytao.wordpress.com")
    
    sync_col1, sync_col2, sync_col3 = st.columns([2, 2, 1])
    with sync_col1:
        post_count = st.number_input("Number of posts to fetch", min_value=1, max_value=100, value=20, step=5)
    with sync_col2:
        category_filter = st.text_input("Category filter (optional)", placeholder="e.g. expository, math.CA, combinatorics")
    with sync_col3:
        force_sync = st.checkbox("Force overwrite", value=False)
        
    if st.button("Sync Now from Blog", type="primary", use_container_width=True):
        with st.spinner(f"Scraping and indexing {post_count} posts from Terence Tao's blog..."):
            try:
                summary = retriever.sync_from_web(
                    count=int(post_count),
                    category=category_filter.strip() if category_filter.strip() else None,
                    force=force_sync
                )
                st.success(f"Sync complete! Saved: {summary['saved']}, Updated: {summary['updated']}, Unchanged: {summary['skipped']} (Total processed: {summary['total_fetched']})")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to sync blog: {e}")
                
    st.markdown("---")
    st.markdown("#### Discover & Ingest Cited arXiv Research Papers")
    st.markdown("Scan all blog posts for cited preprints (`arxiv.org/abs/...`) and automatically ingest paper metadata, abstracts, and proofs via the official arXiv API.")
    
    ar_col1, ar_col2 = st.columns([3, 1])
    with ar_col1:
        arxiv_max = st.number_input("Max papers to fetch", min_value=5, max_value=200, value=30, step=5)
    with ar_col2:
        arxiv_force = st.checkbox("Force re-fetch papers", value=False)
        
    if st.button("Sync Cited arXiv Papers", use_container_width=True):
        with st.spinner(f"Ingesting cited arXiv papers into vector knowledge base..."):
            try:
                summary = retriever.sync_arxiv(max_papers=int(arxiv_max), force=arxiv_force)
                st.success(f"arXiv Sync complete! Discovered: {summary['total_discovered']}, Saved: {summary['total_saved']}, Already Indexed: {summary['already_indexed']}")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to sync arXiv papers: {e}")

    st.markdown("---")
    st.markdown("#### Indexed Knowledge Documents")
    all_docs = list_local_documents()
    if all_docs:
        doc_rows = []
        for d in all_docs:
            doc_rows.append({
                "Title": d["title"],
                "Date": d["date"] or "N/A",
                "Categories": ", ".join(d["categories"]) if d["categories"] else "General",
                "File": d["filename"],
                "Size (KB)": round(d["size_bytes"] / 1024, 1)
            })
        st.dataframe(doc_rows, use_container_width=True)
    else:
        st.info("No documents currently loaded in `documents/`.")