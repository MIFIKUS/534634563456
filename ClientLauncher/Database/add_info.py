from ClientLauncher.Database.get_info import GetInfo

from ClientLauncher.extensions.error_handler import endless_error_handler
from ClientLauncher.extensions.get_config_data import get_pokerstars_version

import mysql.connector
import traceback

HOST = '193.233.75.95'
USERNAME = 'ps123321'
PASSWORD = 'qwert'

get_info = GetInfo()


if get_pokerstars_version().upper() == 'ES':
    database_name = 'pokerstars_es'
else:
    database_name = 'poker'


class AddInfo:
    while True:
        try:
            _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
            _connection.autocommit = True
            cursor = _connection.cursor()
            break
        except Exception:
            traceback.print_exc()

    def add_main_archive_info(self, data: dict):
        while True:
            try:
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

                    query = f"INSERT INTO {database_name}.archives (tournament_id, name, gtd, buy_in, total_buy_in, table_size, speed, tournament_type, archive_name, create_date)"\
                            f" VALUES ('{tournament_id}', '{name}', '{gtd}', '{buy_in}', '{total_buy_in}', {table_size}, '{speed}', '{tournament_type}'," \
                            f"'{archive_name}', NOW());"

                    print(f'add_main_archive_info query {query}')
                    cursor.execute(query)

                _connection.disconnect()
                break
            except Exception:
                traceback.print_exc()

    def add_additional_archive_info(self, data: dict):
        while True:
            try:
                _connection = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD)
                _connection.autocommit = True
                cursor = _connection.cursor()

                tournament_id = data['tournament_id']
                files_in_archive = data['files_in_archive']
                hands = data['hands']

                query = f"UPDATE {database_name}.archives SET "\
                        f"files_in_archive = {files_in_archive}, "\
                        f"hands = {hands} ,"\
                        f"modify_date = NOW()"\
                        f"WHERE tournament_id = '{tournament_id}'"

                print(f'add_additional_archive_info query {query}')

                cursor.execute(query)

                _connection.disconnect()
                break
            except Exception:
                traceback.print_exc()

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

            query = f"INSERT INTO {database_name}.tables (tournament_id, name, gtd, buy_in, total_buy_in, table_size, speed, " \
                    "tournament_type, file_name, hands, create_date, script_name, table_num)" \
                    f"(VALUES ({tournament_id}, {name}, {gtd}, {buy_in}, {total_buy_in}, {table_size}, {speed}, {tournament_type}," \
                    f"{file_name}, {hands}, {create_data}, {script_name}, {table_num});"

            print(f'add_tables_info query {query}')

            while True:
                try:
                    cursor.execute(query)
                    break
                except Exception as e:
                    print(e)

            _connection.disconnect()

    def add_tables_main_info(self, data: dict):
        while True:
            try:
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
                    query = f"INSERT INTO {database_name}.tables (tournament_id, table_num, name, gtd, buy_in, total_buy_in, table_size, speed, tournament_type, hands, file_name, script_name, create_date)"\
                            f" VALUES ('{tournament_id}', {table_num}, '{name}', '{gtd}', '{buy_in}', '{total_buy_in}', {table_size}, '{speed}', '{tournament_type}', {hands}, "\
                            f"'{file_name}', '{script_name}', NOW());"

                    print(f'add_tables_main_info query {query}')
                    cursor.execute(query)

                _connection.disconnect()
                break
            except Exception:
                traceback.print_exc()

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

        query = f"UPDATE {database_name}.tables SET "\
                f"files_in_archive = {files_in_archive}, "\
                f"hands = {hands} "\
                f"WHERE tournament_id = '{tournament_id}'"

        print(f'add_tables_additional_info query {query}')

        while True:
            try:
                cursor.execute(query)
                break
            except Exception as e:
                print(e)

        _connection.disconnect()
