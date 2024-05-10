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

    def add_main_archive_info(self, data:dict):
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

            self.cursor.execute(query)

    def add_additional_archive_info(self, data:dict):
        tournament_id = data['tournament_id']
        files_in_archive = data['files_in_archive']
        hands = data['hands']

        query = "UPDATE poker.archives SET "\
                f"files_in_archive = {files_in_archive}, "\
                f"hands = {hands} ,"\
                f"modify_date = NOW()"\
                f"WHERE tournament_id = '{tournament_id}'"
        print(query)
        self.cursor.execute(query)

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
        archive_name = data['archive_name']
        files_in_archive = data['files_in_archive']
        hands = data['hands']
        script_name = data['script_name']
        create_data = data['create_date']

        query = "INSERT INTO poker.tables (tournament_id, name, gtd, buy_in, total_buy_in, table_size, speed, " \
                "tournament_type, archive_name, files_in_archive, hands, create_date, script_name, table_num)" \
                f"(VALUES ({tournament_id}, {name}, {gtd}, {buy_in}, {total_buy_in}, {table_size}, {speed}, {tournament_type}," \
                f"{archive_name}, {files_in_archive}, {hands}, {create_data}, {script_name}, {table_num});"

        self.cursor.execute(query)

