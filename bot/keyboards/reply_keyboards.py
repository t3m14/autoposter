from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Запустить бота").add(KeyboardButton("Настройки")).add(KeyboardButton("Как пользоваться"))