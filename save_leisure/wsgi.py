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
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

# Django part
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "save_leisure.settings")
application = get_wsgi_application()

TELEGRAM_TOKEN = str(os.getenv("TELEGRAM_TOKEN"))
HEROKU_URL = "https://save-leisure.herokuapp.com/"

from bot.models import User


def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(("", 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port


PORT = "80"
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


# Bot part
def start(update, context):
    """
    Greeting message from bot after /start received.
    In addition new user added to database.
    """

    # Some initialization
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    respond_text = (
        "I'm a SaveLeisure :robot:, please talk to me :speech_balloon:!\n"
        "Currently I'm able only to echo your messages :hear_no_evil:"
    )

    # Check if user has already been added to database
    if User.objects.filter(telegram_id=user_id):
        respond_text = (
            "I know you were here before :expressionless:\n"
            "I'm just kidding, welcome again :heart_eyes:\n"
            "Maybe later you could delete your profile and"
            " start a new one, but it is not for sure :thinking_face:"
        )
    else:
        user = User(chat_id=chat_id, telegram_id=user_id)
        user.save()

    # Send message
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=emojize(respond_text, use_aliases=True),
    )


def echo(update, context):
    """Send user message with his text. Like echo in the mountains"""
    respond_text = update.message.text
    user_id = update.effective_user.id

    # Check if user has used /start command (registered in database)
    if not User.objects.filter(telegram_id=user_id):
        respond_text = "You haven't used /start command :warning:\nPlease do it!"

    # Check wheather it is responding or not
    if update.message.reply_to_message:
        respond_text = (
            "I know that you a responding to some other message :grinning:\n"
            "But currently I can't understand the sense"
        )

    # Send message
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=emojize(respond_text, use_aliases=True)
    )


# Basic connection setup
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Handlers initialization
start_handler = CommandHandler("start", start)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

# Setting dispatcher to use handlers
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(start_handler)

# Start to listen for messages
# updater.start_polling()

updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TELEGRAM_TOKEN)
updater.bot.setWebhook(HEROKU_URL + TELEGRAM_TOKEN)

updater.idle()
