import os
import json
import streamlit as st
from datetime import datetime
import google.generativeai as genai

from prompts import SYSTEM_PROMPT, GRAPH_PROMPT, EXPLAIN_PROMPT, FACT_EXTRACTION_PROMPT
from memory import (
    load_long_term_memory,
    save_long_term_memory,
    add_notable_question,
    format_long_term_context,
    init_session_memory,
    add_message,
    get_api_messages,
    get_display_messages,
    extract_topics_from_exchange
)
from rag import get_retriever

from streamlit_agraph import agraph, Node, Edge, Config

def configure_gemini(api_key=None):
    if not api_key:
        api_key = os.environ.get('GEMINI_API_KEY')
    genai.configure(api_key=api_key)

def generate_topic_graph(topic, api_key=None):
    configure_gemini(api_key)
    prompt = GRAPH_PROMPT.format(topic=topic)
    model_instance = genai.GenerativeModel('gemini-2.5-flash')
    response = model_instance.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            response_mime_type="application/json"
        )
    )
    
    text = response.text.strip()
    try:
        return json.loads(text)
    except Exception:
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())

def explain_graph_topic(topic_label, core_topic, api_key=None):
    configure_gemini(api_key)
    retriever = get_retriever()
    rag_context = retriever.format_context(topic_label, top_k=2)
    
    prompt = EXPLAIN_PROMPT.format(
        topic_label=topic_label,
        core_topic=core_topic,
        rag_context=rag_context
    )
    model_instance = genai.GenerativeModel('gemini-2.5-flash')
    response = model_instance.generate_content(prompt)
    return response.text

def build_system_prompt(user_query, long_term_memory):
    retriever = get_retriever()
    rag_context = retriever.format_context(user_query, top_k=3)
    memory_context = format_long_term_context(long_term_memory)
    return SYSTEM_PROMPT.format(rag_context=rag_context, memory_context=memory_context)

def send_message(user_message, conversation_history, long_term_memory, api_key=None, model_name='gemini-2.5-flash', stream=True):
    configure_gemini(api_key)
    system_prompt = build_system_prompt(user_message, long_term_memory)
    model_instance = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_prompt,
        generation_config=genai.types.GenerationConfig(temperature=0.85, top_p=0.95, max_output_tokens=4096)
    )
    history = []
    for msg in conversation_history[:-1]:
        role = 'user' if msg['role'] == 'user' else 'model'
        history.append({'role': role, 'parts': [msg['content']]})
    chat = model_instance.start_chat(history=history)
    if stream:
        response = chat.send_message(user_message, stream=True)
        for chunk in response:
            try:
                if chunk.text:
                    yield chunk.text
            except (ValueError, AttributeError, IndexError):
                pass
    else:
        response = chat.send_message(user_message)
        yield response.text

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

def extract_and_save_user_fact(user_message, api_key):
    configure_gemini(api_key)
    prompt = FACT_EXTRACTION_PROMPT.format(user_message=user_message[:300])
    model_instance = genai.GenerativeModel('gemini-2.5-flash')
    try:
        response = model_instance.generate_content(prompt)
        fact = response.text.strip()
        if fact and fact != 'NONE':
            memory = st.session_state.long_term_memory
            if 'user_facts' not in memory:
                memory['user_facts'] = []
            if fact not in memory['user_facts']:
                memory['user_facts'].append(fact)
                if len(memory['user_facts']) > 30:
                    memory['user_facts'] = memory['user_facts'][-30:]
                save_long_term_memory(memory)
    except Exception:
        pass

st.set_page_config(page_title='Terence Tao AI', layout='wide')

if 'session_memory' not in st.session_state:
    st.session_state.session_memory = init_session_memory()
if 'long_term_memory' not in st.session_state:
    st.session_state.long_term_memory = load_long_term_memory()
if 'retriever' not in st.session_state:
    st.session_state.retriever = get_retriever()
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

api_key = os.environ.get('GEMINI_API_KEY')
model = 'gemini-2.5-flash'

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


chat_tab, visualize_tab, explore_tab = st.tabs(['Chat', 'Memory Visualization', 'Explore Mode'])

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
                    st.markdown(msg['content'])
                    
    if msgs and msgs[-1]['role'] == 'assistant':
        last_user_msgs = [m for m in msgs if m['role'] == 'user']
        if last_user_msgs:
            last_query = last_user_msgs[-1]['content']
            retrieved = st.session_state.retriever.retrieve(last_query, top_k=3)
            if retrieved:
                sources = [doc['title'] for doc, score in retrieved if score > 0.02]
                if sources:
                    st.caption("Retrieved sources: " + ", ".join(sources))
                
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
            extract_and_save_user_fact(query, api_key)
            
        with st.chat_message('assistant'):
            try:
                full_response = st.write_stream(send_message(user_message=query, conversation_history=get_api_messages(st.session_state.session_memory), long_term_memory=st.session_state.long_term_memory, api_key=api_key, model_name=model, stream=True))
            except Exception as e:
                error_msg = str(e)
                if 'API_KEY' in error_msg.upper():
                    st.error('Invalid or missing API key. Check your Gemini API key.')
                elif 'QUOTA' in error_msg.upper():
                    st.error('API quota exceeded. Please try again later.')
                else:
                    st.error(f'Error calling Gemini API: {error_msg}')
                st.session_state.session_memory['messages'].pop()
                st.session_state.session_memory['display_messages'].pop()
                st.stop()
                
        add_message(st.session_state.session_memory, 'assistant', full_response)
        topics = extract_topics_from_exchange(query, full_response)
        for topic in topics:
            if topic not in st.session_state.session_memory['topics_this_session']:
                st.session_state.session_memory['topics_this_session'].append(topic)
                if topic not in st.session_state.long_term_memory['discussed_topics']:
                    st.session_state.long_term_memory['discussed_topics'].append(topic)
        save_long_term_memory(st.session_state.long_term_memory)
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
                st.session_state.explore_graph = generate_topic_graph(st.session_state.explore_topic, api_key)
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
                                core_topic=st.session_state.explore_topic,
                                api_key=api_key
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