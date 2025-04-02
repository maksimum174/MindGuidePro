from app import app

# Этот файл нужен для запуска через Gunicorn
# В workflow используется команда: gunicorn --bind 0.0.0.0:5000 --reuse-port --reload flask_web:app