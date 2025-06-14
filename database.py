# database.py
import sqlite3
import os

DB_FILE = "whatsapp_history.db"

def initialize_database():
    """Creates the database and tables if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Table for conversation history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_name TEXT NOT NULL,
            message_text TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # NEW: Table for tasks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending'
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

# --- Message History Functions ---
def add_message(sender_name, message_text):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (sender_name, message_text) VALUES (?, ?)", (sender_name, message_text))
    cursor.execute("DELETE FROM messages WHERE id NOT IN (SELECT id FROM messages ORDER BY timestamp DESC LIMIT 50)")
    conn.commit()
    conn.close()

def get_recent_messages(limit=20):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT sender_name, message_text FROM messages ORDER BY timestamp DESC LIMIT ?", (limit,))
    messages = cursor.fetchall()
    conn.close()
    return [f"{sender}: {text}" for sender, text in reversed(messages)]

def clear_history():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages")
    conn.commit()
    conn.close()
    print("Conversation history cleared.")

# --- NEW: Task Management Functions ---
def add_task(task_description):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task_description) VALUES (?)", (task_description,))
    conn.commit()
    conn.close()
    return f"✅ משימה נוספה: {task_description}"

def get_tasks():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, task_description FROM tasks WHERE status = 'pending'")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def complete_task(task_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,))
    conn.commit()
    # Check if the update was successful
    if conn.total_changes > 0:
        return f"✅ משימה {task_id} הושלמה!"
    else:
        return f"🤔 לא נמצאה משימה עם המספר {task_id}."