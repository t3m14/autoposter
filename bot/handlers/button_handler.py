from aiogram import Dispatcher, types
from bot.keyboards import inline_keyboards
from userbot import load_app, parser
from bot.states.states import States
from database import operations
async def keyboard_handler(message: types.Message):
    match message.text:
        case "Настройки":
            await message.answer("Выберите нужное", reply_markup=inline_keyboards.get_settings(message.from_user.id))
        case "Как пользоваться":
            await message.answer("По техническим вопросам работы бота писать @bvdtripp", reply_markup=inline_keyboards.close)
        case "Запустить бота":
            config = operations.get_config(user_id=message.from_user.id)
            not_empty = False
            if operations.get_sources_for_config(user_id=message.from_user.id) != []:
                if config.public_public_id != None:
                    if config.private_public_id != None:
                        not_empty=True
            if not_empty:
                # app_started = False
                # if not app_started:                
                #     app_started = True
                #     try:
                #         app_data = await load_app.start("89292394343")
                #         if (type(app_data) is dict):
                #             code = input("Code: ")
                #             app = await load_app.authApp(app_data, code)
                #         else:
                #             app = app_data
                #         await parser.start_parse(app, message.from_user.id)
                #     except:pass

                await message.answer("Теперь в скором времени в ваш приватный паблик придёт пост из источников, чтобы опубликовать его нужно написать цифру под этим постом со знаком ' + '\n\nВы можете остановить рассылку кнопкой ниже", reply_markup=inline_keyboards.stopBot)
                await parser.start_parse()
            else: 
                await message.answer("Сначала заполните настройки")
            try:
                await message.delete()
            except Exception as e:
                print(e)
            

def register_button_handler(dp: Dispatcher):
    dp.register_message_handler(keyboard_handler, state=States.start)
