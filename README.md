# @psi_help24_bot (Бесплатный ИИ-Психолог 24/7)

Telegram-бот психологической поддержки, основанный на гештальт-терапии и нейро-лингвистическом программировании (НЛП), разработанный с использованием Gemini AI и специализированный для русскоязычной аудитории. Проект работает в роли опытного гештальт-терапевта и предоставляет персонализированную психологическую помощь через современные коммуникационные технологии.

## 🌟 Ключевые возможности

- 👁️ **Гештальт-терапевтический подход** - фокус на "здесь и сейчас", осознавание, полярности, незавершённые гештальты
- 🧠 **Техники нейро-лингвистического программирования (НЛП)** - рефрейминг, якорение, работа с субмодальностями, метамодель
- 🧘 **Психотерапевтические эксперименты** - практические упражнения и техники осознавания для самостоятельной работы
- 🇷🇺 **Полностью на русском языке** - с учетом культурных особенностей русскоязычной аудитории
- 💬 **Краткие, интерактивные ответы** - в стиле реальной гештальт-сессии (3-5 предложений)
- 🔄 **Многоступенчатый гештальт-цикл** - осознавание, мобилизация, действие, контакт, завершение
- 🕒 **Доступен 24/7** - психологическая поддержка в любое время суток
- 🔐 **Конфиденциальность** - все данные остаются между пользователем и ботом

## 🛠️ Технический стек

- **Язык программирования**: Python 3.10+
- **ИИ-платформа**: Gemini 1.5 Pro от Google
- **Интерфейс**: Telegram Bot API
- **Библиотеки**:
  - pyTelegramBotAPI - для работы с Telegram
  - google-generativeai - для взаимодействия с Gemini AI
  - Flask - для веб-интерфейса администрирования (опционально)
- **Логирование**: JSON-формат для анализа взаимодействий
- **Деплой**: Docker-контейнеры, инструкции для различных платформ

## 🚀 Быстрый старт

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ваш_логин/psi-help24-bot.git
   cd psi-help24-bot
   ```

2. Создайте виртуальное окружение и установите зависимости:
   ```bash
   python -m venv venv
   source venv/bin/activate  # На Windows: venv\Scripts\activate
   pip install -r requirements-bot.txt
   ```

3. Скопируйте файл `.env.example` в `.env` и заполните необходимые данные:
   ```bash
   cp .env.example .env
   # Отредактируйте файл .env, добавив ваши API-ключи
   ```

4. Запустите бота:
   ```bash
   python main.py
   ```

## 📊 Примеры диалогов в гештальт-подходе и с применением НЛП

### Пример 1: Гештальт-подход (работа с телесными ощущениями и незавершенными гештальтами)

**Пользователь**: Я часто чувствую тревогу без причины. Что мне делать?

**Бот**: Я слышу, что тревога возникает "без причины", и это может быть непонятно и неприятно. Давайте сначала обратимся к тому, что происходит в вашем теле, когда появляется эта тревога. Где именно в теле вы её ощущаете? Можете описать эти телесные ощущения?

**Пользователь**: В груди давит, дыхание становится поверхностным, и появляется ком в горле.

**Бот**: Спасибо за эти важные наблюдения. Ощущение давления в груди, поверхностное дыхание и ком в горле — это способ, которым ваше тело сигнализирует о чём-то значимом. В гештальт-подходе мы можем использовать эти телесные "якоря" как путь к незавершённым ситуациям.

Предлагаю простой эксперимент: когда появляются эти ощущения, положите руку на грудь, сделайте глубокий вдох и скажите вслух: "Я сейчас замечаю давление и напряжение. Чего хочет эта часть меня?" Что первым приходит в голову, когда вы задаёте себе этот вопрос?

### Пример 2: НЛП-подход (рефрейминг и работа с субмодальностями)

**Пользователь**: Я постоянно боюсь совершить ошибку на работе, и это парализует меня.

**Бот**: Понимаю ваши ощущения. Интересно, когда вы думаете об "ошибке", какой образ возникает перед внутренним взором? Он цветной или черно-белый? Большой или маленький? Близкий или далекий?

**Пользователь**: Это большое темное пятно, очень близко ко мне, почти давит.

**Бот**: Спасибо за такое точное описание. Давайте попробуем изменить эти субмодальности. Представьте, что вы можете взять этот образ "ошибки" и начать медленно отодвигать его от себя, делая меньше и добавляя немного света. 

Попробуйте также представить, что это не "ошибка", а "обратная связь для роста". Как меняется ваше ощущение, когда вы представляете этот новый образ немного дальше, меньше и светлее? Что вы замечаете прямо сейчас?

## 🔧 Настройка для разработчиков

Для настройки системных промптов и параметров модели можно изменить файлы:
- `prompts.py` - для редактирования системных инструкций
- `config.py` - для изменения параметров генерации (temperature, top_p и др.)
- `gemini_client.py` - для изменения логики взаимодействия с API Gemini

## 📂 Структура проекта

- `main.py` - основной файл запуска бота (pyTelegramBotAPI)
- `bot.py` - альтернативная реализация бота на python-telegram-bot
- `telebot_main.py` - содержит ту же реализацию что и main.py (для совместимости)
- `gemini_client.py` - клиент для работы с API Gemini
- `prompts.py` - системные промпты для Gemini
- `config.py` - конфигурационные параметры
- `logger.py` - система логирования взаимодействий
- `utils.py` - вспомогательные функции
- `flask_app.py` - веб-интерфейс для управления ботом
- `wsgi.py` - конфигурация для деплоя на хостинг с WSGI

## 🌐 Варианты развертывания

В репозитории есть подробные инструкции для развертывания на различных платформах:
- [Развертывание на Fly.io](DEPLOY_FLY.md) - бесплатный круглосуточный хостинг
- [Развертывание на PythonAnywhere](DEPLOY_PYTHONANYWHERE.md) - простая настройка с возможностью веб-интерфейса
- [Размещение на GitHub](DEPLOY_GITHUB.md) - для хранения и версионирования кода
- [Развертывание на Heroku](DEPLOY_HEROKU.md) - для опытных пользователей

## 🧪 Тестирование и поддержка

В репозитории есть несколько вспомогательных скриптов для тестирования:
- `check_telegram_imports.py` - проверка корректности импортов библиотеки python-telegram-bot
- `test_bot.py` и `test_bot_v13.py` - тестовые версии Telegram-бота
- `test_gemini_models.py` - проверка доступных моделей Gemini

## 📑 Лицензия

MIT License

## ⚠️ Ограничения

Бот не заменяет профессиональной психологической помощи. В случае серьезных психологических проблем или кризисов, пожалуйста, обратитесь к квалифицированному специалисту.