import mysql.connector

HOST = '193.233.75.95'
USERNAME = 'ps123321'
PASSWORD = 'qwert'


class AddTable:
    def add(self, tournament_id: str, table: str):
        _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
        _connection.autocommit = True
        cursor = _connection.cursor()

        query = f"INSERT INTO poker.opened_tables (tournament_id, table_num) VALUES "\
                f"('{tournament_id}', {table});"

        cursor.execute(query)

        _connection.disconnect()
