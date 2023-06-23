from userbot import parser, load_app
async def start_parse():
    # try:
    app_data = await load_app.start("89292394343")
    if (type(app_data) is dict):
        code = input("Code: ")
        app = await load_app.authApp(app_data, code)
    else:
        app = app_data
    await parser.start_parse(app)
    # except Exception as e:
    #     print(e)