import sqlite3
from datetime import datetime
from pydantic import BaseModel
from enum import Enum
from typing import Optional

# SQLite connection
conn = sqlite3.connect('chat.db', check_same_thread=False)
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        created_at TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        message_id TEXT PRIMARY KEY,
        sender TEXT,
        recipient TEXT,
        content TEXT,
        timestamp TEXT,
        status TEXT,
        is_bot_response INTEGER
    )
''')

conn.commit()

class MessageStatus(str, Enum):
    SENT = "Sent"
    DELIVERED = "Delivered"
    READ = "Read"

class Message(BaseModel):
    message_id: str
    sender: str
    recipient: str
    content: str
    timestamp: datetime
    status: MessageStatus
    is_bot_response: bool

class User(BaseModel):
    email: str
    created_at: datetime
    # Add more fields as needed

def create_message(message: Message):
    cursor.execute('''
        INSERT INTO messages (message_id, sender, recipient, content, timestamp, status, is_bot_response)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (message.message_id, message.sender, message.recipient, message.content,
          message.timestamp.isoformat(), message.status.value, int(message.is_bot_response)))
    conn.commit()

def get_conversation(user1: str, user2: str):
    cursor.execute('''
        SELECT * FROM messages
        WHERE (sender = ? AND recipient = ?) OR (sender = ? AND recipient = ?)
        ORDER BY timestamp
    ''', (user1, user2, user2, user1))
    rows = cursor.fetchall()
    messages = []
    for row in rows:
        messages.append({
            'message_id': row[0],
            'sender': row[1],
            'recipient': row[2],
            'content': row[3],
            'timestamp': row[4],
            'status': row[5],
            'is_bot_response': bool(row[6])
        })
    return messages

def update_message_status(message_id: str, status: MessageStatus):
    cursor.execute('UPDATE messages SET status = ? WHERE message_id = ?', (status.value, message_id))
    conn.commit()

def create_user(email: str):
    cursor.execute('INSERT OR IGNORE INTO users (email, created_at) VALUES (?, ?)',
                   (email, datetime.utcnow().isoformat()))
    conn.commit()

def get_user(email: str):
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    row = cursor.fetchone()
    if row:
        return {'email': row[0], 'created_at': row[1]}
    return None
