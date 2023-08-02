import os
from dataclasses import dataclass
from pathlib import PurePath, Path
import configparser

WIN_POINTS = 10
LOSE_POINTS = -12


@dataclass
class DbConfig:
    path: str
    # host: str
    # password: str
    # user: str
    # database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list
    # use_redis: bool


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def __is_prod():
    if 'OS' in os.environ and os.environ['OS'] == 'Windows_NT':
        return False
    else:
        return True


def load_config(path=None):
    path = PurePath(Path(__file__).parents[1], 'bot.ini') if path is None else path

    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["test" if __is_prod else "prod"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot.get("tg_token"),
            admin_ids=list(map(int, tg_bot.get("admins").split(',')))
        ),
        db=DbConfig(path=tg_bot.get("base_path")),
    )
