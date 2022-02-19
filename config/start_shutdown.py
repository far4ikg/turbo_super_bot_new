from dotenv.main import load_dotenv
from os import getenv
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.types.bot_command import BotCommand
from keyboards.inline.parsing import update_db_ikb


async def start_up(dp: Dispatcher):
    load_dotenv()
    await dp.bot.set_webhook(url=getenv(key="WEBHOOK_URL"))
    await dp.bot.set_my_commands([BotCommand(command="main_menu", description="Главное меню")])
    await dp.bot.send_message(chat_id=getenv(key="OWNER_ID"), text="Я в сети, обновить БД?", reply_markup=update_db_ikb)


async def shut_down(dp: Dispatcher):
    load_dotenv()
    await dp.bot.delete_webhook()
    await dp.bot.delete_my_commands()
    await dp.storage.close()
    await dp.bot.send_message(chat_id=getenv(key="OWNER_ID"), text="Я выключился", reply_markup=ReplyKeyboardRemove())
