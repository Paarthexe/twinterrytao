import streamlit as st
import os
from datetime import datetime
import google.generativeai as genai
from typing import List, Dict, Optional
from persona import SYSTEM_PROMPT
from memory import *
from rag import get_retriever

def configure_gemini(api_key=None):
    if not api_key:
        api_key = os.environ.get('GEMINI_API_KEY')
    genai.configure(api_key=api_key)

def build_system_prompt(user_query, long_term_memory):
    retriever = get_retriever()
    rag_context = retriever.format_context(user_query, top_k=3)
    memory_context = format_long_term_context(long_term_memory)
    return SYSTEM_PROMPT.format(rag_context=rag_context, memory_context=memory_context)

def send_message(user_message, conversation_history, long_term_memory, api_key=None, model_name='gemini-2.5-flash', stream=True):
    configure_gemini(api_key)
    system_prompt = build_system_prompt(user_message, long_term_memory)
    model = genai.GenerativeModel(model_name=model_name, system_instruction=system_prompt, generation_config=genai.types.GenerationConfig(temperature=0.85, top_p=0.95, max_output_tokens=4096))
    history = []
    for msg in conversation_history[:-1]:
        role = 'user' if msg['role'] == 'user' else 'model'
        history.append({'role': role, 'parts': [msg['content']]})
    chat = model.start_chat(history=history)
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
    prompt = f"""Does this message reveal any personal fact about the user, such as their mathematical background,
     education level, research area, or interests?\nIf yes, state the fact in one short sentence starting with 
     'User is' or 'User studies' or similar. Do not include any other text. If no, reply with just: NONE
    Message: {user_message[:300]}\n"""
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
st.set_page_config(page_title='Terence Tao AI', page_icon='∮', layout='wide', initial_sidebar_state='collapsed')
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
api_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
model = 'gemini-2.5-flash'
(col_title, col_btn_new, col_btn_clear) = st.columns([4, 1, 1])
with col_title:
    st.title('Terence Tao AI')
with col_btn_new:
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    if st.button('New Chat', use_container_width=True):
        st.session_state.session_memory = init_session_memory()
        st.session_state.session_saved = False
        st.rerun()
with col_btn_clear:
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    if st.button('Clear Memory', use_container_width=True):
        st.session_state.long_term_memory = {'sessions': [], 'user_facts': [], 'discussed_topics': [], 'user_questions': [], 'last_updated': None}
        save_long_term_memory(st.session_state.long_term_memory)
        st.rerun()
if not api_key:
    st.error('**API Key is missing!** Please set the `GEMINI_API_KEY` or `GOOGLE_API_KEY` environment variable in your terminal and restart the application.')
    st.stop()
(tab_chat, tab_visualize) = st.tabs(['Chat', 'Memory Visualization'])
with tab_chat:
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
                source_html = '<div style="margin-top:0.5rem; margin-bottom:1rem">'
                source_html += '<span style="font-size:0.75rem; color:#94a3b8">Retrieved sources: </span>'
                for (doc, score) in retrieved:
                    if score > 0.02:
                        short_title = doc['title'][:50]
                        source_html += f'<span style="font-size: 0.75rem; color: #64748b; background: #f1f5f9; border: 1px solid #e2e8f0; padding: 4px 10px; border-radius: 20px; display: inline-block; margin: 4px 3px; font-family: monospace;">{short_title}</span>'
                source_html += '</div>'
                st.markdown(source_html, unsafe_allow_html=True)
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    default_value = ''
    (col_input, col_btn) = st.columns([5, 1])
    with col_input:
        user_input = st.text_area('Ask Terence Tao anything...', value=default_value, height=90, placeholder='e.g. What is the key difficulty in the Kakeya conjecture?', label_visibility='collapsed', key='user_input_field')
    with col_btn:
        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        send_button = st.button('Send →', use_container_width=True, type='primary')
    if send_button and user_input.strip():
        query = user_input.strip()
        add_message(st.session_state.session_memory, 'user', query)
        add_notable_question(st.session_state.long_term_memory, query)
        if should_check_for_facts(query):
            extract_and_save_user_fact(query, api_key)
        with st.chat_message('assistant'):
            full_response = ''
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
        info_parts = [f'**{msg_count}** exchanges this session']
        if topics_this:
            info_parts.append(f"Topics: {', '.join(topics_this[:4])}")
        st.caption(' · '.join(info_parts))
with tab_visualize:
    st.subheader('What the Agent Remembers')
    (col_stat1, col_stat2, col_stat3) = st.columns(3)
    discussed_topics = st.session_state.long_term_memory.get('discussed_topics', [])
    user_questions = st.session_state.long_term_memory.get('user_questions', [])
    user_facts = st.session_state.long_term_memory.get('user_facts', [])
    with col_stat1:
        st.metric('Mathematical Topics', len(discussed_topics))
    with col_stat2:
        st.metric('Notable Questions Asked', len(user_questions))
    with col_stat3:
        st.metric('Learned Profile Facts', len(user_facts))
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    (col_mem_left, col_mem_right) = st.columns(2)
    with col_mem_left:
        st.markdown('### Explored Math Topics')
        if discussed_topics:
            pills_html = "<div style='display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px;'>"
            for topic in discussed_topics:
                pills_html += f'<span style="background-color: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; border-radius: 20px; padding: 6px 12px; font-size: 0.85rem; font-weight: 500; font-family: sans-serif;">{topic}</span>'
            pills_html += '</div>'
            st.markdown(pills_html, unsafe_allow_html=True)
        else:
            st.info('No mathematical topics registered yet.')
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        st.markdown('### User Facts Profile')
        if user_facts:
            for fact in user_facts:
                st.markdown(f'**{fact}**')
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
                st.markdown(f"""\n                <div style="background-color: #f8fafc; border-left: 4px solid #6366f1; padding: 10px 16px; border-radius: 6px; margin-bottom: 12px; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);">\n                    <div style="font-size: 0.78rem; color: #94a3b8; font-weight: 500;">{date_parsed}</div>\n                    <div style="font-size: 0.92rem; color: #334155; font-weight: 600; margin-top: 4px; line-height: 1.4;">{item['question']}</div>\n                </div>\n                """, unsafe_allow_html=True)
        else:
            st.info('No questions logged in timeline history yet.')
    last_updated = st.session_state.long_term_memory.get('last_updated')
    if last_updated:
        try:
            formatted_updated = datetime.fromisoformat(last_updated).strftime('%b %d, %Y at %I:%M %p')
        except ValueError:
            formatted_updated = last_updated
        st.caption(f'Memory last synchronized: {formatted_updated}')