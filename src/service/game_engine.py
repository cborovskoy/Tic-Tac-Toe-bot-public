from src.db.sqlite_db import get_field, add_win, get_statistics, add_move

import random

EMPTY_SYMB = "-"
COMP_SYMB = "0"
USER_SYMB = "X"

USER_WIN = 'user'
COMP_WIN = 'comp'
DRAW = 'draw'
PLAY = 'play'


def comp_move(user_id: int):
    """
    Функция хода компьютера

    :param user_id:
    :return:
    """
    field = get_field(user_id=user_id)
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = field

    num_cell = 0

    # Проверка выйгрышных ходов

    if c5 == EMPTY_SYMB:
        num_cell = 5

    # Диагональ с символами компа
    elif c5 == c9 == COMP_SYMB and c1 == EMPTY_SYMB:
        num_cell = 1
    elif c1 == c9 == COMP_SYMB and c5 == EMPTY_SYMB:
        num_cell = 5
    elif c1 == c5 == COMP_SYMB and c9 == EMPTY_SYMB:
        num_cell = 9

    elif c5 == c7 == COMP_SYMB and c3 == EMPTY_SYMB:
        num_cell = 3
    elif c3 == c7 == COMP_SYMB and c5 == EMPTY_SYMB:
        num_cell = 5
    elif c3 == c5 == COMP_SYMB and c7 == EMPTY_SYMB:
        num_cell = 7

    # Строки с символами компа
    elif c2 == c3 == COMP_SYMB and c1 == EMPTY_SYMB:
        num_cell = 1
    elif c1 == c3 == COMP_SYMB and c2 == EMPTY_SYMB:
        num_cell = 2
    elif c1 == c2 == COMP_SYMB and c3 == EMPTY_SYMB:
        num_cell = 3

    elif c5 == c6 == COMP_SYMB and c4 == EMPTY_SYMB:
        num_cell = 4
    elif c4 == c6 == COMP_SYMB and c5 == EMPTY_SYMB:
        num_cell = 5
    elif c4 == c5 == COMP_SYMB and c6 == EMPTY_SYMB:
        num_cell = 6

    elif c8 == c9 == COMP_SYMB and c7 == EMPTY_SYMB:
        num_cell = 7
    elif c7 == c9 == COMP_SYMB and c8 == EMPTY_SYMB:
        num_cell = 8
    elif c7 == c8 == COMP_SYMB and c9 == EMPTY_SYMB:
        num_cell = 9

    # Столбцы с символами компа
    elif c4 == c7 == COMP_SYMB and c1 == EMPTY_SYMB:
        num_cell = 1
    elif c1 == c7 == COMP_SYMB and c4 == EMPTY_SYMB:
        num_cell = 4
    elif c1 == c4 == COMP_SYMB and c7 == EMPTY_SYMB:
        num_cell = 7

    elif c5 == c8 == COMP_SYMB and c2 == EMPTY_SYMB:
        num_cell = 2
    elif c2 == c8 == COMP_SYMB and c5 == EMPTY_SYMB:
        num_cell = 5
    elif c2 == c5 == COMP_SYMB and c8 == EMPTY_SYMB:
        num_cell = 8

    elif c6 == c9 == COMP_SYMB and c3 == EMPTY_SYMB:
        num_cell = 3
    elif c3 == c9 == COMP_SYMB and c6 == EMPTY_SYMB:
        num_cell = 6
    elif c3 == c6 == COMP_SYMB and c9 == EMPTY_SYMB:
        num_cell = 9


    # Строки с символами пользователя
    elif c2 == c3 == USER_SYMB and c1 == EMPTY_SYMB:
        num_cell = 1
    elif c1 == c3 == USER_SYMB and c2 == EMPTY_SYMB:
        num_cell = 2
    elif c1 == c2 == USER_SYMB and c3 == EMPTY_SYMB:
        num_cell = 3

    elif c5 == c6 == USER_SYMB and c4 == EMPTY_SYMB:
        num_cell = 4
    elif c4 == c6 == USER_SYMB and c5 == EMPTY_SYMB:
        num_cell = 5
    elif c4 == c5 == USER_SYMB and c6 == EMPTY_SYMB:
        num_cell = 6

    elif c8 == c9 == USER_SYMB and c7 == EMPTY_SYMB:
        num_cell = 7
    elif c7 == c9 == USER_SYMB and c8 == EMPTY_SYMB:
        num_cell = 8
    elif c7 == c8 == USER_SYMB and c9 == EMPTY_SYMB:
        num_cell = 9

    # Столбцы с символами пользователя
    elif c4 == c7 == USER_SYMB and c1 == EMPTY_SYMB:
        num_cell = 1
    elif c1 == c7 == USER_SYMB and c4 == EMPTY_SYMB:
        num_cell = 4
    elif c1 == c4 == USER_SYMB and c7 == EMPTY_SYMB:
        num_cell = 7

    elif c5 == c8 == USER_SYMB and c2 == EMPTY_SYMB:
        num_cell = 2
    elif c2 == c8 == USER_SYMB and c5 == EMPTY_SYMB:
        num_cell = 5
    elif c2 == c5 == USER_SYMB and c8 == EMPTY_SYMB:
        num_cell = 8

    elif c6 == c9 == USER_SYMB and c3 == EMPTY_SYMB:
        num_cell = 3
    elif c3 == c9 == USER_SYMB and c6 == EMPTY_SYMB:
        num_cell = 6
    elif c3 == c6 == USER_SYMB and c9 == EMPTY_SYMB:
        num_cell = 9

    # Диагональ с символами пользователя
    elif c5 == c9 == USER_SYMB and c1 == EMPTY_SYMB:
        num_cell = 1
    elif c1 == c9 == USER_SYMB and c5 == EMPTY_SYMB:
        num_cell = 5
    elif c1 == c5 == USER_SYMB and c9 == EMPTY_SYMB:
        num_cell = 9

    elif c5 == c7 == USER_SYMB and c3 == EMPTY_SYMB:
        num_cell = 3
    elif c3 == c7 == USER_SYMB and c5 == EMPTY_SYMB:
        num_cell = 5
    elif c3 == c5 == USER_SYMB and c7 == EMPTY_SYMB:
        num_cell = 7

    else:
        temp = True
        while temp:
            num_cell = random.randint(1, 9)
            # if get_cell(user_id=user_id, cell=num_cell) == EMPTY_SYMB:
            if get_field(user_id=user_id)[num_cell - 1] == EMPTY_SYMB:
                temp = False

    add_move(user_id=user_id, cell=num_cell, symb=COMP_SYMB)


