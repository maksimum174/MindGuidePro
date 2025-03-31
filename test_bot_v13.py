#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Простой бот для ответа на сообщения в Telegram.
"""
import os
import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Включение логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Определение обработчиков
def start(update: Update, context: CallbackContext) -> None:
    """Отправляет сообщение при команде /start."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        f'Привет, {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Отправляет сообщение при команде /help."""
    update.message.reply_text('Помощь!')


def echo(update: Update, context: CallbackContext) -> None:
    """Эхо на сообщение пользователя."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Запуск бота."""
    # Создание Updater и передача токена бота
    updater = Updater(os.environ["TELEGRAM_TOKEN"])

    # Получение диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрация обработчиков
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Обработчик сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Запуск бота
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()