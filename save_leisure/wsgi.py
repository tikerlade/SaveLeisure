"""
WSGI config for save_leisure project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import logging
import os
import socket

from django.core.wsgi import get_wsgi_application
from emoji import emojize
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, CallbackQueryHandler, ConversationHandler, \
    CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, \
    KeyboardButtonPollType, Update

# Django part
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "save_leisure.settings")
application = get_wsgi_application()

TELEGRAM_TOKEN = "1333523508:AAGlKzQgOqsGSRKr7kuV3u-pV4ArYrvuKcg"
HEROKU_URL = "https://save-leisure.herokuapp.com/"
PORT = int(os.environ.get('PORT', '8443'))

from bot.models import User, ToSeeItem, ItemType


def echo(update, context):
    """Send user message with his text. Like echo in the mountains"""
    respond_text = update.message.text
    print("tesp")
    # Send message
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=respond_text
    )


# Basic connection setup
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(Filters.text, echo))

# Start to listen for messages
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TELEGRAM_TOKEN)
updater.bot.set_webhook("https://delete-bot-webhook.herokuapp.com/" + TELEGRAM_TOKEN)
# updater.idle()