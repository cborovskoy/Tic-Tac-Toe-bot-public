import sqlite3

WIN_POINTS = 10
LOSE_POINTS = -12


def ensure_connection(func):
    """ Декоратор для подключения к СУБД: открывает соединение,
        выполняет переданную функцию и закрывает за собой соединение.
        Потокобезопасно!
    """

    def inner(*args, **kwargs):
        with sqlite3.connect('anketa.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force: bool = False):
    """ Проверить что нужные таблицы существуют, иначе создать их

        Важно: миграции на такие таблицы вы должны производить самостоятельно!

        :param conn: подключение к СУБД
        :param force: явно пересоздать все таблицы
    """
    c = conn.cursor()

    # Информация о пользователе
    #TODO: создать при необходимости...

    # Сообщения от пользователей
    if force:
        c.execute('DROP TABLE IF EXISTS user_message')
    # TODO: Разобраться, почему всё это подсвечивается жёлтым

    c.execute('''
        CREATE TABLE IF NOT EXISTS user_message (
            id          INTEGER PRIMARY KEY,
            user_id     INTEGER,
            user_name   TEXT,
            user_win    INTEGER DEFAULT 0,
            comp_win    INTEGER DEFAULT 0,
            points      INTEGER DEFAULT 0,
            cell_1      TEXT DEFAULT "-",
            cell_2      TEXT DEFAULT "-",
            cell_3      TEXT DEFAULT "-",
            cell_4      TEXT DEFAULT "-",
            cell_5      TEXT DEFAULT "-",
            cell_6      TEXT DEFAULT "-",
            cell_7      TEXT DEFAULT "-",
            cell_8      TEXT DEFAULT "-",
            cell_9      TEXT DEFAULT "-",
            UNIQUE(user_id)
        )
    ''')
    # Сохранить изменения
    conn.commit()


@ensure_connection
def create_user(conn, user_id: int, user_name: str = "anonim"):
    # TODO: Записывать имя пользователя
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
