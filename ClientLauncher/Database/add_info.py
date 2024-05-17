import mysql.connector
from ClientLauncher.Database.get_info import GetInfo


HOST = '193.233.75.95'
USERNAME = 'ps123321'
PASSWORD = 'qwert'

get_info = GetInfo()


class AddInfo:
    def __init__(self):
        self._connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
        self._connection.autocommit = True
        self.cursor = self._connection.cursor()

    def add_main_archive_info(self, data: dict):
        tournament_id = data['tournament_id']
        name = data['name']
        gtd = data['gtd']
        buy_in = data['buy_in']
        total_buy_in = data['total_buy_in']
        table_size = data['table_size']
        speed = data['speed']
        tournament_type = data['type']
        archive_name = data['archive_name']

        if not get_info.tournament_in_db(tournament_id):

            query = "INSERT INTO poker.archives (tournament_id, name, gtd, buy_in, total_buy_in, table_size, speed, tournament_type, archive_name, create_date)"\
                    f" VALUES ('{tournament_id}', '{name}', '{gtd}', '{buy_in}', '{total_buy_in}', {table_size}, '{speed}', '{tournament_type}'," \
                    f"'{archive_name}', NOW());"

            print(query)

            while True:
                try:
                    self.cursor.execute(query)
                    break
                except Exception as e:
                    print(e)

    def add_additional_archive_info(self, data: dict):
        tournament_id = data['tournament_id']
        files_in_archive = data['files_in_archive']
        hands = data['hands']

        query = "UPDATE poker.archives SET "\
                f"files_in_archive = {files_in_archive}, "\
                f"hands = {hands} ,"\
                f"modify_date = NOW()"\
                f"WHERE tournament_id = '{tournament_id}'"
        while True:
            try:
                self.cursor.execute(query)
                break
            except Exception as e:
                print(e)

    def add_tables_info(self, data: dict):
        tournament_id = data['tournament_id']
        table_num = data['table_num']
        name = data['name']
        gtd = data['gtd']
        buy_in = data['buy_in']
        total_buy_in = data['total_buy_in']
        table_size = data['table_size']
        speed = data['speed']
        tournament_type = data['type']
        file_name = data['file_name']
        hands = data['hands']
        script_name = data['script_name']
        create_data = data['create_date']

        query = "INSERT INTO poker.tables (tournament_id, name, gtd, buy_in, total_buy_in, table_size, speed, " \
                "tournament_type, file_name, hands, create_date, script_name, table_num)" \
                f"(VALUES ({tournament_id}, {name}, {gtd}, {buy_in}, {total_buy_in}, {table_size}, {speed}, {tournament_type}," \
                f"{file_name}, {hands}, {create_data}, {script_name}, {table_num});"

        while True:
            try:
                self.cursor.execute(query)
                break
            except Exception as e:
                print(e)

    def add_tables_main_info(self, data: dict):
        tournament_id = data['tournament_id']
        name = data['name']
        table_num = data['table_num']
        gtd = data['gtd']
        buy_in = data['buy_in']
        total_buy_in = data['total_buy_in']
        table_size = data['table_size']
        speed = data['speed']
        tournament_type = data['type']
        file_name = data['file_name']
        script_name = data['script_name']
        hands = data['hands']

        query = "INSERT INTO poker.tables (tournament_id, table_num, name, gtd, buy_in, total_buy_in, table_size, speed, tournament_type, hands, file_name, script_name, create_date)"\
                f" VALUES ('{tournament_id}', {table_num}, '{name}', '{gtd}', '{buy_in}', '{total_buy_in}', {table_size}, '{speed}', '{tournament_type}', {hands}, "\
                f"'{file_name}', '{script_name}', NOW());"


        while True:
            try:
                self.cursor.execute(query)
                break
            except Exception as e:
                print(e)

    def add_tables_additional_info(self, data: dict):
        tournament_id = data['tournament_id']
        files_in_archive = data['files_in_archive']
        hands = data['hands']

        query = "UPDATE poker.tables SET "\
                f"files_in_archive = {files_in_archive}, "\
                f"hands = {hands} "\
                f"WHERE tournament_id = '{tournament_id}'"

        while True:
            try:
                self.cursor.execute(query)
                break
            except Exception as e:
                print(e)
