from aiogram.utils.executor import start_webhook, start_polling
from logging import basicConfig, INFO
from config.bot import dp_my_bot
from config.start_shutdown import start_up, shut_down
from handlers.register import register_all_handlers
from dotenv.main import load_dotenv
from os import getenv


if __name__ == '__main__':
    load_dotenv()
    basicConfig(level=INFO)
    register_all_handlers(dp_my_bot)
    """start_webhook(dispatcher=dp_my_bot,
                  webhook_path=getenv(key="WEBHOOK_PATH"),
                  skip_updates=True,
                  on_startup=start_up,
                  on_shutdown=shut_down,
                  host=getenv("WEBAPP_HOST"),
                  port=getenv("WEBAPP_PORT"))"""

    start_polling(dispatcher=dp_my_bot, skip_updates=True, on_startup=start_up, on_shutdown=shut_down)
