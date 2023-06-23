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


def is_conf_exists(user_id):
    try:
        Config.get(Config.user_id == user_id)
        return True
    except:
        return False


def create_config(user_id: int, private_public: str, public_public: str, source_publics: list):
    try:
        Config.create(
            user_id=user_id, public_public=public_public, private_public=private_public)
    except Exception as e:
        logger.error(
            f"Конфиг для юзерайди {user_id} уже существует - {e}")
    if source_publics:
        for source_public in source_publics:
            try:
                Source_public.create(source_public=source_public, config_id=Config.get(
                    Config.user_id == user_id).id)
            except:
                logger.warning("Source паблик уже добавлен")


def delete_private_public(user_id):
    try:
        config = Config.get(Config.user_id == user_id)
        config.private_public_id = None
        config.save()
    except:
        logger.error(
            f"Конфига для юзерайди {user_id} не существует")


def add_private_public(user_id, private_public_id):
    try:
        config = Config.get(Config.user_id == user_id)
        config.private_public_id = private_public_id
        config.save()
    except:
        logger.error(
            f"Конфига для юзерайди {user_id} не существует")


def delete_public_public(user_id):
    try:
        config = Config.get(Config.user_id == user_id)
        config.public_public_id = None
        config.save()
    except:
        logger.error(
            f"Конфига для юзерайди {user_id} не существует")


def add_public_public(user_id, public_public_id):
    try:
        config = Config.get(Config.user_id == user_id)
        config.public_public_id = public_public_id
        config.save()
    except:
        logger.error(
            f"Конфига для юзерайди {user_id} не существует")


def get_all_privates():
    privates_list = []
    try:
        for config in Config.select():
            privates_list.append(config.private_public_id)
        return privates_list
    except Exception as e:
        logger.error(e)


def get_all_publics():
    publics_list = []
    try:
        for config in Config.select():
            publics_list.append(config.public_public_id)
        return publics_list
    except Exception as e:
        logger.error(e)


def add_source_public(user_id: int, source_publics: list):
    try:

        for source_public in source_publics:
            try:
                Source_public.get(
                    Source_public.source_public_id == source_public)
                logger.info(
                    "Вы пытаетесь добавить source_public, который уже существует у этого пользователя")
            except Exception as e:
                Source_public.create(
                    source_public_id=source_public, config_id=Config.get(Config.user_id == user_id).id)
                logger.info("Source public создан")
    except:
        logger.error(
            f"Конфига для юзерайди {user_id} не существует")


def delete_source_public(user_id: int, source_public: str):
    try:
        sources = Source_public.get(source_public_id=source_public, config_id=Config.get(
            Config.user_id == user_id).id)
        for source in sources:
            source.delete_instance()
    except:
        logger.error(
            "Вы пытаетесь удалить паблик которго не существует")


def get_config(user_id):
    try:
        return Config.get(Config.user_id == user_id)
    except:
        logger.error(
            f"Конфига для юзерайди {user_id} не существует")


def get_all_sources():
    try:
        sources_list = []
        sources = Source_public.select()
        try:
            for source in sources:
                sources_list.append(source.source_public_id)
        except Exception as e:
            logger.error(
                f"{e}")
            sources_list.append(sources.source_public_id)
        return sources_list
    except Exception as e:
        logger.error(
            f"{e}")


def get_sources_for_config(user_id):
    try:
        sources_list = []
        sources = Source_public.get(
            config_id=Config.get(Config.user_id == user_id).id)
        try:
            for source in sources:
                sources_list.append(source.source_public_id)
        except:
            sources_list.append(sources.source_public_id)
        return sources_list
    except Exception as e:
        logger.error(
            f"Конфига для юзерайди {user_id} не существует - {e}")


def get_all_configs_by_source(username):
    conf_list = []
    sources = Source_public.select().where(
        Source_public.source_public_id == username)
    try:
        for source in sources:
            conf_list.append(Config.get_by_id(source.config_id))
    except Exception as e:
        logger.error(e)
        conf_list.append(Config.get_by_id(sources.config_id))
    return conf_list

def get_all_privates_by_source(username):
    privates_list = []
    configs = get_all_configs_by_source(username=username)
    try:
        for config in configs:
            privates_list.append(config.private_public_id)
    except Exception as e:
        logger.error(e)
        privates_list.append(configs.private_public_id)
    return privates_list
def get_all_publics_by_source(username):
    publics_list = []
    configs = get_all_configs_by_source(username=username)
    try:
        for config in configs:
            publics_list.append(config.public_public_id)
    except Exception as e:
        logger.error(e)
        publics_list.append(configs.public_public_id)
    return publics_list
# Подписка


def is_sub(user_id):
    return Config.get(Config.user_id == user_id).is_subscribed


def make_sub(user_id):
    config = Config.get(Config.user_id == user_id)
    if (config.is_subscribed == False):
        config.is_subscribed = True
        config.save()
    else:
        logger.error(
            f"Пользователь {user_id} уже имеет подписку")


def make_unsub(user_id):
    config = Config.get(Config.user_id == user_id)
    if (config.is_subscribed):
        config.is_subscribed = False
        config.save()
    else:
        logger.error(
            f"Пользователь {user_id} уже отписан")

# Подключаемся к базе данных и создаём таблицу поста


def init_database():
    try:
        from database.models import db
        db.connect()
        Config.create_table()
        Source_public.create_table()
        Post.create_table()
    except InternalError as px:
        logger.error(str(px))
    finally:
        db.close()
