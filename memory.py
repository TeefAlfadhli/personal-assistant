# memory.py
import sqlite3
from datetime import datetime

DB_PATH = "database.db"

def log_conversation(user_input, agent_response):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO conversations (user_input, agent_response, timestamp)
        VALUES (?, ?, ?)
    """, (user_input, agent_response, timestamp))
    conn.commit()
    conn.close()

def get_conversation_history(limit=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_input, agent_response FROM conversations
        ORDER BY id DESC LIMIT ?
    """, (limit,))
    history = cursor.fetchall()
    conn.close()
    return history[::-1]  # Reverse to show oldest first