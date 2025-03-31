"""
Проверка импортов библиотеки python-telegram-bot
"""

try:
    print("Проверка импортов из telegram:")
    import telegram
    print("  telegram импортирован успешно")
    print("  Доступные модули и классы:")
    for item in dir(telegram):
        if not item.startswith("_"):
            print(f"    - {item}")
except ImportError as e:
    print(f"  Ошибка импорта telegram: {e}")

try:
    print("\nПроверка импортов из telegram.ext:")
    import telegram.ext
    print("  telegram.ext импортирован успешно")
    print("  Доступные модули и классы:")
    for item in dir(telegram.ext):
        if not item.startswith("_"):
            print(f"    - {item}")
except ImportError as e:
    print(f"  Ошибка импорта telegram.ext: {e}")

try:
    print("\nПроверка импортов классов:")
    from telegram import Update, Bot
    print("  Update и Bot импортированы успешно")
except ImportError as e:
    print(f"  Ошибка импорта Update и Bot: {e}")

try:
    from telegram.ext import Application, CommandHandler
    print("  Application и CommandHandler импортированы успешно")
except ImportError as e:
    print(f"  Ошибка импорта Application и CommandHandler: {e}")