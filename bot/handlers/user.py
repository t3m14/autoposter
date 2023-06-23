from loguru import logger
from aiogram import types, Dispatcher
from bot.states.states import States
from bot.keyboards import reply_keyboards, inline_keyboards
from database import operations
async def start_handler(message: types.Message):
    if(operations.is_conf_exists(user_id=message.from_user.id) == False):
        operations.create_config(user_id=message.from_user.id, private_public=None, public_public=None, source_publics=None) 
    elif (operations.is_sub(user_id=message.from_user.id)):
        await message.answer("Привет!\n\n**Бот треша**\n рад вас приветствовать!\nЧтобы начать работу нажимите на любую из подходящих клавиш снизу!\n\nПриятного использования :)", reply_markup=reply_keyboards.main_menu_kb)
        await message.answer("отписаться", reply_markup=inline_keyboards.make_unsub)
    else:
        await message.answer("Пожалуйста подпишитесь", reply_markup=inline_keyboards.make_sub)
    await States.start.set()

def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'], state="*")