"""
Main functionality and logic of bot. Handlers, running, functions, database working - all happens here.
"""
import logging
import os
from datetime import datetime

from emoji import emojize
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telegram import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)

from bot.keyboards import (
    end_confirmation_keyboard_markup,
    get_types_keyboard_markup,
    types_keyboard_markup,
    welcome_keyboard_markup,
)
from bot.models import ItemType, ToSeeItem, User

# General information
RUNNING_MODE = "PRODUCTION"
TELEGRAM_TOKEN = str(os.getenv("TELEGRAM_TOKEN"))
HEROKU_URL = str(os.getenv("HEROKU_APP"))
DATABASE_URL = str(os.getenv("DATABASE_URL"))
PORT = int(os.environ.get("PORT", "8443"))

# Stages
FIRST, SECOND, THIRD, FOURTH, FIFTH, SIXTH, SEVEN = range(7)
END_CONFIRMATION = 18

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def start(update, context):
    """
    Greeting message from bot after '/start' received.
    In addition new user added to database.
    """

    # Some initialization
    telegram_id = update.effective_user.id
    chat_id = update.effective_chat.id
    respond_text = (
        "I'm a SaveLeisure :robot:, please talk to me :speech_balloon:!\n"
        "Currently I'm able only to echo your messages :hear_no_evil:"
    )

    # Check if user has already been added to database
    if session.query(User).filter_by(telegram_id=telegram_id).first():
        # If user has already been created - detect it
        respond_text = (
            "I know you were here before :expressionless:\n"
            "I'm just kidding, welcome again :heart_eyes:\n"
            "Maybe later you could delete your profile and"
            " start a new one, but it is not for sure :thinking_face:"
        )
    else:
        # If user used /start in a first time - register him
        new_user = User(
            chat_id=chat_id, telegram_id=telegram_id, registration_date=datetime.today()
        )
        session.add(new_user)
        session.commit()

    # Send message with information about what has been done
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=emojize(respond_text, use_aliases=True),
        reply_markup=welcome_keyboard_markup,
    )

    return FIRST


def send_answer(update, context, arguments):
    query = update.callback_query
    if not query:
        context.bot.send_message(chat_id=update.effective_chat.id, **arguments)
    else:
        query.answer()
        query.edit_message_text(**arguments)


def new_iteration(update, context):
    # Some initialization
    respond_text = "I like to see you here again :heart_eyes:\nHow can I help you?"

    # Send message with information about what has been done
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=emojize(respond_text, use_aliases=True),
        reply_markup=welcome_keyboard_markup,
    )
    return FIRST


def new_item(update, context):
    arguments = {
        "text": emojize(
            f"Okay :fire:, Tell me what is your item you want to add is about"
        ),
        "reply_markup": types_keyboard_markup,
    }

    send_answer(update, context, arguments)

    return SECOND


def get_items(update, context):
    arguments = {
        "text": emojize(f"Okay :fire:, Tell me what type of items you want to get"),
        "reply_markup": get_types_keyboard_markup,
    }

    send_answer(update, context, arguments)

    return FOURTH


def get_items_type(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text=emojize(
            f"Now enter how many :{query.data}: to return to you :input_numbers:"
        ),
        reply_markup=end_confirmation_keyboard_markup,
    )
    context.user_data["get_data_type"] = query.data

    return FIFTH


def get_items_number(update, context):

    print(update.message.text)
    # Check that input is a number.
    number = update.message.text
    if not number.isnumeric():
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=emojize("No no no! It's not a number! Try again. :warning_selector:"),
        )

        # Return to this stage.
        return FIFTH

    # Get other users parameters for database query.
    data_type = context.user_data["get_data_type"]
    telegram_id = update.effective_user.id
    number = int(number)

    # Get foreign keys for datatbase query.
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    item_type = session.query(ItemType).filter_by(data_type=data_type).first()

    # Retrieve data with given parameters.
    if item_type:
        # If one of known types was selected.
        items = (
            session.query(ToSeeItem)
            .filter_by(user_id=user.user_id, type_id=item_type.type_id, showed=False)
            .all()
        )
    else:
        # If mix was selected as type.
        items = (
            session.query(ToSeeItem).filter_by(user_id=user.user_id, showed=False).all()
        )

    # Send received items
    respond_text = "Do you want to try again or you leaving?"
    if not items:
        # No items of given data was found.
        respond_text = (
            f"You have not added any :{data_type}: yet :pensive_face:.\n" + respond_text
        )
    else:
        # Send each message which was retrieved.
        context.user_data["items"] = {}

        if len(items) < number:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=emojize(
                    f"You have only {len(items)}/{number} of :{data_type}: and here they are"
                ),
            )

        for idx in range(min(len(items), number)):
            context.user_data["items"][idx + 1] = items[idx].record_id
            print(items[idx].record_id)

            context.bot.send_message(
                text=emojize(number_to_emoji(idx + 1)),
                chat_id=update.effective_chat.id,
                reply_to_message_id=items[idx].message_id,
            )

            # TODO update value of showed to True
            session.query(ToSeeItem).filter(
                ToSeeItem.record_id == items[idx].record_id
            ).update({ToSeeItem.showed: True})
            session.commit()

        # Information about user can skip his information.
        context.bot.send_message(
            text="If you want to skip some items and mark them as unread you can do so.\n"
            "However it will work only with last sent by me numbers.\n"
            "Just follow the instructions after the command:\n"
            "`/unread`",
            chat_id=update.effective_chat.id,
            parse_mode=ParseMode.MARKDOWN,
        )

    # Prompt for staying and use bot one more time.
    update.message.reply_text(
        text=emojize(respond_text), reply_markup=end_confirmation_keyboard_markup
    )

    # Move to confirmation of users choice for following up.
    return END_CONFIRMATION


