import os
import subprocess
import time
import threading
import signal
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "psihelpbot_secret_key")

# Переменная для хранения процесса бота
bot_process = None
bot_status = {
    "running": False,
    "start_time": None,
    "uptime": "Не запущен"
}

def update_uptime():
    """Обновляет информацию об uptime бота"""
    while bot_status["running"]:
        if bot_status["start_time"]:
            elapsed = time.time() - bot_status["start_time"]
            hours, remainder = divmod(int(elapsed), 3600)
            minutes, seconds = divmod(remainder, 60)
            bot_status["uptime"] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        time.sleep(1)

def start_bot():
    """Запускает процесс телеграм-бота"""
    global bot_process
    global bot_status
    
    if bot_process is not None:
        return False
        
    try:
        # Запуск бота с перенаправлением вывода в файл
        log_file = open("bot.log", "a")
        bot_process = subprocess.Popen(
            ["python", "main.py"], 
            stdout=log_file,
            stderr=log_file,
            preexec_fn=os.setsid
        )
        
        # Обновление статуса
        bot_status["running"] = True
        bot_status["start_time"] = time.time()
        
        # Запуск обновления времени работы
        threading.Thread(target=update_uptime, daemon=True).start()
        
        return True
    except Exception as e:
        print(f"Ошибка запуска бота: {e}")
        return False

def stop_bot():
    """Останавливает процесс телеграм-бота"""
    global bot_process
    global bot_status
    
    if bot_process is None:
        return False
        
    try:
        # Отправляем сигнал завершения группе процессов
        os.killpg(os.getpgid(bot_process.pid), signal.SIGTERM)
        bot_process.wait(timeout=5)  # Ожидаем завершения процесса
        bot_process = None
        
        # Обновление статуса
        bot_status["running"] = False
        bot_status["uptime"] = "Не запущен"
        
        return True
    except Exception as e:
        print(f"Ошибка остановки бота: {e}")
        return False

def restart_bot():
    """Перезапускает процесс телеграм-бота"""
    if stop_bot():
        time.sleep(2)  # Даем время на корректное завершение
        return start_bot()
    return False

def check_bot_running():
    """Проверяет, запущен ли бот"""
    global bot_process
    
    if bot_process is None:
        return False
        
    # Проверяем, работает ли процесс
    if bot_process.poll() is not None:
        # Процесс завершился
        bot_process = None
        bot_status["running"] = False
        bot_status["uptime"] = "Не запущен"
        return False
        
    return True

