# WhatsEase Chat Application

A real-time chat application with AI bot integration, built with FastAPI backend, MySQL database, and Streamlit frontend.

## 🚀 Features

- **Real-time messaging** with WebSocket support
- **AI chatbot integration** using Groq API
- **User authentication** with JWT tokens
- **MySQL database** for message storage
- **Responsive Streamlit UI**
- **Message status tracking** (Sent, Delivered, Read)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Streamlit UI   │◄──►│   FastAPI       │◄──►│    MySQL        │
│   (Frontend)    │    │   Backend       │    │   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Groq API      │
                       │   (AI Chatbot)  │
                       └─────────────────┘
```

## 📋 Project Structure

```
whats-ease-groq/
├── app.py              # Streamlit frontend application
├── main.py             # FastAPI backend server
├── requirements.txt    # Python dependencies
├── .env               # Environment configuration
├── backend/           # Backend modules
│   ├── auth.py        # Authentication utilities
│   ├── bot_groq.py    # AI chatbot integration
│   └── models.py      # Database models & operations
└── frontend/          # Frontend assets
    ├── public/
    │   └── index.html # Main HTML file
    └── src/
        ├── App.css    # Styles
        ├── App.js     # Main React component
        ├── index.css  # Global styles
        └── index.js   # React entry point
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance async web framework
- **MySQL** - Relational database for data persistence
- **JWT** - JSON Web Tokens for authentication
- **WebSockets** - Real-time bidirectional communication
- **SQLAlchemy** - Database ORM (planned for future)

### Frontend
- **Streamlit** - Python web app framework for UI
- **HTML/CSS/JavaScript** - Core web technologies

### AI Integration
- **Groq API** - Fast AI inference for chatbot responses

## 🚀 Quick Start

### Prerequisites

1. **Python 3.9+** installed
2. **MySQL Server** installed and running
3. **Git** (optional, for version control)

### 1. Clone and Setup

```bash
# Navigate to project directory
cd whatease-chat

# Install Python dependencies
pip install -r requirements.txt
```

### 2. MySQL Database Setup

```bash
# Start MySQL service
sudo systemctl start mysql  # Linux/Mac
# OR
net start mysql             # Windows

# Create database
mysql -u root -p
CREATE DATABASE chatapp;
EXIT;
```

### 3. Environment Configuration

Update `.env` file with your settings:

```env
# MySQL Database Configuration
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=chatapp
MYSQL_PORT=3306

# Groq API Configuration (Optional)
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Start Backend Server

```bash
# Terminal 1 - Start FastAPI backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Start Frontend Application

```bash
# Terminal 2 - Start Streamlit frontend
streamlit run app.py
```

### 6. Access Application

- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MYSQL_HOST` | MySQL server hostname | `localhost` |
| `MYSQL_USER` | MySQL username | `root` |
| `MYSQL_PASSWORD` | MySQL password | `` |
| `MYSQL_DATABASE` | Database name | `chatapp` |
| `MYSQL_PORT` | MySQL port | `3306` |
| `GROQ_API_KEY` | Groq API key for AI chatbot | `your_key` |

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API status |
| `GET` | `/health` | Health check |
| `POST` | `/login` | User login |
| `POST` | `/register` | User registration |
| `GET` | `/me` | Get current user |
| `POST` | `/messages` | Send message |
| `GET` | `/messages/{recipient}` | Get conversation |
| `WebSocket` | `/ws/{user_email}` | Real-time messaging |

## 🧪 Testing

### Test Backend API

```bash
# Test login endpoint
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password"}'

# Test health check
curl http://localhost:8000/health
```

### Test Database Connection

```python
# test_db.py
import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',
        database='chatapp'
    )
    print("✅ MySQL connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

## 🔒 Security Features

- **JWT Authentication** - Secure token-based auth
- **Password Hashing** - Bcrypt for password security
- **Input Validation** - Pydantic models for data validation
- **CORS Support** - Cross-origin resource sharing

## 🤖 AI Chatbot Integration

The application includes an AI chatbot powered by Groq API:

1. Set your Groq API key in `.env`
2. Chat with the bot in the interface
3. Responses are generated using Llama models

## 📝 Recent Changes

### v2.0.0 - MySQL Migration
- ✅ **Migrated from SQLite to MySQL** for better scalability
- ✅ **Cleaned project structure** - removed unnecessary files
- ✅ **Updated dependencies** - added MySQL connector
- ✅ **Improved error handling** - better database connection management

### v1.0.0 - Initial Release
- ✅ Basic chat functionality with SQLite
- ✅ FastAPI backend with authentication
- ✅ Streamlit frontend UI
- ✅ WebSocket real-time messaging

## 🚨 Troubleshooting

### Common Issues

**1. Port 8000 Already in Use**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <PID> /F
```

**2. MySQL Connection Failed**
```bash
# Check MySQL service status
sudo systemctl status mysql

# Restart MySQL service
sudo systemctl restart mysql
```

**3. Module Not Found Errors**
```bash
# Reinstall dependencies
pip uninstall -y -r requirements.txt
pip install -r requirements.txt
```

**4. Frontend Connection Issues**
- Ensure backend server is running on port 8000
- Check that `BASE_URL` in `app.py` points to correct backend
- Verify network connectivity

## 📚 API Documentation

Once the backend server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review existing issues on GitHub
3. Create a new issue with detailed information

---

**Made with ❤️ for seamless communication**