def get_info(update, context):
    arguments = {
        "text": emojize(
            "This is a bot :robot_face: for automation your basic routine of sending staff that you want to"
            " read :SOON_arrow: to your *Saved Messages* which will "
            "shortly become a mess :woozy_face: where you can't find anything.\n\n"
            "`Forwarding` - forward article that you like to bot and save it\n\n"
            "`/start` - start a conversation with this bot\n"
            "`/help` - here you are\n"
            "`/new` - add new item to your list\n"
            "`/get` - get items from your added items\n"
            "`/unread` - mark listed items as unread\n"
            "`/stats` - will give you general statistics\n"
            "`/end` - end current conversation\n\n"
            "`/new` & `/get` will give you options :gear_selector: to set everything as you need.\n\n"
            ":warning_selector: Developing is still in progress :warning_selector:"
        ),
        "parse_mode": ParseMode.MARKDOWN,
        "reply_markup": end_confirmation_keyboard_markup,
    }

    send_answer(update, context, arguments)

    return END_CONFIRMATION


def stat(update, context):

    respond_text = "Based on your full history of adding items.\nHere are some stats :bar_chart: about them:\n\n"
    item_types = ["cinema", "page_with_curl", "books"]
    item_to_count = {}

    for item in item_types:
        type_id = session.query(ItemType).filter_by(data_type=item).first().type_id
        counter = len(session.query(ToSeeItem).filter_by(type_id=type_id).all())

        item_to_count[item] = counter
        respond_text += f":{item}: - {counter} items\n"

    respond_text += "\nThank you for using me :folded_hands:"

    context.bot.send_message(
        text=emojize(respond_text),
        chat_id=update.effective_chat.id,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=end_confirmation_keyboard_markup,
    )

    return END_CONFIRMATION


def new_item_type(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text=emojize(
            f"Now send me information about :{query.data}: you want to store."
        ),
        reply_markup=end_confirmation_keyboard_markup,
    )
    context.user_data["data_type"] = query.data

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

    query.edit_message_text(
        text=emojize("Please choose your next step", use_aliases=True),
        reply_markup=welcome_keyboard_markup,
    )

    return FIRST


def cross_mark(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text=emojize("Do you want to try again or you leaving?"),
        reply_markup=end_confirmation_keyboard_markup,
    )

    return END_CONFIRMATION


def save_item(update, context):

    # Information retrieving
    data_type = context.user_data["data_type"]
    telegram_id = update.effective_user.id
    message_id = update.message.message_id
    message_date = update.message.date
    text = update.message.text

    # # Foreign keys extracting
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    item_type = session.query(ItemType).filter_by(data_type=data_type).first()

    # Register new item for user
    new_item = ToSeeItem(
        user_id=user.user_id,
        message_id=message_id,
        date_received=message_date,
        type_id=item_type.type_id,
        raw_data=text,
    )
    session.add(new_item)
    session.commit()

    update.message.reply_text(
        "We have saved your information. What you will do next?",
        reply_markup=end_confirmation_keyboard_markup,
    )

    # Clear used user data
    context.user_data["data_type"] = ""

    # Go to the next stage
    return END_CONFIRMATION


def new_forwarded_item(update, context):

    context.user_data["message_id"] = update.message.message_id
    context.user_data["message_text"] = update.message.text

    update.message.reply_text(
        text=emojize(f"Okay :fire:, Now give me understanding of what the data it is"),
        reply_markup=types_keyboard_markup,
    )

    return SIXTH


def new_forwarded_item_type(update, context):
    query = update.callback_query
    query.answer()

    # Information retrieving
    data_type = query.data
    telegram_id = query.from_user.id
    message_id = int(context.user_data["message_id"])
    message_date = query.message.date
    text = context.user_data["message_text"]

    # Foreign keys extracting
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    item_type = session.query(ItemType).filter_by(data_type=data_type).first()

    # Register new item for user
    new_item = ToSeeItem(
        user_id=user.user_id,
        message_id=message_id,
        date_received=message_date,
        type_id=item_type.type_id,
        raw_data=text,
    )
    session.add(new_item)
    session.commit()

    # Show that we have created new item for this user
    query.edit_message_text(
        text=emojize(f"Okay :fire:, Now I have registered it. What's next?"),
        reply_markup=end_confirmation_keyboard_markup,
    )

    return END_CONFIRMATION


