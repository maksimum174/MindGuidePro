import re
import time
from datetime import datetime

def sanitize_text(text):
    """Remove any potentially harmful content from text."""
    # Basic sanitization to prevent injection issues
    if text:
        # Remove any control characters
        text = re.sub(r'[\x00-\x1F\x7F]', '', text)
    return text

def get_timestamp():
    """Get the current timestamp in a human-readable format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_time_elapsed(start_time):
    """Format the elapsed time since start_time."""
    elapsed = time.time() - start_time
    
    if elapsed < 60:
        return f"{elapsed:.1f} секунд"
    elif elapsed < 3600:
        minutes = elapsed / 60
        return f"{minutes:.1f} минут"
    else:
        hours = elapsed / 3600
        return f"{hours:.1f} часов"
