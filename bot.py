import os
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
    ConversationHandler,
)
from conversation_handler import handle_message, reset_conversation
from config import TELEGRAM_TOKEN
from logger import log_interaction

# Enable logging
logger = logging.getLogger(__name__)

# Define states
CHAT = 0

async def start(update: Update, context: CallbackContext) -> int:
    """Send a welcome message when the /start command is issued."""
    user = update.effective_user
    
    await update.message.reply_text(
        f"👋 Здравствуйте, {user.first_name}!\n\n"
        "Я ИИ-психолог, готовый выслушать Вас и помочь разобраться с Вашими вопросами и проблемами. "
        "Я работаю на базе технологии Gemini и обладаю знаниями в области психологии.\n\n"
        "Расскажите, что Вас беспокоит, или задайте вопрос, и я постараюсь помочь.\n\n"
        "📌 Команды:\n"
        "/start - начать беседу заново\n"
        "/help - получить справку\n"
        "/reset - сбросить историю разговора"
    )
    
    # Reset the conversation context
    reset_conversation(context)
    
    # Log the interaction
    log_interaction(user.id, "start", "", "Начало беседы")
    
    return CHAT

async def help_command(update: Update, context: CallbackContext) -> int:
    """Send a help message when the command /help is issued."""
    await update.message.reply_text(
        "🤝 Я здесь, чтобы помочь Вам:\n\n"
        "• Обсудить эмоциональные проблемы\n"
        "• Помочь разобраться в сложных ситуациях\n"
        "• Предложить психологические техники\n"
        "• Ответить на вопросы о психическом здоровье\n\n"
        "Просто напишите мне то, что Вас беспокоит, и я постараюсь помочь.\n\n"
        "📌 Команды:\n"
        "/start - начать беседу заново\n"
        "/help - получить эту справку\n"
        "/reset - сбросить историю разговора\n\n"
        "⚠️ Помните: я не являюсь заменой профессиональной психологической помощи. "
        "Если Вы в кризисной ситуации, обратитесь к квалифицированному специалисту."
    )
    
    # Log the interaction
    user = update.effective_user
    log_interaction(user.id, "help", "", "Запрос справки")
    
    return CHAT

async def reset_command(update: Update, context: CallbackContext) -> int:
    """Reset the conversation context."""
    reset_conversation(context)
    
    await update.message.reply_text(
        "🔄 История нашего разговора сброшена. Мы можем начать сначала.\n"
        "Расскажите, что Вас беспокоит сейчас?"
    )
    
    # Log the interaction
    user = update.effective_user
    log_interaction(user.id, "reset", "", "Сброс истории разговора")
    
    return CHAT

def create_bot() -> Application:
    """Create and configure the application."""
    # Create the Application using the bot token
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Create a ConversationHandler with the states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHAT: [
                CommandHandler("help", help_command),
                CommandHandler("reset", reset_command),
                CommandHandler("start", start),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add the ConversationHandler to the application
    application.add_handler(conv_handler)

    return application

def start_bot(application: Application) -> None:
    """Start the bot."""
    # Run the bot until the user presses Ctrl-C
    application.run_polling()
    logger.info("Bot started")