def unread(update, context):
    respond_text = (
        "Okay. Here is what you need to do:\n"
        "1. Send me numbers which you have skipped from previous session."
        "You should do that as following: `1 5 12`. Just separate them with witespace.\n"
        "2. No more steps :winking_face_with_tongue:\n\n"
        ":warning_selector: Just remember that it will apply only to last"
        " numbers that I've sent to you. :warning_selector:"
    )

    context.bot.send_message(
        text=emojize(respond_text),
        chat_id=update.effective_chat.id,
        parse_mode=ParseMode.MARKDOWN,
    )

    return SEVEN


def unread_numbers(update, context):
    respond_text = "I have marked these messages as unread :OK_hand:"
    exception_flag = False

    numbers = update.message.text.split()
    try:
        numbers = list(map(int, numbers))

        for number in numbers:
            session.query(ToSeeItem).filter(
                ToSeeItem.record_id == context.user_data["items"][number]
            ).update({ToSeeItem.showed: False})
        session.commit()

    except ValueError:
        respond_text = "No no no! It's not a number! Try again. :warning_selector:"

    update.message.reply_text(
        text=emojize(respond_text),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=end_confirmation_keyboard_markup,
    )

    return END_CONFIRMATION if not exception_flag else SEVEN


def number_to_emoji(number):
    mapper = {
        0: ":keycap_0:",
        1: ":keycap_1:",
        2: ":keycap_2:",
        3: ":keycap_3:",
        4: ":keycap_4:",
        5: ":keycap_5:",
        6: ":keycap_6:",
        7: ":keycap_7:",
        8: ":keycap_8:",
        9: ":keycap_9:",
    }
    result = ""

    while number:
        result = mapper[number % 10] + result
        number //= 10

    return result


def main():
    # Updater initialization with TELEGRAM token
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    common_handlers = [
        CommandHandler("unread", unread),
        CommandHandler("help", get_info),
        CommandHandler("new", new_item),
        CommandHandler("get", get_items),
        CommandHandler("stats", stat),
    ]

    # Logics
    conv_handler = ConversationHandler(
        entry_points=common_handlers
        + [
            CommandHandler("start", start),
            MessageHandler(Filters.forwarded, new_forwarded_item),
            MessageHandler(Filters.text, new_iteration),
        ],
        states={
            FIRST: [
                CallbackQueryHandler(new_item, pattern="^new_item$"),
                CallbackQueryHandler(get_items, pattern="^get_items$"),
                CallbackQueryHandler(get_info, pattern="^info$"),
                CallbackQueryHandler(end, pattern="^end$"),
            ]
            + common_handlers,
            SECOND: [
                CallbackQueryHandler(
                    new_item_type, pattern="^(cinema|page_with_curl|books)$"
                ),
                CallbackQueryHandler(cross_mark, pattern="^cross_mark$"),
            ]
            + common_handlers,
            THIRD: [
                MessageHandler(Filters.text, save_item),
                CallbackQueryHandler(end, pattern="^end$"),
                CallbackQueryHandler(to_beginning, pattern="^to_beginning$"),
            ]
            + common_handlers,
            FOURTH: [
                CallbackQueryHandler(
                    get_items_type,
                    pattern="^(cinema|page_with_curl|books|person_shrugging)$",
                ),
                CallbackQueryHandler(cross_mark, pattern="^cross_mark$"),
            ]
            + common_handlers,
            FIFTH: [
                MessageHandler(Filters.text, get_items_number),
                CallbackQueryHandler(end, pattern="^end$"),
                CallbackQueryHandler(to_beginning, pattern="^to_beginning$"),
            ]
            + common_handlers,
            SIXTH: [
                CallbackQueryHandler(
                    new_forwarded_item_type, pattern="^(cinema|page_with_curl|books)$"
                ),
                CallbackQueryHandler(cross_mark, pattern="^cross_mark$"),
            ]
            + common_handlers,
            SEVEN: [MessageHandler(Filters.text, unread_numbers)],
            END_CONFIRMATION: [
                CallbackQueryHandler(end, pattern="^end$"),
                CallbackQueryHandler(to_beginning, pattern="^to_beginning$"),
            ]
            + common_handlers,
        },
        fallbacks=[CommandHandler("end", end)],
        per_message=False,
    )

    # Add ConversationHandler to dispatcher for handle updates of conversation
    dispatcher.add_handler(conv_handler)

    # Start receiving updates
    if RUNNING_MODE == "LOCAL":
        updater.start_polling()
    elif RUNNING_MODE == "PRODUCTION":
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TELEGRAM_TOKEN)

    # Close listener when it's necessary
    updater.idle()


if __name__ == "__main__":
    # Initialize database management objects
    engine = create_engine(DATABASE_URL)
    session = sessionmaker(bind=engine)()

    # Run the main part of the program
    main()
