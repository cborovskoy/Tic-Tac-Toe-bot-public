from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder


def get_keyboard(field, is_game_over=False):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=field[0], callback_data='1'),
                InlineKeyboardButton(text=field[1], callback_data='2'),
                InlineKeyboardButton(text=field[2], callback_data='3'))
    builder.row(InlineKeyboardButton(text=field[3], callback_data='4'),
                InlineKeyboardButton(text=field[4], callback_data='5'),
                InlineKeyboardButton(text=field[5], callback_data='6'))
    builder.row(InlineKeyboardButton(text=field[6], callback_data='7'),
                InlineKeyboardButton(text=field[7], callback_data='8'),
                InlineKeyboardButton(text=field[8], callback_data='9'))

    if is_game_over:
        builder.row(InlineKeyboardButton(text="restart", callback_data='restart'))

    return builder.as_markup()
