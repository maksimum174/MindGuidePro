import os

# Telegram Bot Token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
if not TELEGRAM_TOKEN:
    raise ValueError("No TELEGRAM_TOKEN found in environment variables!")

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    raise ValueError("No GEMINI_API_KEY found in environment variables!")

# Gemini model to use
GEMINI_MODEL = "gemini-pro"

# Conversation timeout (in seconds)
CONVERSATION_TIMEOUT = 3600  # 1 hour

# Maximum messages to store in conversation history
MAX_HISTORY_LENGTH = 20
