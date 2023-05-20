from config import CONFIG
from pyrogram import Client
import os, fnmatch
def is_session_exists(phone):
    return os.path.isfile(f"./sessions/{phone}.session")
async def start(phone_number: str):
    api_id = CONFIG["API_ID"]
    api_hash = CONFIG["API_HASH"]
    if is_session_exists(phone=phone_number) == True:
        app = Client(f'{phone_number}', api_id=api_id, api_hash=api_hash, workdir="sessions")
        await app.start()
        return app
    app = Client(f'{phone_number}', api_id=api_id, api_hash=api_hash, workdir="sessions")
    await app.connect()
    #отправляем код для входа
    sCode = await app.send_code(phone_number)
    return {"app": app, "phone_code_hash": sCode.phone_code_hash, "phone": phone_number}

async def authApp(app_data:dict, code: int):
    app = app_data["app"]
    await app.sign_in(app_data["phone"],app_data["phone_code_hash"], code)
    return app
