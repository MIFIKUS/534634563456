import sqlite3
from ClientLauncher.Google.Sheets.get_config import GetConfig


while True:
    try:
        config = GetConfig()
        break
    except Exception as e:
        print(f"Ошибка при инициализации GetConfig {e}")


class DealsAndFiles:
    def __init__(self):
        self._database_name = 'deals_data.db'

    def add_deal(self):
        connection = self._get_connection()
        cursor = self._get_cursor(connection)

        query = "INSERT INTO deals (date) VALUES (datetime('now'));"

        cursor.execute(query)
        connection.commit()

        self._close_connection(connection)

    def get_amount_deals_for_time(self):
        amount_of_time_to_collect = int(config.get_collect_data()['deals_per_days']) * 24
        connection = self._get_connection()
        cursor = self._get_cursor(connection)

        query = f"""SELECT * 
FROM deals 
WHERE date >= datetime('now', '-{amount_of_time_to_collect} hour');"""

        cursor.execute(query)

        deals = cursor.fetchall()

        self._close_connection(connection)

        return len(deals)

    def add_file(self):
        connection = self._get_connection()
        cursor = self._get_cursor(connection)

        query = "INSERT INTO files (date) VALUES (datetime('now'));"

        cursor.execute(query)
        connection.commit()

        self._close_connection(connection)

    def get_amount_files_for_time(self):
        amount_of_time_to_collect = int(config.get_collect_data()['files_per_hour'])

        connection = self._get_connection()
        cursor = self._get_cursor(connection)

        query = f"""SELECT * 
FROM files 
WHERE date >= datetime('now', '-{amount_of_time_to_collect} hour');"""

        cursor.execute(query)
        files = cursor.fetchall()

        self._close_connection(connection)

        return len(files)

    def _get_connection(self):
        return sqlite3.connect(self._database_name)

    def _get_cursor(self, connection):
        return connection.cursor()

    def _close_connection(self, connection):
        connection.close()

    def _commit(self, connection):
        connection.commit()

