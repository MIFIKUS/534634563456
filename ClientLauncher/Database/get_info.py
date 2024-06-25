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
    @endless_error_handler
    def tournament_in_db(self, tournament_id: str) -> bool:
        _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
        _connection.autocommit = True
        cursor = _connection.cursor()
        query = f"SELECT * FROM {database_name}.archives WHERE tournament_id = '{tournament_id}';"

        cursor.execute(query)

        result = cursor.fetchall()

        _connection.disconnect()

        if len(result) > 0:
            return True
        return False

    def table_in_db(self, tournament_id: str, table_num) -> bool:
        _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
        _connection.autocommit = True
        cursor = _connection.cursor()
        query = f"SELECT * FROM {database_name}.tables WHERE tournament_id = '{tournament_id}' AND table_num = {table_num};"

        cursor.execute(query)

        result = cursor.fetchall()

        _connection.disconnect()

        if len(result) > 0:
            return True
        return False

    @endless_error_handler
    def table_opened(self, tournament_id: str, table: str) -> bool:
        _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
        _connection.autocommit = True
        cursor = _connection.cursor()

        query = f"SELECT * FROM {database_name}.opened_tables WHERE tournament_id = '{tournament_id}' AND table_num = {table};"

        cursor.execute(query)

        result = cursor.fetchall()

        _connection.disconnect()

        if len(result) > 0:
            return True
        return False
