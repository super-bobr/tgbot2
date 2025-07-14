from apscheduler.schedulers.asyncio import AsyncIOScheduler
#импорт библиотеки для задач по расписанию 
import config, crypto, users
#наши модули 
from aiogram import Bot
import asyncio
#библиотека для асинх задач
from datetime import datetime
#для работы с датой и временем
import logging
#чтобы было легче отлавливать ошибки

logging.basicConfig(level=logging.INFO)
#Включаем вывод логов уровня INFO и выше

async def send_daily(bot: Bot):
    message = f"💵 Ежедневные цены ({datetime.now().strftime('%d.%m.%Y')}):\n"
    #Создаёт строку с датой в формате ДД.ММ.ГГГГ
    for sym in config.DEFAULT_CRYPTOS:
        #цикл перебора всех криптовалют
        try:
            price = crypto.get_price(sym)
            #получаем цену каждой крипты
            display_name = sym.replace("USDT", "")
            #убираем usdt из назван
            message += f"{display_name}: {price:.2f} USD\n"
            #добавляем нашу строку в сообщение 
        except Exception as e:
            #обырабатываем любые исключения
            logging.error(f"Error processing {sym}: {str(e)}")\
            #записываем ошибку в логи
            display_name = sym.replace("USDT", "")
            message += f"{display_name}: сервис недоступен\n"
    
    for user_id in users.get_all():
        #отправка сообщения всем пользователям 
        try:
            await bot.send_message(user_id, message)
            #пытаемся отправить пользователю сообщение
        except Exception as e:
        #если не получилось обрабатываем искл
            logging.error(f"Error sending to {user_id}: {str(e)}")
            #записываем ошибку в логи
def setup_scheduler(bot: Bot):
#планировщик рассылки 
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    #Инициализируем планировщик с московским часовым поясом
    scheduler.add_job(
        lambda: asyncio.create_task(send_daily(bot)),
        #lambda функция нужная чтобы обернуть вызов и отложить его выполнение ,без неё функция выполнится сразу при старте бота
        trigger="cron", 
        hour=12,
        minute=0
        #настраиваем время отправки
    )
    scheduler.start()
    #запуск планировщика, планировщик начинает работать в фоне.