from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import CONFIG
from database.operations import get_config
close_button = InlineKeyboardButton(text="X", callback_data="close")
close = InlineKeyboardMarkup().add(close_button)

def get_settings(user_id) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    if user_id in CONFIG["ADMIN_IDS"]:
        kb.add(InlineKeyboardButton("Токены", callback_data="tokens"))
    kb.add(InlineKeyboardButton("Каналы источники", callback_data="source_publics"))
    kb.add(InlineKeyboardButton("Настроить свои каналы", callback_data="channel_settings"))
    
    kb.add(close_button)
    return kb

def get_private_kb(user_id) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    config = get_config(user_id=user_id)
    if config:
        kb.add(InlineKeyboardButton("Удалить", callback_data=f"delete~private~{user_id}"))
    else:
        kb.add(InlineKeyboardButton("Добавить", callback_data=f"add~private~{user_id}"))
    kb.add(close_button)
    return kb