import mysql.connector

HOST = '193.233.75.95'
USERNAME = 'ps123321'
PASSWORD = 'qwert'


class GetInfo:
    def tournament_in_db(self, tournament_id: str) -> bool:
        _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
        _connection.autocommit = True
        cursor = _connection.cursor()
        query = f"SELECT * FROM poker.archives WHERE tournament_id = '{tournament_id}';"

        while True:
            try:
                self.cursor.execute(query)
                break
            except Exception as e:
                print(e)
        result = cursor.fetchall()

        _connection.disconnect()

        if len(result) > 0:
            return True
        return False

    def table_opened(self, tournament_id: str, table: str) -> bool:
        _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
        _connection.autocommit = True
        cursor = _connection.cursor()

        query = f"SELECT * FROM poker.opened_tables WHERE tournament_id = '{tournament_id}' AND table_num = {table};"
        while True:
            try:
                cursor.execute(query)
                break
            except Exception as e:
                print(e)
        result = cursor.fetchall()

        _connection.disconnect()

        if len(result) > 0:
            return True
        return False
