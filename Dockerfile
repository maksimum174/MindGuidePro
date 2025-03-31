FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements-fly.txt .
RUN pip install --no-cache-dir -r requirements-fly.txt

# Копирование исходного кода
COPY . .

# Запуск бота
CMD ["python", "main.py"]