import traceback

from ClientLauncher.MainFunctions.windows import Windows

from ClientLauncher.ClientActions.main_lobby import TournamentActions, LobbyActions
from ClientLauncher.TablesController.hand_history_controller import TablesControl, InstantHandHistoryController

from ClientLauncher.Google.Sheets.get_statistics import GetStatistics
from ClientLauncher.Google.Sheets.write_statistics import WriteStatistics

from ClientLauncher.Naming.create_file_name import CreateFileName

from ClientLauncher.Database.deals import DealsAndFiles

from ClientLauncher.extensions.work_statuses import *
from ClientLauncher.extensions.duplicates import delete_duplicates

from datetime import datetime

import time
import json
import os

import logging


logging.basicConfig(level=print(), filename=f'logs\\main_{datetime.now().strftime("%d_%m_%Y")}.log',
                    filemode='a',  format="%(asctime)s %(levelname)s %(message)s")

with open('tournaments_data.json') as w:
    d = json.load(w).get('3729120825')


file_name = CreateFileName()
print('CreateFileName инициализирован')

tournament_actions = TournamentActions()
print('TournamentActions инициализирован')

tables_control = TablesControl()
print('TablesControl инициализирован')

instant_history_controller = InstantHandHistoryController()
print('InstantHandHistoryController инициализирован')

while True:
    try:
        get_statistics = GetStatistics()
        print('GetStatistics инициализирован')
        break
    except Exception as e:
        logging.warning("GetStatistics не удалось инициализировать", exc_info=True)

while True:
    try:
        write_statistics = WriteStatistics()
        print('WriteStatistics инициализирован')
        break
    except Exception as e:
        logging.warning("WriteStatistics не удалось инициализировать", exc_info=True)

deals_and_files = DealsAndFiles()
print('DealsAndFiles инициализирован')

windows = Windows()
print('Windows инициализирован')

closed_tables = []

num = 0


def cleanup_tournaments_data():
    with open('tournaments_data.json', 'w') as tournament_data_json:
        tournament_data_json.write('{}')


def add_new_tables(amount_of_tables, num):
    windows.get_main_window()
    print('Главное окно получено')
    print('Переход к открытию новых столов')

    try:
        num = tournament_actions.switch_tournaments(amount_of_tables, num)
    except Exception:
        logging.error('Ошибка при открытии турнира', exc_info=True)

    time.sleep(2)
    return num


def get_closed_tables_file():
    try:
        with open('closed_tables.txt', 'r') as closed_tables_txt:
            tables = closed_tables_txt.read().split('\n')
            return [table_row for table_row in tables if table_row != '']
    except AttributeError as e:
        print('closed tables пустой', e)
        return []


def change_closed_tables(table_id):
    tables = get_closed_tables_file()
    a = []
    for i in tables:
        if table_id == i:
            continue
        a.append(i)
    a.append('\n')
    with open('closed_tables.txt', 'w') as closed_tables_txt:
        closed_tables_txt.write('\n'.join(a))


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
    print('Открытие Instant HandHistory')
    instant_history_controller.open_instant_hand_history_menu()
    time.sleep(2)

    if tables_control.get_closed_table_in_hand_history_menu(data) is not False:
        print('Стол найден')
        deal = tables_control.get_table_deal()
        print('Раздачи скопированы')
        write_deals_in_file(deal, data[0], data[1])
        print('Раздачи записаны в файл')
        deals_and_files.add_file()
        del deal
    else:
        logging.warning('Не удалось найти стол')


def write_files_per_time():
    amount_of_files_per_hour = deals_and_files.get_amount_files_for_time()
    amount_of_files_per_days = deals_and_files.get_amount_files_for_time(True)

    write_statistics.set_files_per_time(amount_of_files_per_days, amount_of_files_per_hour)


def write_deals_per_time():
    amount_of_deals_hour = deals_and_files.get_amount_deals_for_time()
    amount_of_deals_days = deals_and_files.get_amount_deals_for_time(True)

    write_statistics.set_deals_per_time(amount_of_deals_days, amount_of_deals_hour)


def main():
    windows.get_main_window()

    LobbyActions.reset_wight()
    print('Ширина стоблцов сброшена')

    cleanup_tournaments_data()
    print('JSON файл с данными турниров очищен')

    print('Список турниров в файле очищен')
    num = 0
    opened_tables = get_statistics.get_open_tables()
    print(f'На данный момент открыто {opened_tables} столов')

    while True:
        LobbyActions.close_banner()
        print('Произведена попытка нажать на крестик банера')
        try:
            try:
                print('Получение открытых столов из таблицы')
                opened_tables = get_statistics.get_open_tables()
                print(f'В таблице открыто {opened_tables} столов')
            except Exception as e:
                print('Ошибка при получении открытых столов из таблицы')
                traceback.print_exc()
                continue

            if len(get_closed_tables_file()) > 0:
                print('Есть столы в списке закрытых')

                write_files_per_time()
                print('Записаны файлы за время в таблицу')
                write_deals_per_time()
                print('Записаны раздачи за время в таблицу')

                write_statistics.set_status(COLLECT_DEALS)
                print('Задан статус сбора раздач')

                while len(get_closed_tables_file()):
                    for i in get_closed_tables_file():
                        print(f'Попытка найти строку для {i}')
                        try:
                            change_closed_tables(i)
                            print('Стол удален из списка')
                        except IndexError:
                            print('Список пустой')
                            break

                        text = i.split(' ')
                        handle_closed_tables(text, opened_tables)

            if opened_tables < 21:
                print('Колличество столов меньше чем 21')
                write_statistics.set_status(OPENING_TOURNEYS)
                print('Задан статус открытия турнира')

                write_files_per_time()
                print('Записаны файлы за время в таблицу')
                write_deals_per_time()
                print('Записаны раздачи за время в таблицу')

                amount_of_add_tables = 21 - opened_tables
                num = add_new_tables(amount_of_add_tables, num)

            else:
                write_files_per_time()
                print('Записаны файлы за время в таблицу')
                write_deals_per_time()
                print('Записаны раздачи за время в таблицу')

                write_statistics.set_status(WAITING)
                print('Задан статус ожидания открытых столов')

        except Exception:
            write_statistics.set_status(BREAK)
            print('Задан статус сломался')
            traceback.print_exc()
            return


if __name__ == '__main__':
    main()
