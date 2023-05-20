from peewee import InternalError
from database.models import Post
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
