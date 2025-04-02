# Этот файл содержит конфигурацию WSGI для Flask
import sys
import os

# Добавляем путь к папке с проектом
project_path = os.path.dirname(os.path.abspath(__file__))
if project_path not in sys.path:
    sys.path.append(project_path)

# Импорт приложения Flask для запуска через Gunicorn
from app import app as application

# Объявляем app для запуска через Gunicorn в main:app
app = application