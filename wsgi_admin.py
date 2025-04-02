from app import app

# Файл для запуска через Gunicorn
# gunicorn --bind 0.0.0.0:5000 wsgi_admin:app