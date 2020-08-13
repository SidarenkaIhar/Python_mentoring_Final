from manager.db_dao import insert_item, insert_prices, insert_currency
from onliner.items.currency import Currency
from onliner.items.item import Item
from onliner.items.shop import Prices


class SqlitePipeline:
    def process_item(self, item, spider):
        if isinstance(item, Item):
            insert_item(item)
        elif isinstance(item, Currency):
            insert_currency(item)
        elif isinstance(item, Prices):
            insert_prices(item)
        return item
