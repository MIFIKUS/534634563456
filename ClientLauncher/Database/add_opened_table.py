from ClientLauncher.extensions.get_config_data import get_pokerstars_version, get_script_name
import mysql.connector

HOST = '147.78.67.17'
USERNAME = 'poker'
PASSWORD = 'root'

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
        while True:
            try:
                _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
                _connection.autocommit = True
                cursor = _connection.cursor()

                query = f"INSERT INTO {database_name}.opened_tables (tournament_id, table_num, script_name, date, is_collected) VALUES "\
                        f"('{tournament_id}', {table}, '{SCRIPT_NAME}', NOW(), 0);"

                print(f'add query {query}')

                cursor.execute(query)

                _connection.disconnect()
                break
            except:
                pass

    @staticmethod
    def set_table_collected_status(tournament_id: str, table: str):
        if not table or not tournament_id:
            print(f'Нету айди турнира или номера стола чтобы добавить его в бд tournament_id {tournament_id} table {table}')
            return

        while True:
            try:
                _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
                _connection.autocommit = True
                cursor = _connection.cursor()

                query = f"UPDATE {database_name}.opened_tables SET "\
                        f"is_collected = 1 WHERE tournament_id = '{tournament_id}' AND table_num = {table};"

                print(f'set_table_collected_status query {query}')

                cursor.execute(query)

                _connection.disconnect()
                break
            except:
                pass
