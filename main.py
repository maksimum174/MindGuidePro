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
    """Обработчик команды /start - начало новой гештальт-сессии."""
    user_id = message.from_user.id
    username = message.from_user.username or "пользователь"
    first_name = message.from_user.first_name or "клиент"
    
    # Создаем новую сессию для пользователя
    user_sessions[user_id] = get_initial_chat()
    
    # Персонализированное приветственное сообщение
    personalized_welcome = WELCOME_MESSAGE.replace("Здравствуйте!", f"Здравствуйте, {first_name}!")
    
    # Отправляем приветственное сообщение без клавиатуры
    bot.send_message(message.chat.id, personalized_welcome)
    
    log_interaction(user_id, "start", f"/start от @{username}", personalized_welcome)


@bot.message_handler(commands=['help'])
def handle_help(message):
    """Обработчик команды /help - информация о гештальт-подходе и НЛП."""
    user_id = message.from_user.id
    username = message.from_user.username or "пользователь"
    
    # Отправляем сообщение без инлайн-клавиатуры
    bot.send_message(message.chat.id, HELP_MESSAGE)
    
    log_interaction(user_id, "help", f"/help от @{username}", HELP_MESSAGE)


@bot.message_handler(commands=['reset'])
def handle_reset(message):
    """Обработчик команды /reset - завершение текущей сессии и начало новой."""
    user_id = message.from_user.id
    username = message.from_user.username or "пользователь"
    
    # Создаем новую сессию
    user_sessions[user_id] = get_initial_chat()
    
    # Отправляем сообщение без клавиатуры
    bot.send_message(message.chat.id, RESET_MESSAGE)
    
    log_interaction(user_id, "reset", f"/reset от @{username}", RESET_MESSAGE)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    """Обработчик нажатий на инлайн-кнопки."""
    user_id = call.from_user.id
    username = call.from_user.username or "пользователь"
    
    # Информационные сообщения в зависимости от нажатой кнопки
    if call.data == "about_gestalt":
        response_text = """🔍 <b>О гештальт-терапии</b>

Гештальт-терапия — это психотерапевтический подход, фокусирующийся на <i>осознавании настоящего момента</i>. 

Основные принципы:
• Фокус на "здесь и сейчас"
• Осознавание телесных ощущений и эмоций
• Работа с незавершёнными ситуациями (гештальтами)
• Принятие ответственности за свой опыт
• Интеграция противоположностей

В нашей работе я буду помогать вам замечать то, что происходит в текущий момент, и находить новые способы контакта с собой и окружающими."""
        
        bot.send_message(call.message.chat.id, response_text, parse_mode="HTML")
        log_interaction(user_id, "callback", f"Запрос информации о гештальт-терапии от @{username}", response_text)
        
    elif call.data == "about_nlp":
        response_text = """🧠 <b>О нейро-лингвистическом программировании (НЛП)</b>

НЛП — это подход к коммуникации и личностному развитию, изучающий связь между мышлением, языком и поведением.

Ключевые элементы НЛП:
• Рефрейминг — изменение смысла ситуации
• Якорение — связывание ресурсных состояний с триггерами
• Работа с субмодальностями — изменение качеств внутренних образов
• Метамодель языка — прояснение искажений, обобщений и опущений
• Моделирование успешных стратегий

В нашей работе я буду использовать эти инструменты для трансформации ограничивающих убеждений и создания новых возможностей."""
        
        bot.send_message(call.message.chat.id, response_text, parse_mode="HTML")
        log_interaction(user_id, "callback", f"Запрос информации о НЛП от @{username}", response_text)
        
    elif call.data == "about_session":
        response_text = """🔄 <b>Как проходит сессия</b>

Наша сессия строится по принципу гештальт-цикла:

1. <b>Осознавание</b> — замечаем, что происходит внутри и вокруг
2. <b>Мобилизация</b> — определяем потребность и намерение
3. <b>Действие</b> — экспериментируем с новыми способами поведения
4. <b>Контакт</b> — взаимодействуем с проблемой по-новому
5. <b>Завершение</b> — интегрируем полученный опыт

В процессе я буду задавать вопросы, предлагать эксперименты и техники, помогающие увидеть ситуацию с разных сторон и найти новые решения.

Начните с описания вашей текущей ситуации и ощущений."""
        
        bot.send_message(call.message.chat.id, response_text, parse_mode="HTML")
        log_interaction(user_id, "callback", f"Запрос информации о сессии от @{username}", response_text)
    
    # Отмечаем запрос как обработанный
    bot.answer_callback_query(call.id)


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """Обработка всех текстовых сообщений от пользователя через гештальт-подход и НЛП."""
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
        # Преобразуем сообщение для лучшего понимания контекста гештальт-терапии
        enhanced_message = f"[Запрос клиента в рамках гештальт-сессии]: {user_message}"
        
        response = get_gemini_response(user_sessions[user_id], enhanced_message)
        
        # Убираем клавиатуру и отправляем чистый ответ
        bot.send_message(message.chat.id, response)
        log_interaction(user_id, "message", user_message, response)
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")
        bot.send_message(message.chat.id, ERROR_MESSAGE)
        log_interaction(user_id, "error", user_message, str(e))


