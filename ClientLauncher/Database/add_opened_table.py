import mysql.connector

HOST = '193.233.75.95'
USERNAME = 'ps123321'
PASSWORD = 'qwert'


class AddTable:
    def __init__(self):
        self._connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
        self._connection.autocommit = True
        self.cursor = self._connection.cursor()

    def add(self, tournament_id: str, table: str):
        query = f"INSERT INTO poker.opened_tables (tournament_id, table) VALUES "\
                f"('{tournament_id}', {table});"

        self.cursor.execute(query)
