import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

class Config:
    # Токен бота из переменных окружения
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    if not BOT_TOKEN:
        print("❌ Ошибка: BOT_TOKEN не найден в .env файле")
        print("Создайте файл .env с содержимым:")
        print("BOT_TOKEN=ваш_токен_от_botfather")
        exit(1)