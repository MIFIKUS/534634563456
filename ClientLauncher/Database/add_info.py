from ClientLauncher.Database.get_info import GetInfo
from ClientLauncher.extensions.error_handler import endless_error_handler
import mysql.connector
import traceback

HOST = '193.233.75.95'
USERNAME = 'ps123321'
PASSWORD = 'qwert'

get_info = GetInfo()


class AddInfo:
    while True:
        try:
            _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
            _connection.autocommit = True
            cursor = _connection.cursor()
            break
        except Exception:
            traceback.print_exc()

    @endless_error_handler
    def add_main_archive_info(self, data: dict):
        _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
        _connection.autocommit = True
        cursor = _connection.cursor()

        tournament_id = data['tournament_id']
        print(f'tournament_id {tournament_id}')
        name = data['name']
        print(f'name {name}')
        gtd = data['gtd']
        print(f'gtd {gtd}')
        buy_in = data['buy_in']
        print(f'buy_in {buy_in}')
        total_buy_in = data['total_buy_in']
        print(f'total buy_in {total_buy_in}')
        table_size = data['table_size']
        print(f'table_size {table_size}')
        speed = data['speed']
        print(f'speed {speed}')
        tournament_type = data['type']
        print(f'tournament_type {tournament_type}')
        archive_name = data['archive_name']
        print(f'archive_name {archive_name}')
        if not get_info.tournament_in_db(tournament_id):

            query = "INSERT INTO poker.archives (tournament_id, name, gtd, buy_in, total_buy_in, table_size, speed, tournament_type, archive_name, create_date)"\
                    f" VALUES ('{tournament_id}', '{name}', '{gtd}', '{buy_in}', '{total_buy_in}', {table_size}, '{speed}', '{tournament_type}'," \
                    f"'{archive_name}', NOW());"

            print(query)
            cursor.execute(query)

        _connection.disconnect()

    @endless_error_handler
    def add_additional_archive_info(self, data: dict):
        _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
        _connection.autocommit = True
        cursor = _connection.cursor()

        tournament_id = data['tournament_id']
        files_in_archive = data['files_in_archive']
        hands = data['hands']

        query = "UPDATE poker.archives SET "\
                f"files_in_archive = {files_in_archive}, "\
                f"hands = {hands} ,"\
                f"modify_date = NOW()"\
                f"WHERE tournament_id = '{tournament_id}'"

        cursor.execute(query)

        _connection.disconnect()

    def add_tables_info(self, data: dict):
        while True:
            try:
                _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
                _connection.autocommit = True
                cursor = _connection.cursor()
                break
            except Exception:
                traceback.print_exc()

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

        if not get_info.table_in_db(tournament_id, table_num):

            gtd = gtd.replace(' ', '')
            gtd = gtd.replace(',', '')

            query = "INSERT INTO poker.tables (tournament_id, name, gtd, buy_in, total_buy_in, table_size, speed, " \
                    "tournament_type, file_name, hands, create_date, script_name, table_num)" \
                    f"(VALUES ({tournament_id}, {name}, {gtd}, {buy_in}, {total_buy_in}, {table_size}, {speed}, {tournament_type}," \
                    f"{file_name}, {hands}, {create_data}, {script_name}, {table_num});"

            while True:
                try:
                    cursor.execute(query)
                    break
                except Exception as e:
                    print(e)

            _connection.disconnect()

    @endless_error_handler
    def add_tables_main_info(self, data: dict):
        _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
        _connection.autocommit = True
        cursor = _connection.cursor()

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

        gtd = gtd.replace(' ', '')
        gtd = gtd.replace(',', '')

        if not get_info.table_in_db(tournament_id, table_num):
            query = "INSERT INTO poker.tables (tournament_id, table_num, name, gtd, buy_in, total_buy_in, table_size, speed, tournament_type, hands, file_name, script_name, create_date)"\
                    f" VALUES ('{tournament_id}', {table_num}, '{name}', '{gtd}', '{buy_in}', '{total_buy_in}', {table_size}, '{speed}', '{tournament_type}', {hands}, "\
                    f"'{file_name}', '{script_name}', NOW());"

            cursor.execute(query)

        _connection.disconnect()

    def add_tables_additional_info(self, data: dict):
        while True:
            try:
                _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
                _connection.autocommit = True
                cursor = _connection.cursor()
                break
            except Exception:
                traceback.print_exc()

        tournament_id = data['tournament_id']
        files_in_archive = data['files_in_archive']
        hands = data['hands']

        query = "UPDATE poker.tables SET "\
                f"files_in_archive = {files_in_archive}, "\
                f"hands = {hands} "\
                f"WHERE tournament_id = '{tournament_id}'"

        while True:
            try:
                cursor.execute(query)
                break
            except Exception as e:
                print(e)

        _connection.disconnect()
