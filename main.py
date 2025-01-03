from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram import Router
import asyncio
import os
from dotenv import load_dotenv
from bs_parser import search_google

# Загрузка переменных окружения
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

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
async def handle_query(message: Message):
    query = message.text

    try:
        # Ищем результаты в Google
        results = search_google(query)

        if not results:
            await message.reply("По вашему запросу ничего не найдено.")
            return

        # Отправляем результаты по одному сообщению
        for i, result in enumerate(results, 1):
            title = result['title']
            link = result['link']

            # Проверяем, что ссылка начинается с HTTPS
            if not link.startswith('https://'):
                await message.answer(
                    f"{i}. <b>{title}</b>\n{link}",
                    parse_mode=ParseMode.HTML
                )
                continue

            # Создаем кнопку для Web App
            web_app_button = InlineKeyboardButton(
                text="Открыть в Telegram",
                web_app={"url": link}  # Открываем ссылку через Web App
            )
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[web_app_button]])

            # Отправляем сообщение с кнопкой
            await message.answer(
                f"{i}. <b>{title}</b>\n{link}",
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard
            )

    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
