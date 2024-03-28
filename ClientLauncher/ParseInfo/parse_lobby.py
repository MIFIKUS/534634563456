from ClientLauncher.MainFunctions.image import Image
from ClientLauncher.MainFunctions.mouse_and_keyboard import Mouse, Keyboard
from ClientLauncher.MainFunctions.windows import Windows

from tkinter import Tk

import win32gui

import re
import time
import json
import os


image = Image()
mouse = Mouse()
keyboard = Keyboard()
windows = Windows()


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
        opened_tables = self._amount_of_opened_tables + len(availible_tables)
        self._write_opened_tables(availible_tables, tournament_name)
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
        mouse.move_and_click(680, 160)
        counter = 0
        tournament_name = ''

        keyboard.tab()

        while True:
            time.sleep(2)
            counter += 1
            if self._amount_of_opened_tables + len(availible_tables) == 21:
                print(f'Открыто столов: {self._amount_of_opened_tables + len(availible_tables)}')
                return availible_tables, tournament_name
            keyboard.copy()
            table_num = Tk().clipboard_get()
            if table_num in availible_tables:
                break
            skip = False
            for i in self._get_deal_files():
                print(i)
                if f'T{table_num}' in i and self._tournament_id in i:
                    print('IN')
                    keyboard.arrow_down()
                    availible_tables.append(table_num)
                    tournament_name = ''
                    skip = True
                    break
            if skip:
                continue

            else:
                self._open_table()
                time.sleep(5)

                if counter == 1:
                    tournament_name = self._get_tournament_name()
                    tournament_name = tournament_name.replace(',', '')

                windows.open_window_by_hwnd(self._hwnd)
                time.sleep(0.1)
                keyboard.arrow_down()

            availible_tables.append(table_num)

        return availible_tables, tournament_name

    def _get_tournament_name(self):
        hwnd = win32gui.GetForegroundWindow()
        table_text = win32gui.GetWindowText(hwnd)

        return re.search(r'^.*?,', table_text).group(0)

    def _open_table(self):
        keyboard.enter()

    def _write_opened_tables(self, availible_tables, tournament_name):
        tournament_data = self._open_tournament_file()
        print(self._tournament_id)
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
        files =  os.listdir('deals_files')
        return files