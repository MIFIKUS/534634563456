from ClientLauncher.Google.Sheets.url import GOOGLE_SHEET_URL
from ClientLauncher.extensions.get_config_data import get_google_row, get_pokerstars_version

import gspread
import json


if get_pokerstars_version().upper() == 'ES':
    worksheet_num = 5
else:
    worksheet_num = 1


class WriteStatistics:
    def __init__(self):
        path_to_credentials = 'services_files\\google_credentials.json'
        self.gs = gspread.service_account(path_to_credentials)
        self.sh = self.gs.open_by_url(GOOGLE_SHEET_URL).get_worksheet(worksheet_num)
        self.client_row = get_google_row()

    def set_status(self, status):
        while True:
            try:
                cells = self._open_cells_file()
                status_cell = cells.get('status')

                self.sh.update(f'{status_cell}{self.client_row}', [[status]])
                break
            except Exception as e:
                print(f'Ошибка в set_status {e}')

    def set_opened_tables(self, opened_tables: int):
        while True:
            try:
                cells = self._open_cells_file()
                opened_tables_cell = cells.get('opened_tables')

                self.sh.update(f'{opened_tables_cell}{self.client_row}', [[opened_tables]])
                break
            except Exception as e:
                print(f'Ошибка в set_opened_tables {e}')

    def set_files_per_time(self, files_per_days: int, files_per_hour: int):
        while True:
            try:
                cells = self._open_cells_file()
                files_per_hour_cell = cells.get('files_for_time')
                files_per_time = files_per_days + files_per_hour

                self.sh.update(f'{files_per_hour_cell}{self.client_row}', [[files_per_time]])
                break
            except Exception as e:
                print(f'Ошибка в set_files_per_time {e}')

    def set_deals_per_time(self, deals_per_days: int, deals_per_hour: int):
        while True:
            try:
                cells = self._open_cells_file()
                deals_per_hour_cell = cells.get('deals_for_time')

                deals_per_time = deals_per_days + deals_per_hour

                self.sh.update(f'{deals_per_hour_cell}{self.client_row}', [[deals_per_time]])
                break
            except Exception as e:
                print(f'Ошибка в set_deals_per_time {e}')

    def _open_cells_file(self):
        with open('ClientLauncher\\Statistics\\statistics_cells.json') as cells_json:
            return json.load(cells_json)

