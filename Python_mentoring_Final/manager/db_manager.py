import logging
import sqlite3

import project_settings
from manager.sql_queries import CREATE_TABLE_ITEMS, CREATE_TABLE_CURRENCIES, CREATE_TABLE_SHOPS, \
    CREATE_TABLE_POSITIONS, CREATE_TABLE_USERS, CREATE_TABLE_PARSING_ITEMS

logging.basicConfig(filename=project_settings.LOG_FILE, format=project_settings.LOG_FORMAT,
                    level=project_settings.LOG_LEVEL)
_logger = logging.getLogger(__name__)


class DatabaseManager:
    _create_all_tables = (CREATE_TABLE_ITEMS, CREATE_TABLE_CURRENCIES, CREATE_TABLE_SHOPS, CREATE_TABLE_POSITIONS,
                          CREATE_TABLE_USERS, CREATE_TABLE_PARSING_ITEMS)

    def __init__(self) -> None:
        super().__init__()
        for query in self._create_all_tables:
            self.create(query)

    @staticmethod
    def _execute_queries(query, parameters, *, select=False, many=False):
        try:
            with sqlite3.connect(project_settings.DATABASE_NAME) as connection:
                cursor = connection.cursor()
                if select:
                    answer = cursor.execute(query, parameters).fetchall()
                else:
                    if many:
                        answer = cursor.executemany(query, parameters).rowcount
                    else:
                        answer = cursor.execute(query, parameters).rowcount
                    connection.commit()
                return answer
        except sqlite3.Error as error:
            _logger.warning(f"An error occurred while executing a query to the database: {error}")

    def create(self, query, parameters=tuple()):
        return self._execute_queries(query, parameters)

    def create_many(self, query, parameters):
        return self._execute_queries(query, parameters, many=True)

    def read(self, query, parameters=tuple()):
        return self._execute_queries(query, parameters, select=True)

    def delete(self, query, parameters):
        return self._execute_queries(query, parameters)

    def delete_many(self, query, parameters):
        return self._execute_queries(query, parameters, many=True)
