import json
import os
from datetime import datetime
from typing import List, Dict, Optional
LONG_TERM_MEMORY_PATH = 'long_term_memory.json'

def load_long_term_memory():
    if os.path.exists(LONG_TERM_MEMORY_PATH):
        try:
            with open(LONG_TERM_MEMORY_PATH, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {'sessions': [], 'user_facts': [], 'discussed_topics': [], 'user_questions': [], 'last_updated': None}

def save_long_term_memory(memory):
    memory['last_updated'] = datetime.now().isoformat()
    try:
        with open(LONG_TERM_MEMORY_PATH, 'w') as f:
            json.dump(memory, f, indent=2)
    except IOError as e:
        print(f'Warning: could not save long-term memory: {e}')

def add_notable_question(memory, question):
    memory['user_questions'].append({'date': datetime.now().isoformat(), 'question': question[:300]})
    if len(memory['user_questions']) > 50:
        memory['user_questions'] = memory['user_questions'][-50:]
    save_long_term_memory(memory)

def format_long_term_context(memory):
    parts = []
    if memory.get('user_facts'):
        parts.append('Things I know about this person:\n' + '\n'.join((f'- {f}' for f in memory['user_facts'][-10:])))
    if memory.get('discussed_topics'):
        recent = memory['discussed_topics'][-15:]
        parts.append('Mathematical topics we have discussed before:\n' + ', '.join(recent))
    if memory.get('sessions'):
        recent_sessions = memory['sessions'][-3:]
        summaries = []
        for s in recent_sessions:
            date_str = s['date'][:10]
            summaries.append(f"[{date_str}] {s['summary']}")
        parts.append('Recent conversation summaries:\n' + '\n'.join(summaries))
    if not parts:
        return 'This is the first conversation with this person.'
    return '\n\n'.join(parts)

def init_session_memory():
    return {'messages': [], 'display_messages': [], 'session_start': datetime.now().isoformat(), 'topics_this_session': []}

def add_message(session, role, content):
    session['messages'].append({'role': role, 'content': content})
    session['display_messages'].append({'role': role, 'content': content})
    if len(session['messages']) > 40:
        session['messages'] = session['messages'][-40:]

def get_api_messages(session):
    return session['messages']

def get_display_messages(session):
    return session['display_messages']

def extract_topics_from_exchange(user_msg, assistant_msg):
    topic_keywords = {'Green-Tao theorem': ['green-tao', 'green tao', 'arithmetic progression', 'primes progression'], 'Compressed sensing': ['compressed sensing', 'RIP', 'restricted isometry', 'sparse signal'], 'Navier-Stokes': ['navier-stokes', 'navier stokes', 'fluid dynamics', 'blowup'], 'Erdős discrepancy': ['erdos discrepancy', 'erdős discrepancy', 'discrepancy'], 'Random matrix theory': ['random matrix', 'eigenvalue', 'GUE', 'wigner'], 'Additive combinatorics': ['additive combinatorics', 'sumset', 'sum-product'], 'Harmonic analysis': ['harmonic analysis', 'fourier', 'restriction conjecture'], 'Number theory': ['prime number', 'riemann', 'number theory', 'chowla'], 'PDE': ['partial differential', 'nonlinear schrodinger', 'dispersive', 'wave equation'], 'Collatz conjecture': ['collatz'], 'Szemerédi theorem': ['szemeredi', 'szemerédi', 'density hales-jewett'], 'Gowers norms': ['gowers norm', 'uniformity norm', 'higher order fourier']}
    text = (user_msg + ' ' + assistant_msg).lower()
    found = []
    for (topic, keywords) in topic_keywords.items():
        if any((kw in text for kw in keywords)):
            found.append(topic)
    return found