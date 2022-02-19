from asyncio.tasks import sleep
from sqlite3.dbapi2 import connect
from sqlite3.dbapi2 import IntegrityError
from os import getenv
from random import randint
from dotenv.main import load_dotenv

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton


async def create_parse_db(search_attr: str, call: CallbackQuery, break_parse: bool):
    load_dotenv()
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

    sql_db = connect(database=f"{getenv(key='DB_PATH')}parsing.db")
    db_cursor = sql_db.cursor()
    db_cursor.execute('CREATE TABLE IF NOT EXISTS products'
                      '(link TEXT PRIMARY KEY, image TEXT, price TEXT, name TEXT, desc TEXT, datetime TEXT)')
    db_cursor.execute('DELETE FROM products')
    sql_db.commit()

    try:
        async with ClientSession(base_url=getenv(key="URL"), headers=browser_headers) as session:
            async with session.get(url=search_attr) as response:
                text_response = await response.text()
                soup = BeautifulSoup(markup=text_response, features="html.parser")
                main_container = soup.find(name="div", class_="main-container")
                products_container = main_container.find(name="div", class_="products-container")
                products = products_container.find_all(name="div", class_="products")
                if len(products) == 3:
                    product_tables = products[2]
                elif len(products) == 2:
                    product_tables = products[1]
                else:
                    product_tables = products[0]
    except Exception as error:
        await call.bot.send_message(
            chat_id=call.from_user.id, text=f'Парсинг: Ошибка подключения к {search_attr}\n{error}')
        break_parse = True
        return break_parse
    finally:
        response.close()
        await session.close()

    for product in product_tables:
        product_link = f"{getenv(key='URL')}{product.find(name='a').get(key='href')}"

        product_image = product.find(name="div", class_="products-i__top").find(name="img").get(key="src")

        product_price = product.find(
            name="div", class_="products-i__bottom").find(
            name='div', class_='product-price').get_text(strip=True)

        product_name = product.find(
            name="div", class_="products-i__bottom").find(
            name='div', class_='products-i__name').get_text(strip=True)

        product_desc = product.find(
            name="div", class_="products-i__bottom").find(
            name='div', class_='products-i__attributes').get_text(strip=True)

        product_datetime = product.find(
            name="div", class_="products-i__bottom").find(
            name='div', class_='products-i__datetime').get_text(strip=True)

        product_tuple = (product_link, product_image, product_price, product_name, product_desc, product_datetime)
        try:
            db_cursor.execute('INSERT INTO products VALUES(?, ?, ?, ?, ?, ?);', product_tuple)
        except Exception as error:
            await call.bot.send_message(chat_id=call.from_user.id, text=f"Ошибка старта: {error}")
            break_parse = True
            return break_parse
        finally:
            sql_db.commit()
    db_cursor.close()
    sql_db.close()
    await sleep(delay=0.1)


# noinspection PyBroadException
async def start_parse(search_attr: str, call: CallbackQuery, break_parse: bool):
    await sleep(delay=randint(a=2, b=5))
    load_dotenv()
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

    sql_db = connect(database=f"{getenv(key='DB_PATH')}parsing.db")
    db_cursor = sql_db.cursor()
    db_cursor.execute('CREATE TABLE IF NOT EXISTS products'
                      '(link TEXT PRIMARY KEY, image TEXT, price TEXT, name TEXT, desc TEXT, datetime TEXT)')
    sql_db.commit()

    try:
        async with ClientSession(base_url=getenv(key="URL"), headers=browser_headers) as session:
            async with session.get(url=search_attr) as response:
                text_response = await response.text()
                soup = BeautifulSoup(markup=text_response, features="html.parser")
                main_container = soup.find(name="div", class_="main-container")
                products_container = main_container.find(name="div", class_="products-container")
                products = products_container.find_all(name="div", class_="products")
                if len(products) == 3:
                    product_tables = products[2]
                elif len(products) == 2:
                    product_tables = products[1]
                else:
                    product_tables = products[0]
    except Exception as error:
        await call.bot.send_message(
            chat_id=call.from_user.id, text=f'Парсинг: Ошибка подключения к {search_attr}\n{error}')
        break_parse = True
        return break_parse
    finally:
        response.close()
        await session.close()
    for product in product_tables:
        product_link = f"{getenv(key='URL')}{product.find(name='a').get(key='href')}"

        product_image = product.find(name="div", class_="products-i__top").find(name="img").get(key="src")

        product_price = product.find(
            name="div", class_="products-i__bottom").find(
            name='div', class_='product-price').get_text(strip=True)

        product_name = product.find(
            name="div", class_="products-i__bottom").find(
            name='div', class_='products-i__name').get_text(strip=True)

        product_desc = product.find(
            name="div", class_="products-i__bottom").find(
            name='div', class_='products-i__attributes').get_text(strip=True)

        product_datetime = product.find(
            name="div", class_="products-i__bottom").find(
            name='div', class_='products-i__datetime').get_text(strip=True)

        product_tuple = (product_link, product_image, product_price, product_name, product_desc, product_datetime)
        try:
            db_cursor.execute('INSERT INTO products VALUES(?, ?, ?, ?, ?, ?);', product_tuple)
            await call.bot.send_photo(chat_id=call.from_user.id, photo=product_image,
                                      caption=f"{product_name}\n{product_desc}\n{product_price}\n{product_datetime}",
                                      reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                          text="Посмотреть", url=product_link)))
        except IntegrityError:
            pass
        except Exception as error:
            await call.bot.send_message(chat_id=call.from_user.id, text=f"Ошибка парсинга: {error}")
            break_parse = True
            return break_parse
        finally:
            sql_db.commit()
    db_cursor.close()
    sql_db.close()
    await sleep(delay=randint(a=2, b=5))
