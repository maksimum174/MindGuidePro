#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Телеграм-бот психологической поддержки на базе Gemini AI.
Оптимизирован для русскоязычного населения.
Реализован на библиотеке pyTelegramBotAPI.
"""

import os
import logging
import time
import telebot
from telebot import types

from config import TELEGRAM_TOKEN, WELCOME_MESSAGE, HELP_MESSAGE, RESET_MESSAGE, ERROR_MESSAGE
from gemini_client import get_initial_chat, get_gemini_response
from logger import log_interaction

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Проверка наличия токена
if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN не найден в переменных окружения")
    raise ValueError("TELEGRAM_TOKEN не найден")

# Создание экземпляра бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Словарь для хранения чат-сессий пользователей
user_sessions = {}


@bot.message_handler(commands=['start'])
def handle_start(message):
    """Обработчик команды /start."""
    user_id = message.from_user.id
    username = message.from_user.username or "пользователь"
    
    # Создаем новую сессию для пользователя
    user_sessions[user_id] = get_initial_chat()
    
    # Отправляем приветственное сообщение
    bot.send_message(message.chat.id, WELCOME_MESSAGE)
    
    log_interaction(user_id, "start", f"/start от @{username}", WELCOME_MESSAGE)


@bot.message_handler(commands=['help'])
def handle_help(message):
    """Обработчик команды /help."""
    user_id = message.from_user.id
    username = message.from_user.username or "пользователь"
    
    bot.send_message(message.chat.id, HELP_MESSAGE)
    
    log_interaction(user_id, "help", f"/help от @{username}", HELP_MESSAGE)


@bot.message_handler(commands=['reset'])
def handle_reset(message):
    """Обработчик команды /reset - сброс контекста разговора."""
    user_id = message.from_user.id
    username = message.from_user.username or "пользователь"
    
    # Создаем новую сессию
    user_sessions[user_id] = get_initial_chat()
    
    bot.send_message(message.chat.id, RESET_MESSAGE)
    
    log_interaction(user_id, "reset", f"/reset от @{username}", RESET_MESSAGE)


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """Обработка всех текстовых сообщений от пользователя."""
    user_id = message.from_user.id
    username = message.from_user.username or "пользователь"
    user_message = message.text
    
    logger.info(f"Сообщение от {username} (ID: {user_id}): {user_message}")
    
    # Если у пользователя нет активной сессии, создаем новую
    if user_id not in user_sessions or user_sessions[user_id] is None:
        user_sessions[user_id] = get_initial_chat()
    
    # Отправляем "typing..." статус
    bot.send_chat_action(message.chat.id, "typing")
    
    # Получаем ответ от Gemini
    try:
        response = get_gemini_response(user_sessions[user_id], user_message)
        bot.send_message(message.chat.id, response)
        log_interaction(user_id, "message", user_message, response)
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")
        bot.send_message(message.chat.id, ERROR_MESSAGE)
        log_interaction(user_id, "error", user_message, str(e))


def main():
    """Запуск бота."""
    logger.info("Бот запущен")
    try:
        # Бесконечный цикл для получения сообщений
        bot.infinity_polling()
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")


if __name__ == "__main__":
    main()