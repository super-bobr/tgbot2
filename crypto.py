#суть файла получить актуальные цены крипты с Binance Api
import requests
#нужен для http запросов к Binance Api
from requests.exceptions import RequestException
#нужен для обработки ошибок по типу Connection error, Timeout, HTTP error
from functools import lru_cache
#нужен чтобы повторно не дублировать запросы к API для одних и тех же пар 
import logging
#чтобы было легче отлавливать ошибки

logging.basicConfig(level=logging.INFO)
#Включаем вывод логов уровня INFO и выше

@lru_cache(maxsize=10)
#оптимизирует работу, если пользователь запросит 5 раз подряд биткоин binance получит только 1 запрос, а не 5
def get_price(symbol: str) -> float:
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    #формируем url
    try:
        response = requests.get(url, timeout=5)
        #наш запрос к binance, если не будет ответа 5 сек то запрос прервется
        response.raise_for_status()
        #проверка http статуса, если статус не 200 то будет ошибка httperror
        return float(response.json()["price"])
        #извлекаем наш результат в формате {"symbol": "BTCUSDT", "price": "12345.67"}
        #все запросы в api хранятся в json файле 
    except RequestException as e:
        #ловим любые ошибку от requests
        logging.error(f"API Error for {symbol}: {str(e)}")
        #записываем ошибку в логи
        raise
        #пробрасываем иск дальше в чтобы обработать его уже в handlers.py
    except (ValueError, KeyError) as e:
        #valueError-если цена не конверт в float, keyError-если в ответе нет ключа price
        logging.error(f"Parsing Error for {symbol}: {str(e)}")
        raise