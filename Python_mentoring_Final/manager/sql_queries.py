# ITEMS
CREATE_TABLE_ITEMS = """CREATE TABLE IF NOT EXISTS items(
                            id INTEGER PRIMARY KEY,
                            key TEXT,
                            extended_name TEXT,
                            price DECIMAL,
                            html_url TEXT)"""
INSERT_ITEM = "INSERT OR REPLACE INTO items VALUES(?, ?, ?, ?, ?)"
SELECT_ITEMS = "SELECT * FROM items"
SELECT_ITEM_BY_KEY = "SELECT * FROM items WHERE key=?;"
DELETE_ITEM = "DELETE FROM items WHERE key=?;"
DROP_TABLE_ITEMS = "DROP TABLE IF EXISTS items"

# CURRENCIES
CREATE_TABLE_CURRENCIES = """CREATE TABLE IF NOT EXISTS currencies(
                            id TEXT PRIMARY KEY,
                            date DATE,
                            abbreviation TEXT,
                            rate DECIMAL)"""
INSERT_CURRENCY = "INSERT OR REPLACE INTO currencies VALUES(?, ?, ?, ?)"
SELECT_CURRENCIES = "SELECT * FROM currencies"
SELECT_CURRENCIES_BY_ABBREVIATION = "SELECT * FROM currencies WHERE abbreviation=? ORDER BY date desc"
DELETE_CURRENCY = "DELETE FROM currencies WHERE abbreviation=?"
DROP_TABLE_CURRENCIES = "DROP TABLE IF EXISTS currencies"

# SHOPS
CREATE_TABLE_SHOPS = """CREATE TABLE IF NOT EXISTS shops(
                            id INTEGER PRIMARY KEY,
                            title TEXT,
                            html_url TEXT,
                            reviews_rating DECIMAL,
                            reviews_count INTEGER)"""
INSERT_SHOP = "INSERT OR REPLACE INTO shops VALUES(?, ?, ?, ?, ?)"
SELECT_SHOPS = "SELECT * FROM shops"
DELETE_SHOP = "DELETE FROM shops WHERE id=?"
DROP_TABLE_SHOPS = "DROP TABLE IF EXISTS shops"

# POSITIONS
CREATE_TABLE_POSITIONS = """CREATE TABLE IF NOT EXISTS positions(
                            id TEXT PRIMARY KEY,
                            item_id INTEGER,
                            shop_id INTEGER,
                            price DECIMAL,
                            warranty INTEGER,
                            date_update DATE)"""
INSERT_POSITION = "INSERT OR REPLACE INTO positions VALUES(?, ?, ?, ?, ?, ?)"
SELECT_POSITIONS = "SELECT * FROM positions"
SELECT_LAST_POSITIONS_BY_ITEM = """SELECT
                                    positions.id, positions.item_id, positions.shop_id, positions.price,
                                    positions.warranty, MAX(positions.date_update)
                                    FROM positions
                                    WHERE item_id=?
                                    GROUP BY shop_id
                                    ORDER BY price ASC"""
SELECT_DISPLAYED_POSITIONS_BY_ITEM = """SELECT
                            positions.id, positions.shop_id, positions.price, positions.warranty, positions.date_update,
                            shops.title, shops.html_url, shops.reviews_rating, shops.reviews_count
                            FROM positions
                            LEFT JOIN shops ON positions.shop_id = shops.id
                            WHERE positions.item_id = ?
                            GROUP BY shop_id
                            ORDER BY price"""
DELETE_POSITION = "DELETE FROM positions WHERE item_id=?"
DROP_TABLE_POSITIONS = "DROP TABLE IF EXISTS positions"

# USERS
CREATE_TABLE_USERS = """CREATE TABLE IF NOT EXISTS users(
                            id INTEGER PRIMARY KEY,
                            chat_id INTEGER,
                            email TEXT,
                            price_threshold DECIMAL,
                            currency_abbreviation TEXT)"""
INSERT_USER = "INSERT OR REPLACE INTO users VALUES(?, ?, ?, ?, ?)"
SELECT_USERS = "SELECT * FROM users"
SELECT_USERS_BY_ID = "SELECT * FROM users WHERE id=?"
DELETE_USER = "DELETE FROM users WHERE id=?"
DROP_TABLE_USERS = "DROP TABLE IF EXISTS users"

# PARSING ITEMS
CREATE_TABLE_PARSING_ITEMS = "CREATE TABLE IF NOT EXISTS parsing_items(item TEXT PRIMARY KEY)"
INSERT_PARSING_ITEM = "INSERT OR REPLACE INTO parsing_items VALUES(?)"
SELECT_PARSING_ITEMS = "SELECT * FROM parsing_items"
DELETE_PARSING_ITEM = "DELETE FROM parsing_items WHERE item=?"
