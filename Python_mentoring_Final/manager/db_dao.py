from manager.db_manager import DatabaseManager
from manager.sql_queries import SELECT_ITEMS, SELECT_CURRENCIES, SELECT_SHOPS, SELECT_POSITIONS, INSERT_ITEM, \
    INSERT_CURRENCY, INSERT_SHOP, INSERT_POSITION, SELECT_ITEM, DELETE_ITEM, DELETE_POSITION, DROP_TABLE_ITEMS, \
    SELECT_POSITIONS_BY_ITEM
from onliner.items.currency import Currency
from onliner.items.item import Item
from onliner.items.shop import Shop, Position, Prices

_db_manager = DatabaseManager()


# ITEMS
def insert_item(item: Item = None):
    if item:
        _db_manager.execute_queries(INSERT_ITEM, item.get_values())


def get_items():
    return [Item(*item) for item in _db_manager.execute_queries(SELECT_ITEMS)]


def get_item(key=None):
    return [Item(*item) for item in _db_manager.execute_queries(SELECT_ITEM, (key,))]


def delete_items():
    return _db_manager.execute_queries(DROP_TABLE_ITEMS)


def delete_item(item=None):
    print(item)
    if item:
        _db_manager.execute_queries(DELETE_POSITION, [(item.id,)])
        return _db_manager.execute_queries(DELETE_ITEM, [(item.key,)])


# CURRENCIES
def insert_currency(currency: Currency = None):
    if currency:
        _db_manager.execute_queries(INSERT_CURRENCY, currency.get_values())


def get_currencies():
    return [Currency(*currency) for currency in _db_manager.execute_queries(SELECT_CURRENCIES)]


# SHOPS
def get_shops():
    return [Shop(*shop) for shop in _db_manager.execute_queries(SELECT_SHOPS)]


# POSITIONS
def get_positions():
    return [Position(*position) for position in _db_manager.execute_queries(SELECT_POSITIONS)]


def get_positions_by_item(item=None):
    return [Position(*position) for position in _db_manager.execute_queries(SELECT_POSITIONS_BY_ITEM, (item,))]


def insert_prices(prices: Prices = None):
    if prices:
        _db_manager.execute_queries(INSERT_SHOP, prices.get_shops_values(), many=True)
        _db_manager.execute_queries(INSERT_POSITION, prices.get_positions_values(), many=True)
