import asyncio
#библиотека для асинх програм
from aiogram import Bot, Dispatcher
#
from config import BOT_TOKEN
#импортируем наш токен
from handlers import router
#импортируем все команды и кнопки из handlers.py
from scheduler import setup_scheduler
#функция для ежедневной рассылки
import logging
#чтобы было легче отлавливать ошибки

logging.basicConfig(level=logging.INFO)
#Включаем вывод логов уровня INFO и выше

async def main():
    bot = Bot(token=BOT_TOKEN)
    #создаем объект бота и передаем ему токен
    dp = Dispatcher()
    #создаем диспетчер, он решает что делать с каждым сообщением бота

    dp.include_router(router)
    #подключаем все команды /start и кнопки из handlers.py
    setup_scheduler(bot)
    #запускаем рассылку

    logging.info("Бот запущен")
    #пишем в консоль "Бот запущен" 
    await dp.start_polling(bot)
    #запускаем пулинг

if __name__ == "__main__":
    asyncio.run(main())