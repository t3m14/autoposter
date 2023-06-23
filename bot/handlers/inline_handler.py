from aiogram import Dispatcher, types
from bot.states.states import States
from loguru import logger
from database import operations
async def inline_keyboard_handler(call: types.CallbackQuery):
    match call.data:
        case "close":
            await call.message.delete()
        case "channel_settings":
            first_message = call.message.message_id
            logger.debug(first_message)
            await call.message.answer("Введите ссылку или юзернейм СКРЫТОГО канала\n Сюда приходят все посты из каналов ИСТОЧНИКОВ, скрытый канал должен быть открыт (но иметь сложный юзернейм, чтобы другие не могли туда зайти)")
            await States.private.set()
        case "source_publics":
            first_message = call.message.message_id
            await call.message.answer("Введите ссылку или юзернейм каналов ИСТОЧНИКОВ")
            await States.source.set()
        case "make_sub":
            operations.make_sub(call.from_user.id)
            await call.message.answer(f"Подписано")
        case "make_unsub":
            operations.make_unsub(call.from_user.id)
        case "stop_bot":
            await call.message.answer("Бот остановлен, чтобы возобновить работу бота, нужно просто снова заполнить настройки")
            operations.delete_private_public(user_id=call.from_user.id)
            operations.delete_public_public(user_id=call.from_user.id)

def register_inline_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(inline_keyboard_handler, state="*")