from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler, Updater, MessageHandler, Filters, CommandHandler

from work_with_db import init_db, create_user, add_move, get_statistics, add_win, get_users_stat
from game_engine import comp_move, space_is_free, check_game_over, clear_field, game_engine

from settings import is_prod, get_tg_token, get_id_admin
from work_with_keyboards import get_keyboard

USER_SYMB = "X"
COMP_SYMB = "0"
EMPTY_SYMB = "-"

USER_WIN = 'user'
COMP_WIN = 'comp'
DRAW = 'draw'
PLAY = 'play'


def add_user(user):
    # Добавить пользователя
    if user:
        name = user.first_name
    else:
        name = 'anonim'
    create_user(user_id=user.id, user_name=name)


def message_handler(update: Update, context: CallbackContext):
    """
    Функция ловит все сообщения пользователя

    :param update:
    :param context:
    :return:
    """

    # Добавить пользователя
    user = update.effective_user
    add_user(user)

    if check_game_over(user_id=user.id) == PLAY:
        keyboard = get_keyboard(user.id)
        reply_text = f'Крестики-нолики'
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
    """

    user = update.effective_user
    add_user(update.effective_user)
    callback_data = update.callback_query.data

    if callback_data.isnumeric():
        text, is_game_over = game_engine(cell_num=int(callback_data), user_id=user.id)

        keyboard = get_keyboard(user_id=user.id, is_game_over=is_game_over)
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    elif callback_data == 'restart':
        restart(update=update, context=context)


def restart(context: CallbackContext, update: Update):
    """
    Функция очищает поле и создаёт новую игру
    """
    user_id = int(update["callback_query"]["message"]["chat"]["id"])
    clear_field(user_id)
    context.bot.send_message(chat_id=user_id,
                             text="Новая игра",
                             reply_markup=get_keyboard(user_id=user_id))


def is_admin(update: Update):
    return update.effective_user.id == get_id_admin()


def new_game(update, context):
    user_id = int(update["message"]["chat"]["id"])
    clear_field(user_id)
    update.message.reply_text(text=f'Новая игра',
                              reply_markup=get_keyboard(user_id=user_id))


def show_stat(update, context):
    if is_admin(update):
        users_stat = get_users_stat()
        msg_txt = '\n'.join([f'{user_name} - {user_win} : {comp_win}.  {points} points.'
                             for user_name, user_win, comp_win, points in users_stat])

        update.message.reply_text(
            text=f'{msg_txt}\n\n/stat — показать статистику'
        )


def main():
    print('Startanuli')
    updater = Updater(
        token=get_tg_token(), use_context=True
    )

    # Подключаемся к СУБД
    if is_prod():
        force = False
    else:
        force = False
    init_db(force=force)

    # Навесить обработчики команд
    updater.dispatcher.add_handler(CommandHandler("stat", show_stat))
    updater.dispatcher.add_handler(CommandHandler("new_game", new_game))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, message_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))

    # Начать бесконечную обработку входящих сообщений
    updater.start_polling()
    updater.idle()
    # logger.info('Stop bot')


if __name__ == '__main__':
    main()
