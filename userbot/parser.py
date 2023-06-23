from pyrogram import Client, filters, idle
from database import operations
from loguru import logger
from config import CONFIG
import re

async def start_parse():
    application = Client(name="89292394343",
                         api_id=CONFIG["API_ID"], api_hash=CONFIG["API_HASH"])
    try:
        await application.start()
    except:
        pass

    logger.info("Приложение запущено!")

    async def join_all_chats():
        try:
            for source in operations.get_all_sources():
                await application.join_chat(source)
                logger.info("Joined into " + source)
            for public in operations.get_all_publis():
                await application.join_chat(public)
                logger.info("Joined into " + public)
            for private in operations.get_all_privates():
                await application.join_chat(private)
                logger.info("Joined into " + private)
        except Exception as e:
            logger.error(e.with_traceback)
    await join_all_chats()
    async def private_forwarding(message):
        operations.create_post(
            username=message.chat.username, message_id=message.id)
        privates = operations.get_all_privates_by_source(
            username=message.chat.username)
        for private in privates:
            private = await application.get_chat(private)
            await message.forward(private.id)
            await application.send_message(private.id, message.id)
        logger.info("Сообщение переслано")
    async def public_forwarding(message):
        post_id = str(message.text).split("+")[0].strip()
        print(post_id)
        post = operations.get_post(message_id=post_id)
        msg = await application.get_messages(post.username, post.message_id)
        publics = operations.get_all_publics_by_source(post.username)
        for public in publics:
            public = await application.get_chat(public)
            await msg.copy(public.id)
            await application.send_message(message.chat.id, "Пост успешно опубликован!")
    @application.on_message()
    async def new_channel_post(client, message):
        sources = operations.get_all_sources()
        if message.chat.username in sources:
            await join_all_chats()
            await private_forwarding(message=message)
        privates = operations.get_all_privates()
        if message.chat.username in privates:
            print("private")
            if re.match('\d+\+', message.text):
                await public_forwarding(message=message)
    
    await idle()
    await application.stop()
