import pkg_resources

# Получить версию пакета python-telegram-bot
try:
    version = pkg_resources.get_distribution("python-telegram-bot").version
    print(f"Установленная версия python-telegram-bot: {version}")
except pkg_resources.DistributionNotFound:
    print("python-telegram-bot не установлен")

# Проверить наличие пакета telegram
try:
    version = pkg_resources.get_distribution("telegram").version
    print(f"Установленная версия telegram: {version}")
except pkg_resources.DistributionNotFound:
    print("telegram не установлен")