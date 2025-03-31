import os
import logging
from bot import create_bot, start_bot

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == "__main__":
    # Create and start the bot
    bot = create_bot()
    start_bot(bot)
