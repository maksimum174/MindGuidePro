"""Модуль для работы с API Gemini."""

import os
import logging
import time
from google import generativeai as genai

from prompts import SYSTEM_PROMPT
from config import GEMINI_API_KEY, GEMINI_MODEL, TEMPERATURE, TOP_P, TOP_K, MAX_OUTPUT_TOKENS

# Настройка логирования
logger = logging.getLogger(__name__)

def configure_gemini():
    """Настройка клиента Gemini."""
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY не найден в переменных окружения")
        raise ValueError("GEMINI_API_KEY не найден")
    
    # Конфигурация API Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini API настроен успешно")


def create_chat_session():
    """Создание новой сессии чата с системным промптом."""
    try:
        # Убеждаемся, что API настроен
        configure_gemini()
        
        # Получаем модель
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config={
                "temperature": TEMPERATURE,
                "top_p": TOP_P,
                "top_k": TOP_K,
                "max_output_tokens": MAX_OUTPUT_TOKENS,
            }
        )
        
        # Создание сессии чата с системным промптом
        initial_chat_history = [
            {
                "role": "user",
                "parts": [{"text": "Пожалуйста, действуй согласно следующей инструкции для всех наших последующих взаимодействий."}]
            },
            {
                "role": "model",
                "parts": [{"text": "Я готов действовать согласно вашей инструкции. Пожалуйста, поделитесь ею."}]
            },
            {
                "role": "user",
                "parts": [{"text": SYSTEM_PROMPT}]
            },
            {
                "role": "model",
                "parts": [{"text": "Я понял вашу инструкцию и буду следовать ей в наших взаимодействиях. Я - психолог-консультант для русскоязычных пользователей, специализирующийся на поддержке в сложных жизненных ситуациях.\n\nЯ буду руководствоваться научно обоснованными методами, такими как КПТ, ACT и другими, проявлять эмпатию и этичность в работе. Я буду учитывать культурный контекст русскоязычного общества и использовать техники активного слушания.\n\nВ своей работе я буду помогать с такими темами как тревожность, стресс, отношения, самооценка, профессиональное развитие и адаптация к изменениям. При этом я не буду ставить диагнозы, назначать лекарства или выходить за рамки психологического консультирования.\n\nМоя главная цель - создать безопасное пространство, где вы сможете разобраться в своей ситуации и найти ресурсы для её улучшения. Чем я могу вам помочь сегодня?"}]
            }
        ]
        
        # Создаем чат-сессию с начальной историей
        chat = model.start_chat(history=initial_chat_history)
        
        return chat
    except Exception as e:
        logger.error(f"Ошибка при создании чат-сессии Gemini: {e}")
        raise


def get_gemini_response(chat, message):
    """Получение ответа от модели Gemini."""
    try:
        start_time = time.time()
        logger.info(f"Отправка запроса в Gemini: {message[:100]}...")
        
        # Отправляем сообщение как словарь с текстом
        response = chat.send_message({"text": message})
        
        # Преобразуем ответ в текст
        response_text = response.text
        
        process_time = time.time() - start_time
        logger.info(f"Ответ получен за {process_time:.2f} секунд")
        
        return response_text
    except Exception as e:
        logger.error(f"Ошибка при получении ответа от Gemini: {e}")
        raise


def get_initial_chat():
    """Создание и возврат начальной сессии чата."""
    return create_chat_session()