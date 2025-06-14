# database.py
import sqlite3
import os

# Define the path for the database file
DB_FILE = "whatsapp_history.db"

def initialize_database():
    """Creates the database and the messages table if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Create table to store messages with sender's name
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_name TEXT NOT NULL,
            message_text TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def add_message(sender_name, message_text):
    """Adds a new message to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (sender_name, message_text) VALUES (?, ?)", (sender_name, message_text))
    # Keep the database from growing too large by keeping only the last 50 messages
    cursor.execute("DELETE FROM messages WHERE id NOT IN (SELECT id FROM messages ORDER BY timestamp DESC LIMIT 50)")
    conn.commit()
    conn.close()

def get_recent_messages(limit=20):
    """Retrieves the most recent messages from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT sender_name, message_text FROM messages ORDER BY timestamp DESC LIMIT ?", (limit,))
    messages = cursor.fetchall()
    conn.close()
    # Format as "Sender: Message" and reverse to get chronological order
    return [f"{sender}: {text}" for sender, text in reversed(messages)]

def clear_history():
    """Clears all messages from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages")
    conn.commit()
    conn.close()
    print("Conversation history cleared.")
