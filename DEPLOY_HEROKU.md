# Инструкция по развертыванию бота на Heroku

## Предварительные требования
1. Аккаунт на [Heroku](https://signup.heroku.com/)
2. Установленный [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. Установленный [Git](https://git-scm.com/downloads)

## Шаги по развертыванию

### 1. Подготовка проекта
Убедитесь, что в корневой директории проекта присутствуют следующие файлы:
- `Procfile` (содержит: `worker: python main.py`)
- `runtime.txt` (содержит версию Python, например: `python-3.11.8`)
- `requirements-heroku.txt` (переименуйте в `requirements.txt` перед загрузкой на Heroku)

### 2. Инициализация Git и создание приложения Heroku

```bash
# Войдите в аккаунт Heroku
heroku login

# Инициализируйте Git репозиторий
git init
git add .
git commit -m "Initial commit"

# Создайте приложение на Heroku
heroku create your-bot-name

# Переименуйте requirements-heroku.txt в requirements.txt
mv requirements-heroku.txt requirements.txt
```

### 3. Настройка переменных окружения

```bash
# Установите переменные окружения для API ключей
heroku config:set TELEGRAM_TOKEN=ваш_токен_телеграм_бота
heroku config:set GEMINI_API_KEY=ваш_ключ_api_gemini
```

### 4. Загрузка кода на Heroku

```bash
# Отправьте код в Heroku
git push heroku master

# Проверьте, что воркер запущен
heroku ps

# Если воркер не запущен, запустите его
heroku ps:scale worker=1
```

### 5. Мониторинг и логи

```bash
# Просмотр логов приложения
heroku logs --tail
```

### 6. Масштабирование и поддержка

По мере роста использования бота вы можете масштабировать количество воркеров:

```bash
# Увеличить количество рабочих процессов
heroku ps:scale worker=2
```

### Решение проблем

Если возникают проблемы с запуском:

1. Проверьте логи: `heroku logs --tail`
2. Убедитесь, что зависимости правильно указаны в `requirements.txt`
3. Проверьте, что переменные окружения правильно настроены: `heroku config`

### Обновление существующего приложения

Для обновления кода бота выполните:

```bash
git add .
git commit -m "Update bot code"
git push heroku master
```

## Важные замечания

1. Убедитесь, что вы не превышаете ограничения бесплатного плана Heroku (если используете его)
2. Для непрерывной работы рекомендуется перейти на платный план Heroku
3. Настройте бота на использование вебхуков для более эффективной работы на Heroku