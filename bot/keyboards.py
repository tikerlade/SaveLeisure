"""
Inline keyboards for slight interacting with user.
"""

from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Keyboard on Stage 1 when user just arrived.
welcome_keyboard = [
    [
        InlineKeyboardButton(
            emojize("Add new item :NEW_button:"), callback_data="new_item"
        )
    ],
    [
        InlineKeyboardButton(
            emojize("Get my items :page_with_curl:"), callback_data="get_items"
        )
    ],
    [
        # InlineKeyboardButton(emojize("Add my own category :package:"), callback_data="new_category"),
        InlineKeyboardButton(emojize("Information :information:"), callback_data="info")
    ],
    [InlineKeyboardButton(emojize("End :stop_sign:"), callback_data="end"),],
]
welcome_keyboard_markup = InlineKeyboardMarkup(welcome_keyboard)

# Keyboard for choosing type of item that user's adding.
types_keyboard = [
    [
        InlineKeyboardButton(emojize("Film :cinema:"), callback_data="cinema"),
        InlineKeyboardButton(
            emojize("Paper :page_with_curl:"), callback_data="page_with_curl"
        ),
        InlineKeyboardButton(emojize("Book :books:"), callback_data="books"),
    ],
    [InlineKeyboardButton(emojize("Cancel :cross_mark:"), callback_data="cross_mark")],
]
types_keyboard_markup = InlineKeyboardMarkup(types_keyboard)

# Keyboard for user to choose which type of items to get from database.
get_types_keyboard = [
    [
        InlineKeyboardButton(emojize("Film :cinema:"), callback_data="cinema"),
        InlineKeyboardButton(
            emojize("Paper :page_with_curl:"), callback_data="page_with_curl"
        ),
        InlineKeyboardButton(emojize("Book :books:"), callback_data="books"),
    ],
    [
        InlineKeyboardButton(
            emojize("Mix :person_shrugging:"), callback_data="person_shrugging"
        ),
        InlineKeyboardButton(
            emojize("Cancel :cross_mark:"), callback_data="cross_mark"
        ),
    ],
]
get_types_keyboard_markup = InlineKeyboardMarkup(get_types_keyboard)


# Keyboard for confirmation of exit from the conversation with bot.
end_confirmation_keyboard = [
    [
        InlineKeyboardButton(emojize("End :stop_sign:"), callback_data="end"),
        InlineKeyboardButton(
            emojize("To beginning :right_arrow_curving_left:"),
            callback_data="to_beginning",
        ),
    ],
]
end_confirmation_keyboard_markup = InlineKeyboardMarkup(end_confirmation_keyboard)
