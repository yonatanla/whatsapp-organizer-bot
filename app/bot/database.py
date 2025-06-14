# app/bot/database.py
import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "whatsapp_history.db")

def initialize_database():
    """Creates the database and tables if they don't exist."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_name TEXT NOT NULL,
                message_text TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_description TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending'
            )
        ''')
    print("Database initialized successfully.")

def add_message(sender_name, message_text):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (sender_name, message_text) VALUES (?, ?)", (sender_name, message_text))
        cursor.execute("DELETE FROM messages WHERE id NOT IN (SELECT id FROM messages ORDER BY timestamp DESC LIMIT 50)")

def get_recent_messages(limit=20):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT sender_name, message_text FROM messages ORDER BY timestamp DESC LIMIT ?", (limit,))
        messages = cursor.fetchall()
    return [f"{sender}: {text}" for sender, text in reversed(messages)]

def clear_history():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("DELETE FROM messages")
    print("Conversation history cleared.")

def add_task(task_description):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task_description) VALUES (?)", (task_description,))
        return f"✅ משימה נוספה: {task_description}"

def get_tasks():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, task_description FROM tasks WHERE status = 'pending'")
        return cursor.fetchall()

def complete_task(task_id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,))
        if conn.total_changes > 0:
            return f"✅ משימה {task_id} הושלמה!"
        return f"🤔 לא נמצאה משימה עם המספר {task_id}."