def main():
    """Запуск бота."""
    import os
    logger.info(f"Бот запущен")
    logger.info(f"TELEGRAM_TOKEN доступен: {bool(os.environ.get('TELEGRAM_TOKEN'))}")
    logger.info(f"GEMINI_API_KEY доступен: {bool(os.environ.get('GEMINI_API_KEY'))}")
    
    try:
        # Проверка доступности API перед запуском
        try:
            me = bot.get_me()
            logger.info(f"Подключение к API Telegram успешно установлено. Имя бота: {me.first_name}, Username: @{me.username}")
        except telebot.apihelper.ApiException as api_error:
            # Специальная обработка ошибки конфликта (код 409)
            if "409" in str(api_error):
                logger.error("Обнаружен конфликт с другим экземпляром бота. Возможно, другой экземпляр уже запущен.")
                # Попытка принудительного сброса соединения
                try:
                    bot.remove_webhook()
                    logger.info("Webhook удален, пауза перед повторной попыткой...")
                    import time
                    time.sleep(10)  # Пауза перед повторной попыткой
                except Exception as e2:
                    logger.error(f"Ошибка при сбросе webhook: {e2}")
            else:
                logger.error(f"Ошибка API Telegram: {api_error}")
                return
        except Exception as e:
            logger.error(f"Неизвестная ошибка при подключении к API Telegram: {e}")
            return
        
        # Настройка и запуск с обновленными параметрами
        logger.info("Запуск в режиме infinity_polling")
        # Добавляем счетчик попыток
        retry_count = 0
        max_retries = 3
        
        while retry_count < max_retries:
            try:
                retry_count += 1
                logger.info(f"Попытка {retry_count}/{max_retries}")
                
                # Сброс настроек перед запуском
                bot.remove_webhook()
                
                bot.infinity_polling(timeout=30, 
                                    long_polling_timeout=10, 
                                    allowed_updates=["message", "callback_query", "chat_member"],
                                    skip_pending=True)
                break  # Если polling запустился успешно, выходим из цикла
            except telebot.apihelper.ApiException as api_error:
                logger.error(f"API ошибка при попытке {retry_count}: {api_error}")
                if retry_count < max_retries:
                    import time
                    time.sleep(5 * retry_count)  # Увеличивающаяся пауза между попытками
            except Exception as e:
                logger.error(f"Общая ошибка при попытке {retry_count}: {e}")
                if retry_count < max_retries:
                    import time
                    time.sleep(5)
    except Exception as e:
        logger.error(f"Критическая ошибка при работе бота: {e}")


if __name__ == "__main__":
    main()