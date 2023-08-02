from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from src.db.sqlite_db import get_field
from src.keyboards.main_kb import get_keyboard
from src.service.game_engine import check_game_over, PLAY, game_engine, clear_field

router = Router()


@router.message(~F.text.startswith('/'))
async def msg_handler(message: Message):
    user_id = message.from_user.id
    field = get_field(user_id=user_id)

    if check_game_over(user_id=user_id) == PLAY:
        keyboard = get_keyboard(field=field)
        reply_text = 'Крестики-нолики'
    else:
        keyboard = get_keyboard(field=field, is_game_over=True)
        reply_text = 'Игра окончена'

    # Ответить пользователю
    await message.answer(text=reply_text, reply_markup=keyboard)


@router.callback_query()
async def callback_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    callback_data = callback.data

    if callback_data.isnumeric():
        text, is_game_over = game_engine(cell_num=int(callback_data), user_id=user_id)
        kb = get_keyboard(field=get_field(user_id=user_id), is_game_over=is_game_over)
        await callback.message.edit_text(text=text, reply_markup=kb)
        await callback.answer()

    elif callback_data == 'restart':
        clear_field(user_id)
        kb = get_keyboard(field=get_field(user_id=user_id))
        await callback.bot.send_message(chat_id=user_id, text='Новая игра', reply_markup=kb)
        await callback.answer()
