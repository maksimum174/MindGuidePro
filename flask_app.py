from flask import Flask
import threading
import subprocess
import os
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"flask_app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Глобальная переменная для отслеживания статуса бота
bot_process = None
bot_status = "Не запущен"
last_restart = None

# Запуск бота в отдельном процессе
def run_bot():
    global bot_process, bot_status, last_restart
    try:
        logger.info("Запуск бота...")
        # Запускаем бота как отдельный процесс
        bot_process = subprocess.Popen(["python", "main.py"], 
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        bot_status = "Работает"
        last_restart = datetime.now()
        logger.info(f"Бот запущен с PID {bot_process.pid}")
        return True
    except Exception as e:
        bot_status = f"Ошибка запуска: {str(e)}"
        logger.error(f"Ошибка при запуске бота: {str(e)}")
        return False

# Остановка бота
def stop_bot():
    global bot_process, bot_status
    if bot_process:
        logger.info(f"Остановка бота с PID {bot_process.pid}...")
        bot_process.terminate()
        bot_process.wait()
        bot_status = "Остановлен"
        logger.info("Бот остановлен")
        return True
    return False

# Перезапуск бота
def restart_bot():
    stop_bot()
    return run_bot()

# Запускаем бот при старте приложения
@app.before_first_request
def initialize_bot():
    run_bot()

@app.route('/')
def home():
    global bot_status, last_restart
    uptime = ""
    if last_restart:
        uptime = f" (работает с {last_restart.strftime('%Y-%m-%d %H:%M:%S')})"
    return f"""
    <html>
        <head>
            <title>Психологический бот - Статус</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                h1 {{ color: #333; }}
                .status {{ padding: 20px; background-color: #f4f4f4; border-radius: 5px; }}
                .controls {{ margin-top: 20px; }}
                .controls a {{ display: inline-block; margin-right: 10px; padding: 10px 15px;
                            background-color: #4CAF50; color: white; text-decoration: none; 
                            border-radius: 4px; }}
                .controls a:hover {{ background-color: #45a049; }}
                .controls a.stop {{ background-color: #f44336; }}
                .controls a.stop:hover {{ background-color: #d32f2f; }}
            </style>
        </head>
        <body>
            <h1>Психологический бот - Панель управления</h1>
            <div class="status">
                <h2>Текущий статус: {bot_status}{uptime}</h2>
                <p>Бот доступен в Telegram для взаимодействия.</p>
            </div>
            <div class="controls">
                <a href="/restart">Перезапустить бота</a>
                <a href="/start">Запустить бота</a>
                <a href="/stop" class="stop">Остановить бота</a>
            </div>
        </body>
    </html>
    """

@app.route('/ping')
def ping():
    # Эндпоинт для проверки активности приложения внешними сервисами
    return "pong"

@app.route('/restart')
def restart():
    if restart_bot():
        return """
        <html>
            <head>
                <meta http-equiv="refresh" content="3;url=/" />
                <title>Перезапуск бота</title>
                <style>body { font-family: Arial; margin: 40px; }</style>
            </head>
            <body>
                <h1>Бот перезапущен!</h1>
                <p>Перенаправление на главную страницу через 3 секунды...</p>
            </body>
        </html>
        """
    else:
        return """
        <html>
            <head>
                <meta http-equiv="refresh" content="3;url=/" />
                <title>Ошибка</title>
                <style>body { font-family: Arial; margin: 40px; }</style>
            </head>
            <body>
                <h1>Ошибка при перезапуске бота</h1>
                <p>Перенаправление на главную страницу через 3 секунды...</p>
            </body>
        </html>
        """

@app.route('/start')
def start():
    if bot_status == "Работает":
        return """
        <html>
            <head>
                <meta http-equiv="refresh" content="3;url=/" />
                <title>Бот уже запущен</title>
                <style>body { font-family: Arial; margin: 40px; }</style>
            </head>
            <body>
                <h1>Бот уже запущен!</h1>
                <p>Перенаправление на главную страницу через 3 секунды...</p>
            </body>
        </html>
        """
    else:
        if run_bot():
            return """
            <html>
                <head>
                    <meta http-equiv="refresh" content="3;url=/" />
                    <title>Запуск бота</title>
                    <style>body { font-family: Arial; margin: 40px; }</style>
                </head>
                <body>
                    <h1>Бот запущен!</h1>
                    <p>Перенаправление на главную страницу через 3 секунды...</p>
                </body>
            </html>
            """
        else:
            return """
            <html>
                <head>
                    <meta http-equiv="refresh" content="3;url=/" />
                    <title>Ошибка</title>
                    <style>body { font-family: Arial; margin: 40px; }</style>
                </head>
                <body>
                    <h1>Ошибка при запуске бота</h1>
                    <p>Перенаправление на главную страницу через 3 секунды...</p>
                </body>
            </html>
            """

@app.route('/stop')
def stop():
    if stop_bot():
        return """
        <html>
            <head>
                <meta http-equiv="refresh" content="3;url=/" />
                <title>Остановка бота</title>
                <style>body { font-family: Arial; margin: 40px; }</style>
            </head>
            <body>
                <h1>Бот остановлен!</h1>
                <p>Перенаправление на главную страницу через 3 секунды...</p>
            </body>
        </html>
        """
    else:
        return """
        <html>
            <head>
                <meta http-equiv="refresh" content="3;url=/" />
                <title>Ошибка</title>
                <style>body { font-family: Arial; margin: 40px; }</style>
            </head>
            <body>
                <h1>Ошибка при остановке бота или бот не был запущен</h1>
                <p>Перенаправление на главную страницу через 3 секунды...</p>
            </body>
        </html>
        """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)