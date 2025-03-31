"""Утилиты для работы с ботом."""

import re
import time
from datetime import datetime

def sanitize_text(text):
    """Remove any potentially harmful content from text."""
    if not text:
        return ""
    
    # Убираем потенциально опасные HTML-теги
    sanitized = re.sub(r'<(script|iframe|object|embed|form|style|meta|link)', 
                       r'&lt;\1', text, flags=re.IGNORECASE)
    
    return sanitized

def get_timestamp():
    """Get the current timestamp in a human-readable format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_time_elapsed(start_time):
    """Format the elapsed time since start_time."""
    elapsed = time.time() - start_time
    
    if elapsed < 60:
        return f"{int(elapsed)} секунд"
    elif elapsed < 3600:
        minutes = int(elapsed / 60)
        seconds = int(elapsed % 60)
        return f"{minutes} минут {seconds} секунд"
    else:
        hours = int(elapsed / 3600)
        minutes = int((elapsed % 3600) / 60)
        return f"{hours} часов {minutes} минут"