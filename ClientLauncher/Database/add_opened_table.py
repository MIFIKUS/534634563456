from ClientLauncher.extensions.get_config_data import get_pokerstars_version
import mysql.connector

HOST = '193.233.75.95'
USERNAME = 'ps123321'
PASSWORD = 'qwert'

if get_pokerstars_version().upper() == 'ES':
    database_name = 'pokerstars_es'
else:
    database_name = 'poker'


class AddTable:
    def add(self, tournament_id: str, table: str):
        _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
        _connection.autocommit = True
        cursor = _connection.cursor()

        query = f"INSERT INTO {database_name}.opened_tables (tournament_id, table_num) VALUES "\
                f"('{tournament_id}', {table});"

        print(f'add query {query}')

        cursor.execute(query)

        _connection.disconnect()
