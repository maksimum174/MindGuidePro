"""Скрипт для проверки доступных моделей Gemini."""

import os
import sys
import logging
from google import generativeai as genai

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def list_models():
    """Вывести список доступных моделей Gemini."""
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        logger.error("GEMINI_API_KEY не найден в переменных окружения")
        return
    
    try:
        # Конфигурация API Gemini
        genai.configure(api_key=api_key)
        
        # Получение списка моделей
        models = genai.list_models()
        
        logger.info("Доступные модели:")
        for model in models:
            logger.info(f"- {model.name}")
            logger.info(f"  Поддерживаемые генерации: {model.supported_generation_methods}")
            logger.info("---")
            
    except Exception as e:
        logger.error(f"Ошибка при получении списка моделей: {e}")

if __name__ == "__main__":
    list_models()