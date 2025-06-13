from ClientLauncher.MainFunctions.mouse_and_keyboard import Mouse, Keyboard
from ClientLauncher.MainFunctions.image import Image
from ClientLauncher.MainFunctions.windows import Windows

from ClientLauncher.ParseInfo.parse_header import GetType
from ClientLauncher.ParseInfo.parse_lobby import ParseLobby

from ClientLauncher.TablesController.hand_history_controller import TablesControl

from ClientLauncher.Google.Sheets.write_statistics import WriteStatistics
from ClientLauncher.Google.Sheets.get_statistics import GetStatistics

from ClientLauncher.Naming.create_file_name import CreateFileName

from ClientLauncher.extensions.main_lobby_actions import check_ok_button, click_ok_button

import win32gui
import time
import json

mouse = Mouse()
keyboard = Keyboard()
windows = Windows()
image = Image()

parse_header = GetType()

tables_control = TablesControl()

while True:
    try:
        write_stats = WriteStatistics()
        break
    except Exception as e:
        print(f'Ошибка при инициализации WriteStatistics {e}')

while True:
    try:
        get_stats = GetStatistics()
        break
    except Exception as e:
        print(f'Ошибка при инициализации GetStatistics {e}')


file_name = CreateFileName()


class TournamentActions:
    def __init__(self):
        self._tournament_x = 225
        self._tournament_y = 260

    def switch_tournaments(self, amount_of_tables, num):
        if not num or num <= 0:
            num = 0
        print(f'Попытка открыть турнир №{num}')

        if check_ok_button():
            print('Обнаружена кнопка ок')
            click_ok_button()

        y_counter = 26 * num
        mouse.move_and_click(900, 70)
        main_hwnd = win32gui.GetForegroundWindow()
        print(main_hwnd)

        amount_of_opened_tables = windows.get_amount_of_opened_tables()
        print(f'Количество открытых столов {amount_of_opened_tables}')

        write_stats.set_opened_tables(amount_of_opened_tables)

        if amount_of_opened_tables == 21:
            return num

        mouse.move_and_click(self._tournament_x, self._tournament_y + y_counter)

        tournament_info = parse_header.get_header_info(num)
        print(f'Информация из хедера {tournament_info}')

        if tournament_info is False:
            print('Просмотрены все доступные турниры')
            return 0

        file = self._get_tournament_file()

        self._write_tournament_info(tournament_info)

        print('Турнир открывается')

        self._open_tournament()

        time.sleep(3)

        tournament_hwnd = self._get_tournament_hwnd()

        print(f'HWND лобби турнира {tournament_hwnd}')
        time.sleep(3)

        lobby = ParseLobby(tournament_hwnd, amount_of_opened_tables, ''.join(tournament_info.keys()), file)
        lobby_info = lobby.get_lobby_info()

        print(f'Lobby Info {lobby_info}')

        tournament_info_for_cycle = self._get_tournament_info(str(''.join(tournament_info.keys())))
        tournament_info_for_cycle.update({'tournament_id': str(''.join(tournament_info.keys()))})

        availble_tables = lobby_info.get('availible_tables')

        print(f'Список откртытых столов в этом турнире {availble_tables}')

        for table in availble_tables:
            filename = file_name.get_file_name(tournament_info_for_cycle, table)
            self._create_empty_deals_file(filename)

        windows.close_window_by_hwnd(tournament_hwnd)
        windows.open_window_by_hwnd(main_hwnd)
        windows.open_fullscreen_window_by_hwnd(main_hwnd)

        y_counter += 26
        num += 1

        amount_of_opened_tables = windows.get_amount_of_opened_tables()
        print(f'amount of tables {amount_of_opened_tables}')

        return num

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


class LobbyActions:
    @staticmethod
    def reset_wight():
        def _open_settings():
            mouse.move_and_click(1570, 240)

        def _choose_reset_checkbox():
            mouse.move_and_click(870, 617)

        def _apply():
            mouse.move_and_click(880, 710)

        _open_settings()
        time.sleep(2)

        _choose_reset_checkbox()
        _apply()

    @staticmethod
    def close_banner():
        def _check_banner() -> bool:
            image.take_screenshot('imgs\\screenshots\\is_there_cross.png', (1560, 238, 1580, 266))
            return image.matching('imgs\\screenshots\\is_there_cross.png',
                                  'imgs\\templates\\banner_cross.png')

        mouse.move_and_click(1575, 251)
        time.sleep(1)

    @staticmethod
    def close_email_banner():
        def _check_banner() -> bool:
            image.take_screenshot('imgs\\screenshots\\is_there_cross.png', (1350, 365, 1365, 380))
            return image.matching('imgs\\screenshots\\is_there_cross.png',
                                  'imgs\\templates\\email_cross.png')

        mouse.move_and_click(1355, 370)
        time.sleep(1)

