import os
import sys
from dotenv import load_dotenv

from loguru import logger

logger.remove()

logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    colorize=True
)

logger.add(
    "logs/app_{time}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    rotation="10 MB",
    retention="30 days",
    compression="zip"
)

# Загружаем переменные окружения
load_dotenv()

class Config:
    # Токен бота из переменных окружения
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    VK_TOKEN = os.getenv("VK_TOKEN")


    if not BOT_TOKEN:
        logger.warning("❌ Ошибка: BOT_TOKEN не найден в .env файле")
        logger.warning("Создайте файл .env с содержимым:")
        logger.warning("BOT_TOKEN=ваш токен от botfather")
        exit(1)

    