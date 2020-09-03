from entities.currency import Currency
from entities.item import Item
from entities.price import Prices
from manager.db_dao import insert_item, insert_prices, insert_currency


class SqlitePipeline:

    @staticmethod
    def process_item(item, spider):
        if isinstance(item, Item):
            insert_item(item)
        elif isinstance(item, Currency):
            insert_currency(item)
        elif isinstance(item, Prices):
            insert_prices(item)
        return item
