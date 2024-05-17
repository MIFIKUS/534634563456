from ClientLauncher.MainFunctions.mouse_and_keyboard import Mouse, Keyboard
from ClientLauncher.MainFunctions.image import Image
from ClientLauncher.MainFunctions.windows import Windows

from ClientLauncher.Google.Sheets.write_statistics import WriteStatistics
from ClientLauncher.Google.Sheets.get_statistics import GetStatistics

from ClientLauncher.Database.deals import DealsAndFiles

from ClientLauncher.extensions.error_handler import do_without_error

from tkinter import Tk

from gspread.exceptions import APIError

import time
import re


mouse = Mouse()
keyboard = Keyboard()
windows = Windows()
image = Image()

clipboard = Tk()


while True:
    try:
        write_statistics = WriteStatistics()
        break
    except Exception as e:
        print(f'Ошибка при инициализации WriteStatistics {e}')

while True:
    try:
        get_statistics = GetStatistics()
        break
    except Exception as e:
        print(f'Ошибка при инициализации GetStatistics {e}')


deals_and_files = DealsAndFiles()


class InstantHandHistoryController:
    def open_instant_hand_history_menu(self):
        keyboard.ctrl_i()
        time.sleep(4)
        hwnd = windows.get_hwnd_by_name('Instant Hand History')
        windows.open_fullscreen_window_by_hwnd(hwnd)


class TablesControl:
    def get_closed_table(self):
        list_of_tables = windows.find_all_tables_windows()
        while True:
            try:
                tables = windows.find_all_tables_windows()
                closed_tables = list(set(list_of_tables) - set(tables))

                if closed_tables:
                    print('Есть разница в столах')
                    list_of_tables = tables
                else:
                    print('Нет разница в столах')
                    list_of_tables = tables
                    continue

                for i in closed_tables:
                    print(f'Обработка стола {i}')
                    info = i.split('  ')
                    table_id = ''.join(filter(str.isdigit, info[0]))
                    table_num = ''.join(filter(str.isdigit, info[1]))
                    print(f'table_id {table_id}')
                    print(f'table_num {table_num}')

                    self._write_closed_table(table_id, table_num)

                amount_of_tables = windows.get_amount_of_opened_tables()
                write_statistics.set_opened_tables(amount_of_tables)

            except APIError:
                print('Ошибка квоты, ждем 30 секунды')
                time.sleep(30)
            except AttributeError as e:
                print(f'Ошибка {e}')

    def get_closed_table_in_hand_history_menu(self, closed_table):
        def _reset_hand_history():
            mouse.move_and_click(1400, 60)
            keyboard.end()
            time.sleep(1)
            mouse.move_and_click(1400, 60)

        def _get_table_id_and_table(table_header):
            print(f'table_header {table_header}')

            table_id = table_header[0]
            table_num = table_header[1]

            return table_id, table_num

        table_id, table_num = _get_table_id_and_table(closed_table)
        table_num = table_num.replace(' ', '')
        table_num = table_num.replace('\n', '')
        table_num = 'Table' + table_num
        
        _reset_hand_history()

        table_names = []

        found = False
        while True:
            print(f'Поиск {table_id} Стол {table_num}')
            time.sleep(0.5)
            not_found = False
            try:
                image.take_screenshot('imgs\\screenshots\\instant_hand_history\\table_name.png', (5, 43, 670, 68))
                time.sleep(0.5)
            except Exception as e:
                print(e)
                _reset_hand_history()
                continue
            table_name = image.image_to_string('imgs\\screenshots\\instant_hand_history\\table_name.png', False)
            print(f'table_name {table_name}')
                
            if 'all' in table_name.lower():
                return False

            table_name = table_name.replace(' ', '')
            table_name = table_name.replace('\n', '')
            table_name = table_name.replace('.', '')
            table_name = table_name.replace(',', '')
                    
            try:
                table_name_for_seat = 'Table' + re.search(r'Table(.*)', table_name).group(1)
                    
            except AttributeError:
                print('Не удалось получить название стола')
                return False
            print(f'ID: {table_id} TABLE: {table_name_for_seat}')
            if table_id in table_name and table_num == table_name_for_seat:
                break
            if table_name in table_names:
                continue
            table_names.append(table_name)

            if not_found:
                return False
            if found:
                break

            keyboard.arrow_up()

    def get_table_deal(self):
        mouse.move_and_click(900, 120)

        keyboard.copy_fast()
        deals = []
        deal = do_without_error(clipboard.clipboard_get)

        deals.append(deal)

        while True:
            keyboard.arrow_down()
            same = 0
            for _ in range(2):
                keyboard.copy_fast()
                deal = do_without_error(clipboard.clipboard_get)

                if deal in deals:
                    same += 1
                else:
                    deals_and_files.add_deal()

                if same == 2:
                    return deals
                deals.append(deal)

                del deal

    def _write_closed_table(self, tournament_id, table_num):
        with open('closed_tables.txt', 'a') as closed_tables_txt:
            text = tournament_id + ' ' + str(table_num) + '\n'
            closed_tables_txt.write(text)
