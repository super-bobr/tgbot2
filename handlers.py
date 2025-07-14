from aiogram import Router, F
#импротируем роутер(базовый маршутиризатор) 
#импортируем фильтры - помогают уточнить какие сообщения или кнопки ловить 
from aiogram.types import Message, CallbackQuery
#базовые типы данных от телеграм 
import config, crypto, users
#наши модули 
from keyboards import main_menu
#импорт модуля клавиатуры
import logging
#чтобы было легче отлавливать ошибки

logging.basicConfig(level=logging.INFO)
#Включаем вывод логов уровня INFO и выше

router = Router()
#создание диспетчера который распределяет входящие сообщения по обработчикам

@router.message(F.text == "/start")
#@router.message ловит только текстовые сообщения, регариует только на команду /start
async def start_handler(msg: Message):
    #объявление асинх функции 
    await msg.answer("💰 Криптобот: отслеживание цен и ежедневная рассылка", reply_markup=main_menu())#парам приклеп кнопки к сообщению
    #объявляем метод объкта Message который отправ ответ пользователю на /start 

@router.callback_query(F.data == "price")
#ловит нажатия кнопок, если у кнопки в данных напис price
async def price_handler(query: CallbackQuery): #объект с данными о нажатии кнопки
#объявление асинх функции 
    texts = []
    #Создаём пустой список, куда будем складывать строки с ценами криптовалют
    for symbol in config.DEFAULT_CRYPTOS:
        #цикл перебора всех криптовалют
        try:
        #начинаем обработку исключений, быть может binance не ответит
            price = crypto.get_price(symbol)
            #извлекаем цену на нашу крипту
            display_name = symbol.replace("USDT", "")
            #убираем из название крипты USDT - BTCUSDT → BTC
            texts.append(f"{display_name}: {price:.2f} USD")
            #округляем цену до 2 знаков после точки и добавляем в список texts
        except Exception as e:
        #обрабатываем любую ошибку
            logging.error(f"Price error for {symbol}: {str(e)}")
            #записывем нашу ошибку в логи
            display_name = symbol.replace("USDT", "")
            texts.append(f"{display_name}: сервис недоступен")
            #если не удается получить цену то выводим таоке сообщение вместо цены
    
    await query.message.edit_text("💵 Актуальные цены:\n" + "\n".join(texts), reply_markup=main_menu())
    #редактируем предыдущ сообщение объединяя все строки texts через перенос строки 
    await query.answer()
    #Говорим Telegram что мы обработали нажатие кнопки, позволяя повторно нажимать кнопку
    #Без этого кнопка будет "висеть" в нажатом состоянии
@router.callback_query(F.data == "subscribe")
#ловит нажатия кнопок, если у кнопки в данных напис subscribe
async def subscribe_handler(query: CallbackQuery):
    #объявление асинх функции 
    chat_id = query.message.chat.id
    #получаем id чата
    if users.is_subscribed(chat_id):
        await query.message.edit_text("ℹ️ Вы уже подписаны на рассылку!", reply_markup=main_menu())
    else:
        users.subscribe(chat_id)
        await query.message.edit_text("✅ Вы успешно подписались на ежедневную рассылку!", reply_markup=main_menu())
    await query.answer()

@router.callback_query(F.data == "unsubscribe")
#ловит нажатия кнопок, если у кнопки в данных напис unsubscribe
async def unsubscribe_handler(query: CallbackQuery):
    chat_id = query.message.chat.id
    if not users.is_subscribed(chat_id):
        await query.message.edit_text("ℹ️ Вы не подписаны на рассылку!", reply_markup=main_menu())
    else:
        users.unsubscribe(chat_id)
        await query.message.edit_text("❌ Вы отписались от рассылки", reply_markup=main_menu())
    await query.answer()