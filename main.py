from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from backend.models import Message, User, MessageStatus, create_message, get_conversation, update_message_status, create_user, get_user
from backend.auth import create_access_token, verify_token, hash_password, verify_password
from backend.bot_groq import generate_bot_reply
import json
import logging
from datetime import datetime

app = FastAPI()

# Mount static files for React build
app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage for active connections (for WebSocket)
active_connections = {}

# User registration
@app.post("/register")
async def register(user: dict):
    email = user.get("email")
    password = user.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    existing_user = get_user(email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = hash_password(password)
    create_user(email)  # For simplicity, store email only; in production, store hashed password
    return {"message": "User registered successfully"}

# User login
@app.post("/login")
async def login(user: dict):
    email = user.get("email")
    password = user.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    # For simplicity, assume password verification; in production, check hashed password
    access_token = create_access_token(data={"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}

# Get current user
@app.get("/me")
async def get_me(current_user: str = Depends(verify_token)):
    return {"email": current_user}

# Send message (RESTful)
@app.post("/messages")
async def send_message(message: dict, current_user: str = Depends(verify_token)):
    msg = Message(
        message_id=message.get("message_id"),
        sender=current_user,
        recipient=message.get("recipient"),
        content=message.get("content"),
        timestamp=datetime.utcnow(),
        status=MessageStatus.SENT,
        is_bot_response=message.get("is_bot_response", False)
    )
    create_message(msg)
    logger.info(f"Message sent from {current_user} to {msg.recipient}")
    return {"message": "Message sent"}

# Get conversation (RESTful)
@app.get("/messages/{recipient}")
async def get_messages(recipient: str, current_user: str = Depends(verify_token)):
    messages = get_conversation(current_user, recipient)
    return {"messages": messages}

# Update message status
@app.put("/messages/{message_id}/status")
async def update_status(message_id: str, status: str, current_user: str = Depends(verify_token)):
    update_message_status(message_id, MessageStatus(status))
    return {"message": "Status updated"}

# WebSocket for real-time messaging
@app.websocket("/ws/{user_email}")
async def websocket_endpoint(websocket: WebSocket, user_email: str):
    await websocket.accept()
    active_connections[user_email] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            # Handle message sending
            if message_data.get("type") == "send_message":
                recipient = message_data.get("recipient")
                content = message_data.get("content")
                msg = Message(
                    message_id=f"{user_email}_{datetime.utcnow().isoformat()}",
                    sender=user_email,
                    recipient=recipient,
                    content=content,
                    timestamp=datetime.utcnow(),
                    status=MessageStatus.SENT,
                    is_bot_response=False
                )
                create_message(msg)
                # Send to recipient if online
                if recipient in active_connections:
                    await active_connections[recipient].send_text(json.dumps({
                        "type": "new_message",
                        "message": msg.dict()
                    }))
                # Send back to sender
                await websocket.send_text(json.dumps({
                    "type": "new_message",
                    "message": msg.dict()
                }))
                logger.info(f"Message sent from {user_email} to {recipient}")
            elif message_data.get("type") == "bot_message":
                content = message_data.get("content")
                bot_reply = generate_bot_reply(user_email, content)
                bot_msg = Message(
                    message_id=f"bot_{datetime.utcnow().isoformat()}",
                    sender="whatease@bot.local",
                    recipient=user_email,
                    content=bot_reply,
                    timestamp=datetime.utcnow(),
                    status=MessageStatus.SENT,
                    is_bot_response=True
                )
                create_message(bot_msg)
                await websocket.send_text(json.dumps({
                    "type": "bot_reply",
                    "message": bot_msg.dict()
                }))
                logger.info(f"Bot replied to {user_email}")
    except WebSocketDisconnect:
        if user_email in active_connections:
            del active_connections[user_email]

# Serve React frontend
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("frontend/build/index.html", "r") as f:
        return f.read()

# Health check
@app.get("/health")
async def health_check():
    return {"status": "OK"}
