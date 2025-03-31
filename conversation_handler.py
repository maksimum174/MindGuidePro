import logging
from telegram import Update, constants
from telegram.ext import ContextTypes
from gemini_client import get_gemini_response, get_initial_chat
from logger import log_interaction

# Enable logging
logger = logging.getLogger(__name__)

# Define the key for storing chat history in context.user_data
CHAT_SESSION_KEY = "chat_session"

def reset_conversation(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reset the conversation context."""
    if context.user_data and CHAT_SESSION_KEY in context.user_data:
        del context.user_data[CHAT_SESSION_KEY]

def get_chat_session(context: ContextTypes.DEFAULT_TYPE):
    """Get or create a chat session for the user."""
    if CHAT_SESSION_KEY not in context.user_data:
        context.user_data[CHAT_SESSION_KEY] = get_initial_chat()
    
    return context.user_data[CHAT_SESSION_KEY]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle user messages and generate responses using Gemini API."""
    user_message = update.message.text
    user_id = update.effective_user.id
    
    # Log user message
    logger.info(f"User {user_id} sent: {user_message}")
    
    # Get or create chat session
    chat_session = get_chat_session(context)
    
    # Show typing indicator
    await update.message.chat.send_chat_action(constants.ChatAction.TYPING)
    
    # Get response from Gemini
    response = get_gemini_response(chat_session, user_message)
    
    # Log the interaction
    log_interaction(user_id, "message", user_message, response)
    
    # Send the response to the user
    await update.message.reply_text(response)
    
    # Return the state
    return 0  # CHAT state
