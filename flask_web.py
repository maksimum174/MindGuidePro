"""
Веб-интерфейс для управления ботом.
"""

import os
import logging
import subprocess
import psutil
import time
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация приложения
app = Flask(__name__, 
            template_folder='web_interface/templates',
            static_folder='web_interface/static')

# Настройка секретного ключа для сессий
app.secret_key = os.environ.get("SESSION_SECRET", "temporary_session_secret")

# Настройка базы данных
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///bot_admin.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Инициализация базы данных
db = SQLAlchemy(app)

# Определение моделей
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Глобальные переменные для отслеживания состояния бота
bot_process = None
bot_start_time = None

def get_uptime():
    """Возвращает время работы бота в читаемом формате"""
    if bot_start_time is None:
        return "Бот не запущен"
    
    uptime = datetime.now() - bot_start_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if days > 0:
        return f"{days}д {hours}ч {minutes}м {seconds}с"
    elif hours > 0:
        return f"{hours}ч {minutes}м {seconds}с"
    elif minutes > 0:
        return f"{minutes}м {seconds}с"
    else:
        return f"{seconds}с"

def check_bot_running():
    """Проверяет, запущен ли процесс бота"""
    global bot_process
    
    if bot_process is None:
        return False
    
    try:
        # Проверяем, существует ли процесс с таким PID
        return psutil.pid_exists(bot_process.pid) and bot_process.poll() is None
    except:
        return False

