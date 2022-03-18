from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from work_with_db import get_field

def get_keyboard(user_id: int = 0, is_game_over=False):
    """
    Создаём обычную клавиатуру

    :param user_id:
    :return: Возвращаем обычную клавиатуру
    """

    field = get_field(user_id=user_id)
    inline_keyboard = [
        [
            InlineKeyboardButton(text=field[0], callback_data='1'),
            InlineKeyboardButton(text=field[1], callback_data='2'),
            InlineKeyboardButton(text=field[2], callback_data='3'),
        ],
        [
            InlineKeyboardButton(text=field[3], callback_data='4'),
            InlineKeyboardButton(text=field[4], callback_data='5'),
            InlineKeyboardButton(text=field[5], callback_data='6'),
        ],
        [
            InlineKeyboardButton(text=field[6], callback_data='7'),
            InlineKeyboardButton(text=field[7], callback_data='8'),
            InlineKeyboardButton(text=field[8], callback_data='9'),
        ],
    ]

    if is_game_over:
        inline_keyboard.append([InlineKeyboardButton(text="restart", callback_data='restart')])

    return InlineKeyboardMarkup(inline_keyboard)