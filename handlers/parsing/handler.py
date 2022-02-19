from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.message import Message
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from dotenv.main import load_dotenv
from os import getenv

from keyboards.reply.main_menu import menu_reply_kb
from keyboards.inline.parsing import marks_mode_first_ikb, marks_mode_second_ikb, parse_ikb, update_db_ikb, models_ikb
from keyboards.inline.parsing import models_mode_first_ikb, models_mode_second_ikb
from parsing.database.db_functions import get_products_db
from parsing.parse import create_parse_db, start_parse


load_dotenv()


class MarksFSM(StatesGroup):
    mark_auto = State()


class ModelsFSM(StatesGroup):
    mark_auto = State()
    model_auto = State()


stop_parsing = bool


async def call_main_menu(msg: Message):
    await msg.reply(text="Держи главное меню", reply_markup=menu_reply_kb)


async def close_main_menu(msg: Message):
    await msg.answer(text="Я закрыл главное меню", reply_markup=ReplyKeyboardRemove())


async def set_parse_mode(msg: Message):
    await msg.answer(text="Выбери метод", reply_markup=parse_ikb)


async def change_parse_mode_marks(call: CallbackQuery, state_group=MarksFSM):
    global stop_parsing
    if not stop_parsing:
        stop_parsing = True
        await call.bot.send_message(chat_id=call.message.chat.id, text="Остановка парсинга...")
    await state_group.mark_auto.set()
    await call.bot.send_message(chat_id=call.message.chat.id, text="1-ой список", reply_markup=marks_mode_first_ikb())
    await call.bot.send_message(chat_id=call.message.chat.id, text="2-ой список", reply_markup=marks_mode_second_ikb())
    await call.answer(text="Выбирай марку", show_alert=True)


async def change_parse_mode_models(call: CallbackQuery, state_group=ModelsFSM):
    global stop_parsing
    if not stop_parsing:
        stop_parsing = True
        await call.bot.send_message(chat_id=call.message.chat.id, text="Остановка парсинга...")
    await state_group.mark_auto.set()
    await call.bot.send_message(chat_id=call.message.chat.id, text="1-ой список", reply_markup=models_mode_first_ikb())
    await call.bot.send_message(chat_id=call.message.chat.id, text="2-ой список", reply_markup=models_mode_second_ikb())
    await call.answer(text="Выбирай марку", show_alert=True)


async def parse_mode_marks(call: CallbackQuery, state: FSMContext):
    global stop_parsing
    search_attr = getenv(key='PAGE')
    if call.data == "-1":
        stop_parsing = False
        await state.finish()
        await state.storage.close()
        await call.answer(text="Выбор сделан")
        await create_parse_db(search_attr=search_attr, call=call, break_parse=stop_parsing)
        while not stop_parsing:
            await start_parse(search_attr=search_attr, call=call, break_parse=stop_parsing)
        await call.bot.send_message(chat_id=call.from_user.id, text="Парсинг остановлен")
    elif call.data == "-2":
        stop_parsing = False
        for i in await state.get_data():
            search_attr += f"{getenv(key='MARK') + i + '&'}"
        search_attr = search_attr[:-1]
        await state.finish()
        await state.storage.close()
        await call.answer(text="Выбор сделан")
        await create_parse_db(search_attr=search_attr, call=call, break_parse=stop_parsing)
        while not stop_parsing:
            await start_parse(search_attr=search_attr, call=call, break_parse=stop_parsing)
        await call.bot.send_message(chat_id=call.from_user.id, text="Парсинг остановлен")
    elif call.data == "-3":
        if not stop_parsing:
            stop_parsing = True
            await call.bot.send_message(chat_id=call.message.chat.id, text="Остановка парсинга...")
        await state.finish()
        await state.storage.close()
        await call.answer(text="Парсинг отменен")
    else:
        async with state.proxy() as data:
            data[f"{int(call.data)}"] = int(call.data)
        await call.answer(text="Выбор сделан\n\"Отменить\" - отменить процесс")


async def parse_mode_models_set_mark(call: CallbackQuery, state: FSMContext, state_group=ModelsFSM):
    global stop_parsing
    if call.data == "-2":
        if not stop_parsing:
            stop_parsing = True
            await call.bot.send_message(chat_id=call.message.chat.id, text="Остановка парсинга...")
        await state.finish()
        await state.storage.close()
        await call.answer(text="Парсинг отменен")
    else:
        async with state.proxy() as data:
            data["mark_id"] = call.data
        await call.answer(text="Марка выбрана")
        await state_group.model_auto.set()
        await call.bot.send_message(chat_id=call.from_user.id, text="Выбери модель",
                                    reply_markup=models_ikb(mark_id=call.data))


async def parse_mode_models(call: CallbackQuery, state: FSMContext):
    global stop_parsing
    state_data = await state.get_data()
    mark_id = state_data["mark_id"]
    search_attr = f"{getenv(key='PAGE')}{getenv(key='MARK')}{mark_id}&"
    if call.data == "-1":
        stop_parsing = False
        for i, j in enumerate(await state.get_data()):
            if i == 0:
                continue
            search_attr += f"{getenv(key='MODEL') + j + '&'}"
        search_attr = search_attr[:-1]
        await state.finish()
        await state.storage.close()
        print(search_attr)
        await call.answer(text="Выбор сделан")
        await create_parse_db(search_attr=search_attr, call=call, break_parse=stop_parsing)
        while not stop_parsing:
            await start_parse(search_attr=search_attr, call=call, break_parse=stop_parsing)
        await call.bot.send_message(chat_id=call.from_user.id, text="Парсинг остановлен")
    elif call.data == "-2":
        if not stop_parsing:
            stop_parsing = True
            await call.bot.send_message(chat_id=call.message.chat.id, text="Остановка парсинга...")
        await state.finish()
        await state.storage.close()
        await call.answer(text="Парсинг отменен")
    else:
        async with state.proxy() as data:
            data[call.data] = call.data
        await call.answer(text="Выбор сделан\n\"Отменить\" - отменить процесс")


async def stop_parse(msg: Message):
    global stop_parsing
    await msg.answer(text="Остановка парсинга...")
    stop_parsing = True


async def update_products_db(msg: Message):
    await msg.answer(text="Обновить БД?", reply_markup=update_db_ikb)


async def confirm_update_products_db(call: CallbackQuery):
    if call.from_user.id == int(getenv(key="OWNER_ID")):
        await call.answer()
        await get_products_db(call=call)
    else:
        await call.answer(text="Обновлять БД может только мой хозяин...")
