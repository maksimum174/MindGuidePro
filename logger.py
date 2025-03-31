"""Модуль для логирования взаимодействий с ботом."""

import os
import logging
import json
from datetime import datetime

# Получаем логгер
logger = logging.getLogger(__name__)

# Директория для логов
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")

# Создаем директорию, если она не существует
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
    # Текущая дата и время для имени файла
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Создаем запись лога
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": user_id,
        "type": interaction_type,
        "user_message": user_message,
        "bot_response": bot_response
    }
    
    # Имя файла лога
    log_file = os.path.join(LOG_DIR, f"interaction_{user_id}_{timestamp}.json")
    
    try:
        # Записываем лог в файл
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(log_entry, f, ensure_ascii=False, indent=4)
        
        # Также выводим в консоль для отладки
        logger.info(f"Логирование взаимодействия с пользователем {user_id} успешно.")
        
    except Exception as e:
        logger.error(f"Ошибка при логировании: {e}")