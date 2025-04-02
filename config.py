"""Конфигурационный файл для бота."""

import os
import logging
import sys

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Проверяем доступность dotenv и загрузка переменных окружения из файла .env
try:
    from dotenv import load_dotenv
    # Пробуем загрузить переменные из .env файла
    result = load_dotenv()
    if result:
        logger.info("Переменные окружения загружены из .env файла")
    else:
        logger.warning("Файл .env не найден или пуст")
except ImportError:
    logger.warning("Модуль python-dotenv не установлен. Используем только системные переменные окружения.")
except Exception as e:
    logger.error(f"Ошибка при загрузке переменных окружения: {str(e)}")

# Токен Telegram бота
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN не найден в переменных окружения!")

# API ключ Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY не найден в переменных окружения!")

# Настройки логирования
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Настройки Gemini
GEMINI_MODEL = "models/gemini-1.5-pro"  # Используем доступную модель
TEMPERATURE = 0.75  # Немного повышаем креативность для НЛП-подхода
TOP_P = 0.92  # Более высокая вероятностная отсечка для гештальт-терапевтического стиля
TOP_K = 30  # Добавляем параметр для разнообразия техник
MAX_OUTPUT_TOKENS = 800  # Ограничиваем длину ответа для краткости

# Тексты команд бота
WELCOME_MESSAGE = """Здравствуйте! 👋

Я ваш персональный психотерапевт с многолетним опытом в различных терапевтических подходах. Я подберу наиболее эффективные методы, отвечающие именно вашим потребностям. В моем арсенале гештальт-терапия, когнитивно-поведенческий подход, схема-терапия, НЛП и другие направления современной психотерапии.

Что привело вас сегодня к диалогу?
"""

HELP_MESSAGE = """Я универсальный психотерапевт, который самостоятельно выбирает наиболее эффективные подходы и техники в работе с вашим запросом. Моя цель – создать безопасное пространство для вашего личностного роста и трансформации.

Команды:
/start - Начать новую сессию
/help - Показать это сообщение
/reset - Завершить текущую работу и начать новую

Что вы хотели бы исследовать в нашей работе?
"""

RESET_MESSAGE = """Мы завершили предыдущую работу и готовы начать новую. Важно полностью присутствовать в текущем моменте и быть открытым новому опыту.

С чем вы хотели бы поработать сейчас?"""

ERROR_MESSAGE = """Я заметил небольшое затруднение в нашем диалоге. Такие моменты часто открывают возможности для нового понимания.

Пожалуйста, попробуйте переформулировать ваш запрос или используйте команду /reset для начала новой сессии."""