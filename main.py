from database.operations import init_database
import dotenv, os, json
from config import CONFIG
import asyncio
from userbot import load_app, parser
from bot.bot import start
from loguru import logger
from pyrogram.client import Client

def load_config():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        dotenv.load_dotenv(dotenv_path)
    CONFIG["API_HASH"] = os.environ.get("API_HASH")
    CONFIG["API_ID"] = os.environ.get("API_ID")
    CONFIG["BOT_TOKEN"] = os.environ.get("BOT_TOKEN")
    CONFIG["BOT_TOKEN2"] = os.environ.get("BOT_TOKEN2")
    CONFIG["ADMIN_IDS"] = json.loads(os.environ.get("ADMIN_IDS"))
    logger.info("Конфиг загружен")
async def run():
    # app_data = await load_app.start("89292394343")
    # if (type(app_data) is dict):
    #     code = input("Code: ")
    #     app = await load_app.authApp(app_data, code)
    # else:
    #     app = app_data
    # await parser.start_parse(app, "hhfdssaqq", "qqq111c", ["FFFwwew"])
    await start()
if __name__ == "__main__":
    # Загружаем переменные окружения в конфиг
    load_config()
    # Инициализруем базу данных
    init_database()
    asyncio.run(run())
    

    
