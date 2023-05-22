from peewee import InternalError
from database.models import Post, Config, Source_public
from loguru import logger

# Создание поста


def create_post(username: str, message_id: int):
    try:
        Post.create(username=username, message_id=message_id)
    except Exception as ex:
        logger.error(f"Пост уже существует - {ex}")

# Получение поста


def get_post(message_id: int) -> Post:
    try:
        return Post.get(Post.message_id == message_id)
    except:
        logger.error(
            f"Поста с message_id: '{message_id}' не существует")


# Редактирование поста
def edit_post():
    pass

# Удаление поста


def delete_post(message_id):
    try:
        Post.delete_instance(Post.get(Post.message_id == message_id))
    except:
        logger.error(
            f"Поста с message_id: '{message_id}' не существует")


def create_config(user_id: int, private_public: str, public_public: str, source_publics: list):
    try:
        config = Config.create(
            user_id=user_id, public_public=public_public, private_public=private_public)
    except:
        logger.error("Конфиг уже существует")
    if source_publics:
        for source_public in source_publics:
            try:
                Source_public.create(source_public=source_public, config=config)
            except:
                logger.error("Source паблик уже добавлен")


def add_source_public(user_id: int, source_publics: list):
    try:
        config = Config.get(Config.user_id == user_id)
        for source_public in source_publics:
            if Config.get(Config.source_publics == source_public & Config.user_id == user_id):
                logger.info(
                    "Вы пытаетесь добавить source_public, который уже существует у этого пользователя")
            else:
                Source_public.create(
                    config=config, source_public=source_public)
    except:
        logger.error(
            "Конфига для такого user_id не существует")


def delete_source_public(user_id: int, source_public: str):
    try:
        public = Config.get(
            Config.source_publics.source_public == source_public)
        public.delete_instance()
    except:
        logger.error(
            "Вы пытаетесь удалить паблик которго не существует")


def get_config(user_id):
    try:
        return Config.get(Config.user_id == user_id)
    except:
        logger.error(
            "Конфига для такого юзерайди не существует")

# Подключаемся к базе данных и создаём таблицу поста


def init_database():
    try:
        from database.models import db
        db.connect()
        Post.create_table()
    except InternalError as px:
        logger.error(str(px))
    finally:
        db.close()
