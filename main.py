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
from telegram.ext import (
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType,
    Update,
)

# Django part
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "save_leisure.settings")
application = get_wsgi_application()

# TELEGRAM_TOKEN = str(os.getenv("TELEGRAM_TOKEN"))
TELEGRAM_TOKEN = "1333523508:AAG-iK2wa8Iqvgum-NHs-gZ7h5SxsA-FVmU"
HEROKU_URL = "https://save-leisure.herokuapp.com/"

from bot.models import User, ToSeeItem, ItemType


def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(("", 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port


PORT = 88
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Stages
FIRST, SECOND, THIRD, FOURTH, FIFTH, SIXTH, SEVEN = range(7)
END_CONFIRMATION = 8


# Bot part
def start(update, context):
    """
    Greeting message from bot after '/start' received.
    In addition new user added to database.
    """

    # Some initialization
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    respond_text = (
        "I'm a SaveLeisure :robot:, please talk to me :speech_balloon:!\n"
        "Currently I'm able only to echo your messages :hear_no_evil:"
    )

    # Keyboard with 3 options from the start
    keyboard = [
        [InlineKeyboardButton("Add new item", callback_data="new_item")],
        [InlineKeyboardButton("Get my items", callback_data="get_items")],
        [InlineKeyboardButton("Information", callback_data="info")],
    ]
    keyboard = InlineKeyboardMarkup(keyboard)

    # Check if user has already been added to database
    # if User.objects.filter(telegram_id=user_id):
    #     # If user has already been created - detect it
    #     respond_text = (
    #         "I know you were here before :expressionless:\n"
    #         "I'm just kidding, welcome again :heart_eyes:\n"
    #         "Maybe later you could delete your profile and"
    #         " start a new one, but it is not for sure :thinking_face:"
    #     )
    # else:
    #     # If user used /start in a first time - register him
    #     user = User(chat_id=chat_id, telegram_id=user_id)
    #     user.save()

    # Send message with information about what has been done
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=emojize(respond_text, use_aliases=True),
        reply_markup=keyboard,
    )

    return FIRST


def new_item(update, context):
    query = update.callback_query
    query.answer()

    keyboard = [
        [
            InlineKeyboardButton(emojize("Film :cinema:"), callback_data="cinema"),
            InlineKeyboardButton(emojize("Paper :scroll:"), callback_data="scroll"),
            InlineKeyboardButton(emojize("Book :books:"), callback_data="book"),
        ],
        [
            InlineKeyboardButton(
                emojize("Cancel :cross_mark:"), callback_data="cross_mark"
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text=emojize(
            f"Okay :fire:, Tell me what is your item you want to add is about"
        ),
        reply_markup=reply_markup,
    )

    return SECOND


def get_items(update, context):
    query = update.callback_query
    query.answer()

    keyboard = [
        [
            InlineKeyboardButton(emojize("Film :cinema:"), callback_data="cinema"),
            InlineKeyboardButton(emojize("Paper :scroll:"), callback_data="scroll"),
            InlineKeyboardButton(emojize("Book :books:"), callback_data="book"),
        ],
        [
            InlineKeyboardButton(
                emojize("Mix :person_shrugging:"), callback_data="mix"
            ),
            InlineKeyboardButton(
                emojize("Cancel :cross_mark:"), callback_data="cross_mark"
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text=emojize(f"Okay :fire:, Tell me what type of items you want to get"),
        reply_markup=reply_markup,
    )

    return FOURTH


def get_items_type(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text("Now enter how many items to return to you")

    return FIFTH


def get_items_number(update, context):
    number = int(update.message.text)

    for i in range(number):
        update.message.reply_text(str(i))

    keyboard = [
        [
            InlineKeyboardButton(emojize("End :stop_sign:"), callback_data="end"),
            InlineKeyboardButton(
                emojize("To beginning :right_arrow_curving_left:"),
                callback_data="to_beginning",
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        text=emojize("Do you want to try again or you leaving?"),
        reply_markup=reply_markup,
    )

    return END_CONFIRMATION


def get_info(update, context):
    query = update.callback_query
    query.answer()

    keyboard = [
        [
            InlineKeyboardButton(emojize("End :stop_sign:"), callback_data="end"),
            InlineKeyboardButton(
                emojize("To beginning :right_arrow_curving_left:"),
                callback_data="to_beginning",
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text=emojize("Here will be provided full help information"),
        reply_markup=reply_markup,
    )

    return END_CONFIRMATION


def new_item_type(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text("Now send me a message with information you want to store.")

    return THIRD


def end(update, context):
    query = update.callback_query
    user_data = context.user_data
    query.answer()

    query.edit_message_text(emojize("Bye Bye :waving_hand:"))

    user_data.clear()
    return ConversationHandler.END


def to_beginning(update, context):
    query = update.callback_query
    query.answer()

    keyboard = [
        [InlineKeyboardButton("Add new item", callback_data="new_item")],
        [InlineKeyboardButton("Get my items", callback_data="get_items")],
        [InlineKeyboardButton("Information", callback_data="info")],
    ]
    keyboard = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text=emojize("Please choose your next step", use_aliases=True),
        reply_markup=keyboard,
    )

    return FIRST


def cross_mark(update, context):
    query = update.callback_query
    query.answer()

    keyboard = [
        [
            InlineKeyboardButton(emojize("End :stop_sign:"), callback_data="end"),
            InlineKeyboardButton(
                emojize("To beginning :right_arrow_curving_left:"),
                callback_data="to_beginning",
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text=emojize("Do you want to try again or you leaving?"),
        reply_markup=reply_markup,
    )

    return END_CONFIRMATION


def save_item(update, context):

    # Store users data
    print(context.user_data)

    keyboard = [
        [
            InlineKeyboardButton(emojize("End :stop_sign:"), callback_data="end"),
            InlineKeyboardButton(
                emojize("To beginning :right_arrow_curving_left:"),
                callback_data="to_beginning",
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "We have saved your information. What you will do next?",
        reply_markup=reply_markup,
    )

    return END_CONFIRMATION


def detect_forwarding(update, context):
    """
    Detecting when user forward to us some message.
    After detection we need to understand which type of content was forwarded.
    Returns to user keyboard to choose type of content.
    """

    # Initialization phase
    user_id = str(update.effective_user.id)
    keyboard = [
        [
            InlineKeyboardButton(
                emojize(":cinema:"), callback_data="forwarding_cinema"
            ),
            InlineKeyboardButton(
                emojize(":scroll:"), callback_data="forwarding_scroll"
            ),
            InlineKeyboardButton(emojize(":books:"), callback_data="forwarding_books"),
        ],
        [
            InlineKeyboardButton(
                emojize("Cancel :cross_mark:"), callback_data="cross_mark"
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Reply with keyboard of types
    update.message.reply_text(
        "What type of content is in message:", reply_markup=reply_markup
    )


def new_forwarded_item_type(update, context):
    query = update.callback_query
    query.answer()

    # # Information retrieving
    # post_type = query.data
    # user_id = query.from_user.id
    # message_id = query.message.message_id
    # message_date = query.message.date
    # text = query.message.text
    #
    # # Foreign keys extracting
    # user = User.objects.get(telegram_id=user_id)
    # item_type = ItemType.objects.get(data_type=post_type)
    #
    # # Register new item for user
    # item = ToSeeItem(
    #     user_id=user,
    #     message_id=message_id,
    #     date_received=message_date,
    #     data_type=item_type,
    #     raw_data=text,
    # )
    # item.save()

    keyboard = [
        [
            InlineKeyboardButton(emojize("End :stop_sign:"), callback_data="end"),
            InlineKeyboardButton(
                emojize("To beginning :right_arrow_curving_left:"),
                callback_data="to_beginning",
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # TODO: random emojis when they are placeholders.
    # Show that we have created new item for this user
    query.edit_message_text(
        text=emojize(f"Okay :fire:, Now I have registered it. What's next?"),
        reply_markup=reply_markup,
    )

    return END_CONFIRMATION


def new_forwarded_item(update, context):
    keyboard = [
        [
            InlineKeyboardButton(emojize("Film :cinema:"), callback_data="cinema"),
            InlineKeyboardButton(emojize("Paper :scroll:"), callback_data="scroll"),
            InlineKeyboardButton(emojize("Book :books:"), callback_data="book"),
        ],
        [
            InlineKeyboardButton(
                emojize("Cancel :cross_mark:"), callback_data="cross_mark"
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        text=emojize(f"Okay :fire:, Now give me understanding of what the data it is"),
        reply_markup=reply_markup,
    )
    return SIXTH


def get_all(update, context):
    # TODO: check that user in database
    user_id = update.effective_user.id
    user = User.objects.get(telegram_id=user_id)
    items = ToSeeItem.objects.filter(user_id=user)

    mapping = {
        1: "keycap_digit_one",
        2: "keycap_digit_two",
        3: "keycap_digit_three",
        4: "keycap_digit_four",
    }

    if len(items) > 0:
        for idx, entry in enumerate(items, 1):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=emojize(f":{mapping[idx]}:"),
                reply_to_message_id=entry.message_id,
            )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=emojize("There is nothing for you now :pensive:"),
        )


#
# def start(update: Update, context: CallbackContext) -> None:
#     """Send message on `/start`."""
#     # Get user that sent /start and log his name
#     user = update.message.from_user
#     # logger.info("User %s started the conversation.", user.first_name)
#     # Build InlineKeyboard where each button has a displayed text
#     # and a string as callback_data
#     # The keyboard is a list of button rows, where each row is in turn
#     # a list (hence `[[...]]`).
#     keyboard = [
#         [
#             InlineKeyboardButton("1", callback_data=str(ONE)),
#             InlineKeyboardButton("2", callback_data=str(TWO)),
#         ]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     # Send message with text and appended InlineKeyboard
#     update.message.reply_text(
#         "Start handler, Choose a route", reply_markup=reply_markup
#     )
#     # Tell ConversationHandler that we're in state `FIRST` now
#     return FIRST


def func():
    pass


def cancel():
    pass


def main():
    # Updater initialization with TELEGRAM token
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Logics
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(Filters.forwarded, new_forwarded_item),
            MessageHandler(Filters.text, cancel),
        ],
        states={
            FIRST: [
                CallbackQueryHandler(new_item, pattern="^new_item$"),
                CallbackQueryHandler(get_items, pattern="^get_items$"),
                CallbackQueryHandler(get_info, pattern="^info$"),
            ],
            SECOND: [
                CallbackQueryHandler(new_item_type, pattern="^(cinema|scroll|book)$"),
                CallbackQueryHandler(cross_mark, pattern="^cross_mark$"),
            ],
            THIRD: [MessageHandler(Filters.text, save_item)],
            FOURTH: [
                CallbackQueryHandler(
                    get_items_type, pattern="^(cinema|scroll|book|mix)$"
                ),
                CallbackQueryHandler(cross_mark, pattern="^cross_mark$"),
            ],
            FIFTH: [MessageHandler(Filters.text, get_items_number)],
            SIXTH: [
                CallbackQueryHandler(
                    new_forwarded_item_type, pattern="^(cinema|scroll|book)$"
                ),
                CallbackQueryHandler(cross_mark, pattern="^cross_mark$"),
            ],
            END_CONFIRMATION: [
                CallbackQueryHandler(end, pattern="^end$"),
                CallbackQueryHandler(to_beginning, pattern="^to_beginning$"),
            ],
        },
        fallbacks=[CommandHandler("end", end)],
    )

    # Add ConversationHandler to dispatcher for handle updates of conversation
    dispatcher.add_handler(conv_handler)

    # Start listening for updates
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    # TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

    main()
