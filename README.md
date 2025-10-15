# WhatsEase Chat Application

## Overview
WhatsEase is a WhatsApp-like chat application with multiple frontend options:

**Backend**: FastAPI server with WebSocket support for real-time messaging
**Frontend Options**:
- **Streamlit** (Primary): Clean chat UI with real-time messaging
- **React** (Production): Modern web interface

**Features**:
- Real-time chat with AI bot (powered by Groq)
- User authentication with JWT tokens
- SQLite database for message storage
- Context-aware AI responses

## Architecture
- **Backend**: FastAPI + WebSockets + SQLite
- **Frontend**: Streamlit (Python) + React (JavaScript)
- **AI**: Groq API for intelligent bot responses

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Backend Server
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Start Frontend (Choose one)

**Option A: Streamlit Frontend**
```bash
streamlit run app.py
```
Access at: http://localhost:8501

**Option B: React Frontend**
```bash
cd frontend
npm install
npm start
```
Access at: http://localhost:3000

## Environment Variables
Create a `.env` file with:
```
GROQ_API_KEY=your_groq_api_key_here
```

## API Endpoints
- `POST /login` - User authentication
- `POST /register` - User registration
- `GET /me` - Get current user
- `POST /messages` - Send message
- `GET /messages/{recipient}` - Get conversation
- `WebSocket /ws/{user_email}` - Real-time messaging
