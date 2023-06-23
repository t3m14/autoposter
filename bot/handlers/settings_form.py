from aiogram import Dispatcher, Bot, types
from bot.states.states import States
from bot.keyboards import inline_keyboards
from config import CONFIG
from loguru import logger
from database import operations
bot = Bot
form_data = {}
delete_counter = 0
async def source_enter(message: types.Message):
    source_publics = []
    if ('\n') in message.text:
        
        for text in message.text.split('\n'):
            if text not in source_publics:
                if ("/" in text):
                    text = text.split("/")[-1]
                source_publics.append(text)
            else:
                try:
                    await message.delete()
                except:pass
        form_data["source_publics"] = source_publics
        
        operations.add_source_public(user_id=message.from_user.id, source_publics=source_publics)
        await message.answer("Ответы записаны, спасибо!)", reply_markup=inline_keyboards.close)
        await States.start.set()
    else:
        try:
            await message.delete()
        except:pass        

async def private_enter(message: types.Message):
    if (message.text):
        text = message.text.strip()
        try:
            text = text.split("/")[1]
        except:pass
        operations.add_private_public(user_id=message.from_user.id, private_public_id=text.strip())
        await message.answer("Спасибо, теперь ссылку или юзернейм ПУБЛИЧНОГО канала \n Сюда переслылаются уже одобренные посты, без указания авторства из СКРЫТОГО канала.")
        await States.public.set()
    else:
        try:
            await message.delete()
        except:pass

async def public_enter(message: types.Message):
    if (message.text):
        text = message.text.strip()
        try:
            text = text.split("/")[-1]
        except:pass
        operations.add_public_public(user_id=message.from_user.id, public_public_id=text.strip())
        await message.answer("Ответы записаны, спасибо!)", reply_markup=inline_keyboards.close)
        await States.start.set()
        
def register_form_handler(dp: Dispatcher):
    global bot
    bot = Bot(token=CONFIG["BOT_TOKEN"])
    dp.register_message_handler(source_enter, state=States.source)
    dp.register_message_handler(private_enter, state=States.private)
    dp.register_message_handler(public_enter, state=States.public)
