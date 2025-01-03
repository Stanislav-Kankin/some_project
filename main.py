from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram import Router
import asyncio
import os
from dotenv import load_dotenv
from bs_parser import search_google, search_yandex

# Загрузка переменных окружения
dot_env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dot_env_path):
    load_dotenv(dot_env_path)

# Инициализация бота и диспетчера
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

# Роутер для обработки сообщений
router = Router()
dp.include_router(router)


# Обработчик команды /start
@router.message(Command("start"))
async def handle_start(message: Message):
    await message.reply(
        "Привет! Я бот, который поможет тебе найти информацию в интернете.\n"
        "Просто напиши свой запрос, и я найду для тебя ссылки!"
    )


# Обработчик текстовых сообщений (поиск)
@router.message()
async def handle_search(message: Message):
    query = message.text
    try:
        # Ищем в Google (можно заменить на search_yandex)
        results = search_google(query)

        if not results:
            await message.reply("По вашему запросу ничего не найдено.")
            return

        # Формируем ответ
        response = "Вот что я нашел:\n\n"
        for i, result in enumerate(results, 1):
            response += f"{i}. <a href='{result['link']}'>{result['title']}</a>\n"

        # Отправляем ответ
        await message.reply(response, parse_mode=ParseMode.HTML)
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