def run_bot():
    """Запускает процесс бота"""
    global bot_process, bot_start_time
    
    if check_bot_running():
        logger.info("Бот уже запущен")
        return
    
    try:
        # Запускаем бот в отдельном процессе
        bot_process = subprocess.Popen(
            ["python", "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        bot_start_time = datetime.now()
        logger.info(f"Бот запущен, PID: {bot_process.pid}")
        return True
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        return False

def stop_bot():
    """Останавливает процесс бота"""
    global bot_process, bot_start_time
    
    if not check_bot_running():
        logger.info("Бот не запущен")
        return True
    
    try:
        # Пытаемся корректно завершить процесс
        process = psutil.Process(bot_process.pid)
        for child in process.children(recursive=True):
            child.terminate()
        process.terminate()
        
        # Даем процессу время на завершение
        time.sleep(2)
        
        # Если процесс все еще работает, принудительно завершаем
        if psutil.pid_exists(bot_process.pid):
            process.kill()
        
        bot_process = None
        bot_start_time = None
        logger.info("Бот остановлен")
        return True
    except Exception as e:
        logger.error(f"Ошибка при остановке бота: {e}")
        return False

def restart_bot():
    """Перезапускает процесс бота"""
    stop_result = stop_bot()
    time.sleep(2)  # Даем время на освобождение ресурсов
    start_result = run_bot()
    return stop_result and start_result

def get_logs(count=10):
    """Получает последние логи взаимодействий с ботом"""
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    logs = []
    
    if os.path.exists(logs_dir):
        # Получаем список файлов логов, сортируем по времени изменения
        log_files = sorted(
            [os.path.join(logs_dir, f) for f in os.listdir(logs_dir) if f.endswith('.json')],
            key=os.path.getmtime,
            reverse=True
        )
        
        # Читаем последние файлы логов
        for log_file in log_files[:count]:
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
                    logs.append(log_data)
            except Exception as e:
                logger.error(f"Ошибка при чтении лога {log_file}: {e}")
    
    return logs

def get_user_stats():
    """Получает статистику пользователей бота"""
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    user_stats = {}
    
    if os.path.exists(logs_dir):
        log_files = [os.path.join(logs_dir, f) for f in os.listdir(logs_dir) if f.endswith('.json')]
        
        for log_file in log_files:
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
                    user_id = log_data.get('user_id')
                    interaction_type = log_data.get('type')
                    timestamp = log_data.get('timestamp')
                    
                    if user_id:
                        if user_id not in user_stats:
                            user_stats[user_id] = {
                                'total_interactions': 0,
                                'first_interaction': timestamp,
                                'last_interaction': timestamp,
                                'interaction_types': {}
                            }
                            
                        user_stats[user_id]['total_interactions'] += 1
                        user_stats[user_id]['last_interaction'] = timestamp
                        
                        if interaction_type:
                            if interaction_type not in user_stats[user_id]['interaction_types']:
                                user_stats[user_id]['interaction_types'][interaction_type] = 0
                            user_stats[user_id]['interaction_types'][interaction_type] += 1
            except Exception as e:
                logger.error(f"Ошибка при анализе лога {log_file}: {e}")
    
    return user_stats

def initialize_admin():
    """Инициализирует администратора по умолчанию, если он не существует"""
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(username="admin").first()
        if not admin:
            admin = User(username="admin", is_admin=True)
            admin.set_password("admin123")  # Временный пароль
            db.session.add(admin)
            db.session.commit()
            logger.info("Администратор по умолчанию создан")

# Декоратор для проверки авторизации
def login_required(view_func):
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            flash('Для доступа к этой странице необходимо войти в систему', 'warning')
            return redirect(url_for('login'))
        return view_func(*args, **kwargs)
    wrapped_view.__name__ = view_func.__name__
    return wrapped_view

def admin_required(view_func):
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            flash('Для доступа к этой странице необходимо войти в систему', 'warning')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('У вас нет прав администратора для доступа к этой странице', 'danger')
            return redirect(url_for('dashboard'))
        
        return view_func(*args, **kwargs)
    wrapped_view.__name__ = view_func.__name__
    return wrapped_view

# Роуты для авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Вы успешно вошли в систему', 'success')
            return redirect(url_for('dashboard'))
        
        flash('Неверное имя пользователя или пароль', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Вы вышли из системы', 'success')
    return redirect(url_for('login'))

# Роуты для панели управления
@app.route('/')
@login_required
def dashboard():
    bot_status = check_bot_running()
    uptime = get_uptime() if bot_status else "Не запущен"
    last_logs = get_logs(10)
    user_stats = get_user_stats()
    
    # Статистика за последние 24 часа
    current_time = datetime.now()
    users_24h = 0
    interactions_24h = 0
    
    for user_id, stats in user_stats.items():
        last_interaction = datetime.strptime(stats['last_interaction'], "%Y-%m-%d %H:%M:%S")
        if current_time - last_interaction <= timedelta(days=1):
            users_24h += 1
            interactions_24h += stats['total_interactions']
    
    return render_template('dashboard.html', 
                          bot_status=bot_status, 
                          uptime=uptime,
                          logs=last_logs,
                          user_stats=user_stats,
                          total_users=len(user_stats),
                          users_24h=users_24h,
                          interactions_24h=interactions_24h)

@app.route('/logs')
@login_required
def logs():
    count = request.args.get('count', 50, type=int)
    logs = get_logs(count)
    return render_template('logs.html', logs=logs)

@app.route('/user/<int:user_id>')
@login_required
def user_details(user_id):
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    user_logs = []
    
    if os.path.exists(logs_dir):
        log_files = [os.path.join(logs_dir, f) for f in os.listdir(logs_dir) 
                     if f.startswith(f'interaction_{user_id}_') and f.endswith('.json')]
        
        for log_file in sorted(log_files, key=os.path.getmtime, reverse=True):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
                    user_logs.append(log_data)
            except Exception as e:
                logger.error(f"Ошибка при чтении лога {log_file}: {e}")
    
    return render_template('user_details.html', user_id=user_id, logs=user_logs)

@app.route('/settings', methods=['GET', 'POST'])
@admin_required
def settings():
    if request.method == 'POST':
        # Обработка изменения настроек
        pass
    
    return render_template('settings.html')

@app.route('/users')
@admin_required
def users():
    admin_users = User.query.all()
    return render_template('users.html', users=admin_users)

@app.route('/users/add', methods=['GET', 'POST'])
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_admin = 'is_admin' in request.form
        
        if not username or not password:
            flash('Необходимо указать имя пользователя и пароль', 'danger')
            return redirect(url_for('add_user'))
        
        if User.query.filter_by(username=username).first():
            flash('Пользователь с таким именем уже существует', 'danger')
            return redirect(url_for('add_user'))
        
        new_user = User(username=username, is_admin=is_admin)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Пользователь успешно добавлен', 'success')
        return redirect(url_for('users'))
    
    return render_template('add_user.html')

@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_admin = 'is_admin' in request.form
        
        if not username:
            flash('Необходимо указать имя пользователя', 'danger')
            return redirect(url_for('edit_user', user_id=user_id))
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != user_id:
            flash('Пользователь с таким именем уже существует', 'danger')
            return redirect(url_for('edit_user', user_id=user_id))
        
        user.username = username
        user.is_admin = is_admin
        
        if password:
            user.set_password(password)
        
        db.session.commit()
        flash('Пользователь успешно обновлен', 'success')
        return redirect(url_for('users'))
    
    return render_template('edit_user.html', user=user)

@app.route('/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    if session.get('user_id') == user_id:
        flash('Нельзя удалить самого себя', 'danger')
        return redirect(url_for('users'))
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    flash('Пользователь успешно удален', 'success')
    return redirect(url_for('users'))

# API для управления ботом
@app.route('/api/status')
@login_required
def api_status():
    return jsonify({
        'status': 'running' if check_bot_running() else 'stopped',
        'uptime': get_uptime(),
        'pid': bot_process.pid if bot_process else None
    })

@app.route('/api/start', methods=['POST'])
@admin_required
def api_start():
    result = run_bot()
    return jsonify({
        'success': result,
        'status': 'running' if check_bot_running() else 'stopped',
        'message': 'Бот запущен' if result else 'Ошибка при запуске бота'
    })

@app.route('/api/stop', methods=['POST'])
@admin_required
def api_stop():
    result = stop_bot()
    return jsonify({
        'success': result,
        'status': 'stopped' if not check_bot_running() else 'running',
        'message': 'Бот остановлен' if result else 'Ошибка при остановке бота'
    })

@app.route('/api/restart', methods=['POST'])
@admin_required
def api_restart():
    result = restart_bot()
    return jsonify({
        'success': result,
        'status': 'running' if check_bot_running() else 'stopped',
        'message': 'Бот перезапущен' if result else 'Ошибка при перезапуске бота'
    })

@app.route('/api/logs')
@login_required
def api_logs():
    count = request.args.get('count', 10, type=int)
    logs = get_logs(count)
    return jsonify(logs)

@app.route('/api/users')
@login_required
def api_users():
    user_stats = get_user_stats()
    return jsonify(user_stats)

# Обработчик ошибок
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Инициализация администратора при первом запуске
initialize_admin()

# Запуск приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)