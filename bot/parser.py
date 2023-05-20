from pyrogram import Client, filters, idle
from database.operations import create_post, get_post
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CONFIG
from loguru import logger
async def start_parse(application: Client, private_public: str, public_public: str, source_publics: dict):
    app = application
    logger.info("Приложение запущено!")

    @app.on_message(filters=filters.chat(source_publics))
    async def new_channel_post(client, message):
        logger.info("Новый пост")
        create_post(username=message.chat.username, message_id=message.id)
        post_id = get_post(message_id=message.id).message_id
        
        await message.forward(private_public)
        await client.send_message(private_public, post_id)
        logger.info("Сообщение переслано")
    @app.on_message(filters=filters.chat(private_public) & filters.regex(r'\d+\+'))
    async def post_request(client, message):
        post_id = str(message.text).split("+")[0].strip()
        post = get_post(message_id=post_id)
        msg = await app.get_messages(post.username, post.message_id)
        await msg.copy(public_public)
        await app.send_message(private_public, "Пост успешно опубликован!")
    await idle()
    await app.stop()