from aiogram import Bot, Dispatcher
from aiogram.types import Message

from dotenv import load_dotenv
import os

dot_env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dot_env_path):
    load_dotenv(dot_env_path)

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    await message.reply(
        "Привет, я бот, который поможет "
        "тебе найти нужную информацию о фильме"
        )


