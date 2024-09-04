from ClientLauncher.extensions.get_config_data import get_pokerstars_version, get_script_name
import mysql.connector

HOST = '193.233.75.95'
USERNAME = 'ps123321'
PASSWORD = 'qwert'

SCRIPT_NAME = get_script_name()

if get_pokerstars_version().upper() == 'ES':
    database_name = 'pokerstars_es'
else:
    database_name = 'poker'


class AddTable:
    def add(self, tournament_id: str, table: str):
        if not table or not tournament_id:
            print(f'Нету айди турнира или номера стола чтобы добавить его в бд tournament_id {tournament_id} table {table}')
            return
        _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
        _connection.autocommit = True
        cursor = _connection.cursor()

        query = f"INSERT INTO {database_name}.opened_tables (tournament_id, table_num, script_name, date) VALUES "\
                f"('{tournament_id}', {table}, '{SCRIPT_NAME}', NOW());"

        print(f'add query {query}')

        cursor.execute(query)

        _connection.disconnect()
