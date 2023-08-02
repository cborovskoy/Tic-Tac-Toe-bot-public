from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from src.config import load_config
from src.db.sqlite_db import create_user, get_users_stat, get_field
from src.keyboards.main_kb import get_keyboard
from src.service.game_engine import clear_field

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    user = message.from_user
    user_name = user.first_name if user.first_name is not None and len(user.first_name) > 0 else f'id{user.id}'
    create_user(user_id=user.id, user_name=user_name)


@router.message(Command("new_game"))
async def cmd_new_game(message: Message):
    user_id = message.from_user.id
    clear_field(user_id)
    kb = get_keyboard(field=get_field(user_id=user_id))
    await message.answer(text='Новая игра', reply_markup=kb)


@router.message((F.text == '/stat') & (F.from_user.id.in_(set(load_config().tg_bot.admin_ids))))
async def cmd_stat(message: Message):
    msg_txt = '\n'.join([f'{user_name} - {user_win} : {comp_win}.  {points} points.'
                         for user_name, user_win, comp_win, points in get_users_stat()])
    await message.answer(text=msg_txt)
