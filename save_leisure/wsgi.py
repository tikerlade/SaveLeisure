"""
WSGI config for save_leisure project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import logging
import os

from django.core.wsgi import get_wsgi_application
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

# Django part
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "save_leisure.settings")
application = get_wsgi_application()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


# Bot part
def start(update, context):
    """Greeting message from bot after /start received."""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a SaveLeisure bot, please talk to me!"
        + "Currently I'm able only to echo your messages :(",
    )


def echo(update, context):
    """Send user message with his text. Like echo in the mountains"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


# Basic connection setup
updater = Updater(token=os.getenv("TELEGRAM_TOKEN"), use_context=True)
dispatcher = updater.dispatcher

# Handlers initialization
start_handler = CommandHandler("start", start)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

# Setting dispatcher to use handlers
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(start_handler)

# Start to listen for messages
updater.start_polling()
