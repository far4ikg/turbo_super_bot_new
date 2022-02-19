from dotenv.main import load_dotenv
from os import getenv

from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from sqlite3.dbapi2 import connect

parse_ikb = InlineKeyboardMarkup(row_width=2).row(InlineKeyboardButton(text="ПО МАРКАМ", callback_data="on_marks"),
                                                  InlineKeyboardButton(text="ПО МОДЕЛЯМ", callback_data="on_models"))
update_db_ikb = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="Обновить",
                                                                           callback_data="update_db"))


def marks_mode_first_ikb():
    load_dotenv()
    dbase = connect(database=f"{getenv(key='DB_PATH')}all_products.db")
    db_cur = dbase.cursor()
    inline_kb = InlineKeyboardMarkup(row_width=3)
    db_cur.execute("SELECT * FROM all_marks")
    marks = sorted(db_cur.fetchall())[:80]
    dbase.commit()
    db_cur.close()
    dbase.close()
    for mark in marks:
        inline_kb.insert(InlineKeyboardButton(text=f"{mark[1]}", callback_data=f"{mark[0]}"))
    inline_kb.row(InlineKeyboardButton(text="Все марки", callback_data="-1"),
                  InlineKeyboardButton(text="Готово", callback_data="-2"),
                  InlineKeyboardButton(text="Отменить", callback_data="-3"))
    return inline_kb


def marks_mode_second_ikb():
    load_dotenv()
    dbase = connect(database=f"{getenv(key='DB_PATH')}all_products.db")
    db_cur = dbase.cursor()
    inline_kb = InlineKeyboardMarkup(row_width=3)
    db_cur.execute("SELECT * FROM all_marks")
    marks = sorted(db_cur.fetchall())[80:]
    dbase.commit()
    db_cur.close()
    dbase.close()
    for mark in marks:
        inline_kb.insert(InlineKeyboardButton(text=f"{mark[1]}", callback_data=f"{mark[0]}"))
    inline_kb.row(InlineKeyboardButton(text="Все марки", callback_data="-1"),
                  InlineKeyboardButton(text="Готово", callback_data="-2"),
                  InlineKeyboardButton(text="Отменить", callback_data="-3"))
    return inline_kb


def models_mode_first_ikb():
    load_dotenv()
    dbase = connect(database=f"{getenv(key='DB_PATH')}all_products.db")
    db_cur = dbase.cursor()
    inline_kb = InlineKeyboardMarkup(row_width=3)
    db_cur.execute("SELECT * FROM all_marks")
    marks = sorted(db_cur.fetchall())[:80]
    dbase.commit()
    db_cur.close()
    dbase.close()
    for mark in marks:
        inline_kb.insert(InlineKeyboardButton(text=f"{mark[1]}", callback_data=f"{mark[0]}"))
    inline_kb.row(InlineKeyboardButton(text="Отменить", callback_data="-2"))
    return inline_kb


def models_mode_second_ikb():
    load_dotenv()
    dbase = connect(database=f"{getenv(key='DB_PATH')}all_products.db")
    db_cur = dbase.cursor()
    inline_kb = InlineKeyboardMarkup(row_width=3)
    db_cur.execute("SELECT * FROM all_marks")
    marks = sorted(db_cur.fetchall())[80:]
    dbase.commit()
    db_cur.close()
    dbase.close()
    for mark in marks:
        inline_kb.insert(InlineKeyboardButton(text=f"{mark[1]}", callback_data=f"{mark[0]}"))
    inline_kb.row(InlineKeyboardButton(text="Отменить", callback_data="-2"))
    return inline_kb


def models_ikb(mark_id):
    load_dotenv()
    models_kb = InlineKeyboardMarkup(row_width=3)
    dbase = connect(database=f"{getenv(key='DB_PATH')}all_products.db")
    db_cur = dbase.cursor()
    db_cur.execute(f"SELECT * FROM mark_{mark_id}")
    mark = db_cur.fetchall()
    db_cur.close()
    dbase.close()
    for model in mark:
        models_kb.insert(InlineKeyboardButton(text=f"{model[2]}", callback_data=f"{model[1]}"))
    models_kb.row(InlineKeyboardButton(text="Готово", callback_data="-1"),
                  InlineKeyboardButton(text="Отменить", callback_data="-2"))
    return models_kb
