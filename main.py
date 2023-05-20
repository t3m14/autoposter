from database.operations import init_database
import dotenv, os
from bot import parser
from config import CONFIG
def load_config():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        dotenv.load_dotenv(dotenv_path)
    CONFIG["API_HASH"] = os.environ.get("API_HASH")
    CONFIG["API_ID"] = os.environ.get("API_ID")


if __name__ == "__main__":
    # Загружаем переменные окружения в конфиг
    load_config()
    # Инициализруем базу данных
    init_database()
    
