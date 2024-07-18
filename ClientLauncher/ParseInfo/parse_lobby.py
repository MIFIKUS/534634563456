from ClientLauncher.MainFunctions.image import Image
from ClientLauncher.MainFunctions.mouse_and_keyboard import Mouse, Keyboard
from ClientLauncher.MainFunctions.windows import Windows

from ClientLauncher.Database.get_info import GetInfo
from ClientLauncher.Database.add_opened_table import AddTable

from ClientLauncher.extensions.error_handler import do_without_error
from ClientLauncher.extensions.get_config_data import get_pokerstars_version

from tkinter import Tk

import win32gui

import string
import re
import time
import json
import os


image = Image()
mouse = Mouse()
keyboard = Keyboard()
windows = Windows()

get_info = GetInfo()
add_table = AddTable()

clipboard = Tk()


class ParseLobby:
    def __init__(self, hwnd, amount_of_opened_tables, tournament_id, file):
        self._hwnd = hwnd
        self._amount_of_opened_tables = amount_of_opened_tables
        self._tournament_id = tournament_id
        self._file = file
        self._lobby_window_size = (986, 729)
        self._lobby_cords = self._get_lobby_cords()
        self._lobby_window = ('Tournament', 'Lobby')

        self._table_x0 = 10 + self._lobby_cords[0]
        self._table_x1 = 45 + self._lobby_cords[0]
        self._table_y0 = 335 + self._lobby_cords[1]
        self._table_y1 = 350 + self._lobby_cords[1]

    def get_lobby_info(self) -> dict:
        lobby_id = self._get_lobby_id()
        tables_info = self._get_availible_tables()
        availible_tables = tables_info[0]
        tournament_name = tables_info[1]
        try:
            lobby_gtd = tables_info[2]
        except Exception:
            lobby_gtd = None

        opened_tables = self._amount_of_opened_tables + len(availible_tables)
        self._write_opened_tables(availible_tables, tournament_name, lobby_gtd)
        return {'id': lobby_id, 'availible_tables': availible_tables, 'opened_tables': opened_tables, 'tournament_name': tournament_name}

    def _get_lobby_id(self) -> str:
        lobby_text = win32gui.GetWindowText(self._hwnd)
        lobby_id = re.search(r'Tournament(.*?)Lobby', lobby_text, re.DOTALL).group(1).strip()
        return lobby_id

    def _get_lobby_cords(self) -> tuple:
        cords = win32gui.GetWindowRect(self._hwnd)
        return cords[0], cords[1]

    def _get_availible_tables(self):
        availible_tables = []
        tables_in_file = self._get_tables_from_file()
        print(tables_in_file)

        for _ in range(2):
            mouse.move_and_click(680, 160)

        time.sleep(1)

        for _ in range(5):
            mouse.move_and_click(800, 400)

        keyboard.tab()

        counter = 0
        tournament_name = ''

        same = 0
        gtd = '0'

        tables = []

        while True:
            skip = False
            time.sleep(2)
            counter += 1

            amount_of_tables = windows.get_amount_of_opened_tables()
            if amount_of_tables == 21:
                print(f'Открыто столов: {self._amount_of_opened_tables + len(availible_tables)}')
                return availible_tables, tournament_name, gtd

            for _ in range(2):
                keyboard.copy()
            table_num = do_without_error(clipboard.clipboard_get)

            if table_num in tables:
                return availible_tables, tournament_name, gtd

            if table_num in availible_tables:
                keyboard.arrow_down()
                continue

            for i in self._get_deal_files():
                if f'PS__{self._tournament_id}__T{table_num}' == '__'.join(i.split('__')[:3]):
                    print('IN')
                    skip = True
                    tables.append(table_num)
                    break
                else:
                    skip = False

            if not skip:
                if get_info.table_opened(self._tournament_id, table_num):
                    print('IN')
                    tables.append(table_num)
                    keyboard.arrow_down()
                    continue

                else:
                    try:
                        add_table.add(self._tournament_id, table_num)
                        tables.append(table_num)
                    except Exception as e:
                        print(e)
                        return availible_tables, tournament_name, gtd

            else:
                keyboard.arrow_down()
                continue

            fails = 0
            self._open_table()

            while True:
                try:
                    if fails >= 150:
                        time.sleep(2)
                        self._open_table()
                        fails = 0

                    tournament_name = self._get_tournament_name()
                    tournament_name = tournament_name.replace(',', '')
                    break

                except Exception as e:
                    fails += 1
                    print(f'Не удалось получить название стола, пробуем еще раз\nОшибка {e}')

            gtd = self._get_lobby_gtd()

            time.sleep(2)
            mouse.move_and_click(250, 50)
            time.sleep(1)

            keyboard.arrow_down()

            tables.append(table_num)
            availible_tables.append(table_num)

        return availible_tables, tournament_name, gtd

    def _get_tournament_name(self):
        got_name = False
        for _ in range(1000):
            try:
                hwnd = win32gui.GetForegroundWindow()
                table_text = win32gui.GetWindowText(hwnd)
                if get_pokerstars_version().upper() == 'ES':
                    if '|' in table_text or ', €' in table_text:
                        got_name = True
                        break
                else:
                    re.search(r'^(.*), \$(.*)K', table_text).group(1)

                    got_name = True
                    break
            except:
                continue

        if got_name:
            if get_pokerstars_version().upper() == 'ES':
                if '|' in table_text:
                    tournament_name = table_text.split(' | ')[0]
                    return self._handle_tournament_name(tournament_name)

                elif ', €' in table_text:
                    tournament_name = table_text.split(', €')[0]
                    return self._handle_tournament_name(tournament_name)

                else:
                    return 'False'
            else:
                splited_header = re.split(r', | \$', table_text)
                if len(splited_header) > 2:
                    tournament_name = ', '.join(splited_header[0:-1])
                    return self._handle_tournament_name(tournament_name)

                else:
                    tournament_name = table_text.split(', $')[0]
                    return self._handle_tournament_name(tournament_name)

        else:
            if ' - ' in table_text:
                tournament_name = table_text.split(' - ')[0]
                return self._handle_tournament_name(tournament_name)

    def _handle_tournament_name(self, tournament_name: str) -> str:
        tournament_name = tournament_name.split(' ')
        tournament_list = []

        if get_pokerstars_version().upper() == 'ES':
            for i in tournament_name:
                if i[0] in string.digits and '€' not in i[0]:
                    i = '€' + i
                tournament_list.append(i)
        else:
            for i in tournament_name:
                if i[0] in string.digits and '$' not in i[0]:
                    i = '$' + i
                tournament_list.append(i)

        return '_'.join(tournament_name)

    def _open_table(self):
        keyboard.enter()

    def _write_opened_tables(self, availible_tables, tournament_name, gtd):
        tournament_data = self._open_tournament_file()
        print(self._tournament_id)
        if gtd != '0':
            tournament_data.get(self._tournament_id).update({'availible_tables': availible_tables, 'tournament_name': tournament_name, 'gtd': gtd})
        else:
            tournament_data.get(self._tournament_id).update({'availible_tables': availible_tables, 'tournament_name': tournament_name})
        with open('tournaments_data.json', 'w') as tournament_data_json:
            json.dump(tournament_data, tournament_data_json)

    def _open_tournament_file(self) -> dict:
        with open('tournaments_data.json', 'r') as tournament_data_json:
            return json.load(tournament_data_json)

    def _get_tables_from_file(self):
        data = self._file
        print(f'data {data}')
        tournament_data = data.get(self._tournament_id)
        print(f'tournament_data {tournament_data}')
        try:
            print(f'tables {tournament_data.get('availible_tables')}')
            return tournament_data.get('availible_tables')
        except Exception:
            return None

    def _get_deal_files(self):
        files = os.listdir('deals_files')
        return files

    def _get_lobby_gtd(self):
        time.sleep(1)
        hwnd = win32gui.GetForegroundWindow()
        header = win32gui.GetWindowText(hwnd)
        if get_pokerstars_version().upper() == 'ES':
            try:
                gtd = re.search(r', (€.+?) Gtd', header).group(1)
                print(',', gtd)
            except:
                gtd = re.search(r'\| (€.+?) Gtd', header).group(1)
                print('|', gtd)
            return gtd

        else:
            splited_header = re.split(r', | \$', header)

            if len(splited_header) > 2:
                gtd = re.search(r'(\$.+?)K', splited_header[-1]).group(1)
                return gtd

            gtd = re.search(r', (\$.+?) Gtd', header).group(1)
            return gtd
