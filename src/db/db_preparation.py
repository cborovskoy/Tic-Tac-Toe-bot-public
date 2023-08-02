import sqlite3
from pathlib import PurePath, Path
from src.config import load_config


def ensure_connection(func):
    """ Декоратор для подключения к СУБД: открывает соединение,
        выполняет переданную функцию и закрывает за собой соединение.
        Потокобезопасно!
    """

    def inner(*args, **kwargs):
        config_path = PurePath(Path(__file__).parents[2], 'bot.ini')
        config = load_config(config_path)
        base_path = ('../' if __name__ == '__main__' else '') + config.db.path

        with sqlite3.connect(base_path) as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force: bool = False):
    """ Проверить что нужные таблицы существуют, иначе создать их

        Важно: миграции на такие таблицы вы должны производить самостоятельно!

        :param conn: Подключение к СУБД
        :param force: Явно пересоздать все таблицы
    """
    c = conn.cursor()

    # Сообщения от пользователей
    if force:
        c.execute('DROP TABLE IF EXISTS user_message')

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
