# bot_instance.py
from dotenv import load_dotenv
from os import getenv
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена")

# Создаем бота
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))