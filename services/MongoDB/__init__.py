import logging
from dataclasses import dataclass

from pymongo import MongoClient

from config import load_config

config = load_config()  # config
logger = logging.getLogger(__name__)  # logging

db = MongoClient(config.db.conn).hse_matlab  # hse_matlab - название БД

logger.info('Database engine inited')


@dataclass
class MongoDBResult:
    # Класс для возврата данных
    success: bool
    data: ...
