from dotenv.main import load_dotenv
from os import getenv

from bs4 import BeautifulSoup
from sqlite3.dbapi2 import connect
from aiohttp.client import ClientSession
from config.bot import dp_my_bot
from asyncio.tasks import sleep
from time import monotonic
from aiogram.types.callback_query import CallbackQuery


# noinspection PyPep8Naming,PyUnboundLocalVariable
@dp_my_bot.async_task
async def get_products_db(call: CallbackQuery):
    start = monotonic()
    load_dotenv()
    await call.bot.send_message(chat_id=call.from_user.id, text="Обновление запущено")
    browser_headers = {"Accept": getenv(key="HEADER_ACC"),
                       "Accept-Language": getenv(key="HEADER_ACC_LNG"),
                       "Alt-Used": getenv(key="HEADER_ALT_US"),
                       "Cache-Control": getenv(key="HEADER_CACHE_CTRL"),
                       "Connection": getenv(key="HEADER_CON"),
                       "Cookie": getenv(key="HEADER_COOKIE"),
                       "Host": getenv(key="HEADER_HOST"),
                       "Referer": getenv(key="HEADER_REF"),
                       "Sec-Fetch-Dest": getenv(key="HEADER_SEC_D"),
                       "Sec-Fetch-Mode": getenv(key="HEADER_SEC_M"),
                       "Sec-Fetch-Site": getenv(key="HEADER_SEC_S"),
                       "Upgrade-Insecure-Requests": getenv(key="HEADER_UPG_REG"),
                       "User-Agent": getenv(key="HEADER_AGENT")}
    products_db = connect(database=f"{getenv(key='DB_PATH')}all_products.db")
    products_db_cur = products_db.cursor()
    try:
        products_db_cur.execute("DELETE FROM all_marks")
    except Exception as products_db_error:
        products_db_cur.execute("CREATE TABLE IF NOT EXISTS all_marks(id INTEGER PRIMARY KEY, name TEXT)")
        print(products_db_error)
    finally:
        products_db.commit()

    try:
        async with ClientSession(headers=browser_headers) as session:
            async with session.get(url=getenv(key="URL")) as response:
                soup = BeautifulSoup(markup=await response.text(), features="html.parser")
    except Exception as parsing_error:
        print(f"Ошибка парсинга: {parsing_error}")
    finally:
        response.close()
        await session.close()

    marks_soup = soup.find(name="select", id="q_make", class_="select optional", attrs={"name": "q[make][]"})
    marks_soup = marks_soup.find_all(name="option", value=str.isalnum)

    for mark in marks_soup:
        await sleep(delay=0.01)
        mark_id = mark.get("value")
        mark_name = mark.get_text(strip=True)
        try:
            products_db_cur.execute("INSERT INTO all_marks VALUES(?, ?)", (int(mark_id), mark_name))
        except Exception as products_db_error:
            print(products_db_error)
        finally:
            products_db.commit()
        models_soup = soup.find_all(name="option", class_=f"{mark.get('value')}")
        try:
            products_db_cur.execute(f"DELETE FROM mark_{mark_id}")
        except Exception as products_db_error:
            products_db_cur.execute(
                f"CREATE TABLE IF NOT EXISTS mark_{mark_id}(mark_id INTEGER, model_id TEXT, model_name TEXT)")
            print(products_db_error)
        finally:
            products_db.commit()
        for model in models_soup:
            try:
                model_id = model.get("value")
                model_name = model.get_text(strip=True)
                products_db_cur.execute(f"INSERT INTO mark_{mark_id} VALUES(?, ?, ?)",
                                        (int(mark_id), model_id, model_name))
            except Exception as products_db_error:
                print(products_db_error)
            finally:
                products_db.commit()
    products_db_cur.close()
    products_db.close()
    await call.bot.send_message(chat_id=call.from_user.id, text="Обновление завершено")
    end = monotonic()
    print(end - start)


def get_marks_id_list():
    load_dotenv()
    dbase = connect(database=f"{getenv(key='DB_PATH')}all_products.db")
    db_cur = dbase.cursor()
    db_cur.execute("SELECT id FROM all_marks")
    marks_id = db_cur.fetchall()
    dbase.commit()
    db_cur.close()
    dbase.close()
    marks_id_list = []
    for mark_id in marks_id:
        marks_id_list.append(mark_id[0])
    marks_id_list.append(-1)
    marks_id_list.append(-2)
    marks_id_list.append(-3)
    return marks_id_list


def get_models_id_list(mark_ids):
    load_dotenv()
    dbase = connect(database=f"{getenv(key='DB_PATH')}all_products.db")
    db_cur = dbase.cursor()
    db_cur.execute(f"SELECT model_id FROM mark_{mark_ids}")
    marks_id = db_cur.fetchall()
    dbase.commit()
    db_cur.close()
    dbase.close()
    models_id_list = []
    for mark_id in marks_id:
        models_id_list.append(mark_id[0])
    models_id_list.append(-1)
    models_id_list.append(-2)
    return models_id_list
