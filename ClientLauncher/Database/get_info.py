import mysql.connector

HOST = '193.233.75.95'
USERNAME = 'ps123321'
PASSWORD = 'qwert'


class GetInfo:
    def __init__(self):
        self._connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
        self._connection.autocommit = True
        self.cursor = self._connection.cursor()

    def tournament_in_db(self, tournament_id: str) -> bool:
        query = f"SELECT * FROM poker.archives WHERE tournament_id = '{tournament_id}';"

        self.cursor.execute(query)
        result = self.cursor.fetchall()

        if len(result) > 0:
            return True
        return False

    def table_opened(self, tournament_id: str, table: str) -> bool:
        query = f"SELECT * FROM poker.opened_tables WHERE tournament_id = '{tournament_id}' AND table_num = {table};"
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        if len(result) > 0:
            return True
        return False
