from telegram import Update
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.ext import CallbackQueryHandler
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CommandHandler

from cXO_db import init_db
from cXO_db import create_user
from cXO_db import add_move
from cXO_db import get_field
from cXO_db import get_statistics
from cXO_db import add_win
from cXO_db import get_users_stat

from cXO_GameEngine import comp_move
from cXO_GameEngine import space_is_free
from cXO_GameEngine import check_game_over, clear_field

from settings import is_prod

TG_TOKEN_TEST = ""
TG_TOKEN_PROD = ""
ADMIN_ID = 0

BTN_1 = '1'
BTN_2 = '2'
BTN_3 = '3'
BTN_4 = '4'
BTN_5 = '5'
BTN_6 = '6'
BTN_7 = '7'
BTN_8 = '8'
BTN_9 = '9'
RESTART = 'restart'

USER_SYMB = "X"
COMP_SYMB = "0"
EMPTY_SYMB = "-"

USER_WIN = 'user'
COMP_WIN = 'comp'
DRAW = 'draw'
PLAY = 'play'


def get_keyboard(user_id: int = 0, is_game_over=False):
    """
    Создаём обычную клавиатуру

    :param user_id:
    :return: Возвращаем обычную клавиатуру
    """

    field = get_field(user_id=user_id)
    inline_keyboard = [
        [
            InlineKeyboardButton(text=field[0], callback_data=BTN_1),
            InlineKeyboardButton(text=field[1], callback_data=BTN_2),
            InlineKeyboardButton(text=field[2], callback_data=BTN_3),
        ],
        [
            InlineKeyboardButton(text=field[3], callback_data=BTN_4),
            InlineKeyboardButton(text=field[4], callback_data=BTN_5),
            InlineKeyboardButton(text=field[5], callback_data=BTN_6),
        ],
        [
            InlineKeyboardButton(text=field[6], callback_data=BTN_7),
            InlineKeyboardButton(text=field[7], callback_data=BTN_8),
            InlineKeyboardButton(text=field[8], callback_data=BTN_9),
        ],
    ]

    if is_game_over:
        inline_keyboard.append([InlineKeyboardButton(text="restart", callback_data=RESTART)])

    return InlineKeyboardMarkup(inline_keyboard)


def message_handler(update: Update, context: CallbackContext):
    """
    Функция ловит все сообщения пользователя

    :param update:
    :param context:
    :return:
    """

    # Добавить пользователя
    user = update.effective_user

    if user:
        name = user.first_name
    else:
        name = 'anonim'

    create_user(user_id=user.id, user_name=name)

    reply_text = f'Крестики-нолики'

    if check_game_over(user_id=user.id) == PLAY:
        keyboard = get_keyboard(user.id)
    else:
        keyboard = get_keyboard(user_id=user.id, is_game_over=True)
        reply_text = "Игра окончена"

    # Ответить пользователю
    update.message.reply_text(
        text=reply_text,
        reply_markup=keyboard,
    )


def callback_handler(update: Update, context: CallbackContext):
    """
    Функция ловит все нажатия на кнопки
    :param update:
    :param context:
    :return:
    """

    user = update.effective_user

    if user:
        name = user.first_name
    else:
        name = 'anonim'

    create_user(user_id=user.id, user_name=name)

    callback_data = update.callback_query.data

    btn_num = None

    if callback_data == BTN_1:
        btn_num = 1

    elif callback_data == BTN_2:
        btn_num = 2

    elif callback_data == BTN_3:
        btn_num = 3

    elif callback_data == BTN_4:
        btn_num = 4

    elif callback_data == BTN_5:
        btn_num = 5

    elif callback_data == BTN_6:
        btn_num = 6

    elif callback_data == BTN_7:
        btn_num = 7

    elif callback_data == BTN_8:
        btn_num = 8

    elif callback_data == BTN_9:
        btn_num = 9

    elif callback_data == RESTART:
        do_restart(update=update, context=context)

    if btn_num:
        game_engine(cell_num=btn_num, update=update, context=context)


