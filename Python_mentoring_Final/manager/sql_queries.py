# ITEMS
CREATE_TABLE_ITEMS = """CREATE TABLE IF NOT EXISTS items(
                            id INTEGER PRIMARY KEY,
                            key TEXT,
                            extended_name TEXT,
                            price DECIMAL,
                            html_url TEXT)
                        """
INSERT_ITEM = "INSERT OR REPLACE INTO items VALUES(?, ?, ?, ?, ?)"
SELECT_ITEMS = "SELECT * FROM items"
SELECT_ITEM = "SELECT * FROM items WHERE key=?;"
DROP_TABLE_ITEMS = "DROP TABLE IF EXISTS items"
DELETE_ITEM = "DELETE FROM items WHERE key=?;"

# CURRENCIES
CREATE_TABLE_CURRENCIES = """CREATE TABLE IF NOT EXISTS currencies(
                            date DATE PRIMARY KEY,
                            abbreviation TEXT,
                            rate DECIMAL)
                        """
INSERT_CURRENCY = "INSERT OR REPLACE INTO currencies VALUES(?, ?, ?)"
SELECT_CURRENCIES = "SELECT * FROM currencies"
DROP_TABLE_CURRENCIES = "DROP TABLE IF EXISTS currencies"
DELETE_CURRENCY = "DELETE FROM items WHERE abbreviation=?"

# SHOPS
CREATE_TABLE_SHOPS = """CREATE TABLE IF NOT EXISTS shops(
                            id INTEGER PRIMARY KEY,
                            title TEXT,
                            html_url TEXT,
                            reviews_rating DECIMAL,
                            reviews_count INTEGER)
                        """
INSERT_SHOP = "INSERT OR REPLACE INTO shops VALUES(?, ?, ?, ?, ?)"
SELECT_SHOPS = "SELECT * FROM shops"
DROP_TABLE_SHOPS = "DROP TABLE IF EXISTS shops"
DELETE_SHOP = "DELETE FROM shops WHERE id=?"

# POSITIONS
CREATE_TABLE_POSITIONS = """CREATE TABLE IF NOT EXISTS positions(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            item_id INTEGER,
                            shop_id INTEGER,
                            price DECIMAL,
                            warranty INTEGER,
                            date_update DATE)
                        """
INSERT_POSITION = "INSERT OR REPLACE INTO positions(item_id, shop_id, price, warranty, date_update) VALUES(?, ?, ?, ?, ?)"
SELECT_POSITIONS = "SELECT * FROM positions"
SELECT_POSITIONS_BY_ITEM = "SELECT * FROM positions WHERE item_id=? ORDER BY price ASC"
DROP_TABLE_POSITIONS = "DROP TABLE IF EXISTS positions"
DELETE_POSITION = "DELETE FROM positions WHERE product_id=?"
