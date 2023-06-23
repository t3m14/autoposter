from config import CONFIG
from aiogram import Bot, Dispatcher
from bot.handlers import button_handler, inline_handler, settings_form, user
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger
form_data = {}
first_message = 0
app_data = ""

async def start():
    logger.info("Запуск бота...")
    bot = Bot(token=CONFIG["BOT_TOKEN"])
    dp = Dispatcher(bot, storage=MemoryStorage())
    logger.info("Бот запущен!")

    user.register_user_handlers(dp=dp)
    button_handler.register_button_handler(dp=dp)
    inline_handler.register_inline_handlers(dp=dp)
    settings_form.register_form_handler(dp=dp)
   
    await dp.start_polling(bot)
    

#hhfdssaqq
#qqq111c
#FFFwwew