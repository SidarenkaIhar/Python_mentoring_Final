from entities.currency import Currency
from entities.displayed_position import DisplayedPosition
from entities.item import Item
from entities.price import Position
from entities.user import User
from manager.db_manager import DatabaseManager
from manager.sql_queries import SELECT_ITEMS, SELECT_CURRENCIES, INSERT_ITEM, \
    INSERT_CURRENCY, INSERT_SHOP, INSERT_POSITION, SELECT_ITEM_BY_KEY, DELETE_ITEM, DELETE_POSITION, \
    SELECT_LAST_POSITIONS_BY_ITEM, SELECT_DISPLAYED_POSITIONS_BY_ITEM, INSERT_USER, SELECT_USERS_BY_ID, \
    SELECT_CURRENCIES_BY_ABBREVIATION, SELECT_USERS, INSERT_PARSING_ITEM, SELECT_PARSING_ITEMS, DELETE_PARSING_ITEM

_db_manager = DatabaseManager()


# ITEMS
def insert_item(item):
    if item:
        return _db_manager.create(INSERT_ITEM, item.get_values())
    return 0


def get_items():
    return [Item(*item) for item in _db_manager.read(SELECT_ITEMS)]


def get_item_by_key(key):
    return [Item(*item) for item in _db_manager.read(SELECT_ITEM_BY_KEY, (key,))]


def delete_item(item_key):
    items = get_item_by_key(item_key)
    if items:
        _db_manager.delete(DELETE_POSITION, (items[0].id,))
        return _db_manager.delete(DELETE_ITEM, (items[0].key,))
    return 0


# CURRENCIES
def insert_currency(currency):
    if currency:
        return _db_manager.create(INSERT_CURRENCY, currency.get_values())
    return 0


def get_currencies():
    return [Currency(*currency) for currency in _db_manager.read(SELECT_CURRENCIES)]


def get_currencies_by_abbreviation(abbreviation):
    return [Currency(*cur) for cur in _db_manager.read(SELECT_CURRENCIES_BY_ABBREVIATION, (abbreviation,))]


# POSITIONS
def get_last_positions_by_item(item_id):
    return [Position(*position) for position in _db_manager.read(SELECT_LAST_POSITIONS_BY_ITEM, (item_id,))]


def get_displayed_positions_by_item(item_key):
    item = get_item_by_key(item_key)
    if item:
        positions = _db_manager.read(SELECT_DISPLAYED_POSITIONS_BY_ITEM, (item[0].id,))
        return [DisplayedPosition(*position) for position in positions]
    return []


# PRICES
def insert_prices(prices):
    if prices:
        _db_manager.create_many(INSERT_SHOP, prices.get_shops_values())
        return _db_manager.create_many(INSERT_POSITION, prices.get_positions_values())
    return 0


# USERS
def insert_user(user):
    if user:
        return _db_manager.create(INSERT_USER, user.get_values())
    return 0


def get_users():
    return [User(*user) for user in _db_manager.read(SELECT_USERS)]


def get_user_by_id(user_id):
    return [User(*user) for user in _db_manager.read(SELECT_USERS_BY_ID, (user_id,))]


# PARSING ITEMS
def insert_parsing_items(items):
    if items:
        return _db_manager.create_many(INSERT_PARSING_ITEM, [(item,) for item in items])
    return 0


def get_parsing_items():
    return [items[0] for items in _db_manager.read(SELECT_PARSING_ITEMS)]


def delete_parsing_items(items):
    if items:
        return _db_manager.delete_many(DELETE_PARSING_ITEM, [(item,) for item in items])
    return 0
