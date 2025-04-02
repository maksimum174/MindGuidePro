#!/bin/bash
# Запуск веб-интерфейса для управления ботом
gunicorn --bind 0.0.0.0:5000 flask_web:app