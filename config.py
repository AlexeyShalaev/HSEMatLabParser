from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    admins: list


@dataclass
class DbConfig:
    conn: str  # connection string to database


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admins=env.str("ADMIN_TOKENS").split(',')
        ),
        db=DbConfig(
            conn=env.str('DB_CONN')
        ),
    )
