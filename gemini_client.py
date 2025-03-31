import os
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL
from prompts import SYSTEM_PROMPT

# Configure the API
genai.configure(api_key=GEMINI_API_KEY)

# Set up the model
model = genai.GenerativeModel(GEMINI_MODEL)

def create_chat_session():
    """Create a new chat session with the system prompt."""
    chat = model.start_chat(history=[
        {
            "role": "user",
            "parts": ["Ты будешь выполнять роль психолога для русскоязычной аудитории. Пожалуйста, ответь на это сообщение как психолог, чтобы подтвердить, что ты готов."]
        },
        {
            "role": "model",
            "parts": [SYSTEM_PROMPT]
        }
    ])
    return chat

def get_gemini_response(chat, message):
    """Get a response from the Gemini model."""
    try:
        response = chat.send_message(message, stream=False)
        return response.text
    except Exception as e:
        print(f"Error getting response from Gemini: {e}")
        return "Извините, произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте еще раз позже."

def get_initial_chat():
    """Create and return an initial chat session."""
    return create_chat_session()
