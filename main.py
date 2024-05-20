from ClientLauncher.MainFunctions.windows import Windows

from ClientLauncher.ClientActions.main_lobby import TournamentActions
from ClientLauncher.TablesController.hand_history_controller import TablesControl, InstantHandHistoryController

from ClientLauncher.Google.Sheets.get_statistics import GetStatistics
from ClientLauncher.Google.Sheets.write_statistics import WriteStatistics

from ClientLauncher.Naming.create_file_name import CreateFileName

from ClientLauncher.Database.deals import DealsAndFiles

from ClientLauncher.extensions.work_statuses import *
from ClientLauncher.extensions.duplicates import delete_duplicates

import time
import json
import os


with open('tournaments_data.json') as w:
    d = json.load(w).get('3729120825')


file_name = CreateFileName()

tournament_actions = TournamentActions()
tables_control = TablesControl()
instant_history_controller = InstantHandHistoryController()

while True:
    try:
        get_statistics = GetStatistics()
        break
    except Exception as e:
        print(f'Ошибка при инициализации GetStatistics {e}')

while True:
    try:
        write_statistics = WriteStatistics()
        break
    except Exception as e:
        print(f'Ошибка при инициализации WriteStatistics {e}')

deals_and_files = DealsAndFiles()

windows = Windows()
closed_tables = []


def cleanup_tournaments_data():
    with open('tournaments_data.json', 'w') as tournament_data_json:
        tournament_data_json.write('{}')


def add_new_tables(amount_of_tables, num):
    windows.get_main_window()
    num = tournament_actions.switch_tournaments(amount_of_tables, num)
    #instant_history_controller.open_instant_hand_history_menu()
    time.sleep(2)
    return num


def get_closed_tables_file():
    try:
        with open('closed_tables.txt') as closed_tables_txt:
            tables =  closed_tables_txt.read().split('\n')
            return [table_row for table_row in tables if table_row != '']
    except AttributeError as e:
        print('closed tables пустой', e)
        return []

def change_closed_tables(table_id):
    tables = get_closed_tables_file()
    a = ''
    for i in tables:
        if table_id in i:
            continue
        a += i

    with open('closed_tables.txt', 'w') as closed_tables_txt:
        closed_tables_txt.write(a)


def write_deals_in_file(deals, tournament_id, table_num):
    print(f'deals, tournament_id, table_num {deals, tournament_id, table_num}')
    files = os.listdir('deals_files')
    file = ''
    for i in files:
        if tournament_id in i and f'T{table_num}' in i:
            file = i
    deals = '\n'.join(deals)
    if file == '':
        print('Нет такого файла')
        return
    with open(f'deals_files\\{file}', 'w', encoding='utf-8') as deals_file_txt:
        deals_file_txt.write(deals)

    delete_duplicates(f'deals_files\\{file}')


def handle_closed_tables(data, opened_tables: int):
    print('opened tables изменен')
    instant_history_controller.open_instant_hand_history_menu()
    time.sleep(2)
    if tables_control.get_closed_table_in_hand_history_menu(data) is not False:
        deal = tables_control.get_table_deal()
        write_deals_in_file(deal, data[0], data[1])
        deals_and_files.add_file()
        del deal


def write_files_per_time():
    amount_of_files_per_hour = deals_and_files.get_amount_files_for_time()
    amount_of_files_per_days = deals_and_files.get_amount_files_for_time(True)

    write_statistics.set_files_per_time(amount_of_files_per_days, amount_of_files_per_hour)


def write_deals_per_time():
    amount_of_deals_hour = deals_and_files.get_amount_deals_for_time()
    amount_of_deals_days = deals_and_files.get_amount_deals_for_time(True)

    write_statistics.set_deals_per_time(amount_of_deals_days, amount_of_deals_hour)


def main():
    cleanup_tournaments_data()
    num = 0
    opened_tables = get_statistics.get_open_tables()
    if opened_tables < 21:
        amount_of_add_tables = 21 - opened_tables
        add_new_tables(amount_of_add_tables, num)

    while True:
        try:
            time.sleep(30)
            try:
                opened_tables = get_statistics.get_open_tables()
            except Exception as e:
                print(e)
                continue
            if opened_tables < 21:
                write_statistics.set_status(OPENING_TOURNEYS)

                write_files_per_time()
                write_deals_per_time()

                amount_of_add_tables = 21 - opened_tables
                num = add_new_tables(amount_of_add_tables, num)

            if len(get_closed_tables_file()) > 0:
                write_files_per_time()
                write_deals_per_time()

                write_statistics.set_status(COLLECT_DEALS)
                while len(get_closed_tables_file()):
                    for i in get_closed_tables_file():
                        try:
                            change_closed_tables(i[0])
                        except IndexError:
                            print('список пустой')
                            break
                        text = i.split(' ')
                        handle_closed_tables(text, opened_tables)

            else:
                write_files_per_time()
                write_deals_per_time()
                write_statistics.set_status(WAITING)

        except Exception as e:
            write_statistics.set_status(BREAK)
            print(e)
            return


if __name__ == '__main__':
    os.system('')
    main()
