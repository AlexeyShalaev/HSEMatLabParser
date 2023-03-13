from dataclasses import dataclass

from bson import ObjectId


@dataclass
class Document:
    id: ObjectId  # ID курса
    content: str  # контент
    url: str  # ссылка на работу

    def __init__(self, data):
        self.id = data['_id']
        self.content = data['content']
        self.url = data['url']
