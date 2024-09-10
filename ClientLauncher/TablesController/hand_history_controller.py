from ClientLauncher.MainFunctions.mouse_and_keyboard import Mouse, Keyboard
from ClientLauncher.MainFunctions.image import Image
from ClientLauncher.MainFunctions.windows import Windows

from ClientLauncher.Google.Sheets.write_statistics import WriteStatistics
from ClientLauncher.Google.Sheets.get_statistics import GetStatistics

from ClientLauncher.Database.deals import DealsAndFiles

from ClientLauncher.extensions.error_handler import do_without_error

from tkinter import Tk

from gspread.exceptions import APIError

from pywinauto.application import Application

import win32gui
import win32process

import time
import traceback


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
        while True:
            try:
                hwnd = windows.get_hwnd_by_name('Instant Hand History')
                windows.open_fullscreen_window_by_hwnd(hwnd)
                print(f'Instant Hand History открыт')
                break
            except:
                pass


class TablesControl:
    def get_closed_table(self):
        list_of_tables = windows.find_all_tables_windows()
        while True:
            try:
                tables = windows.find_all_tables_windows()
                closed_tables = list(set(list_of_tables) - set(tables))

                if closed_tables:
                    list_of_tables = tables
                else:
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
        def _get_table_id_and_table(table_header):
            print(f'table_header {table_header}')

            table_id = table_header[0]
            table_num = table_header[1]

            return table_id, table_num

        def _get_all_tables_from_check_box(app: Application) -> list:
            return app.child_window(class_name='ComboBox').texts()

        def _get_necessary_checkbox_text(tables: list or tuple,
                                         necessary_table: str, necessary_tournament_id: str) -> str:
            for i in tables:
                table_id = i.split(' ')[0].replace('T', '')
                table_num = i.split(' ')[- 1]
                print(f'Проверка подходит ли {table_id} {table_num}')
                if necessary_table == table_num and necessary_tournament_id == table_id:
                    print(f'Подходит {table_id} {table_num}')
                    return i
            print('Не найдено нужного стола')

        def _select_necessary_table(app: Application, table_name: str):
            try:
                print(f'Попытка выбрать стол {table_name}')
                app.child_window(class_name='ComboBox').select(table_name)
                print('Удалось выбрать стол')
            except Exception:
                print('Не удалось выбрать стол')

        while True:
            try:
                _, instant_hand_history_pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
                instant_hand_history_window = Application(backend='win32').connect(process=instant_hand_history_pid).InstantHandHistory
                break
            except:
                traceback.print_exc()
                pass

        table_id, table_num = _get_table_id_and_table(closed_table)
        table_num = table_num.replace(' ', '')
        table_num = table_num.replace('\n', '')

        print(f'Стол который нужно найти {table_id} {table_num}')

        available_tables = _get_all_tables_from_check_box(instant_hand_history_window)
        table_text = _get_necessary_checkbox_text(available_tables, table_num, table_id)

        print(f'table_text {table_text} type {type(table_text)}')

        if table_text:
            _select_necessary_table(instant_hand_history_window, table_text)
        else:
            return False

    def get_table_deal(self):
        while not windows.top_window_is_instant_hand_history():
            windows.open_instant_hand_history_menu()
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
                    deals.append(deal)

                if same == 5:
                    return deals

                del deal

    def _write_closed_table(self, tournament_id, table_num):
        with open('closed_tables.txt', 'a') as closed_tables_txt:
            text = tournament_id + ' ' + str(table_num) + '\n'
            closed_tables_txt.write(text)
