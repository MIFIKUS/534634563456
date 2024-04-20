from ClientLauncher.MainFunctions.mouse_and_keyboard import Mouse, Keyboard
from ClientLauncher.MainFunctions.windows import Windows

from ClientLauncher.ParseInfo.parse_header import GetType
from ClientLauncher.ParseInfo.parse_lobby import ParseLobby

from ClientLauncher.TablesController.hand_history_controller import TablesControl

from ClientLauncher.Google.Sheets.write_statistics import WriteStatistics
from ClientLauncher.Google.Sheets.get_statistics import GetStatistics

from ClientLauncher.Naming.create_file_name import CreateFileName

import win32gui
import time
import json

mouse = Mouse()
keyboard = Keyboard()
windows = Windows()

parse_header = GetType()

tables_control = TablesControl()

write_stats = WriteStatistics()
get_stats = GetStatistics()

file_name = CreateFileName()


class TournamentActions:
    def __init__(self):
        self._tournament_x = 225
        self._tournament_y = 260

    def switch_tournaments(self, amount_of_tables):
        num = 0
        y_counter = 0
        mouse.move_and_click(900, 70)
        main_hwnd = win32gui.GetForegroundWindow()
        print(main_hwnd)

        for _ in range(20):
            amount_of_opened_tables = windows.get_amount_of_opened_tables()
            write_stats.set_opened_tables(amount_of_opened_tables)

            if amount_of_opened_tables == amount_of_tables:
                return
            mouse.move_and_click(self._tournament_x, self._tournament_y + y_counter)
            tournament_info = parse_header.get_header_info(num)
            print(f'tournament_info {tournament_info}')
            file = self._get_tournament_file()
            print(f'file {file}')

            self._write_tournament_info(tournament_info)

            self._open_tournament()
            time.sleep(3)

            tournament_hwnd = self._get_tournament_hwnd()
            windows.open_fullscreen_window_by_hwnd(tournament_hwnd)
            time.sleep(3)

            lobby = ParseLobby(tournament_hwnd, amount_of_opened_tables, ''.join(tournament_info.keys()), file)

            lobby_info = lobby.get_lobby_info()

            tournament_info_for_cycle = self._get_tournament_info(str(''.join(tournament_info.keys())))
            tournament_info_for_cycle.update({'tournament_id': str(''.join(tournament_info.keys()))})

            availble_tables = lobby_info.get('availible_tables')

            for table in availble_tables:
                filename = file_name.get_file_name(tournament_info_for_cycle, table)
                self._create_empty_deals_file(filename)
            

            windows.close_window_by_hwnd(tournament_hwnd)
            windows.open_window_by_hwnd(main_hwnd)
            windows.open_fullscreen_window_by_hwnd(main_hwnd)

            y_counter += 26
            num += 1
            print(f'amount of tables {amount_of_opened_tables}')
            if amount_of_opened_tables == 21:
                return

    def _open_tournament(self):
        keyboard.enter()

    def _get_tournament_hwnd(self):
        return win32gui.GetForegroundWindow()

    def _write_tournament_info(self, info: dict):
        with open('tournaments_data.json', 'r') as tournaments_data_json:
            tournaments_data = json.load(tournaments_data_json)

        tournaments_data.update(info)

        with open('tournaments_data.json', 'w') as tournaments_data_json:
            json.dump(tournaments_data, tournaments_data_json)

    def _get_tournament_info(self, tournament_id):
        with open('tournaments_data.json') as tournaments_data_json:
            print(f'tournament_id {tournament_id}')
            return json.load(tournaments_data_json).get(tournament_id)

    def _create_empty_deals_file(self, filename):
        with open(f'deals_files\\{filename}', 'w+') as file:
            print(f'{filename} создан')

    def _get_tournament_file(self):
        with open('tournaments_data.json') as tournaments_data_json:
            return json.load(tournaments_data_json)
