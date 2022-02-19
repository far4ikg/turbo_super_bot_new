from dotenv.main import load_dotenv
from os import getenv
from aiogram.bot.bot import Bot
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware


load_dotenv()
my_bot = Bot(token=getenv(key="API_TOKEN"))
dp_my_bot = Dispatcher(bot=my_bot, storage=MemoryStorage())
dp_my_bot.middleware.setup(middleware=LoggingMiddleware())
