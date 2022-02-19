from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.dispatcher import Text

from parsing.database.db_functions import get_marks_id_list, get_models_id_list

from handlers.parsing.handler import MarksFSM, ModelsFSM, call_main_menu, close_main_menu, confirm_update_products_db
from handlers.parsing.handler import change_parse_mode_marks, parse_mode_models_set_mark, parse_mode_marks
from handlers.parsing.handler import update_products_db, stop_parse, set_parse_mode, change_parse_mode_models
from handlers.parsing.handler import parse_mode_models


def register_all_handlers(dp: Dispatcher):
    dp.register_message_handler(callback=call_main_menu, commands="main_menu")
    dp.register_message_handler(set_parse_mode, Text(equals="НАЧАТЬ ПАРСИНГ"))
    dp.register_message_handler(stop_parse, Text(equals="ОСТАНОВИТЬ ПАРСИНГ"))
    dp.register_message_handler(callback=stop_parse, commands="stop_parse")
    dp.register_message_handler(update_products_db, Text(equals="ОБНОВИТЬ БД"))
    dp.register_message_handler(close_main_menu, Text(equals="Убрать кнопки"))
    dp.register_callback_query_handler(parse_mode_marks,
                                       lambda call: int(call.data) in get_marks_id_list(), state=MarksFSM)
    dp.register_callback_query_handler(parse_mode_models_set_mark,
                                       lambda call: int(call.data) in get_marks_id_list(), state=ModelsFSM.mark_auto)
    dp.register_callback_query_handler(parse_mode_models, state=ModelsFSM.model_auto)
    dp.register_callback_query_handler(confirm_update_products_db, Text(equals="update_db"))
    dp.register_callback_query_handler(change_parse_mode_marks, Text(equals="on_marks"))
    dp.register_callback_query_handler(change_parse_mode_models, Text(equals="on_models"))