@app.route('/', methods=['GET'])
def home():
    """Главная страница панели управления"""
    # Проверяем статус бота
    is_running = check_bot_running()
    
    return f"""
    <html>
        <head>
            <title>Психологический бот - Панель управления</title>
            <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <script>
                // Функция для обновления статуса бота каждые 5 секунд
                function updateStatus() {{
                    fetch('/status')
                        .then(response => response.json())
                        .then(data => {{
                            const statusElement = document.getElementById('bot-status');
                            const uptimeElement = document.getElementById('bot-uptime');
                            
                            if (data.running) {{
                                statusElement.innerHTML = '<span class="badge bg-success">Активен</span>';
                                uptimeElement.textContent = data.uptime;
                            }} else {{
                                statusElement.innerHTML = '<span class="badge bg-danger">Не активен</span>';
                                uptimeElement.textContent = 'Не запущен';
                            }}
                        }});
                }}
                
                // Запускаем обновление статуса каждые 5 секунд
                setInterval(updateStatus, 5000);
                
                // Обновляем статус при загрузке страницы
                document.addEventListener('DOMContentLoaded', updateStatus);
            </script>
        </head>
        <body data-bs-theme="dark">
            <div class="container mt-5">
                <div class="row">
                    <div class="col-12">
                        <div class="card">
                            <div class="card-header">
                                <h1 class="card-title">Психологический бот - Панель управления</h1>
                            </div>
                            <div class="card-body">
                                <div class="card mb-4">
                                    <div class="card-header">
                                        <h3>Статус бота</h3>
                                    </div>
                                    <div class="card-body">
                                        <div class="row align-items-center">
                                            <div class="col-md-4">
                                                <p><strong>Состояние:</strong> <span id="bot-status">
                                                    {'<span class="badge bg-success">Активен</span>' if is_running else '<span class="badge bg-danger">Не активен</span>'}
                                                </span></p>
                                                <p><strong>Время работы:</strong> <span id="bot-uptime">{bot_status['uptime']}</span></p>
                                            </div>
                                            <div class="col-md-8">
                                                <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                                                    <a href="/start" class="btn btn-success me-md-2 {'disabled' if is_running else ''}">
                                                        <i class="bi bi-play-fill"></i> Запустить
                                                    </a>
                                                    <a href="/stop" class="btn btn-danger me-md-2 {'disabled' if not is_running else ''}">
                                                        <i class="bi bi-stop-fill"></i> Остановить
                                                    </a>
                                                    <a href="/restart" class="btn btn-warning {'disabled' if not is_running else ''}">
                                                        <i class="bi bi-arrow-clockwise"></i> Перезапустить
                                                    </a>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <h2>Как использовать бота</h2>
                                <p>Найдите бота в Telegram по имени <code>@psi_help24_bot</code> и отправьте команду <code>/start</code>.</p>
                                
                                <h2>Команды бота:</h2>
                                <ul class="list-group mb-4">
                                    <li class="list-group-item d-flex justify-content-between align-items-center">
                                        /start
                                        <span class="badge bg-primary rounded-pill">Начать диалог</span>
                                    </li>
                                    <li class="list-group-item d-flex justify-content-between align-items-center">
                                        /help
                                        <span class="badge bg-primary rounded-pill">Получить помощь</span>
                                    </li>
                                    <li class="list-group-item d-flex justify-content-between align-items-center">
                                        /reset
                                        <span class="badge bg-primary rounded-pill">Сбросить контекст</span>
                                    </li>
                                </ul>
                                
                                <div class="card mb-4">
                                    <div class="card-header">
                                        <h3>Информация о боте</h3>
                                    </div>
                                    <div class="card-body">
                                        <p>Бот психологической поддержки, разработанный с использованием Gemini AI и специализированный для русскоязычной аудитории.</p>
                                        <p>Проект предоставляет персонализированную психологическую помощь через современные коммуникационные технологии.</p>
                                    </div>
                                </div>
                            </div>
                            <div class="card-footer text-muted">
                                &copy; 2025 Психологический бот на базе Gemini AI
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """

@app.route('/status', methods=['GET'])
def status():
    """Возвращает текущий статус бота в формате JSON"""
    is_running = check_bot_running()
    return jsonify({
        "running": is_running,
        "uptime": bot_status["uptime"] if is_running else "Не запущен"
    })

@app.route('/start', methods=['GET'])
def start():
    """Запускает бота"""
    if not check_bot_running():
        if start_bot():
            flash("Бот успешно запущен", "success")
        else:
            flash("Ошибка при запуске бота", "danger")
    else:
        flash("Бот уже запущен", "warning")
    return redirect(url_for('home'))

@app.route('/stop', methods=['GET'])
def stop():
    """Останавливает бота"""
    if check_bot_running():
        if stop_bot():
            flash("Бот успешно остановлен", "success")
        else:
            flash("Ошибка при остановке бота", "danger")
    else:
        flash("Бот не запущен", "warning")
    return redirect(url_for('home'))

@app.route('/restart', methods=['GET'])
def restart():
    """Перезапускает бота"""
    if check_bot_running():
        if restart_bot():
            flash("Бот успешно перезапущен", "success")
        else:
            flash("Ошибка при перезапуске бота", "danger")
    else:
        flash("Бот не запущен, запускаем...", "warning")
        start_bot()
    return redirect(url_for('home'))

@app.route('/ping', methods=['GET'])
def ping():
    """Проверка работоспособности сервера"""
    return "pong"

# Автоматический запуск бота при запуске сервера
def initialize_bot():
    """Инициализирует бота при первом запросе к серверу"""
    if not check_bot_running():
        start_bot()

# Регистрируем функцию, которая будет вызываться при первом запросе
@app.route('/initialize', methods=['GET'])
def handle_initialize():
    """Эндпоинт для инициализации бота"""
    initialize_bot()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)