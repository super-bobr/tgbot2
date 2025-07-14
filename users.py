import json
#для работы с json файлами
from pathlib import Path
#современный объектно-ориентированный интерфейс для путей
import logging
#чтобы было легче отлавливать ошибки

logging.basicConfig(level=logging.INFO)
#Включаем вывод логов уровня INFO и выше

DB_PATH = Path("subscribers.json")
#указываем путь к файлу с данными subscribers.json

def _load() -> set:
    try:
        if DB_PATH.exists():
            #проверка существования файла
            return set(json.loads(DB_PATH.read_text()))
            #читаем весь файл как строчку. Загружаем json из строки. Преобразуем в множество set для удаления дубликатов
        return set()
    except Exception as e:
        logging.error(f"Error loading subscribers: {str(e)}")
        return set()

def _save(users: set):
    #т.к. json не поддерживает set а только list и dict, нам надо преобразовать наш set в list
    try:
        DB_PATH.write_text(json.dumps(list(users)))
        #конвертируем множество в список, преобразовываем строку в json строку, записываем строку в файл 
    except Exception as e:
        logging.error(f"Error saving subscribers: {str(e)}")

def subscribe(chat_id: int):
    #добавляем chat id в подписчики(автоматически убирает дубликаты из-за set)
    subs = _load()
    subs.add(chat_id)
    _save(subs)

def unsubscribe(chat_id: int):
    #удаление id 
    subs = _load()
    subs.discard(chat_id)
    _save(subs)

def get_all() -> list:
    #возвращает список всех пользователей, нужен для рассылки
    return list(_load())

def is_subscribed(chat_id: int) -> bool:
    #проверяет есть ли пользователь в подписчиках, вернет T/F
    return chat_id in _load()