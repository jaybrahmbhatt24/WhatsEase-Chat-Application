import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

user_context = {}  # last 10 messages per user

def add_context(user_email: str, message: str):
    lst = user_context.setdefault(user_email, [])
    lst.append(message)
    if len(lst) > 10:
        lst.pop(0)

def get_context(user_email: str):
    return user_context.get(user_email, [])

def generate_bot_reply(user_email: str, message: str):
    add_context(user_email, message)
    context = get_context(user_email)
    
    # Groq payload - using OpenAI compatible format
    if context:
        context_str = "\n".join([f"User: {msg}" if i % 2 == 0 else f"Bot: {msg}" for i, msg in enumerate(context)])
        full_prompt = f"{context_str}\nUser: {message}\nBot:"
    else:
        full_prompt = f"User: {message}\nBot:"

    payload = {
        "model": "llama-3.1-8b-instant",  # Using a currently supported Groq production model
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": full_prompt}
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        bot_reply = data.get("choices", [{}])[0].get("message", {}).get("content", "Sorry, I couldn't understand that.")
    except requests.exceptions.HTTPError as e:
        # Get the actual error message from the API response
        try:
            error_data = response.json()
            bot_reply = f"API Error: {error_data.get('error', {}).get('message', str(e))}"
        except:
            bot_reply = f"HTTP Error: {str(e)}"
    except requests.exceptions.RequestException as e:
        bot_reply = f"Request Error: {str(e)}"
    except Exception as e:
        bot_reply = f"Error: {str(e)}"
    
    add_context(user_email, bot_reply)
    return bot_reply
