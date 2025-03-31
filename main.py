import os
import logging
import asyncio
from bot import create_bot, start_bot

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

async def main():
    """Start the Telegram bot."""
    # Create and start the bot
    application = await create_bot()
    await start_bot(application)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user")
