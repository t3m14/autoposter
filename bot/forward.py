
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import IDFilter
import asyncio
from database.operations import create_post, get_post
from loguru import logger
Private_public = ""
Public_public = ""
Source_publics = []
bot= Bot (token="6129108105:AAE2fQ8FKSXJUDWVn1PkJ73QMB78yPk4J5c")
dp= Dispatcher(bot)
@dp.channel_post_handler()
async def start(message: types.Message):
    print(message.text)
    if message.chat_id in Source_publics:
        logger.info("Новый пост")
        create_post(username=message.chat.username, message_id=message.id)
        post_id = get_post(message_id=message.id).message_id
        
        await message.forward(Private_public)
        await bot.send_message(Private_public, post_id)
        
        logger.info("Сообщение переслано")

@dp.channel_post_handler()
async def start(message: types.Message):
    if message.chat.id == Private_public:
        if message.text[-1] == "+":
            post_id = str(message.text).split("+")[0].strip()
            post = get_post(message_id=post_id)
            await bot.copy_message(Public_public, Private_public, post.message_id)
            await bot.send_message(Private_public, "Пост успешно опубликован!")
            await dp.start_polling(bot)
async def run(): 
    print("Второй бот запущен")
    await dp.start_polling(bot)
async def start_parse(private_public: str, public_public: str, source_publics: dict):
    global Private_public, Public_public, Source_publics
    Private_public = private_public
    Public_public = public_public
    Source_publics = source_publics
    await run()