from services.MongoDB.models.document import *
from . import db, MongoDBResult

"""
Это собственно-написанная ORM - для NoSql базы данных MongoDB, для взаимодействия с моделью Document
Документ: documents
"""


def get_documents() -> MongoDBResult:
    res = db.documents.find()
    if res:
        documents = []
        for i in list(res):
            documents.append(Document(i))
        return MongoDBResult(True, documents)
    else:
        return MongoDBResult(False, [])


def add_document(content, url):
    db.documents.insert_one({
        "content": content,
        "url": url
    })


def add_documents(documents):
    db.documents.insert_many(documents)


# очистка Документа
def truncate_documents():
    db.documents.drop()
