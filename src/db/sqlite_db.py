from src.config import LOSE_POINTS, WIN_POINTS
from src.db.db_preparation import ensure_connection


@ensure_connection
def create_user(conn, user_id: int, user_name: str):
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO user_message (user_id, user_name) VALUES (?, ?)', (user_id, user_name))
    conn.commit()


@ensure_connection
def add_move(conn, user_id: int, cell: int, symb: str):
    """
    Записываем ход
    :param conn: подключение к СУБД
    :param user_id: id пользователя
    :param cell: номер ячейки
    :param symb: игрок, Пусто = 0, X = 1, 0 = 2
    """

    c = conn.cursor()
    c.execute(f'UPDATE user_message SET cell_{cell} = "{symb}" WHERE user_id = {user_id}')
    conn.commit()


@ensure_connection
def get_field(conn, user_id: int):
    """
    Функция возвращает массив со значениями в ячейке

    :param conn:
    :param user_id: id пользователя
    :return: Возвращает символ записанный в ячейке
    """

    c = conn.cursor()

    field = []
    for i in range(1, 10):
        cell_content = c.execute(f'SELECT cell_{i} FROM user_message WHERE user_id = {user_id}')
        field.append(cell_content.fetchone()[0])

    return field


@ensure_connection
def get_statistics(conn, user_id: int):
    """
    Функция возвращает строку со статистикой побед и поражений

    :param conn:
    :param user_id:
    :return: строка со статистикой побед и поражений
    """
    c = conn.cursor()
    c.execute('SELECT points FROM user_message WHERE user_id = ? ORDER BY id DESC LIMIT ?', (user_id, 1))
    (points,) = c.fetchone()

    c.execute('SELECT points FROM user_message ORDER BY points DESC LIMIT 1')
    (leader_points,) = c.fetchone()

    return f"\n\nВаш счёт: {points} очков\nУ лидера: {leader_points} очков"


@ensure_connection
def add_win(conn, user_id: int, who_is_win: str):
    c = conn.cursor()

    c.execute('SELECT points FROM user_message WHERE user_id = ? ORDER BY id DESC LIMIT ?', (user_id, 1))
    (points,) = c.fetchone()

    if who_is_win == "user":
        c.execute('SELECT user_win FROM user_message WHERE user_id = ? ORDER BY id DESC LIMIT ?', (user_id, 1))
        (counter_user_win,) = c.fetchone()
        counter_user_win += 1
        c.execute('UPDATE user_message SET user_win = ? WHERE user_id = ?', (counter_user_win, user_id))

        points += WIN_POINTS
        c.execute('UPDATE user_message SET points = ? WHERE user_id = ?', (points, user_id))

    elif who_is_win == "comp":
        c.execute('SELECT comp_win FROM user_message WHERE user_id = ? ORDER BY id DESC LIMIT ?', (user_id, 1))
        (counter_comp_win,) = c.fetchone()
        counter_comp_win += 1
        c.execute('UPDATE user_message SET comp_win = ? WHERE user_id = ?', (counter_comp_win, user_id))

        points += LOSE_POINTS
        c.execute('UPDATE user_message SET points = ? WHERE user_id = ?', (points, user_id))

    conn.commit()


@ensure_connection
def get_users_stat(conn):
    """
    Функция функция показывает последнии сообщения пользователя
    :param conn:
    :return:
    """

    c = conn.cursor()
    c.execute('SELECT user_name, user_win, comp_win, points  FROM user_message LIMIT 80')

    return c.fetchall()
