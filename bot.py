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
        docs = parse_matlab()
        if len(docs) == 0:
            truncate_documents()
            for url, content in docs.items():
                add_document(content, url)
            await message.answer('qq')


@dp.message_handler()
async def echo(message: types.Message):
    query = message.text
    r = get_documents()
    if r.success:
        result = search_documents(documents=r.data, query=query, max_result_document_count=-1)
        await message.answer('\n'.join(result))
    else:
        await message.answer('гг вп')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
