import mysql.connector
from mysql.connector import Error
from datetime import datetime
from pydantic import BaseModel
from enum import Enum
from typing import Optional
import os

# MySQL connection configuration
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'chatapp')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))

# Create MySQL connection
def create_connection():
    """Create a database connection to MySQL"""
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            port=MYSQL_PORT
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

# Initialize connection and cursor
conn = create_connection()
if conn:
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email VARCHAR(255) PRIMARY KEY,
            created_at DATETIME
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            message_id VARCHAR(255) PRIMARY KEY,
            sender VARCHAR(255),
            recipient VARCHAR(255),
            content TEXT,
            timestamp DATETIME,
            status VARCHAR(50),
            is_bot_response BOOLEAN
        )
    ''')
    
    conn.commit()
else:
    print("Failed to connect to MySQL database. Please check your configuration.")
    cursor = None

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
    if cursor is None:
        print("Database connection not available")
        return
    
    cursor.execute('''
        INSERT INTO messages (message_id, sender, recipient, content, timestamp, status, is_bot_response)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (message.message_id, message.sender, message.recipient, message.content,
          message.timestamp, message.status.value, message.is_bot_response))
    conn.commit()

def get_conversation(user1: str, user2: str):
    if cursor is None:
        print("Database connection not available")
        return []
        
    cursor.execute('''
        SELECT message_id, sender, recipient, content, timestamp, status, is_bot_response
        FROM messages
        WHERE (sender = %s AND recipient = %s) OR (sender = %s AND recipient = %s)
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
            'timestamp': row[4].isoformat() if hasattr(row[4], 'isoformat') else str(row[4]),
            'status': row[5],
            'is_bot_response': bool(row[6])
        })
    return messages

def update_message_status(message_id: str, status: MessageStatus):
    if cursor is None:
        print("Database connection not available")
        return
        
    cursor.execute('UPDATE messages SET status = %s WHERE message_id = %s', (status.value, message_id))
    conn.commit()

def create_user(email: str):
    if cursor is None:
        print("Database connection not available")
        return
        
    cursor.execute('INSERT IGNORE INTO users (email, created_at) VALUES (%s, %s)',
                   (email, datetime.utcnow()))
    conn.commit()

def get_user(email: str):
    if cursor is None:
        print("Database connection not available")
        return None
        
    cursor.execute('SELECT email, created_at FROM users WHERE email = %s', (email,))
    row = cursor.fetchone()
    if row:
        return {'email': row[0], 'created_at': row[1].isoformat() if hasattr(row[1], 'isoformat') else str(row[1])}
    return None
