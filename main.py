from ClientLauncher.MainFunctions.windows import Windows

from ClientLauncher.ClientActions.main_lobby import TournamentActions
from ClientLauncher.TablesController.hand_history_controller import TablesControl, InstantHandHistoryController

from ClientLauncher.Google.Sheets.get_config import GetConfig
from ClientLauncher.Google.Sheets.write_statistics import WriteStatistics
from ClientLauncher.Google.Sheets.get_statistics import GetStatistics
from ClientLauncher.Google.Sheets.write_statistics import WriteStatistics

from ClientLauncher.Naming.create_file_name import CreateFileName

from multiprocessing import Process

import time
import json
import os


with open('tournaments_data.json') as w:
    d = json.load(w).get('3729120825')


file_name = CreateFileName()


tournament_actions = TournamentActions()
tables_control = TablesControl()
instant_history_controller = InstantHandHistoryController()

get_statistics = GetStatistics()
write_statistics = WriteStatistics()

windows = Windows()
closed_tables = []


def cleanup_tournaments_data():
    with open('tournaments_data.json', 'w') as tournament_data_json:
        tournament_data_json.write('{}')

def add_new_tables(amount_of_tables):
    windows.get_main_window()
    tournament_actions.switch_tournaments(amount_of_tables)
    #instant_history_controller.open_instant_hand_history_menu()
    time.sleep(2)



def get_closed_tables_file():
    try:
        with open('closed_tables.txt') as closed_tables_txt:
            return closed_tables_txt.read().split('\n')
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

def handle_closed_tables(data, opened_tables: int):
    print('opened tables изменен')
    instant_history_controller.open_instant_hand_history_menu()
    time.sleep(2)
    if tables_control.get_closed_table_in_hand_history_menu(data) is not False:
        deal = tables_control.get_table_deal()
        write_deals_in_file(deal, data[0], data[2])

if __name__ == '__main__':
    cleanup_tournaments_data()

    opened_tables = get_statistics.get_open_tables()
    if opened_tables < 21:
        amount_of_add_tables = 21 - opened_tables
        add_new_tables(amount_of_add_tables)

    while True:
        list_of_tables = windows.find_all_tables_windows()
        time.sleep(30)
        try:
            opened_tables = get_statistics.get_open_tables()
        except Exception:
            continue
        if opened_tables < 21:
            amount_of_add_tables = 21 - opened_tables
            add_new_tables(amount_of_add_tables)
        elif len(get_closed_tables_file()) > 0:
            for i in get_closed_tables_file():
                try:
                    change_closed_tables(i[0])
                except IndexError:
                    print('список пустой')
                    break
                text = i.split(' ')
                handle_closed_tables(text, opened_tables)

        tables_control.get_closed_table(list_of_tables)