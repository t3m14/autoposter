from config import CONFIG
from aiogram import Bot, Dispatcher
from aiogram import types
from bot.keyboards import inline_keyboards, reply_keyboards
from loguru import logger
from database.operations import create_config, get_config, add_source_public
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from userbot import load_app, parser
from bot.forward import start_parse
form_data = {}

class States(StatesGroup):
    start = State()
    public = State()
    source = State()
    private = State()
    phone = State()
    code = State()
async def start():
    logger.info("Запуск бота...")
    bot = Bot(token=CONFIG["BOT_TOKEN"])
    dp = Dispatcher(bot, storage=MemoryStorage())
    logger.info("Бот запущен!")
    first_message = 0
    app_data = ""
    @dp.message_handler(commands=["start"], state="*")
    async def start(message: types.Message):
        await message.answer("Привет!\n\n**Бот треша**\n рад вас приветствовать!\nЧтобы начать работу нажимите на любую из подходящих клавиш снизу!\n\nПриятного использования :)", reply_markup=reply_keyboards.main_menu_kb)
        await States.start.set()
    @dp.message_handler(state=States.start)
    async def keyboard_handler(message: types.Message):
        match message.text:
            case "Настройки":
                await message.answer("Выберите нужное", reply_markup=inline_keyboards.get_settings(message.from_user.id))
            case "Как пользоваться":
                await message.answer("По техническим вопросам работы бота писать @bvdtripp", reply_markup=inline_keyboards.close)
            case "Запустить бота":
                global form_data
                try:
                    await start_parse(form_data["private_public"], form_data["public_public"], form_data["source_publics"])
                except:
                    await message.answer("Сначала заполните настройки")
        try:
            await message.delete()
        except:pass
    @dp.callback_query_handler(state=States.start)
    async def inline_keyboard_handler(call: types.CallbackQuery):
        match call.data:
            case "close":
                await call.message.delete()
            case "channel_settings":
                global first_message
                first_message = call.message.message_id
                await call.message.answer("Введите АЙДИ СКРЫТОГО канала (НЕ ССЫЛКУ) айди можно узнать тут @getmyid_bot")
                await States.private.set()
            case "source_publics":
                first_message = call.message.message_id
                await call.message.answer("Отправьте АЙДИ каналов ИСТОЧНИКОВ с новой строки (НЕ ССЫЛКУ) айди можно узнать тут @getmyid_bot")
                await States.source.set()

    @dp.message_handler(state=States.phone)
    async def phone_enter(message: types.Message):
        global app_data
        application_data = await load_app.start(message.text)
        if (type(application_data) is dict):
            global first_message
            first_message = message.message_id
            app_data = application_data
            await message.answer("Вам должен прийти код, проверьте личные сообщения")
            await States.code.set()
            
        else:
            app = application_data
            global form_data
            try:
                await start_parse(form_data["private_public"], form_data["public_public"], form_data["source_publics"])
            except:
                await message.answer("Сначала заполните настройки")
            await States.start.set()
    @dp.message_handler(state=States.code)
    async def code_enter(message: types.Message):
        global app_data, form_data
        app = await load_app.authApp(app_data, message.text)
        try:
            if form_data["private_public"] != "" &  form_data["public_public"] != "" & form_data["source_publics"] != "":
                await parser.start_parse(app, form_data["private_public"], form_data["public_public"], form_data["source_publics"])
            global first_message
            
            await message.answer("Бот запущен, проверьте каналы\nА так же добавьте в качестве админа @testingbot52bot")
        except:
            await message.answer("Сначала заполните настройки")
        await States.start.set()

    @dp.message_handler(state=States.source)
    async def source_enter(message: types.Message):
        source_publics = []
        if ('\n') in message.text:
            for text in message.text.split('\n'):
                if (text.lstrip('-').isdigit()):
                    if text not in source_publics:
                        source_publics.append(text)
                else:
                    try:
                        await message.delete()
                    except:pass
            form_data["source_publics"] = source_publics
            global first_message
            while first_message < message.message_id:
                try:
                    await bot.delete_message(message.chat.id, first_message)
                except:pass
                first_message+=1
            try:
                await message.delete()
            except:pass
            await message.answer("Ответы записаны, спасибо!)", reply_markup=inline_keyboards.close)
            await States.start.set()
        else:
            try:
                await message.delete()
            except:pass        
    @dp.message_handler(state=States.private)
    async def private_enter(message: types.Message):
        if (message.text.lstrip('-').isdigit()):
            form_data["private_public"] = message.text.strip()
            await message.answer("Спасибо, теперь АЙДИ ПУБЛИЧНОГО канала (НЕ ССЫЛКУ) айди можно узнать тут @getmyid_bot")
            await States.public.set()
        else:
            try:
                await message.delete()
            except:pass

    @dp.message_handler(state=States.public)
    async def public_enter(message: types.Message):
        if (message.text.lstrip('-').isdigit()):
            form_data["public_public"] = message.text.strip()
            await message.answer("Ответы записаны, спасибо!)", reply_markup=inline_keyboards.close)
            await States.start.set()
            global first_message
            while first_message < message.message_id:
                await bot.delete_message(message.chat.id, first_message)
                first_message+=1
            try:
                await message.delete()
            except:pass
        else:
            try:
                await message.delete()
            except:pass
    await dp.start_polling(bot)
    

#hhfdssaqq
#qqq111c
#FFFwwew