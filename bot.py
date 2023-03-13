import logging

from aiogram import Bot, Dispatcher, executor, types
from config import load_config
from services.MongoDB.documents import get_documents, add_document, truncate_documents
from services.parser import parse_matlab
from services.search_engine import search_documents

# Configure logging
logging.basicConfig(level=logging.INFO)

config = load_config(".env")
admin_tokens = config.tg_bot.admins

# Initialize bot and dispatcher
bot = Bot(token=config.tg_bot.token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['update'])
async def admin_update(message: types.Message):
    user_id = message.from_user.id
    if str(user_id) in admin_tokens:
        try:
            docs = parse_matlab()
            if len(docs) == 0:
                await message.answer(f'Не удалось обновить документы.')
            else:
                truncate_documents()
                for url, content in docs.items():
                    add_document(content, url)
                await message.answer(f'База обновлена. Добавлено {len(docs)} документов.')
        except Exception as ex:
            print(f'Ошибка:\n{ex}')


@dp.message_handler()
async def echo(message: types.Message):
    query = message.text
    r = get_documents()
    if r.success:
        docs = r.data
        result = search_documents(documents=docs, query=query, max_result_document_count=10)
        if len(result) == 0:
            await message.answer(f'По запросу ничего не найдено.')
        else:
            msg = f'По вашему запросу найдено {len(result)} работ:\n'
            for doc_id in result:
                for doc in docs:
                    if str(doc.id) == doc_id:
                        msg += f'[{doc.url.split("/")[-1]}]({doc.url})\n'
                        break
            await message.answer(msg, parse_mode=types.ParseMode.MARKDOWN)
    else:
        await message.answer('Не удалось получить данные из базы данных.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
