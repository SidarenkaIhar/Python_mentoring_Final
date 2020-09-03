import time

import schedule

from manager.db_dao import delete_parsing_items, get_parsing_items, get_items
from manager.spiders_manager import parse_items, parse_currencies, parse_prices

CURRENCIES = ('USD', 'EUR', 'RUB')


def parse_new_items():
    items = get_parsing_items()
    if items:
        delete_parsing_items(items)
        parse_items(items)
        parse_prices(items)


def parse_currencies_and_prices():
    parse_currencies(CURRENCIES)
    parse_prices(tuple(item.key for item in get_items()))


if __name__ == "__main__":
    parse_new_items()
    parse_currencies_and_prices()
    schedule.every(2).minutes.do(parse_new_items)
    schedule.every(8).hours.do(parse_currencies_and_prices)
    while True:
        schedule.run_pending()
        time.sleep(1)