def game_engine(cell_num: int, update: Update, context: CallbackContext):
    """
    В этой функции находится большинство игровой логики

    :param user_id: id пользователя
    :param cell_num: Номер ячейки
    :param is_move: Это ход?
    :param update:
    :param context:
    :return:
    """

    user_id = update.effective_user.id

    text = 'Крестики-нолики'
    keyboard = get_keyboard(user_id=user_id)

    if check_game_over(user_id=user_id) == PLAY:
        if space_is_free(user_id=user_id, cell=cell_num):

            add_move(user_id=user_id, cell=cell_num, symb=USER_SYMB)
            if check_game_over(user_id=user_id) == PLAY:
                comp_move(user_id=user_id)

            # Проверки состояния игры
            if check_game_over(user_id=user_id) == PLAY:
                keyboard = get_keyboard(user_id=user_id)
                text = f"Нажата кнопка {cell_num}"
            elif check_game_over(user_id=user_id) == USER_WIN:
                add_win(user_id=user_id, who_is_win="user")
                text = 'Вы победили, +10 очков' + get_statistics(user_id=user_id)
                keyboard = get_keyboard(user_id=user_id, is_game_over=True)
            elif check_game_over(user_id=user_id) == COMP_WIN:
                add_win(user_id=user_id, who_is_win="comp")
                text = 'Победил компьютер, -12 очков' + get_statistics(user_id=user_id)
                keyboard = get_keyboard(user_id=user_id, is_game_over=True)
            elif check_game_over(user_id=user_id) == DRAW:
                text = 'Ничья' + get_statistics(user_id=user_id)
                keyboard = get_keyboard(user_id=user_id, is_game_over=True)

        else:
            if check_game_over(user_id=user_id) == PLAY:
                text = f"Клетка {cell_num} занята"
                keyboard = get_keyboard(user_id=user_id)
    else:
        text = "Игра закончена"
        keyboard = get_keyboard(user_id=user_id, is_game_over=True)

    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)


def do_restart(context: CallbackContext, update: Update):
    """
    Функция очищает поле и создаёт новую игру

    :param context:
    :param update:
    :return:
    """

    user_id = None
    try:
        user_id = int(context["message"]["chat"]["id"])
    except:
        pass

    try:
        user_id = int(update["callback_query"]["message"]["chat"]["id"])
    except:
        pass

    print(user_id)

    clear_field(user_id)

    text = "Новая игра"
    keyboard = get_keyboard(user_id=user_id)

    context.bot.send_message(chat_id = user_id, text=text, reply_markup=keyboard)


def is_admin(update: Update):
    if update.effective_user.id == ADMIN_ID:
        return True
    else:
        return False


def show_stat(update, context):
    print('зашли в стат')
    if is_admin(update):
        users_stat = get_users_stat()
        msg_txt = '\n'.join([f'{user_name} - {user_win} : {comp_win}.  {points} points.'
                             for user_name, user_win, comp_win, points in users_stat])

        update.message.reply_text(
            text=f'{msg_txt}\n\n/stat — показать статистику'
        )


def main():
    if is_prod():
        tg_token = TG_TOKEN_PROD
        force = True
    else:
        tg_token = TG_TOKEN_TEST
        force = False

    updater = Updater(
        token=tg_token, use_context=True
    )
    print('Startanuli')

    # Подключаемся к СУБД
    init_db(force=force)

    # Навесить обработчики команд
    updater.dispatcher.add_handler(CommandHandler("restart", do_restart))
    updater.dispatcher.add_handler(CommandHandler("stat", show_stat))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, message_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))

    # Начать бесконечную обработку входящих сообщений
    updater.start_polling()
    updater.idle()
    # logger.info('Stop bot')


if __name__ == '__main__':
    main()
