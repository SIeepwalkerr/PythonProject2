import logging
import os
import asyncio
from aiogram import Bot, Dispatcher
from app.admin import admin
from app.user import user
from app.database.models import async_main
from dotenv import load_dotenv
async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

    dp = Dispatcher()
    dp.include_routers(user,admin)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

async def on_startup(dispatcher):
    await async_main()
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO) # Подключение логирования
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')