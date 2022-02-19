from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton


menu_reply_kb = ReplyKeyboardMarkup(resize_keyboard=True)
btn_1 = KeyboardButton(text="НАЧАТЬ ПАРСИНГ")
btn_2 = KeyboardButton(text="ОСТАНОВИТЬ ПАРСИНГ")
btn_3 = KeyboardButton(text="ОБНОВИТЬ БД")
btn_close = KeyboardButton(text="Убрать кнопки")

menu_reply_kb.row(btn_1, btn_2).row(btn_3, btn_close)