def space_is_free(user_id: int, cell: int):
    """
    Функция проверяет ячейку на пустоту

    :param user_id:
    :param cell: номер ячейки
    :return:
    """
    is_cell_free = True
    # symb = get_cell(user_id=user_id, cell=cell)
    symb = get_field(user_id=user_id)[cell - 1]
    if symb != EMPTY_SYMB:
        is_cell_free = False
    return is_cell_free


def check_game_over(user_id: int):
    """
    Функция проверяет закончилась ли игра, и кто в ней выйграл
    :param user_id:
    :param update:
    :param context:
    :return:
    """

    win = PLAY

    field = get_field(user_id=user_id)
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = field

    if (
            c1 == c2 == c3 == USER_SYMB or c4 == c5 == c6 == USER_SYMB or c7 == c8 == c9 == USER_SYMB or
            c1 == c4 == c7 == USER_SYMB or c2 == c5 == c8 == USER_SYMB or c3 == c6 == c9 == USER_SYMB or
            c1 == c5 == c9 == USER_SYMB or c3 == c5 == c7 == USER_SYMB):
        win = USER_WIN
    elif (
            c1 == c2 == c3 == COMP_SYMB or c4 == c5 == c6 == COMP_SYMB or c7 == c8 == c9 == COMP_SYMB or
            c1 == c4 == c7 == COMP_SYMB or c2 == c5 == c8 == COMP_SYMB or c3 == c6 == c9 == COMP_SYMB or
            c1 == c5 == c9 == COMP_SYMB or c3 == c5 == c7 == COMP_SYMB):
        win = COMP_WIN

    elif (c1 != EMPTY_SYMB and c2 != EMPTY_SYMB and c3 != EMPTY_SYMB and c4 != EMPTY_SYMB and c5 != EMPTY_SYMB and
          c6 != EMPTY_SYMB and c7 != EMPTY_SYMB and c8 != EMPTY_SYMB and c9 != EMPTY_SYMB):
        win = DRAW

    return win


def clear_field(user_id: int):
    for i in range(1, 10):
        add_move(user_id=user_id, cell=i, symb=EMPTY_SYMB)


def game_engine(cell_num: int, user_id):
    """
    В этой функции находится большинство игровой логики
    """

    text = 'Новая игра'
    check_is_game_over = False

    if check_game_over(user_id=user_id) == PLAY:
        if space_is_free(user_id=user_id, cell=cell_num):

            add_move(user_id=user_id, cell=cell_num, symb=USER_SYMB)

            if check_game_over(user_id=user_id) == PLAY:
                comp_move(user_id=user_id)

            # Проверки состояния игры
            if check_game_over(user_id=user_id) == PLAY:
                text = f"Нажата кнопка {cell_num}"

            elif check_game_over(user_id=user_id) == USER_WIN:
                add_win(user_id=user_id, who_is_win="user")
                text = '🥳 Вы победили\n📈 +10 очков' + get_statistics(user_id=user_id)
                check_is_game_over = True

            elif check_game_over(user_id=user_id) == COMP_WIN:
                add_win(user_id=user_id, who_is_win="comp")
                text = '🤖 Победил компьютер\n📉 –12 очков' + get_statistics(user_id=user_id)
                check_is_game_over = True

            elif check_game_over(user_id=user_id) == DRAW:
                text = '🤝 Ничья' + get_statistics(user_id=user_id)
                check_is_game_over = True
        else:
            if check_game_over(user_id=user_id) == PLAY:
                text = f"Клетка {cell_num} занята"
    else:
        text = "Игра закончена"
        check_is_game_over = True

    return [text, check_is_game_over]

# if __name__ == '__main__':
#     main()
