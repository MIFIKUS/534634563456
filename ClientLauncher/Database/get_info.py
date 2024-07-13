import traceback

from ClientLauncher.extensions.error_handler import endless_error_handler
from ClientLauncher.extensions.get_config_data import get_pokerstars_version
import mysql.connector

HOST = '193.233.75.95'
USERNAME = 'ps123321'
PASSWORD = 'qwert'

if get_pokerstars_version().upper() == 'ES':
    database_name = 'pokerstars_es'
else:
    database_name = 'poker'


class GetInfo:
    def tournament_in_db(self, tournament_id: str) -> bool:
        while True:
            try:
                _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
                _connection.autocommit = True
                cursor = _connection.cursor()
                query = f"SELECT * FROM {database_name}.archives WHERE tournament_id = '{tournament_id}';"

                print(f'tournament_in_db query {query}')

                cursor.execute(query)

                result = cursor.fetchall()

                _connection.disconnect()

                if len(result) > 0:
                    return True
                return False
            except Exception:
                traceback.print_exc()

    def table_in_db(self, tournament_id: str, table_num) -> bool:
        while True:
            try:
                _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
                _connection.autocommit = True
                cursor = _connection.cursor()
                query = f"SELECT * FROM {database_name}.tables WHERE tournament_id = '{tournament_id}' AND table_num = {table_num};"

                print(f'table_in_db query {query}')

                cursor.execute(query)

                result = cursor.fetchall()

                _connection.disconnect()

                if len(result) > 0:
                    return True
                return False
            except Exception:
                traceback.print_exc()

    def table_opened(self, tournament_id: str, table: str) -> bool:
        while True:
            try:
                _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
                _connection.autocommit = True
                cursor = _connection.cursor()

                query = f"SELECT * FROM {database_name}.opened_tables WHERE tournament_id = '{tournament_id}' AND table_num = {table};"

                print(f'table_opened query {query}')

                cursor.execute(query)

                result = cursor.fetchall()

                _connection.disconnect()

                if len(result) > 0:
                    return True
                return False
            except Exception:
                traceback.print_exc()
