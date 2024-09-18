import asyncio
import logging
import sys
from dotenv import load_dotenv
from os import getenv
from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand

from bot_instance import bot
from app.handlers import router

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена")


dp = Dispatcher()


# Функция для установки команд
async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать работу с ботом"),
        BotCommand(command="/about", description="О Лизе"),
        BotCommand(command="/video", description="Исполнение"),
    ]
    await bot.set_my_commands(commands)


async def main() -> None:
    # Устанавливаем команды
    await set_bot_commands(bot)
    
    dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
