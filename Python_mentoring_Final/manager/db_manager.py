import logging
import sqlite3

from manager.sql_queries import CREATE_TABLE_ITEMS, CREATE_TABLE_CURRENCIES, CREATE_TABLE_SHOPS, \
    CREATE_TABLE_POSITIONS, DROP_TABLE_ITEMS, DROP_TABLE_CURRENCIES, DROP_TABLE_SHOPS, DROP_TABLE_POSITIONS


class DatabaseManager:
    _create_all_tables = (CREATE_TABLE_ITEMS, CREATE_TABLE_CURRENCIES, CREATE_TABLE_SHOPS, CREATE_TABLE_POSITIONS)
    _drop_all_tables = (DROP_TABLE_ITEMS, DROP_TABLE_CURRENCIES, DROP_TABLE_SHOPS, DROP_TABLE_POSITIONS)
    _logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        super().__init__()
        for query in self._create_all_tables:
            self.execute_queries(query)

    def execute_queries(self, query, parameters=tuple(), *, many=False):
        try:
            with sqlite3.connect('mydatabase.db') as connection:
                cursor = connection.cursor()
                if many:
                    answer = cursor.executemany(query, parameters).rowcount
                else:
                    answer = cursor.execute(query, parameters).fetchall()
                connection.commit()
                return answer
        except sqlite3.Error as error:
            self._logger.warning(f"An error occurred while executing a query to the database: {error}")
