import os #импортируем os для работы с опер.сис.
from dotenv import load_dotenv #для подгрузки env файла

load_dotenv()
#читаем файл .env в текущей директории и загружаем все переменные в окружение Python

BOT_TOKEN = os.getenv("BOT_TOKEN")
#получаем токен бота из нашего .env файла

DEFAULT_CRYPTOS = [sym for sym in os.getenv("DEFAULT_CRYPTOS", "").split(",") if sym.strip()]
#получаем список криптовалют. Getenv - получаем значение перем., если нет ничего получим пустую строку " ".Strip убирает пробелы в начале строки. Split разделяет строку по запятым "BTCUSDT,ETHUSDT" → ["BTCUSDT", "ETHUSDT"]