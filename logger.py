import os
import json
import logging
from datetime import datetime
from utils import sanitize_text

# Configure logging
logger = logging.getLogger(__name__)

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def log_interaction(user_id, interaction_type, user_message, bot_response):
    """
    Log user interactions with the bot.
    
    Args:
        user_id: The user's Telegram ID
        interaction_type: The type of interaction (start, message, help, reset)
        user_message: The message from the user
        bot_response: The bot's response
    """
    try:
        # Sanitize input
        user_message = sanitize_text(user_message)
        bot_response = sanitize_text(bot_response)
        
        # Create log entry
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": user_id,
            "interaction_type": interaction_type,
            "user_message": user_message,
            "bot_response": bot_response
        }
        
        # Create log filename with date
        log_date = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(LOG_DIR, f"interactions_{log_date}.log")
        
        # Append to log file
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
            
    except Exception as e:
        logger.error(f"Error logging interaction: {e}")
