from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Цены криптовалют", callback_data="price")],
        [InlineKeyboardButton(text="✅ Подписаться", callback_data="subscribe")],
        [InlineKeyboardButton(text="❌ Отписаться", callback_data="unsubscribe")]
    ])